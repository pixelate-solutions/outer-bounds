# B: Compute, memory/storage, connectivity, and the SoC power tree

Outer Bounds "Pro" (battery, display, Wi-Fi/BLE) and "Indoor" (plug-in, Wi-Fi + GbE) share one sensing core. Researched 7 Oct 2026.

Conventions:
- **[est.]** marks my estimate, not a published price.
- "Quote" means the vendor publishes no price.
- Every published price has a URL in the table or in §9.
- EUR is converted at 1 EUR ≈ 1.16 USD [est. FX].
- Distributor snapshots move week to week (DRAM/NAND shock), so re-check before a PO.

---

## 0. Bottom line

1. **Only Jetson meets the "shipping camera stack" criterion as written.** NVIDIA Jetson Orin Nano has vendor IMX900 drivers from FRAMOS, e-con and Vision Components (VC), with external-trigger modes in the open VC driver.
   - It handles 3 cameras, but only as 4× 2-lane ports: 8 CSI lanes in total, up to 4 cameras without virtual channels.
   - It cannot take the 5-camera IMX296 fallback without a virtual-channel aggregator or GMSL.
   - Price: **$399 at 1 ku since July 2026**, up from $299. It needs an external NVMe (no eMMC), and availability is published **only until Jan 2032**.
2. **No non-Jetson SoC has a vendor IMX900 driver**, but RK3588 is close:
   - The Rockchip BSP gained an `imx900.c` (4-lane, streaming only; see report A).
   - VEYE ships a **triggered IMX296 driver for RK3588** (MV-MIPI-IMX296M).
   - Mainline has `imx296.c`.
   - VC's platform-agnostic `vc_mipi_core` (IMX900/IMX296 with all trigger modes) is open source, and VC writes Rockchip drivers on request.
   - Closing the gap is a bounded one-time port (**[est.] 4–8 engineer-weeks**, or a paid VC/FRAMOS project). The alternative is roughly **$200+/unit** more for Jetson for the life of the product.
3. **Recommended production SOM: Forlinx FET3588J-C, 4 GB LPDDR4x / 32 GB eMMC** (RK3588J, industrial −40…+85 °C). MPN `FET3588J-C+224GSE32GI` (DigiKey: `FORLINX-FET3588J-C+224GSE32GIA11`, $489 at qty 1).
   - Natively 2× 4-lane DC-PHY + 4× 2-lane D-PHY, so **up to 6 CSI cameras**. That covers both the 3× IMX900 plan and the 5× IMX296 fallback.
   - eMMC on module, mass-production status, listed at DigiKey.
   - The RK3588J's capped clocks (A76 at 1.6 GHz) and industrial rating fit a sealed box at 40 °C in sun better than any 2.4 GHz part.
   - The commercial FET3588-C+244GSE32GC (pin-compatible, $448) is the cost-down if a 0 °C minimum is acceptable.
4. **Backup: NVIDIA Jetson Orin Nano 8 GB (900-13767-0030-000)** plus an industrial 2230 NVMe, on its own carrier. This is the "guaranteed drivers" path if the RK3588 camera port misses its gate.
   - **Longevity hedge (not a backup carrier):** Thundercomm **C6490P-U8A-3690000** (QCS6490, 8 GB/128 GB UFS).
   - It has 5× 4-lane CSI, **life cycle to 2036**, and published volume pricing ($228 @100 / $190 @2k / $149 @30k).
   - The catch is the camera stack: mainline CAMSS is raw-RDI only, and the proprietary CamX path needs Qualcomm/partner support.
5. **RAM: 4 GB.** The workload needs under ~2 GB [est.]: Linux + app + 3 camera ring buffers + an RKNN model. DRAM pricing makes 8 GB expensive:
   - Forlinx 8 GB/64 GB is **+$83** at qty 1.
   - Raspberry Pi CM5 is +$45 (4 GB) vs **+$90** (8 GB) since launch.
   - On Jetson the 4 GB module is $349 vs $399 for 8 GB. The 4 GB module halves the GPU and memory bandwidth for a 12.5% saving, so the Jetson backup stays at 8 GB.
6. **Storage: use the SOM's 32 GB eMMC and add no separate part.** NAND is in shortage: Kingston industrial 2230 NVMe is **$310 for 256 GB** at DigiKey. A Jetson build must add that cost; the RK3588 build does not.
7. **Wi-Fi/BT: u-blox MAYA-W266-00B** (NXP IW611, Wi-Fi 6 + BT 5.3, SDIO 3.0, $14.17 @1 / $11.58 @500).
   - It is the only candidate found with **FCC + ISED + RED + UKCA + MIC + KCC + ANATEL + ACMA** module approvals. Korea matters for golf sim.
   - Sona IF573 and AzureWave AW-XM458 have no KC.
   - It can use its internal antenna (zero cost) or an external Ezurio FlexPIFA through a U.FL.
8. **Ethernet (Indoor):** Realtek **RTL8211F-CG** RGMII PHY (~$0.89 @1k) plus **Pulse JXD1-0001NL** MagJack ($4.66 @1k).
   - PoE+ (802.3at) costs about **+$13–18/unit** (Silvertel AG53012 + PoE MagJack JK0-0177NL). It is worth keeping as a **populate-option footprint**. Commit only if the measured Indoor draw stays ≤ ~20 W (802.3at gives 25.5 W at the PD), and bundle an injector.
9. **Power tree:**
   - The SoM carries its own PMIC.
   - The carrier needs one **TI TPS56637** (4.5–28 V in, 6 A) to make 5 V for the SoM from the 7–17 V rail. That is the same 5 V feed a Jetson backup would take.
   - A second TPS56637 (or a smaller 3 A buck) makes 3.3 V for the radio, PHY and MCU.
10. **Timing MCU: STM32G474CET6.**
    - HRTIM gives 184 ps edge placement, and its hardware fault inputs plus comparators can cut IR strobes in ns, independent of firmware (eye-safety interlock).
    - $7.95 @1, ~$5.4 in reel.
    - Alternate: **RP2350A** (PIO, ~$0.95–0.99). Jitter against an async radar trigger is ~6 ns-class for both.
    - Don't generate triggers from the SoC. Linux GPIO jitter is tens of µs.

---

## 1. LINE-ITEM BOM (centerpiece)

Production build on the primary SOM. Qty column = **Pro / Indoor**. "opt" = footprint only, populated if the option is taken.

