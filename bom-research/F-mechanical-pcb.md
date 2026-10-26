# F. Mechanical, PCB Fabrication and Assembly: BOM Research

*Outer Bounds launch monitor. Research date: 7 October 2026. Slice F covers PCB fab and assembly, the optical bench, enclosure, IR window, hardware, cables, accessories, packaging and labor.*

**Conventions**
- **Prices** are USD per finished unit unless noted. Shipping, import duty and VAT are excluded.
- **$@1** is the cash cost of building one unit. Unavoidable minimum lots and setup fees are charged to that single unit; for example, a PCB is bought as a 5-piece lot.
- **$@100** spreads setup over 100 units.
- **$@1k and $@10k** are piece prices **excluding** hard tooling. Tooling is listed separately in §3.
- **[est.]** marks my engineering estimate where no published price exists. The basis is given in the notes.
- **Not in this slice, so not double-counted:** electronic components on the boards (SOM, camera modules, LEDs, radar, Wi-Fi, display, battery cells, fan motor electronics).
- **Tariffs:** JLCPCB collects US tariffs at order time. China-origin PCBAs carry Section 301 stacking (see `research/09-manufacturing-team-roadmap.md` §2). Budget +25–40% on China-sourced fab and assembly lines if the units land in the US.

---

## 1. Line-item BOM (centerpiece)

