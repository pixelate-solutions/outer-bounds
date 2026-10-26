# P-power: Outer Bounds Pro power tree, reference schematic data

Prepared 2026-10-07. Sources are the TI datasheets and EVM guide listed at the end; section numbers refer to those revisions:
TPS25751 SLVSH93A (Mar 2024), BQ25730 SLUSE65A (Jan 2024), BQ2573x EVM SLUUCB9A, TPS56637 SLVSEG1A, TPS62933 SLUSEA4D, LM5155 SNVSB75E, CSD17578Q3A SLPS525A, CSD18543Q3A.
Anything marked **[unverified]** could not be confirmed in a primary source and must be checked before the schematic is frozen.

---

## 0. Problems with the decided architecture (read these first)

| # | Severity | Finding | Evidence | Recommended action |
|---|---|---|---|---|
| A1 | **Blocking** | **The TPS25751D (DREF) has no external sink-FET gate drivers.** The **D** variant integrates a 20 V / 5 A / 16 mΩ bidirectional load switch (VBUS_IN → PPHV). GATE_VBUS (pin 21), GATE_VSYS (pin 20) and VSYS (pin 19) exist only on the **TPS25751S** (RSM, 32-pin 4×4 QFN), which drives external back-to-back N-FETs ("PP_EXT"). So the DREF part cannot drive the two CSD17578Q3A sink FETs. | DS §5 Tables 5-1/5-2; §8.3.3 "TPS25751D has an integrated bidirectional high voltage load switch… PPHV. TPS25751S has a high voltage gate driver… PP_EXT" | **Recommended:** keep the TPS25751DREFR and **delete the two sink FETs**. 65 W at 20 V is 3.25 A, which is within the 5 A internal switch. If external FETs are required for thermal reasons, change the part to **TPS25751SRSMR**. Its pins are in Appendix A. |
| A2 | **High** | **BQ25730 is not on the TPS25751's supported-charger list.** The list is BQ25756, BQ25756E, BQ25790, BQ25792, BQ25798, BQ25713, **BQ25731**. The BQ25731 is the same family with the same address 0x6B, but it has **no BATFET power path** and no pre-charge LDO mode. | TPS25751 DS §1; BQ25730 DS §5 Device Comparison Table | Option 1: select the BQ25731 profile in the TPS25751 Application Customization Tool and confirm on the bench that it drives the BQ25730 correctly **[unverified]**. TI E2E has said unlisted chargers "may work if registers are similar", and that only basic V/I programming per PD contract is done. Option 2: have the SoM host the charger (Section 1.3). |
| A3 | **High** | **I2Cc is single-controller.** "Multi-controller configuration is not supported." If the TPS25751 manages the charger, the SoM **cannot** be on the BQ25730 I2C bus. | TPS25751 DS §8.3.11, Table 8-4 | Either accept PD-managed charging and route the BQ25730 IBAT/PSYS/CHRG_OK/PROCHOT pins to the SoM, or use Option 2. |
| A4 | **High** | **BATDRV drives a P-channel BATFET.** BATDRV is "shorted to VSYS to turn off… goes 10 V below VSYS to turn on". The CSD17578Q3A (N-ch) cannot be used as the battery FET. | BQ25730 DS Table 6-1 | Use a −30 V P-FET. The EVM uses **AOS AON6407** (−30 V, DFN5×6). |
| A5 | **High** | **LM5155 strobe boost: no inrush or short-circuit control when VOUT ≤ VIN.** "Boost converters cannot provide current limit protection when the output voltage is close to or less than the input supply voltage." 940 µF is charged from VSYS through L and D at power-up with only parasitic limiting. | LM5155 DS §9.3.7 | Add a soft-start load switch or eFuse between VSYS and the boost input, for example a TI TPS2595x/TPS25947-class eFuse with dV/dt and ILIM **[part not verified]**. The eFuse's current limit also gives a much more accurate "10 W" input limit than the LM5155 peak limit (±15 %, see Section 5.4). |
| A6 | **Medium** | **LM5155 with the 10 µH inductor at high duty cycle.** At 12 V → 38 V, D ≈ 0.69. With fixed slope compensation only, subharmonic stability needs fSW ≥ ~3 MHz, which is out of range. The baseline below works at **~2 MHz with RSL = 1 kΩ**. A **22 µH SRP7028A-220M at 1 MHz** (same footprint) gives the same RS and RSL with half the switching loss. | LM5155 DS §9.3.6 Eq. 8/9 | Baseline keeps the decided 10 µH. Option B is listed in Section 5. |
| A7 | **Medium** | **BQ25730 has no TS/thermistor pin.** Charge temperature qualification (JEITA) must come from the smart pack (its protector FETs) or from host firmware. | BQ25730 DS Table 6-1 (no TS pin) | Confirm that the pack's gauge/protector enforces charge temperature limits. |
| A8 | **Medium** | **TPS56637 is D-CAP3 with a maximum of 100 µF effective COUT.** If the SoM module has large bulk capacitance on VPH_PWR, the loop may go unstable. | TPS56637 DS §8.2.2.2 Table 4 | Check the SoM's VPH_PWR input capacitance **[unverified]**. |

---

## 1. TPS25751DREFR: USB-C PD sink controller (WQFN-38, 4×6 mm, "REF")

Datasheet: https://www.ti.com/lit/ds/symlink/tps25751.pdf (SLVSH93A)

### 1.1 Pin list (DREF, Fig. 5-1, Table 5-1; pads 39/40 from Fig. 9-26)