| Item | Manufacturer | MPN | Vendor | URL | Qty/unit (Pro / Indoor) | $@1 | $@100 | $@1k | $@10k | Stock/lead | Lifecycle | Notes/alternates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Compute SOM**: RK3588J, 4 GB LPDDR4x, 32 GB eMMC, −40…+85 °C | Forlinx Embedded | **FET3588J-C+224GSE32GI** (DigiKey: FORLINX-FET3588J-C+224GSE32GIA11) | DigiKey Marketplace / Forlinx direct | https://www.digikey.com/en/products/result?keywords=FORLINX-FET3588 | 1 / 1 | **489.00** | [est.] 240 | [est.] 185 | [est.] 155 | DigiKey: 5 in stock, ships ~7 days; Forlinx samples 5 days, bulk ~6 weeks | Forlinx "Mass Production". **No Rockchip silicon-longevity commitment**: get an LTS letter | Factory listing for FET3588-C is $170–250 (https://www.globalsources.com/product/fet3588-c-rk3588-rockchip_1208005892f.htm), so volume tiers are estimates and need a quote. **Cost-down:** FET3588-C+244GSE32GC (commercial, 2.4 GHz, 0…+80 °C), $448 @1 (https://www.digikey.com/en/products/detail/forlinx-embedded/FORLINX-FET3588-C-244GSE32GCC11/21776976). **8 GB:** FET3588-C+248GSE64GC, $531 @1. |
| SoM↔carrier board-to-board connectors (4× 100-pin, 0.4 mm pitch, 1.5 mm stack) | per Forlinx design guide | TBD (from Forlinx carrier reference) | Forlinx / distributor | (no URL; MPN not published in brief) | 4 / 4 | [est.] 1.50 | [est.] 1.20 | [est.] 0.90 | [est.] 0.75 | — | — | Get the exact mating MPN from the Forlinx OK3588-C design files. |
| On-module storage (OS + shot logs + clips) | (on SOM) | included in SOM | — | — | 0 / 0 | 0 | 0 | 0 | 0 | — | — | 32 GB eMMC is enough for OS (~4–6 GB) plus a rolling buffer of ~2,000 shots with clips [est.]. Cloud/app sync handles archive. No microSD in a sealed box. |
| **Timing / trigger MCU** (camera XTRIG, LED strobe gates, radar sync, link to SoC) | STMicroelectronics | **STM32G474CET6** (LQFP-48) | DigiKey | https://www.digikey.com/en/products/detail/stmicroelectronics/STM32G474CET6/10326773 | 1 / 1 | **7.95** | [est.] 6.20 | [est.] 5.70 | [est.] 5.40 | CET6 in stock ("ships today"). UFQFPN CEU6 is **0 stock, 52 wk** | Active | Volume anchor from CEU6: $6.16 @100, $5.72 @500, $5.43 @2.5k reel (https://www.digikey.com/en/products/detail/stmicroelectronics/STM32G474CEU6/10326774). **Alt:** RP2350A SC1509 reel, $0.99 @500 / $0.95 @1k (https://www.digikey.com/en/products/detail/raspberry-pi/SC1509-13/26241107) + QSPI flash. Could absorb the radar MCU (report D) later. |
| **Wi-Fi 6 + BT 5.3 module** (SDIO 3.0 + UART) | u-blox | **MAYA-W266-00B** | DigiKey | https://www.digikey.com/en/products/detail/u-blox/MAYA-W266-00B/18688832 | 1 / 1 | **14.17** | 11.58 (500 reel) | [est.] 11.00 | [est.] 9.50 | **0 stock**; 350 due 9 Oct 2026; 20 wk lead | Active ("Initial production" per datasheet R07) | Approvals: RED, UKCA, FCC XPYMAYAW2A, ISED 8595A-MAYAW2A, MIC 003-230375, **KCC**, ANATEL, ACMA. Internal antenna, or RF pin to external antenna. Linux: u-blox/NXP `mxm_wifiex`, kernel ≥4.19. **Alt (PCIe, 2×2, no KC):** Ezurio Sona IF573 453-00120, $39.51 @1. |
| Wi-Fi/BT antenna (external option; FlexPIFA 2.4/5 GHz, 200 mm MHF1 cable integrated) | Ezurio | **EFB2455A3S-20MHF1** | DigiKey | https://www.digikey.com/en/products/result?keywords=EFB2455A3S-20MHF1 | 1 / 1 (opt) | **5.22** | [est.] 4.50 | [est.] 3.80 | [est.] 3.30 | 200 in stock, 12 wk | Active | The cable is part of the antenna, so no separate U.FL jumper. **Must be on u-blox's approved-antenna list** or needs a Class II permissive change. **Zero-cost alternative:** MAYA-W266 internal antenna (−1 to −7 dBi peak). MIMO alt: EFD2455A3S-10MHF1, $7.69. |
| U.FL receptacle on carrier (for the antenna) | Hirose | **U.FL-R-SMT-1(10)** | DigiKey | https://www.digikey.com/en/products/result?keywords=U.FL-R-SMT-1(10) | 1 / 1 (opt) | 1.67 | 1.20 | 1.02 | 0.89 (7.5k) | 374k in stock, 16 wk | Active | Only if the external antenna is used. |
| **5 V SoM rail buck** (7–17 V → 5.0 V, 6 A) | Texas Instruments | **TPS56637RPAR** | DigiKey | https://www.digikey.com/en/products/detail/texas-instruments/TPS56637RPAR/10715537 | 1 / 1 | 2.71 | 1.66 | 1.53 (500) | 1.38 (6k) | 9,331 in stock, 16 wk | Active | The SoM's PMIC and core bucks are on the module. The SoM takes 5–13 V per the Forlinx brief, but the web page says "12 V" (**confirm**). 20 W SoM peak is 4 A at 5 V. Same 5 V feed suits the Jetson backup. 8 A pin-compatible upgrade: TPS56837. |
| **3.3 V carrier rail buck** (Wi-Fi, PHY, MCU, radar digital) | Texas Instruments | **TPS56637RPAR** (2nd instance) | DigiKey | https://www.digikey.com/en/products/detail/texas-instruments/TPS56637RPAR/10715537 | 1 / 1 | 2.71 | 1.66 | 1.53 | 1.38 | as above | Active | One part number for simplicity. A 3 A buck run from 5 V would save about $0.5 [est.]. Camera and radar analog LDOs are in reports A and D. |
| **GbE PHY** (RGMII; the SoM exposes 2× GMAC, no on-module PHY) | Realtek | **RTL8211F-CG** | LCSC | https://www.lcsc.com/product-detail/C187932.html | 0 / 1 | 1.52 | 1.04 | 0.89 (980) | [est.] 0.80 | 59k–89k in stock | Active | Forlinx validated the RTL8211FSI-CG on OK3588-C. Industrial alt: RTL8211FI-CG, $2.00 (https://www.lcsc.com/product-detail/C717681.html). Second source: Motorcomm YT8521SH (not priced). Needs a 25 MHz crystal (passives, report F). |
| **RJ45 MagJack**, 1 G, LEDs, tab up (non-PoE) | Pulse Electronics | **JXD1-0001NL** | DigiKey | https://www.digikey.com/en/products/detail/pulse-electronics/JXD1-0001NL/5361447 | 0 / 1 | 7.59 | 5.48 | 4.66 | [est.] 4.30 | 620 in stock, 8 wk | Active | −40…+85 °C. Tab-down twin: JXD0-0001NL. Alt: Würth 7499111121A, $8.69 / $7.24 @100. |
| *Option:* PoE+ MagJack (replaces JXD1) | Pulse Electronics | **JK0-0177NL** | DigiKey | https://www.digikey.com/en/products/detail/pulse-electronics/JK0-0177NL/2649122 | 0 / opt | 13.54 | [est.] 9.50 | 8.29 (1,035) | [est.] 7.80 | 2,970 in stock | Active | 0–70 °C. Industrial: JXK0-0190NL. Alt: Würth 7499511611A, $16.24. |
| *Option:* PoE+ PD module (802.3at, 12 V out, isolated) | Silvertel | **AG53012** (or AG5300) | DigiKey | https://www.digikey.com/en/product-highlight/s/silvertel/ag53000-series-poe-pd-modules | 0 / opt | 11.75 | [est.] 11.00 | [est.] 10.50 | [est.] 9.80 | AG5300: 16 wk | Active | AG5300: $16.00 / $15.85 @10 / $15.00 @520 / $13.50 @1,040 (https://www.digikey.com/en/products/detail/silvertel/AG5300/19285345). **Do not use TI TPS23758: it is 13 W Type 1 only.** |

