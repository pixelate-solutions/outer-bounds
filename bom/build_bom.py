#!/usr/bin/env python3
"""Single source of truth for the Outer Bounds BOM.

Generates:
  outer-bounds-bom.csv          master BOM (every line, both SKUs)
  cart-<vendor>.csv             order-today carts for the first build (5 Pro + 5 Indoor)
  one-time-costs.csv            tooling / NRE / certification
  bom-data.json                 data consumed by outer-bounds-bom.html

Price columns are per-unit cost of that line at a build volume:
  proto  = building ~5-10 units (qty-1 distributor pricing, small-lot fab)
  v100   = 100-unit build
  v1k    = 1,000-unit build
  v10k   = 10,000-unit build
"[est.]" in the source column marks an estimate, not a published price.
"""
import csv, json, math, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = {"pro": 5, "indoor": 5}   # first build quantities for the order carts

# fields: id, subsystem, item, mfr, mpn, vendor, url, qty_pro, qty_indoor,
#         [proto, v100, v1k, v10k], stock_lead, orderable, notes
# orderable: "now" = click-to-buy today | "quote" = vendor quote / RFQ |
#            "design" = custom part, needs our design files then a fab/molder order
L = []
def add(*a): L.append(a)

# ---------------------------------------------------------------- 1 CAMERAS & OPTICS
S = "Cameras & optics"
add("CAM-01", S, "IMX900 3.2 MP global-shutter MONO MIPI camera module (stereo top, stereo bottom, club)",
    "Vision Components", "VK000601", "Vision Components (sales@vision-components.com) / Ampheo",
    "https://www.mipi-modules.com/en/vc-mipi-flyer-02-06-26-en/", 3, 3, [230, 165, 95, 65],
    "In production; lead time on quote", "quote",
    "€109.99 @1k catalog (≈$128). PM decision: 1k column = VC/e-con OEM custom module (NRE in one-time list) ≈$95; "
    "10k column = our own IMX900 board w/ active lens alignment ≈$65. Alt now: Leopard LI-IMX900-MIPI-078H $399 (has QCS6490 driver), "
    "Vadzo Bolt-900MGS $199 @250+.")
add("CAM-02", S, "S-mount (M12) lens holder for VC module, no IR-cut", "Vision Components", "VK000057",
    "Vision Components", "https://www.mipi-modules.com/fileadmin/external/documentation/hardware/VC_MIPI_Camera_Module/index.html",
    3, 3, [12, 8, 0, 0], "Quote", "quote", "Folded into the custom module from 1k up.")
add("CAM-03", S, "M12 lens 6.1 mm f/1.8, IR-corrected, 5 MP, 1/1.8\" image circle", "Commonlands", "CIL361-F1.8-M12ANIR",
    "Commonlands", "https://commonlands.com/products/ir-corrected-6mm-m12-lens-cil361", 3, 3, [39, 28, 9, 5],
    "15 in stock (buy 30+ now)", "now",
    "1k/10k = same optical prescription from Evetar/Jinyuan volume line [est.]. Alt in stock: CIL061-F1.9-M12BNIR $39 (171 pcs).")
add("CAM-04", S, "940 nm bandpass filter, 40 nm FWHM, OD4, 7×7×0.3 mm (in lens-holder IR-cut seat)", "MidOpt (custom BN940 cut)",
    "BN940-7x7-custom", "MidOpt (RFQ)", "https://midopt.com/filters/bn940/", 3, 3, [30, 8, 2.5, 1.2],
    "4–6 wk on quote", "quote",
    "Order-today stand-in for first builds: Commonlands CBP940-070S030 $9 (930 in stock, ~80 nm FWHM, OD3). Centre ~948 nm for off-axis shift.")
add("CAM-05", S, "Camera FPC 22→22 pin 0.5 mm, 100 mm (stereo pair)", "Vision Components", "EK004418", "Vision Components",
    "https://www.mipi-modules.com/fileadmin/external/documentation/hardware/VC_MIPI_Camera_Module/index.html", 2, 2, [12, 8, 4, 2],
    "Quote", "quote", "Generic alt: Molex Premo-Flex 0150200241 (203 mm) $5.21, 1,951 in stock.")
add("CAM-06", S, "Camera FPC 22→22 pin 0.5 mm, 200 mm (club camera)", "Molex", "0150200241", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=0150200241", 1, 1, [5.21, 4.10, 3.20, 2.50], "1,951 in stock", "now",
    "Premo-Flex 22-pos 0.5 mm 203 mm, same-side contacts. Check pin-1 orientation vs VC pinout (trigger pin 17, flash pin 18).")
add("CAM-07", S, "FPC connector 22-pos 0.5 mm right-angle (carrier side)", "Hirose", "FH12-22S-0.5SH(55)", "Digi-Key",
    "https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/FH12-22S-0-5SH/583540", 3, 3, [2.57, 1.60, 1.10, 0.85],
    "18,035 in stock", "now", "Alt: TE 2-2492104-2 $0.96.")

# ---------------------------------------------------------------- 2 COMPUTE & CONNECTIVITY
S = "Compute & connectivity"
add("CPU-01", S, "Compute SOM: Qualcomm QCS6490, 8 GB + 128 GB UFS, Wi-Fi 6E 2×2 + BT 5.2 on-module, 5× 4-lane MIPI CSI",
    "Thundercomm", "C6490P-U8A-3690000", "Arrow", "https://www.arrow.com/en/products/c6490p-u8a-3690000-qcs6490/thundercomm",
    1, 1, [286.52, 228.09, 189.60, 165.00], "0 stock, 16 wk", "now",
    "PM decision over RK3588: same 1k cost once Wi-Fi is counted, lifecycle to 2036, phone-class power (helps 6 h runtime & 40 °C sealed box), "
    "12 TOPS NPU, integrated FCC/CE Wi-Fi. LGA solder-down. 10k = $149.18 @30k published, $165 [est.] @10k. "
    "Alt: Forlinx FET3588J-C+224GSE32GI (RK3588J) $489 @1 + u-blox MAYA-W266 Wi-Fi.")
