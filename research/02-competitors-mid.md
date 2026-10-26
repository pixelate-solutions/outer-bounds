# 02: Mid-Tier Launch Monitor Competitors ($1,500–$7,000 street)

**Research date:** 7 October 2026.
**Scope:** portable and semi-portable launch monitors selling for roughly $1,500–$7,000 street. A few products just outside that band are noted because they shape what buyers in it expect.

**How to read the citations**
- Every number has a URL next to it.
- Items marked **‡** come from a research sub-agent's reading of the cited page. I did not re-fetch those pages myself. Treat them as likely but not double-checked.
- Unmarked items I fetched or searched directly this session.
- **⚠** marks conflicts between sources or open uncertainty.

**Coverage limits**
- The shared web-search budget (200 per turn) ran out partway through. All later work used WebFetch against known URLs.
- fccid.io, fcc.report and the FCC's own EAS database all blocked automated access (Cloudflare or Akamai 403). FCC details therefore come from search-indexed snippets and forum posts that link the filings. I could not open any internal-photo PDF myself.
- MyGolfSpy and GolfWRX also returned 403. Their lab and forum data are missing.

---

## 0. TL;DR

1. **Every portable unit in this band that gives face-angle-class club data needs a club sticker, or is radar that needs marked balls indoors.**
   - GC3 and Bushnell Launch Pro: a face dot, and they don't report face angle at all.
   - Garmin R50: a face sticker.
   - Uneekor EYE MINI: a toe sticker, and no face angle.
   - Square Golf Omni: two stickers per club, and face angle and dynamic loft are only *estimated*.
   - The only markerless camera units with club data are ceiling-mounted: ProTee VX ($6,500), Uneekor EYE XR ($5,999, 4 club metrics only) and TruGolf Apogee ($7,995). None is portable or usable outdoors.
   - Radar units such as the Full Swing KIT ($4,999) and FlightScope Mevo Gen2/Mevo+ get face and path without stickers. But they need 16–20 ft of depth indoors. The Mevo also needs metallic dots or RCT balls for reliable indoor spin.
   - **No product in the band offers portable, markerless, measured face angle, dynamic loft and impact location, indoors and outdoors.**
2. **Prices collapsed in 2025–2026.**
   - The floor of "real" camera data fell to $1,599 (Square Omni) and $1,699 (new Foresight GC2, ball-only).
   - FlightScope's radar plus camera fusion fell to $1,299 (Mevo Gen2).
   - The SkyTrak ST MAX is on sale at $1,695. The EYE MINI was cut to $2,999 and the EYE MINI LITE to $1,999.
   - The $3k–$5k middle is now defended mainly by Bushnell Launch Pro ($2,999.99), Garmin R50 ($4,999.99) and Full Swing KIT ($4,999).
3. **Subscriptions are getting more aggressive, not less.**
   - On 18 Sept 2026 Foresight replaced its perpetual FSX licences with **Foresight+**: Silver $199/yr, Gold $599/yr, plus Course Pass $295–$595/yr.
   - Bushnell Launch Pro owners now need at least Silver for club data, and Gold for GSPro. That is about $849/yr including GSPro's own $250.
   - Uneekor needs Pro ($199/yr) for any third-party simulator.
   - Subscription-free players are FlightScope (one-time add-ons), Square, ProTee, Full Swing (optional $99.99/yr) and TruGolf (E6 bundled but closed to GSPro).
4. **The gap:** a portable side-of-ball or down-the-line unit at **$2,000–$3,500** with:
   - markerless, *measured* full club delivery (path, face, face-to-path, dynamic loft, attack angle, impact location);
   - no subscription;
   - an open simulator API;
   - real indoor and outdoor parity.

   Nobody ships this. The nearest is Square Omni at $1,599 with stickers and estimated face and loft. The next nearest are ceiling units at $6k–$8k. Section 3 covers what such a product would do to the tier.

---

## 1. Master comparison table