**Slice subtotal, primary build, published + [est.] prices:**

| | @1 | @100 | @1k | @10k |
|---|---|---|---|---|
| Pro (SOM, connectors, MCU, Wi-Fi, ext. antenna + U.FL, 2 bucks) | ≈ $529 | ≈ $272 | ≈ $213 | ≈ $180 |
| Indoor (Pro set + PHY + MagJack) | ≈ $539 | ≈ $278 | ≈ $219 | ≈ $185 |
| Indoor PoE option (delta) | +$17.7 | +$15.0 | +$14.1 | +$13.3 |

### 1b. Backup / hedge parts (not in the subtotal above)

| Item | Manufacturer | MPN | Vendor | URL | Qty/unit (Pro / Indoor) | $@1 | $@100 | $@1k | $@10k | Stock/lead | Lifecycle | Notes/alternates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Backup SOM**: Jetson Orin Nano 8 GB | NVIDIA | **900-13767-0030-000** (DigiKey/Seeed SKU 102110798) | NVIDIA partners, DigiKey, Silicon Highway | https://www.cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101/ | 1 / 1 | €399 ex VAT ≈ $463 (https://www.siliconhighwaydirect.com/product-p/900-13767-0030-000.htm) | 506.66 (DigiKey, 500 break) | **399** (NVIDIA 1 ku list; was $299) | [est.] 380 | DigiKey: non-stock, 4 wk | **Available through Jan 2032** (https://developer.nvidia.com/embedded/lifecycle) | 4 GB: 900-13767-0040-000, $349 @1 ku / $337.26 @500 DigiKey. Needs 5 V in (same TPS56637), NVMe, and a PCIe Wi-Fi (the module has no SDIO for Wi-Fi). |
| Jetson boot/log storage (2230 NVMe, industrial pSLC) | ATP | **AF40GSAJB-DBAIX** (N700Si 40 GB) | Mouser/ATP | https://www.mouser.com/datasheet/2/1133/ATP_I_Temp__NVMe_PCIe_Gen3_pSLC_M_2_2230_SSD_Datas-3009768.pdf | 1 / 1 | quote | quote | quote | quote | — | Active | No price found. NAND reference: Kingston OM3SGP4512K2-A00 (512 GB), $438 (https://www.digikey.com/en/products/detail/kingston-technology/OM3SGP4512K2-A00/26832996). Budget [est.] $60–150. |
| Wi-Fi for the Jetson path (PCIe M.2 2230, 2×2 Wi-Fi 6E) | Ezurio | **453-00120** (Sona IF573) | DigiKey | https://www.digikey.com/en/products/detail/ezurio/453-00120/20525586 | 1 / 1 | 39.51 | £26.22 ≈ $34 (DigiKey UK, https://www.digikey.co.uk/en/products/detail/laird-connectivity-inc/453-00120/20525586) | [est.] 30 | [est.] 27 | 0 stock US, 34 wk | RND (PCN 6F-2025 PCIe boot fix) | FCC SQG-SONAIF573, IC 3147A-SONAIF573, CE/UKCA, MIC, RCM. **No KC.** |
| Longevity hedge SOM: QCS6490, 8 GB + 128 GB UFS, LGA | Thundercomm | **C6490P-U8A-3690000** | Arrow | https://www.arrow.com/en/products/c6490p-u8a-3690000-qcs6490/thundercomm | — | 286.52 | 228.09 | 189.60 (2k) | [est.] 165 (149.18 @30k) | 0 stock, 16 wk | **Life cycle to 2036** (https://www.thundercomm.com/product/c6490p-som/) | 5× 4-lane CSI, 5 concurrent cameras (3 IFE + 2 IFE-lite, RDI raw). No 4 GB SKU found. |

### 1c. Dev kits / ready carriers (EVT, not production)