| Pin | Name | Type | Connection in Outer Bounds Pro |
|---|---|---|---|
| 1 | LDO_3V3 | O | 10 µF to GND. Pull-up rail for the I2Cc bus, ADCIN straps and EEPROM VCC. In dead battery it can supply ≤18 mA. |
| 2 | ADCIN1 | I | Strap (Section 1.3) |
| 3 | ADCIN2 | I | Strap (Section 1.3) |
| 4 | LDO_1V5 | O | 10 µF to GND (cannot supply external loads) |
| 5 | GPIO0 | GPIO | Spare. Tie to GND if unused, or map per the Web Tool. |
| 6 | GPIO1 | GPIO | Same as GPIO0 |
| 7 | GPIO2 | GPIO | Same as GPIO0 |
| 8 | I2Ct_SDA | I/O | To SoM I2C (target port). Pull-up to SoM rail (VIH 1.3 V, so 1.8 V or 3.3 V both work). |
| 9 | I2Ct_SCL | I | To SoM I2C |
| 10 | I2Ct_IRQ (GPIO10) | O | To SoM GPIO. 10 kΩ pull-up. |
| 11, 12, 14, 31 | GND | — | Ground plane |
| 13 | GPIO11 | O | Spare. Tie to GND if unused. |
| 15, 30 | DRAIN | — | Internal PPHV FET drain. Connect to the DRAIN pad only. **Not GND.** |
| 16 | I2Cc_SDA | I/O | To BQ25730 SDA and EEPROM SDA. 2.2 kΩ to LDO_3V3. |
| 17 | I2Cc_SCL | O | To BQ25730 SCL and EEPROM SCL. 2.2 kΩ to LDO_3V3. |
| 18 | I2Cc_IRQ (GPIO12) | I | 10 kΩ to LDO_3V3. **Do not tie to GND.** |
| 19 | GPIO3 | GPIO | Spare |
| 20, 21, 22 | PPHV | I/O | Sink output, routed to the BQ25730 input node (before RAC) |
| 23, 24, 25 | VBUS_IN | I/O | Type-C VBUS (5–20 V) |
| 26 | GPIO4/USB_P/LD1 | GPIO | D+ for BC1.2 or liquid detect. Otherwise GND. |
| 27 | GPIO5/USB_N/LD2 | GPIO | D− for BC1.2 or liquid detect. Otherwise GND. |
| 28 | CC1 | I/O | Type-C CC1 |
| 29 | CC2 | I/O | Type-C CC2 |
| 32, 33 | VBUS | O | Also connects to Type-C VBUS (5 V source path output and LDO input) |
| 34, 35 | PP5V | I | +5 V system rail (see note) |
| 36 | GPIO7 | GPIO | Spare |
| 37 | GPIO6 | GPIO | Spare |
| 38 | VIN_3V3 | I | +3V3 (from TPS62933) |
| 39 | GND_PAD | — | GND |
| 40 | DRAIN_PAD | — | Isolated copper pour with thermal vias to an isolated bottom-side pour. **Must not touch GND** (DS §9.4.1.2.2.6). |

**Sink-FET gate-drive pin names (requested confirmation):** none exist on the DREF package. On the TPS25751S (RSM) they are **GATE_VSYS = pin 20**, **GATE_VBUS = pin 21** and **VSYS (RCP sense) = pin 19**. The DS requires series gate resistance ≤3 Ω (§8.3.3.3).

### 1.2 Components

| Ref role | Value | Rating / size | MPN (suggested) | Note / source |
|---|---|---|---|---|
| C_VIN3V3 | 10 µF | X5R/X7R ≥6.3 V (use 10 V), 0603 | GRM188R61A106KE69 **[MPN unverified]** | DS §6.4: 5 µF min, 10 µF nominal |
| C_LDO3V3 | 10 µF | ≥6.3 V, 0603 | same | §6.4: 5–25 µF |
| C_LDO1V5 | 10 µF | ≥4 V, 0603 | same | §6.4: 4.5–12 µF |
| C_VBUS (pins 32/33) | 4.7 µF | ≥25 V (use 35 V), 0805 | — | §6.4: 1–10 µF. Use the high end if fast sink disable is configured. |
| C_PPHV | 22 µF near IC, plus the charger input caps | 35 V, 1206 | — | §6.4: 47 µF typ, **100 µF max total on PPHV** (USB PD cSnkBulkPd). Count the BQ25730 input caps (Section 2) in this budget. |
| C_PP5V | 10 µF | ≥10 V, 0805 | — | §6.4 note 2: keep ≥10 µF at PP5V. The 120 µF minimum is the cSrcBulkShared *source* requirement. Configure sink-only in the Web Tool. Behaviour of PP5V in a sink-only design is **[unverified]**. Default: tie to +5 V. |
| C_CC1, C_CC2 | 390 pF | C0G, 50 V, 0402 | — | §6.4: CCCy 200–480 pF **total** including connector and ESD capacitance |
| C_conn (×4) | 10 nF | 50 V X7R, 0402 | — | At the connector VBUS pins (Fig. 9-26 C2–C5) |
| D_TVS | 22 V flat-clamp TVS | — | **TVS2200DRVR** (TI) | Fig. 9-26 U2, placed at the connector |
| R_I2Cc SDA/SCL | 2.2 kΩ | 1 %, 0402 | — | To LDO_3V3. Fig. 9-26 uses 2.2 kΩ for SDA/SCL and 10 kΩ for IRQ. |
| R_I2Cc_IRQ, R_I2Ct_IRQ | 10 kΩ | 0402 | — | IRQ pull-ups |
| R_ADCIN1, R_ADCIN2 | 0 Ω straps (see 1.3) | — | — | Direct ties, so no divider is needed |
| U_EEPROM | 512 kbit I2C EEPROM, address 0x50 | VCC = LDO_3V3 | 24LC512 / M24512 / CAT24C512 **[any ≥36 kB part]** | §8.3.11: "EEPROM must be at least 36 kilo-bytes", 7-bit address 0x50, must not be shared |
| Q_sink ×2 | **DNP / remove** | — | (CSD17578Q3A) | Not drivable by DREF (finding A1) |

### 1.3 Configuration

**ADCIN straps (DS §8.3.6 Table 8-2, §8.4.1 Table 8-6):**

| Mode | ADCIN1 | ADCIN2 | I2Ct address | When to use |
|---|---|---|---|---|
| **Recommended: SafeMode, index #1** | tie to **LDO_3V3** (decode 7) | tie to **GND** (decode 0) | **0x20** (index #1: 0100 000x) | The patch loads from the I2Cc EEPROM and the TPS25751 then manages the charger. TI marks this mode as recommended "when the application loads the patch from EEPROM" and "when the PD controller manages the battery charger". |
| Alternative: AlwaysEnableSink, index #1 | tie to LDO_3V3 (7) | tie to **LDO_1V5** (decode 5) | 0x20 | The SoM acts as embedded controller and hosts the BQ25730 on its own I2C bus (finding A2/A3 Option 2). |

