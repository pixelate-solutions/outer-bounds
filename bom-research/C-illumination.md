# C. IR Illumination and Strobe Driver: Production BOM Research

*Outer Bounds launch monitor. Researched 7 Oct 2026. All prices are Digi-Key USD list prices seen on that date unless marked [est.]. Tariffs are extra. "$@N" means the unit price when building N product units, so it uses the distributor break for N × qty/unit parts. The 10k column uses the highest published Digi-Key break, so it overstates true 10k contract pricing. A contract-price estimate follows the table.*

Tags: [calc] = my calculation; [est.] = estimate with no quote; [verify] = a datasheet or vendor detail to confirm before design freeze.

---

## 0. Summary

- **LED:** **Vishay VSMA1094250** (940 nm, ±28°, double-stack, rated 5 A at t_p = 100 µs, **6.0 W/sr typ at 5 A**). Second source: **ams OSRAM SFH 4728AS A01**, the official successor to the NRND SFH 4727AS A01 (±25°, 5 A, 5.9 W/sr at 5 A). Vishay is about 25% cheaper ($1.38 vs $1.81 at reel) and slightly brighter. The two packages differ, so the PCB needs a dual footprint [verify].
- **Topology:** 24 LEDs on 3 LED boards. Each board carries **one 8-LED series string at 5 A**, with its own GaN switch (EPC2036), gate driver (UCC27611), sense resistor, local hybrid-polymer and MLCC storage, NTC, and hardware pulse limiter. A programmable boost (LM5155) supplies a **~34 V bus (servoed 30–38 V)**.
- **Peak / energy:** 15 A and about 510 W electrical peak from the bus (444 W into the LEDs). Optical output is about 134 W peak, which drops to about 0.13 kW per 5 µs pulse at 30% wall-plug efficiency. Each 5 µs flash takes **2.55 mJ** from the bus, and a 12-flash shot takes **31 mJ**. Total storage is 1,250 µF holding 0.72 J.
- **Optics:** no secondary lens in Rev A. The native ±25–28° dome is already close to the 48° × 37° field. Off-the-shelf LEDiL/Carclo TIR optics are designed for flat-top emitters and are too narrow (TINA2-O is 34° × 17°). Use an IR-pass window. A custom molded freeform lens array is the volume cost-down lever (§2).
- **Eye safety:** **Exempt group under IEC 62471 by a wide margin, even at 0.2 m** [calc]. The boost converter's input-power limit (≤10 W) is a hardware bound on average emission whatever the firmware does. A diffuser is not needed for classification. The ToF face sensor is optional.
- **Board:** **FR-4 4-layer with thermal vias, not MCPCB.** Average LED dissipation is under 1 W per board. The driver parts (bumped GaN die, fine-pitch logic) need a multilayer ground plane, which MCPCB cannot give.
- **Subsystem cost (Digi-Key list):** **$155 @1 / $77 @100 / $64 @1k / $62 @10k**. At 10k with contract pricing, about **$45–50 [est.]**. Add **+$3** for the optional ToF sensor.

---

## 1. 940 nm LED comparison

Requirement: at least 3–5 A for pulses of 10 µs or less, at 940 nm, currently orderable.