| Item | MPN | $ | URL | CSI ports | Notes |
|---|---|---|---|---|---|
| Forlinx OK3588-C dev kit (matches the primary SoM) | OK3588-C (4 GB/32 GB) | ~$280 sample (aggregator listing) | https://www.accio.com/plp/forlinx-ok3588-c-price | **5** (2× 4-lane D-PHY v2.0, 2× 2-lane, 1× 4-lane) on 26-pin FPC | 12 V in, 2× GbE (RTL8211FSI). **Usable for EVT directly**, with FPC adapters to VC 22-pin cameras. |
| Leopard Orin Nano 4-camera carrier | LI-ONO-CB-4CAM-FP | $499 | https://leopardimaging.com/product/accessories/adapters-carrier-boards/for-nvidia-jetson/li-ono-cb-4cam-fp/ | 4× 2-lane | 5 V in. Backorder. Jetson EVT path. |
| Connect Tech Boson-22 (Orin Nano/NX) | NGX021 | $609 (1–9) | https://www.wdlsystems.com/connect-tech-ngx021 | 4× 2-lane or 2× 4-lane | 9–36 V in, −40…+85 °C. |
| Auvidea JNX40S | JNX40S | €249 ex VAT | https://aetherix.com/product/auvidea-jnx40s-carrier-board-for-jetson-orin-nano-nx/ | 4× 2-lane | Out of stock at reseller. |
| Jetson Orin Nano Super Dev Kit | 945-13766-0005-000 [MPN from memory, verify] | $399 | https://www.cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101/ | 2 | Prototype benchmark platform only. |
| Radxa Dragon Q6A (QCS6490 SBC) | 8 GB | $83.28 | https://www.cnx-software.com/2025/10/27/radxa-dragon-q6a-a-qualcomm-qcs6490-edge-ai-sbc-with-gbe-wifi-6-three-camera-connectors/ | 3 (2× 2-lane + 1× 4-lane) | Cheapest way to test CAMSS raw capture on QCS6490. Not a SOM. |
| u-blox MAYA-W2 EVK | EVK-MAYA-W276-00C | ~$199 | https://www.symmetryelectronics.com/products/u-blox/evk-maya-w276-00c/ | — | Covers W266/W276. |
| Thundercomm C6490P Development Kit | — | $1,399 | https://www.thundercomm.com/product/c6490p-development-kit/ | 3× 4-lane + 2 GMSL | Only if the QCS6490 hedge is pursued. |

---

## 2. Compute-module comparison

Key criterion: a shipping Linux camera stack for ≥3 (ideally 5) CSI cameras, with raw/mono capture and external-trigger sensors, plus vendor IMX900/IMX296 drivers.

| Module (SoC) | CSI lanes / ports | Concurrent cams (native) | NPU | Typical power | Price @1 / @100 / @1k / @10k | Availability (Oct 2026) | Longevity | Linux BSP and camera stack | IMX900 / IMX296 driver support | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| **Forlinx FET3588(J)-C** (RK3588/RK3588J) | 2× DC-PHY (4-lane D-PHY or 3-trio C-PHY) + 4× 2-lane D-PHY (pairs mergeable to 4-lane) | **up to 6** (VICAP raw bypass + 2× ISP3.0) | 6 TOPS (RKNN) | Firefly measured RK3588: 1.35 W idle / **4.8 W typical** / 20 W max; Forlinx SoM standby 3.25 W @12 V | $448 (C 4 GB) / $489 (J 4 GB) @1 DigiKey; factory $170–250; @1k–10k [est.] $140–185 | In stock in small qty; "Mass Production" | Vendor only. **Rockchip publishes no silicon commitment** (techveda) | Linux 5.10.66 / 5.10.209, Forlinx Desktop 20.04/22.04, Android 12/14. Rockchip `develop-6.1` BSP. Upstream 6.1 fixes end Dec 2027. Mainline RK3588 CSI-2 receiver at patch v8 (Jan 2026) | IMX900: Rockchip BSP `imx900.c` (no trigger/mono, report A). VC `vc_mipi_core` portable; VC does Rockchip "on request". **IMX296: VEYE MV-MIPI-IMX296M ships with hardware trigger on RK3588**; mainline `imx296.c` | **Primary** |
| Firefly Core-3588J (RK3588J) | 2× DC-PHY 4-lane + 1× 4-lane or 2× 2-lane | 4 | 6 TOPS | 4.8 W typ / 20 W max @12 V | $289 (4/32) sold out | Sold out | Not stated | Ubuntu/Debian 11/Buildroot/RT | as RK3588 | Viable, but MXM3.0 314-pin and stock is thin |
| Mixtile Core 3588E (RK3588) | 3× 4-lane or **5× 2-lane** on a Jetson TX2 NX SO-DIMM | 5 | 6 TOPS | — | $132 (4/32, Mixtile store); $184 (CorpShadow, after Jan 2026 DRAM price adjustment); no 8 GB price | Out of stock | Not stated | Debian 11 / Ubuntu 22.04 / Armbian | as RK3588 | Interesting (TX2 NX footprint; Orin Nano carrier pin compatibility unverified), but small vendor, no LTS |
| Geniatech SOM3588 (RK3588) | "2× MIPI CSI" exposed | 2 | 6 TOPS | 5 V/3 A | Quote | — | "10+ year" claim | Android 12, Debian 11, Ubuntu | as RK3588 | **Fails ≥3 CSI** |
| Radxa CM5 (RK3588S2) | 1× 4-lane D/C-PHY + 1× 2-lane D-PHY | **2** | 6 TOPS | — | Launch $69 (4/32) → AllNet $89 (4/32), $119 (8/64), sold out | Sold out | Not stated | Radxa OS / Debian | as RK3588 | **Fails ≥3 CSI** |
| Toradex (Rockchip) | — | — | — | — | — | — | — | No Rockchip SOM found; Toradex is NXP/TI | — | n/a |
| Boardcon / ArmDesigner CM3588 | not verified | — | 6 TOPS | — | Quote | — | Not stated | — | — | Not evaluated (budget) |
| **Thundercomm C6490P** (QCS6490) | **5× 4-lane** D-PHY (2 C-PHY) | 5 (3 IFE + 2 IFE-lite; IFE-lite raw only) | 12–12.5 TOPS | [est.] 5–8 W | $286.52 / $228.09 / $189.60 @2k / $149.18 @30k (8 GB/128 GB UFS) | 0 stock, 16 wk | **2036** | Qualcomm Linux (BSP `qcom-6.18.y`), Ubuntu. Mainline CAMSS sc7280 = **raw RDI only** (GREY/Y10 OK; Qualcomm says no PIX/NV12 plans). CamX path proprietary | IMX900: Leopard lists RB3 Gen2 (report A). FRAMOS supplies Qualcomm drivers for FSM:GO (IMX678/676 featured; IMX900 unconfirmed). IMX296: mainline V4L2 driver should bind to CAMSS | **Longevity hedge** |
| Radxa Dragon Q6A (QCS6490) | 2× 2-lane + 1× 4-lane | 3 | 12 TOPS | — | $62 (4 GB) / $83 (8 GB) | Partly out of stock | Not stated | Ubuntu 24.04, near-mainline 6.17+ | as QCS6490 | SBC only (no SOM). Good EVT probe |
| Lantronix Open-Q 6490, TechNexion (QCS6490) | not verified | — | 12 TOPS | — | Quote | — | — | — | — | Not evaluated (budget) |
| NXP i.MX 95: Variscite DART-MX95 / Toradex Verdin iMX95 | 2× 4-lane (one muxed with DSI) | **2** (8 via virtual channels with GMSL/FPD) | 2 TOPS eIQ Neutron [vendor class] | [est.] 3–6 W | DART-MX95: "from $93" volume; $455 sample (8 GB/32 GB); EVK $569+. Verdin: quote | Available | NXP 10–15 yr program | Toradex forum (May 2026): MIPI-CSI driver issues; FRAMOS CSI not supported on Verdin iMX95 | None listed | **Fails ≥3 CSI natively; immature** |
| NXP i.MX 8M Plus | 2× 4-lane | **2** | 2.3 TOPS | [est.] 2–4 W | not verified | Available | NXP 15 yr | Mature Yocto | **FRAMOS IMX900 and VC IMX900/IMX296 (with trigger) drivers ship** | **Fails ≥3 CSI**; weak NPU |
| **NVIDIA Jetson Orin Nano 8 GB** | 8 lanes total: 4× 2-lane or 2× 4-lane (or 1× 4 + 2× 2) | **4** (8 via virtual channels) | 40 TOPS sparse INT8 (67 Super) | **7–15 W** (25 W Super) | €399 @1 / $506.66 @500 (DigiKey) / **$399 @1 ku** / [est.] $380 | Non-stock, 4 wk | **Jan 2032** | JetPack (L4T), best tooling (CUDA/TensorRT/Argus) | **Best: FRAMOS (Orin), e-con (Orin Nano/NX, up to 2 cams on their adapter), VC (IMX900 + IMX296, 9 trigger modes)** | **Backup** |
| Jetson Orin Nano 4 GB / Orin NX 8/16 GB | same CSI as Nano 8 GB | 4 | 20–34 / 70–100 TOPS | 7–25 W | $349 / $649 / $999 @1 ku | — | Jan 2032 | as above | as above | NX costs much more for no camera gain |
| Raspberry Pi CM5 (+ Hailo-8L) | 2× 4-lane | **2** | CPU only (+13 TOPS with Hailo-8L) | [est.] 4–8 W + ~2 W Hailo | 4 GB/32 GB: ~$110 calc list, $135 PiShop; 8 GB ~$175 calc | Available | (not verified this session) | Pi OS / libcamera. VC fork adds external triggering | FRAMOS (RPi5), VC (IMX900/IMX296 with trigger) | **Fails ≥3 CSI** |