Divider decode thresholds, in case resistors are ever used instead of ties: DIV = RDOWN/(RUP+RDOWN). Targets are 0.0114 / 0.0475 / 0.1074 / 0.1899 / 0.3022 / 0.5368 / 0.8062 / 0.9530 for codes 0–7 (Table 8-2). Code 0 is a GND tie, code 5 is a LDO_1V5 tie, code 7 is a LDO_3V3 tie.

**I2Cc to the BQ25730:** I2Cc_SDA (pin 16) to BQ SDA (pin 12), and I2Cc_SCL (pin 17) to BQ SCL (pin 13). Pull-ups go to LDO_3V3 (Table 8-4: "Use the LDO_3V3 pin as the pullup voltage"). The BQ25730 is at 0x6B and the EEPROM at 0x50. The BQ25730 has no INT pin, so I2Cc_IRQ stays pulled up. Charger-related GPIO assignments (for example CHRG_OK into a TPS25751 GPIO) are set by the Application Customization Tool's charger profile **[unverified; check the tool]**.

**Dead-battery path:** with VIN_3V3 = 0, the internal VBUS LDO powers the core. The TPS25751 loads the patch from the EEPROM, closes PPHV, and VBUS reaches the BQ25730. The BQ25730 REGN comes up and the charger regulates VSYS ≥ VSYS_MIN (12.3 V), which brings up the bucks.

**Web Tool settings:** sink-only, PDOs 5 V/3 A, 9 V/3 A, 15 V/3 A, 20 V/3.25 A (65 W). Charger = BQ25731 profile (see A2). Program 4S, ChargeVoltage 16.8 V and ChargeCurrent **2.944 A** (= 23 × 128 mA LSB at 5 mΩ, just under the 3 A pack limit). IIN_HOST follows the contract.

---

## 2. BQ25730RSNR: 1–5S buck-boost NVDC charger (WQFN-32, 4×4 mm, RSN)

Datasheet: https://www.ti.com/lit/ds/symlink/bq25730.pdf (SLUSE65A). EVM: https://www.ti.com/lit/ug/sluucb9a/sluucb9a.pdf

### 2.1 Pin list (Fig. 6-1, Table 6-1)

| Pin | Name | Pin | Name |
|---|---|---|---|
| 1 | VBUS | 17 | COMP2 |
| 2 | ACN | 18 | CELL_BATPRESZ |
| 3 | ACP | 19 | SRN |
| 4 | CHRG_OK | 20 | SRP |
| 5 | OTG/VAP/FRS | 21 | BATDRV |
| 6 | ILIM_HIZ | 22 | VSYS |
| 7 | VDDA | 23 | SW2 |
| 8 | IADPT | 24 | HIDRV2 |
| 9 | IBAT | 25 | BTST2 |
| 10 | PSYS | 26 | LODRV2 |
| 11 | PROCHOT | 27 | PGND |
| 12 | SDA | 28 | REGN |
| 13 | SCL | 29 | LODRV1 |
| 14 | CMPIN | 30 | BTST1 |
| 15 | CMPOUT | 31 | HIDRV1 |
| 16 | COMP1 | 32 | SW1 |
| EP | Thermal pad | | Connect to PGND with vias |

### 2.2 Operating point

- **400 kHz, 4.7 µH.** This is the POR default (PWM_FREQ = 1b), so it works without host writes in PD-managed mode. Table 8-4/8-5 give the matching values.
- Sense resistors: **RAC = RSR = 5 mΩ**, the POR default (RSNS_RAC = RSNS_RSR = 1b, §8.3.5). The EVM uses the same values. 10 mΩ is more accurate at 3 A but requires a write of RSNS_x = 0 after every POR, which the TPS25751 profile may not do **[unverified]**.
- Worst-case inductor current: buck from 20 V to VSYS = 12.3 V at 62 W out gives IL,DC = 5.04 A. Ripple (Eq. 3) is 2.52 A pp, so **IL,pk ≈ 6.3 A**. In boost from 5 V to 16.8 V, ripple is 1.87 A pp and IL,pk ≈ 3.9 A. Specify **Isat ≥ 8 A, Irms ≥ 6 A**.

### 2.3 Components