| # | Item | Supplier | MPN/spec | URL | Qty/unit (Pro / Indoor) | $@1 | $@100 | $@1k | $@10k | One-time tooling/NRE | Lead time | Notes/alternates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **P1** | Main carrier PCB (bare) | JLCPCB (proto, HDI since 14 Sep 2026). PCBWay / Highleap / Atlas for volume | 10L 1+N+1 HDI (8L through-via fallback), ~120×90 mm, 1.6 mm, TG170 (S1000-2M / NP-175F), ENIG, ±10% impedance, POFV via-in-pad, 4-wire Kelvin test | [JLC caps](https://jlcpcb.com/capabilities/pcb-capabilities), [JLC HDI launch](https://jlcpcb.com/news/hdi-pcb-manufacturing-services), [Schemalyzer](https://www.schemalyzer.com/en/blog/manufacturing/jlcpcb/jlcpcb-design-rules), [Highleap](https://hilelectronic.com/8-layer-blind-buried-via-pcb-price/), [AtlasPCB](https://www.atlaspcb.com/blog/jlcpcb-vs-custom-pcb-manufacturer-production-volume-cost-2026/), [PCBSync](https://pcbsync.com/pcb-manufacturing-cost/) | 1 / 1 | 350 (5-pc lot) [est.] | 38 | 20 | 13 [est.] | $25–250 fab tooling per design at production fabs (PCBSync). JLC has none. | Proto 7–12 working days [est.]. Production 3–4 wk | JLC 8L starts ~$82/5 pcs and 10L+ at $137+/5 pcs, both at 100×100 non-HDI (Schemalyzer). HDI 8L 1+6+1 at 100×100 ENIG: $62–78 @10, $48–62 @50, $28–38 @500 (Highleap). 10L 1+N+1 @500: $18–24 (AtlasPCB). JLC HDI is ~10–20% dearer at 500+ (AtlasPCB). JLC raised substrate-linked prices on 13 Jun 2026 ([notice](https://jlcpcb.com/news/jlcpcb-pcb-pricing-notice)). PCBWay builds 1+N+1 to 6+N+6 ([PCBWay HDI](https://www.pcbway.com/hdi-pcb.html)) but publishes no HDI price, so get a quote. **Avoid HDI if the RK3588 SOM sits on B2B connectors.** Then a 10L through-via board can work (0.15 mm vias, POFV free at JLC 6L+), saving ~30–40%. |
| **P2** | Carrier SMT assembly (labor only) | JLCPCB Standard PCBA (proto, ≤1k). Taiwan/Vietnam EMS (volume). MacroFab (US alt.) | Double-sided, ~400 placements ≈1,500 joints, ~80 unique parts, ~15 X-ray parts (PMIC/QFN/LGA). SOM **not soldered**; only its B2B receptacles are placed. | [JLC PCBA price](https://jlcpcb.com/help/article/pcb-assembly-price), [MacroFab invoice](https://docushare.wipac.wisc.edu/dsweb/Get/r_Document-90455/unknown), [MacroFab FabIQ](https://www.macrofab.com/blog/fabiq-saves-time-money), [RayPCB](https://www.raypcb.com/what-affect-pcb-assembly-cost/) | 1 / 1 | 254 (5-board lot) | 7 | 5 [est.] | 4 [est.] | JLC stencils $16.42 (2-sided). ICT/FCT fixture $8–25k (§3) | JLC +3–5 days after fab. EMS 3–5 wk | JLC Standard: $51.12 double-sided setup + $16.42 stencil + $1.53/unique-part feeder load + $0.0016/joint (falls to $0.0012 >100k joints) + X-ray $1.64→$0.082 per component by volume. @1k: about $2.4 joints + $1.2 X-ray + AOI/FCT. **MacroFab (US):** 2022 invoice for 8 complex boards shows labor $157/unit including setup and loading. Budget $150–250 per board @≤10 and ~$25–40 @100 [est.]. Components and SOM are sourced or consigned on top (other slices). The JLC page doesn't describe consignment, so confirm the parts-library/consign flow. |
| **P3** | LED / strobe boards | JLCPCB (MCPCB or FR4), PCBWay | 3 × ~30×25 mm. **Recommended: 2-layer FR4 or 2-layer IMS** with the GaN FET + local cap bank at the LEDs. 1-layer Al MCPCB is the alternative. | [JLC home: MCPCB from $4/5 pcs](https://jlcpcb.com/), [PCBWay Al PCB](https://www.pcbway.com/aluminum-pcb.html), [JLC PCBA price](https://jlcpcb.com/help/article/pcb-assembly-price) | 3 / 3 (set) | 30 (lot: fab $4 + economic PCBA setup $8.18 + stencil $1.53 + feeders) | 4.20 | 2.10 [est.] | 1.35 [est.] | none | 1–2 wk | Price is for the board set (3) incl. assembly, excl. LEDs/FETs. Strobe duty cycle is µs-scale, so average heat is low and MCPCB isn't needed thermally. A 1-layer MCPCB can't build a tight high-di/dt loop over a return plane, which matters more for a 10s-of-amps pulse. |
| **P4** | Flex interconnects | JLCPCB (flex), PCBWay (flex and rigid-flex) | 2 × 2-layer PI FPC, ~80×15 mm, ENIG fingers, PI/FR4 stiffener, no SMT (ZIF/B2B ends) | [JLC flex cost guide](https://jlcpcb.com/blog/flex-pcb-cost-pricing-guide), [JLC flex caps (no rigid-flex)](https://jlcpcb.com/capabilities/flex-pcb-capabilities), [PCBWay: flex/rigid-flex from $46.74](https://www.pcbway.com/) | 2 / 2 | 50 (2 designs × ~$25/5 pcs) | 5 | 2.40 [est.] | 1.20 [est.] | none (flex SMT would add $24.63/fixture at JLC) | 5–6 days proto | JLC flex is $2/5 pcs promo and ~$25/5 pcs typical. **JLC does not make rigid-flex.** Rigid-flex at PCBWay runs ~3–5× flex+connector [est.]. Keep passive FPC with connectors. |
| **M1** | Optical bench | Xometry / Protolabs / Fictiv (≤100, US). China CNC shop (1k+). Die-cast or extrusion at 10k | 6061-T6, ~200×80×15 mm, ~20 tapped holes (M2/M2.5/M3), 2 reamed Ø3 H7 dowel bores, datum face flatness ≤0.02 mm, black Type II anodize, stress-relieved stock (T651) | [Otronatlas (Xometry $118 qty1)](https://www.otronatlas.com/guides/cnc-machining-cost/), [Precision Smith](https://precisionsmith.com/capabilities/aluminum-6061-machining/), [Baetro](https://baetrocnc.com/resources/cnc-machining-cost-calculator/), [Davantech](https://www.davantech.com/how-much-does-cnc-machining-cost/), [Xometry anodize](https://www.xometry.com/anodizing-service/) | 1 / 1 | 250 [est.] | 40 [est.] | 20 [est.] | 12 (CNC) [est.] | Soft jaws/fixtures $1–3k [est.]. Die-cast tool $5–15k (§3) | US instant quote 3–10 days. China 3–4 wk | **@10: ~$110.** Benchmarks: Xometry quoted $118 for a simple unanodized bracket at qty 1 (Mar 2026). Precision Smith quotes a 150×100×40 anodized bracket at $80 @1, $30 @10, $12 @50, $4 @1k. Baetro: $295/$122/$70 at 1/10/100. Davantech: 100-pc anodized bracket ~$70 US vs ~$25 China. Our part has more features and tight datums, so I used the high side. **10k alternatives:** die-cast A380 ~$2.35 vs $6 machined for a bracket at 10k ([Meco 2026](https://www.mecomeco.com/blog/how-much-does-it-cost-to-get-a-metal-part-made-the-complete-2026-pricing-guide/)). Ours still needs datum machining + anodize, so ~$6–7 [est.]. Extruded 6061/6063 profile + light CNC ~$6–9 [est.] ([Xometry extrusions](https://www.xometry.com/capabilities/metal-extrusion-services/custom-aluminum-extrusions/)). |
| **M2** | Enclosure rigid parts | ≤500: JLC3DP MJF PA12 (dyed). 1k+: injection molder (China/Vietnam) | Front housing, rear housing (battery bay, tripod boss, vent port), battery door / blank plate (**one tool, swap insert**), display bezel / blank plate (swap insert), 2 fold-out feet (2-cav), internal LED/camera baffle (black PC), button caps / light pipe. PC/ABS UL94 V-0, MT-11010-class texture. ~410 g/set. | [JLC3DP $0.275/g](https://jlc3dp.com/news/drastic-material-price-cuts-and-adjusted-post-processing-service-fees), [JLC3DP Jul 2026 cuts](https://jlc3dp.com/news/materials-finishing-pricing-update-july2026), [xinyangmfg](https://xinyangmfg.com/low-volume-injection-molding-cost-hardware-startups/), [Jaycon](https://www.jaycon.com/injection-moulding-price-a-2025-guide-for-engineers-procurement/), [Elite Mold](https://elitemoldtech.com/injection-mold-cost/) | 1 set / 1 set | 180 (Pro) / 170 (Indoor) | 135 / 128 | 13.50 / 13.20 [est.] | 8.80 / 8.60 [est.] | Al bridge set ≈ $40k, or P20 set ≈ $80k incl. T1→T3 mods (§3) | MJF 72 h build. Al tools 15–25 working days, P20 20–35 days, plus T1→T3 4–8 wk | MJF: 410 g × $0.275/g ≈ $113 + dye + shipping. July 2026 cuts may lower this. Molded piece prices are built up from part mass and PC/ABS resin at $2.00–3.50/lb (ABIS/xinyang). One source gives $1.80–3.60/part at 1k from 1-cavity Al tools for small parts. Our housings are ~260×180, so: front $4.50/$3.00, rear $5.00/$3.40, door $0.90/$0.55, bezel $0.70/$0.45, feet $0.60/$0.35, baffle $0.80/$0.50, buttons $0.50/$0.30, laser/pad print + insert install $0.50/$0.25 (@1k/@10k). **Urethane casting is worse than MJF at 100:** MakerStage puts master+silicone at ~$1,200 and ~$55/part for a *palm-sized* enclosure ([MakerStage](https://www.makerstage.com/resources/urethane-casting-vs-injection-molding)). Molds last ~20–50 shots ([RJC](https://rjcmold.com/urethane-casting-cost/)), so a 6-part set ≈ $700+/unit at 100 [est.]. Use urethane only for cosmetic samples. |
| **M3** | Bumper | ≤500: MJF/SLS TPU or cast 60A urethane. 1k+: separate TPE molding | Stretch-fit TPE (Shore 60–70A) bumper with retention ribs, ~70 g | [xinyang overmolding](https://xinyangmfg.com/overmolding-cost-guide-startups/), [RJC](https://rjcmold.com/urethane-casting-cost/) | 1 / 1 | 30 [est.] | 22 [est.] | 2.50 [est.] | 1.60 [est.] | Separate TPE tool $6–10k [est.]. 2-shot onto housing $14–48k; insert-overmold $6.5–22k (xinyang) | 4–6 wk tool | **Recommend a separate stretch-on bumper over 2-shot.** The tool is ~1/3 the cost, the bumper is user-replaceable, and the housing tool stays simple. Overmold benchmark: 35 g part $3.20–5.40 @5k, $2.40–4.20 @25k (xinyang). |
| **M4** | IR front window | Prototype: laser-cut ACRYLITE 9M020 (ex-1146-0) or Plexiglas 3143. Production: chemically strengthened glass with IR ink (Felix Glass / Saida Glass, Dongguan) | Prod: 0.7–1.1 mm CS soda-lime/aluminosilicate, ~180×60 mm, IR-transmissive black ink (vis <2%, ≥90% @940 nm per Felix), AR both sides on camera apertures, **IR-opaque black band between LED and camera zones** | [ACRYLITE extruded LT&R (9M020)](https://www.acrylite.co/files/content/acrylite.co/documents/product-information/ACRYLITE-Extruded-Light-Transmission-Reflectance-Information.pdf), [ePlastics 3143](https://www.eplastics.com/plexiglass/acrylic-sheets/ir-transmitting), [Felix Glass](https://www.felixglass.com/products2152731/Smart-Appliance-Display-Glass.htm), [Saida Glass](https://saidaglass.en.made-in-china.com/product/ifARENDBJLhV/China-OEM-0-5mm-Precise-Camera-Cover-7h-Glass-with-Double-Side-Ar-Coating-and-Transmittivity-Over-95-at-940nm-IR.html) | 1 / 1 | 25 (acrylic) | 8 [est.] | 5 [est.] | 3.50 [est.] | Print screens, CNC/cut jigs $0.5–1k [est.]. Molded IR-PC alt: tool $10–18k incl. SPI-A2 polish | Glass 3–5 wk [est.]. Acrylic stock | ePlastics 3143 0.118" 12×12 in is $23.89 (1–2 pcs); 24×48 in is $34.27 (50+), giving ~40 windows/sheet. Saida's small 0.5 mm 940 nm AR camera glass (>95% @940) is $4.00 @500–999, $3.00 @1k–5k, $2.50 @5k+, $20 sample; our larger printed window is scaled up. **Alternatives:** molded IR-black PC, either Makrolon (Covestro IR-transparent black 900346 or ST colors 978001/970001/971064/970005, [Covestro](https://solutions.covestro.com/-/media/covestro/solution-center/brochures/pcs/brochures/optical-properties-of-makrolon-and-apec.pdf)) or LEXAN SLX2271T ([SABIC](https://materialfinder.sabic-specialties.com/material/lexan-copolymer-slx2271t)). That needs a hard-coat. **Do not specify "LEXAN 940"**: it is a flame-retardant grade, not an IR grade. |
| — | *(Reference, counted in camera slice)* Per-lens 940 nm bandpass | Commonlands, Edmund, MidOpt | CBP940: T>90% @940, OD3, ~80 nm FWHM, 0.3 mm. Or ~40–55 nm FWHM (MidOpt BN940: 928–955 nm) | [Commonlands](https://commonlands.com/products/940nm-bandpass-filter), [Edmund #65-670](https://www.edmundoptics.com/p/940nm-cwl-10nm-fwhm-125mm-mounted-diameter/20188/), [Edmund Everix](https://www.edmundoptics.com/p/everix-ultra-thin-od-2-bandpass-filter-940nm-125mm-dia/48729/), [RMA BN940](https://www.rmaelectronics.com/midwest-optical-bn940/) | 3 / 3 | $9–15 ea | — | ~1.5–4 ea [est.] | ~1–2.5 ea [est.] | — | stock | Edmund 10 nm mounted 12.5 mm: $105 (1–9). Everix 0.4 mm: $76.50. See §4 for why the window can't replace these. |
| **M5** | Gaskets | China die-cutter (volume). Pres-Bond-style digital cut (proto) | Window gasket (closed-cell silicone foam, PSA), housing perimeter (silicone or EPDM foam), battery-door gasket (Pro). FIPG dispensing is an alternative for the perimeter. | [Alibaba die-cut gaskets](https://www.alibaba.com/supplier/die-cut-gasket-manufacturer.html), [Strouse](https://www.strouse.com/blog/custom-gasket-cost), [Pres-Bond](https://presbond.com/collections/die-cut-foam-tape-gaskets) | 3 / 2 | 15 / 10 [est.] | 2.50 / 1.80 [est.] | 1.20 / 0.85 | 0.60 / 0.42 [est.] | Steel-rule dies $500+ each (Strouse), ~$1.5–3k for 3 | 2–4 wk | Listings: custom die-cut foam (incl. silicone) $0.158–0.169 @1k MOQ; closed-cell silicone PSA $0.56–0.76; EPDM/neoprene/PORON $0.06–0.12. Silicone foam (Bisco-class) holds compression set better outdoors than EPDM. Use it on the window. |
| **M6** | Protective (ePTFE) vent | Amphenol LTW (Digi-Key 1754-1230-ND). Alt: Gore VE8 adhesive | VENT-PS1YBK-N8001 (M12×1.5 screw-in w/ nut, IP69K, >1000 ml/min @70 mbar). Alt: Gore VE80510 / VE80205 adhesive | [Digi-Key](https://www.digikey.com/en/products/detail/amphenol-ltw/VENT-PS1YBK-N8001/7898285), [Arrow](https://www.arrow.com/en/products/vent-ps1ybk-n8001/amphenol.html), [Gore adhesive datasheet](https://www.gore.com/sites/default/files/resources/pdf/2025-09/gore-ptv-adhesive-series-datasheet-en.pdf), [RS VE80205](https://uk.rs-online.com/web/p/enclosure-ventilation/2879532) | 1 / 1 | 3.47 | 2.22 | 1.77 | 1.40 [est.] | none | stock | Arrow 1000+ is $1.439. Gore VE80205: £2.93 (50) → £1.58 (1000+), sold only in packs of 50. "PolyVent" is Gore's snap-in/screw-in line; the adhesive line is VE7/VE8/VE9. **Adhesive VE8 is preferred for production** (low profile, no M12 boss). |
| **M7** | Tripod 1/4"-20 thread | McMaster-Carr (proto). Generic CN brass insert (volume) | 93365A162: heat-set tapered brass insert, 1/4"-20 × 0.5" L | [McMaster](https://www.mcmaster.com/93365A162/), [reseller price](https://shop.trymaterialize.com/products/mcmaster-carr/93365a162) | 1 / 1 | 0.59 | 0.59 | 0.30 [est.] | 0.15 [est.] | none | stock | **Recommendation:** put the 1/4"-20 thread in metal tied to the chassis. Either tap it directly into a boss on the optical bench (≈$0 extra) or use a knurled press-in brass insert in a rib-backed boss screwed to the bench. A heat-set insert in PC/ABS alone will creep under tripod torque and a 2.5 kg cantilever. |
| **M8** | Fasteners, pins, hinge hardware | McMaster (proto). CN fastener house (volume) | ~14 screws (thread-forming PT/Delta-PT M2.5/M3 into PC/ABS; M2/M3 SS machine screws into bench), 2 × Ø3 h6 dowel pins (bench datum), 2 SS hinge pins + detent springs (fold-out feet), battery-door latch spring (Pro) | [McMaster](https://www.mcmaster.com/) | 1 kit / 1 kit | 4 [est.] | 1.50 [est.] | 0.60 [est.] | 0.35 [est.] | none | stock / 2–3 wk | No live quote. Low-cost commodity line. |
| **M9** | Feet pads | 3M via Digi-Key | Bumpon SJ5302 (7.9 × 2.2 mm PU dome). Use a larger Bumpon or molded-in TPE pads on the fold-out feet | [Digi-Key SJ5302](https://www.digikey.com/en/products/detail/3m/SJ5302/2345107) | 4 / 4 | 0.50 (min pack 144 ≈ $18) | 0.48 | 0.42 | 0.37 | none | mfr std 4 wk | $0.12451 @144, $0.10516 @1,008, $0.09316 @5,040, $0.08057 @50k. |
| **M10** | Thermal kit (mechanical) | Extruded/skived Al heatsink vendor, blower OEM | Heatsink (Al extrusion or die-cast, heat-pipe to SOM), thermal pads, ~50 mm blower with lead | [Internal research §1.2 row 15](../research/09-manufacturing-team-roadmap.md) | 1 / 1 | 70 [est.] | 35 [est.] | 18 [est.] | 12 [est.] | Heatsink extrusion die $1–3k [est.] | 3–6 wk | Carried over from the roadmap BOM ($18 @1k, $12 @10k). No live quote in this pass. **Couple the heatsink to the shell, not to the optical bench.** That keeps SOM heat gradients out of the stereo baseline. |
| **M11** | Labels | label printer | Rating/serial/FCC label, polyester, laser-markable | — | 1 / 1 | 1 [est.] | 0.50 [est.] | 0.15 [est.] | 0.08 [est.] | none | 2 wk | — |
| **C1** | Battery-bay connector + harness | Pack house / harness CM | Blade or pogo contact block in bay + 4–6 wire, 18–22 AWG harness to carrier, keyed | [MiniProto: custom JST from $46.07](https://www.miniproto.com/products/custom-jst-ph-to-jst-pa-wire-harness-assembly), [WireHarnessProduction 2026](https://wireharnessproduction.com/blog/custom-wire-harness-cost-guide) | 1 / 0 | 46 | 12 [est.] | 4 [est.] | 2.50 [est.] | Harness NRE $500–5,000 (all harnesses) | 2–4 wk | Simple harness (2–5 wires, China/SEA): $15–50 proto, $5–20 @50–500, $2–8 @500–5k, $0.50–3 @5k+. US adds 30–60%. Contact block ≈ $1 at volume [est.]. |
| **C2** | LED board harnesses | Harness CM | 3 × 4-wire twisted (pulse power + trigger), JST GH/PH, ~120 mm | [WireHarnessProduction 2026](https://wireharnessproduction.com/blog/custom-wire-harness-cost-guide) | 3 / 3 (set) | 15 [est.] | 9 | 4.50 | 2.40 | (in C1 NRE) | 2–4 wk | Prototypes are hand-built from pre-crimped leads. Could be replaced by P4 flex. |
| **C3** | Fan cable | — | Comes on the fan | — | 0 | 0 | 0 | 0 | 0 | — | — | Included with M10. |
| **C4** | Display FPC (Pro) | — | Supplied as the display tail | — | 0 | 0 | 0 | 0 | 0 | — | — | If an extension is needed, use a P4-type FPC (+$1.20 @1k). |
| **C5** | Radar cable | Harness CM | 6–10 pin JST GH 1.25 mm, ~100 mm | [WireHarnessProduction 2026](https://wireharnessproduction.com/blog/custom-wire-harness-cost-guide) | 1 / 1 | 5 [est.] | 3 | 1.20 | 0.70 | (in C1 NRE) | 2–4 wk | Standard tier: $3–15 @5k+. Shorter or simpler is cheaper. |
| **C6** | Camera MIPI FFC/FPC jumpers | FFC vendor | 3 × 15/22-pin 0.5 mm FFC (only if module tails don't reach) | — | 3 / 3 | 9 [est.] | 4.50 [est.] | 1.50 [est.] | 0.90 [est.] | none | stock | Often $0 if the camera modules carry their own FPC. |
| **A1** | Carry case (Pro in-box) | ≤100: Nanuk 920 + custom PE foam (GunFoam/Fuerte). 1k+: custom molded EVA semi-hard case | Nanuk 920 w/ foam (interior 15×10.5×6.2 in, 2.3 kg). Alt: Pelican 1450-000-110 | [Nanuk](https://nanuk.com/products/nanuk-920), [B&H Nanuk](https://www.bhphotovideo.com/c/product/902354-REG/Nanuk_920_1001_Case_with_Cubed.html), [REI Pelican](https://www.rei.com/product/245078/pelican-1450-protector-case-with-foam), [GunFoam 1450 insert](https://www.gunfoam.com/foam-inserts/pelican/classic/pelican-1450-custom-foam-insert-only), [Fuerte](https://www.fuertecases.com/mm5/merchant.mvc?Screen=CTGY&Category_Code=Custom-Foam) | 1 / 0 | 215 | 150 [est.] | 18 [est.] (EVA) | 11 [est.] (EVA) | EVA case mold $3–5k [est.]. Foam die $0.5–1.5k [est.] | stock / EVA 5–7 wk | Nanuk 920 is $159.95 list, $127.96 on sale. Pelican 1450 with foam is $169.95 (REI, B&H). GunFoam custom 1450 insert is $86.99, or $234.99 with the case. No OEM volume price is published; dealer pricing at 100 is ~30% off list [est.]. **At 1k the Nanuk/Pelican route is ≈ $100–115 [est.]**, so sell it as a premium accessory and ship an EVA case. SKB iSeries not priced. |
| **A2** | Retail box | Rigid-box packager (Cubit, CustomPackingCo, CN) | 2-piece or magnetic rigid box ~330×240×130 mm, 1200 g greyboard, printed wrap, molded-pulp or EVA insert | [CustomPackingCo 2026](https://custompackingco.com/custom-rigid-boxes-cost/), [Cubit](https://www.cubitpackaging.com/blog/custom-rigid-box-pricing-guide) | 1 / 1 | 40 [est.] | 14 | 11 | 5.50 | Plates/dies $0.5–1k [est.] | 3–5 wk | For an 8×6×3 in box: $7.00 @1k (+$1.00 magnet), $3.50 @10k (+~$0.70). Magnetic @100 is $7.80–10.50. Scaled ×1.3–1.4 for our size. EVA insert $0.40–1.20 @1k. |
| **A3** | Alignment stick | CN OEM | 2-piece fiberglass/Al rod, printed alignment marks, storage clips | — | 1 / 1 | 15 [est.] | 6 [est.] | 2.50 [est.] | 1.50 [est.] | — | 3–4 wk | — |
| **A4** | Quick-start card + regulatory leaflet | printer | 4-color card + leaflet | — | 1 / 1 | 2 [est.] | 0.80 [est.] | 0.25 [est.] | 0.10 [est.] | — | 1–2 wk | — |
| **A5** | Shipping carton | corrugated | RSC outer + void fill | — | 1 / 1 | 5 [est.] | 2.50 [est.] | 1.20 [est.] | 0.80 [est.] | — | 1–2 wk | — |
| **L1** | Final assembly, EOL test, calibration, pack | Self (≤100) / US-MX NPI line / Taiwan-VN EMS | 1.0–1.5 labor-h at volume | [Internal research §2](../research/09-manufacturing-team-roadmap.md) | 1 / 1 | 240 [est.] | 100 [est.] | 35 | 18 | Calibration station $25–80k each. EOL fixtures $100–300k total (§3) | — | @1 ≈ 3 h engineer time. @100 ≈ 1.5–2 h at US/MX $55–70/h. @1k/@10k from the roadmap (CN ~$30→$15; TW +~$10; VN ~−$1). |

### 1.1 Roll-up per unit (this slice only)

| Group | Pro $@1 | Pro $@100 | Pro $@1k | Pro $@10k | Indoor $@1 | Indoor $@100 | Indoor $@1k | Indoor $@10k |
|---|---|---|---|---|---|---|---|---|
| PCB fab + assembly (P1–P4) | 684 | 54 | 29.50 | 19.55 | 684 | 54 | 29.50 | 19.55 |
| Mechanical (M1–M11) | 580 | 248 | 63.44 | 40.85 | 565 | 240 | 62.79 | 40.47 |
| Cables (C1–C6) | 75 | 28.50 | 11.20 | 6.50 | 29 | 16.50 | 7.20 | 4.00 |
| Accessories + packaging (A1–A5) | 277 | 173 | 32.95 | 18.90 | 62 | 23.30 | 14.95 | 7.90 |
| Final assembly labor (L1) | 240 | 100 | 35 | 18 | 240 | 100 | 35 | 18 |
| **Total excl. tooling** | **≈ 1,856** | **≈ 604** | **≈ 172** | **≈ 104** | **≈ 1,580** | **≈ 434** | **≈ 149** | **≈ 90** |
| + amortized slice tooling (see §3 assumption) | — | — | +68.50 | +10.85 | — | — | +68.50 | +10.85 |
| **Total incl. amortized tooling** | 1,856 | 604 | **≈ 241** | **≈ 115** | 1,580 | 434 | **≈ 218** | **≈ 101** |

At $@1 the PCB lines include whole 5-piece lots, so four spare boards come with them. The calibration station and EOL fixtures ($100–300k) are **not** in the amortized line. They were covered in the roadmap; amortizing them adds roughly +$15–50/unit at 10k.

### 1.2 Enclosure per-unit, including tooling (as requested)

| Volume | Process | Piece (rigid set + bumper) | Tooling | Amortization assumption | **Enclosure $/unit** |
|---|---|---|---|---|---|
| 1 | MJF PA12 (JLC3DP) + TPU bumper | $210 | 0 | — | **$210** |
| 100 | MJF PA12 + TPU/cast bumper | $157 | 0 | — | **$157** |
| 1k | Aluminum bridge tools (CN), PC/ABS + separate TPE bumper | $16.00 | ≈ $40k (8 tools) | Spread over 1,000 units only | **≈ $56** |
| 10k | P20 production tools (CN), PC/ABS + TPE | $10.40 | ≈ $80k (8 tools incl. T1→T3 mods) | Spread over 10,000 units | **≈ $18.40** |
| Alt. 1k→10k | Go **straight to P20** at DVT; skip the Al bridge | $16 → $10.40 | ≈ $80k once | Spread over 10k lifetime | ≈ $24 @1k cohort, $18.40 @10k |

Indoor uses the same tools; its blank plates come from swap inserts in the door and bezel tools. Indoor is ~$0.30–0.50 cheaper per unit (no door gasket or latch).

---

## 2. Key research findings by topic (short)

**PCBs**
- JLCPCB launched **HDI on 14 Sep 2026** (1st–3rd order, 3/3 mil, 0.075 mm laser vias) but publishes no price.
- 8L+ boards include ENIG and POFV via-in-pad at no charge, and 8L+ requires the 4-wire Kelvin test.
- Impedance is ±10% standard, with ±5% on request ([JLC caps](https://jlcpcb.com/capabilities/pcb-capabilities)).
- JLC does **not** offer rigid-flex ([JLC flex caps](https://jlcpcb.com/capabilities/flex-pcb-capabilities)).
- PCBWay builds HDI up to 6+N+6 plus rigid-flex, quote-only.
- MacroFab publishes no rate card. Quotes come from FabIQ, and production can run in the USA or Mexico.

**Optical bench**
- CNC 6061-T6 is the right process through 1k.
- At 10k, a **6061/6063 extrusion with CNC-finished datums** is safer for 0.01° stability than A380 die-cast. Die-cast has porosity, lower stiffness consistency and residual stress, and still needs datum machining.
- Mount the bench to the shell **kinematically** (one fixed point, one slot, one floating) so shell flex and thermal growth don't bend the stereo baseline.
- For scale, 0.01° over 80 mm is about 14 µm.

**Enclosure**
- MJF beats urethane casting at 1–500 for a set this size.
- Aluminum bridge tooling suits ≤5–10k shots. P20 wins above about 10k ([xinyang](https://xinyangmfg.com/low-volume-injection-molding-cost-hardware-startups/), [Elite Mold](https://elitemoldtech.com/injection-mold-cost/), [Jaycon](https://www.jaycon.com/injection-moulding-price-a-2025-guide-for-engineers-procurement/)).

**Labor and fixtures**
- See `research/09-manufacturing-team-roadmap.md`. It uses 1.0–1.5 labor-hours per unit. Each calibration station costs $25–80k and handles about 10k units per year on one shift.

---

## 3. One-time tooling / NRE (this slice)

| Item | Low | High | Used in amortization | Notes |
|---|---|---|---|---|
| Enclosure, aluminum bridge set (8 tools: front, rear, door/blank, bezel/blank, feet 2-cav, baffle, buttons/light-pipe, TPE bumper) | $30k | $45k | **$40k @1k** | Al ~0.3–0.5× P20; 5k–80k shot life ([Elite Mold](https://elitemoldtech.com/injection-mold-cost/), [Jaycon](https://www.jaycon.com/injection-moulding-price-a-2025-guide-for-engineers-procurement/)) |
| Enclosure, P20 production set (same 8 tools), incl. 15–20% T1→T3 mods | $60k | $95k | **$80k @10k** | Front/rear housings $14–20k each with slides; small tools $3–6k; TPE $6–10k ([xinyang](https://xinyangmfg.com/low-volume-injection-molding-cost-hardware-startups/)) |
| *Option:* 2-shot TPE bumper instead of separate tool | $14k | $48k | — | [xinyang overmolding](https://xinyangmfg.com/overmolding-cost-guide-startups/) |
| IR window: glass print screens / cut jigs | $0.5k | $1k | $1k | *Option:* molded IR-PC window tool with SPI-A2 polish $10–18k |
| Gasket steel-rule dies (×3) | $1.5k | $3k | $2k | [Strouse](https://www.strouse.com/blog/custom-gasket-cost) |
| Optical bench CNC fixtures / soft jaws | $1k | $3k | $2k | *Option @10k:* die-cast die $5–15k ([Meco](https://www.mecomeco.com/blog/how-much-does-it-cost-to-get-a-metal-part-made-the-complete-2026-pricing-guide/)), or extrusion die $1–3k [est.] |
| Heatsink extrusion die | $1k | $3k | (in M10) | [est.] |
| PCB fab tooling (carrier, LED, flex) + stencils | $0.1k | $0.8k | $0.5k | [PCBSync](https://pcbsync.com/pcb-manufacturing-cost/), [JLC](https://jlcpcb.com/help/article/pcb-assembly-price) |
| Carrier ICT/FCT fixture | $8k | $25k | $15k | Roadmap §3.2 |
| Harness NRE (all harnesses) | $0.5k | $5k | $3k | [WireHarnessProduction](https://wireharnessproduction.com/blog/custom-wire-harness-cost-guide) |
| EVA case mold + foam die | $3.5k | $6.5k | $4k | [est.] |
| Retail box plates / dies | $0.5k | $1k | $1k | [est.] |
| **Slice total used for amortization** | | | **$68.5k @1k (Al path) / $108.5k @10k (P20 path)** | gives +$68.50/unit @1k and +$10.85/unit @10k |
| Calibration station(s) + other EOL fixtures (**not** in the amortized line) | $100k | $300k | — | Roadmap §3.2. Station $25–80k each |

---

## 4. IR window and filter: recommendation

**Materials**

| Option | Material / part number | Supplier | 940 nm transmission | Cost at volume | Assessment |
|---|---|---|---|---|---|
| A (proto) | ACRYLITE extruded **9M020** IRT black (the old GP code 1146-0). Comparable: Plexiglas **3143** | Röhm/ACRYLITE ([PDF](https://www.acrylite.co/files/content/acrylite.co/documents/product-information/ACRYLITE-Extruded-Light-Transmission-Reflectance-Information.pdf)); ePlastics ([3143](https://www.eplastics.com/plexiglass/acrylic-sheets/ir-transmitting)) | Graph only in the datasheet. ~85–90% at 905 nm for 3 mm per [user reports](https://www.rdforum.org/threads/93943/) [unverified]. Cut-on ~750 nm. | ~$1–3 laser-cut | Cheap and stocked, but soft (scratches on turf grit). Use for EVT. |
| B | Molded IR-black PC: **Makrolon** IR-transparent black 900346 / ST colors; **LEXAN SLX2271T**, SLX1432, EXL1433T | Covestro ([brochure](https://solutions.covestro.com/-/media/covestro/solution-center/brochures/pcs/brochures/optical-properties-of-makrolon-and-apec.pdf)), SABIC ([SLX2271T](https://materialfinder.sabic-specialties.com/material/lexan-copolymer-slx2271t)) | SABIC patent claims ≥80–90% at 800–1,100 nm for 2 mm | ~$1–2 + hard-coat $1–2 [est.] + $10–18k tool | Tough and integrable. Needs hard-coat and optical-polish tooling, and is sensitive to flow lines and birefringence. |
| **C (recommended)** | **Chemically strengthened glass + IR-transmissive ink + AR** | Felix Glass ([link](https://www.felixglass.com/products2152731/Smart-Appliance-Display-Glass.htm)), Saida Glass ([link](https://saidaglass.en.made-in-china.com/product/ifARENDBJLhV/China-OEM-0-5mm-Precise-Camera-Cover-7h-Glass-with-Double-Side-Ar-Coating-and-Transmittivity-Over-95-at-940nm-IR.html)) | Ink area ≥90% (Felix spec). Clear AR aperture >95% (Saida) | $3–5 [est.]. Saida small part: $3 @1k, $2.50 @5k | Best scratch resistance for outdoor use, flat with low wavefront distortion, cheap tooling. |

**Can the window double as the 940 nm bandpass? No. Keep per-lens bandpass filters.**

1. **IR-black materials are long-pass, not bandpass.** All of A, B and C cut on around 750 nm and pass everything to ~1,100 nm. That band carries most of the solar NIR the silicon sensor can see.
2. **A dielectric bandpass on the big window has three problems:**
   - It shifts blue with angle across a wide field of view. With n_eff ≈ 2 at 25° AOI, the shift is ~20 nm, so a 10 nm filter would vignette the field edges.
   - Coating a large area costs more.
   - It looks mirrored or colored, which spoils the industrial design.
3. **Per-lens filters are cheap and tunable.** Use a ~40–55 nm FWHM per-lens filter centered on the 940 nm LED peak, e.g. the Commonlands CBP940 at $9–15 retail, glued behind the M12 lens. LED spectral width plus AOI shift make sub-20 nm filters counterproductive with wide lenses.
4. **What the window should do:** cosmetics, sealing and scratch protection.

**Crosstalk risk with a single shared window.** LED light can couple into the camera through internal reflection in the window.
- **Mitigation:** print an **IR-opaque black band** (not IR ink) on the glass between the LED and camera zones; ink in optical contact absorbs light that is guided inside the glass. Back it with a black foam baffle gasket compressed against the glass.
- **Alternative:** use separate small windows per camera and per LED cluster.

---

## 5. Key decisions and risks

**Decisions**
1. **Carrier:** prototype at JLCPCB (HDI is new as of September 2026, so check DFM). Production goes to a camera-literate Taiwan/Vietnam EMS that does fab plus PCBA in the **same country** as box build, for tariff origin. Before committing to HDI, test whether a through-via 10L can fan out the board-to-board SOM connectors; that saves ~30–40% on fab.
2. **LED boards:** 2-layer FR4/IMS with the switch and caps local to the LEDs, not a 1-layer MCPCB. The loop inductance matters more than heat at µs pulse duty.
3. **No rigid-flex.** Use passive FPC plus connectors; JLC can't build rigid-flex and it costs 3–5× more.
4. **Optical bench:**
   - Through 1k: CNC 6061-T651 with black anodize and reamed dowel datums.
   - At 10k: extrusion plus CNC datums, preferred over die-cast.
   - Kinematic 3-point mount to the shell.
   - Tripod thread tied into the bench or chassis metal, not just a heat-set insert in plastic.
5. **Enclosure:**
   - MJF PA12 through ~300–500 units.
   - Then **go straight to P20 at DVT** if the forecast is ≥5k. Al bridge plus P20 means paying for tooling twice (~$120k vs ~$80k).
   - Separate stretch-on TPE bumper, not 2-shot.
   - Indoor and Pro share all tools via swap inserts.
6. **IR window:** CS glass with IR ink, AR coat and an IR-opaque isolation band, plus per-lens 940 nm bandpass filters.
7. **Case:** a Nanuk/Pelican plus custom foam is ≈ $100–115 even at 1k, so sell it as a premium accessory and put a molded EVA case in the Pro box.

**Risks**
1. **Stereo drift above 0.01° from mechanical stress.** Causes: housing screws clamping the bench, heatsink gradients, tripod moment and drop shock. Mitigation: kinematic mount, thermal path to the shell, and a drop/thermal-cycle calibration-retention test at EVT.
2. **IR window optics:**
   - LED-to-camera crosstalk through the shared window.
   - Ink transmission varies batch to batch; ePlastics itself says IR acrylic varies by batch.
   - Requirement: get measured %T curves at 940 nm on the actual ink-on-glass sample, and set a minimum %T and a haze spec in incoming QC.
3. **Price data quality:**
   - HDI and MacroFab assembly have no published list prices; these lines are benchmarks and estimates. Run JLC, PCBWay and MacroFab instant quotes on the first Gerber/BOM set.
   - JLC raised prices on 13 Jun 2026 for substrate cost reasons, and collects tariffs up front.
4. **Tooling iteration:** budget T1→T3 at +15–20% and 4–8 weeks. IP54 gasket compression and window bonding usually need one or more steel-safe iterations.
5. **Aluminum bridge tool life** (5k–80k shots) is marginal for TPE and textured PC/ABS at 10k. Plan the P20 transfer early, or go P20 directly.
6. **IP54 vs fan:** a fan needs either a sealed heatsink (fins outside the sealed volume, fan in an external ducted channel, and a gasketed heatsink-to-shell interface) or a fully ducted path with IP-rated filters. **Do not run an open fan path through the sealed optics volume.** The ePTFE vent handles only pressure equalization.