**Why RK3588 over the Jetson for production:**
- **The camera port cost is fixed; the Jetson premium is per unit.** The Jetson premium is ≈ $200–250/unit over the SOM alone, and more with the NVMe it needs. At 10k units that is ≥ $2M, against an [est.] 4–8-week driver port, and VC writes Rockchip drivers on request.
- **RK3588 covers the 5-camera fallback natively.** It has 6 ports; Orin Nano needs virtual channels for a 5th camera.
- **Supply is less exposed on RK3588.** NVIDIA has already raised prices once (+33–75%). Jetson availability ends Jan 2032, which gives under 5 years if production starts in 2027–28.

**Why not QCS6490 as the primary:**
- **Its camera path is the least proven for custom mono triggered sensors.** CAMSS is raw-RDI only, a user's custom IR sensor hit STREAMON failures, and CamX needs partner support.
- **It is a solder-down LGA package.**
- **No 4 GB SKU was found.**

Its 2036 longevity and published volume curve make it the right hedge if Forlinx/Rockchip won't put a supply date in writing.

**CSI mapping on the primary (3× IMX900 plan):**
- DC-PHY0 (4-lane): stereo-top IMX900.
- DC-PHY1 (4-lane): stereo-bottom IMX900.
- D-PHY 2-lane: club IMX900 (2-lane, per report A).
- 3× 2-lane spare.
- **Fallback:** 4× IMX296 (1-lane each) + club on the 6 ports.

On Orin Nano, all three IMX900s must run 2-lane (report A says 2-lane is ample for triggered bursts). With 2× IMX900 at 4 lanes, the 8 lanes are used up and no lanes are left for the club camera.

---

## 3. Storage

- **Primary: on-SOM 32 GB eMMC 5.1, no extra part.**
  - Shot record = 8–20 crops of 256×256 (≈ 0.5–1.3 MB raw, less compressed) + JSON + optional H.265 replay clip from the RK3588 VPU (≈ 3–5 MB) [est.].
  - At ~5 MB/shot, 32 GB holds a rolling ~2,000+ shots beyond the OS.
  - Lifetime writes of ~100k shots × 5 MB ≈ 500 GB, about 16 full-drive writes. That is well inside eMMC endurance [est.].
- **Not recommended:**
  - microSD: sealed box, ingress, support burden.
  - Separate NVMe: NAND shortage pricing. Kingston industrial 2230 is $310 for 256 GB and $438 for 512 GB, with backorders refused.
- **Upgrade path:** the 8 GB/64 GB SoM variant (+$83 at qty 1). A second eMMC is not worth it.
- **Jetson backup:** NVMe is mandatory because the Orin Nano module has no eMMC. Use a 2230 industrial pSLC such as ATP N700Si 40 GB (AF40GSAJB-DBAIX), quote only.

## 4. Wi-Fi 6 + BT 5.x