| Ref role | Value | Rating / size | MPN | Note / source |
|---|---|---|---|---|
| Q1 (buck HS), Q2 (buck LS), Q3 (boost LS), Q4 (boost HS) | N-FET 30 V, 6.3 mΩ | SON3.3×3.3 | **CSD17578Q3A** ×4 | §9.2.2.6: "30 V or higher… for 19–20 V input". 6 V gate drive. Q1 HIDRV1/SW1, Q2 LODRV1, Q3 LODRV2, Q4 HIDRV2/SW2. |
| Q5 BATFET | P-FET −30 V | DFN5×6 | **AON6407** (AOS) | EVM Q5. Must be P-channel (finding A4). |
| L1 | **4.7 µH**, Isat 13 A, 9 mΩ | 10×10×4 mm | **Chilisin BMQADY1010404R7MA1** | EVM L1. Smaller alternative: Coilcraft XAL7070-472ME **[ratings unverified]**. |
| RAC (input sense) | 5 mΩ, 1 % | 1 W, 1206 | **Vishay WSLP12065L000FEA** | EVM R1 |
| RSR (charge sense) | 5 mΩ, 1 % | 1 W, 1206 | WSLP12065L000FEA | EVM R2 |
| RACP, RACN | 4.99 Ω, 1 % | 0603 | CRCW06034R99FKEA | §9.2.2.2 Fig. 9-3 |
| CACP, CACN | 33 nF | 50 V X7R, 0603 | GRM188R71H333KA61D | to PGND, Fig. 9-3 |
| CDIFF (ACP–ACN) | 10 nF | 50 V, 0603 | C0603C103J5RACTU | "10 nF for 400 kHz" (§9.2.2.2) |
| C after RAC (Q1 drain) | 10 nF + 1 nF | 50 V, 0603 / 0402 C0G | C0603C103J5RACTU + C1005NP01H102J050BA | §9.2.2.4: limit to 10 nF + 1 nF after RAC |
| CIN (before RAC, on PPHV) | 6 × 10 µF | 35 V X5R, 0805 | GRM21BR6YA106KE43L | §9.1 / EVM. Counts toward the ≤100 µF PPHV budget: about 82 µF nominal with the 22 µF at the TPS25751, roughly 35 µF effective at 20 V. |
| R_VBUS / C_VBUS (pin 1 filter) | 1 Ω / 0.47 µF | 0805 / 50 V 0805 | CRCW08051R00JNEA / C2012X7R1H474K125AB | Table 6-1: "1 Ω and 0.47 µF (minimum)". EVM R13/C25. |
| C_BTST1, C_BTST2 | 47 nF | 25 V X7R, 0603 | GRM188R71E473KA01D | Table 6-1: 0.047 µF (bootstrap diode is internal) |
| C_REGN | 2.2 µF | 35 V X5R, 0603 | GRM188R6YA225KA12D | Table 6-1: 2.2–3.3 µF. EVM C30. |
| R_VDDA / C_VDDA | 10 Ω / 1 µF | 0603 / 35 V X7R 0603 | CRCW060310R0JNEA / CGA3E1X7R1V105K080AC | Table 6-1: 10 Ω from REGN to VDDA, 1 µF |
| C_VSYS (at Q3/Q4) | 7 × 10 µF | 25 V min (use 35 V X5R), 0603/0805 | GRM21BR6YA106KE43L | §9.2.2.5, Table 9-1 for 65 W |
| C_VSYS bulk | 2 × 33 µF (≥2 × 22 µF required) | 35 V Ta-polymer, 7343 | Kemet T521D336M035ATE065 | Table 9-1 asks for 2 × 22 µF POSCAP. EVM uses T521D. The total effective VSYS capacitance must be ≥50 µF, and the buck input caps count toward it. |
| C_BAT (after RSR) | ≥2 × 10 µF | 35 V, 0805 | GRM21BR6YA106KE43L | §9.2.2.5: ≥20 µF after the charge sense resistor |
| R_SRP, R_SRN | 10 Ω | 1206 0.25 W | ERJ-8ENF10R0V | Table 6-1 / EVM R10, R38 |
| C_SRP–SRN | 0.1 µF | 50 V X7R, 0603 | CGA3E2X7R1H104K080AA | Table 6-1 |
| R_IADPT | **191 kΩ ±1 %** (≤±3 % required) | 0603 | CRCW0603191KFKEA | Table 8-4: 4.7 µH at 400 kHz uses 191 kΩ or 187 kΩ |
| C_IADPT | 100 pF | C0G, 0603 | C0603C101J5GAC | ≤100 pF |
| C_IBAT | 100 pF | C0G, 0603 | C0603C101J5GAC | ≤100 pF. Route IBAT to a SoM ADC for battery current telemetry. |
| R_PSYS / C_PSYS | **30.1 kΩ** / 100 pF | 0603 | CRCW060330K1FKEA | KPSYS default 1 µA/W gives 30.1 mV/W: 1.96 V at 65 W and 3.0 V at 100 W, below the 3.3 V clamp. Enable with PSYS_CONFIG = 00b (POR = 11b, disabled). |
| COMP1: R1 / C11 / C12 | **40.2 kΩ / 4.7 nF / 33 pF** | 0402 | CRCW040240K2FKED, GRM155R71H472KA01D, GRM1555C1H330JA01D | Table 8-5, 400 kHz with 4.7 µH. Do not change. |
| COMP2: R2 / C21 / C22 | **15.0 kΩ / 680 pF / 15 pF** | 0402 | CRCW040215K0FKED, GRM1555C1H681JA01D, GRM1555C1H150JA01D | Table 8-5 |
| ILIM_HIZ divider (VDDA → pin → GND) | **Rtop 300 kΩ / Rbot 113 kΩ** | 1 %, 0603 | — | See 2.4. Optional N-FET from SoM to GND forces HIZ (pin <0.4 V). |
| CELL_BATPRESZ divider (VDDA → pin → GND) | **Rtop 100 kΩ / Rbot 301 kΩ** | 1 %, 0603 | — | See 2.4. **No capacitor allowed on this pin.** |
| R_CHRG_OK | 10 kΩ | 0402 | — | Pull-up to +3V3, then to SoM GPIO |
| R_PROCHOT | 10 kΩ | 0402 | — | Pull-up to +3V3 (abs max 5.5 V), then to SoM GPIO/IRQ |
| SDA/SCL pull-ups | shared with TPS25751 I2Cc (2.2 kΩ to LDO_3V3) | — | — | Table 6-1 suggests 10 kΩ. One set per bus is enough. |
| CMPIN / CMPOUT | CMPIN to GND, CMPOUT floating | — | — | Comparator unused (Table 6-1) |
| OTG/VAP/FRS | 100 kΩ to GND | — | — | OTG not used |

### 2.4 Pin-strap calculations