| Product | Street price (Oct 2026) | Sensing | Placement | Club data, and markers required | Spin | Recurring fees | GSPro |
|---|---|---|---|---|---|---|---|
| FlightScope **Mevo Gen2** (2025) | $1,299 [FS](https://flightscope.com/products/mevo-gen2) | 24 GHz Doppler + 1 camera ("Fusion") | Behind ball, 7–9 ft; 16 ft+ total indoors | Base: club speed, AoA. Pro Package ($1,000): path, face, face-to-path, dynamic loft. FIL ($499): impact. **No stickers.** | Indoors needs metallic dot stickers or RCT balls | None ($0) | Yes |
| FlightScope **Mevo+** (2020; discontinued) | $1,099 clearance (reg. $2,299) [FS](https://flightscope.com/products/mevo-plus) | Same as Gen2 | Same | Same add-ons | Same | None | Yes |
| **Square Golf Omni** (2026) | $1,599 [Square](https://www.squaregolf.com/) | 4 IR cameras, photometric | Side of ball | Path, AoA, speed, impact measured. Face and dynamic loft *estimated*. **2 stickers per club** (shaft + face) | Optical, any ball | None (credits for native courses) | Yes, no Square fee |
| **Foresight GC2** (all-new, 2026) | $1,699 [Foresight](https://www.foresightsports.com/products/gc2) | 2 cameras | Side | **None (ball only)** | Optical | Foresight+ after 30-day trial | Gold needed ($599/yr) |
| **SkyTrak ST MAX** (late 2025) / ST+ | $1,695 sale (reg. $2,995) [SkyTrak](https://www.skytrakgolf.com/pages/skytrak-st-max) | Photometric camera + "dual Doppler radar" | Side, about 18 in | Speed, path, face, face-to-path. **No AoA** (⚠ disputed). No stickers | Optical | $0–$599.99/yr for courses | **Not officially supported** |
| **Uneekor EYE MINI LITE** | $1,999 (from $2,750) [Uneekor](https://uneekor.com/en-us/products/eye-mini-lite-standalone) | 2 IR cameras | Side/front, about 16 in | Speed, path, AoA, smash only. **Toe sticker required** | Optical (dimples), any ball | Pro $199/yr needed for third-party sims | With Pro |
| **Uneekor EYE MINI** | $2,999 (from $4,500) [Uneekor](https://uneekor.com/en-us/products/eye-mini-standalone) | 2 IR cameras | Same | Same 4 metrics; sticker | Optical | Same | With Pro |
| **Bushnell Launch Pro** (Circle B) | $2,999.99 [Bushnell via search](https://www.bushnellgolf.com/products/launch-pro) | 3 cameras + IR (= GC3) | Side, about 2 ft | Speed, smash, path, AoA. **Face dot sticker.** **Silver $199/yr required** | Optical, any ball | Silver $199 / Gold $599 | Gold + GSPro ($849/yr) |
| **TruGolf LaunchBox** (2026) | $2,999 [SI](https://www.si.com/golf/gear/5-golf-launch-monitors-excited-2026) | Camera + IR | ⚠ not published | ⚠ metrics not published; "no marked clubs" | Optical | None (E6 Connect with 27 courses included) | **No (E6 only)** |
| **Foresight GC3S** | $3,299–$3,799 ‡; "leaving the line" ‡ | 3 cameras + IR | Side | 4 metrics; dot sticker | Optical | Subscription after year 1 | Gold |
| **Full Swing KIT** | $4,999 list [Full Swing](https://www.fullswinggolf.com/kit/); $3,999 at some retailers ‡ | 24 GHz "dual-mode ML" radar; camera for video only | Behind, 8–10 ft; 16–20 ft total indoors | Speed, path, face, face-to-path, AoA, smash. No stickers. **No dynamic loft, no impact** | Radar (RCT balls recommended indoors) | Optional Premium $99.99/yr | Yes |
| **Garmin Approach R50** | $4,999.99 [Garmin PR](https://www.garmin.com/en-US/newsroom/press-release/outdoor/meet-the-garmin-approach-r50-the-only-portable-golf-launch-monitor-with-a-built-in-simulator/) | 3 cameras, no radar | Side, 1.5 ft | Speed, path, face, face-to-path, AoA. **Face sticker required** | Optical, any ball | Garmin Golf $99.99/yr for Home Tee Hero only | Yes (Windows PC) |
| **Uneekor EYE XR** (overhead) | $5,999 [Top Shelf](https://topshelfgolf.com/blogs/golf/uneekor-eye-xr-review) | 2 IR cameras, ceiling behind golfer | Ceiling | Speed, path, smash, face (face *derived*). **No stickers** ("Club AI") | Optical | Uneekor tiers | With Pro |
| **ProTee VX** (overhead, 2023) | $6,500 [Indoor Golf Shop](https://shopindoorgolf.com/products/protee-vx-launch-monitor) | 2 high-speed cameras + AI | Ceiling, 9 ft min | Full: path, face, face-to-path, AoA, dynamic loft, lie, impact. **No stickers** | Optical, any ball | **None** | Yes |
| **Foresight GC3** | $6,999 [Foresight](https://www.foresightsports.com/products/gc3) | 3 cameras + IR | Side | 4 metrics; dot sticker | Optical | Foresight+ after 30-day trial (new units) | Gold |
| **TruGolf Apogee** (overhead) | $7,995 sale (reg. $9,000) [TruGolf](https://shop.trugolf.com/products/apogee-by-trugolf) | Camera, ceiling | Ceiling | Speed, AoA, face, path markerless. **Stickers needed for dynamic loft and lie** | Optical | E6 ENJOY bundled | ⚠ not mentioned |
| *Foresight Falcon (overhead)* | *$16,999 [Foresight](https://www.foresightsports.com/products/foresight-falcon-launch-monitor). Out of band* | 4 cameras | Ceiling | Full GCQuad set; stickers | Optical | Foresight+ | Gold |

**Out of band, for context**
- **Below:**
  - Rapsodo MLM2PRO: $699.99, on sale at $549.99 ([Rapsodo](https://rapsodo.com/)).
  - Rapsodo **MLM2XPRO**: $899.99, announced Oct 2026 ([Rapsodo](https://rapsodo.com/products/mlm2xpro-golf-launch-monitor-simulator)).
  - Square Home Edition: $699 ([Square](https://www.squaregolf.com/)).
  - Garmin R10: about $599 ([Hit The Pin](https://www.hitthepin.com/articles/garmin-approach-r50-review-2026)).
  - Uneekor EYE MINI CORE: $1,249, Amazon only ‡ ([Amazon](https://www.amazon.com/MINI-CORE-Launch-Monitor-Simulator/dp/B0FPHVNCQ7)).
- **Above:** GCQuad $15,999, QuadMAX $19,999 ([Foresight](https://www.foresightsports.com/products/gc3)); Uneekor EYE XO2 $10,999 ([Top Shelf](https://topshelfgolf.com/blogs/golf/uneekor-launch-monitors-compared)).
- **Golfzon has no product in this band.** Its home simulators start at **$21,300** ([golfzongolf.com](https://golfzongolf.com/)).

---

## 2. Product-by-product

### 2.1 FlightScope Mevo+ (incl. 2023 edition, Pro Package, FIL, Fusion Tracking) and Mevo Gen2

**Status and price**

| Item | Detail | Source |
|---|---|---|
| Launch | Shipped about Feb 2020. FCC grant 2019-12-13 | ‡ [GSF](https://golfsimulatorforum.com/forum/flightscope/275027-mevo-rating) |
| Launch price | ⚠ Not verified. Later list price was $2,299 | — |
| Current | **Discontinued**, "final sales phase", **$1,099** (regular $2,299). FlightScope promises long-term support | [FlightScope](https://flightscope.com/products/mevo-plus) |
| Discontinued | 2025 | [SimLab](https://simlab.golf/reviews/flightscope-mevo-gen2/) |

- **2023 edition:** the only stated changes are longer battery life (up to about 3 h, from about 1.5 h ‡) and an upgraded kickstand ([MyGolfSimulator](https://mygolfsimulator.com/mevo-plus-pro-package-fusion-tracking-update/); ‡ [Breaking Eighty](https://breakingeighty.com/flightscope-mevo-plus-review)).
- **Successor, Mevo Gen2:**
  - $1,299, no subscription, 6 h USB-C battery, 1.1 lb ([FlightScope](https://flightscope.com/products/mevo-gen2)).
  - Same Fusion engine as the Mevo+ and the $15k X3C ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/flightscope-mevo-gen2-review)).
  - Launched Aug 2025 ‡ ([FlightScope PGA Show post](https://flightscope.com/blogs/news/flightscope-to-showcase-industry-leading-technology-at-2026-pga-show)).
  - MyGolfSpy "Staff Pick… Best Personal Launch Monitor of 2025", per FlightScope's own page ([FlightScope](https://flightscope.com/products/mevo-gen2)).

**Technology**

- **Radar**
  - 24 GHz K-band 3D Doppler.
    - Mevo+: FCC ID **QXP-LJ361** ([GSF teardown thread](https://golfsimulatorforum.com/forum/flightscope/277362-mevo-teardown)).
    - Mevo Gen2: FCC ID **QXP-SK878**, **24.083–24.168 GHz, §15.245** Field Disturbance Sensor, application listed 2025-03-24 (search snippet of [fccid.io/QXP-SK878](https://fccid.io/QXP-SK878)).
    - The original Mevo, QXP-A7310, used 24.075–24.175 GHz plus 2.404–2.478 GHz ([fccid.io](https://fccid.io/QXP-A7310)).
  - Exact LJ361 band: ⚠ not retrievable because fccid.io blocked access. ‡ The agent read it as 24.080–24.160 GHz.
  - Antennas: **four receive antennas**, a forum reading of the FCC internal photos ([Golf Simulator Advisor](https://golfsimulatoradvisor.com/mevo-plus-data-parameters/); [GSF](https://golfsimulatorforum.com/forum/flightscope/275027-mevo-rating)).
  - Not radar-diverse: a forum post notes that both the X3 (10 GHz) and the Mevo+ (24 GHz) are single radars with multiple receivers ([GSF spin thread](https://golfsimulatorforum.com/forum/flightscope/360576-mevo-spin-measured-vs-calculated)).
- **Camera:** one built-in "Fusion Tracking Camera" ([FlightScope Gen2](https://flightscope.com/products/mevo-gen2)).
  - Teardown posters describe the Mevo+ camera as slow.
  - It exposes an **MJPEG stream** on the unit's Linux network ports ([GSF teardown](https://golfsimulatorforum.com/forum/flightscope/277362-mevo-teardown)).
  - T5 Golf claims "dual 240fps cameras" on the Gen2 ([T5](https://t5golf.com/best-golf-launch-monitors-2026/)). ⚠ This contradicts FlightScope's one-camera diagram. Treat it as unreliable.
- **Fusion Tracking**
  - A patented blend of 3D Doppler with "synchronized image processing", first on the X3 and pushed free to all Mevo+ owners.
  - It "does not add more data points but increases the accuracy of existing ones", with the biggest gains on chips and wedges ([MyGolfSimulator](https://mygolfsimulator.com/mevo-plus-pro-package-fusion-tracking-update/); [Breaking Eighty via search](https://breakingeighty.com/flightscope-mevo-plus-review)).
  - FlightScope does not publish which metric comes from which sensor.
- **Trigger:** radar. There is no IR strobe.
- **Teardown / BOM hints:**
  - **Raspberry Pi**-based main board, a USB Wi-Fi dongle, and an off-the-shelf-style battery. It runs Linux ([GSF teardown](https://golfsimulatorforum.com/forum/flightscope/277362-mevo-teardown)).
  - No chip part numbers have been posted.
  - Internal photos: https://fccid.io/QXP-LJ361/Internal-Photos/Internal-Photos-4549449 (public since about mid-2020).

**Placement and space**
- Down-the-line behind the ball: 7–9 ft to the tee, plus at least 8 ft of ball flight indoors ([FlightScope Gen2](https://flightscope.com/products/mevo-gen2)).
- That is about **16 ft minimum**. Reviewers say 16 ft "feels tight" and suggest 25 ft or more ([FlightScope page review quote](https://flightscope.com/products/mevo-gen2)).
- Over 105 mph club speed, 9–10 ft behind the ball is advised. Minimum ceiling 8.5 ft ([SimLab](https://simlab.golf/reviews/flightscope-mevo-gen2/)).
- Fluorescent lights, fans and HVAC cause interference ([FlightScope](https://flightscope.com/products/mevo-gen2)).

**Metrics**
- **Base unit (claimed 20):** carry, roll, total, ball speed, club speed, smash, vertical and horizontal launch, spin rate, spin axis, apex, flight time, lateral landing, AoA, spin loft, dispersion, shot type, plus putting speed, distance and direction ([FlightScope](https://flightscope.com/products/mevo-gen2)).
- **Measured vs calculated:** FlightScope claims "no calculated estimates" without a per-metric split.
  - Golf Simulator Advisor lists these as radar-measured: ball speed, both launch angles, spin, spin axis, club speed and AoA.
  - It lists these as modelled: carry, roll, total, apex, flight time, descent and lateral.
  - It says dynamic loft "calculates… using a collision model" ([GSA](https://golfsimulatoradvisor.com/mevo-plus-data-parameters/)).
  - Carry and roll indoors are necessarily extrapolated from a few feet of flight.
- **Spin, how measured**
  - Radar Doppler modulation. FlightScope patent US9868044B2, discussed in [this GSF thread](https://golfsimulatorforum.com/forum/flightscope/360576-mevo-spin-measured-vs-calculated).
  - **Indoors, aluminium stickers or RCT balls are "required for accurate spin measurements."** 100 stickers come in the box ([FlightScope Gen2](https://flightscope.com/products/mevo-gen2)).
  - Users report that a single dot gave measured spin on only about 30–40% of shots in Short Indoors mode for one owner. When spin isn't caught, the unit falls back to an *estimated* value, shown in italics ([GSF](https://golfsimulatorforum.com/forum/flightscope/360576-mevo-spin-measured-vs-calculated)).
  - ⚠ Users dispute whether spin axis is ever truly measured indoors or is back-calculated from path, horizontal launch and AoA (same thread).
- **Pro Package**
  - One-time **$1,000**, launched Jan 2022, unlocked by licence key ([MyGolfSimulator](https://mygolfsimulator.com/mevo-plus-pro-package-fusion-tracking-update/)). It was on sale at $699 at one point ‡.
  - Adds 11 parameters: club path, face to path, face to target, dynamic loft, vertical and horizontal swing plane, low point, vertical descent angle, curve, and club speed and acceleration profiles ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/flightscope-mevo-gen2-review)).
- **Face Impact Location (FIL)**
  - One-time **$499** ([SimLab](https://simlab.golf/reviews/flightscope-mevo-gen2/)), $500 elsewhere.
  - Combines radar and image processing to place the strike toe/heel and high/low as heat maps, with no stickers ([MyGolfSimulator](https://mygolfsimulator.com/mevo-plus-pro-package-fusion-tracking-update/)).
  - Needs at least 300 lux ‡.
  - Pro Package + FIL bundle: **$1,499**. Gen2 fully loaded: **$2,798** ([SimLab](https://simlab.golf/reviews/flightscope-mevo-gen2/)).
- **Not offered by any FlightScope tier:** lie and closure rate ‡.
- **No club stickers needed for any club metric.** This is the Mevo's quiet advantage.

**Accuracy**

| Test | Result | Source |
|---|---|---|
| Gen2 vs TrackMan, indoor | About 7 in 10 shots within 1–2 yd carry and 200 rpm. The other 2–3 showed driver carry gaps of 5–7 yd and occasional spin errors up to 3,000 rpm. Driver horizontal launch inconsistent at minimum depth | [SimLab](https://simlab.golf/reviews/flightscope-mevo-gen2/) |
| Mevo+ vs TrackMan/GCQuad/EYE XO (unnamed "independent tests") | Ball speed ±1–2 mph, carry ±2–4 yd, total ±3–6 yd, launch ±1°. Spin "less accurate indoors" without dots | [MyGolfSimulator](https://mygolfsimulator.com/mevo-plus-accuracy/) — low rigour |
| FlightScope's own claim | "Within 1%" of GCQuad and TrackMan 4 | [FlightScope](https://flightscope.com/products/mevo-gen2) — vendor |

**Fees and software**
- No subscription. E6 Connect lifetime licence included: 8 courses on Gen2, 12 on Mevo+.
- Compatible with GSPro, Awesome Golf, Creative Golf and TGC 2019 ([FlightScope](https://flightscope.com/products/mevo-gen2); [PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/flightscope-mevo-gen2-review)).
- The unit creates its own Wi-Fi network.

**Outdoor, battery, left-handed**
- Outdoors with full flight, no dots are needed; this is radar's home turf.
- Battery: Mevo+ about 2.5–3 h; Gen2 6 h.
- Lefty: sits behind the ball, so handedness doesn't matter (inferred).

**Complaints**
- Space hungry; fussy alignment and leveling.
- App drops from "Ready" to "Connected" between shots; Wi-Fi password trailing-space bug.
- Putts under 3 ft missed; dated app; fewer E6 courses on Gen2 ([SimLab](https://simlab.golf/reviews/flightscope-mevo-gen2/); [PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/flightscope-mevo-gen2-review)).
- Expensive add-ons; the Mevo+ had a mini-USB port ‡.

---

### 2.2 Garmin Approach R50

**Launch and price**
- Announced **12 Nov 2024** at **$4,999.99**, available immediately ([Garmin press release](https://www.garmin.com/en-US/newsroom/press-release/outdoor/meet-the-garmin-approach-r50-the-only-portable-golf-launch-monitor-with-a-built-in-simulator/)).
- Still $4,999.99 in 2026 with no discount shown ([Top Shelf, May 2026](https://topshelfgolf.com/blogs/golf/garmin-approach-r50-review); [SimLab, July 2026](https://simlab.golf/reviews/garmin-r50/)). UK £4,299 ([Top Shelf via search](https://topshelfgolf.com/blogs/golf/garmin-approach-r50-review)).

**Technology**
- **Three high-speed cameras, no radar,** plus a barometer.
- 10" 1280×800 touchscreen that runs the simulator on-device, with HDMI out ([Garmin PR](https://www.garmin.com/en-US/newsroom/press-release/outdoor/meet-the-garmin-approach-r50-the-only-portable-golf-launch-monitor-with-a-built-in-simulator/); [Top Shelf](https://topshelfgolf.com/blogs/golf/garmin-approach-r50-review)).
- Cameras arranged horizontally ‡ ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/garmin-approach-r50-review)).
- Frame rate, IR illumination and trigger method are not published.
- The **owner's manual lists only "2.4 GHz @ 19.7 dBm"** as wireless spec, which confirms there is no radar emitter.
- IPX3; operating range −10 to 55 °C; up to 4 h battery ([R50 Owner's Manual](https://www8.garmin.com/manuals/webhelp/GUID-D31AA1A2-C026-46EB-9699-FA94F1E8AF0B/EN-US/Approach_R50_OM_EN-US.pdf)).
- About 9 lb; 16.5 × 10.6 × 7.5 in ([Top Shelf](https://topshelfgolf.com/blogs/golf/garmin-approach-r50-review)).
- ⚠ Some sites (ParPrecision, Cubical Golfer) wrongly call it radar.

**Placement and space** (all from the [manual](https://www8.garmin.com/manuals/webhelp/GUID-D31AA1A2-C026-46EB-9699-FA94F1E8AF0B/EN-US/Approach_R50_OM_EN-US.pdf) unless noted)
- "Approximately **1.5 ft (0.5 m) to the side** of the tee location," facing the tee, at about the same height. It self-compensates for an uneven surface.
- "The shape of the hitting area varies depending on whether club data is enabled."
- SimLab: 9 ft ceiling minimum; 8 ft depth for practice, 14 ft for full sim ([SimLab](https://simlab.golf/reviews/garmin-r50/)).
- Hitting zone about 70 sq in, per a reviewer estimate ([Plugged In Golf](https://pluggedingolf.com/garmin-approach-r50-launch-monitor-review/)).

**Metrics**
- **Ball:** ball speed, launch angle, launch direction, **spin rate and spin axis, both measured**, carry, total, deviation, apex.
- **Club:** club speed, path, AoA, face angle, face-to-path, smash ([Garmin PR](https://www.garmin.com/en-US/newsroom/press-release/outdoor/meet-the-garmin-approach-r50-the-only-portable-golf-launch-monitor-with-a-built-in-simulator/); [SimLab](https://simlab.golf/reviews/garmin-r50/)).
- **Not measured:** dynamic loft ([Top Shelf](https://topshelfgolf.com/blogs/golf/garmin-approach-r50-review)), impact location, lie, closure rate.
- **Stickers**
  - The manual says: "In order to track club data, you need to apply one of the included club stickers to the face… **top-center of the club face**." No putter club data. 250 stickers included ([Top Shelf](https://topshelfgolf.com/blogs/golf/garmin-approach-r50-review)).
  - Sunlight on the face "can reduce the visibility of the club sticker, which can cause no club metrics to be detected." Don't place it near white face decorations ([manual](https://www8.garmin.com/manuals/webhelp/GUID-D31AA1A2-C026-46EB-9699-FA94F1E8AF0B/EN-US/Approach_R50_OM_EN-US.pdf)).
- **Ball:** any ball. The manual advises "logos or markings facing the launch monitor, especially if the ball has a matte surface." Hit The Pin says RCT balls are recommended indoors ([Hit The Pin](https://www.hitthepin.com/articles/garmin-approach-r50-review-2026)). ⚠ That RCT claim is unofficial.

**Accuracy**
- vs GCQuad ([Plugged In Golf](https://pluggedingolf.com/garmin-approach-r50-launch-monitor-review/)):
  - Ball data "almost perfectly in line" (qualitative).
  - **Club data "hit and miss"**, with "numerous shots where the club data was not captured." AoA was the worst metric.
  - A TrackMan 4 reader saw a 7-iron AoA of −4° on TrackMan against −7.5° or steeper on the R50.
- vs GC3: within "a yard or two, a degree or two, a hundred-or-so RPM". Club data was missed on about 2/3 of shots when using Foresight stickers ‡ ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/garmin-approach-r50-review)).
- Driver and long clubs read short ([SimLab](https://simlab.golf/reviews/garmin-r50/)).

**Fees and software**
- **Garmin Golf $9.99/mo or $99.99/yr**, needed only for Home Tee Hero (43,000+ courses) and tournaments. Practice, data and impact video are free ([SimLab](https://simlab.golf/reviews/garmin-r50/); [Top Shelf](https://topshelfgolf.com/blogs/golf/garmin-approach-r50-review)).
- **Third party at launch:** GSPro, Awesome Golf, E6 Connect/Apex "coming soon" ([Garmin PR](https://www.garmin.com/en-US/newsroom/press-release/outdoor/meet-the-garmin-approach-r50-the-only-portable-golf-launch-monitor-with-a-built-in-simulator/)).
- **Now:** GSPro through a Windows PC over Wi-Fi with no Garmin fee; Awesome Golf licensed separately; E6 through a TruGolf workflow ([Top Shelf](https://topshelfgolf.com/blogs/golf/garmin-approach-r50-review)).
- ⚠ SimLab contradicts itself on GSPro.
- No public open API found.

**Outdoor, left-handed, complaints**
- **Outdoors:** works, but the manual warns that low sun facing the unit causes misreads, and that grass and divots obstruct the view.
- **Lefty:** there's a per-profile Handedness setting ([manual](https://www8.garmin.com/manuals/webhelp/GUID-D31AA1A2-C026-46EB-9699-FA94F1E8AF0B/EN-US/Approach_R50_OM_EN-US.pdf)), but the unit must move to the other side for mixed groups ([SimLab](https://simlab.golf/reviews/garmin-r50/)).
- **Complaints:**
  - Price; stickers; 4 h battery that shuts off soon after the low-battery warning.
  - IPX3 only; small hitting zone ([Plugged In](https://pluggedingolf.com/garmin-approach-r50-launch-monitor-review/)).
  - Club data reliability.
- **FCC:** Garmin's grantee code is **IPH** ([fccid.io company list](https://fccid.io/company/Garmin-International-Inc)). The R50's specific ID was **not found**. The manual says it is under Settings > Legal. The R10 is IPH-03985 ‡.

---

### 2.3 Bushnell Launch Pro (original → Circle B), LPi, and its unlock tiers

**History and price**

| When | Event | Source |
|---|---|---|
| 2021 | Launched alongside the GC3 on identical hardware after Vista brought Bushnell and Foresight under one parent | [Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review) |
| Aug 2022 | A reader reports $3,999. Fees in that era were cited as Basic $99 → $250/yr and Gold $800 → $700/yr (⚠ confusing; low confidence) | same, comments |
| Oct 2023 | One-time unlock option "ended" | [SimLab](https://simlab.golf/reviews/bushnell-launch-pro/) |
| Jan 2025 | Ball-only $1,999 vs club-data $3,499 ‡. The Launch Pro was then discontinued and replaced by the indoor-only **LPi** at $2,799 ‡ | [Breaking Eighty GC3s](https://breakingeighty.com/foresight-gc3s) ‡ |
| Nov 2025 | **Circle B Edition** relaunch: same hardware, orange back panel, new app, new pricing. Launched at $2,499 ‡ | [Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review) |
| Mid/late 2026 | **$2,999.99** on bushnellgolf.com; LPi $1,999.99 list. "About 3 weeks ago" PlayBetter updated to $2,999.99 | [search summary of bushnellgolf.com / PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/indepth-bushnell-launch-pro-review-should-you-buy) |
| Late Sept 2026 | LPi on sale at **$999** at Golf Galaxy and sold out at most retailers; probably being phased out | [Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review) |

- Canada: CAD $4,595 ([Bushnell Canada via search](https://www.bushnellgolfcanada.com/products/launch-pro)).
- Sold to US customers only. It must check in from the US every 45 days ‡ ([bushnellgolf.com](https://www.bushnellgolf.com/products/launch-pro)).

**Tiers: this has changed again**
- **Before 18 Sept 2026** ([Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review)):
  - Free: ball data on the built-in screen.
  - Silver **$199/yr**: all club data, Foresight app, FSX Pro, 5 FSX Play courses.
  - Gold **$499/yr**: adds 25 courses, FSX 2020, and third-party software (GSPro).
  - "No one-time unlock exists for the Launch Pro."
- ⚠ Bushnell's own software page still advertises **one-time club data at $1,500** within 14 days, then **$1,750** ([bushnellgolf.com](https://www.bushnellgolf.com/pages/launch-pro-how-to-purchase-software-packages)). It also still mentions "Basic" and "Full Unlock" tiers without prices. This page looks stale; verify before relying on it.
- **From 18 Sept 2026 (Foresight+)** ([plus.foresightsports.com](https://plus.foresightsports.com/); [PlayBetter guide](https://www.playbetter.com/blogs/golf-simulator-software/foresight-sports-subscriptions-guide-2026)):
  - **Free** $0: ball and club data views, 10-session history, no third-party access.
  - **Silver $199/yr**: unlimited history, drills, Course Pass eligible, and "**Club data on Bushnell Golf devices**". The PlayBetter guide puts it as "To unlock Club Data on the Bushnell Launch Pro, you must have at least the Silver Package."
  - **Gold $599/yr**: everything in Silver, plus video, profiles, and **third-party integrations**. GSPro still needs its own subscription.
  - **Course Pass** $295/yr (35 courses) or **Course Pass Pro** $595/yr (full library, 110–111 courses). Either requires Silver or Gold.
  - 30-day trial with a credit card. All plans billed annually, auto-renew, "sales are final."
- **Effective cost for a GSPro user:** Gold $599 + GSPro about $250 = **about $849/yr**.
  - Breaking Eighty's pre-change figure was about $750/yr ([Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review)).
  - SimLab's pre-change 3-year totals: $3,096 Silver, $3,996 Gold, $4,746 Gold + GSPro ([SimLab](https://simlab.golf/reviews/bushnell-launch-pro/)).

**Technology**
- The same three-camera "Triscopic" photometric unit as the GC3, plus IR, about 2 ft beside the ball ([SimLab](https://simlab.golf/reviews/bushnell-launch-pro/)). See 2.4 for the imaging method.
- 3 × 2 in transflective touchscreen.
- Wi-Fi (2.4 GHz only ‡), Ethernet, USB-C, **no Bluetooth** ([Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review)).

**Metrics**
- **Ball:** carry, ball speed, total spin, launch angle, horizontal launch angle, spin tilt axis, backspin, sidespin, with derived flight data.
- **Club (4):** club speed, smash, path, AoA ([SimLab](https://simlab.golf/reviews/bushnell-launch-pro/)).
- **No face angle, face-to-path, dynamic loft or impact location** ("No impact detection") ([Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review)).
- **Stickers:** club data needs a subscription plus the included club markers; "you need a sticker for club path" ([Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review)). 48 included; 192 for $49.99 ‡.
- **Balls:** no marked balls needed.

**Accuracy**
- Qualitative: "the most accurate launch monitor I own." It delivers about 98% of the QuadMAX experience, and range distances match a rangefinder ([Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review)).
- "Nearly identical shot after shot" to the GC3 ([SimLab](https://simlab.golf/reviews/bushnell-launch-pro/)).
- No published numeric deltas against TrackMan.

**Software:** Foresight Premier (new Windows sim), legacy FSX, GSPro with Gold. **No E6** and no mobile sim ([Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review)).

**Outdoor, battery, left-handed**
- Indoor and outdoor; battery 5–7 h ‡.
- Battery fails to recharge after fully dying in storage ([Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review)).
- Lefty: physically move it to the other side.

**Complaints**
- Subscription cost; no Bluetooth; dated screen that shows dashes for club data with no subscription.
- Hours-long first pairing ([SimLab](https://simlab.golf/reviews/bushnell-launch-pro/)).
- Five-year-old hardware; repeated SKU and price churn; US only.

---

### 2.4 Foresight GC3 and GC3S (plus the new GC2)

**Price and status**
- **GC3:** $6,999 MSRP ([Foresight](https://www.foresightsports.com/products/gc3)); UK £7,500 incl. VAT, £6,250 ex ([Foresight EU](https://foresightsports.eu/launch-monitors/gc3/)).
  - Introduced 2021 ([GolfMagic](https://www.golfmagic.com/equipment/buying-guides/best-launch-monitors)).
  - Launch price ⚠ not verified.
  - **New GC3s now ship with "30 days of Foresight+ Gold Membership with Course Pass Pro"** rather than the old lifetime FSX bundle ([Foresight](https://www.foresightsports.com/products/gc3)).
  - ⚠ It's unclear whether a post-18-Sept GC3 keeps any data functions after the trial beyond the Free tier. The Free tier does include ball and club data views on Foresight devices ([plus.foresightsports.com](https://plus.foresightsports.com/)).
- **GC3S:** announced about 7 Jan 2025 at **$3,799** with a Bushnell Pro X3 LINK rangefinder.
  - Same internals as the GC3. **Subscription of $500/yr after a free first year** ([Breaking Eighty](https://breakingeighty.com/foresight-gc3s)). UK £3,990 ([GolfMagic](https://www.golfmagic.com/equipment/buying-guides/best-launch-monitors)).
  - The "S" means **subscription**, not a different club-capture method. There is no hosel fiducial.
  - Reported "leaving the line" while stock lasts ‡ ([Top Shelf guide](https://topshelfgolf.com/pages/foresight-sports-complete-guide)).
- **GC2 (all-new, 2026):** $1,699, dual high-speed cameras, **ball data only** (14 metrics).
  - 123 sq in hitting zone, against 91.5 sq in for the GC3. 2.8" colour screen, 5–7 h battery, 4.5 lb.
  - **"Shipping Begins October 9."** 30-day Foresight+ trial ([Foresight GC2](https://www.foresightsports.com/products/gc2)).
  - Foresight is now competing directly at the low end of this band.

**Technology** (all from [Foresight EU](https://foresightsports.eu/launch-monitors/gc3/) unless noted)
- Three high-speed, high-resolution cameras ("Triscopic") plus "infrared object tracking."
- Captures "hundreds of images of the ball **within the first 30 cm** of ball flight" from three perspectives to build a 3D model.
- **Spin by "spherical correlation"** of the dimple pattern across frames, so spin rate and axis are measured directly and no marked balls are needed.
- Accelerometer for auto-level; barometer for altitude.
- Magnesium housing; 15.2 × 30.5 × 12.7 cm; 2.3 kg; hitting zone 17.8 × 25.4 cm.
- Battery 5–7 h; Wi-Fi, Ethernet, Bluetooth, USB-C.
- **Not published:** frame rate, camera baseline and arrangement, strobe timing, trigger.
  - T5 Golf calls it "stereoscopic cameras plus infrared emitters" and claims ±0.1 mph / ±25 rpm ([T5](https://t5golf.com/best-golf-launch-monitors-2026/)). ⚠ Those figures are unsourced; ignore them.

**Metrics**
- **Ball (measured):** ball speed, launch angle, side angle, total spin, side spin and spin axis. Carry and other flight values are calculated.
- **Club (4):** club head speed, smash ("efficiency"), path, AoA.
- **Face angle, loft and lie, impact location and closure rate are GCQuad, Falcon and QuadMAX only** ([Foresight EU](https://foresightsports.eu/launch-monitors/gc3/)).
- **Markers:** "1 dot data" ([Foresight EU](https://foresightsports.eu/launch-monitors/gc3/)). A small metallic dot on the clubface; "Club Markers" are in the box ([Foresight](https://www.foresightsports.com/products/gc3)). 192 included ‡.
  - Without the dot you get ball data only.
  - Even the GCQuad needs "a Club Feature licence and clubface markers" for full club and impact data ([GolfBays](https://golfbays.co.uk/blogs/news/new-golf-launch-monitors-2026)).

**Accuracy:** carry within 1–2% across driver, 6-iron and PW in Carl's Place testing, as cited by Rain or Shine ‡. I didn't reach the primary page.

**Software:** see the Foresight+ tiers in 2.3. GSPro needs Gold. Legacy FSX licences keep working ([PlayBetter guide](https://www.playbetter.com/blogs/golf-simulator-software/foresight-sports-subscriptions-guide-2026)).

**Lefty and complaints**
- Lefty: move the unit to the other side.
- Complaints: stickers; a thin club data set for $7k; random shutoffs ([Breaking Eighty](https://breakingeighty.com/bushnell-launch-pro-review)); naming confusion; subscription backlash after 18 Sept ‡ (thread URLs not captured).

**FCC**
- Foresight's grantee code is **2A6QA** ("WAWGD Newco LLC dba Foresight Sports"). Seen in a search snippet for [2A6QA-MACH2FSS](https://fccid.io/2A6QA-MACH2FSS), a 24 GHz baseball radar.
- ‡ The other 2A6QA ID is 2A6QA-JODYW263FSS: a re-ID'd **u-blox JODY-W263** Wi-Fi/BT module with a Pulse W3006 antenna, granted 13 Sep 2022.
- No GC3 or Launch Pro host filing was found. These products likely rely on the certified module plus Part 15B verification (inference).

---

### 2.5 Foresight Falcon (overhead): out of band, context only

- **Price:** **$16,999** ([Foresight](https://www.foresightsports.com/products/foresight-falcon-launch-monitor)); $15,999 at PlayBetter, March 2026 ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/foresight-sports-falcon-review)).
- **Launch:** released about 2025 ("last year", per the March 2026 review).
- **Technology:**
  - 4 cameras ("Quadrascopic"), ceiling mount 4 ft in front of the ball.
  - Ceiling ≥9.5 ft (10 ft ideal); about 14 ft room depth.
  - 59 × 28 in zone, but club data works only in **two 11 × 11 in corner squares**.
- **Club data:** full GCQuad set (face, loft, lie, impact, closure), and **stickers are still required** ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/foresight-sports-falcon-review)).
- **Relevance:** even Foresight's $17k overhead unit is not markerless.

---

### 2.6 Uneekor EYE MINI, EYE MINI LITE (+ EYE XR overhead)

**Price and launch**
- **EYE MINI:** launched early 2023 at **$4,500**; now **$2,999** ([SimLab](https://simlab.golf/reviews/uneekor-eye-mini/); [Uneekor](https://uneekor.com/en-us/products/eye-mini-standalone)).
- **EYE MINI LITE:** **$2,750** at launch (on sale by early 2024); now **$1,999** ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/uneekor-eye-mini-lite-review); [Uneekor](https://uneekor.com/en-us/products/eye-mini-lite-standalone)).
- **EYE XR (ceiling):** $5,999 ([Top Shelf](https://topshelfgolf.com/blogs/golf/uneekor-eye-xr-review)).
- **EYE MINI CORE:** $1,249, ball-only, Amazon-only, 2025 ‡.

**Technology**
- "2 High-speed photometric **infrared** cameras" ([Uneekor](https://uneekor.com/en-us/products/eye-mini-standalone)).
- The LITE manual carries an IEC "RISK GROUP 2 – IR emitted" warning ([LITE manual PDF](https://download.uneekor.com/docs/EYE_MINI_LITE_Manual.pdf)).
- Frame rate not published.
- "Dimple Optix" reads the dimples, so no marked balls are needed.
- **EYE MINI:** battery 5–8 h, e-ink display, Wi-Fi. Wi-Fi hotspot mode kills iPad internet; no Bluetooth ([SimLab](https://simlab.golf/reviews/uneekor-eye-mini/)).
- **LITE:** mains power + Ethernet only, PC required, indoor only ([Top Shelf](https://topshelfgolf.com/blogs/golf/uneekor-launch-monitors-compared)).
- **Certifications:** "KC, CE, FCC, VCCI", with no FCC ID printed in the manual. The LITE has no radio, so it is probably Part 15B (inference).

**Placement**
- "Sensor position: Front", meaning beside the ball facing the golfer.
- Ready zone **12" × 8"**, about **16" (40 cm)** from the unit, per the manual diagram ([LITE manual](https://download.uneekor.com/docs/EYE_MINI_LITE_Manual.pdf)).
- 9 ft ceiling ([SimLab](https://simlab.golf/reviews/uneekor-eye-mini/)).

**Metrics** ([Uneekor](https://uneekor.com/en-us/products/eye-mini-standalone))
- **Ball (15):** ball speed, launch, side angle, back spin, side spin, spin axis, flight type, carry, run, total, apex, distance to apex, flight time, descent, side total.
- **Club (4):** club speed, path, AoA, smash.
- **Explicitly not supported:** impact point, face angle, face-to-path, dynamic loft, lie.
- Ranges (LITE manual): back spin up to 12,000 rpm; ball speed 11–223 mph; putter 0.22–67 mph.

**Stickers: the manual is unambiguous**
- "Club stickers are **required** for the EYE MINI LITE to capture club data." Every club metric is listed as "Requires EYE MINI LITE Club Stickers."
- Placement by club ([LITE manual](https://download.uneekor.com/docs/EYE_MINI_LITE_Manual.pdf)):

| Club | Sticker position |
|---|---|
| Driver (8 grooves) | 1" from the toe edge, 5 grooves up |
| Driver (5 grooves) | 1" from the toe, on the 3rd groove |
| Woods and hybrids (5 grooves) | 1" in from the toe, level with the 3rd groove |
| Irons | Toe side of the face, 7 grooves up, on the smooth part of the face |

- 1,280 stickers come in the box.
- ⚠ Uneekor's product pages say "Stickers Recommended" or "Optional" ([Uneekor](https://uneekor.com/en-us/products/eye-mini-standalone)). That conflicts with its own manual.
- **EYE XR is the only sticker-free Uneekor ("Club AI").** It reports just 4 club metrics (speed, path, smash, face angle), and **face angle is "calculated… from ball and club data"** rather than imaged ([Top Shelf](https://topshelfgolf.com/blogs/golf/uneekor-eye-xr-review)).

**Accuracy**

| Test | Result | Source |
|---|---|---|
| EYE MINI vs GC3 | Ball data close. **Club speed sometimes 10–15 mph off**; smash occasionally too high | [SimLab](https://simlab.golf/reviews/uneekor-eye-mini/) |
| LITE vs GC3 | "Mathematically impossible" smash factors; path not matching start line; occasional wedge misreads | [PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/uneekor-eye-mini-lite-review) |
| LITE, user forum test, 7-iron | GCQuad 83.8/115.0 mph and 156.3 yd; TM4 84.0/115.3 and 158.1; LITE 81.5/107.3 and 152.3 (reads low) ‡ | [GSF](https://golfsimulatorforum.com/forum/golf-simulator-brands-and-types/uneekor-qed/418180-eye-mini-lite-users-ball-speed-and-clubhead-speed-accuracy) |
| Golf Laboratories robot test (Foresight-sponsored) | EYE MINI toe-strike club speed SD 10.4 mph ‡ | [Foresight blog](https://www.foresightsports.com/blogs/golf-tips/comparing-golf-launch-monitor-foresight-sports-gcquad-and-gc3-stand-above-the-rest) |

**Fees**
- Free Player tier: View software, range, data.
- **Pro $199/yr (needed for GSPro, E6 and TGC)**, Champion $399/yr, Ultimate $599/yr. 3-month Ultimate trial ([Uneekor](https://uneekor.com/en-us/products/eye-mini-standalone); [PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/uneekor-eye-mini-lite-review)).
- Legend was a $1,999 one-time option ([Indoor Golf Shop](https://shopindoorgolf.com/products/uneekor-eye-mini-launch-monitor)).
- GSPro adds its own $250/yr ([SimLab](https://simlab.golf/reviews/uneekor-eye-mini/)).

**Lefty and complaints**
- Lefty: side unit, presumably moved (not documented).
- Complaints: PC needed for first setup; stickers wear; club speed and smash errors; dated Refine graphics; name ("neither light nor mini").

**Patent note:** in Sept 2024 Foresight licensed patents "related to portable golf launch monitor screen technology" to Uneekor ([BusinessWire](https://www.businesswire.com/news/home/20240930838753/en/Foresight-Sports-and-Uneekor-Agree-on-License-of-Foresight-Sports-Patents-Related-to-Portable-Golf-Launch-Monitor-Screen-Technology)). **Foresight asserts IP in the portable side-camera space. Run a freedom-to-operate search before committing to a side-of-ball photometric design.**

---

### 2.7 SkyTrak+ and SkyTrak ST MAX

**Launch and price**
- **Original SkyTrak:** 2014, about $2,000.
- **SkyTrak+:** 2023 at **$2,995** ([Breaking Eighty](https://breakingeighty.com/skytrak-plus-review)). Now in closeout at $1,195–$1,995 (⚠ figures vary; [Northcourse](https://northcourse.golf/articles/skytrak-core-cost)). Certified pre-owned: $1,495 ([search summary](https://golfsimulatorvideos.com/skytrak-membership-plans/)).
- **ST MAX:** late 2025 at $2,995. **On sale at $1,695 "this week only"** with a free year of software ([SkyTrak](https://www.skytrakgolf.com/pages/skytrak-st-max)).
  - Breaking Eighty calls it "pretty much the exact same thing as the SkyTrak+": adds swing speed training, a second USB port and a faster processor ([Breaking Eighty](https://breakingeighty.com/skytrak-plus-review)).
- SkyTrak claims **"115,000 Units Sold and Counting"** ([skytrakgolf.com](https://skytrakgolf.com/)). GOLFTEC owns SkyTrak ‡.

**Technology**
- ST MAX: "**Dual Doppler Radar + Photometric Cameras**" ([SkyTrak ST MAX](https://www.skytrakgolf.com/pages/skytrak-st-max)).
- ST+: dual-Doppler plus camera, confirmed after a reader correction ([Breaking Eighty](https://breakingeighty.com/skytrak-plus-review)).
- Which metrics come from radar and which from camera is not published. The likely split is radar for club speed and path, camera for ball (inference).
- Radar band and channel count not published. No SkyTrak FCC ID found.
- Side-of-ball, about 18 in, with a laser dot for ball placement.

**Metrics**
- **Ball:** ball speed, launch, side angle, back spin, side spin, carry, total, descent, shot shape.
- **Club:** club speed, path, face angle, face-to-path.
- **⚠ No angle of attack**, an "odd omission" ([Breaking Eighty](https://breakingeighty.com/skytrak-plus-review)). Other sites claim AoA and dynamic loft ([Golf Simulator Nerd](https://www.golfsimulatornerd.com/blog/skytrak-plus-review-2026)); treat as unreliable.
- No impact location. **No stickers.**

**Accuracy**
- vs TrackMan: club speed, carry and spin in line; **side carry about double TrackMan's** ([Breaking Eighty](https://breakingeighty.com/skytrak-plus-review)).
- ‡ Golfible, ST+ vs TrackMan, 10 shots per club:
  - PW: ball speed +0.33 mph, carry −0.62 yd, spin −70 rpm.
  - 7-iron: −0.72 mph, −0.79 yd, −44 rpm.
  - Driver: +0.46 mph, +1.28 yd, −136 rpm.
  - Club path errors 0.6–1.7° ([Golfible](https://golfible.com/skytrak-plus-review/)).
- Struggles on grass and in bright light ([Golf Simulator Nerd](https://www.golfsimulatornerd.com/blog/skytrak-plus-review-2026)).

**Fees: prices are volatile and conflict across sources**
- SkyTrak's own site: **Elite $599.99/yr, Core (TrackMan) $349.99/yr** ([skytrakgolf.com](https://skytrakgolf.com/)).
- Northcourse (Aug–Oct 2026): Essential $99.99, Core Foresight $249.99–$299.99, Core TM $299.99–$349.99, Elite $499.99–$599.99. A 10% promo applies in Aug 2026 ([Northcourse](https://northcourse.golf/articles/skytrak-core-cost)).
- The free level (range plus ball and club data) never expires.

**Third party**
- **GSPro not officially supported.** It needs the community bridge OpenSkyPlus 2 (Windows).
- Official E6 and GSPro support "has ended for new customers" ([Breaking Eighty](https://breakingeighty.com/skytrak-plus-review); [Northcourse](https://northcourse.golf/articles/skytrak-core-cost)).
- **SkyTrak is a closed ecosystem now.**

**Complaints**
- Subscription needed for any sim; no AoA; weak on grass; no Bluetooth; iPad Wi-Fi hotspot issue; weak putting ([Breaking Eighty](https://breakingeighty.com/skytrak-plus-review)).

---

### 2.8 Full Swing KIT

**Launch and price**
- Late 2021, **$4,999**. Still $4,999 list ([Full Swing](https://www.fullswinggolf.com/kit/); [Breaking Eighty](https://breakingeighty.com/full-swing-kit-review)). Some retailers sell at $3,999 ‡.
- No successor found as of March 2026 ([Breaking Eighty](https://breakingeighty.com/full-swing-kit-review)).

**Technology**
- "**Patented, 24 GHz Dual-Mode, ML Enhanced Radar**" ([Full Swing specs](https://www.fullswinggolf.com/kit-specs/)).
- 1080p 60 fps camera **used only for swing video and alignment**, not measurement ([SimLab](https://simlab.golf/reviews/full-swing-kit/)).
- 5.3" OLED; dual-core A9; Wi-Fi ac; BT 5.0; 8,000 mAh, about 5 h ([Full Swing specs](https://www.fullswinggolf.com/kit-specs/)).
- Channel and antenna count not published.
- FCC grantee 2AY26 (registered March 2021) ‡; specific ID not found.

**Placement**
- Behind the ball, 8–10 ft, plus 8–10 ft of flight: **16–20 ft total indoors, "the most of any unit reviewed."** 9 ft ceiling ([SimLab](https://simlab.golf/reviews/full-swing-kit/); [Full Swing](https://www.fullswinggolf.com/kit/)).

**Metrics (16, all unlocked)**
- **Ball:** carry, total, spin rate, spin axis, launch, horizontal angle, ball speed, apex, side carry, side total.
- **Club:** club speed, smash, path, **face angle, face-to-path**, AoA ([Full Swing](https://www.fullswinggolf.com/kit/)).
- **No dynamic loft, no impact location, no lie.** No stickers.
- RCT balls recommended indoors ([SimLab](https://simlab.golf/reviews/full-swing-kit/)).

**Accuracy**
- **Outdoors:** "less than 1% variance across most clubs" vs TrackMan, in a test Full Swing hosted ([Breaking Eighty](https://breakingeighty.com/full-swing-kit-review)).
- **Indoors:** carry **4–7 yd shorter than the GC3 consistently** ([SimLab](https://simlab.golf/reviews/full-swing-kit/)). Commenters report 25–33% driver and 3-wood errors; the author "wouldn't recommend that one for indoor use" ([Breaking Eighty](https://breakingeighty.com/full-swing-kit-review)).

**Fees and software**
- Optional Premium **$99.99/yr** for video storage and history.
- GSPro supported. E6 mobile, 5 courses, included. Full Swing's own sim only in Studio packages from about $9.5k–$12k ([SimLab](https://simlab.golf/reviews/full-swing-kit/); [Breaking Eighty](https://breakingeighty.com/full-swing-kit-review)).

**Lefty and complaints**
- Lefty: behind the ball, so neutral.
- Complaints: OLED glare in sun; iOS-only app; no virtual range; space; indoor accuracy; one return dispute ([SimLab](https://simlab.golf/reviews/full-swing-kit/); [Breaking Eighty](https://breakingeighty.com/full-swing-kit-review)).

---

### 2.9 ProTee VX (correction: ceiling-mounted, so it fails our form-factor constraint)

- **Price:** **$6,500** with two free swing cameras ([Indoor Golf Shop](https://shopindoorgolf.com/products/protee-vx-launch-monitor)). "One of the most anticipated… releases of 2023."
- **Technology:** "Dual high speed camera systems", "machine vision and A.I. powered", ceiling mount, Dutch-made ([ProTee](https://proteegroup.com/)).
  - AI places "virtual tracking markers" on the clubhead ‡ ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/protee-vx-review)).
  - Frame rate and IR not published by ProTee.
- **Space:** ceiling ≥9 ft (2.75 m); hitting zone 25 × 21 in ([ProTee VX](https://proteegroup.com/the-power-of-vx/); [FAQ](https://proteegroup.com/faq/)). Indoor only.
- **Metrics, all markerless:** "No special golf balls, no club stickers" ([ProTee VX](https://proteegroup.com/the-power-of-vx/)).
  - **Ball:** speed, total, back and side spin, spin axis, launch angle and direction.
  - **Club:** speed, path, **face, face-to-path**, AoA, **dynamic loft, lie, vertical and horizontal impact**.
  - **Flight:** carry, total, apex, apex time, offline, air time, run, descent.
- **Fees:** **none**; ProTee Labs licence is perpetual ([FAQ](https://proteegroup.com/faq/)).
- **Software:**
  - GSPro direct.
  - E6 and Creative Golf may need a paid connector.
  - TGC 2019 support was discontinued spring 2025 ([Indoor Golf Shop](https://shopindoorgolf.com/products/protee-vx-launch-monitor)).
- **PC:** Windows, RTX 3060 minimum, USB 3.0.
- **Lefty:** switch "in seconds."
- **Accuracy:** no independent numbers found.
- **Relevance:** this is the existence proof that **markerless full club data is achievable with two cameras and ML at a $6.5k retail price.** It does it from above, though, where the camera sees the face and loft geometry far better than a side or DTL view does.

---

### 2.10 Square Golf Omni (and Home Edition)

**Price and launch**
- **Omni:** $1,599 ([Square](https://www.squaregolf.com/)). Shown at the Jan 2026 PGA Show; production reviews from June–July 2026 ([Breaking Eighty](https://breakingeighty.com/square-omni-launch-monitor)). Frequently sold out or backordered ([Rain or Shine](https://rainorshinegolf.com/products/square-golf-omni-launch-monitor)).
- **Home Edition:** $699, from late 2024.

**Technology** ([SimLab](https://simlab.golf/reviews/square-golf-omni/) unless noted)
- **Four high-speed cameras with IR illuminators in a vertical column**, recessed with no glass. The Home Edition has 2 cameras.
- Frame rate not published.
- Tilt sensor; auto-alignment from an alignment stick (±5°).
- **Swappable 14.4 V 5,000 mAh battery, 5–7 h; IP44.**
- Bluetooth; 2.4 lb; 1-second shot delay ([Rain or Shine](https://rainorshinegolf.com/products/square-golf-omni-launch-monitor)).

**Placement**
- Side or front of the ball; about 8 ft ceiling.
- Zone about 10 × 10 in for ball data, but **only the front half (about 5 × 5 in) for full club data and impact**.

**Metrics (21)**
- **Ball:** ball speed, launch, direction, total, back and side spin, spin axis, carry, total, descent, apex, hang time, side carry.
- **Club:** speed, smash, path, AoA, face, face-to-path, dynamic loft, impact location.
- **Stickers: two per club**, a reflective shaft sticker above the hosel and a dot top-centre on the face.
  - **Measured:** path, AoA, club speed, impact.
  - **Estimated:** face angle and dynamic loft ([SimLab](https://simlab.golf/reviews/square-golf-omni/); [Breaking Eighty](https://breakingeighty.com/square-omni-launch-monitor)).
  - Square's own page calls club markers "optional" ([Square OE](https://www.squaregolf.com/pages/launch-monitors-oe)). In practice they're needed for club data.
- **Balls:** any ball.

**Accuracy**
- **vs TrackMan, indoors:** ball speed "almost identical 90% of the time," spin usually within about 100 rpm and at most 300.
  - Example iron: carry 181.1 vs 180.6 yd; ball speed 119.3 vs 119.5 mph; spin 3,465 vs 3,597 rpm.
  - Driver noisier. Impact location gave 2–3 no-reads per 10 shots ([Breaking Eighty](https://breakingeighty.com/square-omni-launch-monitor)).
- **vs EYE XO and GC3:** carry within a couple of yards (about 5 yd on some drives), ball speed about 1 mph, spin about 200 rpm, grass equals mat ([SimLab](https://simlab.golf/reviews/square-golf-omni/)).

**Fees and software**
- **No subscription.** 1,000 credits included for native courses (1 per hole per player, about $20 per 1,000 more).
- GSPro, E6 Connect, Awesome Golf and Creative Golf with **no Square fee** ([Square software](https://www.squaregolf.com/pages/software); [SimLab](https://simlab.golf/reviews/square-golf-omni/)).

**Outdoor, left-handed, complaints**
- **Outdoors:** claimed on real turf. The ready indicator is hard to see in sun.
- **Lefty:** handedness toggle; side unit, so it moves.
- **Complaints:**
  - Two stickers per club; small 5 × 5 in club zone.
  - Weak native app and courses; impact location only in the PC app.
  - Poor screen; no case.
  - **Notoriously hard-to-reach support** ([Breaking Eighty](https://breakingeighty.com/square-omni-launch-monitor); [SimLab](https://simlab.golf/reviews/square-golf-omni/)).
- **Significance:** the Omni is the **price-performance disruptor** of 2026. It is the closest existing product to our spec, short on markerless, measured face and loft, and polish.

---

### 2.11 TruGolf LaunchBox and Apogee

- **LaunchBox (2026 PGA Show):**
  - **$2,999**; camera + infrared; on-board screen; about 4.5 h battery.
  - Indoor-focused, collects ball data outdoors on mats.
  - "You don't need marked clubs or specialty balls."
  - No annual fee; E6 Connect with 27 courses included.
  - **E6 only, no GSPro** ([SI](https://www.si.com/golf/gear/5-golf-launch-monitors-excited-2026); [Golfers Authority](https://shop.golfersauthority.com/blogs/golf/launch-monitors-to-buy-2026); [TruGolf](https://trugolf.com/)).
  - ⚠ Club metric list, camera count and placement are not published. Product pages returned 404.
  - **Worth watching:** it claims markerless club data at $2,999, but in a closed ecosystem with no independent tests yet.
- **Apogee:**
  - **$7,995** sale (regular $9,000), ceiling mount, 38 × 5.5 × 8 in, about 22 lb.
  - Ball: speed, back and side spin, launch and direction.
  - Club: speed, AoA, **face, path markerless**. **Stickers ($50 per 150) needed for dynamic loft and lie.**
  - E6 ENJOY bundled. GSPro not mentioned ([TruGolf shop](https://shop.trugolf.com/products/apogee-by-trugolf)).

### 2.12 Rapsodo (below band, but setting expectations)

- **MLM2PRO:**
  - $699.99, $549.99 on sale ([Rapsodo](https://rapsodo.com/)). Launched 2023 ‡.
  - Doppler radar (24 GHz @ 20 dBm per manual ‡) plus two cameras: 240 fps Impact Vision and Shot Vision.
  - **Spin measured only with RPT-marked balls.**
  - Club path and AoA "directly measured" since a May 2025 firmware update ([SimLab](https://simlab.golf/reviews/rapsodo-mlm2pro/)).
  - Premium $199/yr or $599.99 lifetime is required for spin and third-party sims.
- **MLM2XPRO:**
  - **$899.99**, announced Oct 2026, orders from 15 Oct ‡.
  - 8 measured metrics (club speed, ball speed, launch direction and angle, spin rate and axis **with RPT balls**, path, AoA).
  - Core $199.99/yr, Studios $399.99/yr ([Rapsodo MLM2XPRO](https://rapsodo.com/products/mlm2xpro-golf-launch-monitor-simulator)).
- **FCC grantee 2AH3O** (Rapsodo Pte Ltd): IDs 2AH3O-MLM2PRO and 2AH3O-MLM2XPRO, with internal photos listed ‡ ([fccid.io/2AH3O](https://fccid.io/2AH3O)).

### 2.13 Golfzon, Carl's Place, others

- **Golfzon:** nothing between $1.5k and $7k. Home simulators "Starting at $21,300" ([golfzongolf.com](https://golfzongolf.com/)).
- **Carl's Place:** a retailer and test source, not a hardware brand in this band.
- **Other 2026 launches, all below the band:**
  - Blue Tees Rainmaker: $599, radar.
  - Garmin Approach G82: $599.99.
  - Shot Scope LM1: $199.99.
  - Spectrum Element: sub-$1,500 photometric, "purportedly" coming.
  - Spica 3 / 3 Lite.
  - Sources: [SI](https://www.si.com/golf/gear/5-golf-launch-monitors-excited-2026); [search summary of GolfWRX thread](https://forums.golfwrx.com/topic/2080640-new-launch-monitors-for-2026/).
- **Open source, PiTrac:**
  - GPL-2.0 DIY photometric launch monitor on Raspberry Pi 5 with Pi cameras. Pis and cameras cost "roughly $250."
  - Measures ball speed, 3D launch and spin; works with GSPro and E6.
  - Self-described "really immature" ([GitHub](https://github.com/PiTracLM/PiTrac)).
  - The core photometric pipeline is commoditising. The moat is in club-face perception, accuracy validation and polish.

---

## 3. Synthesis

### 3.1 Why the winners win at their price

| Product | What sells it | What it gives up |
|---|---|---|
| **Bushnell Launch Pro** | GC3-grade ball data (spin measured from the dimples) at less than half the GC3's price. Foresight brand halo, plus the "most accurate I own" reviewer consensus | Monetised through unlock fees. Club data is thin (4 metrics, sticker, no face). Since Sept 2026, Silver $199 for club data and Gold $599 for GSPro. Effective 3-yr cost for a GSPro user about $5.5k |
| **Foresight GC3** | Same hardware with perpetual software (historically). Fitter credibility | $6,999; now also moving to Foresight+ |
| **Mevo Gen2 / Mevo+** | Radar is cheap and excels outdoors over full flight. One-time pricing; open to every sim. Club face, path and loft with no stickers via the Pro Package | Needs 16 ft+ indoors; metallic dots for indoor spin; flight extrapolated indoors; add-ons push it to about $2.8k |
| **Garmin R50** | All-in-one: 10" screen runs the simulator with no PC. Garmin brand and retail reach. Measured spin, any ball | $5k; stickers; club data reliability; 4 h battery |
| **SkyTrak+/ST MAX** | Cheapest photometric spin (115k units sold); simple; now $1,695 | Closed ecosystem (no official GSPro), subscription for any sim, no AoA |
| **Uneekor EYE MINI/LITE** | Dimple-reading photometric at $2k–$3k; big zone; impact video | Stickers; 4 club metrics; $199/yr for third-party; club speed errors |
| **Full Swing KIT** | Tiger and TGL halo; 16 unlocked metrics incl. face, no stickers; outdoor accuracy | Indoor weakness, 16–20 ft depth, $5k |
| **Square Omni** | Near-complete club list, 4 cameras, no subscription, free GSPro hook-up, $1,599 | Two stickers per club; face and loft estimated; tiny club zone; support and app quality |
| **ProTee VX** | Only true markerless full-club-data unit with no subscription and GSPro | Ceiling-only, indoor-only, $6.5k, PC tethered |

**Patterns**
1. **Ball data is now a commodity.** Measured spin on any ball costs $1,599 (Square), $1,695 (ST MAX) or $1,699 (GC2). Square Omni's spin is within about 100–300 rpm of TrackMan on good strikes. A ball-only unit or 4-metric club data cannot command $3k+ on its own anymore.
2. **The premium for club data is paid in stickers or space.**
   - Photometric side units read a high-contrast fiducial because the side view of a clubface is a poor imaging target. The face is nearly edge-on and moving at 100+ mph.
   - Radar units avoid stickers but need depth behind the ball, and they lose spin indoors without marked balls.
3. **Recurring revenue is how the incumbents defend margins.** Foresight/Bushnell, Uneekor, SkyTrak and Rapsodo all gate either club data or third-party simulators behind annual fees.
   - The September 2026 Foresight+ change made Bushnell's model more expensive: Gold rose from $499 to $599, and courses moved to separate Course Pass SKUs at $295–$595.
   - That creates a fresh grievance in the exact customer base we'd target. ‡ Forum backlash was reported; thread URLs not captured.
4. **Brands that removed fees won 2025–2026 mindshare.** Mevo Gen2 was "the story of the year" ([T5](https://t5golf.com/best-golf-launch-monitors-2026/)), and Square Omni was GolfMagic's best consumer monitor ([GolfMagic](https://www.golfmagic.com/equipment/buying-guides/best-launch-monitors)).

### 3.2 Where the gap is

The table below shows the most complete option at each price, setting aside ceiling units because they fail our form-factor constraint.

| Need | Cheapest product delivering it | Price |
|---|---|---|
| Measured spin, any ball, side unit | Square Omni / ST MAX / GC2 | $1.6k–$1.7k |
| Face angle + face-to-path, **no stickers**, portable | Mevo Gen2 + Pro Package (radar, 16 ft+, dots for indoor spin) | $2,299 (+$499 for impact) |
| Face, loft and impact on a **side camera** unit | Square Omni (**2 stickers**, face and loft estimated) | $1,599 |
| Face, loft and impact **measured** on a side camera unit | GCQuad (stickers + licence) | $15,999 |
| **Markerless** measured face, loft, lie, impact | ProTee VX (ceiling only) | $6,500 |
| **Markerless + portable side or DTL + indoor/outdoor parity + full club set + no subscription + open API** | **Nobody** | — |

**The gap, concretely:** a **$2,000–$3,500 portable unit** (side-of-ball or DTL) that:
- **measures**, not estimates, face angle, face-to-path, dynamic loft, spin loft, AoA, path and impact location, with **no stickers and no marked balls**;
- works in a **10–12 ft-deep room** and on a **grass range in sun**;
- ships with **no subscription** and an **open, documented simulator API** (GSPro connector, E6, Awesome Golf, plus a published local socket/HTTP protocol).

Secondary gaps nobody addresses well:
- **Hitting-zone generosity for club data.** Square's is 5 × 5 in; Falcon's is two 11 × 11 in corners.
- **Lefty and righty without moving the unit.** Only ceiling or behind-the-ball units manage it. A DTL camera or radar layout solves this for free.
- **Reliability and support reputation**, Square's weak point.
- **Outdoor sunlight robustness for optical units.** The R50 manual and Square reviews both flag it.
- **Low point and lie** are essentially absent below $6.5k.

### 3.3 What a markerless, subscription-free, full-club-data unit at about $2k–$3.5k would do to this tier

1. **It reprices the Bushnell Launch Pro to zero perceived value.**
   - **Bushnell Launch Pro:** $2,999.99 + $599/yr Gold (for GSPro) = **about $4.8k** over 3 years (excluding GSPro, which every buyer pays anyway). That buys 4 club metrics, sticker-based, and no face angle.
   - **A $2,999 unit with no fee** and 8+ markerless club metrics wins every reviewer comparison table on 3-year cost and metric count.
   - Expect Foresight to respond by bundling more into Silver or cutting LP hardware toward $1,999. They have a precedent: the LPi fell from $2,799 to $999 in under two years.
2. **It strands the Garmin R50 and Full Swing KIT at $5k.**
   - Both offer face and path. The R50 needs stickers and has unreliable club capture; the KIT needs 16–20 ft and is weak indoors.
   - Neither offers dynamic loft or impact.
   - Garmin will keep its all-in-one screen and retail channel, so its moat is distribution and on-device simulation, not data.
3. **It pressures Uneekor to move "Club AI" from the $5,999 ceiling XR down to the MINI line.** Uneekor already has the ML, though the XR's face angle is *derived*. Expect a "MINI 2" response within 12–18 months (speculative).
4. **Square Omni is the real competitor, and the main threat.**
   - At $1,599 it already gets about 80% of the spec, with stickers.
   - Square's obvious next step is removing the stickers via ML. Our differentiation must be **measured** face and loft (Square admits estimating them), a **larger club zone**, impact reliability better than Square's 70–80%, outdoor and sun robustness, and support quality.
   - If we price at $3,499 against a $1,599 Omni, the delta must be visible in reviewer TrackMan comparisons, especially face angle and AoA. Reviewers single these out as the failure points on R50 and Uneekor.
5. **It moves the "serious amateur" price anchor from $5k–$7k down to about $3k,** the way the Mevo Gen2 did for radar ($2,299 to $1,299) and Square did for photometric club data. That hurts GC3 ($6,999) and ProTee VX ($6,500) sales among home users. Fitters and coaches stay with GCQuad and TrackMan for brand trust.

**Recommended positioning (for discussion)**
- **Primary:** list at **$2,499–$2,999**.
  - Undercuts the LP Circle B on hardware and crushes it on total cost of ownership.
  - Leaves room above Square ($1,599) justified by markerless measured face, loft and impact.
  - Avoids the $3.5k+ zone where buyers start cross-shopping R50, KIT and used GCQuads.
- **Optional:** a ball-only or reduced-club SKU near $1,699 to block GC2 and ST MAX. But the brand promise ("no stickers, no subscription, open API") should be identical across SKUs, with no feature unlock fees. Unlock fees are the incumbents' most-hated trait.

**Execution risks surfaced by this research**
- **Club-face perception is the hard part.** Every sub-$7k side unit uses a fiducial or estimates. The only markerless face measurement below $15k is from ceiling vantage points (ProTee, Uneekor XR). A down-the-line camera sees the face better than a side camera. A side-of-ball unit may need an elevated or forward camera to see loft and face, or a radar plus camera fusion like FlightScope's for face and path.
- **Accuracy will be judged against TrackMan and GCQuad by Breaking Eighty, SimLab, Plugged In, Golfible and MyGolfSpy.** Their stated failure points for competitors are:
  - AoA bias (R50);
  - club speed outliers (Uneekor, 10–15 mph);
  - side carry and horizontal launch on driver (SkyTrak, Mevo);
  - indoor carry (KIT 4–7 yd short);
  - impact no-reads (Square 20–30%).

  Target those explicitly in validation.
- **Foresight IP.** Foresight has licensed patents on portable launch monitor technology to Uneekor (Sept 2024). Commission a freedom-to-operate review of Foresight, FlightScope (Fusion: US 10,338,209 ‡; spin: US9868044B2), TrackMan and Uneekor patents.
- **BOM reality check:**
  - The Mevo+ is a Raspberry Pi + USB Wi-Fi dongle + 24 GHz board ([GSF teardown](https://golfsimulatorforum.com/forum/flightscope/277362-mevo-teardown)).
  - PiTrac gets photometric ball data for about $250 in Pis and cameras ([GitHub](https://github.com/PiTracLM/PiTrac)).
  - Foresight uses an off-the-shelf u-blox JODY-W263 radio module ‡.
  - Hardware cost isn't the barrier at $2.5k retail. Perception software, calibration and support are.

---

## 4. Open gaps for a follow-up pass

1. FCC filings: open fccid.io in a real browser to pull frequency tables and internal photos for QXP-LJ361, QXP-SK878, 2AH3O-MLM2PRO and -MLM2XPRO. Find the R50's IPH ID (Settings > Legal on a unit), and SkyTrak, Square, Uneekor and Full Swing (2AY26) IDs.
2. MyGolfSpy 2025–2026 launch monitor lab rankings (blocked, 403).
3. Reddit r/Golfsimulator and GolfWRX complaint threads, especially the Foresight+ backlash after 18 Sept 2026.
4. TruGolf LaunchBox: camera count, placement and club metric list; independent accuracy.
5. Exact 2021 launch prices of the GC3 and Launch Pro, and the Mevo+ launch price.
6. Whether a GC3 bought new after 18 Sept 2026 keeps club data free after the trial. The Foresight+ Free tier suggests yes for Foresight-branded units, but this is unconfirmed.
7. Square Omni and GC2 camera frame rates and strobe design (not published).