| Part | Beam (FWHM) | Ie / Φe at pulse current | Max pulse rating | VF @5 A typ/max | Package | $@1 / @100 units (×24) / @1k / @10k (per LED) | Lifecycle / stock | Verdict |
|---|---|---|---|---|---|---|---|---|
| **Vishay VSMA1094250** | ±28° | **6,000 mW/sr typ** (4,975 min) @5 A, 100 µs | I_FSM 5 A @ t_p 100 µs; 1.5 A DC | 3.7 / 4.2 V | ~3.4–3.85 mm sq. SMD, double stack, 42 mil chip [verify footprint] | $2.34 / $1.468 / $1.379 / $1.379 ([DK](https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/VSMA1094250/15786352)) | Active, 4,764 stk, 9 wk | **Primary** |
| Vishay VSMA1094250X02 | ±28° | 6,000 mW/sr @5 A | 5 A | — | AEC-Q102 | not priced | Active ([Vishay](https://www.vishay.com/en/product/80179/)) | Auto-grade alternate |
| Vishay VSMA1094400 / 600X02 / 750X02 | ±40° / ±60° / ±75° | ~ / 2,300 / 1,600 mW/sr @5 A | 5 A | 3.8 / 4.2 V | same | not priced | Active ([Vishay](https://www.vishay.com/en/product/80295/)) | Wide-fill option |
| **ams OSRAM SFH 4728AS A01** (successor of 4727AS A01) | ±25° | **5,900 mW/sr; 5.6 W flux** @5 A, 100 µs | 5 A @ t_p ≤ 3 ms, D ≤ 0.004 | 3.2 / 4.2 V | OSLON Black 3.85 mm, clear dome, AEC-Q102, Rth 6.6 K/W | $2.942 / $1.887 / $1.809 / $1.809 ([DK](https://www.digikey.com/en/products/detail/ams-osram-usa-inc/SFH-4728AS-A01/16399990)) | Active, 3,189 stk, 14 wk ([DS v1.5](https://look.ams-osram.com/m/134882e52f0c40dc/original/SFH-4728AS-A01.pdf)) | **Second source** |
| ams OSRAM SFH 4728CS A01-FA2FB2 | 50° | 1,250 mW/sr min @1 A | 5 A [verify] | 2.75 V @1 A | OSLON Black | $3.158 (10) / $1.914 / $1.834 / $1.834 ([DK](https://www.digikey.com/en/products/detail/ams-osram-ag/SFH-4728CS-A01-FA2FB2/29295529)) | Active (new), 221 stk, 14 wk | Newest OSRAM option |
| ams OSRAM SFH 4728BS A01 | ±25° | 6,600 mW/sr @5 A, 100 µs | 5 A | — | OSLON Black | $2.869 (10) / $1.836 ([DK](https://www.digikey.com/en/products/result?keywords=SFH%204728BS)) | **NFND** | Out |
| ams OSRAM SFH 4727AS A01 | ±25° | 1,000 mW/sr @1 A | 5 A | — | OSLON Black | — | **NFND → SFH 4728AS A01** ([ams](https://ams-osram.com/products/leds/ir-leds/osram-oslon-black-sfh-4727as-a01)) | Out |
| ams OSRAM SFH 4725AS A01 | ±45° | ~1 W/sr class @1 A | 5 A ([search summary](https://www.mouser.com/datasheet/2/588/asset_pdf_5471963-3419497.pdf)) [verify t_p] | — | OSLON Black | not priced | Full production | Wide alternate |
| Lumileds LUXEON IR Domed **L1I0-0940955800000** | **95° × 58° elliptical** | 750 mW/sr, 1,550 mW @1 A | 5 A pulsed, 1.5 A DC (Fig 8a chart) | 2.8 V @1 A | 3.7 × 3.7 mm domed | $3.602 (10) / $2.538 / $2.210 / $2.210 ([DK](https://www.digikey.com/en/products/result?keywords=L1I0-0940955800000)) | Active, 569 stk, 12 wk ([DS191 2026-06](https://lumileds.com/products/infrared-emitters/luxeon-ir-domed-line/)) | Beam too wide (wastes ~40%), 60% dearer |
| Lumileds L1I0-0940060200000 / 050200000 | 60° / 50° | 1,295 / 1,435 mW/sr @1 A | 5 A | — | domed | similar [est.] | Active | Viable 3rd source. The …0000000 versions are only 3 A |
| OSRAM OSLON P1616 SFH 4180S / 4181S | 130° / 70° | 280 / 680 mW/sr @1 A | **2 A** | — | 1.6 mm | — | NFND ([DS](https://look.ams-osram.com/m/6ace65fd000b14be/original/SFH-4181S.pdf)) | Out (2 A) |
| OSRAM SFH 4770S (SYNIOS) / SFH 4740 (OSTAR Obs.) | — | — | 3 A / 1 A | — | — | — | **850–860 nm**; 4740 obsolete ([DS](https://look.ams-osram.com/m/3d14fbd525ac4a30/original/SFH-4770S.pdf)) | Out (wrong λ) |
| OSRAM SFH 4736 / 4737 | — | — | 0.5 A | — | P1616 | — | 4737 is a 650–1050 nm broadband emitter, obsolete | Out |
| OSRAM SFH 47278AS A01 (rect. 130° × 155°) | 4:3 rectangular | — | 1.5 A class | — | OSLON Black | — | Active ([Newark](https://www.newark.com/ams-osram-group/sfh-47278as-a01/led-oslon-rectangular-wide-foi/dp/62AK0115)) | Out (far too wide, no 5 A) |
| Luminus SST-10-IRD-940 | 50/90/130° | — | 5 A pulse, **requires rise time > 0.5 µs** | — | 3.5 mm | — | Active ([DS](https://download.luminus.com/datasheets/Luminus_SST-10-IRD-940_Datasheet.pdf)) | Out (rise-time rule eats 10–20% of a 3–5 µs pulse) |
| Würth WL-SIMW 3535 940 nm | 90/130° | 220 mW/sr | ~1 A | — | 3535 | — | Active ([Mouser](https://www.mouser.com/new/wurth-elektronik/wurth-high-power-ir-led/)) | Out |
| Everlight EAIST3535A1 | — | — | no 5 A rating published | — | 3535 | — | old (2015) DS | Out |
| Nichia | — | — | no 940 nm high-pulse 3535 part found | — | — | — | — | — |

**Pulse rating at our conditions [calc].** Datasheet ratings are 5 A at 100 µs (Vishay) or ≤3 ms with D ≤ 0.004 (OSRAM). We run 3–5 µs pulses, so each pulse is 20–600× shorter than the rated width. One burst of 12 flashes in 4 ms is D = 1.5% for 4 ms. That is ≈1.1 mJ per LED, which raises a ~0.3 mJ/K die-plus-submount by only a few K. The rating that actually binds is the long-term average duty in armed mode. Keep it ≤0.4% at 5 A, or drop the current in armed mode (see §3.5). Ask Vishay and OSRAM FAEs for a "5 A, 5 µs, burst" confirmation [verify].

**Multi-chip emitters.** OSRAM's multi-chip IR parts (OSTAR SFH 4740/4750/4751, 10-chip OSTAR Observation) are 850 nm and/or obsolete, and run at 1 A with 15 V+ forward voltage. They give no benefit over 8 discrete double-stack LEDs and are a single point of failure.

**Why VCSELs are out.**
1. A VCSEL array is a **laser product**. IEC 60825-1 classification (Class 1 needed for a consumer device near faces) must cover **single-fault conditions**, such as a cracked or detached diffuser that turns a Class 1 product into Class 3B/4. In practice that means a redundant diffuser-integrity interlock and a fault analysis.
2. In the US, **21 CFR 1040.10/1040.11** requires an FDA/CDRH product report and accession number, laser labels, and annual reports. Any optics change can force re-classification. Lumileds WP35 notes VCSELs "need additional safety measures."
3. The VCSEL's main benefit, a ~1 nm line that allows a 10 nm filter, adds nothing for us. With 5 µs gating, sunlight is already about 4% of signal using a 50 nm LED filter (prior analysis).
4. Cost: we need about 130 W optical peak, which takes several high-power arrays plus certification NRE. LEDs fall under IEC 62471 lamp safety, which is self-declared and where we are Exempt (§4). The certification burden is the real cost, and it recurs with every optical change.

---

## 2. Optics

**Required beam [calc].** At 0.45 m, a 400 × 300 mm field subtends ±24.0° × ±18.4° (48° × 37° full angle). For a cos^n emitter on a flat target (irradiance ∝ I(θ)·cos³θ):

| LED half-angle | flux landing in field | edge (24°) vs centre | corner vs centre |
|---|---|---|---|
| ±25° (SFH 4728AS) | 49% | 0.40 | 0.26 |
| **±28° (VSMA1094250)** | **42%** | **0.46** | **0.32** |
| ±40° (VSMA1094400) | 26% | 0.60 | 0.47 |
| ±60° | 16% | 0.70 | 0.58 |

A ball is a sphere, not a flat target, so the real fall-off is roughly cos²·I(θ) and a little gentler. **The ideal secondary optic is about 60° × 45° FWHM with a flat top.** That puts about 70% of the flux in the field and keeps it within ±15%.

**Off-the-shelf options:**
- LEDiL TINA2-O (CA12379) gives 34° × 17° FWHM and 80–88% efficiency, and is compatible only with flat-top emitters (LUXEON IR Compact, SFH 4170S/4180S/4770S) ([LEDiL DS](https://www.ledil.com/data/prod/Tina/12379/12379-ds.pdf)). It is too narrow, and our domed 5 A parts are not on its compatibility list.
- In general, LEDiL, Carclo and Khatod catalogue TIR optics are simulated for flat emitters. Over a domed OSLON Black or VSMA they lose efficiency and beam control.
- OSRAM's own point is that the domed OSLON Black variants exist "so designers need not install secondary optics."

**Rev A decision: no secondary optic.** Use ±28° domed LEDs. Aim each 8-LED board, mounted 20–40° off the camera axis, at a different sub-zone: ball-at-rest/launch zone versus the downrange half of the field. Cross-fill from 3 clusters flattens the illumination. Remove the residual with per-camera, per-cluster flat-field calibration, since a 12-bit sensor has the headroom. For bring-up, the Intelligent LED Solutions LEDiL lens-selector boards for OSLON Black IR, e.g. ILR-IO01-94SL-LEDIL-SC221 ([ILS](https://i-led.co.uk/LED-Light-Engines/Ledil-Lens-Selectors/Ledil-lens-selector-PCB.php)), let us try LEDiL optics on a real 940 nm OSLON Black quickly.

**Volume lever (≥2–3k units):** a custom injection-moulded PMMA freeform lens array, one 8-cavity array per board, about 60° × 45°.
- Raises in-field flux from 42% to about 70%, so the same photons need about **15 LEDs instead of 24**.
- Saves about 9 × $1.38 plus driver share, roughly $13–15/unit.
- Tooling about $15–30k and piece price about $0.20–0.50 per array [est., needs a moulder quote].
- Break-even at about 1.5–3k units [calc]. Decide after bench photon-budget validation.

**Window / diffuser.** Use an IR-pass black acrylic window, Plexiglas 3143 (2 mm). It is visible-black and transmits about 90% near 905 nm, with 940 nm well inside its band. A 12" × 12" × 0.080" sheet costs $17.40 (1–2) and $4.91 (50+); 24" × 48" costs $24.69 at 50+ ([ePlastics](https://www.eplastics.com/plexiglass/acrylic-sheets/ir-transmitting)). Small pieces are about $6.66 per 200 × 200 mm ([eBay](https://www.ebay.com/itm/231787983493)). A diffuser is **not needed for IEC 62471** (§4). If one is ever wanted to enlarge apparent source size, add a light mould-texture on the inside face of the window at zero piece cost [est.].

---

## 3. Driver design

### 3.1 Topology

```
7–17 V sys rail ─► LM5155 boost (input-current-limited ≤10 W; Vout servo 30–38 V via MCU DAC/PWM on FB)
                    │
                    ├─ 2 × 470 µF / 50 V alu (main board bulk) ─── bleed FET + 10 kΩ (discharges when disarmed)
                    │
                    └─► 3 × JST-GH 8-pin cable (VBUS×2, GND×2, STROBE_n, nEN, NTC, IMON)
                          │
                LED board ×3:  100 µF hybrid-polymer + 4 × 2.2 µF/100 V MLCC (local pulse reservoir)
                          VBUS ─► 8 × VSMA1094250 in series ─► EPC2036 drain
                                                               EPC2036 source ─► 0.1 Ω WSL2010 ─► GND
                          STROBE ─► [74LVC1G123 max-width one-shot ≈8 µs] ─┐
                                    [74LVC1G123 hold-off one-shot ≈300 µs]─┼─► 3-in AND ─► UCC27611 IN+
                          nEN (pull-up = disabled) ─────────────────────────────────────► UCC27611 IN−
                          Rsense ─► TLV3201 (trip ≈6.5 A) ─► /CLR of width one-shot (instant cut-off)
                          NTC 10 k ─► MCU ADC (and optional comparator to nEN)
```

- **Why 8S at about 34 V.** One FET and one sense resistor per board. Bus current is 5 A per board, so the cable carries only recharge current. A 50 V capacitor rating gives good derating. VF at 5 A is 3.7 V typ / 4.2 V max per LED, so a string is 29.6 V typ / 33.6 V max. On top of that sit 0.5 V across Rsense, 0.35 V across the FET, and about 1–2 V regulation headroom.
- **Current control.** There is no linear current sink. Linear regulation at 5 A within 200 ns needs a >50 MHz loop, which is costly. The MCU samples IMON mid-pulse and servos Vbus with a factory-calibrated setpoint and NTC feed-forward. Flash-to-flash it trims the strobe width so that ∫I·dt is constant. String sensitivity is dI/dV ≈ 0.8 A/V, from 8 × ~0.13 Ω dynamic plus 0.1 Ω sense plus 0.07 Ω FET. **VF tempco (−2 to −4.8 mV/K per LED) moves the current about 10% over 30 K if left uncorrected, so the servo is mandatory** [calc].
- **Switch and driver.** Pulses are µs long, not ns, so we do not need LMG1020-class 400 ps edges. UCC27611 (5 V clamped GaN driver, 4 A/6 A, SON-6 2 × 2 mm, $0.81) with EPC2036 (100 V, 65 mΩ, Qg 0.9 nC) gives about 10 ns edges. Add a 2–10 Ω turn-off gate resistor to tame drain ringing. The LMG1020 is WCSP-only, $3.16 at reel and out of stock until 5 Nov 2026. The LMG1025-Q1 (QFN) is $8. Both are needless here.
- **Silicon fallback.** If GaN die assembly is a CM concern, use a logic-level Si FET in 3 × 3 mm (e.g. CSD18543Q3A, 60 V) with a UCC27517 at 10 V gate drive. Edges of about 20–30 ns are still under 1% of a 4 µs pulse.

### 3.2 Energy and peak-current sizing [calc]

| Quantity | Value |
|---|---|
| LEDs / strings | 24 / 3 × 8S (footprint/connector option for a 4th board → 32 LEDs) |
| Peak current | 3 × 5 A = **15 A** (20 A with 32 LEDs) |
| Peak electrical power from bus | 15 A × 34 V ≈ **510 W** (LEDs 444 W, Rsense/FET/headroom ≈ 66 W) |
| Peak optical power | 24 × ~5.6 W ≈ **134 W** (≈ 144 W/sr summed on-axis) |
| Energy per flash, 5 µs (3 µs) | **2.55 mJ (1.53 mJ)** from bus; 0.67 mJ optical |
| Energy per shot, 12 flashes | **31 mJ** (5 µs) / 18 mJ (3 µs) |
| Charge per shot | 12 × 15 A × 5 µs = **0.90 mC** |
| Storage | 2 × 470 µF (main) + 3 × (100 µF + 4 × ~1 µF effective MLCC at 34 V) ≈ **1,250 µF** → **0.72 J** at 34 V |
| Burst droop, no recharge | 0.90 mC / 1.25 mF = **0.72 V (2.1%)** → about 0.6 A (12%) by the last flash uncompensated |
| With the boost at its current limit through the 4 ms burst | 10 W / 34 V = 0.29 A × 4 ms = 1.2 mC ≥ burst charge, so net droop is about 0.2–0.3 V. Per-flash width trim from an ADC read of Vbus brings flash-to-flash ∫I·dt within about 1% |
| In-pulse local droop (per board) | 25 µC / ~104 µF ≈ 0.24 V → about 4% sag within a 5 µs pulse. This is acceptable because the exposure integrates. Fit a second 100 µF if bench shows it matters |
| Armed-mode continuous strobing | 0.1% duty (3 cams × 60 fps × 5 µs) ≈ 0.5 W; 0.5% duty ≈ 2.6 W from the bus |
| Boost rating | **10 W max, enforced by input-current limit**. That covers 0.5% armed duty plus recharge during the burst. Charging 0.72 J from 0 V at 10 W takes ≈ 70 ms |
| Recovery between shots | < 10 ms |

Capacitor technology:
- **MLCC** is unsuitable as bulk. A 100 V X7R 2.2 µF in 1210 keeps only about 1 µF at 34 V and costs $0.33–0.48, so 1,000 µF of MLCC would cost about $300. Use MLCC only as the local high-frequency loop cap.
- **Hybrid polymer** (Panasonic ZA/ZU, 10–28 mΩ) is the right local pulse reservoir. Watch the **37–43 week lead times**.
- **Aluminium electrolytic** (Panasonic FK, 50 V 470 µF, 16 × 17 mm) is the cheapest bulk at about $1.05.
- **Height risk:** the FK part is 17 mm tall. If the enclosure cannot take it, use 4 × EEH-ZA1H101P (10.5 mm) or several smaller FK cans.

### 3.3 Boost / charger

- **TI LM5155** (non-sync boost controller, 2.2 MHz capable, input-current-limit sense) with a CSD18543Q3A 60 V FET (logic-level, 9.9 mΩ), a PMEG10030ELP 100 V/3 A Schottky, and a 10 µH / 6 A Isat SRP7028A.
- Output is set by an MCU DAC/PWM injected into FB, with OVP at about 40 V.
- LT3757 is an equivalent alternative, at higher cost.
- A flyback photoflash-style charger such as LT3751 is unnecessary at a 34 V output and 10 W.
- LM5155EVM-BST costs $81.12 ([DK](https://www.digikey.com/en/products/detail/texas-instruments/LM5155EVM-BST/9860040)).

### 3.4 Safety hardware

1. **Pulse-width limiter (per LED board, next to the driver).** A 74LVC1G123 one-shot fires on the STROBE rising edge with τ ≈ 8 µs, and GATE = STROBE·Q. If STROBE is held high, Q times out and the gate drops. The part is edge-triggered, so a stuck level cannot re-trigger it. Placing it on the LED board means a shorted cable cannot hold the LEDs on either.
2. **Minimum off-time (hold-off) one-shot.** A second '123 triggers on the GATE falling edge and blocks for about 300 µs. It is compatible with 12 flashes in 4 ms (333 µs spacing). That caps worst-case duty at about 2.6% even if software toggles STROBE as fast as it can.
3. **Over-current trip.** A TLV3201 on Rsense (40 ns) pulls the one-shot's /CLR low at about 6.5 A and ends the pulse at once.
4. **Hardware enable interlock.** UCC27611 IN− = nEN with a pull-up on the LED board, so a disconnected cable is disabled by default. On the main board, nEN is asserted only when *ARM GPIO* AND a *heartbeat missing-pulse detector* (third '123, τ ≈ 20 ms, retriggered by MCU heartbeat) are both true. The same signal enables the boost (LM5155 EN/UVLO) and releases the Vbus bleed FET. If the MCU hangs, strobes stop and the bank discharges.
5. **Thermistor.** Use one 10 k NTC (0402) per LED board, read by the MCU, with derate/inhibit above about 85 °C board temperature. Murata NCP15XH103F03RC is NFND, so use its successor **NCU15XH103F60RC**.
6. **Energy bound (eye-safety backstop).** Even with every gate stuck on, two things limit emission. The bank holds only 0.72 J, and a one-time dump is eye-safe (§4). The boost input-current limit caps sustained average output at ≤10 W electrical, about 3 W optical.
7. **Proximity sensor (optional).** ST **VL53L4CD** ToF (to 1.3 m, Class 1 VCSEL certified by ST) can inhibit when an object is within about 0.25 m of an LED cluster.
   - Caveat: it emits at 940 nm, so its ranging must be time-multiplexed away from camera exposures.
   - Our 62471 margin does not require it (§4). Recommend a DNP footprint in production and populating it only if the certification lab wants it.
   - VL53L1X (4 m) is unnecessary.

### 3.5 Armed-mode note for the system team

At 5 A, the OSRAM long-term duty rating is D ≤ 0.004. If the camera architecture really strobes continuously at 0.4–0.5% while armed, either drop the armed-mode current to about 2–3 A or the rate to ≤200 Hz, or confirm with the vendor. This also keeps average boost load under about 1 W.

---

## 4. IEC 62471 check [calc; limits from IEC 62471 Table 6, verify with lab]

Worst-case geometry: eye at 0.2 m, on-axis.
- One cluster gives 8 × 6.0 W/sr = 48 W/sr peak, which is 1,200 W/m² at 0.2 m.
- If all three clusters' beams overlapped (geometrically unlikely at 0.2 m), it would be 3,600 W/m² peak.

| Hazard | Exposure (worst, 3,600 W/m² peak) | Exempt limit | Margin |
|---|---|---|---|
| Cornea/lens IR, E_IR, 0.1% armed duty | 3.6 W/m² average | 100 W/m² (t > 1000 s) | 28× |
| E_IR at 0.5% duty | 18 W/m² | 100 W/m² | 5.5× |
| E_IR, **firmware fault, boost-power-limited (≈2% duty)** | ≈72 W/m² | 100 W/m² | 1.4× (still Exempt) |
| E_IR, single shot (12 × 5 µs) | 0.22 J/m² dose | 18,000·t^0.25 J/m² (≫ 1,000 J/m²) | > 10³ |
| Retinal thermal, weak visual stimulus, L_IR (1 mm² source, 6 W/sr → 6 × 10⁶ W·m⁻²·sr⁻¹ peak) at 2% fault duty | 1.2 × 10⁵ | 6000/α = 5.5 × 10⁵ (α = 0.011) | 4.5× |
| One-time full-bank dump (0.72 J over ~5 ms) | about 20 J/m² at 0.2 m | ≈5,000 J/m² for 5 ms | > 200× |

Conclusion: **Exempt at 0.2 m even under firmware fault**, *provided* the boost power limit is a hardware element (a sense resistor, not a firmware setting). Treat it as safety-critical in the design FMEA.

---

## 5. LED board

- **Choice: 4-layer FR-4, 1 oz, ENIG, about 40 × 30 mm.** Use a via array (0.3 mm, filled or tented) under each LED thermal pad, connected to an inner GND/heat-spreader plane, and mount the board to a metal bracket with a thermal pad.
- Average dissipation is under 0.5 W per board at 0.1% duty, and about 2.5 W worst-case at the 2.6% hold-off ceiling. FR-4 with vias handles both.
- **MCPCB is rejected.** It is single- or double-layer only and cannot give the solid ground plane the gate loop needs. It is also hostile to bumped GaN die and fine-pitch logic, and costs 2–4× FR-4 per area ([JLCPCB MCPCB](https://jlcpcb.com/pcb-fabrication/metal-core-pcb); [JLC blog](https://jlcpcb.com/blog/metal-core-pcb-thermal-conductivity-design-guide)).
- **Fabrication estimate** (JLCPCB 4-layer small-batch rate $70.6/m², [JLC](https://jlcpcb.com/blog/special-discount-on-quality-4-layers-pcbs)) [est.]:

| Build qty (product units) | boards | $/board | $/unit (3 boards) |
|---|---|---|---|
| 10 | 30 | ~$1.5–5 (proto fees dominate) | ~$5–15 |
| 100 | 300 | ~$0.6–1.0 | ~$2–3 |
| 1k | 3k | ~$0.3–0.4 | ~$1.0–1.2 |
| 10k | 30k | ~$0.2–0.25 | ~$0.6–0.75 |

  SMT assembly is extra: about $0.5–1.5 per board at volume [est.]. The LED thermal pad's electrical polarity differs by vendor, so do not tie the pad net to GND without checking each datasheet [verify].

---

## 6. Per-unit BOM: illumination and strobe subsystem

| Item | Manufacturer | MPN | Vendor | URL | Qty/unit | $@1 | $@100 | $@1k | $@10k | Stock/lead | Lifecycle | Notes/alternates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 940 nm IR LED, ±28°, 5 A pulse | Vishay | VSMA1094250 | Digi-Key | [link](https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/VSMA1094250/15786352) | 24 | 2.34 | 1.468 | 1.379 | 1.379 | 4,764 / 9 wk | Active | 2nd src SFH 4728AS A01 ($2.942/$1.887/$1.809, [DK](https://www.digikey.com/en/products/detail/ams-osram-usa-inc/SFH-4728AS-A01/16399990)); auto: VSMA1094250X02 |
| GaN FET 100 V 65 mΩ (string switch) | EPC | EPC2036 | Digi-Key | [link](https://www.digikey.com/en/products/detail/epc/EPC2036/5224975) | 3 | 2.10 | 0.905 | 0.593 | 0.532 | 29,108 / 16 wk | Active | EPC2204 ($3.66@1, [DK](https://www.digikey.com/en/products/detail/epc/EPC2204/10211092)) if 4 strings share 1 FET; Si alt CSD18543Q3A |
| GaN low-side driver, 5 V clamp | TI | UCC27611DRVR | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=UCC27611DRVR) | 3 | 1.64 | 0.913 | 0.814 | 0.788 | 2,369 / 20 wk | Active | LMG1020YFFR $5.68/$3.64/$3.16 (WCSP, 0 stk) [DK](https://www.digikey.com/en/products/result?keywords=LMG1020YFFR); LMG1025-Q1 $8.16@1k [DK](https://www.digikey.com/en/products/result?keywords=LMG1025QDEERQ1) |
| Monostable (width limit, hold-off, heartbeat) | TI | SN74LVC1G123DCUR | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=SN74LVC1G123DCUR) | 7 | 1.67 | 0.920 | 0.833 | 0.806 | 0 stk (3k due 19 Nov) / 20 wk | Active | Nexperia 74LVC1G123DC,125 $0.48@1 ([DK](https://www.digikey.com/en/products/detail/nexperia-usa-inc/74LVC1G123DC-125/5221579)) |
| Over-current comparator (40 ns) | TI | TLV3201AIDCKR | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=TLV3201AIDCKR) | 3 | 1.81 | 1.014 | 0.906 | 0.878 | 0 stk (Nov) / 20 wk | Active | Could be deleted if IMON is read by MCU only (loses µs-scale OC trip) |
| Current-sense resistor 0.1 Ω 2010 | Vishay Dale | WSL2010R1000FEA | Digi-Key | [link](https://www.digikey.com/en/products/detail/vishay-dale/WSL2010R1000FEA/712538) | 3 | 0.88 | 0.352 | 0.315 | 0.262 | 5,248 / 32 wk | Active | Low-L; 2.5 W peak, 12.5 µJ/pulse |
| Local pulse reservoir 100 µF/50 V hybrid polymer | Panasonic | EEH-ZA1H101P | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=EEH-ZA1H101P) | 3 | 2.05 | 0.951 | 0.655 | 0.624 | **0 stk, 37 wk** | Active | EEH-ZU1H221V 220 µF 10 mΩ $1.52@2.5k ([DK](https://www.digikey.com/en/products/detail/panasonic-industry/EEH-ZU1H221V/14114076)), 17 mm tall |
| HF loop cap 2.2 µF 100 V X7R 1210 | KEMET | C1210C225K1RACTU | Digi-Key | [link](https://www.digikey.com/en/products/detail/kemet/C1210C225K1RACTU/1950689) | 12 | 0.687 | 0.399 | 0.326 | 0.326 | 197k / 18 wk | Active | Murata GRM32ER72A225KA35L is NFND |
| NTC 10 k 0402 | Murata | NCU15XH103F60RC (successor of NCP15XH103F03RC) | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=NCP15XH103F03RC) | 3 | 0.12 | 0.077 | 0.064 | 0.052 | 211k | NCP15 = NFND | Prices are NCP15 listing (proxy) |
| Board connector 8-pin 1.25 mm | JST | BM08B-GHS-TBT | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=BM08B-GHS-TBT) | 6 | 0.50 | 0.325 | 0.276 | 0.246 | 54,619 / 16 wk | Active | 3 on LED boards + 3 on main |
| Cable assembly (2 × GHR-08V-S + crimps + wire, ~100 mm) | JST / CM | GHR-08V-S + SSHL-002T-P0.2 | Digi-Key / CM | [housing $0.17](https://www.digikey.com/en/products/result?keywords=BM08B-GHS-TBT) | 3 | 4.00 [est.] | 1.50 [est.] | 0.90 [est.] | 0.70 [est.] | — | Active | Twist VBUS/GND pairs |
| LED-board misc (3-in AND 74LVC1G11, gate R, RC timing, pull-ups, TVS, ESD) | various | — | — | — | 1 lot | 3.00 [est.] | 1.20 [est.] | 0.60 [est.] | 0.45 [est.] | — | — | Grouped passives/logic |
| LED board PCB, 4L FR-4 ~40 × 30 mm | JLCPCB/PCBWay | custom | — | [rate](https://jlcpcb.com/blog/special-discount-on-quality-4-layers-pcbs) | 3 | 5.00 [est.] | 1.00 [est.] | 0.40 [est.] | 0.25 [est.] | — | — | Fab only, no assembly |
| IR-pass window, Plexiglas 3143 2 mm, cut | Röhm/Plexiglas | 3143 | ePlastics | [link](https://www.eplastics.com/plexiglass/acrylic-sheets/ir-transmitting) | 1 set (3) | 6.66 [eBay piece](https://www.ebay.com/itm/231787983493) | 0.30 [est.] | 0.20 [est.] | 0.15 [est.] | — | Active | Or mould into enclosure bezel |
| Secondary optic | — | none (Rev A) | — | — | 0 | — | — | — | — | — | — | Custom moulded array at ≥2k units (§2) |
| Boost controller | TI | LM5155DSSR | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=LM5155DSSR) | 1 | 2.21 | 1.335 | 1.219 | 1.096 | 0 stk (21 Dec) / 20 wk | Active | LT3757 alt |
| Boost FET 60 V logic-level | TI | CSD18543Q3A | Digi-Key | [link](https://www.digikey.com/en/products/detail/texas-instruments/CSD18543Q3A/6588881) | 1 | 1.39 | 0.575 | 0.448 | 0.322 | 1,006 / 20 wk | Active | Toshiba TPN11006NL |
| Boost diode 100 V 3 A Schottky | Nexperia | PMEG10030ELPX | Digi-Key | [link](https://www.digikey.com/en/products/detail/nexperia-usa-inc/PMEG10030ELPX/5436251) | 1 | 0.79 | 0.79 | 0.184 | 0.184 | 112k | Active | @100 uses CT price (conservative) |
| Boost inductor 10 µH 6 A Isat | Bourns | SRP7028A-100M | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=SRP7028A-100M) | 1 | 1.10 | 0.742 | 0.610 | 0.502 | 17,967 / 22 wk | Active | Coilcraft XAL6060-103 |
| Bulk cap 470 µF/50 V alu SMD | Panasonic | EEE-FK1H471AM | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=EEE-FK1H471AM) | 2 | 2.91 | 1.305 | 1.046 | 1.046 | 1,203 / 37 wk | Active | 16 × 17 mm; low-profile alt 4 × EEH-ZA1H101P |
| Main-board misc (bleed FET + R, FB DAC network, Rsense for input limit, input caps, OVP divider, TVS) | various | — | — | — | 1 lot | 2.50 [est.] | 1.20 [est.] | 0.70 [est.] | 0.50 [est.] | — | — | Grouped |
| **Subtotal (Digi-Key list)** | | | | | | **155.36** | **77.28** | **64.49** | **61.68** | | | 10k contract est. **≈ $45–50** |
| *Optional:* ToF face-proximity inhibit | ST | VL53L4CDV0DH/1 | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=VL53L4CDV0DH%2F1) | 1 | 4.40 | 3.295 | 2.941 | 2.758 | 39,093 / 16 wk | Active | DNP by default; total with it 159.76 / 80.58 / 67.43 / 64.44 |

**Cost structure.** LEDs are 51–54% of the subsystem at ≥100 units. LED swaps change the total as follows:
- SFH 4728AS A01 instead of Vishay: **+$10.1–10.3/unit** at ≥100.
- Lumileds 95 × 58°: **+$20–26/unit**.

**10k contract estimate [est.]:**
- LEDs at about $1.10 (−$6.6).
- Nexperia one-shots at about $0.15 (−$4.6).
- MLCC at about $0.10 (−$2.7).
- Other ICs about 10% below list (−$1.5).
- Total ≈ **$46**. That is in line with the prior plan's $34 (LEDs + optics) + $12 (driver) = $46 at 10k.

---

## 7. Bring-up / evaluation hardware

| Board | Price | URL | Relevance |
|---|---|---|---|
| TI LMG1020EVM-006 | $199.20 (0 stk; 1 due 15 Oct) | [DK](https://www.digikey.com/en/products/result?keywords=LMG1020EVM-006) | ns lidar driver; only useful to compare against UCC27611 |
| EPC9126 (EPC2212 lidar driver) | $390.00 | [DK](https://www.digikey.com/en/products/detail/epc/EPC9126/6579241) | ns-pulse resonant; tiny caps droop at 5 µs. Low value |
| EPC9144 (lidar driver) | $393.75 (25 stk, 8 wk) | [DK](https://www.digikey.com/en/products/result?keywords=EPC9144) | Same caveat |
| TI LM5155EVM-BST | $81.12 | [DK](https://www.digikey.com/en/products/detail/texas-instruments/LM5155EVM-BST/9860040) | **Useful**: bring up the 34 V bus and current limit |
| ILS LEDiL lens-selector boards, OSLON Black IR 940 nm (e.g. ILR-IO01-94SL-LEDIL-SC221) | not priced | [ILS](https://i-led.co.uk/LED-Light-Engines/Ledil-Lens-Selectors/Ledil-lens-selector-PCB.php) | Quick optic A/B |

**Recommendation:** skip the EPC lidar EVMs. Spin a Rev-0 version of our own LED board, which costs about $150–250 for 5 assembled boards at JLC/PCBWay [est.], and drive it from the LM5155EVM. That bench-validates the real photon budget at 5 A / 3–5 µs. The bench run measures:
- Ie at 5 A / 4 µs;
- VF spread across bins;
- tempco;
- droop across a 12-flash burst.

---

## 8. Decisions and risks

**Decisions**
1. **LED:** Vishay VSMA1094250 as primary and OSRAM SFH 4728AS A01 as second source, on a dual footprint. Both are double-stack, rated 5 A, and about 6 W/sr.
2. **Strings:** 24 LEDs as 3 × 8S strings at 5 A, one per LED board. The bus is about 34 V, servoed 30–38 V.
3. **Switching:** EPC2036 with UCC27611. LMG1020-class ns edges are unnecessary for µs pulses.
4. **Storage:** about 1,250 µF total, split between main-board electrolytic bulk and per-board hybrid-polymer local reservoirs.
5. **Boost:** LM5155, input-current-limited to 10 W. That limit doubles as the hardware eye-safety bound.
6. **Hardware safety chain on each LED board:** width one-shot, hold-off one-shot, OC comparator, fail-safe nEN, plus a heartbeat watchdog on the main board.
7. **Optics and board:** no secondary optic in Rev A, FR-4 rather than MCPCB, and the ToF sensor DNP.

**Risks**
1. **Brightness at 5 µs is not specified by any vendor.** All ratings are at 100 µs. Bench-measure before freezing the LED count. The 4th-board option takes the design to 32 LEDs.
2. **Current regulation depends on the Vbus servo.** Without it, VF tempco and bin spread move the current ±10–15%.
3. **Long lead times:**
   - Panasonic hybrid and FK caps: 37–43 weeks.
   - WSL2010: 32 weeks.
   - Several TI parts are at 0 stock with Nov–Dec 2026 restock (LMG1020, LM5155, SN74LVC1G123, TLV3201).
   Qualify alternates now: Nichicon/Chemi-Con hybrids, Nexperia '123, Susumu/Bourns sense resistors.
4. **Package mismatch.** Vishay VSMA and OSLON Black are not drop-in. Verify both land patterns and dome heights for any bracket or window clearance.
5. **Armed-mode duty.** Continuous 0.4–0.5% strobing at 5 A sits at the LED duty rating. Coordinate with the camera slice (§3.5).
6. **Uniformity.** The ±28° native beam gives about 2–3× centre-to-corner fall-off on a flat target. This relies on cluster aiming and flat-field calibration until a custom lens is tooled.
7. **ToF self-interference.** If populated, the VL53L4CD's 940 nm emission must be time-multiplexed away from exposures.
8. **Certification.** The IEC 62471 "Exempt" claim rests on [calc]. Budget a lab measurement (about $3–8k [est.]) and treat the boost power limit as a safety-critical component.