- **ILIM_HIZ** (Table 6-1): V(ILIM_HIZ) = 1 V + 40 × IDPM × RAC.
  - Target IDPM = 3.2 A (TI's 65 W example value, §9.2.1) with RAC = 5 mΩ gives V = 1 + 40 × 3.2 × 0.005 = **1.640 V**.
  - VDDA ≈ REGN = 6.0 V (5.7–6.3 V), so the ratio is 1.64/6.0 = 0.2733. 300 k/113 k gives 0.2736, so **V = 1.642 V and IDPM = 3.21 A** nominal (2.80–3.62 A across REGN tolerance).
  - EN_EXTILIM = 1 at POR, so the effective limit is min(pin, IIN_HOST). The pin acts as a hardware ceiling and the TPS25751 sets lower limits for 5 V and 9 V contracts.
- **CELL_BATPRESZ** (§8.3.7 Table 8-2, EC table): 4S requires 75 % of VDDA (window 68.4–81.5 %). 301 k/(100 k + 301 k) = **75.06 %**. This gives ChargeVoltage default 16.8 V, VSYS_MIN 12.3 V and SYSOVP 19.5 V. Battery removal is detected below 15 %. If the pack connector has a presence pin, wire it to pull this node low on removal.
- **IADPT** (§8.3.11): 191 kΩ selects 4.7 µH at 400 kHz. The charger reads it before the converter starts.

---

## 3. TPS56637RPAR ×2: 3.8 V / 6 A (VPH_PWR) and 5.0 V / 3 A (VQFN-HR 10, 3×3 mm, RPA)

Datasheet: https://www.ti.com/lit/ds/symlink/tps56637.pdf (SLVSEG1A). fSW is fixed at 500 kHz. Control is D-CAP3 with an internal 2 ms soft start, so **no soft-start capacitor and no RT**.

### 3.1 Pin list

| Pin | Name | Function |
|---|---|---|
| 1 | EN | Enable / UVLO divider (floating = enabled, internal 1 µA pull-up) |
| 2 | FB | Feedback, VREF = 0.6 V |
| 3 | AGND | Analog GND, single-point tie to PGND |
| 4 | PG | Open-drain power good |
| 5 | NC | Leave floating |
| 6 | SW | Switch node |
| 7 | BOOT | 0.1 µF to SW |
| 8 | VIN | Input |
| 9 | PGND | Power GND |
| 10 | MODE | GND (≤10 kΩ) = Eco-mode; floating (≥500 kΩ) = FCCM. Latched at start-up. |

### 3.2 FB divider (Eq. 5: VOUT = 0.6 V × (1 + R6/R7), R7 = 10.0 kΩ)

- **3.8 V:** R6 = 10 k × (3.8/0.6 − 1) = 53.33 kΩ. Use **53.6 kΩ**, giving VOUT = 0.6 × (1 + 5.36) = **3.816 V** (+0.4 %). An E192 53.3 kΩ part gives 3.798 V.
- **5.0 V:** R6 = 73.33 kΩ. Use **73.2 kΩ**, giving **4.992 V**. This matches DS Table 4.

### 3.3 EN UVLO (Eq. 2/3; Ip = 1 µA, Ih = 4 µA, VEN rising = 1.18 V, falling = 1.12 V)

Target start at 10.5 V and stop at 9.5 V (below VSYS_MIN of 12.3 V, so the rails stay up while on battery):
R1 = (VSTART × VENf/VENr − VSTOP) / (Ip(1 − VENf/VENr) + Ih) = **115 kΩ**, and R2 = R1 × VENf / (VSTOP − VENf + R1(Ip + Ih)) = **14.3 kΩ**.
Check: start 10.55 V, stop 9.55 V. VEN at VSYS = 19.5 V (SYSOVP) is 2.2 V, below the 5.5 V maximum. The SoM or sequencer can also pull EN low through an open-drain to sequence VPH_PWR.

### 3.4 Inductor (Eq. 7–9, VIN,max = 16.8 V, fSW = 500 kHz)

- 3.8 V / 6 A with L = 3.3 µH: ΔI = 1.78 A pp, IPK = 6.89 A, IRMS = 6.02 A.
- 5 V / 3 A with L = 3.3 µH: ΔI = 2.13 A pp, IPK = 4.06 A, IRMS = 3.06 A.

### 3.5 Components (per instance; "3.8" / "5.0" where they differ)

| Ref role | Value | Rating / size | MPN | Note / source |
|---|---|---|---|---|
| CIN | 3 × 10 µF | 50 V X7R, 1206 | TDK CGA5L1X7R1H106K160AC | DS §8.2.2.3 (>10 µF). At 3.8 V / 6 A from 12 V, ICIN,rms ≈ 2.8 A, hence three parts. MPN from TPS62933 DS §10.2.2.9. |
| CIN HF | 0.1 µF | 50 V X7R, 0402 | — | §8.2.2.3 C3 |
| R6 (FB top) | 3.8: **53.6 kΩ** / 5.0: **73.2 kΩ** | 1 %, 0402 | — | Eq. 5 |
| R7 (FB bottom) | 10.0 kΩ | 1 %, 0402 | — | Table 4 |
| R5 (loop injection) | 0 Ω (49.9 Ω on proto) | 0402 | — | Optional, Fig. 17 |
| C9 + R8 (feed-forward) | 100–220 pF + 20.0 kΩ in series, across R6 | C0G | — | Table 4. Optional, tune on bench. |
| L1 | **3.3 µH**, Isat 10.5 A, Irms 9.7 A | 8.6×8.6 mm | **Vishay IHLP3232DZER3R3M11** | Table 4 (5 V row is used for 3.8 V per note 1). DS example part. Reuse it on the 5 V rail. |
| COUT | 3.8: 2 × 22 µF (≈34 µF eff.) / 5.0: 2 × 22 µF (31 µF eff. at 5 V) | 25 V X7R, 1210 | **Murata GRM32ER71E226KE15L** | Table 4: 20–100 µF effective. **100 µF max total effective including SoM-side caps** (A8). |
| C_BOOT | 0.1 µF | ≥10 V X7R, 0402/0603 | — | §8.2.2.4 |
| R_BOOT | 0 Ω | 0402 | — | Fig. 17 R4 (optional slew control) |
| EN R1 / R2 | **115 kΩ / 14.3 kΩ** | 1 %, 0402 | — | Section 3.3 |
| MODE | 0 Ω to AGND (Eco-mode) | — | — | Eco-mode for battery life. Leave floating for FCCM if ripple or EMI is critical. |
| R_PG | 100 kΩ to +3V3 | 0402 | — | Fig. 17 R9 |

---

## 4. TPS62933DRLR: 3.3 V / 2.5 A (SOT-583, DRL-8)

Datasheet: https://www.ti.com/lit/ds/symlink/tps62933.pdf (SLUSEA4D). The TPS62933 is a 3 A device with peak-current mode, VREF = 0.8 V, and an SS pin. **It has no PG pin.** If PG is needed, use the TPS62933PDRLR (pin 7 = PG, fixed 2 ms SS).

### 4.1 Pin list (Fig. 7-1, Table 7-1)

| Pin | Name | Function |
|---|---|---|
| 1 | RT | Floating (>280 kΩ) = 500 kHz; GND = 1.2 MHz; 8.9–111 kΩ = 200–2200 kHz |
| 2 | EN | Enable / UVLO (internal pull-up, floating = on) |
| 3 | VIN | Input |
| 4 | GND | Ground |
| 5 | SW | Switch node |
| 6 | BST | 100 nF to SW |
| 7 | SS | Soft-start capacitor, ≥6.8 nF, **do not float** |
| 8 | FB | Feedback, 0.8 V |

### 4.2 Calculations

- **FB** (Eq. 14): RTOP = (VOUT − 0.8)/0.8 × RDOWN. With RDOWN = 10.0 kΩ, RTOP = 31.25 kΩ. Use **31.2 kΩ (E192, 0.5 %)**, giving **3.296 V**. An all-E96 alternative is 51.1 k/16.2 k, giving 3.324 V. TI's Table 10-2 lists 31.3 k/10.0 k.
- **fSW:** RT floating gives **500 kHz** (Table 9-1).
- **SS** (§9.3.7): CSS = tSS × ISS / VREF, with ISS = 5.5 µA. For 2 ms that is 13.75 nF. Use **15 nF**, giving 2.18 ms.
- **EN UVLO** (Eq. 3/4; Ip = 0.7 µA, Ih = 1.4 µA, VEN rising = 1.21 V, falling = 1.17 V): start 10.5 V and stop 9.5 V give R1 = **464 kΩ** and R2 = **57.6 kΩ**. Check: 10.63 V / 9.62 V, and VEN at 19.5 V is 2.26 V.
- **Inductor** (Eq. 15–18, VIN,max = 16.8 V): with 4.7 µH, ΔI = 1.13 A (K = 0.45) and IPK = 3.06 A. With **6.8 µH, ΔI = 0.78 A (K = 0.31), IPK = 2.89 A and IRMS = 2.51 A**. The datasheet asks for Isat ≥ IHS_LIMIT max = **5.8 A**. 6.8 µH is chosen because a part meeting that rating is published in the TI datasheet.

### 4.3 Components

| Ref role | Value | Rating / size | MPN | Note / source |
|---|---|---|---|---|
| CIN | 2 × 10 µF | 50 V X7R, 1206 | **TDK CGA5L1X7R1H106K160AC** | §10.2.2.9 |
| CIN HF | 100 nF | 50 V, 0402 | — | §10.2.2.9 |
| L1 | **6.8 µH**, Isat 10 A, Irms 6.5 A | WE-XHMI 6030 | **Würth 74439346068** | §10.2.2.7 example part. A 4.7 µH 74439346047 is also allowed per Table 10-2, but its Isat ≥ 5.8 A is **[unverified]**. |
| COUT | 3 × 22 µF (≈40 µF eff.) | 16 V X7R/X5R, 1206 | C3216X5R1V226M160AC (35 V, used in the DS) | Table 10-2: 40 µF typical, 15 µF minimum effective at 3.3 V / 500 kHz |
| COUT HF | 100 nF | 0402 | — | Fig. 10-1 C8 |
| RTOP / RDOWN | **31.2 kΩ / 10.0 kΩ** | 0.5 %, 0402 | — | Section 4.2 |
| CFF | DNP (10 pF footprint) | C0G 0402 | — | Fig. 10-1 C9, §10.2.2.10 |
| C_BST | 100 nF | ≥16 V X7R, 0402 | — | §10.2.2.5 |
| R_BST | 0 Ω (≤10 Ω allowed) | 0402 | — | §10.2.2.5 |
| C_SS | **15 nF** | X7R, 0402 | — | Section 4.2 |
| RT | DNP (floating) | — | — | 500 kHz |
| EN R1 / R2 | **464 kΩ / 57.6 kΩ** | 1 %, 0402 | — | Section 4.2 |

The +3V3 rail also feeds TPS25751 VIN_3V3 and the I2C, CHRG_OK and PROCHOT pull-ups.

---

## 5. LM5155DSSR: 34 V strobe-bus boost (WSON-12, DSS)

Datasheet: https://www.ti.com/lit/ds/symlink/lm5155.pdf (SNVSB75E). Use the **LM5155** (not the LM51551). The LM51551 adds hiccup after 64 current-limit cycles, which would interrupt the continuous current-limited recharge of the strobe capacitors.

### 5.1 Pin list (Fig. 7-1, Table 7-1)

| Pin | Name | Connection |
|---|---|---|
| 1 | BIAS | VSYS (after the inrush eFuse, A5). 0.1 µF to PGND. |
| 2 | VCC | 6.85 V regulator output. 2.2 µF to PGND. |
| 3 | GATE | To CSD18543Q3A gate through RG |
| 4 | PGND | To the RS ground end |
| 5 | CS | To the RS high side through RSL and RF |
| 6 | COMP | RCOMP + CCOMP to AGND, plus CHF |
| 7 | AGND | Analog ground |
| 8 | FB | Divider plus DAC injection, VREF = 1.0 V |
| 9 | SS | CSS to AGND |
| 10 | RT | RT to AGND |
| 11 | PGOOD | Open-drain, ≥10 kΩ pull-up to +3V3 (must stay ≤ VBIAS + 0.3 V) |
| 12 | UVLO/EN/SYNC | Divider from BIAS. SoM open-drain to GND disables the strobe bus. Do not float. |
| EP | — | AGND plus ground pour |

### 5.2 Operating point

- VIN 12–16.8 V, VOUT 30–38 V, input current limit sized for **10 W at 12 V**: IIN = 10/12 = **0.833 A average**.
- **Baseline (decided 10 µH):** fSW ≈ **2.0 MHz**. RT (Eq. 5) = 2.21×10¹⁰/fRT − 955 = 10.10 kΩ. Use **10.2 kΩ**, giving 1.98 MHz. DMAX at 2.2 MHz is ≥80 % (spec), against D ≈ 0.69–0.72 needed at 12 V → 38 V, so there is margin. tON(min) = 50 ns, which is fine.
- **Option B (recommended if the inductor value may change):** **SRP7028A-220M** (22 µH, Isat 3.5 A, Irms 2.0 A, DCR 190 mΩ max, same 7.3×6.6 mm footprint) at **1.0 MHz with RT = 21.0 kΩ** (1.007 MHz). RS, RSL, COMP and the divider are unchanged, and switching loss is about half.
- Inductor check for the decided part, SRP7028A-100M: 10 µH, **Isat 6 A, Irms 3.5 A, DCR 85 mΩ max** (Bourns datasheet). IPK ≈ 1.0–1.15 A, so it has ample margin.

### 5.3 Slope compensation (Eq. 6–9)

Sensed down-slope = RS × (VLOAD + VF − VSUPPLY)/LM. At 12 V → 38.5 V with RS = 82 mΩ and 10 µH, that is 0.217 V/µs.
Eq. 8 requires 0.5 × 0.217 × 1.2 = 0.130 V/µs ≤ (40 mV + 30 µA × RSL) × fSW.
- Fixed slope only at 2 MHz gives 0.080 V/µs, which **fails**.
- With **RSL = 1.0 kΩ**: (40 + 30) mV × 1.98 MHz = 0.139 V/µs, which **passes** across all corners. RSL must be ≤2 kΩ.

Caveat: the current-limit comparator sees only the RSL ramp (Fig. 9-19). In sustained current limit at VOUT > 34 V with VIN = 12 V, the RSL ramp is 28–36 % of the down-slope, so period-doubling can appear during recharge. It only lowers the average current, which is the safe direction. Option B (22 µH) gives the same result. RSL = 2 kΩ would cure it, but at the cost of current-limit accuracy.

### 5.4 Current-limit sense resistor (Eq. 10/11)

IPEAK-CL = (VCLTH − 30 µA × RSL × D)/RS, with VCLTH = 100 mV (93–107 mV).

Design point (worst case for average current is the lowest VOUT, where ripple is smallest): VIN = 12 V, VOUT = 30 V, VF ≈ 0.5 V.
- D = 1 − 12/30.5 = 0.607.
- ΔIL = VIN × D/(L × fSW) = 12 × 0.607/(10 µH × 2.0 MHz) = 0.36 A pp.
- IPK = IIN + ΔIL/2 = 0.833 + 0.18 = **1.013 A**.
- RS = (0.100 − 30 µA × 1 kΩ × 0.607)/1.013 = 0.0817/1.013 = **80.7 mΩ**. Use **82 mΩ**.

Result with 82 mΩ: IPK = 0.996 A and IIN ≈ 0.82 A, which is **9.8 W at 12 V** (9.3 W at 38 V out). Because this is a current limit, input power rises with VIN: about 13.4–14.9 W at 16.8 V. All parts must be rated for that.

Tolerance from VCLTH ±7 % and ISLOPE ±25 % is IPK 0.86–1.14 A, so **about 8.2–11.6 W at 12 V**. If ±5 % is required, use the eFuse limit from A5.

Dissipation is D × IIN² × RS ≈ 35 mW, so a 0805/1206 part is enough.

### 5.5 FB divider with DAC trim (Eq. 14 extended)

VOUT = VREF × (1 + RFBT/RFBB) + RFBT × (VREF − VDAC)/RINJ, with VREF = 1.0 V. Design for 38 V at VDAC = 0 and 30 V at VDAC = full scale.

For a 0–3.3 V DAC:
- RFBT/RINJ = 8 V/3.3 V = 2.424, and RFBT/RFBB = 37 − 2.424 = 34.58.
- With **RFBT = 200 kΩ**: **RFBB = 5.76 kΩ** and **RINJ = 82.5 kΩ**.
- Result: VDAC = 0 gives **38.15 V**, 1.71 V gives 34.0 V, 3.3 V gives **30.15 V**. If the DAC is Hi-Z or unpowered, the bus goes to **35.7 V**.

For a 0–2.5 V DAC: RFBB = 5.90 kΩ and RINJ = 61.9 kΩ, giving 38.13 V and 30.05 V.

Notes:
- VDAC = 0 V gives the **maximum** voltage. Make sure a DAC reset state does not exceed the strobe/LED rating.
- OVP trips at 110 % of the FB reference, which tracks the setpoint.
- FB abs max is 3.8 V.
- Optional: split RINJ into 2 × 41.2 kΩ with 1 µF to GND at the midpoint to slew-limit DAC steps.

### 5.6 Compensation (peak current mode, Type II; GCOMP = 0.142 from Fig. 9-17; gm = 2 mA/V)

This is an engineering estimate **[verify with the LM5155 Quick-Start Calculator and a Bode measurement]**.

- AC feedback ratio β = (RFBB‖RINJ)/(RFBT + RFBB‖RINJ) = 5.384 k/205.4 k = 0.0262.
- Above the load pole, the control-to-output gain is about (GCOMP/RS) × (1 − D)/(2π f COUT), with COUT = 940 µF.
- RCOMP = 2π fC COUT RS/(β gm GCOMP (1 − D)). For fC = 2 kHz at the highest-gain corner (1 − D = 0.55), RCOMP = **237 kΩ**. fC then ranges 0.94–2.5 kHz over line and COUT tolerance. The RHP zero is ≥100 kHz (22 µH) or ≥220 kHz (10 µH) at full load, so it is far away.
- CCOMP for a zero at ~150 Hz: 1/(2π × 237 k × 150) = 4.48 nF. Use **4.7 nF**.
- CHF for a pole at the electrolytic ESR zero (~5.6 kHz, assuming about 30 mΩ for the pair **[ESR unverified; depends on the 470 µF part]**): **120 pF**.

### 5.7 UVLO (Eq. 1/2), soft start (Eq. 3), CS filter (Eq. 13)

- **UVLO:** start 10.5 V, stop 9.5 V. RUVLOT = (10.5 × 1.45/1.5 − 9.5)/5 µA = **130 kΩ**. RUVLOB = 1.5 × 130 k/(10.5 − 1.5) = 21.67 kΩ. Use **21.5 kΩ**, which checks at 10.57 V on and 9.57 V off. At 16.8 V the pin sees 2.38 V. Add CUVLO ≈ 10 nF.
- **Soft start:** tSS = CSS/ISS × (1 − VSUPPLY/VLOAD) × VREF. **CSS = 0.47 µF** gives about 30 ms at 12 V → 34 V. A 940 µF charge needs ≥55 ms at 10 W, so the converter rides the current limit for the rest. That is fine for the LM5155 because it has no hiccup.
- **CS RC filter:** RF = 100 Ω and CF = 100 pF. 3 × RF × CF = 30 ns, which is less than (1 − D)/fSW = 155 ns, so Eq. 13 is satisfied.

### 5.8 Components

| Ref role | Value | Rating / size | MPN | Note / source |
|---|---|---|---|---|
| Q1 | N-FET 60 V, 8.1 mΩ (10 V), Qg 11.1 nC | SON3.3×3.3 | **CSD18543Q3A** | Decided. Qg × fSW from VCC is about 15 mA, under the 35 mA VCC limit (§10.2.2.6). |
| D1 | Schottky 100 V, 3 A | CFP5 | **PMEG10030ELPX** | Decided. 100 V gives margin over 38 V plus ringing. |
| LM | **10 µH** (Option B: 22 µH) | 7.3×6.6×2.8 mm | **Bourns SRP7028A-100M** (B: SRP7028A-220M) | Isat 6 A / Irms 3.5 A / 85 mΩ (B: 3.5 A / 2.0 A / 190 mΩ) |
| RS | **82 mΩ**, 1 % | ≥0.25 W, 0805/1206 | Vishay WSL1206R0820FEA **[MPN unverified]** | Section 5.4 |
| RSL | **1.00 kΩ** | 1 %, 0402 | — | Section 5.3 (≤2 kΩ) |
| RF / CF | 100 Ω / 100 pF | 0402 / C0G 50 V | — | Section 5.7 |
| RG | 0–2.2 Ω | 0402 | — | Gate damping |
| RT | **10.2 kΩ** (B: 21.0 kΩ) | 1 %, 0402 | — | Eq. 5 |
| RFBT / RFBB / RINJ | **200 kΩ / 5.76 kΩ / 82.5 kΩ** (3.3 V DAC) | 0.1–1 %, 0603 (RFBT sees 38 V) | — | Section 5.5 |
| RCOMP / CCOMP / CHF | **237 kΩ / 4.7 nF / 120 pF** | 1 % / X7R / C0G | — | Section 5.6 [verify] |
| CSS | **0.47 µF** | 16 V X7R, 0603 | — | Section 5.7 |
| RUVLOT / RUVLOB / CUVLO | **130 kΩ / 21.5 kΩ / 10 nF** | 1 %, 0402 | — | Section 5.7 |
| CBIAS | 0.1 µF | 50 V, 0402 | — | Fig. 10-1 |
| CVCC | 2.2 µF | 16 V X7R, 0603 | — | §9.3.2: 1–4.7 µF |
| RPG | 24.9 kΩ to +3V3 | 0402 | — | §9.3.9 (≥10 kΩ) |
| CIN | 2 × 10 µF + 0.1 µF | 50 V X7R, 1206 | TDK CGA5L1X7R1H106K160AC | Plus shared VSYS bulk |
| COUT bulk | 2 × 470 µF | 50 V | (decided) | 76 % voltage stress at 38 V. Ripple current is about 0.4 A rms. |
| COUT HF | 2 × 2.2 µF | **100 V** X7R, 1210 | — | Next to D1/Q1, to absorb the 2 MHz ripple. Use 100 V parts because of DC-bias derating at 38 V. |
| Bleeder | ~10 kΩ/W class, or a switched discharge | — | — | Recommended for the safety of the 0.68 J bank. The FB string bleeds only about 0.2 mA. **[policy decision]** |
| Inrush / ILIM switch | eFuse with dV/dt and ILIM on the boost input | — | TI TPS25947 / TPS2595x class **[unverified]** | Finding A5 |

---

## Appendix A: TPS25751S (RSM, QFN-32 4×4) pin list, only if external sink FETs are kept

| Pin | Name | Pin | Name |
|---|---|---|---|
| 1 | LDO_3V3 | 17 | I2Cc_IRQ |
| 2 | ADCIN1 | 18 | GPIO3 |
| 3 | ADCIN2 | 19 | **VSYS** (RCP sense on the system side) |
| 4 | LDO_1V5 | 20 | **GATE_VSYS** (gate of the FET whose source is on VSYS) |
| 5 | GPIO0 | 21 | **GATE_VBUS** (gate of the FET whose source is on VBUS) |
| 6 | GPIO1 | 22 | GPIO4/USB_P/LD1 |
| 7 | GPIO2 | 23 | GPIO5/USB_N/LD2 |
| 8 | I2Ct_SDA | 24 | CC1 |
| 9 | I2Ct_SCL | 25 | CC2 |
| 10 | I2Ct_IRQ | 26, 27 | VBUS |
| 11, 12, 14 | GND | 28, 29 | PP5V |
| 13 | GPIO11 | 30 | GPIO7 |
| 15 | I2Cc_SDA | 31 | GPIO6 |
| 16 | I2Cc_SCL | 32 | VIN_3V3 |
| EP | GND | | |

Requirements for the external path: two common-source N-FETs (for example CSD17578Q3A, 30 V) between VBUS and VSYS. GATE series resistance must be ≤3 Ω (§8.3.3.3). CVSYS is 47 µF typ and 100 µF max (§6.4).

---

## Sources

- [TPS25751 datasheet SLVSH93A](https://www.ti.com/lit/ds/symlink/tps25751.pdf): §5 pin tables, §6.4 capacitance, §8.3.3 power paths, §8.3.6/8.4.1 ADCIN, §8.3.11 I2C, §9.4 layout example Fig. 9-26
- [TPS25751 product page](https://www.ti.com/product/TPS25751), supported-charger list
- [E2E: TPS25751 with BQ25731](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1321846/tps25751-tps25751-with-bq25731) and [E2E: TPS25751EVM + BQ25731](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1492191/tps25751evm-tps25751-bq25731-pps-and-reading-out-tps25751-status). Read via search summary only; the pages returned 403.
- [BQ25730 datasheet SLUSE65A](https://www.ti.com/lit/ds/symlink/bq25730.pdf): §5 comparison, Table 6-1, §8.3.5–8.3.12, §9.2
- [BQ2573x EVM user's guide SLUUCB9A](https://www.ti.com/lit/ug/sluucb9a/sluucb9a.pdf): Table 3-1 BOM
- [TPS56637 datasheet SLVSEG1A](https://www.ti.com/lit/ds/symlink/tps56637.pdf): §7.3.4, §8.2
- [TPS62933 datasheet SLUSEA4D](https://www.ti.com/lit/ds/symlink/tps62933.pdf): §7, §9.3.5–9.3.7, §10.2
- [LM5155 datasheet SNVSB75E](https://www.ti.com/lit/ds/symlink/lm5155.pdf): §7, §8.5, §9.3.1–9.3.8, §10.2
- [CSD17578Q3A datasheet](https://www.ti.com/lit/ds/symlink/csd17578q3a.pdf), [CSD18543Q3A datasheet](https://www.ti.com/lit/ds/symlink/csd18543q3a.pdf)
- [Bourns SRP7028A datasheet](https://www.bourns.com/docs/Product-Datasheets/SRP7028A.pdf)
