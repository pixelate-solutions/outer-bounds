# Outer Bounds: power, battery, display, sensors, thermal and UI BOM (slice E)

Research date: 7 October 2026. Prices are USD unless marked. They are distributor list prices seen on the cited page on that date, before tariffs and freight.

**Price-tier convention**
- **$@1 and $@100:** Digi-Key cut-tape or bulk price at that quantity, or the nearest break below it.
- **$@1k:** the first full-reel or bulk break at or near 1,000 pcs. Several TI parts have no 1k break, so the 3k reel price is shown.
- **$@10k:** the largest published distributor break. TI-direct or contract pricing is usually 10–25 % lower, but none of that discount is assumed.
- **"e" suffix:** an engineering estimate with no vendor quote behind it. The basis is given in the notes column.

---

## 1. Key decisions (summary)

| # | Decision | Choice |
|---|---|---|
| 1 | Battery format | **Custom smart pack, 4S1P 21700, fuel gauge in the pack (TI BQ40Z50-R2), built by a Shenzhen pack OEM.** Baseline cell is the LG M58T (5.65 Ah nominal, about 81 Wh). Second sources are the Molicel P50B and Samsung 50S (5.0 Ah, 72 Wh) in the same housing. Standard formats are rejected (section 4). |
| 2 | Runtime reality check | 72 Wh gives only **4.2 h at 15 W** (5.2 h at 12 W). 81 Wh (M58T) gives **4.7 / 5.9 h**. A full 6 h at 15 W needs about 103 Wh, which is over the 100 Wh limit. **The power budget has to average ≤12–13 W, or the spec should read "5 h".** The 5S1P 90 Wh fallback is in section 4.6. |
| 3 | USB-C PD sink | **TI TPS25751DREFR**. It has an integrated 28 V/7 A power path and handles PD 3.1 negotiation. The TPS25750 is NRND (not recommended for new designs). |
| 4 | Charger / power path | **TI BQ25730RSNR**, a 1–5S NVDC buck-boost controller with external FETs and a BATFET. The device runs from USB-C with no battery and supports hot-swapping the pack while on USB-C. The BQ25731 is *not* suitable because it has no BATFET or NVDC. The BQ25798 is only acceptable if charging is capped at about 45 W. |
| 5 | Indoor SKU | **Same PCB with a different BOM variant.** The charger, pack header and display FPC are not fitted (DNP). A barrel jack and an LM74700 ideal-diode OR stage are fitted onto VSYS. The 5 V and 3.3 V bucks run from 4.5–28 V, so 24 V input works. |
| 6 | External PSU | **Pro:** a private-label 65 W GaN USB-C PD charger with UL/CE/FCC/PSE, about $13 at volume, optional in the box. **Indoor:** Mean Well GST60A24-P1J (24 V/60 W, Level VI, cULus/CE/PSE). |
| 7 | Display | **2.4" transflective IPS TFT, 240×320, SPI (ST7789)**: VIEWE UEED024QV-RH40-A003 or Leadtek LTK024QVHLM17-V2. The alternate is the Newhaven NHD-2.8-240320AF-CSXP-F (1,000-nit IPS, same controller family). **No touch.** The Pro has three IP67 tact buttons. |
| 8 | Leveling | **Pro: Murata SCL3300-D01 inclinometer.** Its offset tempco is ±0.005 °/°C, which keeps 0–40 °C drift within about ±0.1° without per-unit temperature calibration. **Indoor: Bosch BMI323** plus factory calibration, because the indoor temperature range is small. Both footprints are on the shared PCB. |
| 9 | Air density | **Bosch BMP585** (pressure) and **Sensirion SHT45-AD1F** (T/RH with a PTFE membrane) in a vented pocket isolated from the SoC heat. The BME280 and BMP390 are both out of stock at Digi-Key. |
| 10 | Thermal | Sealed IP54 electronics bay. SoM heat goes through a heat pipe and spreader to a fin stack in a separate air duct, cooled by a **Delta BFB0405HHA-TZP4 IP55 40 mm blower** (30,000 h at 40 °C). The Indoor uses a Sunon MagLev MF40100V1 (70,000 h at 40 °C). |

---

## 2. Line-item BOM (centerpiece)

Qty is per unit, given as Pro / Indoor. "In-pack" rows are costed inside the battery pack price and are **not** added again.