| Module | Chip / host IF | Approvals | Linux | $@1 / volume | Verdict |
|---|---|---|---|---|---|
| **u-blox MAYA-W266-00B** | NXP IW611, 1×1 Wi-Fi 6 + BT 5.3; SDIO 3.0 + UART | RED, UKCA, FCC, ISED, MIC, **KCC**, ANATEL, ACMA (W266/W276 only) | `mxm_wifiex` (u-blox/NXP), kernel ≥4.19. Integrated in NXP BSPs; must be built for the Rockchip BSP | $14.17 / $11.58 @500 | **Pick** |
| u-blox MAYA-W276-00B | IW612 (+802.15.4) | same | same | $13.85 / $12.36 @500 | Equivalent; Thread radio not needed |
| Ezurio Sona IF573 453-00120 / -00119 | Infineon CYW55573, 2×2 Wi-Fi 6E; PCIe or SDIO | FCC, ISED, CE/UKCA, MIC, RCM; **no KC** | Infineon/Ezurio backports | $39.51 / £26.22 @100 | Jetson-path PCIe option |
| AzureWave AW-XM458 / AW-XM458MA-PUR | NXP 88W9098, 2×2 Wi-Fi 6; PCIe+UART (LGA or M.2) | FCC TLZ-XM9098, CE, IC, RCM, MIC, NCC; **no KC** | NXP `moal`; **validated by Forlinx on FET3588** | $27 @1 (LGA, DigiKey Marketplace); ~$20–26 @5k | Good fallback if SDIO is not pinned out on the SoM |
| Murata Type 2EA / 1YN | CYW55573 / CYW43439 | not checked (budget) | — | — | Not evaluated |

**Open item:** confirm the FET3588J-C B2B pinout exposes the RK3588 SDIO 3.0 host. The dev board routes Wi-Fi via M.2/PCIe. If SDIO is not exposed, use AW-XM458 (PCIe) and buy KC certification at the product level.

Antenna options:
- MAYA-W266 internal antenna: certified, $0.
- Or RF_ANT1 → **Hirose U.FL-R-SMT-1(10)** → **Ezurio EFB2455A3S-20MHF1** FlexPIFA (2.5/3.0 dBi, 200 mm MHF1 cable), mounted on the plastic housing away from the heatsink.
  - Check the u-blox approved-antenna list before relying on the modular grant.

## 5. Gigabit Ethernet (Indoor) and PoE

- **The SoM has 2× GMAC RGMII and no PHY on the module.** Use a Realtek **RTL8211F-CG** on the carrier (Forlinx validated the RTL8211FSI-CG).
  - LCSC: $1.52 @1, $1.04 @100, $0.89 @980; 60–89k in stock.
- **MagJack:** Pulse **JXD1-0001NL**, $7.59 / $5.48 @100 / $4.66 @1k, −40…+85 °C.
  - For an exposed rear panel, consider an IP-rated RJ45 in report F.
- **PoE+ (802.3at Type 2, 25.5 W at the PD):**
  - Silvertel **AG53012** (12 V, isolated, SIL, $11.75) or AG5300 ($13.50 @1,040), plus a PoE MagJack **JK0-0177NL** ($8.29 @1,035).
  - BOM delta ≈ **+$13–18**, plus a bundled 802.3at injector [est. $15–25 retail], since simulator PCs don't supply PoE.
  - Indoor draw estimate: SoM 5–12 W + 3 cameras ~2–3 W + radar ~1–2 W + IR strobe average (report C) + Wi-Fi/MCU ~1 W ≈ **15–23 W** [est.]. That is inside 25.5 W only if the LED average stays small; buffer the strobe energy in local capacitance.
  - **Recommendation:** lay out the footprint and decide at EVT from measured power. If over 22 W, 802.3bt Type 3 is needed, which costs more and is out of scope here.
  - TI TPS23758 is **not** suitable: it is a Type 1 (13 W) device despite the "802.3at" label.

## 6. PMIC / SoM power tree

- **On module:**
  - The Forlinx FET3588 carries the RK3588 PMIC and core regulators. Rockchip SOMs normally use RK806 plus discrete big-core bucks; **confirm the exact PMIC from Forlinx schematics, not verified here**.
  - SoM input: the brief says "DC 5–13 V"; the product page says "12 V DC". **Resolve before carrier layout.**
- **Carrier (both SKUs):**
  - System rail 7–17 V (Pro battery / Indoor adapter or PoE 12 V) → **TPS56637RPAR → 5.0 V / 6 A** → SoM VIN (and USB 5 V if any).
  - A second **TPS56637RPAR → 3.3 V** feeds MAYA-W266 (VIO_SD at 1.8 V or 3.3 V, check the SDIO voltage mode), RTL8211F, STM32G474 and radar digital.
  - Camera sensor rails (1.2/1.8/2.9 V) are on the camera modules (report A).
- **If the SoM really needs 12 V:** the Pro's 7–12 V battery region needs a buck-boost (e.g., TI LM5176 class, not priced). Feeding 5 V avoids this. **The Jetson backup takes 5 V too**, so one carrier power architecture serves both.
- **Out of my slice:** input protection (eFuse, TVS, reverse polarity), battery charger/BMS and display power belong to the power and mechanical reports.

## 7. Timing / real-time MCU

| | **STM32G474** (pick) | RP2350A (alternate) | STM32H5 (e.g., H503/H563) |
|---|---|---|---|
| Edge placement | HRTIM: 184 ps resolution, 6 timer units / 12 outputs, synchronized | PIO: 12 state machines, 1 cycle = 6.67 ns at 150 MHz, deterministic | General timers at 250 MHz → 4 ns; no HRTIM |
| Jitter vs async radar trigger | ~1 HRTIM clock (≈ 6 ns) on external-event input | ~1–2 sys clocks (≈ 7–13 ns) | ≈ 4–8 ns |
| Hardware safety | **Fault inputs + 7 comparators + DACs kill outputs in ns**: firmware-independent max-pulse and over-current cutoff for the IR array (eye safety) | None analog; software/PIO only | Limited |
| Price | CET6 $7.95 @1; CEU6 $6.16 @100, $5.43 reel | $0.99 @500, $0.95 @1k (+ ~$0.3 QSPI flash) | not priced |
| Supply | CEU6 0 stock / 52 wk; **CET6 in stock** | Good | — |