add("CPU-02", S, "Wi-Fi/BT dual-band antenna, FPC, 200 mm MHF1 cable", "Ezurio", "EFB2455A3S-20MHF1", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=EFB2455A3S-20MHF1", 2, 2, [5.22, 4.50, 3.80, 3.30], "200 in stock, 12 wk", "now",
    "2×2 MIMO. Must be on Thundercomm's approved-antenna list to reuse the module grant.")
add("CPU-03", S, "U.FL/MHF1 RF receptacle (carrier side)", "Hirose", "U.FL-R-SMT-1(10)", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=U.FL-R-SMT-1(10)", 2, 2, [1.67, 1.20, 1.02, 0.89], "374k in stock", "now", "")
add("CPU-04", S, "Timing master MCU (camera triggers + strobe timing, HRTIM 184 ps, hardware fault inputs)", "STMicroelectronics",
    "STM32G474CET6", "Digi-Key", "https://www.digikey.com/en/products/detail/stmicroelectronics/STM32G474CET6/10326773",
    1, 1, [7.95, 6.20, 5.70, 5.40], "In stock (LQFP)", "now", "Do not specify the QFN (CEU6): 52 wk. Alt: RP2350A $0.99 (PIO, no hardware fault inputs).")
add("CPU-05", S, "USB 3.0 → Gigabit Ethernet controller (Indoor)", "Realtek", "RTL8153B-VB-CG", "LCSC",
    "https://www.lcsc.com/search?q=RTL8153B-VB-CG", 0, 1, [1.80, 1.30, 1.10, 0.95], "Stocked at LCSC [est. price]", "now",
    "QCS6490 SOM has no exposed RGMII PHY path; USB-GbE is mainline Linux (r8152). Needs 25 MHz crystal (in carrier misc).")
add("CPU-06", S, "RJ45 MagJack 1 GbE (Indoor)", "Pulse Electronics", "JXD1-0001NL", "Digi-Key",
    "https://www.digikey.com/en/products/detail/pulse-electronics/JXD1-0001NL/5361447", 0, 1, [7.59, 5.48, 4.66, 4.30], "620 in stock, 8 wk", "now",
    "Alt: Würth 7499111121A. PoE+ option: swap to JK0-0177NL + Silvertel AG53012 (+$14 @1k), see options.")

# ---------------------------------------------------------------- 3 IR STROBE ILLUMINATION
S = "IR strobe illumination"
add("LED-01", S, "940 nm IR LED, ±28°, 5 A pulse rated (3 boards × 8 in series)", "Vishay", "VSMA1094250", "Digi-Key",
    "https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/VSMA1094250/15786352", 24, 24,
    [2.34, 1.468, 1.379, 1.20], "4,764 in stock, 9 wk", "now",
    "Second source on a dual footprint: ams OSRAM SFH 4728AS A01 ($1.81 @1k). 10k = contract price [est.].")
add("LED-02", S, "GaN FET 100 V 65 mΩ (one per LED string)", "EPC", "EPC2036", "Digi-Key",
    "https://www.digikey.com/en/products/detail/epc/EPC2036/5224975", 3, 3, [2.10, 0.905, 0.593, 0.532], "29,108 in stock", "now", "")
add("LED-03", S, "Low-side GaN gate driver", "Texas Instruments", "UCC27611DRVR", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=UCC27611DRVR", 3, 3, [1.64, 0.913, 0.814, 0.788], "2,369 in stock", "now", "")
add("LED-04", S, "Monostable (pulse-width cap 8 µs, 300 µs hold-off, heartbeat watchdog)", "Nexperia", "74LVC1G123DC,125",
    "Digi-Key", "https://www.digikey.com/en/products/detail/nexperia-usa-inc/74LVC1G123DC-125/5221579", 7, 7, [0.48, 0.30, 0.22, 0.18],
    "In stock", "now", "PM swap: TI SN74LVC1G123DCUR was 0 stock / $0.83 @1k. Eye-safety-critical part.")
add("LED-05", S, "Over-current comparator (ends pulse at ~6.5 A)", "Texas Instruments", "TLV3201AIDCKR", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=TLV3201AIDCKR", 3, 3, [1.81, 1.014, 0.906, 0.878], "0 stock until Nov, 20 wk", "now", "")
add("LED-06", S, "Current-sense resistor 0.1 Ω 2010", "Vishay Dale", "WSL2010R1000FEA", "Digi-Key",
    "https://www.digikey.com/en/products/detail/vishay-dale/WSL2010R1000FEA/712538", 3, 3, [0.88, 0.352, 0.315, 0.262], "5,248 in stock", "now", "")
add("LED-07", S, "Local reservoir 100 µF 50 V hybrid polymer", "Panasonic", "EEH-ZA1H101P", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=EEH-ZA1H101P", 3, 3, [2.05, 0.951, 0.655, 0.624], "0 stock, 37 wk", "now",
    "Long lead: qualify EEH-ZU1H221V (220 µF) now.")
add("LED-08", S, "Loop capacitor 2.2 µF 100 V X7R 1210", "KEMET", "C1210C225K1RACTU", "Digi-Key",
    "https://www.digikey.com/en/products/detail/kemet/C1210C225K1RACTU/1950689", 12, 12, [0.687, 0.399, 0.326, 0.30], "197k in stock", "now", "")
add("LED-09", S, "NTC 10 k 0402 (LED board temperature)", "Murata", "NCU15XH103F60RC", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=NCU15XH103F60RC", 3, 3, [0.12, 0.077, 0.064, 0.052], "211k in stock", "now", "")
add("LED-10", S, "JST GH 8-pos header (3 on LED boards, 3 on carrier)", "JST", "BM08B-GHS-TBT", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=BM08B-GHS-TBT", 6, 6, [0.50, 0.325, 0.276, 0.246], "54,619 in stock", "now", "")
add("LED-11", S, "LED-board cable assembly (GHR-08V-S + SSHL crimps)", "JST / harness house", "GHR-08V-S cable assy", "Harness CM (RFQ)",
    "https://www.digikey.com/en/products/result?keywords=GHR-08V-S", 3, 3, [4.00, 1.50, 0.90, 0.70], "[est.]", "quote", "Pre-crimped JST cables work for first builds.")
add("LED-12", S, "Strobe bus boost controller (10 W input-limited = eye-safety cap)", "Texas Instruments", "LM5155DSSR", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=LM5155DSSR", 1, 1, [2.21, 1.335, 1.219, 1.096], "0 stock until 21 Dec, 20 wk", "now", "Alt: LT3757.")
add("LED-13", S, "Boost FET 60 V logic-level", "Texas Instruments", "CSD18543Q3A", "Digi-Key",
    "https://www.digikey.com/en/products/detail/texas-instruments/CSD18543Q3A/6588881", 1, 1, [1.39, 0.575, 0.448, 0.322], "1,006 in stock", "now", "")
add("LED-14", S, "Boost Schottky 100 V 3 A", "Nexperia", "PMEG10030ELPX", "Digi-Key",
    "https://www.digikey.com/en/products/detail/nexperia-usa-inc/PMEG10030ELPX/5436251", 1, 1, [0.79, 0.30, 0.184, 0.184], "112k in stock", "now", "")
add("LED-15", S, "Boost inductor 10 µH 6 A sat", "Bourns", "SRP7028A-100M", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=SRP7028A-100M", 1, 1, [1.10, 0.742, 0.610, 0.502], "17,967 in stock", "now", "")
add("LED-16", S, "Bulk strobe capacitor 470 µF 50 V aluminium", "Panasonic", "EEE-FK1H471AM", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=EEE-FK1H471AM", 2, 2, [2.91, 1.305, 1.046, 1.0], "1,203 in stock, 37 wk", "now", "17 mm tall: check enclosure height.")
add("LED-17", S, "Strobe misc (AND gates, RC, TVS, bleed FET, feedback DAC, resistors)", "various", "lot", "Digi-Key / LCSC",
    "", 1, 1, [5.50, 2.40, 1.30, 0.95], "[est.]", "now", "Itemised in the schematic BOM.")

# ---------------------------------------------------------------- 4 RADAR
S = "Radar (helper sensor)"
add("RAD-01", S, "24 GHz CW I/Q radar module, FCC/ISED/TELEC module grant (rear head = club, down-range head = ball)",
    "InnoSenT", "80.00000346 (SMR-333)", "Digi-Key", "https://www.digikey.com/en/products/detail/innosent-gmbh/80-00000346/10419768",
    2, 2, [19.10, 15.10, 13.80, 11.50], "2,125 in stock, 16 wk", "now",
    "FCC UXS-SMR3X3, 24.150–24.250 GHz. Backup: InnoSenT IPS-354 (80.00000356) $49.20 @100. Data never fused with cameras (patent design-around).")
add("RAD-02", S, "Quad op-amp, IF amplifier / band-pass", "Texas Instruments", "TLV9064IPWR", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=TLV9064IPWR", 2, 2, [1.73, 1.03, 0.93, 0.80], "0 stock until 5 Nov", "now", "Alt in stock: ADI AD8619.")
add("RAD-03", S, "2-ch simultaneous 24-bit ADC 64 kS/s (I + Q)", "Texas Instruments", "ADS131M02IPWR", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=ADS131M02IPWR", 2, 2, [4.51, 2.84, 2.53, 2.43], "3,708 in stock", "now", "")
add("RAD-04", S, "Radar MCU (capture + Doppler FFT, streams speeds to SoC)", "Texas Instruments", "MSPM0G3507SRHBR", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=MSPM0G3507SRHBR", 1, 1, [2.59, 1.57, 1.43, 1.34], "7,477 in stock", "now", "")
add("RAD-05", S, "Low-noise 3.3 V LDO (radar head)", "Texas Instruments", "TPS7A2033PDBVR", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=TPS7A2033PDBVR", 2, 2, [0.35, 0.19, 0.16, 0.15], "0 stock until late Nov", "now", "Any 3.3 V LDO <10 µVrms.")
add("RAD-06", S, "JST SH 6-pos cable, 152 mm", "JST", "A06SR06SR30K152A", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=A06SR06SR30K152A", 2, 2, [1.83, 1.32, 1.12, 0.90], "4,996 in stock", "now", "Reversing cable: check pinout.")
add("RAD-07", S, "JST SH 6-pos right-angle header", "JST", "SM06B-SRSS-TB(LF)(SN)", "Digi-Key",
    "https://www.digikey.com/en/products/detail/jst-sales-america-inc/SM06B-SRSS-TB/926712", 4, 4, [0.68, 0.45, 0.35, 0.25], "In stock", "now", "")
add("RAD-08", S, "Radar head PCB 4-layer FR-4 (×2) + passives", "JLCPCB / PCBWay", "custom", "JLCPCB",
    "https://jlcpcb.com/", 1, 1, [11.00, 2.80, 1.70, 1.15], "[est.]", "design", "RF stays inside the module, so plain FR-4.")

# ---------------------------------------------------------------- 5 POWER & BATTERY
S = "Power & battery"
add("PWR-01", S, "USB-C receptacle IP67, 5 A", "GCT", "USB4720-03-A", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=USB4720-03-A", 1, 1, [2.43, 1.76, 1.46, 1.31], "2,082 in stock", "now", "")
add("PWR-02", S, "USB-C PD sink controller (65 W)", "Texas Instruments", "TPS25751DREFR", "Digi-Key",
    "https://www.digikey.com/en/products/detail/texas-instruments/TPS25751DREFR/23028775", 1, 1, [3.39, 2.10, 1.80, 1.80], "10,469 in stock", "now",
    "TPS25750 is NRND. Alt: STUSB4500QTR.")
add("PWR-03", S, "Buck-boost charger, 1–5S, runs with no battery, hot-swap", "Texas Instruments", "BQ25730RSNR", "Digi-Key",
    "https://www.digikey.com/en/products/detail/texas-instruments/BQ25730RSNR/13896423", 1, 0, [5.08, 3.23, 2.80, 2.80],
    "0 stock until 25 Jan 2027", "now", "Order now for pilot. BQ25731 cannot run battery-less.")
add("PWR-04", S, "30 V N-MOSFET (4 charger FETs Pro / 2 ideal-diode FETs Indoor)", "Texas Instruments", "CSD17578Q3A", "Digi-Key",
    "https://www.digikey.com/en/products/detail/texas-instruments/CSD17578Q3A/5015743", 4, 2, [1.05, 0.43, 0.25, 0.22], "2,216 in stock", "now", "")
add("PWR-05", S, "Charger lot: battery switch FET (30 V), 2.2 µH inductor, sense resistors, caps", "various", "lot", "Digi-Key",
    "", 1, 0, [4.00, 2.50, 1.80, 1.40], "[est.]", "now", "")
add("PWR-06", S, "Ideal-diode controller (USB-C ‖ barrel ORing)", "Diodes Inc.", "AP74700QW6-7", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=AP74700QW6-7", 0, 2, [0.82, 0.55, 0.45, 0.38], "In stock", "now",
    "PM swap: TI LM74700 was $1.23 @1k and 0 stock.")
add("PWR-07", S, "DC barrel jack 8 A (24 V input)", "Same Sky", "PJ-063AH", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=PJ-063AH", 0, 1, [1.52, 1.10, 0.92, 0.90], "18,356 in stock", "now", "Add TVS (in rail lot).")
add("PWR-08", S, "6 A sync buck, 4.5–28 V in (3.8 V SOM rail; 5 V system rail)", "Texas Instruments", "TPS56637RPAR", "Digi-Key",
    "https://www.digikey.com/en/products/detail/texas-instruments/TPS56637RPAR/10715537", 2, 2, [2.71, 1.66, 1.41, 1.38], "14,658 in stock", "now",
    "QCS6490 SOM VIN = 3.4–4.5 V (typ 3.8 V).")
add("PWR-09", S, "3 A buck (3.3 V rail)", "Texas Instruments", "TPS62933DRLR", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=TPS62933DRLR", 1, 1, [1.60, 0.95, 0.85, 0.77], "63,313 in stock", "now", "")
add("PWR-10", S, "Rail lot: inductors, bulk caps, input TVS, eFuse/fuse", "various", "lot", "Digi-Key",
    "", 1, 1, [4.50, 2.70, 1.90, 1.50], "[est.]", "now", "")
add("PWR-11", S, "Battery bay connector (host side), 5-pos 7 A", "TE Connectivity", "5787441-1", "Digi-Key",
    "https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/5787441-1/2135744", 1, 0, [8.18, 5.83, 4.71, 3.50], "2,035 in stock", "now",
    "10k = ACES/FCI equivalent [est.].")
add("PWR-12", S, "Smart battery pack, user-swappable 4S1P 21700 ≈81 Wh (LG M58T ×4, TI BQ40Z50-R2 gauge, BQ771807 OVP, TE 787439-1 plug, UN38.3/IEC 62133-2)",
    "Shenzhen pack OEM (our spec)", "OB-BAT-4S81", "Pack assembler (RFQ to 3 vendors)", "", 1, 0, [167.22, 95, 57, 35],
    "6–10 wk after tooling", "quote",
    "Proto column = Inspired Energy ND4054HD50 off-the-shelf smart pack ($167.22, certified) as stand-in. Alt cells: Molicel P50B, Samsung 50S (72 Wh).")
add("PWR-13", S, "Battery door latch & spring contacts hardware", "molded / stamped", "custom", "Molder", "", 1, 0, [1.00, 0.80, 0.40, 0.25], "[est.]", "design", "")
add("PWR-14", S, "65 W USB-C PD GaN charger (in Pro box), UL/CE/FCC/PSE", "Private-label GaN OEM", "OB-CHG-65W", "Shenzhen OEM (RFQ)",
    "https://www.globalsources.com/manufacturers/usb-c-65w-charger.html", 1, 0, [39.99, 15.00, 13.00, 12.00], "15–30 days", "quote",
    "Proto = retail Anker/UGREEN 65 W GaN. Verify UL file numbers; EU may need a no-charger box.")
add("PWR-15", S, "24 V / 60 W wall adapter, 5.5×2.1 mm (in Indoor box)", "Mean Well", "GST60A24-P1J", "Digi-Key",
    "https://www.digikey.com/en/products/detail/mean-well-usa-inc/GST60A24-P1J/7703715", 0, 1, [19.40, 17.10, 15.00, 13.50], "707 in stock", "now", "")

# ---------------------------------------------------------------- 6 DISPLAY, SENSORS, THERMAL, UI
S = "Display, sensors, thermal & UI"
add("UI-01", S, "2.4\" transflective IPS 240×320, sunlight readable, SPI (ST7789)", "VIEWE", "UEED024QV-RH40-A003", "VIEWE",
    "https://viewedisplay.com/product/2-4-inch-240320-transflective-sunlight-readable-and-super-low-power-tft-lcd-module-with-mcu-8-16bit-spi-interface/",
    1, 0, [14.59, 12.00, 9.00, 7.00], "Quote for volume", "now", "Fallback: Newhaven NHD-2.8-240320AF-CSXP-F $18.45. Get a longevity letter.")
add("UI-02", S, "Display FPC connector 40-pos 0.5 mm", "Hirose", "FH12-40S-0.5SH(55)", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=FH12-40S-0.5SH(55)", 1, 0, [3.55, 2.57, 2.26, 1.98], "19,148 in stock", "now", "Confirm VIEWE pin count.")
add("UI-03", S, "Display cover lens, AR glass, optically bonded", "Cover-glass vendor (Saida/Felix)", "custom", "RFQ", "", 1, 0, [15, 8, 5, 3.5], "[est.]", "design", "")
add("UI-04", S, "Display backlight FET + passives", "various", "lot", "Digi-Key", "", 1, 0, [0.50, 0.30, 0.20, 0.15], "[est.]", "now", "")
add("SEN-01", S, "Inclinometer ±0.1° leveling (Pro)", "Murata", "SCL3300-D01-1", "Digi-Key",
    "https://www.digikey.com/en/products/detail/murata-electronics/SCL3300-D01-1/9950616", 1, 0, [40.12, 31.73, 30.47, 22.00], "1,546 in stock", "now",
    "Cost-down to test at DVT: BMI323 + temperature calibration (saves ~$27).")
add("SEN-02", S, "6-axis IMU (Indoor leveling; Pro shot-shock detection)", "Bosch Sensortec", "BMI323", "Digi-Key",
    "https://www.digikey.com/en/products/detail/bosch-sensortec/BMI323/16719593", 1, 1, [3.91, 2.92, 2.60, 2.43], "31,432 in stock", "now", "")
add("SEN-03", S, "Barometric pressure (air density)", "Bosch Sensortec", "BMP585", "Digi-Key",
    "https://www.digikey.com/en/products/detail/bosch-sensortec/BMP585/19522589", 1, 1, [4.54, 3.41, 3.05, 2.88], "11,371 in stock", "now", "")
add("SEN-04", S, "Temperature/humidity with PTFE membrane (air density)", "Sensirion", "SHT45-AD1F-R2", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=SHT45-AD1F-R2", 1, 1, [6.51, 4.95, 4.53, 4.29], "16,397 in stock", "now", "")
add("THM-01", S, "Blower 40 mm 5 V IP55, 30,000 h @40 °C (Pro)", "Delta", "BFB0405HHA-TZP4", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=BFB0405HHA-TZP4", 1, 0, [15.31, 14.12, 13.78, 10.91], "Not stocked, 40 wk", "quote",
    "Order now. Alt: Orion OD4010-05HB55 $14.52 @500.")
add("THM-02", S, "Fan 40 mm 5 V MagLev, 70,000 h @40 °C (Indoor)", "Sunon", "MF40100V1-1000U-A99", "Digi-Key",
    "https://www.digikey.com/en/products/detail/sunon-fans/MF40100V1-1000U-A99/6198732", 0, 1, [4.87, 3.16, 2.74, 2.74], "14,187 in stock", "now", "")
add("THM-03", S, "SOM heat-pipe + fin stack (sealed bay → separate duct)", "Custom thermal vendor (Auras/CCI)", "custom", "RFQ",
    "", 1, 1, [25, 15, 9, 6], "[est.]", "design", "First builds: machined copper spreader + off-the-shelf 40 mm heatsink.")
add("THM-04", S, "Thermal pad 6.2 W/m·K", "t-Global", "TG-A6200-40-40-1.0", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=t-Global%20TG-A6200", 1, 1, [2.73, 1.50, 0.60, 0.35], "In stock", "now", "")
add("UI-05", S, "Tact switch IP67 (power / mode / handedness on Pro; power on Indoor)", "C&K", "KSC241JLFS", "Digi-Key",
    "https://www.digikey.com/en/products/detail/wee/KSC241JLFS/26327478", 3, 1, [0.38, 0.38, 0.28, 0.27], "6,000 in stock", "now", "")
add("UI-06", S, "RGB status LED", "Würth Elektronik", "150141M173100", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=150141M173100", 1, 2, [0.50, 0.43, 0.34, 0.34], "30,274 in stock", "now", "")
add("UI-07", S, "SMT buzzer (shot-ready / error tones)", "Same Sky", "CMT-8540S-SMT-TR", "Digi-Key",
    "https://www.digikey.com/en/products/result?keywords=CMT-8540S-SMT-TR", 1, 1, [4.13, 2.44, 1.92, 1.72], "20,504 in stock", "now", "")

# ---------------------------------------------------------------- 7 CARRIER PCB & BOARDS
S = "Circuit boards & assembly"
add("PCB-01", S, "Main carrier PCB, 10-layer 1+N+1 HDI, 120×90 mm, ENIG, impedance-controlled", "PCBWay / JLCPCB (proto); same-country fab with assembly (volume)",
    "OB-MAIN rev A", "JLCPCB", "https://jlcpcb.com/capabilities/pcb-capabilities", 1, 1, [70, 38, 20, 13], "7–12 days proto", "design",
    "Same board both SKUs; Indoor depopulates charger/battery/display/inclinometer, populates barrel jack/Ethernet.")
add("PCB-02", S, "Carrier assembly labour (double-sided, ~400 placements, X-ray for LGA SOM)", "JLCPCB (proto) / Taiwan-Vietnam CM", "assembly", "JLCPCB",
    "https://jlcpcb.com/help/article/pcb-assembly-price", 1, 1, [51, 7, 5, 4], "+3–5 days", "design", "SOM is LGA solder-down: X-ray inspect every board.")
add("PCB-03", S, "Carrier misc components (passives, ESD, crystals incl. 25 MHz, connectors for fan/buttons/debug, level shifters, eMMC-free)", "various",
    "lot", "Digi-Key / LCSC", "", 1, 1, [40, 18, 12, 9], "[est.]", "now", "Fully itemised once the schematic exists.")
add("PCB-04", S, "LED strobe boards ×3, 4-layer FR-4 w/ thermal vias, ~40×30 mm, assembled", "JLCPCB / PCBWay", "OB-LED rev A", "JLCPCB",
    "https://jlcpcb.com/", 1, 1, [30, 4.20, 2.10, 1.35], "1–2 wk", "design", "Price is per set of three.")

# ---------------------------------------------------------------- 8 ENCLOSURE & MECHANICAL
S = "Enclosure & mechanical"
add("MEC-01", S, "Optical bench, 6061-T651, 200×80×15 mm, dowelled, black anodize, 1/4\"-20 tripod thread tapped", "Xometry / Protolabs (proto); China CNC / extrusion (volume)",
    "OB-BENCH rev A", "Xometry", "https://www.xometry.com/", 1, 1, [110, 40, 20, 12], "3–10 days", "design", "3-point kinematic mount to shell.")
add("MEC-02", S, "Enclosure shell set PC/ABS V-0 (front, rear, battery door/blank, bezel/blank, feet, baffle, button caps)", "JLC3DP MJF (proto) / injection molder (volume)",
    "OB-ENC rev A", "JLC3DP", "https://jlc3dp.com/", 1, 1, [180, 135, 13.5, 8.8], "1–2 wk proto; 4–8 wk tooling", "design",
    "Indoor ≈$5–10 cheaper (blank plates). Tooling in one-time list.")
add("MEC-03", S, "TPE stretch-on bumper 60–70A", "TPE molder (TPU print for proto)", "OB-BUMP rev A", "Molder", "", 1, 1, [30, 22, 2.5, 1.6], "4–6 wk", "design", "")
add("MEC-04", S, "IR window: strengthened glass, IR-pass ink, AR coat, IR-opaque isolation band", "Saida Glass / Felix", "OB-WIN rev A",
    "Saida Glass (RFQ)", "https://saidaglass.en.made-in-china.com/", 1, 1, [25, 8, 5, 3.5], "3–5 wk", "design",
    "Proto: laser-cut Plexiglas 3143 IR acrylic from ePlastics. Window is NOT the bandpass filter (CAM-04 is).")
add("MEC-05", S, "Die-cut gaskets (silicone foam)", "Die-cutter", "OB-GSK rev A", "RFQ", "", 1, 1, [15, 2.5, 1.2, 0.6], "2–4 wk", "design", "Indoor uses 2 of 3.")
add("MEC-06", S, "Pressure-equalising vent IP67", "Amphenol LTW", "VENT-PS1YBK-N8001", "Digi-Key",
    "https://www.digikey.com/en/products/detail/amphenol-ltw/VENT-PS1YBK-N8001/7898285", 1, 1, [3.47, 2.22, 1.77, 1.40], "In stock", "now", "Production: Gore stick-on vent.")
add("MEC-07", S, "Fasteners, dowel pins, hinge pins, detents (kit)", "McMaster-Carr / fastener house", "kit", "McMaster-Carr",
    "https://www.mcmaster.com/", 1, 1, [4, 1.5, 0.6, 0.35], "Stock", "now", "")
add("MEC-08", S, "Rubber feet", "3M", "SJ5302", "Digi-Key", "https://www.digikey.com/en/products/detail/3m/SJ5302/2345107", 4, 4, [0.13, 0.12, 0.105, 0.09], "Stock", "now", "")
add("MEC-09", S, "Rating / serial / regulatory labels", "Label printer", "OB-LBL", "RFQ", "", 1, 1, [1, 0.5, 0.15, 0.08], "2 wk", "design", "")
add("MEC-10", S, "Battery bay harness (Pro)", "Harness CM", "OB-HAR-BAT", "MiniProto (proto)",
    "https://www.miniproto.com/products/custom-jst-ph-to-jst-pa-wire-harness-assembly", 1, 0, [46, 12, 4, 2.5], "2–4 wk", "quote", "")

# ---------------------------------------------------------------- 9 IN THE BOX
S = "In the box"
add("BOX-01", S, "Carry case (Pro): Nanuk 920 + custom foam (proto/100) → molded EVA case (1k+)", "Nanuk / EVA case OEM",
    "Nanuk 920 / OB-CASE", "Nanuk", "https://nanuk.com/products/nanuk-920", 1, 0, [215, 150, 18, 11], "Stock / 5–7 wk", "now",
    "PM call: Nanuk stays a $149 premium accessory; EVA case ships in the box.")
add("BOX-02", S, "Rigid retail box with insert", "Rigid-box packager", "OB-BOX", "RFQ", "", 1, 1, [40, 14, 11, 5.5], "3–5 wk", "design", "")
add("BOX-03", S, "Alignment stick, 2-piece with marks", "OEM", "OB-STICK", "RFQ", "", 1, 1, [15, 6, 2.5, 1.5], "3–4 wk", "design", "")
add("BOX-04", S, "Quick-start card + regulatory leaflet", "Printer", "OB-QSG", "RFQ", "", 1, 1, [2, 0.8, 0.25, 0.10], "1–2 wk", "design", "")
add("BOX-05", S, "Shipping carton", "Corrugated supplier", "OB-SHIP", "RFQ", "", 1, 1, [5, 2.5, 1.2, 0.8], "1–2 wk", "design", "")
add("BOX-06", S, "USB-C to USB-C cable 1 m, 100 W (Pro: charging; Indoor: service)", "OEM", "OB-CBL-C", "RFQ", "", 1, 1, [9, 2.5, 1.4, 1.0], "[est.]", "quote", "")

# ---------------------------------------------------------------- 10 ASSEMBLY, TEST, CALIBRATION
S = "Final assembly, test & calibration"
add("LAB-01", S, "Final assembly, end-of-line test, stereo/radar/IMU calibration, live-shot test, pack-out (1.0–1.5 labour-h)", "In-house → Taiwan/Vietnam CM",
    "labour", "—", "", 1, 1, [240, 100, 35, 18], "—", "design", "Calibration stations are in the one-time list.")

TIERS = ["proto", "v100", "v1k", "v10k"]

# First-build stand-ins: orderable today, swapped for the production part (by ID) once the RFQ/custom part exists.
STANDINS = [
    # (replaces, mpn, mfr, desc, vendor, url, qty per Pro, qty per Indoor, unit $)
    ("CAM-04", "CBP940-070S030", "Commonlands", "940 nm bandpass 7×7×0.3 mm (80 nm FWHM) - first-build stand-in", "Commonlands",
     "https://commonlands.com/products/940nm-bandpass-filter", 3, 3, 9.00),
    ("CAM-05", "0150200241", "Molex", "Premo-Flex 22-pos 0.5 mm 203 mm FFC - stand-in for VC 100 mm FPC", "Digi-Key",
     "https://www.digikey.com/en/products/result?keywords=0150200241", 2, 2, 5.21),
    ("PWR-12", "ND4054HD50", "Inspired Energy", "Certified 4S smart Li-ion pack (stand-in for custom pack)", "Inspired Energy",
     "https://inspired-energy.com/products/details/3/117-nd4054hd50", 1, 0, 167.22),
    ("MEC-04", "3143 IR acrylic sheet 3 mm", "Röhm (Plexiglas)", "IR-transmitting acrylic sheet for laser-cut windows", "ePlastics",
     "https://www.eplastics.com/plexiglass/acrylic-sheets/ir-transmitting", 1, 1, 20.00),
    ("LED-11", "A08GR08GR28K152A", "JST", "GH 8-pos pre-crimped cable 152 mm (stand-in LED harness)", "Digi-Key",
     "https://www.digikey.com/en/products/result?keywords=A08GR08GR28K152A", 3, 3, 2.10),
    ("THM-01", "OD4010-05HB55", "Orion Fans", "40 mm 5 V IP55 fan (in-stock stand-in for Delta blower)", "Digi-Key",
     "https://www.digikey.com/en/products/result?keywords=OD4010-05HB55", 1, 0, 16.50),
]

# ---------------------------------------------------------------- one-time costs
ONE_TIME = [
    # (category, item, low, high, used, note)
    ("Tooling", "Enclosure injection tools, P20 steel, 8 parts incl. revisions (Pro & Indoor share)", 60000, 95000, 80000, "Aluminium bridge set $30–45k if you want 300–1k units first"),
    ("Tooling", "TPE bumper mold", 6000, 10000, 8000, ""),
    ("Tooling", "IR window screens & jigs", 500, 1000, 1000, ""),
    ("Tooling", "Gasket dies ×3", 1500, 3000, 2000, ""),
    ("Tooling", "Optical bench CNC fixtures", 1000, 3000, 2000, "Extrusion die +$1–3k at 10k"),
    ("Tooling", "Heat-pipe/fin-stack tooling", 1000, 3000, 2000, ""),
    ("Tooling", "EVA case mold + foam die", 3500, 6500, 4000, ""),
    ("Tooling", "Retail box plates", 500, 1000, 1000, ""),
    ("Tooling", "Harness setup (all harnesses)", 500, 5000, 3000, ""),
    ("NRE", "Battery pack NRE: pack tooling, BMS config, UN38.3 + IEC 62133-2", 15000, 45000, 30000, "Retest if the cell changes"),
    ("NRE", "Custom IMX900 camera module NRE (VC / e-con OEM) incl. 940/40 filter integration", 15000, 50000, 30000, "Drops camera cost from ~$165 to ~$95 each"),
    ("NRE", "IMX900 triggered-mono Linux driver for QCS6490 (Leopard / Thundercomm / VC paid port)", 25000, 50000, 40000, "Only gap in the stack; no shipping driver today"),
    ("NRE", "Custom LED secondary optic (60°×45°), optional at ≥2k units", 15000, 30000, 0, "Excluded: optional; cuts LED count ~24→15"),
    ("NRE", "Carrier PCB stencils / fab tooling", 100, 800, 500, ""),
    ("Test", "Carrier board in-circuit/functional test fixture", 8000, 25000, 15000, ""),
    ("Test", "Stereo calibration station + live-shot test station (×1 + spare)", 100000, 300000, 150000, "Ball launcher + laser light gates"),
    ("Certification", "FCC/ISED (Part 15B + radar module reuse), safety CB 62368-1, IEC 62471, battery, CE/UKCA incl. EN 18031, RCM, Japan, Korea", 70000, 170000, 110000, "Radar module grant reuse saves ~$10–20k"),
]

def totals():
    out = {}
    for sku in ("pro", "indoor"):
        qi = 7 if sku == "pro" else 8
        by_sub = defaultdict(lambda: [0.0]*4)
        for r in L:
            q = r[qi]
            if not q: continue
            for i, p in enumerate(r[9]):
                by_sub[r[1]][i] += q * p
        tot = [sum(v[i] for v in by_sub.values()) for i in range(4)]
        out[sku] = {"by_sub": {k: [round(x, 2) for x in v] for k, v in by_sub.items()}, "total": [round(x, 2) for x in tot]}
    return out

def landed(t, tier_units):
    """Landed US cost per unit (no amortisation): BOM x 1.03 scrap, +10% US duty (Taiwan final assembly cap), +$12 freight/insurance."""
    return [round(t[i]*1.03*1.10 + 12, 2) for i in range(4)]

def amort(tier_units, lifetime=10000):
    """One-time cost per unit if spread over the lifetime volume of the product (default 10k units across both SKUs)."""
    total = sum(o[4] for o in ONE_TIME)
    return round(total / lifetime, 2), total

def main():
    T = totals()
    tiers_units = [5, 100, 1000, 10000]
    for sku in T:
        T[sku]["landed"] = landed(T[sku]["total"], tiers_units)
    per_unit_amort, one_time_total = amort(tiers_units)

    # master CSV
    with open(os.path.join(HERE, "outer-bounds-bom.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Subsystem", "Item", "Manufacturer", "MPN", "Vendor", "URL", "Qty Pro", "Qty Indoor",
                    "Unit $ proto", "Unit $ @100", "Unit $ @1k", "Unit $ @10k", "Stock / lead", "Order status", "Notes"])
        for r in L:
            w.writerow([r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], *r[9], r[10], r[11], r[12]])

    # carts for first build (5 Pro + 5 Indoor), +10% attrition (min +2) on parts under $5, +1 spare on parts >=$5
    carts = defaultdict(list)
    for r in L:
        if r[11] not in ("now",) or r[4] in ("lot", "kit", "custom") or not r[6]:
            continue
        need = r[7]*BUILD["pro"] + r[8]*BUILD["indoor"]
        if not need: continue
        unit = r[9][0]
        extra = max(2, math.ceil(need*0.10)) if unit < 5 else 1
        if unit > 100: extra = 0
        vendor = r[5].split(" (")[0].split(" /")[0]
        carts[vendor].append((r[4], r[3], r[2], need + extra, unit, r[6], r[0]))
    for rep, mpn, mfr, desc, vendor, url, qp, qi, unit in STANDINS:
        need = qp*BUILD["pro"] + qi*BUILD["indoor"]
        extra = max(2, math.ceil(need*0.10)) if unit < 5 else (0 if unit > 100 else 1)
        carts[vendor].append((mpn, mfr, desc + f" [replaces {rep}]", need + extra, unit, url, rep + "-SI"))
    cart_summary = {}
    for vendor, rows in carts.items():
        fn = "cart-" + vendor.lower().replace(" ", "-").replace("&", "and") + ".csv"
        with open(os.path.join(HERE, fn), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Manufacturer Part Number", "Manufacturer", "Quantity", "Customer Reference", "Description", "Est unit $", "Est extended $", "URL"])
            sub = 0
            for mpn, mfr, desc, q, unit, url, rid in rows:
                w.writerow([mpn, mfr, q, rid, desc, unit, round(q*unit, 2), url])
                sub += q*unit
        cart_summary[vendor] = {"file": fn, "lines": len(rows), "subtotal": round(sub, 2)}

    # RFQ list: everything that is quote-only or a custom part
    with open(os.path.join(HERE, "rfq-and-custom-parts.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Type", "Item", "Manufacturer / maker", "MPN / spec", "Contact / vendor", "URL", "Qty for first build (5 Pro + 5 Indoor)", "Target $ @1k", "Notes"])
        for r in L:
            if r[11] in ("quote", "design"):
                need = r[7]*BUILD["pro"] + r[8]*BUILD["indoor"]
                w.writerow([r[0], "RFQ" if r[11]=="quote" else "Custom (needs design files)", r[2], r[3], r[4], r[5], r[6], need, r[9][2], r[12]])

    with open(os.path.join(HERE, "one-time-costs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Category", "Item", "Low $", "High $", "Planning $", "Note"])
        for o in ONE_TIME: w.writerow(o)

    data = {
        "lines": [dict(id=r[0], sub=r[1], item=r[2], mfr=r[3], mpn=r[4], vendor=r[5], url=r[6], qp=r[7], qi=r[8],
                       price=r[9], stock=r[10], status=r[11], notes=r[12]) for r in L],
        "totals": T, "one_time": [dict(cat=o[0], item=o[1], lo=o[2], hi=o[3], plan=o[4], note=o[5]) for o in ONE_TIME],
        "carts": cart_summary, "build": BUILD, "amort_per_unit": per_unit_amort, "one_time_total": one_time_total,
        "standins": [dict(rep=x[0], mpn=x[1], mfr=x[2], desc=x[3], vendor=x[4], url=x[5], qp=x[6], qi=x[7], unit=x[8]) for x in STANDINS],
    }
    with open(os.path.join(HERE, "bom-data.json"), "w") as f:
        json.dump(data, f, indent=1)
    tpl = open(os.path.join(HERE, "template.html")).read()
    blob = json.dumps(data).replace("</", "<\\/")
    with open(os.path.join(HERE, "outer-bounds-bom.html"), "w") as f:
        f.write(tpl.replace("__DATA__", blob))

    for sku in T:
        print(sku.upper(), "BOM", T[sku]["total"], "landed", T[sku]["landed"])
        for k, v in T[sku]["by_sub"].items(): print("   ", f"{k:38s}", v)
    print("one-time planning total", one_time_total, "per unit over 10k lifetime", per_unit_amort)
    print("carts", json.dumps(cart_summary, indent=1))

if __name__ == "__main__":
    main()
