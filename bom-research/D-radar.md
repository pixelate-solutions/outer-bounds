# D: Radar Subsystem, Orderable Parts and Production BOM

*Outer Bounds launch monitor. Research date: 7 October 2026. Every price has a source URL. Anything not taken from a distributor or vendor page is labelled **est.** (my estimate) or **RFQ** (not published).*

---

## 0. Decision summary

| | Choice | Why |
|---|---|---|
| **Production** | **2× InnoSenT SMR-333 (order no. 80.00000346)**, 24 GHz CW I/Q SMT modules. One "rear/trigger head" looks back at the hitting zone. One "down-range/speed head" looks out along the target line. They are read by **2× TI ADS131M02** (simultaneous I/Q, 24-bit, 64 kS/s) and a **TI MSPM0G3507** radar MCU on its own board. | It is the **cheapest module with a real FCC/ISED modular grant** (FCC ID UXS-SMR3X3, IC 6902A-SMR3X3, plus TELEC). It transmits in **24.150–24.250 GHz**, which is legal in the US, EU, UK and France. It is I/Q, its IF runs DC–1 MHz, and it is SMT, 21×15×3 mm and −40…+85 °C. Price is **$13.80 @900 reel**, with 2,125 in stock. The full radar subsystem costs about **$42 @1k** (about $35 @10k est.). |
| **Backup** | **2× InnoSenT IPS-354 (80.00000356)**, 24 GHz CW I/Q with built-in IF pre-amp, using the same ADC/MCU chain | It has an FCC modular grant (UXS-IPS354, §15.249, ISED RSS-310) and runs 24.150–24.250 GHz. Sensitivity is better (12 dBi antenna, 27 dB conversion gain), and it is in stock (925). It is about 3.5× the module cost at **$49.20 @100**. |
| **Vendor-diverse "buy" fallback** | OmniPreSense **OPS243-A** (FCC 2ALLL243A) | It is fully digital, and an open-source golf launch monitor ([OpenFlight](https://github.com/open-flight/openflight)) already uses it for ball and club speed. At **$224 @1** with no published volume price, though, it is 5–6× the recommended solution at volume. It also has one narrow beam, so it cannot cover both the club approach and the ball down-range from a side unit. |
| **Rejected** | 60 GHz (IWR6843AOP / IWRL6432AOP / BGT60TR13C / XM125), Hi-Link, K-LD7/IMD-2000, CE-only RFbeam K-LC6/K-LC7 | See §3 and §2. In short: §15.255 duty-cycle and EIRP limits, only limited-modular approvals, speed ceilings below 90 m/s, or no FCC grant. |

**Why two heads (geometry).** From a unit about 50 cm to the side and about 30 cm forward of the ball, the club approaches from **azimuth about −155° → −121°** (behind and to the side). The ball leaves at about −121° and is at **−36° by 1 m and −11° by 3 m** of flight. That is a 145° sector, which no single certified module covers at useful gain. Two cheap heads cost $13.80 more than one, and each sees its target at **>0.8–0.98 of true speed**, so there is little cosine error to correct (numbers in §1).

---

## 1. Physics and geometry

**Doppler scale at 24.2 GHz:** λ = 12.39 mm, so f_d = 2v/λ = **161.4 Hz per m/s**.
- Ball 90 m/s → **14.5 kHz**.
- Club 60 m/s → **9.7 kHz**.
- At 60 GHz the scale is 400 Hz per m/s, so a 90 m/s ball gives 36 kHz.
- With complex (I/Q) sampling, fs ≥ about 1.3× f_dmax is enough. **64 kS/s complex gives ±32 kHz, or ±198 m/s.** 32 kS/s would cap at ±99 m/s with no margin, so do not use it.

**Placement model.** Unit at the origin. +x is down the target line. The ball is at (−0.30, −0.50, 0) m. Launch is 12° vertical, 0° horizontal. The radial factor is cos(angle between line of sight and velocity):

| Object / position | Azimuth from unit | Elevation | Radial factor (v_r / v) | Doppler @ 90 m/s ball / 40 m/s club |
|---|---|---|---|---|
| Club, 20 ms pre-impact (~0.8 m back) | −155° | ~+7° | **−0.91** (approaching) | 5.9 kHz |
| Club, 5 ms pre-impact | −135° | ~+2° | −0.70 | 4.5 kHz |
| Ball at impact | −121° | 0° | −0.50 | 7.3 kHz |
| Ball after 0.5 m | −69° | +11° | +0.38 (crossing) | 5.5 kHz |
| Ball after 1.0 m | −36° | +14° | **+0.81** | 11.8 kHz |
| Ball after 2.0 m | −17° | +13° | **+0.96** | 13.9 kHz |
| Ball after 3.0 m | −11° | +13° | **+0.98** | 14.3 kHz |

**Consequences**
1. **Without a down-range radar, ball speed is unusable.** The ball crosses the unit's broadside, where v_r passes through zero, during the first 0.5 m.
2. **Down-range head:** boresight at about **az −25°, el +12°**. Mount the SMR-333's **116° plane horizontal** (covers −83°…+33° az) and its **43° plane vertical** (covers about −10°…+33° el). Indoors, the ball is at >0.8 cosine from about 1 m out to the screen at 2.4–3.7 m. That is 21–36 ms at 70 m/s: roughly 1,300–2,300 complex samples at 64 kS/s.
3. **Rear/trigger head:** boresight at about **az −140°, el +5°** (roughly along the camera axis), with the 116° plane horizontal (covers −198°…−82°). The club approaches at 0.7–0.9 of its speed for about 20–25 ms before impact. That is the trigger (a) and the club-speed readout (b). Its 116° plane overlaps the forward head at about −83° to −93°, so coverage is continuous.
4. **Cosine correction stays radar-only, which matters for the patent separation.** A target on a straight line past a CW radar gives a Doppler "S-curve": f(t) = (2v/λ)·x(t)/√(x(t)² + d²). Fitting **v, t₀ and miss distance d** to the radar's own time–frequency track gives the asymptotic true speed. Residual error at 3 m with a 12° launch is about 1.5% before the fit. **Do not** use camera-derived geometry to correct the radar. Comparing the two outputs happens only at the application layer (job c, the "disagree" flag).
5. **Link budget for the SMR-333 with a golf ball** (RCS ≈ πa² ≈ 1.4×10⁻³ m²; datasheet gives 120–360 µVrms for 0.5 m² at 5 m). The [r⁻⁴ calc] gives about **70–210 µVrms at 1.5 m** and **18–53 µVrms at 3 m**. Datasheet noise is 20 µVrms over 100 Hz–1 kHz, about 0.67 µV/√Hz. In a 512-point FFT bin (78 Hz) the noise is about 6 µV, so **SNR is about 10–19 dB at 3 m and 22–31 dB at 1.5 m**. That is adequate but not lavish, and it is the main reason the IPS-354 (≥7 dB more sensitive) is the backup.

---

## 2. 24 GHz Doppler module comparison (orderable parts)

"FCC grant" here means a real FCC ID that host products can reuse. "CE" means a self-declaration only.

| Module (MPN) | TX/RX, I/Q | Beam (−3 dB) | Max speed / IF BW | Interface | Certification (as module) | $@1 / $@100 / $@1k | Stock / lifecycle | Verdict | Source |
|---|---|---|---|---|---|---|---|---|---|
| **InnoSenT SMR-333** (80.00000346) | 1T/1R, **I/Q** | **43°×116°** (1×4 patch) | IF DC–1 MHz → no limit; EIRP ≤12.7 dBm; 24.150–24.250 GHz | Analog I/Q (no IF amp; overall gain 29 dB) → ADC needed | **FCC UXS-SMR3X3** (DXT, 15C; modular approval letter on file; host label "Contains FCC ID"), **IC 6902A-SMR3X3**, **TELEC R219-247202**, ETSI EN 300 440 compliant | $19.10 / $15.10 / **$13.80 @900 reel** | 2,125 in stock, 16 wk, **Active**, SMT 21.4×15×3.1 mm, 3.3 V 47 mA, −40…85 °C | **PRODUCTION PICK** | [Digi-Key](https://www.digikey.com/en/products/detail/innosent-gmbh/80-00000346/10419768), [datasheet V2.4](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7183/2191_SMR-313%20%26%20SMR-333%20Data%20Sheet%20V2.4.20241007125146397.pdf), [InnoSenT](https://www.innosent.de/en/sensors/smr-333/), [FCC](https://fccid.io/UXS-SMR-3X3) |
| InnoSenT SMR-313 | 1T/1R, I/Q | 121°×111° (1×1 patch) | Same as SMR-333; 24 dB overall gain | Analog I/Q | Same FCC/IC IDs (no TELEC) | Order no. and price not confirmed (sibling parts are $19.28–$25.29 @1) | Active | Single-head cost-down candidate (one wide beam for club + ball); 5 dB less gain | [datasheet](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7183/2191_SMR-313%20%26%20SMR-333%20Data%20Sheet%20V2.4.20241007125146397.pdf), [Digi-Key list](https://www.digikey.com/en/products/result?keywords=SMR-333) |
| InnoSenT SMR-334 (80.00000347) | FMCW-capable variant | — | — | Analog | SMR-3x4 datasheet V2.5 | $25.29 / $20.39 / $18.50 @900 | 274 stock, Active | Not needed (CW is enough) | [Digi-Key](https://www.digikey.com/en/products/result?keywords=80.00000347) |
| **InnoSenT IPS-354** (80.00000356) | 1T/1R split antennas, **I/Q** | 45°×38° | **IF DC–60 kHz** (≥ 14.5 kHz ✔); EIRP 11.7–12.7 dBm; 24.150–24.250 GHz | Analog I/Q with built-in IF pre-amp (conversion gain 27 dB) | **FCC UXS-IPS354** (§15.249 per datasheet; Modular Approval Letter in filing), ISED RSS-310 | $60.30 / **$49.20** / RFQ | 925 stock, 16 wk, Active; THT header 44×30×8.3 mm; 5 V 48 mA; −30…+60 °C | **BACKUP PICK** | [Digi-Key](https://www.digikey.com/en/products/result?keywords=80.00000356), [datasheet](https://media.digikey.com/pdf/Data%20Sheets/InnoSenT/200730_Data%20Sheet_IPS-354_V1.5.pdf), [FCC](https://fccid.io/UXS-IPS354) |
| InnoSenT IPS-937 (80.00000358) | Analog radar | — | — | Analog | — | $113.88 / $96.59 @54 | 115 stock | Too expensive | [Digi-Key](https://www.digikey.com/en/products/detail/innosent-gmbh/80-00000358/10416543) |
| InnoSenT IMD-2000 (80.00000451) | FMCW, digital target list | — | **±28.4 km/h max** ✘ | UART 256 kBd | FCC UXS-IMD-2000 (§15.245) | $61.27 / $50.02 | 342 stock | **Fails speed** | [Digi-Key](https://www.digikey.com/en/products/detail/innosent-gmbh/80-00000451/15991042), [datasheet](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7183/IMD-2000%20Datasheet%20v1.10.20241007130246134.pdf) |
| InnoSenT IPM-165 / IPM-365_F | 1T/1R, single channel (no direction) | wide | CW | Analog | FCC UXS-IPM165 / UXS-IPM165F (§15.245) | — / — / $8.59 @1k | **NRND** (Mar 2022 notice), not stocked | Dead end | [Digi-Key](https://www.digikey.com/en/products/detail/innosent-gmbh/80-00000062/10482982), [FCC manual](https://fcc.report/FCC-ID/UXS-IPM165/2119950.pdf) |
| RFbeam **K-MC4** | 1T/**2R**, I/Q on both (monopulse → azimuth) | 30°×12° (RX 40°×12°) | IF 15 Hz–300 kHz, 20 dB IF gain; EIRP +16…+20 dBm | Analog I/Q ×2 (4 ADC ch) | **FCC 2ASYV-K-MC4**, **IC 24358-KMC4**, CE | **RFQ** (sibling K-MC1 is $269.91 @1) | Active; **98×78×7 mm**; 140 mA | Strong RF, but large and expensive; vendor-diverse alternate | [RFbeam](https://rfbeam.ch/product/k-mc4-radar-transceiver/), [FCC](https://fccid.io/2ASYV-K-MC4), [datasheet](https://rfbeam.ch/download/k-mc4-datasheet/) |
| RFbeam K-MC1 (K-MC1-RFB-00D) | 1T/1R I/Q, high-gain | narrow | — | Analog | FCC (per RFbeam list) | $269.91 / $226.39 @30 | 13 stock, Active | Too expensive | [Digi-Key](https://www.digikey.com/en/products/detail/rfbeam-microwave-gmbh/K-MC1-RFB-00D/13151975), [RFbeam list](https://rfbeam.ch/products/) |
| RFbeam K-LC6 (K-LC6-RFB-00D) | 1T/1R, I/Q | 80°×12° | FMCW/FSK capable | Analog | **CE only, no FCC** | $57.51 / $46.86 / RFQ | 17 stock, 2 wk, Active (PCN-2026-01) | Needs own FCC cert | [Digi-Key](https://www.digikey.com/en/products/detail/rfbeam-microwave-gmbh/K-LC6-RFB-00D/10638895), [RFbeam](https://rfbeam.ch/product/k-lc6-radar-transceiver/) |
| RFbeam K-LC7 (K-LC7-RFB-00H) | 1T/2R, I/Q | 80°×34° | IF 0–50 MHz; EIRP 12 dBm | Analog | **CE only** | $62.84 / $50.50 / RFQ | 49 stock, 2 wk, Active (SMD -01H on request) | Needs own FCC cert | [Digi-Key](https://www.digikey.com/en/products/detail/rfbeam-microwave-gmbh/K-LC7-RFB-00H/10638901), [RFbeam](https://rfbeam.ch/product/k-lc7-radar-transceiver/) |
| RFbeam K-LD7 | Digital FMCW/FSK | — | ~62 mph ceiling (per OpenFlight) ✘ | UART | FCC | — | Active | **Fails speed** | [RFbeam list](https://rfbeam.ch/products/), [OpenFlight](https://github.com/open-flight/openflight) |
| RFbeam K-MD7-RFB-00H-02 | Digital tracking | — | — | UART | CE only | $212.68 | Active | Expensive, no FCC | [Digi-Key list](https://www.digikey.com/en/products/result?keywords=80.00000356) |
| RFbeam V-LD1 | 61 GHz distance sensor | — | Distance, not Doppler speed | Digital | FCC | — | Active | Wrong function | [RFbeam list](https://rfbeam.ch/products/) |
| **OmniPreSense OPS243-A** (OPS243-A-CW-RP) | 1T/1R I/Q + on-board FFT | **20°×24°** | 20 kS/s → 62 m/s; **30 kS/s → ~93 m/s (OpenFlight)**; 50 kS/s → 155 m/s | **USB / UART / RS-232**, speed reports + raw I/Q | **FCC 2ALLL243A** (24.089–24.161 GHz), FCC/IC + CE modular per vendor | **$224** / ~$227–236 (sibling OPS243-C @25–50) / **not published** (broker RFQ table $135 @1k, unverified) | Backorder at OmniPreSense; 0 at Digi-Key; Mouser 14 wk factory lead time | Great for prototyping, too expensive for production | [OmniPreSense](https://omnipresense.com/product/ops243-doppler-radar-sensor/), [Mouser](https://www.mouser.com/en/ProductDetail/OmniPreSense/OPS243-A-CW-RP?qs=T3oQrply3y%2B5pADMfiP69Q%3D%3D), [FCC](https://fccid.io/2ALLL243A), [manual](https://usermanual.wiki/OmniPreSense/243A-4525695.pdf), [broker](https://www.quarktwin.com/product-detail/omnipresense-ops243-a-cw-wb/13086264) |
| OmniPreSense OPS243-C | FMCW + Doppler | — | — | USB / WiFi | FCC | $244–264 / $227 @50 | 0 at Digi-Key | No advantage | [Digi-Key RP](https://www.digikey.com/en/products/detail/omnipresense/OPS243-C-FC-RP/13145285), [Digi-Key WB](https://www.digikey.com/en/products/detail/omnipresense/OPS243-C-FC-WB/14675869) |
| Infineon **BGT24LTR11N16** (chip) | 1T/1R I/Q MMIC | Your own antenna | CW, fine | Analog I/Q | **None. Needs your own §15.245/15.249 + ISED + RED** | $9.94 / $4.95 / $4.19 @500; **$3.63 @3k reel** | 1,317 stock, Active | Gen-2 cost-down only (saves about $10/head but costs $10–20k+ to certify, plus RF design) | [Digi-Key](https://www.digikey.com/en/products/detail/infineon-technologies/BGT24LTR11N16E6327XTSA1/6599555) |
| Hi-Link HLK-LD2451 | 1T/2R FMCW | ±15° | **0–120 km/h** (33 m/s) per vendor sheet ✘ | UART | "FCC compliant" claim, **no FCC ID found** | $6.08 / — / $5.33 (Alibaba) | — | **Fails speed and cert** | [Alibaba](https://www.alibaba.com/product-detail/Hi-Link-100m-1T2R-24G-Motor_1601275750366.html), [Hi-Link](https://hilink.ltd/index.php?id=1282&cateid=768) |
| Hi-Link HLK-LD2410 | Presence FMCW | — | Presence only ✘ | UART | — | ~$3.20 | — | Fails | [Hi-Link](https://www.hlktech.net/index.php?id=988) |
| Silicon Radar (24 GHz TRX chips) | Chips only | — | — | Analog | None | Not verified | — | Same issue as BGT24 (own cert); not researched further | — |

**Key takeaways**
- Only five relevant 24 GHz parts carry a reusable FCC grant and can cover 90 m/s: InnoSenT **SMR-3x3**, **IPS-354**, RFbeam **K-MC4**, RFbeam **K-MC1**, and OmniPreSense **OPS243-A**. The SMR-333 is the cheapest of these by 3–15×.
- InnoSenT's SMR and IPS parts transmit **only at 24.150–24.250 GHz**. That satisfies the France and UK "upper-band" constraint and fits inside §15.249 (24.0–24.25 GHz) and the EU 24.05–24.25 GHz band. EIRP is ≤12.7 dBm, which is the §15.249 field-strength limit (250 mV/m @3 m ≈ 12.7 dBm EIRP).
- **Fixed-function digital modules (IMD-2000, K-LD7, HLK) all fail the 90 m/s requirement.** They are tuned for people and vehicles.

---

## 3. 60 GHz single-chip options, for completeness

**Regulatory reality (FCC 23-35, effective 23 Aug 2023, §15.255)**
- For indoor field-disturbance sensors in 57–64 GHz the general rule is **14 dBm peak EIRP with ≥25.5 ms of off-time in every 33 ms window (≤23% duty)**.
- Alternatively, 20 dBm is allowed in 57–61.56 GHz at 50% duty, or **3 dBm peak with no duty limit**.
- So continuous CW Doppler at 60 GHz is legal only at about 3 dBm. A duty-cycled radar can miss or truncate a 20–30 ms club approach.

Sources: [FCC 23-35](https://docs.fcc.gov/public/attachments/FCC-23-35A1.pdf), [FCC TCB slides Oct 2023](https://www.fcc.gov/sites/default/files/31-Part-15.255-Rules-Amendment-TCB_Oct_2023.pdf), [Federal Register](https://www.federalregister.gov/documents/2023/07/24/2023-15367/fcc-empowers-short-range-radars-in-the-60-ghz-band).

| Option | TX/RX | 90 m/s? | Price | Certification | Source |
|---|---|---|---|---|---|
| TI **IWR6843AOP** (IWR6843ARQGALP) | 3T/4R AoP, C674x DSP | **Yes**: 1-TX chirp T_c ≈ 9.6 µs → v_max ≈ 129 m/s (calc in research/05) | Chip: $52.73 @1 (Digi-Key); TI ≈ $25.36 @1ku (search snippet). EVM: $187.74 | **No module grant found.** The TI EVM is FCC-certified only as an EVM. Mistral sells a "pre-certified" AoP module at about $109 (old page) / AoPCB $175, with no FCC ID published. Joybien BM501 price and cert not published. | [Digi-Key chip](https://www.digikey.com/en/products/result?keywords=IWR6843ARQGALP), [TI](https://www.ti.com/product/IWR6843AOP/part-details/IWR6843ARQGALP), [EVM](https://www.digikey.com/en/products/detail/texas-instruments/IWR6843AOPEVM/12165115), [Mistral](https://mistralsolutions.com/product/60ghz-aopcb-module/), [Mistral AoP](https://test1.mistralsolutions.com/product/60ghz-indl-aop-module/), [Joybien](http://www.joybien.com/product/P_mmWave(BM501).html), [TI E2E](https://e2e.ti.com/support/sensors-group/sensors/f/sensors-forum/1287327/iwr6843aop-does-fcc-modular-certification-already-exist-for-this-chip) |
| TI **IWRL6432AOP** | 2T/3R AoP, M4F + HWA | **Marginal**: real-only IF, 5 MHz IF BW | Non-AOP IWRL6432 chips $19.70–25.50 @1. AOP chip not listed at Digi-Key (≈$16 @1k per earlier research snippet). EVM $191.40 | No module grant found | [Digi-Key](https://www.digikey.com/en/products/result?keywords=IWRL6432AOP) |
| Infineon **BGT60TR13C** | 1T/3R AoP, needs host MCU | FMCW **marginal (≈77 m/s)**; CW mode exists but hits §15.255 limits | Chip $18.01 @1 → $12.29 @4.5k (0 stock, 26 wk). DEMO board $231.26 | Infineon "form factor module" **FCC 2AYSQ-6011, Limited Single Modular**, 61.0–61.5 GHz, not sold as a production module | [Digi-Key chip](https://www.digikey.com/en/products/detail/infineon-technologies/BGT60TR13CE6327XUMA1/13282953), [FCC](https://fccid.io/2AYSQ-6011), [demo](https://www.digikey.com/en/products/detail/infineon-technologies/DEMOBGT60TR13CTOBO1/16580764) |
| Acconeer **XM125** (A121 pulsed-coherent) | 1T/1R | **Probably** (high sweep rate) but frames are short and SNR on a ball is low; untested | $22.20 @1, $17.57 @100, **$16.49 @500**. 0 stock (84 past due). A121 chip ≈ $6.49 @3k | A121 **FCC 2AQ6KA1201, Limited Single Modular** (tested on XS121 ref board; host must run spurious-emission tests). XM125 has a CE DoC; IC 24388-A121 (unverified) | [Digi-Key XM125](https://www.digikey.com/en/products/detail/acconeer-ab/XM125/17883267), [FCC A121](https://fccid.io/2AQ6KA1201), [XM125 datasheet](https://www.mouser.com/datasheet/2/1126/XM125_datasheet-3133248.pdf), [Digi-Key A121](https://www.digikey.com/en/products/detail/acconeer-ab/A121-001-T-R/17883300) |

**Verdict on 60 GHz: not for v1.**
- Duty-cycle and EIRP rules work against continuous trigger watching.
- There are no full single-modular grants, only "limited" ones that need host testing.
- Chip and module costs are equal or higher, and the DSP work is much larger.
- Keep the IWR6843AOP in the lab for a possible outdoor flight-tracking or angle sensor in v2, which already appears in the plan's dev-kit list.

---

## 4. IF chain and ADC, needed because SMR-333/IPS-354 output analog I/Q

| Function | Choice | Why |
|---|---|---|
| IF amp + band-pass | **TI TLV9064IPWR** quad RRIO op-amp, one per head (I and Q × 2 stages). AC-coupled HPF at about 150–300 Hz (rejects golfer body motion <1–2 m/s). Gain about 40 dB total. 2-pole LPF at about 25 kHz. | 10 MHz GBW is plenty for 40 dB at 25 kHz. Op-amp noise is about 10 nV/√Hz, far below the module's about 0.67 µV/√Hz output noise. Cost $0.93 @1k. |
| ADC | **TI ADS131M02IPWR**, one per head. 2-ch **simultaneous** ΔΣ, 24-bit, up to 64 kS/s, internal PGA ×1–128, SPI. | I/Q simultaneous sampling with no skew. The ΔΣ decimation filter makes anti-alias design trivial. 24-bit range absorbs strong body/club returns. $2.53 @1k, in stock. The 4-ch ADS131M04 ($3.85 reel) would save one part but is **0 stock until Mar 2027**. |
| Radar MCU | **TI MSPM0G3507SRHBR** (M0+ 80 MHz, 2× 12-bit 4 MS/s ADCs, 32 KB SRAM) | Runs the always-on trigger detector (band-energy IIR on the rear head, about 1 ms latency) and timestamps samples. Streams raw I/Q (4 ch × 64 kS/s × 16-bit ≈ 512 KB/s) over SPI/UART to the host, where the S-curve fit runs as a **separate radar process**. In stock, $1.34 @3k. It also gives a **cost-down path**: drop both ADS131M02s and use its internal simultaneous ADC pair with hardware oversampling (saves about $5/unit, at the cost of 12-bit dynamic range). |
| MCU alternate | ST STM32G431CBU6 (M4F + FPU, dual simultaneous ADCs) | Better DSP headroom, but **0 stock, 52-week lead time** at Digi-Key, so it is not the primary. |
| Head supply | **TI TPS7A2033PDBVR**, one per head | The SMR needs 3.2–3.4 V. Low-noise LDO (≈7 µVrms) keeps supply ripple out of the IF. |

---

## 5. PRODUCTION BOM: radar subsystem (per unit), the centerpiece

Architecture: **2 radar heads** (SMR-333 + TLV9064 + ADS131M02 + LDO on a small 4-layer FR-4 board each, mounted at the two boresight angles in §1) + radar MCU (on the main board or a small carrier) + 2 cables.

| Item | Manufacturer | MPN | Vendor | URL | Qty/unit | $@1 | $@100 | $@1k | $@10k | Stock/lead | Lifecycle | Certification | Notes/alternates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 24 GHz CW I/Q radar module (rear/trigger head + down-range/speed head) | InnoSenT | **80.00000346 (SMR-333)** | Digi-Key 2191-80.00000346CT/TR-ND | https://www.digikey.com/en/products/detail/innosent-gmbh/80-00000346/10419768 | **2** | 19.10 | 15.10 | **13.80** (900 reel) | ~11.50 est. (RFQ to InnoSenT) | 2,125 in stock; 16 wk | Active | **FCC UXS-SMR3X3 (modular), IC 6902A-SMR3X3, TELEC R219-247202, ETSI EN 300 440**; 24.150–24.250 GHz | Backup: IPS-354 (§6). Cost-down: one SMR-313 wide-beam head (validate in EVT). Mount the 116° plane horizontal. |
| IF amplifier / band-pass (4 amps per head) | Texas Instruments | **TLV9064IPWR** | Digi-Key | https://www.digikey.com/en/products/result?keywords=TLV9064IPWR | 2 | 1.73 | 1.03 | 0.93 | ~0.80 est. | **0 stock**; 2,000 due 5 Nov 2026; 20 wk | Active | n/a | Alt: 2× TLV9062 per head, or AD8619 ($4.45, in stock) |
| I/Q ADC, 2-ch simultaneous, 24-bit, 64 kS/s | Texas Instruments | **ADS131M02IPWR** | Digi-Key | https://www.digikey.com/en/products/result?keywords=ADS131M02IPWR | 2 | 4.51 | 2.84 | 2.53 | 2.43 (4k reel) | 3,708 in stock; 20 wk | Active | n/a | Alt: 1× ADS131M04IPWR ($3.85 reel, 0 stock until Mar 2027); or MSPM0 internal ADCs (−$5) |
| Radar MCU (trigger detection, capture, stream to host) | Texas Instruments | **MSPM0G3507SRHBR** | Digi-Key | https://www.digikey.com/en/products/result?keywords=MSPM0G3507SRHBR | 1 | 2.59 | 1.57 | 1.43 (500) | 1.34 (3k reel) | 7,477 in stock; 20 wk | Active | n/a | Alt: STM32G431CBU6 ($3.88 @100; 0 stock, 52 wk): https://www.digikey.com/en/products/detail/stmicroelectronics/STM32G431CBU6/10231569 |
| Low-noise 3.3 V LDO (one per head) | Texas Instruments | **TPS7A2033PDBVR** | Digi-Key | https://www.digikey.com/en/products/result?keywords=TPS7A2033PDBVR | 2 | 0.35 | 0.19 | 0.16 | 0.15 (3k reel) | 0 stock; 3,000 due late Nov 2026; 26 wk | Active | n/a | Any ≤10 µVrms 3.3 V LDO with ±3% accuracy |
| Head-to-MCU cable, 6-pos 1.0 mm, 152 mm | JST | **A06SR06SR30K152A** | Digi-Key 455-3003-ND | https://www.digikey.com/en/products/result?keywords=A06SR06SR30K152A | 2 | 1.83 | 1.32 | 1.12 | ~0.90 est. | 4,996 in stock; 8 wk | Active | n/a | Signals: 5V/3V3, GND, SPI (SCLK, MOSI/MISO, CS), DRDY. If the rear head mounts on the main PCB, one cable is saved. Check "reversed" pinout. |
| Mating header, 6-pos 1.0 mm SMD R/A | JST | **SM06B-SRSS-TB(LF)(SN)** | Digi-Key | https://www.digikey.com/en/products/detail/jst-sales-america-inc/SM06B-SRSS-TB/926712 | 4 | 0.68 | ~0.45 est. | ~0.35 est. | ~0.25 est. | Stock not shown | Active | n/a | Breaks at 100+ not shown on the fetched page |
| Radar head PCB, 4-layer FR-4, ~25×30 mm | (EMS/PCB fab) | custom | — | — (estimate, not quoted) | 2 | ~5.00 est. | ~1.20 est. | ~0.70 est. | ~0.45 est. | — | — | — | Standard FR-4 is fine because the RF stays inside the module. Ground pour under the module per InnoSenT footprint. Head may be vertical (perpendicular to main board) to get the 116° plane horizontal. |
| Passives (RC filters, AC-coupling, decoupling, ~30 parts/unit) | various | — | — | — (estimate) | 1 lot | ~1.00 est. | ~0.40 est. | ~0.30 est. | ~0.25 est. | — | — | — | Use C0G for filter capacitors |
| **Radome / radar windows** | (enclosure) | — | — | — | 2 windows | $0 incremental (part of enclosure tool) | — | — | — | — | — | — | **Polycarbonate (εr ≈ 2.8–3.0, low tan δ) or ABS.** Use either a **thin wall ≤0.8 mm** or a **λ_g/2 wall ≈ 3.6–3.7 mm** (12.39 mm / (2√εr)). Put the module ≈ λ₀/2 = 6.2 mm (or a multiple) behind the wall. **No metallic/metal-flake paint, no carbon-loaded "radar-black", no ITO/AR-coated glass** in front of the heads. Keep radar windows separate from camera IR windows. Verify loss (<1 dB) in EVT. |
| **SUBTOTAL, radar subsystem** | | | | | | **≈ $61.35 + PCBs ≈ $71.35** | **≈ $47.10** | **≈ $41.60** | **≈ $35 est.** | | | | |

Notes on the subtotal:
- @1k it is about 2×13.80 + 2×0.93 + 2×2.53 + 1.43 + 2×0.16 + 2×1.12 + 4×0.35 + 2×0.70 + 0.30 ≈ **$41.6**.
- The cost-down variant (one SMR-313 head, MSPM0 internal ADC, no cable) is about **$17–18 @1k**. Validate it in EVT before committing.

---

## 6. BACKUP BOM (same architecture, different module)

| Item | Manufacturer | MPN | Vendor | URL | Qty/unit | $@1 | $@100 | $@1k | $@10k | Stock/lead | Lifecycle | Certification | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 24 GHz CW I/Q module with IF pre-amp | InnoSenT | **80.00000356 (IPS-354)** | Digi-Key 2191-80.00000356-ND | https://www.digikey.com/en/products/result?keywords=80.00000356 | 2 | 60.30 | 49.20 | RFQ (~$42 est.) | RFQ | 925 in stock; 16 wk | Active | **FCC UXS-IPS354** (modular, §15.249 per datasheet), ISED RSS-310 | 5 V, 48 mA, IF DC–60 kHz, 45°×38°, 44×30×8.3 mm on a 2.54 mm header. Same op-amp/ADC/MCU chain; op-amp gain can drop about 20 dB. Op temp only −30…+60 °C. |
| IF / ADC / MCU / LDO / cables / headers / PCBs / passives | as §5 | as §5 | | | | ≈ 33 | ≈ 17 | ≈ 14 | ≈ 12 est. | | | | |
| **Backup subtotal** | | | | | | **≈ $154** | **≈ $115** | **≈ $98 est.** | RFQ | | | | |

**Vendor-diverse alternate:** RFbeam **K-MC4** (FCC 2ASYV-K-MC4 / IC 24358-KMC4). It is 1T2R I/Q monopulse, which adds azimuth. Price is RFQ, probably $150–250 judging by the K-MC1. It is 98×78×7 mm. Use it only if InnoSenT supply fails.

**"Buy, not build" fallback:** OPS243-A, one per unit. Point it down-range and accept that the club approach is outside its 20° beam. Trigger from cameras or sound, as [OpenFlight](https://github.com/open-flight/openflight) does.

---

## 7. Low-cost question: is OPS243-A too expensive at volume?

**Yes.**
- Authorized pricing is **$224 @1** from both [OmniPreSense](https://omnipresense.com/product/ops243-doppler-radar-sensor/) and [Mouser](https://www.mouser.com/en/ProductDetail/OmniPreSense/OPS243-A-CW-RP?qs=T3oQrply3y%2B5pADMfiP69Q%3D%3D).
- The shop shows no volume tiers. Digi-Key's breaks on the sibling OPS243-C fall only about 7% by 50 pcs ([Digi-Key](https://www.digikey.com/en/products/detail/omnipresense/OPS243-C-FC-RP/13145285)).
- The only 1k figure found is an unauthorized broker's auto-generated RFQ table: **$135 @1k** ([Quarktwin](https://www.quarktwin.com/product-detail/omnipresense-ops243-a-cw-wb/13086264)). Treat it as unverified. A realistic OEM price is probably **$120–170**, and that needs an RFQ.
- It also draws 1.5 W, measures 75×90×12 mm, and has a single 20°×24° beam.

**Cheapest credible trigger + speed path**
- 2× SMR-333 + 2× ADS131M02 + MSPM0: **about $42 @1k**.
- 1× SMR-313 (wide beam) + MSPM0 internal ADC: **about $17–18 @1k**. That is roughly 7–9× cheaper than the OPS243-A, with the same "reuse a modular grant" certification story.
- The extra engineering is about 2–4 engineer-weeks of analog front-end and DSP work. The S-curve fit and FFT tracking can borrow from OpenFlight's OPS243 raw-I/Q pipeline.
- Below about $15 you need a bare BGT24LTR11 ($3.63 @3k) with your own antenna. That brings a new §15.245/15.249 + ISED + RED radio test (**about $10–20k**, 6–10 weeks) plus RF layout risk. It is only worth it above roughly 20–50k units/yr.

---

## 8. Certification path and cost

| Path | What you do | Est. cost / time |
|---|---|---|
| **Module grant reuse (recommended: SMR-333 or IPS-354)** | **US:** label the host "Contains FCC ID: UXS-SMR3X3". Run the Part 15B SDoC (needed anyway for the digital device), plus KDB 996369 host-integration checks (radiated spurious emissions with the radar on). Two co-located SMR heads plus WiFi/BT need a **simultaneous-transmission / co-location evaluation**. Avoid it by time-multiplexing the heads (rear head on until trigger, forward head on from impact). **Canada:** "Contains IC: 6902A-SMR3X3" + ICES-003. **EU/UK:** no modular approval exists under RED. Include the module in the product DoC using InnoSenT's EN 300 440 report, and test the host to EN 300 440 (spot), EN 301 489-1/-3, and EN 62311/EN IEC 62479. | **≈ $2–5k incremental (US/CA)** and **≈ $3–6k incremental (RED/UKCA)** on top of camera-only compliance, est. About 2–4 weeks. Well below the plan's "+$15–30k with radar" allowance. |
| New intentional-radiator cert (BGT24 chip-down, K-LC6/K-LC7, any uncertified module) | Full §15.245 or §15.249 test report + TCB grant + ISED RSS-310 + full EN 300 440 | **≈ $10–20k (FCC) + $3–6k (ISED) + RED radio testing**, 6–10 weeks, plus redesign risk |
| 60 GHz limited-modular (A121/XM125, Infineon 2AYSQ-6011) | Host must reproduce the tested configuration and run spurious tests. §15.255 duty limits apply. | More than the 24 GHz modular path; not recommended |

**Before PO, verify on the FCC EAS** (our fetcher was blocked by the FCC site and fcc.report):
- that UXS-SMR3X3 is a full *Single* Modular Approval and not a *Limited* one; the filing includes a "ModularApprovalLetter" and other OEMs such as the KONE KSP 1028-L reuse it;
- the exact rule part. The 2017 manual says §15.249 and the V2.4 datasheet says §15.245. Either is fine.

---

## 9. Risks and open items

1. **Patent: trigger and sanity check.**
   - Rapsodo's patent covers radar tracking that *triggers a camera and combines data* (to 2039). Our radar never feeds the camera estimator, but **counsel should clear the trigger use specifically**.
   - Mitigation: give the cameras a self-sufficient rolling-buffer/image trigger and treat the radar as a power/wake hint plus an independent readout.
   - Never auto-calibrate either sensor from the other; TrackMan's radar-camera calibration patent runs to 2041.
   - Cosine correction must use radar-only S-curve fitting.
2. **Ball SNR at 3 m with the SMR-333** is about 10–19 dB per FFT bin. Validate in EVT against the IPS-354 (≥7 dB better) and the OPS243-A. Dimpled-ball RCS and dimple scintillation are unmeasured.
3. **Two-head mutual interference.** The two free-running oscillators (24.15–24.25 GHz, temperature drift of about −400 kHz/°C) can beat inside the 0–32 kHz IF if their frequencies cross. Mitigations:
   - time-multiplex using the enable pins (TX −30 dB);
   - mount the heads back-to-back for isolation;
   - or use the single SMR-313 head.
4. **SMR-333 beam-plane orientation.** Confirm from the datasheet pattern plots which footprint axis is 43° and which is 116°. The heads may need vertical sub-boards.
5. **Supply.**
   - TLV9064, TPS7A2033 and ADS131M04 are currently out of stock at Digi-Key (restocks due Nov 2026 / Mar 2027). Alternates are listed.
   - STM32G431 has a 52-week lead time, which is why the MSPM0G3507 is primary.
   - InnoSenT lead time is 16 weeks. Place a 1k-unit reel PO early and get a 10k quote.
6. **Lifecycle.**
   - InnoSenT IPM-165/365 went NRND in 2022. SMR-3x3 is Active, but ask InnoSenT for a longevity statement.
   - RFbeam has PCN-2026-01 open on the K-LC6/K-LC7.
7. **Environmental.** IPS-354 (backup) is rated only to +60 °C. A black enclosure in sun on a range could exceed that. SMR-333 is rated to +85 °C.
8. **Floor multipath and golfer motion.** The rear head sees legs, hands and shaft at 1–20 m/s (0.16–3.2 kHz). The trigger must look for a Doppler line accelerating above about 25 m/s (>4 kHz), not raw energy.

---

## 10. Prototype order list (EVT)

| Item | MPN | Price | Source |
|---|---|---|---|
| SMR-333 ×10 | 80.00000346 | $16.79 @10 | https://www.digikey.com/en/products/detail/innosent-gmbh/80-00000346/10419768 |
| IPS-354 ×4 | 80.00000356 | $55.68 @5 | https://www.digikey.com/en/products/result?keywords=80.00000356 |
| OPS243-A ×1 (golf reference, OpenFlight code) | OPS243-A-CW-RP | $224 | https://omnipresense.com/product/ops243-doppler-radar-sensor/ |
| ADS131M02 ×10 | ADS131M02IPWR | $3.42 @10 | https://www.digikey.com/en/products/result?keywords=ADS131M02IPWR |
| MSPM0G3507 LaunchPad | LP-MSPM0G3507 | $23.36 | https://www.digikey.com/en/products/result?keywords=MSPM0G3507SRHBR |
| (optional) TI IWR6843AOPEVM for v2 angle/flight work | IWR6843AOPEVM | $187.74 | https://www.digikey.com/en/products/detail/texas-instruments/IWR6843AOPEVM/12165115 |

---

## Sources (all fetched or searched on 7 Oct 2026)
- InnoSenT: [SMR-333 Digi-Key](https://www.digikey.com/en/products/detail/innosent-gmbh/80-00000346/10419768) · [SMR-3x3 datasheet V2.4](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7183/2191_SMR-313%20%26%20SMR-333%20Data%20Sheet%20V2.4.20241007125146397.pdf) · [SMR-333 page](https://www.innosent.de/en/sensors/smr-333/) · [FCC UXS-SMR3X3](https://fccid.io/UXS-SMR-3X3) · [fcc.report SMR3X3](https://fcc.report/FCC-ID/UXS-SMR3X3) · [SMR-334 Digi-Key](https://www.digikey.com/en/products/result?keywords=80.00000347) · [IPS-354 Digi-Key](https://www.digikey.com/en/products/result?keywords=80.00000356) · [IPS-354 datasheet](https://media.digikey.com/pdf/Data%20Sheets/InnoSenT/200730_Data%20Sheet_IPS-354_V1.5.pdf) · [IPS-354 page](https://www.innosent.de/en/sensors/ips-354/) · [FCC UXS-IPS354](https://fccid.io/UXS-IPS354) · [IPS-937](https://www.digikey.com/en/products/detail/innosent-gmbh/80-00000358/10416543) · [IMD-2000](https://www.digikey.com/en/products/detail/innosent-gmbh/80-00000451/15991042) · [IPM-165/365](https://www.digikey.com/en/products/detail/innosent-gmbh/80-00000062/10482982) · [IPM-165 FCC manual](https://fcc.report/FCC-ID/UXS-IPM165/2119950.pdf)
- RFbeam: [products](https://rfbeam.ch/products/) · [K-MC4](https://rfbeam.ch/product/k-mc4-radar-transceiver/) · [K-MC4 FCC](https://fccid.io/2ASYV-K-MC4) · [K-LC6 Digi-Key](https://www.digikey.com/en/products/detail/rfbeam-microwave-gmbh/K-LC6-RFB-00D/10638895) · [K-LC7 Digi-Key](https://www.digikey.com/en/products/detail/rfbeam-microwave-gmbh/K-LC7-RFB-00H/10638901) · [K-MC1 Digi-Key](https://www.digikey.com/en/products/detail/rfbeam-microwave-gmbh/K-MC1-RFB-00D/13151975) · [K-LC6 page](https://rfbeam.ch/product/k-lc6-radar-transceiver/) · [K-LC7 page](https://rfbeam.ch/product/k-lc7-radar-transceiver/)
- OmniPreSense: [OPS243-A](https://omnipresense.com/product/ops243-doppler-radar-sensor/) · [Mouser](https://www.mouser.com/en/ProductDetail/OmniPreSense/OPS243-A-CW-RP?qs=T3oQrply3y%2B5pADMfiP69Q%3D%3D) · [FCC 2ALLL243A](https://fccid.io/2ALLL243A) · [UM-003 manual](https://usermanual.wiki/OmniPreSense/243A-4525695.pdf) · [OpenFlight](https://github.com/open-flight/openflight) · [Quarktwin broker](https://www.quarktwin.com/product-detail/omnipresense-ops243-a-cw-wb/13086264)
- Chips / 60 GHz: [BGT24LTR11](https://www.digikey.com/en/products/detail/infineon-technologies/BGT24LTR11N16E6327XTSA1/6599555) · [IWR6843ARQGALP](https://www.digikey.com/en/products/result?keywords=IWR6843ARQGALP) · [IWR6843AOPEVM](https://www.digikey.com/en/products/detail/texas-instruments/IWR6843AOPEVM/12165115) · [IWRL6432](https://www.digikey.com/en/products/result?keywords=IWRL6432AOP) · [BGT60TR13C](https://www.digikey.com/en/products/detail/infineon-technologies/BGT60TR13CE6327XUMA1/13282953) · [FCC 2AYSQ-6011](https://fccid.io/2AYSQ-6011) · [XM125](https://www.digikey.com/en/products/detail/acconeer-ab/XM125/17883267) · [FCC 2AQ6KA1201](https://fccid.io/2AQ6KA1201) · [Mistral](https://mistralsolutions.com/product/60ghz-aopcb-module/) · [Joybien](http://www.joybien.com/product/P_mmWave(BM501).html) · [FCC 23-35](https://docs.fcc.gov/public/attachments/FCC-23-35A1.pdf) · [FCC TCB slides](https://www.fcc.gov/sites/default/files/31-Part-15.255-Rules-Amendment-TCB_Oct_2023.pdf)
- Hi-Link: [HLK-LD2451 Alibaba](https://www.alibaba.com/product-detail/Hi-Link-100m-1T2R-24G-Motor_1601275750366.html) · [Hi-Link](https://hilink.ltd/index.php?id=1282&cateid=768)
- Support parts: [TLV9064IPWR](https://www.digikey.com/en/products/result?keywords=TLV9064IPWR) · [ADS131M02IPWR](https://www.digikey.com/en/products/result?keywords=ADS131M02IPWR) · [ADS131M04IPWR](https://www.digikey.com/en/products/result?keywords=ADS131M04IPWR) · [MSPM0G3507SRHBR](https://www.digikey.com/en/products/result?keywords=MSPM0G3507SRHBR) · [STM32G431CBU6](https://www.digikey.com/en/products/detail/stmicroelectronics/STM32G431CBU6/10231569) · [TPS7A2033PDBVR](https://www.digikey.com/en/products/result?keywords=TPS7A2033PDBVR) · [JST A06SR06SR30K152A](https://www.digikey.com/en/products/result?keywords=A06SR06SR30K152A) · [JST SM06B-SRSS-TB](https://www.digikey.com/en/products/detail/jst-sales-america-inc/SM06B-SRSS-TB/926712)