- **Pick: STM32G474CET6.** The hardware interlock is worth ~$5 in a product whose IR strobes need an IEC 62471 risk-group argument. It also has 5× 4 MS/s ADCs, so it could absorb the radar MCU's job (report D uses an MSPM0G3507) in a later cost-down.
- **Use RP2350A** (Pico 2 for prototyping, $6.12) if ST lead times bite.
- **Link to SoC:** SPI (shot/trigger timestamps) + UART (control), plus one GPIO "shot armed/fired" line into the SoM for frame-to-trigger correlation.
- **Can the SoC do it instead?**
  - **No** for event-driven triggers: Linux GPIO has tens of µs of jitter.
  - RK3588 hardware PWM can make periodic ns-accurate pulses but cannot sequence off a radar event deterministically.
  - The Orin's SPE (Cortex-R5) could, but it is niche firmware work.
  - Keep the MCU. It also owns power sequencing and wake on radar.

---

## 8. Key decisions and risks

**Decisions**
1. Production SOM: **Forlinx FET3588J-C+224GSE32GI** (RK3588J, 4 GB/32 GB). Commercial cost-down: FET3588-C+244GSE32GC.
2. Backup: **Jetson Orin Nano 8 GB 900-13767-0030-000** + ATP 2230 NVMe + Sona IF573 on a separate 5 V-fed carrier. Hedge: **Thundercomm C6490P-U8A-3690000** (to 2036).
3. 4 GB RAM; on-SOM eMMC only.
4. **MAYA-W266-00B** Wi-Fi 6/BT 5.3 (only option with KC among those checked).
5. **RTL8211F-CG + JXD1-0001NL** for Indoor GbE. PoE+ as a footprint option (AG53012 + JK0-0177NL).
6. **TPS56637** ×2 for 5 V/3.3 V.
7. **STM32G474CET6** timing MCU.
8. A custom carrier is required for both SKUs (form factor, battery, MCU, LED drivers). EVT can start on the **Forlinx OK3588-C** (5 CSI) or a **Leopard LI-ONO-CB-4CAM-FP** (Jetson).

**Risks (most severe first)**
1. **The IMX900 trigger + mono driver on RK3588 does not exist yet.**
   - Mitigation: port `vc_mipi_core` (or extend the Rockchip BSP `imx900.c` with the FRAMOS TRIGMODE registers), or buy a VC "on request" Rockchip driver.
   - Gate it at end of Phase 1: if 3 triggered mono streams are not landing on RK3588 by then, switch to the Jetson carrier.
2. **No Rockchip silicon-longevity commitment.** Get a written supply date and an LTB clause from Forlinx. Keep QCS6490 (2036) as a hedge.
3. **Kernel age.** Forlinx is on 5.10 and the Rockchip vendor tree on 6.1, whose upstream fixes end Dec 2027. Budget for a security-maintenance plan or a mainline migration.
4. **Distribution pricing is thin.** DigiKey is a Marketplace listing capped at 10 units per 30 days, so all ≥100 SOM prices are estimates. Quote Forlinx before DVT.
5. **Jetson lane budget.** 8 lanes, 4 cameras max; IMX900 must run 2-lane for 3 cameras, and 5× IMX296 doesn't fit without virtual channels. Jetson prices already rose 33–75% in July 2026.
6. **MAYA-W266:** 0 stock now (350 due 9 Oct 2026), 20-week lead, out-of-tree driver, and SDIO pin-out on the SoM unverified. Fallback is the AW-XM458 (PCIe, Forlinx-validated, no KC).
7. **SoM input-voltage ambiguity** (5–13 V vs 12 V) affects the Pro power stage.
8. **PoE+ power margin** (25.5 W) may be too small once the IR strobe average is known.
9. **STM32G4 lead times** (52 weeks on QFN). Use the LQFP or the RP2350 alternate.
10. **External antenna and modular grant.** An antenna not on u-blox's approved list needs a permissive change. The internal antenna avoids this.

---

## 9. Sources

- Jetson price rise (July 2026): https://www.cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101/
- Jetson lifecycle (Jan 2032): https://developer.nvidia.com/embedded/lifecycle
- Orin Nano module specs and price: https://www.siliconhighwaydirect.com/product-p/900-13767-0030-000.htm
- DigiKey Orin Nano listings:
  - 8 GB: https://www.digikey.com/en/products/result?keywords=900-13767-0030-000
  - 4 GB: https://www.digikey.com/en/products/result?keywords=900-13767-0040-000
- Jetson carriers:
  - Leopard: https://leopardimaging.com/product/accessories/adapters-carrier-boards/for-nvidia-jetson/li-ono-cb-4cam-fp/
  - Connect Tech: https://www.wdlsystems.com/connect-tech-ngx021
  - Auvidea: https://aetherix.com/product/auvidea-jnx40s-carrier-board-for-jetson-orin-nano-nx/
- Forlinx:
  - Product brief: https://www.forlinx.net/download/FET3588-C-and-OK3588-C-product-brief.pdf
  - Product page: https://www.forlinx.net/product/rk3588-som-134.html
  - DigiKey: https://www.digikey.com/en/products/result?keywords=FORLINX-FET3588
  - DigiKey 4 GB SoM: https://www.digikey.com/en/products/detail/forlinx-embedded/FORLINX-FET3588-C-244GSE32GCC11/21776976
  - Factory listing: https://www.globalsources.com/product/fet3588-c-rk3588-rockchip_1208005892f.htm
  - OK3588-C price: https://www.accio.com/plp/forlinx-ok3588-c-price
- Firefly Core-3588J: https://www.t-firefly.com/product/core/core3588j
- Mixtile Core 3588E:
  - Product page: https://www.mixtile.com/core-3588e/
  - Store: https://www.mixtile.com/store/som/core-3588e/
  - CorpShadow: https://corpshadow.biz/iot/mixtile/mixtile-core-3588e
- Geniatech SOM3588: https://www.geniatech.com/product/som3588/
- Radxa CM5:
  - Product page: https://radxa.com/products/cm/cm5/
  - Product brief: https://dl.radxa.com/cm5/radxa_cm5_product_brief.pdf
  - AllNet China: https://shop.allnetchina.cn/products/radxa-cm5-1
  - Launch blog: https://radxa.com/blog/CM5-Official-Announcement/