| Item | Manufacturer | MPN | Vendor | URL | Qty/unit (Pro / Indoor) | $@1 | $@100 | $@1k | $@10k | Stock/lead | Lifecycle | Notes/alternates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **POWER INPUT & PATH** | | | | | | | | | | | | |
| USB-C receptacle, IP67, 5 A/48 V, mid-mount | GCT | USB4720-03-A | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=USB4720-03-A) | 1 / 1 | 2.43 | 1.76 | 1.46 (1.3k reel) | 1.31 (6.5k) | 2,082 stk; 7 wk | Active | USB 2.0 pins plus CC/SBU, gasket included. The Amphenol 12401610E4#2A ($1.43→$0.71, [link](https://www.digikey.com/en/products/result?keywords=12401610E4%232A)) and USB4105-GF-A ($0.80) are **not IP-rated**, so they would need a housing gasket. |
| USB-C PD sink controller | TI | TPS25751DREFR | Digi-Key | [link](https://www.digikey.com/en/products/detail/texas-instruments/TPS25751DREFR/23028775) | 1 / 1 | 3.39 | 2.10 | 1.80 (3k reel) | 1.80 | 10,469 stk; 20 wk | Active | Integrated 28 V/7 A load switch with OVP, so no external input FETs are needed. TPS25750 is **NRND** ([TI](https://www.ti.com/product/TPS25750)). Alternates: STUSB4500QTR $2.22/$1.34/$1.12/$1.10 ([link](https://www.digikey.com/en/products/result?keywords=STUSB4500QTR); 30 wk; needs 2 ext. PFETs) and Infineon CYPD3177-24LQXQ $2.07/$1.24/$1.10/$1.03 ([link](https://www.digikey.com/en/products/detail/infineon-technologies/CYPD3177-24LQXQ/10238328)). |
| NVDC buck-boost charge controller, 1–5S | TI | BQ25730RSNR | Digi-Key | [link](https://www.digikey.com/en/products/detail/texas-instruments/BQ25730RSNR/13896423) | 1 / 0 | 5.08 | 3.23 | 2.80 (3k reel) | 2.80 | **0 stk; 2,970 due 25-Jan-2027**; 20 wk | Active | **Supply risk: order early or buy from TI direct.** Has a BATFET and NVDC power path, so the device runs with no battery ([TI E2E](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1190474/bq25731-adjustable-vsys_min-and-power-path-control-questions)). BQ25731RSNR ($4.56/$2.88/$2.49, [link](https://www.digikey.com/en/products/result?keywords=BQ25731RSNR)) has **no** power path, so it is rejected. BQ25798RQMR ($5.90/$3.79/$3.30, [link](https://www.digikey.com/en/products/result?keywords=BQ25798RQMR)) has integrated FETs, a 3.3 A input limit and 1–4S; TI positions it for ≤45 W ([TI](https://www.ti.com/product/TPS25750)). |
| Charger power-stage MOSFETs, 30 V N-ch | TI | CSD17578Q3A | Digi-Key | [link](https://www.digikey.com/en/products/detail/texas-instruments/CSD17578Q3A/5015743) | 4 / 0 | 1.05 | 0.43 | 0.25 (2.5k reel) | 0.22 (7.5k) | 2,216 stk; 12 wk | Active | Four switching FETs for the buck-boost H-bridge. |
| Charger BATFET (30 V P-ch), 2.2 µH ≥15 A inductor, 2 sense resistors, bulk caps | various | TBD at schematic | — | — | 1 lot / 0 | 4.00e | 2.50e | 1.80e | 1.40e | — | — | Estimate. Do not use the CSD25404Q3: it is a 20 V part with too little margin on a 16.8 V bus. |
| Ideal-diode OR controller (Indoor input OR) | TI | LM74700QDBVRQ1 | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=LM74700QDBVRQ1) | 0 / 2 | 2.40 | 1.45 | 1.23 (3k) | 1.21 (6k) | **0 stk; 3,000 due 27-Oct-2026**; 20 wk | Active | ORs barrel and USB-C onto VSYS. The PoE+ PD output from agent D ORs onto the same rail. Alternate: Diodes AP74700QW6-7, $0.82. |
| OR N-FET for LM74700 | TI | CSD17578Q3A | Digi-Key | [link](https://www.digikey.com/en/products/detail/texas-instruments/CSD17578Q3A/5015743) | 0 / 2 | 1.05 | 0.43 | 0.25 | 0.22 | as above | Active | |
| DC barrel jack 5.5×2.1 mm, 8 A/24 V | Same Sky | PJ-063AH | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=PJ-063AH) | 0 / 1 | 1.52 | 1.10 | 0.92 (1.2k) | 0.90 (2.7k) | 18,356 stk; 17 wk | Active | Indoor only. The 24 V rating is at its limit, so add a 26 V TVS. |
| 5 V system buck, 4.5–28 V in, 6 A | TI | TPS56637RPAR | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=TPS56637RPAR) | 1 / 1 | 2.71 | 1.66 | 1.41 (3k) | 1.38 (6k) | 14,658 stk; 20 wk | Active | Feeds the SoM 5 V input, USB and peripherals. Size it with agent A/B for SoM peaks. |
| 3.3 V buck, 3.8–30 V in, 3 A | TI | TPS62933DRLR | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=TPS62933DRLR) | 1 / 1 | 1.60 | 0.95 | 0.85 | 0.77 (8k) | 63,313 stk; 20 wk | Active | Sensors, display logic, LEDs, fan. |
| Rail passives (2 inductors, caps), input TVS, PTC/fuse | various | TBD | — | — | 1 lot / 1 lot | 2.50e | 1.50e | 1.00e | 0.80e | — | — | Estimate. |
| **BATTERY (Pro only)** | | | | | | | | | | | | |
| Host battery header, 5-pos 5.0 mm blade, 7 A/contact | TE | 5787441-1 | Digi-Key | [link](https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/5787441-1/2135744) | 1 / 0 | 8.18 | 5.83 (121) | 4.71 (1,089) | 4.71 | 2,035 stk; 8 wk | Active | Laptop-style SMBus pinout: B+, B−, SMBC, SMBD, T/ID (pack present). Keyless, so it mates any keyed pack receptacle. At volume, the ACES or Amphenol FCI 10174523 families are cheaper; get a quote. |
| **Battery pack, custom smart 4S1P 21700, about 81 Wh (M58T) or 72 Wh (P50B/50S)** | Pack OEM (Shenzhen; e.g. Keeppower, Himax, Saphiion, Large Battery) | OB-BP4S1P (ours) | OEM quote | @1 reference: [Inspired Energy ND4054HD50](https://inspired-energy.com/products/details/3/117-nd4054hd50) | 1 / 0 | 167.22 (off-the-shelf SMBus 4S1P stand-in) | 95e | 57e | 35e | OEM: 6–10 wk after tooling | Custom | The cost build-up is in section 4.4. One-time costs (NRE) are separate: about $15–45k (section 4.5). Spare packs are an accessory SKU. |
| ↳ in-pack: cell, 21700, 5.65 Ah nom. (5.8 Ah label), 12.5 A | LG Energy Solution | INR21700-M58T | United Lithium / CityLion | [US](https://unitedlithium.us/products/lg-inr21700-m58t-5800mah-21700-battery-high-capacity), [EU](https://citylion.pl/en/lg-m58t-inr21700-m58t-5800mah-12-5a-cells/) | (4 in pack) | 5.99 | €6.84 | €6.27 (1000+) | ~2.80 pallet ([QB](https://queenbattery.com.cn/our-products/1316-lg-21700-m58t-inr21700m58t-2c-12a-5800mah-battery-cell-36v.html), historic) | Distributor stock varies | Active | Nominal 5,650 mAh per [RPE-NA](https://rpe-na.com/products/lg-inr21700-m58t-li-ion-battery-5650mah-3-6v-21700-cell). Buy through an authorized LGES channel because counterfeits are common. |
| ↳ in-pack alt cell: 5.0 Ah, 60 A | Molicel | INR-21700-P50B | Stortronics / Battery Junction / NKON | [link](https://stortronics.com/lithium-batteries/molicel-inr21700-p50b-3-6-volt-5000mah-60a-lithium-ion-cell-pre-order/) | (4) | 9.20 | 7.89 | 7.36 (1000+) | quote | Pre-order, ships Nov 2026 | Active | Power cell, more than this product needs. Gives a 72 Wh pack. [Battery Junction](https://www.batteryjunction.com/products/molicel-inr21700-p50b) $9.25 at 200+; [NKON](https://www.nkon.nl/en/molicel-inr21700-p50b-5000mah-50a.html) €5.29 at 200. |
| ↳ in-pack alt cell: 5.0 Ah, 25 A | Samsung SDI | INR21700-50S | 18650 Battery Partners / TheBatteryShop | [link](https://18650batterypartners.com/products/samsung-50s-21700-5000mah-25a) | (4) | 6.99 | 4.79 (200 MOQ) | €4.18 (300) ([link](https://thebatteryshop.eu/Samsung-INR21700-50S-Li-Ion-battery-cell)) | quote | Pre-order | Active | Cheapest Tier-1 5 Ah option. Gives a 72 Wh pack. |
| ↳ in-pack: fuel gauge + protection controller, 1–4S, SHA-1 auth | TI | BQ40Z50RSMR-R2 | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=BQ40Z50RSMR-R2) | (1) | 4.42 | 2.78 | 2.40 (3k reel) | 2.40 | **151 stk**; 20 wk | Active | The gauge stays with the pack, so learned capacity survives a swap. SHA-1 authentication blocks counterfeit packs. For 5S, use BQ40Z80RSMR (2–7S): $6.43/$4.15/$3.62 ([link](https://www.digikey.com/en/products/result?keywords=BQ40Z80RSMR)). |
| ↳ in-pack: secondary over-voltage protector, 2–5S | TI | BQ771807DPJR (pick the threshold variant) | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=BQ7718) | (1) | 1.29 | — | 0.62 (3k) | 0.62 | Stocked | Active | Drives a chemical fuse (e.g. Dexerials SFH series). The pack OEM sources this part. |
| ↳ in-pack: pack receptacle, 5-pos 5.0 mm | TE | 787439-1 | Digi-Key | [link](https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/787439-1/295176) | (1) | 5.73 | 4.14 (99) | 3.49 (1,089) | 3.29 (2,574) | 5,773 stk; 23 wk | Active | Mates with 5787441-1. Uses right-hand keying. |
| (alt, dumb-pack architecture) 2–5S AFE protector | TI | BQ76905RGRR | Digi-Key | [link](https://www.digikey.com/en/products/detail/texas-instruments/BQ76905RGRR/22119523) | 0 | 1.95 | — | 1.02 | 0.98 (3k) | Tight; 26 wk | Active | Only needed if the gauge were moved to the host (BQ34Z100PWR-R2 $5.42/$3.46/$3.04, [link](https://www.digikey.com/en/products/result?keywords=BQ34Z100PWR-R2)). **Not recommended**: a host-side gauge loses its learned state at every swap. The MAX17205G+T ($6.87, [link](https://www.digikey.com/en/products/result?keywords=MAX17205G%2BT)) is listed by Digi-Key as 2–3 cell, so it does not fit 4S. |
| Battery latch, spring, door/pocket seal hardware | Mech (molded) | — | — | — | 1 lot / 0 | 1.00e | 0.80e | 0.40e | 0.25e | — | — | Estimate. The latch is molded into the pack, camera-battery style. A gasket on the connector boss keeps the electronics bay IP54 with the pack out. |
| **DISPLAY (Pro only)** | | | | | | | | | | | | |
| 2.4" transflective IPS TFT 240×320, SPI, ST7789-T3, −20…+70 °C | VIEWE | UEED024QV-RH40-A003 | viewedisplay.com | [link](https://viewedisplay.com/product/2-4-inch-240320-transflective-sunlight-readable-and-super-low-power-tft-lcd-module-with-mcu-8-16bit-spi-interface/) | 1 / 0 | 14.59 | 12e | 9e | 7e | Online stock; quote for volume | Vendor-defined (get a longevity letter) | **Recommended.** Readable in full sun with the backlight off, and the backlight still covers dark simulator bays. Qualified second source: Leadtek LTK024QVHLM17-V2, 2.4" transflective IPS SPI, 25 % reflectivity, quote only ([link](https://www.leadtekdisplay.com/24-inch-transflective-display-p-2849.html)). |
| (alt) 2.8" IPS 240×320, 1,000 nit, SPI, ST7789VI, −20…+70 °C | Newhaven | NHD-2.8-240320AF-CSXP-F | Newhaven | [link](https://newhavendisplay.com/2-8-inch-ips-tft-without-touchscreen/) | 0 (alt) | 18.45 | quote | quote | quote | In stock | Active | Western-supported fallback with the same ST7789 driver. The backlight draws about 0.5–1 W in sun. Other options: the 2.4" NHD-2.4-240320AF-CSXP at $13.94; Orient Display 2.4" 1,000-nit at $9.32 ([link](https://orientdisplay.com/tft-displays/tft-panels/sunlight-readable-ips/)); Newhaven 3.5" 640×480 MIPI-DSI 950-nit NHD-3.5-640480EF-MSXP at $26.90 ([link](https://newhavendisplay.com/3-5-inch-ips-tft-mipi-interface-without-touchscreen/)). |
| (alt) 2.7" reflective memory LCD 400×240, SPI, no backlight | Sharp | LS027B7DH01A | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=LS027B7DH01A) | 0 (alt) | 29.29 | 23.61 (10) | 19.06 (400) | quote | 2,738 stk; 28 wk | Active | Best sunlight contrast and µW power, but **unreadable in dark simulator rooms** without a front light. Not chosen. |
| Display FPC connector, 40-pos 0.5 mm ZIF | Hirose | FH12-40S-0.5SH(55) | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=FH12-40S-0.5SH(55)) | 1 / 0 | 3.55 | 2.57 | 2.26 | 1.98 (4k) | 19,148 stk; 16 wk | Active | Matches the Newhaven pinout. Confirm the VIEWE tail and pin count; cheaper JUSHUO/Kinghelm equivalents exist at volume. |
| Backlight PWM FET + display passives | various | — | — | — | 1 lot / 0 | 0.50e | 0.30e | 0.20e | 0.15e | — | — | Estimate. |
| Cover lens: chemically strengthened glass, AR/AF, IR-cut, bonded | Lens vendor | custom | quote | — | 1 / 0 | 15e | 8e | 5e | 3.5e | — | Custom | Estimate. Coordinate with the mechanical/enclosure agent and check this item isn't counted twice. |
| **SENSORS** | | | | | | | | | | | | |
| 3-axis inclinometer, SPI, ±0.005 °/°C offset tempco, 0.001 °/√Hz | Murata | SCL3300-D01-1 | Digi-Key | [link](https://www.digikey.com/en/products/detail/murata-electronics/SCL3300-D01-1/9950616) | 1 / 0 | 40.12 | 31.73 (100 T&R) | 30.47 (300) | 22e (quote) | 1,546 stk; 17 wk | Active | **Pro leveling.** Spec source: [Murata](https://www.murata.com/en-us/products/sensor/inclinometer/overview/lineup/scl3300). The Indoor PCB has the footprint but leaves it unpopulated (DNP). |
| 6-axis IMU, accel + gyro | Bosch | BMI323 | Digi-Key | [link](https://www.digikey.com/en/products/detail/bosch-sensortec/BMI323/16719593) | 0 / 1 | 3.91 | 2.92 | 2.60 | 2.43 (5k) | 31,432 stk; 16 wk | Active | **Indoor leveling** after per-unit factory calibration, plus bump/knock detection. Avoid the **ICM-42688-P**: $4.86/$3.66/$3.28/$3.07 but **0 stk and 45-wk lead, restock Aug 2027** ([link](https://www.digikey.com/en/products/detail/tdk-invensense/ICM-42688-P/10824934)). The BMI270 ($4.23, 52k stk) is OK as an alternate. |
| Barometer, gel-filled, water-resistant | Bosch | BMP585 | Digi-Key | [link](https://www.digikey.com/en/products/detail/bosch-sensortec/BMP585/19522589) | 1 / 1 | 4.54 | 3.41 | 3.05 | 2.88 (4k) | 11,371 stk; 16 wk | Active | The BMP390 ($3.58/$2.67/$2.38/$2.16, [link](https://www.digikey.com/en/products/detail/bosch-sensortec/BMP390/16164575)) and BME280 ($4.35/$3.27/$2.92/$2.66, [link](https://www.digikey.com/en/products/detail/bosch-sensortec/BME280/6136306)) are both **0 stock, no ETA**. The BME688's gas sensor is not needed. |
| Temp/RH sensor with PTFE membrane cover (IP67) | Sensirion | SHT45-AD1F-R2 | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=SHT45-AD1F-R2) | 1 / 1 | 6.51 | 4.95 | 4.53 | 4.29 (2.5k) | 16,397 stk; 12 wk | Active | ±0.1 °C / ±1 %RH class. Mount it in a vented pocket on a slotted PCB tongue, away from the SoC. The SHT45-AD1B-R2 (no filter, $6.11) is for Indoor-only cost-down. |
| **THERMAL** | | | | | | | | | | | | |
| 40×40×10 mm blower, 5 V, IP55, 140 Pa, tach | Delta | BFB0405HHA-TZP4 | Digi-Key / Octopart | [DK](https://www.digikey.com/en/products/result?keywords=BFB0405HHA-TZP4), [Octopart](https://octopart.com/part/delta/BFB0405HHA-TZP4) | 1 / 0 | 15.31 (Newark) | 14.12 (Onlinecomponents/Master) | 13.78 (DK, 1,280 MOQ) | 10.91 (Avnet, 1,280 bulk) | **DK: not stocked; 40 wk** | Active | Life is 30,000 h at 40 °C (Delta rating; confirm the L10 basis). Its high static pressure suits a fin-stack duct. Alternate IP55 axial: Orion OD4010-05HB55, $20.13/$16.73/$14.52 at 500 ([Newark](https://www.newark.com/orion-fans/od4010-05hb55/dc-fan-ball-6cfm-40mmx10-5mm-0/dp/41AM5813)), out of stock. Noctua NF-A4x10 5V PWM is about $15.95 ([builds.gg](https://builds.gg/parts/nf-a4x10-5v-pwm-4133)), MTTF >150,000 h, but **IP50 only** ([Noctua](https://www.noctua.at/en/products/nf-a4x10-5v-pwm/features)) and retail-channel. |
| 40×40×10 mm axial, 5 V, MagLev/Vapo, 8 CFM | Sunon | MF40100V1-1000U-A99 | Digi-Key | [link](https://www.digikey.com/en/products/detail/sunon-fans/MF40100V1-1000U-A99/6198732) | 0 / 1 | 4.87 | 3.16 | 2.74 (800) | 2.74 | 14,187 stk; 26 wk | Active | **Indoor fan.** Life is 70,000 h at 40 °C. No IP rating, which is fine indoors. |
| SoM heatsink: proto stock part / production custom heat-pipe + fin stack | Radxa (proto) / thermal vendor (prod) | Heatsink 5540B / custom | Arace / quote | [link](https://arace.tech/products/heatsink-5540b-for-cm5) | 1 / 1 | 7.49 | 7.49 | 9e | 6e | Stock | Active / custom | The proto part depends on which SoM agent B picks (RPi CM5 cooler is $5 list, [link](https://www.raspberrypi.com/products/cooler/)). A vapor chamber ($10–20e) isn't needed for an 8–12 W SoC if a heat pipe reaches the duct. |
| Thermal interface pad, 6.2 W/m·K | t-Global | TG-A6200-40-40-1.0 | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=t-global%20TG-A6200) | 1 / 1 | 2.73 | 1.50e | 0.60e | 0.35e | Stock | Active | At volume, die-cut from sheet. Laird Tflex HR600 1.0 mm sheet, 228.6×228.6 mm (A16104-04), is $38.28 ([link](https://www.digikey.com/en/products/result?keywords=Tflex%20HR600)) and yields about 30 pads of 40×40. Bergquist TGP is equivalent. |
| **UI** | | | | | | | | | | | | |
| Sealed tact switch IP67, 3.5 N (power / select / mode) | C&K (Littelfuse) | KSC241JLFS | Digi-Key | [WEC](https://www.digikey.com/en/products/detail/wec/KSC241JLFS/27533238), [LF](https://www.digikey.com/en/products/detail/wee/KSC241JLFS/26327478) | 3 / 1 | 0.38 | 0.38 | 0.28 (2k) | 0.27 (6k) | 6,000 stk (marketplace) | Active | Sits under an overmolded silicone/TPU key membrane (mechanical agent). Indoor has one pair/reset button. |
| RGB status LED, PLCC-4 3528, common anode | Würth | 150141M173100 | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=150141M173100) | 1 / 2 | 0.50 | 0.43 | 0.34 (2k) | 0.34 | 30,274 stk; 13 wk | Active | Light-pipe to housing. Indoor uses two (power plus status). |
| Magnetic buzzer, 5 V, 4 kHz, 100 dB @10 cm | Same Sky | CMT-8540S-SMT-TR | Digi-Key | [link](https://www.digikey.com/en/products/result?keywords=CMT-8540S-SMT-TR) | 1 / 1 | 4.13 | 2.44 | 1.92 | 1.72 (5k) | 20,504 stk; 16 wk | Active | Place behind an acoustic membrane vent (Gore/Saati) to keep IP54. A cheaper piezo is possible. |
| **EXTERNAL SUPPLIES (box contents, not on PCB)** | | | | | | | | | | | | |
| 65 W USB-C PD GaN charger, private label, UL/CE/FCC/PSE | Shenzhen OEM (e.g. Merryking, Wandkey, L Lab) | OB-PSU65 (ours) | Made-in-China / Global Sources | [Global Sources](https://www.globalsources.com/manufacturers/usb-c-65w-charger.html), [MIC](https://www.made-in-china.com/products-search/hot-china-products/Wholesale_65w_Charger.html) | 1 / 0 (optional) | 65.90 (Mean Well NGE100U, [Jameco](https://www.jameco.com/z/NGE100U-MEAN-WELL-100W-4-Port-GaN-Fast-USB-Charger-USA-Plug-Version_2499471.html)) | 10.30 ([Miccell](https://www.alibaba.com/product-detail/OEM-ODM-Phone-Charger-PD-20w_60773564269.html), certs to verify) | 13.00 (UL/CE/FCC/PSE, $13–16 at 3k MOQ) | 13.00 | 15–30 days | — | $8.50–9.00 at 1k without a UL mark. Verify UL file numbers in UL Product iQ. **Mean Well has no 65 W USB-C model**: the NGE65 is barrel-only and the NGE100U (100 W PD) is the nearest. Check whether EU unbundled-charger rules apply. |
| 24 V / 60 W desktop adapter, 5.5×2.1 mm, Level VI | Mean Well | GST60A24-P1J | Digi-Key | [link](https://www.digikey.com/en/products/detail/mean-well-usa-inc/GST60A24-P1J/7703715) | 0 / 1 | 19.40 | 17.10 (25) | 15e | 13.5e | 707 stk; 17 wk | Active | Approvals: cULus, CE, CB, PSE, KC, CCC, RCM, BSMI, BIS. Alternate: NGE65I24-P1J (interchangeable plugs) at about €17.52 at RS ([link](https://benl.rs-online.com/web/p/ac-dc-adapters/0634228)); it is no longer at Digi-Key. Indoor can also take any 20 V USB-C PD charger. |

### 2.1 Subsystem totals (power + battery + display + sensors + thermal + UI), per unit

Calculated from the rows above, including estimate ("e") rows.

| Configuration | @1 | @100 | @1k | @10k |
|---|---|---|---|---|
| **Pro, on-board + 1 battery pack** | **$318** | **$207** | **$155** | **$113** |
| Pro, excluding battery pack | $151 | $112 | $98 | $78 |
| Pro + bundled 65 W USB-C PD charger | $384 | $217 | $168 | $126 |
| **Indoor, on-board** | **$57** | **$40** | **$36** | **$31** |
| Indoor + bundled 24 V adapter | $76 | $57 | $51 | $45 |

The biggest cost drivers in the Pro at 1k are:
- battery pack: $57 (37 %)
- SCL3300: $30
- Delta IP55 blower: $14
- display, lens and connector: about $16
- heatsink: $9

Cost-down levers at 10k:
- SCL3300 to a volume quote, or BMI323 with temperature calibration if validation passes: −$8 to −$20
- Chinese pack connector pair instead of TE: about −$6 across both sides
- Delta direct quote: −$3

---

## 3. Architecture (how the parts fit)

```
 USB-C (USB4720, IP67) ─► TPS25751D (PD sink, 5–20 V, int. 7 A switch) ─► VBUS_IN
                                                                       │
   Pro:  VBUS_IN ─► BQ25730 NVDC buck-boost (4× CSD17578Q3A, L, BATFET) ─► VSYS (≈11–16.8 V)
                                   │                         ▲
                                   └─ BATFET ── 5787441-1 ◄── smart pack (BQ40Z50 + BQ7718, SMBus)
   Indoor: VBUS_IN ─► LM74700+FET ─┐
           PJ-063AH 24 V ─► LM74700+FET ─┼─► VSYS (≈12–24 V)   (PoE+ PD output from agent D also ORs here)
                                   │
   VSYS ─► TPS56637 5 V/6 A (SoM, USB, fan) ─► TPS62933 3.3 V/3 A (sensors, display, LEDs)
   VSYS ─► strobe capacitor-bank charger (agent C/strobe slice; current-limited, keep off 5 V rail)
```

- **Running from USB-C with no battery.** The BQ25730 regulates VSYS to VSYS_MIN through the BATFET when the battery is absent or flat. The Pro therefore boots and runs from a 65 W adapter with the pack removed. A pack can also be swapped while on USB-C power without rebooting.
- **Charge budget.** At 20 V × 3.25 A = 65 W input with 12–15 W of system load, about 48 W is left for the battery. That is about 3.2 A at 15 V, roughly 0.55C on a 5.65 Ah cell, for a 0→100 % charge in about 2 h. **Program the charge current to the cell datasheet limit** and apply JEITA temperature limits in both the BQ40Z50 and the BQ25730. **Charging is inhibited above 45 °C cell temperature**, so the pack bay must be thermally separated from the SoC duct.
- **Why external FETs instead of the BQ25798?** At 65 W through a 4×4 mm QFN with integrated FETs, roughly 1.5–3 W of loss sits in one package inside a 40 °C sealed box. TI's own pairing guidance puts integrated-FET chargers at ≤45 W and the controller class above 45 W ([TI TPS25750 page](https://www.ti.com/product/TPS25750)).
- **Indoor = same PCB.** The variant leaves out the BQ25730 and its power stage, the BATFET, the 5787441-1 header, the display FPC, two of the three buttons and the SCL3300. It adds the PJ-063AH, 2× LM74700 with FETs, a 0 Ω link from the OR output to VSYS, a second RGB LED and the BMI323. Every downstream regulator accepts 4.5–28 V, so 24 V barrel, 20 V PD and 12 V PoE+ outputs all work. The TPS25751D stays fitted so Indoor can run from any ≥45 W USB-C PD charger.

---

## 4. Battery approach

### 4.1 Standard swappable formats evaluated

| Format | Real capacity | Certs on major brands | Mating plate / connector | Price per pack | Own-brand OEM at volume? | Verdict |
|---|---|---|---|---|---|---|
| **Sony NP-F (L-series) 7.2 V** | NP-F970 7.8 Ah ≈ **56 Wh** (SmallRig 4073: 56.16 Wh, [link](https://www.smallrig.com/SmallRig-NP-F970-Camera-Battery-4073.html)). The 10.5 Ah versions claim 76 Wh (SmallRig 4267: 76.3 Wh, [B&H](https://www.bhphotovideo.com/c/product/1785871-REG/smallrig_4267_l_series_np_f970_usb_c.html)). Sony OEM is 6.3 Ah. | SmallRig lists FCC/UL/CE but **no UN38.3/IEC 62133 on the NP-F pages**. | No Tier-1 connector MPN. NP-F "dummy plates" come from AliExpress-grade suppliers. Sony InfoLithium comms are proprietary, so state of charge can't be read from third-party packs. | Neewer TP-F970 10.5 Ah $53.99–59.99 ([Best Buy](https://www.bestbuy.com/product/neewer-10500mah-np-f970-replacement-battery-with-20w-usb-c-pd-fast-charging-gray/CZLV9F2FLR)); Watson 74 Wh $87.49 ([B&H](https://www.bhphotovideo.com/c/product/1468019-REG/watson_b_4238_np_f970_lithium_ion_battery_pack.html)); Sony OEM $168 ([AcePhoto](https://acephoto.net/cameras/np-f970-battery-rech-for-handycam/)) | Yes (Rolux etc.) | **Reject.** Labeled capacities are unreliable, there is no gauge, the open contacts can't be made IP54, and the 7.2 V bus doubles current. |
| **V-mount / micro V-mount 14.8 V** | SmallRig VB50 50 Wh, VB99 99 Wh | **Yes.** SmallRig VB99/VB99 SE claim UN38.3, IEC 62133, UL2054 and UL62368 ([link](https://www.smallrig.com/VB99-SE-mini-V-Mount-Battery-4608.html)). | Mechanical plates: SmallRig mini plate $22.99 ([Walmart](https://www.walmart.com/c/kp/v-mount-battery-plate)). Powered plates such as Paralinx 11-1221/11-1222 ([link](https://www.paralinx.net/store/v-mount-battery-plate)) and Hollyland $119.99. No industry-standard connector MPN. | VB50 $129.99 ([B&H](https://www.bhphotovideo.com/c/product/1858099-REG/smallrig_3579b_vb50_mini_v_mount_battery.html)); VB99 $159.99 ([B&H](https://www.bhphotovideo.com/c/product/1853315-REG/smallrig_3580b_vb99_mini_v_mount_battery.html)); Core SWX XCell 99 $159 sale ([link](https://coreswx.com/collections/v-mount-batteries)) | Yes (Rolux, FXLion) | **Reject as the primary pack.** A 99 Wh pack weighs about 0.6 kg, the plate is about 100×70 mm, the plate contacts aren't sealed and golfers don't own V-mounts. **Support it for free:** these packs have 65–100 W USB-C PD outputs, so they can power the Pro through its USB-C port. |
| **Makita 18V LXT (tool packs)** | BL1850B 18 V 5 Ah = 90 Wh | Yes (Makita) | Only the service part 643852-2 terminal ($3.10–6.15, [RepairClinic](https://www.repairclinic.com/PartDetail/Terminal/643852-2/4302474)), which isn't sold as an OEM component. Third-party mounts are DIY grade. | $139–169 ([Walmart](https://www.walmart.com/ip/Makita-BL1850B-Battery-Li-Ion-5-Ah-90-Wh-for-Makita-DCS553-DGA514-DGA901-DHP482-DHS630-DLW140-DLX3179-DML806-DML815-LXT-DBN500/790286651), [Home Depot](https://www.homedepot.com/p/Makita-18V-LXT-Lithium-Ion-High-Capacity-Battery-Pack-5-0Ah-with-Fuel-Gauge-BL1850B/206607848)) | No (trademark/patent; the ecosystem is split across Makita/DeWalt/Milwaukee) | **Reject.** It also carries legal risk. |
| **Canon LP-E6NH** | 7.2 V × about 2.1 Ah ≈ 16 Wh class | — | — | not priced | — | **Reject on capacity.** It would take 4–5 packs. |

### 4.2 Off-the-shelf "industry smart battery" (a middle path)

The **Inspired Energy ND4054HD50** is a 4S1P 21700 SMBus pack: 14.4 V, 5 Ah, 72 Wh class, IP65, push-button LED gauge, pull tab. It costs **$167.22 at qty 1–11** ([link](https://inspired-energy.com/products/details/3/117-nd4054hd50)). Its sister model ND4054QE50 is 94.9×96.6×27.3 mm and carries IEC/UL/CSA 62133-2, BIS, KC and PSE ([link](https://inspired-energy.com/products/battery-packs/n-series-batteries/details/3/260-nd4054qe50)). Large Battery 41AQ530 is an equivalent pack.

This is the **best EVT/pilot pack**: it is certified on day 1 and needs no tooling. It is too expensive and generic (not branded or shaped to our housing) for production.

### 4.3 Recommendation: custom smart pack

**Custom 4S1P 21700 smart pack.** It contains:
- **LG M58T** cells (second sources P50B / 50S in the same housing)
- **BQ40Z50-R2** gauge and primary protection
- **BQ7718xx** secondary OVP with chemical fuse
- **TE 787439-1** receptacle
- a 2-shot molded housing with an integral latch and a seal lip

It is built by a Shenzhen pack OEM that holds ISO 9001 and UN38.3/IEC 62133 capability. Keeppower, Himax, Saphiion and Large Battery all advertise SMBus 4S1P 21700 packs.

Why this wins:
1. It is the only option that is IP54-capable, branded and authenticatable (SHA-1, so no cloned packs).
2. It keeps the gauge with the pack, so a swap doesn't lose learned capacity.
3. It is about **$35 at 10k**, compared with $130–170 for V-mount or tool packs.
4. It complies with **EU Battery Regulation Art. 11** if it can be removed without tools or with commercially available tools. Ours is a tool-less latch.

Also plan for the Art. 11 duty to keep **spares available for at least 5 years after the last unit is sold**, and for the battery labelling/QR requirements. Confirm both with the regulatory agent.

### 4.4 Custom pack cost build-up (estimate, per pack)

| Element | @1k | @10k | Basis |
|---|---|---|---|
| 4 × M58T cells | $26 (≈€6.27×4) | $14 (≈$3.50×4, factory/authorized-distributor contract) | [CityLion](https://citylion.pl/en/lg-m58t-inr21700-m58t-5800mah-12-5a-cells/), [QueenBattery pallet ref](https://queenbattery.com.cn/our-products/1316-lg-21700-m58t-inr21700m58t-2c-12a-5800mah-battery-cell-36v.html) |
| BMS PCBA (BQ40Z50 $2.40 + BQ7718 $0.62 + 2 FETs + chemical fuse + NTC + PCB + SMT) | $7 | $5 | Digi-Key rows above |
| Pack receptacle (TE 787439-1, or a Chinese equivalent at volume) | $3.50 | $3.30 (≈$1 Chinese) | Digi-Key |
| Molded housing + seal + latch spring | $4 | $2.50 | Molding at $0.50–5.00 per part ([Zetar](https://zetarmold.com/injection-mold-price-list-2026/)) |
| Nickel strip, insulation, label, packaging | $2 | $1.50 | estimate |
| Assembly, aging, test, end-of-line (EOL) gauge programming | $5 | $3.50 | estimate |
| OEM margin (~18–20 %) | $9.50 | $5.50 | Pack quote structure ([PackForge](https://packforgeenergy.com/blogs/battery-insights/moq-lead-times-and-pricing-what-to-expect-when-sourcing-custom-battery-packs)) |
| **Total** | **≈ $57** | **≈ $35** | Sanity check: a bare 4S P50B 72 Wh pack with no PCB is $88 retail ([BatterySpace](https://www.batteryspace.com/Custom-Lithium-21700-Battery-14.4V-5000mAh-72Wh-NO-PCB-2x2SQ.aspx)) |

At @100 (pilot, soft tool) the estimate is about $95.

### 4.5 One-time costs (NRE) for the custom pack

| Item | Cost | Source |
|---|---|---|
| UN38.3 (≤100 Wh) | $1,700 per model at JJR Lab (China); $2k–7k typical | [JJR](https://www.jjrlab.com/news/how-much-does-un383-testing-cost.html), [Ufine](https://www.ufinebattery.com/blog/essential-guide-to-battery-certification-types-costs-timeframes-and-standards/) |
| UN38.3 at a US/EU lab | $3k–8k, 4–8 weeks, about 16 sample packs | [Lithium Battery Co.](https://www.lithiumbatterycompany.com/blog/lithium-battery-pack-certifications-ul-iec-un38-mil-std) |
| IEC 62133-2 (CB) and optional UL 2054 | about $5k–20k+ | same sources |
| Housing mold (P20, 1–2 cavity, 2-shot seal) | $5k–15k (estimate) | Zetar price list |
| BMS design and BQ40Z50 dataflash/chemistry ID characterization | $1.5k–5k (estimate) | — |
| **Total** | **≈ $15k–45k** | — |

**Changing the cell (M58T → P50B) requires a new UN38.3 test**, so qualify both variants at launch if you want real second-sourcing.

### 4.6 Runtime math (assumes 95 % usable capacity × 92 % conversion; new pack)

| Pack | Rated Wh | Delivered Wh | Runtime @12 W | Runtime @15 W |
|---|---|---|---|---|
| 4S1P 5.0 Ah (P50B / 50S) | 72 | 63 | 5.2 h | 4.2 h |
| **4S1P 5.65 Ah (M58T), recommended** | **81** | **71** | **5.9 h** | **4.7 h** |
| 5S1P 5.0 Ah (P50B), BQ40Z80 gauge | 90 | 79 | 6.6 h | 5.2 h |
| (limit) | 99 | 87 | 7.2 h | 5.8 h |

At 80 % state of health, every runtime is 20 % shorter. The 5S1P is the fallback if measured average draw is ≥14 W. The BQ25730 supports 5S and the BQ40Z80 is drop-in on firmware.

---

## 5. External power supplies

- **Pro (65 W USB-C PD).** Bundle or recommend a private-label 65 W GaN charger. Price points:
  - $8.50–9.00 at 1k MOQ ([Global Sources](https://www.globalsources.com/manufacturers/usb-c-65w-charger.html))
  - $13–16 with a full UL/CE/FCC/PSE set at 3k MOQ ([Made-in-China](https://www.made-in-china.com/products-search/hot-china-products/Wholesale_65w_Charger.html))

  Certificates may need to be re-issued under our brand. Verify UL and FCC IDs yourself, and treat ETL-only listings separately. Mean Well does not make a 65 W USB-C PD wall unit. The NGE65 series is barrel-only, and the NGE100U is a 100 W PD unit at $65.90 ([Jameco](https://www.jameco.com/z/NGE100U-MEAN-WELL-100W-4-Port-GaN-Fast-USB-Charger-USA-Plug-Version_2499471.html)). Any ≥65 W PD charger the customer owns, or a V-mount/power bank with a PD output, will also work.
- **Indoor (24 V barrel).** Mean Well **GST60A24-P1J** at $19.40, falling to $17.10 at 25 ([Digi-Key](https://www.digikey.com/en/products/detail/mean-well-usa-inc/GST60A24-P1J/7703715)). It is Level VI and carries cULus/CE/PSE and more. A 60 W adapter covers a 12–15 W draw plus strobe recharge with margin. A 20 V USB-C PD charger is an equally valid input.

---

## 6. Display and touch

- **Pick: 2.4" transflective IPS TFT, SPI (ST7789).** Transflective panels read *better* as sunlight gets brighter, and the backlight covers dark simulator bays. Both are needed because the Pro is used outdoors in full sun and also indoors. Specific parts:
  - VIEWE UEED024QV-RH40-A003: $14.59, −20…+70 °C
  - Leadtek LTK024QVHLM17-V2: quote, 25 % reflectivity
  - Fallback: Newhaven NHD-2.8-240320AF-CSXP-F, 1,000-nit IPS, $18.45, same controller family, so the firmware driver is shared
- **Other panels considered:**
  - **Sharp LS027B7DH01A memory LCD:** $29.29, falling to $19.06 at 400. It is ideal in sun but has no backlight, so it is rejected for indoor use.
  - **MIPI-DSI:** a 3.5" 950-nit Newhaven at $26.90 is only worth it if the SoM has a spare DSI lane and the UI needs more than status.
- **No touch.** Physical buttons are better for this product:
  - they work with gloves, wet hands and sunscreen
  - rain and dew don't cause false touches
  - a touch layer cuts transflective reflectivity
  - they cost less
  - the phone app is the rich UI
- **Heat in sun.** LCD clearing points are near the 70 °C operating limit. Use a light-colored bezel, an IR-cut cover lens and an air gap or bonded glass. Validate under a 1,000 W/m² solar simulator at 40 °C ambient.

---

## 7. Sensors

- **Leveling target ±0.1°.** 1 mg of accelerometer offset ≈ 0.057°. On the SCL3300, the offset tempco of ±0.005 °/°C gives about ±0.1° over a ±20 °C excursion from the calibration temperature, without per-unit temperature calibration. Its noise of 0.001 °/√Hz is negligible after 1 s of averaging ([Murata](https://www.murata.com/en-us/products/sensor/inclinometer/overview/lineup/scl3300)).
  - **Consumer IMUs** (BMI323, LSM6DSV, ICM-42688-P) need a per-unit multi-temperature offset calibration to stay within ±0.1° outdoors. This is fine for the temperature-stable Indoor SKU.
- **The bigger error is mounting, not the sensor.** PCB-to-chassis-to-camera boresight tolerance is typically ±0.5–1°. **Every unit needs an end-of-line (EOL) boresight/level calibration on a reference fixture whichever sensor is used.** A user "rotate 180° and re-measure" routine can cancel residual offset in the field.
- **Air density.**
  - The BMP585 (in stock, water-resistant) handles pressure; ±0.5 hPa ≈ 0.05 % density.
  - The SHT45-AD1F handles T/RH. A temperature error matters more: 1 °C ≈ 0.34 % density, so the T sensor **must** sit in a vented pocket in the intake airstream, upstream of the SoC. Cross-check against the phone's weather API.
  - The BME280 and BMP390 are out of stock at Digi-Key with no ETA.

---

## 8. Thermal

- **Architecture.** The electronics bay is sealed to IP54. The SoC sits on a heat-spreader with a heat pipe running to a fin stack in an **isolated through-duct** (IP55 fan, drainage, mesh). Only the duct sees water and dust.
- **Fan.** The Delta BFB0405HHA-TZP4 (IP55, 140 Pa, 30,000 h at 40 °C, 0.8 W) is the only 40 mm 5 V IP55 blower with distribution. **Its Digi-Key lead time is 40 weeks, so place a 1,280-pc tray order now** or qualify the Orion OD4010-05HB55. Noctua is IP50 only and doesn't suit the duct. Sunon MagLev is fine for Indoor.
- **Solar load.** 1,000 W/m² on about 0.03 m² of top surface is about 30 W absorbed on a dark housing, which is 2–3× the SoC dissipation. Use a light/white top, a sunshade lip and a top surface separated from the hot parts. This matters more than fan choice.
- **Thermal interface.** Use 1.0 mm 3–6 W/m·K gap pads: Laird Tflex HR600 or t-Global TG-A6200, die-cut. A vapor chamber isn't needed at ≤12 W if the heat-pipe path to the duct is short.

---

## 9. UI and miscellaneous

- **Buttons.** 3× C&K KSC241JLFS (IP67) under a silicone overmold. Hold power for 2 s to turn on or off.
- **Status LED.** RGB Würth 150141M173100 behind a light pipe.
- **Buzzer.** Same Sky CMT-8540S behind an acoustic vent membrane.
- **USB-C.** GCT USB4720-03-A, IP67, 5 A, gasketed board-edge mid-mount.
- **Battery interface.** TE 5787441-1 (host) to 787439-1 (pack), with the latch molded into the pack and a connector-boss gasket.
- **Pressure equalization vent.** An ePTFE vent (e.g. a Gore adhesive vent) is needed on the sealed bay so the BMP585 reads ambient pressure. Coordinate with the enclosure agent.

---

## 10. Risks (ranked)

1. **Runtime spec conflict.** 5–6 h at 12–15 W cannot be met with margin under 100 Wh. Decide on the power budget (≤12–13 W average with SoC idle between shots) or accept 4.7–5.9 h. The 5S1P 90 Wh option is the fallback.
2. **Long lead and stock gaps.**
   - BQ25730: 0 stock until Jan 2027
   - Delta IP55 blower: 40 wk
   - ICM-42688-P: 45 wk (avoid)
   - BMP390/BME280: no ETA (avoided)
   - LM74700: 0 stock until 27 Oct
   - BQ40Z50-R2: only 151 at Digi-Key
   - SCL3300: 17 wk

   Buy EVT/DVT quantities now and open TI-direct/Avnet accounts.
3. **Pack certification timeline.**
   - UN38.3 takes 3–8 weeks and IEC 62133-2 takes longer.
   - Any cell, BMS or housing change means a retest.
   - Air shipment needs the UN38.3 test summary in hand.
   - The pack OEM must hold factory capability, and we need our own test reports, not the cell vendor's.
4. **Counterfeit cells.** 21700 prices under about $4 at retail are a red flag. Contract only through authorized LGES/Molicel/Samsung channels with lot traceability.
5. **Charging at temperature.** At 40 °C ambient in full sun, the pack will exceed 45 °C unless it is thermally isolated. Charging will then pause because of the JEITA temperature limits. Design the pack bay to be shaded and away from the duct exhaust.
6. **Display supplier longevity.** VIEWE and Leadtek are small Chinese vendors. Get a longevity/PCN letter, keep the Newhaven ST7789 fallback footprint-compatible, and lock the controller family.
7. **Charger certification under our brand.** UL/PSE listings may need transfer, and Japan PSE needs a registered importer. EU charger-unbundling rules may require a no-charger SKU; confirm with the regulatory agent.
8. **Inclinometer cost.** At $30 the SCL3300 is 20 % of the Pro's non-battery subsystem. Run a DVT study comparing BMI323 with temperature calibration against SCL3300; if the IMU holds ±0.1°, the Pro saves about $25.
9. **Estimated rows ("e").** Heatsink, cover lens, latch, passives, VIEWE volume price and pack price are engineering estimates. Replace them with quotes before the 1k build.

---

## Sources (beyond the inline links)

- TI BQ25798 product page: https://www.ti.com/product/BQ25798
- TI TPS25750 (NRND, charger pairing guidance): https://www.ti.com/product/TPS25750
- TI E2E, BQ25730 vs BQ25731 power path: https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1190474/bq25731-adjustable-vsys_min-and-power-path-control-questions
- BQ76905RGRR (Digi-Key): https://www.digikey.com/en/products/detail/texas-instruments/BQ76905RGRR/22119523
- Murata SCL3300: https://www.murata.com/en-us/products/sensor/inclinometer/overview/lineup/scl3300
- Inspired Energy N-series: https://inspired-energy.com/products/battery-packs/n-series-batteries/details/3/260-nd4054qe50
- Pack-quote structure: https://packforgeenergy.com/blogs/battery-insights/moq-lead-times-and-pricing-what-to-expect-when-sourcing-custom-battery-packs
- UN38.3 cost: https://www.jjrlab.com/news/how-much-does-un383-testing-cost.html, https://www.ufinebattery.com/blog/essential-guide-to-battery-certification-types-costs-timeframes-and-standards/
- Rolux (V-mount/NP-F OEM): https://roluxbattery.com/about-us/
- Makita terminal 643852-2: https://www.ereplacementparts.com/terminal-p-719473.html
- Noctua NF-A4x10 5V PWM specs: https://www.noctua.at/en/products/nf-a4x10-5v-pwm/features
- Raspberry Pi CM5 cooler: https://www.raspberrypi.com/products/cooler/
