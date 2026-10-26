# 09: Manufacturing, BOM, NRE, Team, Timeline and Funding Plan

*Portable camera-based golf launch monitor (side-of-ball or down-the-line). Research date: 7 October 2026.*

---

## 0. How to read this document

- **Sourced figures** have a URL next to them.
- **[est.]** marks an engineering or commercial estimate made by the author from industry experience. These were **not** verified against a 2026 source, because the shared web-search budget for this research session ran out partway through. Treat [est.] numbers as planning placeholders and replace them with quotes. The highest-value numbers to get quoted first are listed in §10.
- The tariff, compute-module, competitor, funding-comparable and tooling figures are sourced. Most per-component prices below the SoM level, and the salary bands, are estimates.

### Executive summary (the ten things that matter)

1. **The compute module drives the BOM.** NVIDIA quietly raised Jetson prices in July 2026. The Orin Nano 8GB module went from **$299 to $399 at 1KU**, and the Orin Nano 4GB from $199 to $349 ([CNX Software, 22 Jul 2026](https://www.cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101/)). This follows a DRAM shortage: TrendForce reported DRAM contract prices up 90–95% QoQ in Q1 2026 ([IEEE Spectrum](https://spectrum.ieee.org/ram-shortage-price-increase), [tech-insider](https://tech-insider.org/dram-ram-price-crisis-2026/)). On a Jetson design the SoM is **about 50% of the BOM**. An RK3588-class module costs about **$110–150** in volume [est., from Alibaba/Firefly listings in [Radxa CM5 results](https://liliputing.com/radxa-cm5-is-a-compute-module-with-an-rk3588s-processor-and-up-to-16gb-ram/), [Firefly Core-3588J](https://www.firefly.store/products/core-3588j-8k-ai-core-board-rockchip-rk3588-new-gen-8-core-64-bit-processor)]. That choice alone moves landed cost by about $280 per unit.
2. **Estimated BOM.** About **$900 / $770 / $700** at 1k / 5k / 10k for a 3-camera, Jetson Orin Nano 8GB, radar-equipped "Pro" unit. About **$625 / $490 / $430** for the same unit on RK3588.
3. **Do not do final assembly in China for the US market.** In October 2026 a China-origin unit pays MFN, plus the legacy Section 301 list duty (25% on Lists 1–3 or 7.5% on List 4A), plus the **new 12.5% Section 301 "forced-labor" duty** in effect since 24 July 2026 ([CBP CSMS #69326983](https://content.govdelivery.com/accounts/USDHSCBP/bulletins/421d887), [EY](https://taxnews.ey.com/news/2026-1607-ustr-finalizes-section-301-forced-labor-tariffs-on-60-economies-additional-tariffs-of-10-percent-or-125-percent-take-effect-24-july-2026)). That is about **37–39%**. Vietnam and Thailand pay 12.5% plus MFN. Malaysia and non-USMCA Mexico pay 10% plus MFN. **Taiwan is capped at 10% combined.** Korea and Japan are capped at 12.5% combined. USMCA-qualifying goods are exempt ([Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/07/and-the-tariff-beat-goes-on)). On a $850 FOB unit, China costs about **$200+ more in duty per unit** than Vietnam or Taiwan.
4. **Landed cost at 5k units (Pro config):** about **$1,200 from China** versus **about $980–1,010 from Taiwan, Vietnam, Malaysia or Mexico**. Add a 3–5% warranty reserve. At a $2,499 MSRP sold through dealers (wholesale about $1,500–1,750), a Jetson build has thin margins. An RK3588 or Qualcomm-class build at about $650 landed works well.
5. **NRE excluding salaries: about $0.7–1.5M** in total. That covers ID/ME, PCB spins, about $90–220k of injection tooling, $60–180k of certification, $100–300k of test and calibration fixtures, and reference equipment.
6. **Factory stereo calibration is a production station you have to build and own.** Each unit is imaged against fixed targets at known poses in a rigid, temperature-controlled fixture, 1–3 minutes per unit, then verified with a live "shot test". Each station costs $25–80k [est.]. One station on one shift covers about 10k units a year.
7. **Prototype path.** Jetson Orin Nano Super dev kit ($399 since July 2026), IMX296 global-shutter MIPI cameras ($45–85: [InnoMaker](https://www.inno-maker.com/product/cam-mipi296raw-trigger/), [Arducam](https://www.arducam.com/1-58mp-imx296-mono-global-shutter-camera-module-with-m12-lens-for-raspberry-pi.html)), and a **used Foresight GCQuad (about $8.5–12.5k)** as ground truth. The GCQuad is camera-based, so it is the right reference for spin. Optionally add a used TrackMan 4 (about $14–17.5k plus a $1,000 transfer fee) ([friendlygolfer](https://friendlygolfer.com/used-gcquad/), [best-golf-simulator](https://best-golf-simulator.com/trackman-cost/)).
8. **Timeline.** It is now October 2026. Plan for **holiday 2028 (stretch)** and **spring 2029 (realistic)**. First-time hardware teams usually slip 3–6 months or more. Instrumental's handbook notes up to about 40% of EVT units can fail, and that renaming a fake DVT as "EVT2" adds a build ([Instrumental](https://instrumental.com/build-better-handbook/evt-dvt-pvt)).
9. **Funding.** A **$4–6M seed** gets you to EVT plus proven accuracy. A **$10–15M Series A** at DVT funds production inventory and go-to-market. That is about **$13–18M to launch** including contingency, with part of the inventory financed through pre-orders and PO/inventory financing. The category supports exits: Versant agreed to buy Full Swing for **$530M** in July 2026 ([CNBC](https://www.cnbc.com/2026/07/06/versant-to-buy-golf-simulator-company-full-swing.html), [SGB](https://sgbonline.com/versant-media-group-acquires-golf-simulator-platform-full-swing/)). Creatz (Uneekor's parent) made ₩104.2bn revenue at a 24% operating margin in 2025 and is listing on KOSDAQ in October 2026 ([IB Tomato](https://www.newstomato.com/ReadNews.aspx?no=1312861)).
10. **Competition is moving down-market quickly.** Singapore's Pixel Field (more than 1M devices shipped) launched the NeoPace G10 Pro on Kickstarter on 17 Sep 2026. It has 3 cameras (2 at up to 480 fps), 24 GHz radar, $899 founder pricing, $1,499 MSRP, and ships November 2026. It raised about $445k from 476 backers in its first days ([PR Newswire](https://www.prnewswire.com/news-releases/neopace-g10-pro-ai-powered-3d-replay-golf-launch-monitor-now-crowdfunding-on-kickstarter-302881801.html), [gizmocrowd](https://www.gizmocrowd.com/post/neopace-g10-pro-review)). A $1,999–2,999 product has to clearly beat this on accuracy, especially spin, club data and outdoor performance.

---

## 1. Bill of Materials

### 1.1 Reference configuration assumed

| Subsystem | Assumption |
|---|---|
| Ball cameras | 2 × global-shutter mono sensors (IMX296-class, 1.6 MP, external trigger) forming a stereo pair, with NIR-corrected M12 lenses and 850 nm bandpass filters. Multi-exposure strobing gets around the sensors' frame-rate limits. |
| Club / alignment / user camera | 1 × lower-cost GS or wide RGB camera (OV9281 / AR0144 class) |
| Illumination | 12 × high-power 850 nm IR LEDs (OSRAM Oslon Black SFH 4715AS class) with TIR secondary optics, plus a GaN-FET pulse driver with capacitor bank and a timing MCU |
| Compute | **Config A:** Jetson Orin Nano 8GB plus 128 GB NVMe. **Config B:** RK3588 8GB SOM with eMMC on board. |
| Radar (optional) | 24 GHz Doppler or 60 GHz FMCW module for triggering, club speed and outdoor ball speed sanity checks |
| Radio | Wi-Fi 6 + BT 5.x pre-certified M.2/LGA module (the Orin Nano module has no Wi-Fi) |
| Battery | About 72 Wh Li-ion (4 × 21700 5 Ah as 2S2P or 4S1P) with BMS. **Keep it under 100 Wh** so it ships as UN3481 "packed with/contained in equipment" without Class 9 full-regulation pain, and stays airline carry-on legal. |
| Charging | USB-C PD 65 W sink (TI TPS25750 + BQ2579x class), plus a 65 W GaN charger in the box |
| Enclosure | 5–7 injection-molded PC/ABS parts, an IR-pass window (PC/PMMA IR-transmissive grade), TPE bumper, an aluminum internal optical bench holding the cameras rigidly (this is critical for keeping stereo calibration stable), and a heatsink with blower fan |
| Mounting / aids | 1/4"-20 tripod insert, bubble level, Class 2 alignment laser (or camera-based alignment) |
| In box | Molded EVA hard carry case, retail box, cable, charger, alignment stick, quick-start guide |

### 1.2 Per-unit BOM (Config A, Jetson Orin Nano 8GB). USD.

| # | Item | 1k | 5k | 10k | Basis |
|---|---|---|---|---|---|
| 1 | 2 × ball camera modules (sensor, sensor PCB/FPC, holder, lens, filter, active focus and glue) | 112 | 92 | 83 | Sensor about $24–34 each: one broker lists the IMX296LQR-C at about $33.60 ([digipart/IMX296 results](https://www.digipart.com/part/IMX296LQR-C)). Complete retail modules are $45 at 120+ ([InnoMaker](https://www.inno-maker.com/product/cam-mipi296raw-trigger/)), $50 for the Raspberry Pi GS Camera ([TechEBlog](https://www.techeblog.com/raspberry-pi-global-shutter-camera-module-price-specs-release-date/)), and $64.99 for Arducam ([Arducam](https://www.arducam.com/1-58mp-imx296-mono-global-shutter-camera-module-with-m12-lens-for-raspberry-pi.html)). Custom module at volume about $40–56 [est.]. |
| 2 | 3rd camera (club / alignment) | 25 | 20 | 18 | [est.] OV9281/AR0144-class module |
| 3 | 12 × 850 nm high-power IR LEDs + TIR optics | 37 | 30 | 25 | [est.] about $1.7–2.5 per LED, $0.4–0.6 per optic |
| 4 | LED pulse driver (GaN FETs, cap bank, timing MCU, current sense) | 15 | 12 | 10 | [est.] |
| 5 | **Compute SoM: Jetson Orin Nano 8GB** | **399** | **385** | **370** | List price $399 at 1KU since July 2026 ([CNX](https://www.cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101/)). Arrow showed a 12-week lead time ([Arrow](https://www.arrow.com/en/products/900-13767-0030-000/nvidia.html)). The 5k/10k discount is [est.] and not guaranteed. |
| 6 | NVMe SSD 128 GB (the Orin Nano module has no eMMC) | 18 | 15 | 14 | [est.] NAND prices are elevated in 2026 ([dropreference](https://dropreference.com/en/blog/news/memory-dram-ssd-shortage-2026-price-increase-2028)) |
| 7 | Carrier PCBA (8-layer, PMIC, STM32-class MCU, IMU, MIPI connectors, USB-C) | 55 | 42 | 36 | [est.] |
| 8 | Wi-Fi 6/BT module + 2 antennas | 18 | 14 | 12 | [est.] Use a module with an existing FCC modular grant |
| 9 | Radar module (optional) | 35 | 25 | 20 | [est.] 24 GHz Doppler or 60 GHz (Infineon BGT60 / TI IWR6843AOP class) |
| 10 | Battery pack, about 72 Wh, 4 × 21700 + BMS + wrap + harness | 36 | 30 | 27 | [est.] Cells about $3–4.50 each. Pack assembly by a pack house. Section 301 on Chinese Li-ion rose to 25% on 1 Jan 2026 if packs are imported separately ([htslookup](https://htslookup.com/changes/2026-01-01-section-301-china-2024-increases/)). |
| 11 | USB-C PD + charger + protection | 8 | 6 | 5 | [est.] |
| 12 | Molded enclosure parts (5–7 PC/ABS + TPE bumper), texture, pad print | 28 | 19 | 15 | PC/ABS parts run $1.80–3.60 each at 1k and $1.40–2.60 at 5k from aluminum tools ([xinyangmfg](https://xinyangmfg.com/low-volume-injection-molding-cost-hardware-startups/)). Large housings plus finishing make this [est.]. |
| 13 | IR-pass window (molded IR-transmissive PC/PMMA with AR or hard coat) | 5 | 3.5 | 3 | [est.] |
| 14 | Internal optical bench (aluminum: CNC at 1k, die-cast at 5k+) | 25 | 12 | 9 | [est.] |
| 15 | Thermal: heatsink + blower + pads | 18 | 14 | 12 | [est.] The Orin Nano runs at 7–25 W ([Silicon Highway](https://www.siliconhighwaydirect.com/product-p/900-13767-0030-000.htm)) |
| 16 | Tripod insert, bubble level, alignment laser, fold-out feet | 8 | 6 | 5 | [est.] |
| 17 | UI: buttons, status LEDs / small display | 6 | 5 | 4 | [est.] |
| 18 | Internal FPCs, cables, fasteners, gaskets, labels | 12 | 9 | 8 | [est.] |
| 19 | Retail packaging (rigid box, inserts, documentation) | 10 | 7 | 6 | [est.] |
| 20 | Custom EVA hard carry case | 18 | 13 | 11 | [est.] |
| 21 | In-box accessories (65 W GaN charger, cable, alignment stick, cloth) | 14 | 11 | 10 | [est.] |
| | **BOM total, Config A** | **≈ $902** | **≈ $771** | **≈ $703** | |

### 1.3 Config B: RK3588 (or Qualcomm QCS6490-class) compute

Swap row 5 for an RK3588 8GB SOM with eMMC at **about $140 / $120 / $110** [est.]. Supporting data: Firefly Core-3588J 8GB/64GB is $379 retail, Geniatech SOM3588 is $219–439, generic 8GB/64GB SOMs on Alibaba are $108–143, and a Radxa CM5 4GB is about $80–115 from Chinese suppliers ([Firefly](https://www.firefly.store/products/core-3588j-8k-ai-core-board-rockchip-rk3588-new-gen-8-core-64-bit-processor), [Geniatech](https://shop.geniatech.com/product/rk3588-board/), [Alibaba Radxa CM5](https://www.alibaba.com/product-detail/Radxa-Cm5-Rk3588s-Eight-Core-Cpu_1601358987823.html)). Radxa commits to supplying the CM5 through 2032 ([CNX](https://www.cnx-software.com/2022/09/08/radxa-cm5-rockchip-rk3588s-module-raspberry-pi-cm4/)). Drop row 6, since eMMC is on the SOM.

| | 1k | 5k | 10k |
|---|---|---|---|
| **BOM total, Config B** | **≈ $625** | **≈ $490** | **≈ $430** |

**Trade-off.** Jetson gives CUDA/TensorRT, the best camera ecosystem (Arducam, e-con, Leopard, RidgeRun drivers) and the fastest path for a software team. RK3588 has a 6 TOPS NPU, mature MIPI/ISP and hardware encoders. It costs about $260–280 less per unit, but needs more BSP and driver work and its NPU toolchain (RKNN) is weaker. **Recommendation:** prototype on Jetson, keep the vision pipeline portable (classical CV + ONNX models, with no CUDA-only kernels in the hot path), and make the production compute decision at the end of Phase 1 based on measured latency and power. The Orin Nano 4GB at $349 is not a meaningful saving.

### 1.4 Lean variant (useful for pricing tiers)

Removing the radar, 3rd camera, laser and carry case cuts about $70 (5k) from either config. Examples: Config B "Lite" at about $420 BOM at 5k; Config A "Lite" at about $700.

---

## 2. Landed cost

### 2.1 Tariff environment for US imports (as of October 2026)

| Layer | Status (Oct 2026) | Source |
|---|---|---|
| IEEPA "reciprocal" / "fentanyl" tariffs | Struck down by the Supreme Court. Replaced by a temporary 10% **Section 122** global surcharge (24 Feb – 24 Jul 2026), which expired at its 150-day limit. | [htsapi](https://htsapi.dev/section-301-tariffs), [Honigman](https://www.honigman.com/alert-3462), [Fennemore](https://www.fennemorelaw.com/new-u-s-tariffs-replace-expiring-section-122-tariffs/) |
| **Section 301 "forced-labor" tariffs (new, 24 Jul 2026)** | **12.5%** for 41 economies including **China, Vietnam, Thailand, Singapore, Philippines**. **10%** for 19 including **Malaysia, Mexico, India, Indonesia, Cambodia, UK, Canada**. **Combined-rate caps:** EU and **Taiwan** at 10% combined with MFN; **Japan, South Korea**, Switzerland at 12.5% combined. **USMCA-qualifying goods are exempt.** Section 232 goods (including "semiconductor articles" per note 52(f)) are exempt. No sunset date. Being challenged at the CIT. | [EY](https://taxnews.ey.com/news/2026-1607-ustr-finalizes-section-301-forced-labor-tariffs-on-60-economies-additional-tariffs-of-10-percent-or-125-percent-take-effect-24-july-2026), [CBP CSMS #69326983](https://content.govdelivery.com/accounts/USDHSCBP/bulletins/421d887), [Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/07/and-the-tariff-beat-goes-on), [Global Trade Alert](https://globaltradealert.org/blog/forced-labour-section-301-final-action) |
| Legacy China Section 301 lists | Still apply **on top**: 25% on Lists 1–3, 7.5% on List 4A, and 25–100% on four-year-review items. **Li-ion non-EV batteries (8507.60) went from 7.5% to 25% on 1 Jan 2026.** | [tariffcalculator2026](https://tariffcalculator2026.com/section-301-tariffs-on-china-latest-updates-2026), [htslookup](https://htslookup.com/changes/2026-01-01-section-301-china-2024-increases/), [Holland & Knight 2024](https://www.hklaw.com/en/insights/publications/2024/09/ustr-finalizes-action-on-new-and-increased-section-301-tariffs) |
| Pending risk | A separate Section 301 **excess-capacity investigation into 16 economies (including China and Mexico)**, opened 11 March 2026. Any resulting tariffs would likely stack on the forced-labor duty. | [tariffstool](https://www.tariffstool.com/guides/section-301-replacing-section-122), [Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/07/and-the-tariff-beat-goes-on) |

**HTS classification is unresolved and matters.** No CBP ruling specifically on launch monitors turned up. Importers declare them under **9506.39** (golf equipment: SkyTrak, Rapsodo, GC3) and under **9031.80** (measuring instruments: also a GC3). CBP's reasoning in a cycling-sensor ruling points to 9031.80.80 ([Volza shipment data](https://www.volza.com/hs-codes/search/golf-launch-monitor/united-states/), [CBP CROSS](https://rulings.cbp.gov/search?term=9506.39.0080)). Cameras under 8525.89.30 carry 25% Section 301 from China ([CBP N327719](https://rulings.cbp.gov/ruling/n327719)). **Action:** get a binding CBP ruling under 19 CFR Part 177 before DVT. The rest of this section assumes **9031.80.80, MFN 1.7%, China List 25%** [est.; verify the list membership of the 10-digit code]. If 9506.39 on List 4A turns out to apply, the China stack falls to about 25%, but China is still the worst option.

**Origin rule.** For non-FTA countries, origin is set by *substantial transformation*. Final box-build in Vietnam of a PCBA made in China risks being treated as **China origin**. The SMT/PCBA and camera-module integration should happen in the assembly country, or at least outside China. For USMCA, the device must meet the product-specific rule of origin (tariff shift and/or regional value content) despite an Asian-made SoM and sensors. Get a customs-attorney opinion before relying on Mexico.

### 2.2 Effective US duty on the finished unit (assumed 9031.80.80)

| Assembly country | Stack | Effective rate |
|---|---|---|
| China | 1.7% MFN + 25% (List) + 12.5% (FL) | **≈ 39.2%** |
| Vietnam / Thailand | 1.7% + 12.5% | **≈ 14.2%** |
| Malaysia / Mexico (non-USMCA) / India | 1.7% + 10% | **≈ 11.7%** |
| Mexico, USMCA-qualifying | exempt | **≈ 0%** |
| Taiwan | combined cap 10% | **≈ 10%** |
| South Korea / Japan | combined cap 12.5% | **≈ 12.5%** |
| USA (final assembly) | none on the finished good. Imported components pay their own duty (Chinese PCBAs and modules at 25% + 12.5% + MFN). | component duty of about $40–80/unit [est.] |

### 2.3 Landed-cost build-up, Config A (Orin Nano), USD per unit

Assumptions [est.]:
- Scrap/attrition 3% / 2% / 1.5%.
- CM material markup 5% / 4% / 3.5%.
- Box-build, test, calibration and pack: 1.0–1.5 labor-hours. China about $30 / $18 / $15. Vietnam about $1 lower but +2.5–3% component-logistics cost. Taiwan about +$10 labor. Mexico +$7–10 labor and +4% logistics. US labor $55–70.
- Yield loss/rework 4% / 2% / 1.5%.
- Ocean freight, insurance, broker and MPF/HMF about $12/unit. Air is about $45–60/unit.
- Mexico trucking about $5.
- MPF is 0.3464% with a per-entry cap. HMF is 0.125% (ocean).

**5,000 units, by assembly location**

| | China | Vietnam | Thailand | Malaysia | Taiwan | Mexico (non-USMCA) | Mexico (USMCA) | USA |
|---|---|---|---|---|---|---|---|---|
| BOM | 771 | 771 | 771 | 771 | 771 | 771 | 771 | 771 |
| Scrap + CM markup + labor + yield | 80 | 100 | 104 | 104 | 107 | 118 | 118 | ~190–230 incl. component duty |
| **FOB / ex-works** | **851** | **871** | **875** | **875** | **878** | **889** | **889** | **~960–1,000** |
| US duty | 334 | 124 | 124 | 102 | 88 | 104 | 0 | (in FOB) |
| Freight / logistics | 12 | 12 | 12 | 12 | 12 | 5 | 5 | 2 |
| **Landed cost** | **≈ 1,197** | **≈ 1,007** | **≈ 1,011** | **≈ 989** | **≈ 978** | **≈ 998** | **≈ 894** | **≈ 960–1,000** |

**1,000 and 10,000 units (Config A)**

| Volume | China landed | Vietnam landed | Taiwan landed | Malaysia / Mexico non-USMCA |
|---|---|---|---|---|
| 1,000 (FOB China ≈ $1,040) | ≈ **$1,463** | ≈ **$1,230** | ≈ **$1,198** | ≈ **$1,205** |
| 5,000 | ≈ $1,197 | ≈ $1,007 | ≈ $978 | ≈ $990–1,000 |
| 10,000 (FOB China ≈ $765) | ≈ **$1,077** | ≈ **$905** | ≈ **$881** | ≈ **$895** |

**Config B (RK3588) at 5k:** FOB China ≈ $547, Vietnam ≈ $560, Taiwan ≈ $565. Landed: **China ≈ $773, Vietnam ≈ $652, Taiwan ≈ $634.**

Reading the numbers:
- At 1k units the CM labor and markup gap between countries is small, and **Taiwan or Vietnam beats China by about $230–265 per unit** on duty alone.
- A small US or Mexico pilot line (DVT/PVT and the first 1–2k units) is competitive with China once duty is counted. It also keeps calibration and quality issues close to the engineering team. The cost is higher labor and Asian component logistics.
- **Recommended path:** do DVT and PVT with a Taiwan-headquartered EMS running **Vietnam or Taiwan** lines. These are mid-size, camera-literate EMS providers. Alternatively, run a US/Mexico NPI line for the first 1–2k units and transfer to Vietnam or Malaysia for volume. Avoid final assembly in China for US-bound product. China remains fine for **EU/UK/rest-of-world** shipments if a second line exists, since the EU has no China-specific surcharge on this kind of device [est.: EU CN 9031.80 is generally 0% duty plus 19–25% import VAT; UK similar plus 20% VAT].

### 2.4 After landed cost: warranty, returns and unit economics

| Item | Assumption | Per unit (5k, Config A) |
|---|---|---|
| Warranty reserve (2-year consumer warranty) | **4–5% of net revenue in year 1** for a first-gen optical/battery product, falling toward 2–3% as field data comes in [est.: mature consumer electronics typically accrue about 1–3%] | ≈ $70–90 at $1,750 wholesale; ≈ $100–125 at $2,499 DTC |
| Returns (30-day trial, DTC) | 8–12% DTC return rate for a premium golf gadget where accuracy expectations are high [est.]. About $60–90 refurb, freight and repack cost per return. | ≈ $7–11 per unit sold |
| Payment, fulfillment, support | DTC: about 3% card fees plus $20–30 3PL and outbound shipping [est.] | ≈ $95–105 |

**Margin check at $2,499 MSRP (Vietnam, 5k):**

| | DTC | Dealer channel (wholesale ≈ 65–70% of MSRP → $1,625–1,750) |
|---|---|---|
| Config A (landed $1,007 + $100 warranty/returns) | GM ≈ 55% before marketing | GM ≈ **33–37%**, thin for a first product |
| Config B (landed $652 + $90) | GM ≈ 70% | GM ≈ **55–58%** |

Rule of thumb: keep **landed COGS at or below 30% of MSRP** for a consumer hardware brand that wants dealer distribution (PlayBetter, Rain or Shine, Carl's Place, Golf Galaxy). At $2,499 that means landed cost of about $750 or less, which points to Config B, a 10k-volume Config A, or a higher MSRP for a Jetson SKU.

---

## 3. NRE (non-recurring engineering) budget

These are external costs excluding salaries. All are [est.] unless a source is shown.

| Category | Low | High | Notes |
|---|---|---|---|
| **Industrial design** (concepts → CMF → final surfaces) | $60k | $250k | Shenzhen or independent studio at the low end. Top US/EU studios (Bresslergroup, Ammunition, Fuseproject, Frog, Teague, Whipsaw) about $150–500k for a full program. |
| **Mechanical engineering** (enclosure, sealing, optical bench, thermal, DFM, drop/IP) | $120k | $350k | Contract; or a 1-FTE ME plus a firm for peaks |
| **EE / carrier PCB design** (SoM carrier, MIPI CSI routing, PMIC, LED driver, USB-PD) | $80k | $220k | Contract design house, or about 1 FTE EE plus a layout contractor |
| **PCB spins** (4 spins: proto, EVT, DVT, PVT; 10–50 boards each, 8–10 layer, impedance controlled) | $40k | $120k | About $8–25k per spin for fab, assembly and parts, plus expedite fees |
| **Camera module / optics** (lens selection, filter spec, custom FPC, module house active-alignment NRE; optional custom lens) | $40k | $150k | Off-the-shelf M12 NIR lenses (Sunex, Evetar, Edmund) plus module-house NRE about $10–30k. Custom lens about $15–50k plus MOQ. Optical consultant about $20–80k. |
| **Injection-mold tooling**: 6–8 parts, plus the IR window tool with optical polish | $90k | $220k | Production P20 steel in China/Vietnam about $8–25k per part. US aluminum bridge tools about $5–15k per part. Benchmarks: aluminum $2–10k vs steel $10–100k+, P20 single cavity $6.5–14k, each side action +$1.2–3.5k, SPI-A2 optical polish +$1.8–4.2k ([Jaycon](https://www.jaycon.com/injection-moulding-price-a-2025-guide-for-engineers-procurement/), [xinyangmfg](https://xinyangmfg.com/low-volume-injection-molding-cost-hardware-startups/), [elitemoldtech](https://elitemoldtech.com/injection-mold-cost/), [Prototek](https://prototek.com/article/a-guide-to-aluminum-vs-steel-tooling-for-injection-molding/)). Budget +15–20% for T1→T3 tool modifications. Aluminum lasts about 10k–100k shots, P20 about 300–500k. |
| Die-cast / CNC chassis tooling, EVA case mold, packaging dies | $20k | $50k | |
| **Certification** (see the breakdown below) | $60k | $180k | |
| **Test fixtures and calibration rigs** (see §3.2) | $100k | $300k | |
| **Embedded Linux BSP / camera drivers** (contracted portion) | $50k | $200k | RidgeRun, D3 Embedded, e-con, Leopard Imaging, Antmicro, or Arrow/Avnet design services |
| **Reference equipment and test bay** (used GCQuad, used TrackMan, hitting bay, launcher, lab gear) | $60k | $180k | §4 |
| **Simulator integrations** (GSPro, E6 Connect, Awesome Golf, Creative Golf; Open Connect APIs) | $10k | $60k | Partner fees and revenue shares vary; GSPro's open API is low cost |
| Cloud, app infrastructure (pre-launch) | $15k | $50k | |
| Legal: patents (FTO search on camera launch monitors, which is a crowded patent space), trademarks, customs ruling | $60k | $200k | Freedom-to-operate on Foresight, TrackMan, Creatz and Rapsodo patents is essential |
| **Total NRE (excluding salaries)** | **≈ $0.8M** | **≈ $2.5M** | **Plan ≈ $1.2–1.5M** |

### 3.1 Certification breakdown

| Mark / test | Est. cost | Notes |
|---|---|---|
| FCC Part 15B (unintentional), with a pre-certified Wi-Fi module | $3–8k | $800–2k for simple products, $3–8k for typical ones ([MarkReady](https://markready.io/learn/fcc-certification-cost), [Promise Legal](https://blog.promise.legal/fcc-certification-ce-marking-connected-devices-hardware-startups/)) |
| FCC Part 15C/15.255 (60 GHz) or 15.249 (24 GHz) for a chip-down radar | $8–25k | Full intentional-radiator certification. RF testing $3–8k, TCB $1–3k ([MarkReady](https://markready.io/learn/fcc-certification-cost)). Avoid this by using a pre-certified radar module. |
| ISED (Canada) | $3–6k | Usually run alongside FCC |
| CE RED including **EN 18031 cybersecurity** (mandatory since 1 Aug 2025) | $8–20k | RED lab testing alone is about $1.5–3k+ ([AESTECHNO](https://www.aestechno.com/en/ce-red-certification-iot/), [ecocomply](https://ecocomply.ai/blog/what-does-ce-marking-cost-for-your-product)). EN 18031 adds documentation and pen-test effort. |
| UKCA, RCM (AU/NZ), MIC/TELEC (Japan), KC (Korea) | $10–35k | Market by market |
| IEC 62368-1 product safety (CB scheme) | $10–25k | Needed by retailers and for the CB report |
| **IEC 62471 photobiological safety (IR LEDs)** | $5–15k | **Critical:** high-power pulsed 850 nm arrays near eye level. Design to "Exempt" or "Risk Group 1". |
| IEC 60825-1 (if the alignment laser is used) | $3–8k | Class 2 at most. Or drop the laser and use camera-based alignment. |
| UN38.3 + IEC 62133-2 battery | $10–20k | The pack supplier often holds these. Requalification needed if cells change. |
| Pre-scans, debug sessions, re-tests | $10–30k | First-time teams almost always need at least one re-test |
| **Total** | **$60–180k** | |

### 3.2 Factory camera calibration at scale

Every unit's stereo pair needs individual intrinsic calibration (focal length, principal point, distortion), extrinsic calibration (the rotation/translation between cameras, plus the radar and alignment axis), and photometric/strobe timing calibration. At volume this is done as follows. The approach is the standard one used for depth cameras (Intel RealSense, Luxonis OAK) and smartphone multi-camera modules; this report did not find a 2026 source describing it.

1. **Do it at two levels.**
   - **Module level (at the camera module house):** active alignment and focus, plus a lens-shading and focus MTF check (Imatest or similar charts). Module houses do this as standard. Their NRE is about $10–30k.
   - **System level (at your EMS):** after the cameras are fixed to the aluminum optical bench and the unit is closed, place the unit in a **calibration station**. The station is a rigid frame with the DUT on a kinematic mount (or a 2-axis motorized gimbal/turntable). It uses several **backlit IR-emitting ChArUco/dot-grid targets** at different depths and angles, or a single target moved by a small robot or linear stage, so the cameras see the target at about 10–20 poses. Capture takes about 30–90 s and the solve 10–30 s. Results are written to a secure partition on the device and to the cloud, keyed by serial number.
2. **Station cost: about $25–80k each** (frame, targets, lighting, gimbal/robot, PC, software, MSA/gauge R&R). Throughput is about 30–60 units per hour with parallel fixtures. 10k units a year is about 40 units a day, so **one station on one shift** is enough, with a second as backup.
3. **Verification ("shot test") station.** A ball launcher or a ball rolled or dropped through **laser light gates of known spacing** checks speed and launch angle against tolerances. A marked ball with known spin from a spin-wheel launcher checks spin sign and magnitude. This catches calibration that passed numerically but is wrong in practice. Cost about $15–40k.
4. **Thermal stability.** Calibrate at a controlled temperature, then verify a hot-soaked unit at about 40 °C to catch bench or lens drift. Plan on-device **self-check** routines too, such as checking the reprojection error of epipolar features on a calibration mat included in the box.
5. **Other EOL fixtures:** carrier-PCBA bed-of-nails/functional test ($8–25k), camera-module test ($5–15k), IR LED radiometric output and eye-safety limit check ($5–15k), RF/Wi-Fi conducted test ($5–15k), battery/charging test, burn-in racks ($5–15k), cosmetic inspection. **Fixture total ≈ $100–300k** including software and the second-source duplicates.
6. **Who builds them.** EMS providers build PCBA testers. Calibration stations are usually built by the device company plus an automation integrator. Vendors include Optofidelity, Imatest (charts and software), and test-equipment integrators near the EMS. Own the calibration software and data yourself; it is core IP.

---

## 4. Prototype path for a software team

### 4.1 Phase-0 works-like rig (weeks 0–12), about $25–45k in hardware

| Item | Choice | Cost |
|---|---|---|
| Compute | **NVIDIA Jetson Orin Nano Super Developer Kit** (×2–3; has 2 MIPI CSI connectors) | $399 each since July 2026 ([CNX](https://www.cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101/)) |
| Cameras | IMX296 mono GS with external trigger: **InnoMaker CAM-IMX296RAW** ($69, $45 at 120+), **Arducam B0619 mono M12** ($64.99), Raspberry Pi GS Camera ($50). For better FPS/resolution: **Vision Components IMX296** ($134.70), Leopard LI-IMX296-MIPI-M12 ($279). USB alternatives: e-con See3CAM_24CUG AR0234 GS ($99). | [InnoMaker](https://www.inno-maker.com/product/cam-mipi296raw-trigger/), [Arducam](https://www.arducam.com/1-58mp-imx296-mono-global-shutter-camera-module-with-m12-lens-for-raspberry-pi.html), [Mouser VC](https://www.mouser.com/new/vision-components/vision-components-imx296-imx296-c-modules/), [Leopard](https://leopardimaging.com/product-tag/imx296/), [e-con](https://www.e-consystems.com/webstore.asp) |
| More than 2 cameras on one Jetson | Third-party carrier (Seeed reComputer, Auvidea) or a GMSL deserializer board, or an Arducam multi-camera adapter | about $200–800 [est.] |
| Higher-speed sensor evaluation | IMX273/IMX287/IMX568 board-level cameras from FRAMOS, VC or Lucid to test whether a faster sensor is needed for spin | about $200–600 each [est.] |
| Lenses / filters | M12 NIR lens kit (several focal lengths) + 850 nm bandpass filters | about $500–1,500 |
| IR illumination | OSRAM Oslon Black 850 nm boards + a bench pulse driver (EPC GaN eval board), strobed from a Jetson GPIO or an MCU | about $500–2,000 |
| Radar (optional) | TI IWR6843AOP EVM or Infineon BGT60TR13C demo kit; a 24 GHz Doppler module for ball/club speed triggers | about $200–600 [est.] |
| Enclosure | Bambu X1C / Prusa (FDM) + Formlabs (SLA) in-house 3D printing; MJF/SLS parts from a service | about $5–10k |
| Lab gear | Oscilloscope, bench supplies, logic analyzer, USB-PD analyzer, thermal camera, IR power meter | about $10–20k |

**Tip:** IMX296 at full resolution runs about 60 fps. Spin measurement comes from **multi-exposure strobing within a single frame**, or very short ROI bursts, with the IR LEDs pulsed at microsecond widths. Validate strobe-plus-sensor timing first. It is the riskiest hardware-software interface in the product.

### 4.2 Ground truth and labelling

| Option | Cost | Use |
|---|---|---|
| **Used Foresight GCQuad** | about **$8.5–12.5k**. Club data adds about $4k. A $1,000 transfer fee may apply. Foresight sells recertified units with a 1-year warranty. | **Primary reference.** It is camera-based and side-of-ball, so its spin and club data methods match ours ([friendlygolfer](https://friendlygolfer.com/used-gcquad/), [SidelineSwap](https://sidelineswap.com/gear/golf/training-technology/launch-monitors/8049132-foresight-used-gcquad)) |
| New QuadMAX | about $19,999 | If club data and warranty matter ([friendlygolfer](https://friendlygolfer.com/used-gcquad/)) |
| **Used TrackMan 4** | about **$14–17.5k** + $1,000 transfer + $1,100/yr TPS subscription | **Outdoor flight / carry reference** and a second opinion on spin ([best-golf-simulator](https://best-golf-simulator.com/trackman-cost/), [eBay](https://www.ebay.com/itm/198526735428)) |
| Rental / time on a fitter's bay | about $100–250/hr [est.] | Spot-checks before buying |
| **Golf Laboratories robot** | Purchase price is not published; contact them for a quote. Six figures is likely. Golf Labs also sells testing services and has supplied all major OEMs, the USGA and R&A ([Golf Labs](https://www.golflabs.com/robotics-information)). Swing speed 5–130 mph and programmable shot shapes. The RoboGolfPro instructional robot was about $150k (2014–2018 pricing) ([CNBC 2016](https://www.cnbc.com/2016/04/05/short-of-giving-you-a-green-jacket-this-robot-will-up-your-golf-game.html)). | Rent **testing days** for repeatability and edge-case sweeps (e.g., spin axis ±20°) during the DVT accuracy validation. Do not buy one. |
| DIY ball launcher (pneumatic barrel + counter-rotating spin wheels, chronograph gates) | about $5–25k [est.] | Repeatable ball-only tests (speed, launch, backspin, sidespin) without a human. Also the basis for the factory shot-test station. |
| High-speed reference camera + marked balls | about $5–15k [est.] | Independent spin labels (count marker rotation across frames) |
| Human data | Local golfers paid per session, plus a golf pro or fitter on retainer | Diverse swings, clubs, ball brands, and lefties. **Most of the long tail lives here.** |

**Labelling pipeline.** Hit every shot in a bay with the GCQuad (and TrackMan) running side by side with our rig. Time-sync shots by impact timestamp (an audio microphone spike works well). Store raw frames, reference outputs and metadata (club, ball type, lighting, temperature). Target **≥50k labelled shots by EVT and ≥200k by DVT** [est.], including outdoor sessions at different sun angles.

### 4.3 Accuracy gates (proposed)

Compare against the reference unit over a **pre-registered test matrix**: driver, 7-iron, wedge, chip, putt; lefty/righty; indoor and outdoor; low, mid and high sun; white, colored and matte balls.

| Gate | When | Example targets (vs GCQuad, mean abs error / 95th percentile) |
|---|---|---|
| G0: feasibility | End of Phase 0 | Ball speed ≤1 mph, VLA ≤0.5°, HLA ≤0.5° indoors on 2–3 clubs. Spin measured on ≥90% of shots. |
| G1: integrated proto | End of Phase 1 | Above, plus total spin ≤250 rpm (iron) / ≤300 rpm (driver), spin axis ≤2°, carry ≤3 yd (7-iron). Outdoor in direct sun at ≥85% capture rate. |
| G2: EVT exit | | All clubs, 98% capture rate, club path/face ≤1°, thermal soak at 40 °C, battery-powered |
| G3: DVT exit / beta | | Production-tooled units; unit-to-unit spread (calibration MSA); 100–200 beta users; independent reviewer tests |

---

## 5. Team plan

### 5.1 Core roles

Salaries are US 2026 base, [est.]. Use a fully loaded multiplier of about 1.25–1.4x for benefits, payroll tax and equipment.

| Role | FT vs contract | When | US base salary [est.] | Notes |
|---|---|---|---|---|
| **CV/ML lead** (ball tracking, spin from multi-exposure, club data, stereo) | **FT, founder-level** | Day 0 | $190–270k + equity | Core IP. Hire 2 by EVT. |
| **Embedded Linux / camera-pipeline engineer** (V4L2/Argus, MIPI, triggers, ISP bypass, Yocto/L4T, OTA) | **FT** | Month 0–2 | $170–230k | Supplement with RidgeRun, D3, e-con or Leopard driver contracts at about $150–250/hr [est.] |
| **Hardware / electrical engineer** (carrier, power, LED driver, EMC) | **FT** by Phase 1, contract before that | Month 2–4 | $160–220k | The founding team's biggest gap. Hire someone who has shipped a SoM-based consumer product. |
| **Mechanical engineer** (optical bench, thermal, DFM, tooling) | **FT** at EVT, plus an ID/ME firm | Month 4–6 | $150–200k | Owns tooling, the EMS relationship and drop/thermal testing |
| **Optical engineer** | **Contract** | Phase 0–1 | $150–250/hr [est.] | Lens/filter/window specs, stray light, illumination uniformity, IEC 62471 design |
| **RF/radar DSP engineer** (if radar is used) | **Contract**, unless radar becomes core to outdoor flight | Phase 1 | $150–250/hr [est.] | Use pre-certified modules and vendor SDKs to minimize this |
| **NPI / operations / supply-chain lead** | **FT** | Before EVT (month 8–10) | $160–210k | Runs the EMS, sourcing, NCNR long-lead buys, logistics, customs rulings. The most underrated hire for software-first teams. |
| **Test / manufacturing-test engineer** | **FT** | EVT | $130–175k | Owns calibration station software, fixtures and yield analytics |
| **iOS/iPadOS + Windows app engineers** | FT (2) | Phase 1 | $160–220k | Simulator API (GSPro/E6/Awesome Golf), practice range, data sync |
| **Backend / cloud engineer** | FT (1) | Phase 1 | $160–210k | Accounts, shot storage, OTA, calibration database |
| **QA (app + device)** | FT/contract | DVT | $110–150k | Beta management |
| **Golf domain pro / club fitter** | **Part-time retainer** | Day 0 | about $50–100/hr or $3–6k/month [est.] | Test-matrix design, swing diversity, credibility with dealers and fitters |
| **Product/marketing, community, customer support** | FT from DVT | DVT | $120–180k | Pre-orders, reviewers, dealer program |
| Offshore contract support (India / Eastern Europe embedded, test automation) | Contract | As needed | about $40–90/hr [est.] | |

Headcount ramp: about **6 FTE** in Q4 2026, **10–12 by EVT** (Q3 2027), **14–16 by launch**.

### 5.2 Design firms, camera specialists, ODMs

**US/EU product-development firms** (end-to-end ID, ME and EE; quote $0.5–2M+ for a full program):
- **Bresslergroup** (Philadelphia): ID, ME, EE.
- **Synapse** (Seattle; part of Capgemini Invent) and **Cambridge Consultants** (UK; Capgemini). Both strong on complex electro-optics. Expensive.
- **Simplexity** (San Diego): ME/EE, strong on consumer devices.
- Studios such as Ammunition, Fuseproject, Frog, Teague, Whipsaw for ID only.
- *Note: **Altia** is an embedded GUI/HMI software company, not a hardware design firm. It is not relevant here.*

**Camera and embedded-vision specialists** (better value for our core risk):
- **e-con Systems** (India/US): custom camera modules and Jetson carrier design; ODM-like services.
- **Leopard Imaging** (US/China): Jetson camera modules and custom modules.
- **D3 Embedded** (US): Jetson camera system design and drivers.
- **RidgeRun** (Costa Rica/US): Jetson drivers and GStreamer.
- **Antmicro** (Poland): open Jetson carriers and camera pipelines.
- **FRAMOS** (Germany) and **Vision Components** (Germany): Sony Pregius sensor modules ([FRAMOS](https://framos.com/products/modules/framos-sensor-modules/fsm-imx296-sensor-module-26347/)).
- **Arducam / UCTRONICS** (China): low-cost custom modules.
- Lens makers **Sunex** and **Evetar**.

**EMS / ODM candidates** [est.: shortlist to qualify, not vetted]:
- Taiwan-headquartered mid-size EMS with Vietnam/Thailand plants (camera and networking ODMs).
- US NPI-friendly EMS for the pilot run.
- Arrow/Avnet design and supply-chain services for SoM procurement and long-lead buys.

**Companies that already build launch monitors** (possible partners, white-label or acquirers; all designers, not open ODMs):

| Company | Country | Notes | Source |
|---|---|---|---|
| **Creatz** (owns **Uneekor**, QED Golf) | Korea | Designs high-speed cameras and sensors in-house and says it manufactures every part itself. 2025 revenue ₩104.2bn, 24% operating margin, 79.9% exports. KOSDAQ IPO in October 2026. Opening a Texas R&D center. Raised about $21.1M VC (Otium Capital, UTC Investment). | [IB Tomato](https://www.newstomato.com/ReadNews.aspx?no=1312861), [nextunicorn](https://www.nextunicorn.kr/company/edc322701fe58dc9), [Tracxn](https://tracxn.com/d/companies/creatz/__O270cIo1IT1SA6ervRXZUBCJs_nMa6FZ5kkKq3I4grU) |
| **Invant** (Square Golf; ExPutt) | Korea | Camera-based Square Golf launch monitor; develops, manufactures and sells in-house | [Golf Business News](https://golfbusinessnews.com/news/new-products/square-golf-launch-monitor-comes-to-market/), [Invant](https://invant.co/sample-page/) |
| **Golfzon**, **Voice Caddie (VC Inc.)**, Kakao VX | Korea | Screen golf and radar/camera launch monitors. Worth contacting for OEM or white-label. | [fnnews (Voice Caddie)](https://www.fnnews.com/news/202104140905313675) |
| **Pixel Field / NeoPace** | Singapore | AI vision hardware; more than 1M devices shipped; 3-camera + 24 GHz radar G10 Pro | [PR Newswire](https://www.prnewswire.com/news-releases/neopace-g10-pro-ai-powered-3d-replay-golf-launch-monitor-now-crowdfunding-on-kickstarter-302881801.html) |
| **Rapsodo** | Singapore/US | MLM2PRO. SGD 50–100M revenue in 2024. | [Tracxn](https://tracxn.com/d/legal-entities/singapore/rapsodo-pte.ltd./__s11iL9jQojQrzJ26El9GzLA-HCQezvD8s_wDkG6hZ5o) |
| Alibaba "launch monitor OEM" listings | China | **Caution:** some listings sell "TrackMan 4" units for about $800–900, which looks like counterfeits or scams ([Alibaba search summary](https://yb-golf.en.alibaba.com/productgrouplist-817973151/OEM_ODM.html)). Not a credible partner path. | |

A licensing or white-label deal with a Korean incumbent (hardware from them, our software and brand) is a viable **plan B** if our accuracy gates slip. It would also be a cheaper way to reach the market. Expect them to protect their own Uneekor/Square brands.

---

## 6. Timeline

### 6.1 Phase plan (starting October 2026)

| Phase | Dates (plan) | Duration | Builds / units | Key outputs | Gate |
|---|---|---|---|---|---|
| **0: Feasibility (works-like)** | Oct 2026 – Jan 2027 | 3–4 mo | 2–3 dev-kit rigs | Hitting bay, GCQuad ground truth, strobe+GS timing, ball tracking/spin v0, compute benchmark (Jetson vs RK3588). **Visit the PGA Show (Orlando, late January 2027)** to meet sim partners, dealers and Korean incumbents. | G0 |
| **1: Integrated proto (alpha)** | Feb – Jul 2027 | 5–6 mo | 10–25 units, carrier v1/v2, 3D-printed and CNC enclosures | ID concept frozen; compute decision; outdoor sunlight testing; ID/ME firm engaged; EMS RFQ and selection; customs ruling filed | G1 |
| **EVT** | Aug – Nov 2027 | 3–4 mo (+1–3 slip) | 50–150 units on production-intent design; aluminum or first steel T1 parts | Pre-compliance scans, IEC 62471 pre-test, calibration station v1, drop/thermal | G2 |
| **DVT** | Dec 2027 – Apr 2028 | 4–5 mo (+2–3 slip) | 300–500 units from hard tools on the EMS line | Formal certification, reliability (drop, vibe, thermal cycling, battery), **beta program (100–200 users)**, independent reviewer units. **Open pre-orders / crowdfunding (about Mar–Apr 2028).** | G3 |
| **PVT** | May – Jul 2028 | 2–3 mo (+1–2 slip) | 1,000–2,000 sellable units at line rate | Line yield, calibration throughput, packaging and drop testing, FAI | Ship decision |
| **MP ramp** | Aug 2028 → | | | First ocean shipments by early September to land for Q4 | |
| **Launch (stretch)** | **Holiday Q4 2028** | | | Fulfil pre-orders, DTC and first dealers | |
| **Launch (realistic, 4–6 mo slip)** | **PGA Show January 2029 → spring 2029** | | | Dealer launch at the show, spring buying season | |

Instrumental's handbook gives typical build sizes of EVT 100–1,000, DVT 300–2,000 and PVT 1K–20K. It also warns that timing is set by how many iterations are needed rather than by the calendar, that up to about 40% of EVT units can fail, and that "fake DVTs" should be called EVT2 ([Instrumental](https://instrumental.com/build-better-handbook/evt-dvt-pvt)). For a first-time team the realistic plan includes an **EVT2**. Budget for it rather than hoping to avoid it.

### 6.2 Seasonality and launch timing

- **Q4 holiday** (Black Friday through December) is the biggest DTC window for launch monitors at our price point. It is also when **northern-hemisphere golfers build indoor simulators** for winter (September–December buying) [est., consistent with industry practice].
- **The PGA Merchandise Show (late January, Orlando)** is where launch monitors are announced and dealers commit. Creatz/Uneekor and Square both launch products there ([Seoul Economic Daily on Creatz at PGA Show](https://www.sedaily.com/article/14018148)).
- **Spring (March–May)** is the second peak, for outdoor and range use.
- **Do not launch in summer.** It is low indoor-sim demand and gives dealers no time to stock before the holiday.
- Plan logistics backwards: holiday stock must be **landed in a US 3PL by about mid-October**. That means ocean departure by about early-to-mid September and **PVT complete by about August**.

### 6.3 Where first-time teams typically slip (and the buffer used above)

1. Camera, strobe and trigger timing, and driver bugs (Phase 0–1): 1–3 months.
2. Thermal: fan noise and throttling in sun (EVT): 1–2 months.
3. Tooling T1→T3 iterations, IR window optical defects (EVT→DVT): 1–2 months.
4. Certification re-tests, especially EMC from MIPI/LED pulse currents, and EN 18031 (DVT): 1–2 months.
5. Calibration yield and unit-to-unit spread (DVT→PVT): 1–2 months.
6. Long-lead parts: SoM lead time is 12 weeks ([Arrow](https://www.arrow.com/en/products/900-13767-0030-000/nvidia.html)), sensors and lenses are 12–26 weeks [est.], and memory allocation in 2026 is a risk.

---

## 7. Funding plan

### 7.1 Capital needed to launch (24 months, Oct 2026 → Q4 2028 / Q1 2029) [est.]

| Bucket | Amount |
|---|---|
| Payroll: average about 10–11 FTE × about $260k loaded × 2 years | $5.2–5.8M |
| Contractors (ID/ME firm, optics, drivers, regulatory consultants) | $0.6–1.0M |
| NRE hard costs (tooling, fixtures, certification, PCB spins, prototypes) | $0.8–1.3M |
| Reference equipment, test bay, robot testing days, data-collection programs | $0.15–0.35M |
| EVT/DVT/beta units (about 600 units at about $1,000–1,500 each, including air freight) | $0.6–0.9M |
| **First production inventory** (3,000 units × about $1,000 landed, Config A; about $650 for Config B) | $2.0–3.0M (**partly financed**) |
| Pre-launch go-to-market (PGA Show booth, reviewers and influencers, website, support tooling) | $0.5–1.0M |
| Legal, IP, insurance (product liability), G&A | $0.4–0.6M |
| Contingency (20%) | $2.0–2.8M |
| **Total to launch** | **≈ $12–17M**, of which $2–3M is inventory that can be partly financed |

### 7.2 Recommended rounds

| Round | Size | Timing | Milestone it buys |
|---|---|---|---|
| **Pre-seed / seed** | **$4–6M** | Q4 2026 – Q1 2027 | Phase 0 → EVT; G0–G2 accuracy gates; EMS selected; IP filed. 18 months of runway. |
| **Series A** (or a large seed extension) | **$10–15M** | About Q2 2028 at DVT, with beta data, independent accuracy results and pre-order traction | PVT, MP inventory, launch GTM, support, Gen-2 R&D |
| Non-dilutive working capital | $1–4M | From DVT | See §7.3 |

### 7.3 Funding sources

- **Golf/sports-tech VCs and investors with category exposure:**
  - **Stadia Ventures** (Rapsodo investor) ([Tracxn](https://tracxn.com/d/companies/rapsodo/__TTRfsH_WzAugUrrRL6M96HdirlIUhbdPgio9JlA85O0/funding-and-investors)).
  - **Phoenix Venture Partners**, **Vertex Ventures**, **Wavemaker**, **SEEDS Capital** (Rapsodo backers; the latter group is from a lower-quality profile site and unverified) ([Tracxn](https://tracxn.com/d/companies/rapsodo/__TTRfsH_WzAugUrrRL6M96HdirlIUhbdPgio9JlA85O0)).
  - **Bruin Capital**, **North Castle Partners** (Full Swing owners) ([CNBC](https://www.cnbc.com/2026/07/06/versant-to-buy-golf-simulator-company-full-swing.html)).
  - **Otium Capital** and **UTC Investment** (Creatz) ([Tracxn/Creatz](https://tracxn.com/d/companies/creatz/__O270cIo1IT1SA6ervRXZUBCJs_nMa6FZ5kkKq3I4grU)).
  - Generalist sports-tech funds [candidates to verify]: Elysian Park, Will Ventures, Courtside, Sapphire Sport.
  - Athlete angels: Full Swing's cap table included Tiger Woods, Spieth, Schauffele, Rahm, D. Johnson, Mahomes, Josh Allen and Steph Curry ([SGB](https://sgbonline.com/versant-media-group-acquires-golf-simulator-platform-full-swing/)). Tour players and celebrity angels are an established route in golf tech.
- **Strategics:**
  - **Versant** (Golf Channel, GolfNow, GolfPass, now Full Swing): an active acquirer that paid $530M ([CNBC](https://www.cnbc.com/2026/07/06/versant-to-buy-golf-simulator-company-full-swing.html)).
  - Topgolf (held a Full Swing stake).
  - Golf OEMs: Acushnet, TaylorMade, Callaway, PXG. Fitting data and ball/club testing are their interest.
  - Golfzon; Garmin; simulator software firms.
  - **Creatz** has set aside ₩7.7bn of IPO proceeds for investment or M&A in simulation software and data analytics ([IB Tomato](https://www.newstomato.com/ReadNews.aspx?no=1312861)). It is a plausible partner or acquirer for a software-strong team.
  - Strategics bring channel and credibility but can limit exits. Prefer commercial agreements, or small minority stakes with no ROFR.
- **Crowdfunding / pre-orders.** Use it for **validation and working capital, not as core funding.**
  - Benchmarks: NeoPace G10 Pro raised about $444.5k from 476 backers (about $934 average) in the opening days of its 2026 campaign. Shotlyt raised $57k from 212 backers in 2025. Phigolf 2 raised $242.6k from 996 backers in 2022 ([gizmocrowd](https://www.gizmocrowd.com/post/neopace-g10-pro-review), [Kicktraq](https://www.kicktraq.com/projects/258587540/shotlyt-train-smarter-with-a-compact-golf-launch-monitor/), [Kickstarter](https://www.kickstarter.com/projects/phigolf/phigolf-2-mini-golf-simulator-3-apps-multi-os-support)).
  - At $1,499–2,499 founder pricing, plan on **$0.5–2M from 300–1,000 backers**.
  - Kickstarter's Design & Technology category had its biggest year ever in 2025, and the platform added Pledge Manager and "Pledge Over Time" ([Kickstarter 2025 review](https://updates.kickstarter.com/a-year-in-review-2025-kickstarter-highlights/)).
  - Fees are about 5% platform plus about 3–5% payment processing [est.].
  - **Launch the campaign at DVT, not before.** Academic work (Mollick) found most Kickstarter technology projects deliver late [est.: not re-verified this session]. Late delivery is a brand killer in golf forums such as GolfWRX and Golf Simulator Forum.
  - A refundable-deposit pre-order on our own Shopify store, plus reviewer units, is the alternative.
- **Inventory / PO financing.** Kickfurther (consumer-brand inventory consignment), PO financing, and EMS payment terms (negotiate 30% deposit and 70% at shipment, moving to net-30 once established).
- **Revenue-based financing** (Wayflyer, Clearco, Shopify Capital) once there is DTC revenue history. Not available pre-launch.
- **Venture debt** after the Series A, sized at 20–30% of the equity raised.
- **Comparables and exits:**

| Company | Data point | Source |
|---|---|---|
| Full Swing | Bruin bought control for about $160M in 2021; Versant agreed to buy for **$530M** (July 2026, closed about 3 Aug 2026) | [CNBC](https://www.cnbc.com/2026/07/06/versant-to-buy-golf-simulator-company-full-swing.html), [PitchBook](https://pitchbook.com/profiles/company/114522-40) |
| Creatz / Uneekor | 2025 revenue ₩104.2bn (+26%), operating profit ₩25.1bn; KOSDAQ IPO October 2026; earlier SPAC valuation of about ₩450bn failed in 2024; about $21.1M VC raised | [IB Tomato](https://www.newstomato.com/ReadNews.aspx?no=1312861), [NEWSTOP](https://www.globalnewstop.com/news/articleView.html?idxno=2685) |
| Uneekor | Bought 70% of Evnroll for about $15.2M (2023); 50% YoY North America growth; entered UK/EU in 2026 | [Tracxn/Uneekor](https://tracxn.com/d/companies/uneekor/__1Z_yGTZZxe1do-nSg4gYPWC0url4hbdxSod-U8qs-pg), [SGI Europe](https://www.sgieurope.com/people/uneekor-launches-in-uk-and-europe-with-new-sales-team/121476.article) |
| Rapsodo | Seed 2015; Series A 2019 (Stadia); SGD 50–100M revenue 2024 | [PitchBook](https://pitchbook.com/profiles/company/62201-80), [Tracxn](https://tracxn.com/d/legal-entities/singapore/rapsodo-pte.ltd./__s11iL9jQojQrzJ26El9GzLA-HCQezvD8s_wDkG6hZ5o) |

---

## 8. Competitive price context (for the BOM and margin targets)

| Product | Tech | Price | Source |
|---|---|---|---|
| NeoPace G10 Pro | 3 cameras + 24 GHz radar | $899 KS / $1,499 MSRP, ships November 2026 | [PR Newswire](https://www.prnewswire.com/news-releases/neopace-g10-pro-ai-powered-3d-replay-golf-launch-monitor-now-crowdfunding-on-kickstarter-302881801.html) |
| Square Golf (HE / Omni) | Camera | about $599–1,500 [est.] | [PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/square-omni-indoor-outdoor-launch-monitor-review) |
| Uneekor EYE MINI / LITE / CORE | Camera | about $1,500–3,000 [est.] | [Uneekor](https://uneekor.com/en-us/products/eye-mini-standalone) |
| Foresight GCQuad / QuadMAX | Quad camera | $15,999–18,649 / $19,999 | [friendlygolfer](https://friendlygolfer.com/used-gcquad/) |
| TrackMan 4 / iO | Radar / indoor camera-radar | $21,495–24,950 / from $13,995 | [best-golf-simulator](https://best-golf-simulator.com/trackman-cost/) |

The $1,999–2,999 band is contested from below (Square, NeoPace, Rapsodo) and above (Uneekor, Bushnell/Foresight, SkyTrak). The product has to **demonstrably match a GCQuad on spin and club data, outdoors**, which is the gap most sub-$2k camera units leave open.

---

## 9. Key risks and mitigations

| # | Risk | Concrete failure scenario | Mitigation | Owner / gate |
|---|---|---|---|---|
| 1 | **Markerless spin accuracy not good enough** | Driver spin error of 600+ rpm on shiny or logo-free balls and low-spin drives, so carry is wrong by 10+ yards. Reviewers call it "unreliable" and returns go above 15%. | Kill or proceed on accuracy at G0/G1 against the GCQuad. Use multi-exposure IR strobes for many ball images per shot, and ensure enough resolution on the ball (pixels per mm) and baseline. Combine optical-flow and dimple-texture spin estimation with learned models trained on more than 200k labelled shots. Offer an optional "marked ball" mode (as several incumbents do). Use radar to cross-check speed. | CV lead; G0–G2 |
| 2 | **Sunlight / outdoor** | Direct sun saturates the 850 nm band. Shadows and turf glare break segmentation. Capture rate falls to about 70% at noon. | Narrow bandpass filters (or 940 nm, where the solar spectrum has an absorption dip); very short exposures synchronized with high-peak LED pulses so the LEDs overpower ambient light over microseconds; HDR/background subtraction; a lens hood; outdoor test matrix by sun angle from Phase 1. Radar helps outdoors. | CV + optical; G1 |
| 3 | **Thermal throttling** | An Orin at 15–25 W in a sealed box in 35 °C sun throttles after 20 minutes. Latency rises and shots are dropped. | Thermal design is decided at Phase 1, not EVT. Blower plus heatsink sized for 40 °C ambient in sun; light-colored housing; a low-power idle state with radar or low-fps wake; a measured power budget. RK3588 runs about 8–12 W. Thermal soak test at every build. | ME + EE; G2 |
| 4 | **Compute/DRAM supply and price** | NVIDIA raises prices again (as in July 2026, up to +101%), or allocates modules to industrial customers. BOM rises by $50–100 overnight. | Portable vision stack (ONNX, no CUDA-only kernels); dual-qualify Jetson and RK3588 or QCS6490 carriers; NCNR buffer buys at DVT; supplier long-term-supply letters (Radxa commits to 2032). | CTO + Ops |
| 5 | **Tariff changes** | The excess-capacity Section 301 action adds tariffs to Vietnam or Mexico. The CIT strikes down or reshapes the forced-labor duty. A China-origin determination because the PCBA came from China. | Avoid China final assembly for the US; do PCBA in the same country; binding CBP classification ruling; build the cost model with a ±15% tariff scenario; keep a second-region option (Taiwan/Malaysia/Mexico) at the EMS. Keep **battery under 100 Wh**. | Ops + customs counsel |
| 6 | **Certification failure** | Radiated emissions fail from fast MIPI edges and multi-amp LED pulse currents. IEC 62471 classifies the illuminator as RG2 (labelling and retail problems). EN 18031 blocks EU launch. | Pre-compliance scans at EVT; LED current loops kept tight and shielded; spread-spectrum clocks; pre-certified Wi-Fi and radar modules; design the illuminator for RG0/RG1 from Phase 1 with an optical consultant; plan the EN 18031 security architecture (secure boot, signed OTA, no default passwords) early. | EE + optical |
| 7 | **Calibration drift / unit-to-unit variance** | The stereo baseline shifts after a drop or temperature cycling, so a customer unit reads 3 mph high. | Rigid aluminum optical bench; adhesive and screw design validated by drop and thermal cycling; factory calibration plus verification shot test; on-device self-check; recalibration service flow. | ME + test |
| 8 | **Supply chain / long-lead parts** | Sensor EOL or allocation (Sony Pregius lead times); an SoM lead time of 12+ weeks delays PVT. | Choose sensors with a long Sony lifecycle and a second source (onsemi/OmniVision fallback footprint); last-time-buy clauses; distributor agreements via Arrow/Avnet. | Ops |
| 9 | **Returns and warranty** | A 2-year warranty on Li-ion and moving fans, plus 30-day accuracy-dissatisfaction returns, push warranty and returns cost above 8% of revenue. | 100–200 user beta at DVT; set honest accuracy claims; set up in-app tools for alignment and setup (most "accuracy" complaints are setup issues); reserve 4–5% for warranty in year 1; quality-grade cells (Samsung/LG/Molicel); fan life rated for 20k+ hours. | Product + Ops |
| 10 | **Schedule slip misses the season** | DVT slips 3 months, so holiday 2028 is missed and inventory lands in January. | Plan around the PGA Show January 2029 as the realistic launch; run the crowdfunding/pre-order campaign only at DVT; keep holiday 2028 as a stretch with a limited "Founders Edition" run. | CEO |
| 11 | **IP / patents** | Patents held by incumbents (Foresight, TrackMan, Creatz, Rapsodo) on camera-based spin and club measurement lead to a demand letter at launch. | FTO study in Phase 1 ($30–80k [est.]); design-around; file our own patents; IP insurance. | Counsel |
| 12 | **Funding gap between DVT and MP** | Inventory cash is needed before revenue: a 30% deposit on 3,000 units is about $900k. | Raise the Series A at DVT; pre-orders; inventory/PO financing; negotiate EMS terms; smaller first build (1,500 units) with fast reorders. | CEO/CFO |

---

## 10. Next actions (first 90 days)

1. Buy 2–3 Orin Nano Super dev kits, IMX296 trigger-capable cameras, IR LED and pulse-driver eval boards, and a **used GCQuad**. Build the hitting bay.
2. Run the **compute benchmark** (Jetson vs RK3588) on the actual ball-tracking pipeline before committing to a carrier design.
3. **Get quotes on the [est.] lines**:
   - Custom IMX296/IMX273 module pricing at 5k/10k (e-con, Leopard, Arducam, FRAMOS).
   - RK3588 SOM volume quotes (Radxa, Firefly, Geniatech).
   - Oslon IR LEDs at volume.
   - 72 Wh pack from 2 pack houses.
   - Enclosure tooling from 3 shops.
   - EMS labor rates in Taiwan, Vietnam and Mexico.
4. Engage a customs broker/attorney: HTS classification (9031.80 vs 9506.39), 10-digit Section 301 list check, and origin strategy.
5. Hire the hardware EE and an NPI/ops advisor (fractional).
6. Book the PGA Show (January 2027) to meet Korean incumbents, simulator software partners and dealers.
7. Start seed fundraising, framed around the G0 accuracy result (target March–April 2027 close).

---

### Research limitations

The shared web-search budget ran out during this research. Several items are therefore marked [est.]:
- per-component prices below the SoM level,
- salaries and contract rates,
- design-firm fee ranges,
- calibration-station costs,
- freight rates,
- crowdfunding delay statistics,
- EU duty rates.

They reflect typical industry figures and should be replaced with vendor quotes (§10). The tariff stack, Jetson pricing, IMX296 module pricing, tooling ranges, certification ranges, competitor and funding comparables, and reference-equipment prices are sourced as cited.