- RK3588 longevity and BSP: https://www.techveda.live/rk3588/
- Mainline Rockchip CSI-2 receiver patches: https://ratatoskr.run/lkml/2026/01/3377619/t
- VEYE MV-MIPI-IMX296M on RK3588:
  - Product: https://www.veye.cc/en/product/mv-mipi-imx296m/
  - Driver repo: https://github.com/veyeimaging/rk35xx_orangepi
  - Application notes: https://wiki.veye.cc/index.php/Rockchip_platform_Application_Note_Index
- Vision Components:
  - Driver list: https://www.mipi-modules.com/fileadmin/external/documentation/software/vc_mipi_driver_list/index.html
  - Compatible boards: https://www.mipi-modules.com/en/mipi-compatible-processor-boards/
  - vc_mipi_core: https://github.com/VC-MIPI-modules/vc_mipi_core
- FRAMOS IMX900: https://docs.framos.com/en/latest/FSMEcosystem/ProductDocumentation/FSMGO/IMX900.html
- FRAMOS Qualcomm: https://framos.com/solutions/processing-platforms/qualcomm/
- e-con IMX900: https://www.e-consystems.com/camera-modules/3mp-sony-pregius-imx900-global-shutter-camera-module.asp
- Thundercomm C6490P:
  - SOM page: https://www.thundercomm.com/product/c6490p-som/
  - Arrow: https://www.arrow.com/en/products/c6490p-u8a-3690000-qcs6490/thundercomm
  - Dev kit: https://www.thundercomm.com/product/c6490p-development-kit/
  - C6490 datasheet: https://fcc.report/FCC-ID/2AOHHTURBOX-C6490/6641523.pdf
- QCS6490 camera stack:
  - CAMSS docs: https://docs.kernel.org/admin-guide/media/qcom_camss.html
  - BSP status: https://www.techveda.live/qcs6490/
  - Qualcomm Linux V4L2 guide: https://docs.qualcomm.com/bundle/publicresource/topics/80-70015-17/v4l2_interface.html
- Radxa Dragon Q6A: https://www.cnx-software.com/2025/10/27/radxa-dragon-q6a-a-qualcomm-qcs6490-edge-ai-sbc-with-gbe-wifi-6-three-camera-connectors/
- i.MX 95:
  - Variscite store: https://shop.variscite.com/product/system-on-module/dart-mx95-system-on-module/
  - Variscite datasheet: https://variscite.com/wp-content/uploads/2024/06/DART-MX95_Datasheet.pdf
  - Toradex Verdin: https://www.toradex.com/computer-on-modules/verdin-arm-family/nxp-imx95
  - Toradex forum: https://community.toradex.com/t/current-state-of-functionality-on-imx95-verdin/28953
- Raspberry Pi CM5 pricing:
  - Raspberry Pi news: https://www.raspberrypi.com/news/more-memory-driven-price-rises/
  - CNX: https://www.cnx-software.com/2025/10/02/ddr4-supply-demand-stress-leads-to-raspberry-pi-cm4-cm5-price-increases/
  - PiShop: https://www.pishop.us/product/raspberry-pi-compute-module-5-4gb-ram-32gb-emmc-cm5004032/
- u-blox MAYA-W2:
  - Datasheet R07: https://content.u-blox.com/sites/default/files/documents/MAYA-W2_DataSheet_UBX-22009721.pdf
  - DigiKey: https://www.digikey.com/en/products/detail/u-blox/MAYA-W266-00B/18688832
  - Symmetry (EVK): https://www.symmetryelectronics.com/products/u-blox/evk-maya-w276-00c/
- Ezurio Sona IF573:
  - DigiKey: https://www.digikey.com/en/products/detail/ezurio/453-00120/20525586
  - Regulatory info: https://connectivity-staging.s3.us-east-2.amazonaws.com/2025-03/EZ-RegulatoryInfo-Sona-IF573_v2_0.pdf
- AzureWave AW-XM458:
  - DigiKey: https://www.digikey.com/en/products/detail/azurewave-technologies-inc/AW-XM458/25881658
  - Octopart: https://octopart.com/part/azurewave/AW-XM458
  - Techship: https://techship.com/products/brands/azurewave/
- Antenna and connector:
  - EFB2455A3S-20MHF1: https://www.digikey.com/en/products/result?keywords=EFB2455A3S-20MHF1
  - FlexPIFA datasheet: https://www.ezurio.com/documentation/datasheet-dual-band-flexpifa
  - U.FL: https://www.digikey.com/en/products/result?keywords=U.FL-R-SMT-1(10)
- Ethernet:
  - RTL8211F-CG: https://www.lcsc.com/product-detail/C187932.html
  - RTL8211FI-CG: https://www.lcsc.com/product-detail/C717681.html
  - JXD1-0001NL: https://www.digikey.com/en/products/detail/pulse-electronics/JXD1-0001NL/5361447
  - JK0-0177NL: https://www.digikey.com/en/products/detail/pulse-electronics/JK0-0177NL/2649122
- PoE:
  - AG5300: https://www.digikey.com/en/products/detail/silvertel/AG5300/19285345
  - AG53000 series: https://www.digikey.com/en/product-highlight/s/silvertel/ag53000-series-poe-pd-modules
  - TPS23758: https://www.ti.com/product/TPS23758
- Regulator: https://www.digikey.com/en/products/detail/texas-instruments/TPS56637RPAR/10715537
- MCUs:
  - STM32G474CEU6: https://www.digikey.com/en/products/detail/stmicroelectronics/STM32G474CEU6/10326774
  - STM32G474CET6: https://www.digikey.com/en/products/detail/stmicroelectronics/STM32G474CET6/10326773
  - RP2350A: https://www.digikey.com/en/products/detail/raspberry-pi/SC1509-13/26241107
- NVMe:
  - Kingston OM3SGP4512K2-A00: https://www.digikey.com/en/products/detail/kingston-technology/OM3SGP4512K2-A00/26832996
  - ATP N700Si datasheet: https://www.mouser.com/datasheet/2/1133/ATP_I_Temp__NVMe_PCIe_Gen3_pSLC_M_2_2230_SSD_Datas-3009768.pdf

**Not verified this session (search budget):** Boardcon/ArmDesigner CM3588, Lantronix Open-Q 6490, TechNexion QCS6490, Murata 2EA/1YN, i.MX 8M Plus SOM pricing, the Hailo-8L price, the exact Forlinx PMIC and B2B connector MPNs, the Orin Nano Super devkit MPN, the u-blox approved-antenna list, and the RK3588 SDIO pin-out on the FET3588.
