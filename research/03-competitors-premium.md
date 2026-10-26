# 03 — Premium Tier Competitors (>$7k) and How They Achieve Full Club + Ball Data

Research date: 2026-10-07. Every number has a source URL next to it. **[UNCERTAIN]** marks figures that conflict between sources, that only a retailer or forum supports, or that I could not verify. **[INFERENCE]** marks my own engineering reasoning, which no source states.

> **Coverage caveat.** The shared WebSearch budget ran out partway through this research. The FlightScope, Golfzon, ProTee, Garmin, Square, IDRA and patent sections therefore rely on direct fetches of manufacturer and retailer pages I could reach. Several pages could not be fetched: MyGolfSpy (403), the TrackMan support center (403), fccid.io (403), ScienceDirect (403), and Google Patents for some numbers (503). Where that left a gap, it is flagged. A follow-up pass with fresh search budget should target: MyGolfSpy's 2025–26 launch monitor test numbers, FlightScope's Fusion Tracking patent number, the Golfin IDRA Pro specs, ProTee VX US price, and the TrackMan 4 indoor spin method from TrackMan's own support pages.

---

## 0. Executive summary (the five things that matter)

1. **Almost every premium photometric unit still needs stickers for clubface data.** Foresight GCQuad, QuadMAX, Falcon and GCHawk need **4 reflective club markers** for face angle, loft, lie and impact location. With 1 marker they give only speed, smash, attack angle and path ([GCQuad User Guide p.18](https://support.foresightsports.com/sites/default/files/files/GCQuad_User_Manual.pdf); [Foresight help center](https://help.foresightsports.com/hc/en-us/articles/4405916455443-Troubleshooting-Club-Data-and-Marker-Detection-on-Foresight-Sports-Launch-Monitors)). Uneekor EYE XO2's spec sheet says club data "Requires EYE XO2 Club Stickers" ([EYE XO2 manual](https://download.uneekor.com/docs/EYEXO2_Manual.pdf)). Garmin R50 says "If you want accurate club data, you must use the club stickers" ([PlayBetter R50](https://www.playbetter.com/products/garmin-approach-r50-golf-launch-monitor-simulator)). The latest GCQuad firmware (v4.1.0.1, Nov 24 2025) improved *fiducial recognition*. It did not remove markers ([GCQuad support](https://support.foresightsports.com/support/hardware/gcquad)).
2. **Products that truly deliver markerless face angle, dynamic loft and impact location** all fuse radar with a camera (TrackMan 4, TrackMan iO, FlightScope X3C), or are a newer overhead camera-plus-ML unit with no independent validation (ProTee VX). TrackMan calls its approach **OERT, "Optically Enhanced Radar Tracking"**: a radar-synchronized camera doing "4D silhouette clubhead tracking," with a club-data pickup rate of "over 90%" ([TrackMan glossary](https://www.trackman.com/blog/the-ultimate-guide-to-understanding-trackman)). So TrackMan itself admits that up to about 1 in 10 shots has no club data.
3. **"Markerless" sometimes means "inferred."** Uneekor's sticker-free EYE XR "calculates the XR's face angle from ball and club data". It is not imaged, and the XR does not report dynamic loft or impact location ([Top Shelf Golf EYE XR review](https://topshelfgolf.com/blogs/golf/uneekor-eye-xr-review)). This "D-plane inversion" (solving face angle from launch direction, spin axis and path) is the cheapest route to markerless face angle. It breaks down on off-center strikes because of gear effect.
4. **Portable radar units cannot meet "indoor + no special balls" for spin.** FlightScope X3C indoors: "Aluminum stickers required," or a Titleist RCT ball ([FlightScope X3C](https://flightscope.com/products/flightscope-x3c)). TrackMan co-developed the RCT ball with Titleist "to enhance the data capture of launch conditions in an indoor environment" ([TrackMan glossary](https://www.trackman.com/blog/the-ultimate-guide-to-understanding-trackman)). It also patents radar-reflective ball markings specifically for short indoor flights ([US 11,673,029 B2](https://patents.google.com/patent/US11673029B2/en)). Our requirements (markerless, any ball, indoor and outdoor, portable) therefore force **camera-measured spin**, with radar at most a supporting sensor.
5. **The price floor for photometric ball data plus marker-based club data has collapsed.** Bushnell Launch Pro, which uses GC3-class three-camera tech, is **$2,999.99**, or **$1,999.99 for the indoor version** ([Bushnell](https://www.bushnellgolf.com/launch-pro)). Square Omni is $1,599 with optional club markers ([Square Golf](https://www.squaregolf.com/)). The open gap is **portable + markerless face, loft and impact + any ball + indoor and outdoor + no subscription + open API**. Every product meeting the markerless-club bar is ≥$13k, ceiling-mounted, or both.

---

## 1. Product-by-product

### 1.1 TrackMan 4 (TM4): portable, behind the ball, indoor and outdoor

| Item | Value | Source |
|---|---|---|
| Price | "Starting at USD 25,495" on TrackMan iO page comparison; $25,995 per SmashFactorLab / TrackMan shop; older 2026 sources $21,995 **[UNCERTAIN: $21,995–$25,995 depending on source/date]** | [TrackMan iO page](https://www.trackman.com/golf/launch-monitors/trackman-io), [SmashFactorLab](https://smashfactorlab.com/software/trackman-virtual-golf/), [PlayBetter](https://www.playbetter.com/blogs/golf-simulator-comparisons/foresight-sports-vs-trackman-launch-monitors) |
| Recurring | ~$1,100/yr after year 1 (TPS + Virtual Golf); ~$4,000 3-year package; one source says $1,200/yr | [SmashFactorLab](https://smashfactorlab.com/software/trackman-virtual-golf/), [best-golf-simulator.com](https://best-golf-simulator.com/trackman-cost/), [GolfGearRanked](https://golfgearranked.com/tools/trackman-4/) **[UNCERTAIN]** |
| Radars | "Dual Radar systems, synchronized in time and space": a short-range "ultra high-resolution system, focused on putting, club and impact data" and a long-range "high accuracy ball tracking system" | [TrackMan tech specs](https://www.trackman.com/golf/launch-monitors/tech-specs) |
| Radar bands | FCC ID SFX-TMB4A: 10,500–10,550 MHz and 24,075–24,175 MHz (Part 15.245) | fccid.io/SFX-TMB4A, via search snippet. The page returned 403 to direct fetch **[UNCERTAIN: secondary]** |
| Radar architecture | Forum reading of FCC internal photos: 10 GHz Tx/Rx in the corners (full flight), 24 GHz in the center (near impact) | [GolfSimulatorForum](https://golfsimulatorforum.com/forum/off-topic/all-off-topic/273222-new-higher-frequency-radar-sensors) **[UNCERTAIN: forum]** |
| Sampling | "The radars operate at 40,000 samples per second and per receiver" | [TrackMan glossary](https://www.trackman.com/blog/the-ultimate-guide-to-understanding-trackman) |
| Camera | "Radar Synchronized High Speed Optics" (frame rate not published). Separate video camera: 720p@60 / 1080p@45 | [TrackMan tech specs](https://www.trackman.com/golf/launch-monitors/tech-specs) |
| Club tracking | OERT "synchronizes an inbuilt full HD video camera with the dual radar system"; "4D silhouette clubhead tracking with a pickup rate for club data of over 90%" | [TrackMan glossary](https://www.trackman.com/blog/the-ultimate-guide-to-understanding-trackman) |
| Impact location | "Trackman 4 uses patented optically enhanced radar tracking (OERT) technology to capture the exact impact location on the clubface" | [TrackMan 4 page](https://www.trackman.com/golf/launch-monitors/trackman-4) |
| Parameters | 17 club, 13 ball, 25 putting ("40+") | [TrackMan 4 page](https://www.trackman.com/golf/launch-monitors/trackman-4) |
| Club list | Club Speed, Attack Angle, Dynamic Loft, Club Path, Face Angle, Face to Path, Spin Loft, Swing Plane, Swing Direction, Low Point, Impact Height, Impact Offset, Dynamic Lie, Low Point Side, Low Point Height, Swing Radius, D Plane Tilt | [TrackMan tech specs](https://www.trackman.com/golf/launch-monitors/tech-specs) |
| Ball list | Ball Speed, Smash, Launch Angle, Spin Rate, Launch Direction, Spin Axis, Height, Curve, Landing Angle, Carry, Side, Total, Side Total | same |
| Indoor | Min 4.7 m (16 ft) TrackMan-to-net | same |
| Physical | 300×300×45 mm, 3.0 kg, 10,400 mAh, 4+ h, auto-levelling, camera-based auto-alignment | same |

**Measured vs calculated (TM4).** TrackMan does not publish a per-parameter list. Explicitly calculated or derived: **Side Total** ("a calculated value... A flat surface (ground) and 'normal' hardness is assumed"), **Smash Factor** (ball/club speed) and **Face-to-Path** (face minus path) ([TrackMan glossary](https://www.trackman.com/blog/the-ultimate-guide-to-understanding-trackman)). Outdoors, carry, height, landing angle and curve come from radar tracking of the actual flight (about 6 s) ([TM4 page](https://www.trackman.com/golf/launch-monitors/trackman-4)). Indoors these must be modelled from launch conditions **[INFERENCE]**.

**How TM4 gets spin (radar).** Spin comes from Doppler sidebands caused by the rotating, non-spherical ball surface. Spin *axis* comes from the geometry of several separated receivers. TrackMan's patent describes a ~10.525 GHz CW source of a few mW with "at least one, but typically 3 or more receivers" (via search summary of TrackMan patents; [spin-axis family US 10,850,179 / 11,446,546 / 11,938,375](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11938375). **[UNCERTAIN: assignee of that family not directly verified]**). Indoors, short flight degrades this. Hence the RCT ball and TrackMan's ball-marking patent ([US 11,673,029 B2](https://patents.google.com/patent/US11673029B2/en): silver conductive-ink markers placed so "every great circle" is within distance d of a marker, read by a CW Doppler radar with ≥3 non-co-linear receivers, so spin and axis work "even from very short flights, such as indoor golf shots into a screen"). Forum consensus is that "not using the stickers on the balls" is the most common cause of poor indoor radar spin ([GolfSimulatorForum](https://golfsimulatorforum.com/forum/trackman/194143-trackman-indoor-spin-rate-accuracy) **[UNCERTAIN: forum]**).

**How TM4 gets face angle, dynamic loft and impact location.** The radar gives the 3D clubhead *trajectory*: speed, path, attack angle, swing plane, low point. Path and attack angle are directions of the velocity vector, and Doppler radar measures those natively. Face orientation and impact location come from the synchronized high-speed camera's silhouette tracking (OERT) ([TrackMan glossary](https://www.trackman.com/blog/the-ultimate-guide-to-understanding-trackman)). **[INFERENCE]** TrackMan very likely also cross-checks face angle and dynamic loft against the ball's launch direction, launch angle and spin axis, which it measures independently. The D-plane model is TrackMan's own published framework and makes this a strong prior. The ">90% pickup" figure suggests the camera-silhouette path fails on some shots.

**Independent accuracy.** The Golf Laboratories (Gene Parente) robot test, as reported by PlayBetter, compared GCQuad and TM4. On off-center strikes the spin-axis standard deviation was "82, compared to Trackman's 175". Clubhead speed SD was "0.2 compared to Trackman 4's 0.8". On 15 mm heel strikes it was "0.3 compared to 1.0". Both did well on center strikes ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-comparisons/foresight-sports-vs-trackman-launch-monitors)). **[UNCERTAIN: PlayBetter is a Foresight-leaning retailer; units of the SD values not stated; primary report not located.]** One reviewer quotes ±0.3 mph ball speed, ±0.2° launch and ±50 rpm spin. These are not on TrackMan's spec page, so treat them as unverified ([GolfGearRanked](https://golfgearranked.com/tools/trackman-4/)).

### 1.2 TrackMan iO: ceiling-mounted, indoor only (the markerless benchmark)

| Item | Value | Source |
|---|---|---|
| Price | "Starting at USD 13,995"; Complete / Commercial ~$21,495–$23,995 by retailer | [TrackMan iO](https://www.trackman.com/golf/launch-monitors/trackman-io), [PlayBetter](https://www.playbetter.com/products/trackman-io-indoor-golf-launch-monitor), [PGA Tour Superstore](https://www.pgatoursuperstore.com/trackman-io---home-complete-golf-launch-monitor/2000000058149.html) |
| Tiers | Home: club data = **Club Speed only**. Home Complete / Commercial: "Club Speed, Face Angle, Club Path, Face to Path, Impact Height, Impact Offset, Dynamic Loft, Spin Loft, Attack Angle" | [TrackMan tech specs](https://www.trackman.com/golf/launch-monitors/tech-specs) |
| Recurring | Home $700/yr; Home Complete $1,100/yr (year 1 included) | [MyGolfSpy forum review](https://forum.mygolfspy.com/topic/74571-trackman-io-review-%E2%80%93-why-this-13995-setup-outperforms-most-floor-units-indoors/), [SmashFactorLab](https://smashfactorlab.com/software/trackman-virtual-golf/) **[UNCERTAIN: secondary]** |
| Sensors | "24 GHz ultra-low-power radar"; "High-speed (up to 4,600 fps) camera for club and ball tracking"; "Patented alignment camera"; "Embedded infrared light system (810–850 nm)" | [TrackMan tech specs](https://www.trackman.com/golf/launch-monitors/tech-specs) |
| Spin | "directly measured 3D spin" (camera, not radar) | same |
| Markers | "No markers required on club or ball" | same |
| Compute | "Dual Trackman iO processor and PC GPU" | same |
| Physical | 333×333×107 mm, 3.9 kg, avg 17 W, Ethernet, VESA mount | same |
| Placement | Ceiling, 9–10 ft operating window; "no minimum distance requirements in front of or behind the ball" | [search summary of retailer listings](https://shopindoorgolf.com/products/trackman-io-launch-monitor) **[UNCERTAIN: height window is retailer-sourced]** |

**Why it matters to us.** iO is the clearest public proof of a minimal markerless full-suite configuration: **one high-speed IR camera (≤4,600 fps) plus 810–850 nm IR flood plus one 24 GHz short-range radar plus GPU post-processing**, with spin measured by the camera. Its weaknesses are an overhead mount, indoor only, and a tier price wall: the same hardware gives club speed only on the $13,995 Home tier. **[INFERENCE]** The hardware is identical across tiers, so the full club suite is a software unlock. TrackMan's marginal hardware cost for full club data is roughly zero.

### 1.3 TrackMan 2025–26 releases
No new TrackMan hardware was found in 2025–26. TrackMan's 2026 activity is software: TPS 10.4 (Sept 23 2026) and a new TrackMan Golf app ([TrackMan home, via search](https://www.trackman.com/)). At PGA Show 2026, TrackMan "focused on its platform rather than introducing new hardware" ([SimCaddy](https://simcaddy.com/blogs/simcaddy-blog/pga-show-2026-updates-amp-takeaways); [Rain or Shine Golf](https://rainorshinegolf.com/blogs/industry-news/pga-show-2026-whats-new)). Forum threads speculated about a new short-range indoor radar ([GolfSimulatorForum](https://golfsimulatorforum.com/forum/trackman/391364-new-indoor-lm-from-trackman)) **[UNCERTAIN]**.

### 1.4 Foresight GCQuad: portable, side of ball, photometric

| Item | Value | Source |
|---|---|---|
| Price | $15,999; $18,499 with putting | [Top Shelf Golf guide](https://topshelfgolf.com/pages/foresight-sports-complete-guide), [PlayBetter](https://www.playbetter.com/blogs/golf-simulator-comparisons/foresight-sports-vs-trackman-launch-monitors) |
| Cameras | "4 TRACKING CAMERAS — High speed cameras used for ball placement and tracking". The User Guide figure shows them as an **upper horizontal pair and a lower horizontal pair** (two stereo pairs stacked vertically) | [GCQuad User Guide p.1](https://support.foresightsports.com/sites/default/files/files/GCQuad_User_Manual.pdf) |
| Why 4 | Replaced GC2's 2 cameras. Cameras "spread farther apart" with a Foresight-designed fish-eye-type lens. Claims "20 times the information" of GC2. Each pair is stereoscopic, "with both the golf ball and the golf club" | [Golf Digest](https://www.golfdigest.com/story/foresights-gcquad-launch-monitor-expands-to-four-cameras-wider-view-20-times-the-information) (via search summary; direct fetch 403) |
| Frame rate | 6,000 fps (retailers) vs "10,000 frames per second" (GOLF.com) **[UNCERTAIN: Foresight does not publish]** | [Top Shelf](https://topshelfgolf.com/pages/foresight-sports-complete-guide), [GOLF.com](https://golf.com/gear/how-it-works-foresight-sports-gcquad-launch-monitor/) |
| Illumination | Per-camera flash. "The slower you swing, the more light each camera must produce" | [GOLF.com](https://golf.com/gear/how-it-works-foresight-sports-gcquad-launch-monitor/) |
| Capture | Up to ~200 ball images in first 30 cm. Reads dimple pattern for spin | search summary of reviews; [Foresight EU Falcon page](https://foresightsports.eu/launch-monitors/falcon/) confirms "first 30cm" and "dimple pattern" **[200-image figure UNCERTAIN]** |
| Processing | "on the order of gigapixels per second" (Foresight's Rick Cuellar) | [GOLF.com](https://golf.com/gear/how-it-works-foresight-sports-gcquad-launch-monitor/) |
| Placement | Ball zone centre ~22" from unit front; zone 14"×14" with club tracking, 18"×14" ball only | [GCQuad User Guide p.15](https://support.foresightsports.com/sites/default/files/files/GCQuad_User_Manual.pdf) |
| Other sensors | Accelerometer (pitch/roll) and barometer (pressure, temperature, estimated altitude) | [GCQuad User Guide p.13](https://support.foresightsports.com/sites/default/files/files/GCQuad_User_Manual.pdf) |
| Markers | "In order to capture club data with the GCQuad, club markers must be applied to the clubface." 4 markers: speed, smash, attack angle, path, face angle, loft, lie. 1 marker: speed, smash, attack angle, path | [GCQuad User Guide p.17–18](https://support.foresightsports.com/sites/default/files/files/GCQuad_User_Manual.pdf) |
| Licensing | Full 4-dot data needs the Club Analysis add-on. 4-dot devices "default to 1-Dot Mode if markers are applied incorrectly, damaged, or not visible" | [Foresight help](https://help.foresightsports.com/hc/en-us/articles/4405916455443-Troubleshooting-Club-Data-and-Marker-Detection-on-Foresight-Sports-Launch-Monitors) |

**Why the GCQuad needs fiducials.** Foresight's Tim Briand says the photoluminescent stickers let the cameras "pinpoint the precise coordinates of various points on the clubface" and are "needed to ensure the most accurate and precise impact data regarding the orientation of the face" ([GOLF.com](https://golf.com/gear/rory-sabbatini-foresight-gcquad-launch-monitor-dq/)). **[INFERENCE]** Four non-coplanar or well-spread points on the face give a full 6-DoF rigid pose by stereo triangulation, and so face normal, loft, lie and the face-plane impact point. One dot gives only a 3D point track, which yields velocity direction (path, attack angle) and speed but no orientation. That is exactly the 1-dot vs 4-dot split in the manual. A bare clubface is low-texture, specular, often dark, and moves about 5 cm per millisecond. Edge or silhouette pose estimation is possible but much harder and less robust than tracking 4 retro-reflective points. One GolfWRX owner reported path showing up for most irons without stickers, but impact and face data did not ([GolfWRX](https://forums.golfwrx.com/topic/1806704-gcquad-club-data-wo-stickers/) **[UNCERTAIN: forum, older]**).

**Contradiction.** GOLF.com's ClubTest article says "no club markers are required" with four *optional* markers ([GOLF.com ClubTest](https://golf.com/gear/golf-foresights-sports-2022-golf-clubtest/)). Foresight's own manual and help center say markers are required for club data. Trust Foresight's documentation.

**Foresight's critique of radar** (vendor claim, not independent): competitors "work out spin axis from the face-to-path difference," which ignores impact location and gear effect. "If you ding that thing way off the toe, it's still going to hook" ([GOLF.com ClubTest](https://golf.com/gear/golf-foresights-sports-2022-golf-clubtest/)). Foresight also claims a "99.99 percent" capture rate (same source).

**Firmware.** v4.0.3.0 (Nov 2024) improved "fiducial recognition". v4.1.0.1 (Nov 24 2025) refined capture for off-target launch directions ([GCQuad support](https://support.foresightsports.com/support/hardware/gcquad), via search summary).

### 1.5 Foresight QuadMAX
- **Price:** $19,999 MSRP ([Foresight](https://www.foresightsports.com/products/quadmax-launch-monitor)); dealers $14,999–$15,999 ([PlayBetter](https://www.playbetter.com/products/foresight-quadmax-golf-launch-monitor-simulator), [Top Shelf](https://topshelfgolf.com/pages/foresight-sports-complete-guide)).
- **Changes vs GCQuad:** same "four-camera photometric technology". Adds on-device Apex, Descent Angle and Offline. Touchscreen. 12,000 mAh field-swappable battery (7–9 h) vs 10,400 mAh. 6.3 lb with magnesium internals (15% lighter). Storage "for up to two billion shots". USB-C, WiFi, Ethernet, BT, NFC. 2-year warranty. Club markers in box. 18"×14" hitting zone ([Foresight QuadMAX](https://www.foresightsports.com/products/quadmax-launch-monitor)). Debuted January 2024 ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-comparisons/foresight-sports-vs-trackman-launch-monitors)).
- **Takeaway:** an ergonomic and UI refresh. The sensing hardware is unchanged.

### 1.6 Foresight GCHawk to Falcon (overhead)
- **GCHawk** is about $20k ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/foresight-sports-falcon-review); [Virtual Tee](https://www.virtualtee.golf/blogs/recent-articles/trackman-io-review-2026-is-it-the-right-forever-launch-monitor-for-a-premium-home-golf-simulator) lists $19,999). foresightsports.com's GCHawk product URL now redirects to the Falcon page, which suggests the Falcon superseded it **[INFERENCE from redirect]**.
- **Falcon:** $16,999 MSRP ([Foresight](https://www.foresightsports.com/products/gchawk-launch-monitor), via the redirect); $15,999 per PlayBetter's March 2026 update ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/foresight-sports-falcon-review)); €17,999 / from £16,788 ex VAT in the EU and UK ([Foresight EU](https://foresightsports.eu/launch-monitors/falcon/)).
- **Technology:** "The same Quadrascopic photometric system that powers the GCQuad, reading from above." Measures within the first 30 cm and reads the dimple pattern for spin ([Foresight EU](https://foresightsports.eu/launch-monitors/falcon/)). Hitting zone 59"×28". 43" long. 26 lb ([Foresight US](https://www.foresightsports.com/products/gchawk-launch-monitor)). Mounted about 4 ft in front of the ball, ≥9.5 ft ceiling ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/foresight-sports-falcon-review)).
- **Markers:** "Club data is enabled with 4 dot club markers, included with the unit" ([Foresight EU](https://foresightsports.eu/launch-monitors/falcon/)). Club data is captured only in "two 11-inch by 11-inch squares in the front corners of the hitting area" ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/foresight-sports-falcon-review)). Some retailers call the Falcon "markerless" ([Top Shelf](https://topshelfgolf.com/collections/foresight-sports-golf-simulator-packages)). That conflicts with Foresight and is wrong.
- **Takeaway for us:** Foresight's overhead product does *not* do markerless club data.

### 1.7 Foresight / Bushnell software and fees (changed Sept 18 2026)
- FSX Play, 2020 and Pro are discontinued. New purchases get **Foresight+** (Free / Silver $199/yr / Gold $599/yr) plus **Course Pass** ($295/yr for 35 courses) or **Course Pass Pro** ($595/yr for ~110–111 courses). A Course Pass requires Silver or Gold. Existing perpetual FSX licenses remain valid but get no new features ([PlayBetter subscriptions guide](https://www.playbetter.com/blogs/golf-simulator-software/foresight-sports-subscriptions-guide-2026); [Top Shelf](https://topshelfgolf.com/pages/foresight-sports-complete-guide)).
- **Third-party integrations (e.g., GSPro) need Gold ($599/yr)** ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-software/foresight-sports-subscriptions-guide-2026)). Bushnell lists "GSPro, $250/year (Requires active Gold Membership)" ([Bushnell](https://www.bushnellgolf.com/launch-pro)). **This is directly relevant to our "open API, no subscription" positioning.** Foresight now charges at least about $849/yr to pipe shots to a third-party simulator.
- Foresight EU says the Falcon "requires no additional subscriptions or fees to use its features" ([Foresight EU](https://foresightsports.eu/launch-monitors/falcon/)). That conflicts with the US Foresight+ model **[UNCERTAIN: regional difference or stale page]**.

### 1.8 Bushnell Launch Pro (GC3 tech; for comparison)
- **Price:** $2,999.99 (indoor and outdoor, club and ball); **Launch Pro Indoor $1,999.99**; "Circle B Edition" is a cosmetic refresh ([Bushnell](https://www.bushnellgolf.com/launch-pro)).
- **Tech:** "proprietary high speed/high resolution cameras with infrared... an auto calibrating three-camera system" ([Bushnell](https://www.bushnellgolf.com/launch-pro)).
- **Club data:** speed, smash, path, attack angle only (no face angle). Needs markers: "The three cameras need a clear view of the club markers ('fiducials')". Needs at least the Silver tier ([Bushnell](https://www.bushnellgolf.com/launch-pro); [PlayBetter](https://www.playbetter.com/blogs/golf-simulator-software/foresight-sports-subscriptions-guide-2026)).
- **Foresight GC3:** $6,999, "triscopic", club markers, LCD, indoor and outdoor ([Top Shelf](https://topshelfgolf.com/pages/foresight-sports-complete-guide)). GC3S $3,799, being phased out (same).
- **Takeaway:** a three-camera photometric ball engine with marker-based basic club data sells for $2k–$3k retail. That sets the BOM ceiling we must beat on ball data.

### 1.9 Uneekor EYE XO2 / EYE XO / QED to EYE XR ("Optix")

| Model | Price | Cameras | Mount | Club data | Markers |
|---|---|---|---|---|---|
| EYE XO2 | $10,999 | 3 high-speed photometric IR | Ceiling, 3.5 ft in front of tee, 9–10 ft high | 9: speed, smash, path, face-to-path, AoA, face, dynamic loft, lie, impact point V/H | "Requires EYE XO2 Club Stickers" (bar sticker + dot sticker) |
| EYE XO | $6,499 | 2 IR | Ceiling front | Same club stats as XO2, smaller zone (16"×12") | Stickers |
| EYE XR (2025, replaced QED) | $5,999 | 2 IR, 1440×1080 | Ceiling rear, 9–10 ft | 4: speed, path, smash, face angle | **None**, but "calculates the XR's face angle from ball and club data" |
| QED (disc.) | ~$6,000 | — | Ceiling rear | speed, smash, path, face, face-to-path | Marked balls + club stickers |

Sources: [Uneekor XO2 page](https://uneekor.com/golf-launch-monitors/eye-xo2); [EYE XO2 manual](https://download.uneekor.com/docs/EYEXO2_Manual.pdf) (mount 3'6" in front of tee and 9–10 ft high, "Failure to meet these requirements will result in accuracy issues"; ball speed 11–223 mph; back spin up to 12,000 rpm; launch −10° to 50° driver; PoE 802.3bt; 2.63 kg; "Risk Group 2" IR warning; indoor only); [Top Shelf collection prices](https://topshelfgolf.com/collections/uneekor); [Top Shelf EYE XR review](https://topshelfgolf.com/blogs/golf/uneekor-eye-xr-review); [Carl's Place comparison](https://www.carlofet.com/blog/uneekor-qed-vs-eye-xo-vs-eye-xo2); [Golf Wire](https://thegolfwire.com/uneekor-milestone-year-innovation).

- **Frame rate conflict:** 180 fps @ 1440×1080 (Ace Indoor Golf), "3,000+" (Top Shelf), 240 fps (Elite Sim Golf). Uneekor itself says "2,500 Frames at Impact" for Club Optix ([search summary of retailer pages](https://uneekor.com/golf-launch-monitors/eye-xo2)) **[UNCERTAIN]**. **[INFERENCE]** This is consistent with a global-shutter sensor at ~180 fps full frame that switches to a small region of interest for thousands of fps at impact. Treat it as a hypothesis.
- **"Optix" branding:** *Dimple Optix* (patented; reads dimples, so any ball works), *Club Optix* (impact video and club data, stickers recommended or required), *Swing Optix* (2 external 120 fps swing-video cameras, $1,700). "Optix" is **not** a markerless club-pose technology on the XO2. The XO2 product page lists "Reflective stickers (required)" for club tracking, while the spec sheet says "recommended" **[Uneekor is internally inconsistent; the manual spec table says "Requires"]**.
- **Recurring:** Player free, Pro $199/yr, Champion $399/yr, Ultimate $599/yr ([Top Shelf](https://topshelfgolf.com/collections/uneekor)).
- **2026:** software only (AIMY AI coach, GameDay tournaments, Launcher 2.0). No EYE XO3 found ([Golf Wire PGA Show](https://thegolfwire.com/uneekor-milestone-year-innovation); [Rain or Shine](https://rainorshinegolf.com/blogs/industry-news/pga-show-2026-whats-new)).

### 1.10 FlightScope X3 / X3C: portable radar plus camera ("Fusion Tracking")
- **Price:** $14,995 list, $13,495 sale. The X3 URL now redirects to the X3C ([FlightScope X3C](https://flightscope.com/products/flightscope-x3c)).
- **Tech:** "3D Doppler tracking radar and synchronized image processing". Fusion Tracking is "an innovative combination of 3D Doppler tracking radar technology and synchronized high speed image processing... a revolutionary patented method". Carbon-fiber housing. Internal camera. Radar frequency and frame rate not published (same page).
- **Parameters:** 50 claimed. Club: speed, AoA, spin loft, path, face-to-path, face-to-target, V/H swing plane, low point, dynamic loft, speed and acceleration profiles, **Face Impact Location** (lateral and vertical; "requires a minimum of 300 lux"). Ball: full suite including spin rate and axis, apex, descent, curve (same).
- **Indoor:** sensor 8–12 ft behind tee with 8–13 ft of ball flight; **"Aluminum stickers required"** on the ball (or a Titleist RCT ball). Avoid fluorescent lighting. 100 aluminum stickers in the box (same).
- **Recurring:** includes 12 E6 Connect courses. Larger E6 bundles are annual. **Third-party software: "No, not unless you are an approved systems integrator"** (same). Another closed ecosystem.
- **Radar spin IP:** EDH (FlightScope's parent) owns [US 9,868,044 B2 "Ball spin rate measurement"](https://patents.google.com/patent/US9868044B2/en) (priority 2013). It demodulates the Doppler phase and detects bipolar pulses from features passing the ball's far side. The ball core acts as a lens ("unique to the ball lens effect"), and the period of those pulses gives spin.
- **No 2026 X-series hardware found.** FlightScope's PGA Show 2026 news was Mevo Gen2 Range for multi-bay ranges ([Rain or Shine](https://rainorshinegolf.com/blogs/industry-news/pga-show-2026-whats-new)).

### 1.11 Full Swing KIT and Full Swing Pro simulators
- **KIT:** $4,999. "Patented, 24GHz Dual-Mode, ML Enhanced Radar"; camera 1080p @ 60 fps (video, not high-speed); dual-core A9; 8,000 mAh (~5 h) ([KIT specs](https://www.fullswinggolf.com/kit-specs/); [KIT page](https://www.fullswinggolf.com/kit-launch-monitor/)). 16 parameters including face angle, face-to-path, attack angle, club path and speed, spin rate and axis. **No dynamic loft, no impact location.** Indoor: 8–10 ft behind the ball and 8–10 ft of flight. The site does not say how indoor spin is obtained ([KIT page](https://www.fullswinggolf.com/kit-launch-monitor/)). **[INFERENCE]** A 60 fps camera cannot image the club at impact, so KIT's face angle is almost certainly radar plus ML inference (D-plane-style), not imaged. Below the $7k tier but relevant as the "markerless face angle via ML radar" reference.
- **Full Swing Pro 2.0 simulator:** from $54,900. "4 HyperClear cameras – ION3 overhead camera". In-flight tracking via "infrared technology & high-speed blue light LED cameras". The ball is measured "at impact with an overhead ION3 Camera" ([Full Swing Pro](https://www.fullswinggolf.com/pro-series-simulator/)). Club metric list not published. Not portable.

### 1.12 ProTee VX: overhead, claims full markerless club data
- "Captures club and ball data with dual high-speed cameras." Club: "Club Speed, Swing Path, Club Face Angle, Club Face to Path, Attack Angle, Dynamic Loft", plus lie and vertical and horizontal impact location. Ball: speed, total, back and side spin, axis, launch direction and angle. "No special golf balls, no club stickers". Ceiling ≥9 ft. Zone 25"×21". "No recurring software fees" ([ProTee VX](https://proteegroup.com/the-power-of-vx/)). Machine vision plus "A.I." ([ProTee home](https://proteegroup.com/)). It first appeared in beta about 3 years ago and is GSPro-compatible ([SimCaddy](https://simcaddy.com/blogs/simcaddy-blog/pga-show-2026-updates-amp-takeaways)).
- **Price:** not published on the manufacturer site **[UNKNOWN; needs a follow-up search]**. No independent accuracy data found.
- **Why it matters:** this is the closest existing product to our business model (no subscription, open to third-party sims, markerless full club suite from 2 cameras). But it is overhead and indoor only.

### 1.13 Golfzon (TwoVisionNX, GDR MAX)
- TwoVisionNX: "dual high-speed camera sensors", moving plate (64 directions, 56,000 lies), weight-shift sensors. Club stats: head speed, attack angle, face angle, dynamic loft, face-to-path, club path, smash ([Golfzon TwoVisionNX](https://www.golfzongolf.com/gameplay-simulators/twovisionnx)). Home simulators "Starting at $21,300" ([Golfzon US](https://www.golfzongolf.com/)). Marker requirements, fps and mounting are not published **[UNKNOWN]**. Golfzon is a turnkey simulator vendor, not a portable LM competitor.

### 1.14 Garmin Approach R50 (sub-$7k but a full-suite claimant)
- $4,999.99. "3 High-Speed Cameras (Photometric)". 10" touchscreen. Barometer. IPX3. Spin rate and axis "measured, not calculated". Club: speed, path, AoA, face angle, face-to-path. **"If you want accurate club data, you must use the club stickers."** Garmin Golf Premium $9.99/mo or $99.99/yr for Home Tee Hero ([PlayBetter R50](https://www.playbetter.com/products/garmin-approach-r50-golf-launch-monitor-simulator)). No dynamic loft or impact location listed.

### 1.15 Square Golf (Omni), Rapsodo, Golfin IDRA, TruGolf, Sportsbox: emerging
- **Square Omni:** $1,599, no subscription, any ball, "optional club markers provide precise feedback on club movement and impact", indoor and outdoor including natural turf ([Square](https://www.squaregolf.com/); [Square Omni](https://www.squaregolf.com/pages/launch-monitors-oe)). Pre-orders opened around PGA Show 2026 ([Rain or Shine](https://rainorshinegolf.com/blogs/industry-news/pga-show-2026-whats-new)).
- **Golfin IDRA Pro:** previewed at PGA Show 2026. Adds "a third high-speed camera" over IDRA II for "deeper club and swing data capture" ([SimCaddy](https://simcaddy.com/blogs/simcaddy-blog/pga-show-2026-updates-amp-takeaways)). Club data "without using stickers" ([Golf Wire](https://thegolfwire.com/indoor-golf-2026-ai-value/)). Price and specs unknown **[UNCERTAIN; follow up]**.
- **Rapsodo:** a ceiling-mounted concept due "later this year" (2026) ([Rain or Shine](https://rainorshinegolf.com/blogs/industry-news/pga-show-2026-whats-new)). No specs.
- **TruGolf LaunchBox:** about $2,999, "club data without stickers" per a Tom's Guide headline ([Tom's Guide](https://www.tomsguide.com/wellness/fitness/i-cant-believe-the-trugolf-launchbox-offers-club-data-without-stickers-for-this-price)). Article body not retrievable **[UNCERTAIN]**.
- **VTrack** (overhead): "1,800 frames per second... without stickers, marked balls, or annual subscription fees" ([Indoor Golf Outlet](https://indoorgolfoutlet.com/products/vtrack-launch-monitor), via search summary) **[UNCERTAIN]**.
- **Sportsbox AI:** markerless 3D *body* motion from a phone, not a launch monitor. Not researched in depth here.

### 1.16 Price and recurring-fee summary

| Product | Hardware (USD) | Recurring | Markerless face/loft/impact? | Portable? | Outdoor? | Indoor normal ball spin? |
|---|---|---|---|---|---|---|
| TrackMan 4 | $21,995–25,995 | ~$1,100/yr | **Yes** (OERT, >90% pickup) | Yes | Yes | Weak; RCT ball recommended |
| TrackMan iO | $13,995 (club speed only) / ~$21.5–24k (full club) | $700 / $1,100/yr | **Yes** | No (ceiling) | No | Yes (camera spin) |
| FlightScope X3C | $13,495–14,995 | E6 add-ons | **Yes** (Fusion; impact needs 300 lux) | Yes | Yes | **No**: aluminum ball stickers |
| GCQuad | $15,999 | Foresight+ $0–599 + Course Pass | No: 4 markers | Yes | Yes | Yes |
| QuadMAX | $19,999 (street ~$15k) | same | No: 4 markers | Yes | Yes | Yes |
| Falcon (GCHawk successor) | $15,999–16,999 | same | No: 4 markers | No | No | Yes |
| Uneekor EYE XO2 | $10,999 | $0–599/yr | No: stickers | No | No | Yes |
| Uneekor EYE XR | $5,999 | $0–599/yr | Face angle *inferred*; no loft or impact | No | No | Yes |
| ProTee VX | not published | none | **Claimed yes** (unvalidated) | No | No | Yes |
| Golfzon TwoVisionNX | from $21,300 (sim) | n/a | unknown | No | No | unknown |
| Full Swing KIT | $4,999 | app free; sim sub | Face angle (ML radar); no loft or impact | Yes | Yes | unknown |
| Garmin R50 | $4,999 | $99.99/yr optional | No: stickers | Yes | Yes | Yes |
| Bushnell Launch Pro | $2,999 / $1,999 indoor | Silver $199+ for club data; Gold+GSPro $849 | No (no face angle) | Yes | Yes | Yes |

---

## 2. Independent accuracy evidence: what exists and what doesn't

- **Golf Laboratories robot test (GCQuad vs TM4)**, reported by PlayBetter: GCQuad had tighter spin-axis SD on off-center hits (82 vs 175), tighter clubhead-speed SD (0.2 vs 0.8), and tighter heel-strike results (0.3 vs 1.0). Both were similar on center hits ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-comparisons/foresight-sports-vs-trackman-launch-monitors)). **[UNCERTAIN: retailer-relayed; not the primary report.]** The pattern of radar diverging on off-center strikes is consistent with Foresight's claim that radar-derived spin axis ignores gear effect.
- **GOLF ClubTest** uses GCQuad with Golf Laboratories robots for 9-point face mapping ([GOLF.com](https://golf.com/gear/golf-foresights-sports-2022-golf-clubtest/)). This is a commercial partnership, not a validation study.
- **Academic:** Leach, Forrester, Mears & Roberts (2017), *"How valid and accurate are measurements of golf impact parameters obtained using commercially available radar and stereoscopic optical launch monitors?"*, *Measurement* 112, compared a TrackMan radar and a stereoscopic optical LM (GC2 era) against a high-speed reference. The DOI [10.1016/j.measurement.2017.08.009](https://doi.org/10.1016/j.measurement.2017.08.009) resolves to Elsevier's *Measurement*, but the full text was blocked (403). **[UNCERTAIN: findings not verified here; obtain the PDF.]**
- **MyGolfSpy** launch-monitor testing: the page returned 403. **Not covered; needs follow-up.**
- **USGA / R&A:** no public LM accuracy standard was found in this pass **[gap]**.
- **Gap that matters to us:** I found **no independent test of markerless face angle, dynamic loft or impact location** for any product, including TrackMan, ProTee VX, FlightScope Fusion and Uneekor EYE XR. Every validation of club-face metrics found is either vendor-run or marker-based. A credible third-party validation protocol would therefore be a differentiator **[INFERENCE]**.

---

## 3. Answers to the four questions

### (1) Which sensing approaches reliably produce markerless face angle, path, dynamic loft and impact location today?

| Metric | Approaches proven in shipping products | Notes |
|---|---|---|
| **Club speed, path, attack angle, swing plane, low point** | (a) Short-range multi-receiver Doppler radar on the clubhead trajectory (TM4 24 GHz short-range radar, FlightScope 3D Doppler, Full Swing 24 GHz). (b) Stereo or multi-camera tracking of the head centroid or silhouette pre-impact. | These are properties of the head's *velocity vector*, so they are the easy metrics. Radar measures radial velocity at 40 kS/s per receiver; angle comes from phase differences across receivers ([TrackMan glossary](https://www.trackman.com/blog/the-ultimate-guide-to-understanding-trackman)). Even GCQuad gets path and AoA from just 1 dot. |
| **Face angle, dynamic loft** | (a) **Imaged**: a high-speed camera synchronized to radar fits the head silhouette and pose at impact (TrackMan OERT, "4D silhouette clubhead tracking"; iO 4,600 fps IR camera; ProTee VX dual cameras plus ML, claimed). (b) **Inferred**: D-plane inversion from measured ball launch direction, vertical launch, spin axis and spin rate plus measured path and AoA (EYE XR: "calculates the XR's face angle from ball and club data"; Full Swing KIT ML radar, by inference). (c) **Marker-based** 6-DoF pose from ≥4 fiducials (Foresight, Uneekor XO/XO2, Garmin, Bushnell). | (b) is cheap but biased on off-center hits (gear effect changes spin axis and launch direction independently of face). (a) is what premium markerless units do, and TrackMan still reports only ">90%" pickup. The robust production answer is (a) fused with (b): use the ball-derived estimate as a prior or consistency check on the imaged pose **[INFERENCE]**. |
| **Impact location** | (a) Imaged: ball and face positions at the contact frame (TM4 OERT; FlightScope Fusion with ≥300 lux; TrackMan iO impact height and offset). (b) Marker-based (GCQuad 4-dot, XO2). (c) Inferred from smash-factor loss plus gear-effect spin-axis residual. | Requires knowing the head's face plane and the ball position in the same frame. That is the hardest metric, and the first one cheaper markerless units drop (EYE XR, KIT, R50, Launch Pro all omit it). |
| **Lie** | Imaged pose or 4 markers only | Only TM4 (dynamic lie), GCQuad 4-dot, XO2 and ProTee (claimed) report it. |

**Bottom line.** The reliable markerless recipe is **high-speed, IR-flood-lit, global-shutter imaging of the club head at impact, fitted to a 3D head model (silhouette or edges), time-synchronized with a trajectory sensor (radar or stereo) and constrained by the measured ball launch**. No shipping product does markerless face, loft and impact from a side-of-ball camera unit. Foresight, the photometric leader, still uses stickers in 2026.

### (2) What is the minimum hardware configuration proven capable of the full suite?

Proven configurations, smallest first:

1. **Markerless, overhead, indoor (TrackMan iO):** one high-speed camera at up to 4,600 fps, IR flood at 810–850 nm, one 24 GHz low-power radar, plus a separate alignment camera, a dual on-board processor and **a host PC GPU** ([TrackMan tech specs](https://www.trackman.com/golf/launch-monitors/tech-specs)). Camera resolution is not published. This is the minimal markerless full-suite system on record, but it uses a top-down view at 9–10 ft.
2. **Markerless, overhead, 2 cameras (ProTee VX, claimed):** dual high-speed cameras plus ML, no radar ([ProTee](https://proteegroup.com/the-power-of-vx/)). Unvalidated.
3. **Marker-based, overhead, 2 IR cameras (Uneekor EYE XO):** full 9-metric club data with stickers, 16"×12" zone ([Carl's Place](https://www.carlofet.com/blog/uneekor-qed-vs-eye-xo-vs-eye-xo2)). The XO2's 3rd camera exists mainly to enlarge the zone to 28"×21".
4. **Marker-based, side of ball, 4 cameras (GCQuad / QuadMAX):** two stereo pairs stacked vertically, wide-baseline fish-eye optics, per-camera IR flash, ~22" standoff, 14"×14" club zone, 6,000–10,000 fps **[UNCERTAIN]** ([GCQuad manual](https://support.foresightsports.com/sites/default/files/files/GCQuad_User_Manual.pdf); [GOLF.com](https://golf.com/gear/how-it-works-foresight-sports-gcquad-launch-monitor/)). Three-camera side units (GC3, Launch Pro, Garmin R50) deliver full *ball* data but either stop at path and AoA (Launch Pro) or give face angle only with stickers (R50).
5. **Markerless, portable, behind the ball (TM4, FlightScope X3C):** dual radar (TM4: 10.5 GHz full-flight plus 24 GHz short-range; multiple receivers; 40 kS/s per receiver) plus one radar-synchronized high-speed camera. **Both need marked or RCT balls for good indoor spin.**

**What a side-of-ball markerless full-suite unit would minimally need [INFERENCE: engineering estimate, to be validated by the camera and radar research tracks in 04/05]:**
- **Cameras:** at least 2 synchronized global-shutter NIR cameras as a stereo pair with a baseline of about 10–20 cm (GCQuad's "spread farther apart" redesign was about baseline). For full-face pose robustness across drivers and irons, a 3rd camera or a vertically offset pair helps a lot: the GCQuad's upper and lower pairs give a vertical baseline too, which constrains loft and lie. Effective frame rate around 1,500–5,000 fps in a region of interest around impact, or strobe multi-exposure on a lower-fps sensor. At 4,600 fps a 120 mph (53.6 m/s) head moves about 1.2 cm per frame and a 170 mph ball about 1.65 cm per frame, so roughly 3–5 usable ball frames in the first 10 cm and 2–4 head frames within ±2.5 cm of impact.
- **Illumination:** pulsed 810–850 nm IR with microsecond-scale exposure to freeze motion, plus a narrow-band filter. Outdoors, sunlight at 850 nm is the main challenge, which is why per-camera flash and short exposures matter. GOLF.com: "the slower you swing, the more light each camera must produce."
- **Radar (optional but valuable):** one 24 GHz multi-receiver module for club speed, path and attack angle pre-impact, independent of vision. It also gives ball speed and direction redundancy. Outdoors it could track flight to validate the aero model. Do not rely on it for indoor spin.
- **Compute:** the iO offloads to a PC GPU. A portable unit needs an on-board NPU or GPU for head-pose fitting within roughly 1 s.

### (3) Patents and proprietary methods they rely on (pointers only; IP is covered in depth elsewhere)

| Owner | Item | Pointer |
|---|---|---|
| TrackMan A/S | OERT "patented" (camera plus radar fusion for impact location and club data) | [TrackMan 4](https://www.trackman.com/golf/launch-monitors/trackman-4) (number not identified) **[follow up]** |
| TrackMan A/S | Ball markings for radar spin on short (indoor) flights: US 11,673,029 B2 (priority 2019-07-11) and continuation US 12,179,068 | [Google Patents 11673029](https://patents.google.com/patent/US11673029B2/en); [USPTO 12179068](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12179068) |
| TrackMan A/S (likely) | "System and method for determining a spin axis of a sports ball": US 10,850,179; 11,446,546; 11,938,375 | [USPTO 11938375](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11938375) **[assignee unverified]** |
| TrackMan A/S | iO "Patented alignment camera" | [TrackMan tech specs](https://www.trackman.com/golf/launch-monitors/tech-specs) |
| TrackMan A/S | FCC IDs SFX-TMB4A (TM4 rev), SFX-TMAN4 (internal photos and test reports useful for teardown) | fccid.io/SFX-TMB4A, fccid.io/SFX-TMAN4 **[403 on fetch]** |
| EDH / FlightScope | US 9,868,044 B2 "Ball spin rate measurement" (radar phase-demodulation, ball-lens pulse) | [Google Patents](https://patents.google.com/patent/US9868044B2/en) |
| FlightScope | Fusion Tracking: "a revolutionary patented method" | [FlightScope X3C](https://flightscope.com/products/flightscope-x3c) (number not identified) **[follow up]** |
| Foresight (Wintriss to WAWGD) | US 7,497,780 B2 "Integrated golf ball launch monitor" (GC2-era, priority 2006) | [Google Patents](https://patents.google.com/patent/US7497780B2/en) |
| Foresight | Additional US and Japan patents shown on the GCQuad "About" screen (unreadable at manual resolution) | [GCQuad User Guide p.14](https://support.foresightsports.com/sites/default/files/files/GCQuad_User_Manual.pdf) |
| Full Swing | "Patented, 24GHz Dual-Mode, ML Enhanced Radar" | [KIT specs](https://www.fullswinggolf.com/kit-specs/) |
| Uneekor | "patented Dimple Optix" (markerless ball spin from dimples); trademarks Club Optix® and Swing Optix® | [Uneekor EYE MINI LITE (via search)](https://uneekor.com/golf-launch-monitors/eye-mini-lite) |
| Titleist / TrackMan | RCT ball (radar-capture-technology ball for indoor) | [TrackMan glossary](https://www.trackman.com/blog/the-ultimate-guide-to-understanding-trackman) |

### (4) What would we copy or replicate to reach TrackMan-class data at a fraction of the cost, and where are they over-engineered?

**Replicate (the load-bearing parts):**
1. **Camera-measured spin from the ball's surface texture (dimples, logo, seams)** rather than radar sidebands. This is what makes "any ball, indoor" work (Foresight, Uneekor Dimple Optix, TrackMan iO). Radar spin indoors needs marked balls, which our spec forbids.
2. **Wide-baseline stereo with a vertical component**, as in the GCQuad's stacked pairs, for full 6-DoF pose of the ball and club near impact.
3. **Hardware time-sync between sensors.** OERT's essence is "synchronized in time and space". Microsecond-level exposure timestamps on all cameras and the radar matter more than raw fps.
4. **Pulsed narrow-band NIR illumination** (810–850 nm) with short exposures. Per-camera flash scaled to swing speed is what lets photometric units work outdoors (GCQuad).
5. **Model-based markerless head-pose estimation** (CAD or learned silhouette fitting, TrackMan's "4D silhouette") **fused with a D-plane / gear-effect physics prior** from the ball. This is the software moat, and it suits a software-strong team. The minimum viable version is the EYE XR approach (inferred face angle). The target version is imaged face, loft and impact, falling back to inferred values with a confidence flag when imaging fails. TrackMan's own >90% pickup suggests a fallback is necessary.
6. **Self-calibration**: auto-levelling with an accelerometer, a barometer for air density (GCQuad has both), and camera-based target alignment (TM4 and iO patent this, so design around it).

**Where premium units are over-engineered for a consumer product:**
- **TM4's long-range 10.5 GHz full-flight radar.** About 6 s of flight tracking is valuable for tour range work, but the market's reference device for club testing (GCQuad, used by GOLF ClubTest) models flight from launch conditions. Indoors, full-flight radar adds nothing. **[INFERENCE]** A launch-condition-plus-aero model gets most of the value for most users. Optional outdoor radar validation could be a v2.
- **Over 40 parameters, putting-green physics and stimp** (TM4 has 25 putting parameters). Nice to have, not core.
- **Premium materials and storage**: aerospace carbon fiber (X3C), magnesium internals and storage for "two billion shots" (QuadMAX), field-swappable 12,000 mAh batteries, built-in touchscreens. Phones and tablets can do the UI.
- **4 cameras for zone size.** Uneekor gets the full marker-based club suite from 2 cameras; the XO2's 3rd camera mainly enlarges the zone. Hitting-zone size is a cost lever we can tune.
- **Business-model over-engineering:** tiered software locks on identical hardware (iO Home vs Complete; Foresight 1-dot vs 4-dot add-on; Bushnell club data behind Silver) and paywalled or closed third-party access (Foresight Gold plus $250/yr GSPro; FlightScope "approved systems integrator" only). Our "no subscription, open API" stance attacks this directly. Of the premium-adjacent players, only ProTee VX, Square and Uneekor's base tier are reasonably open.

**Where they are *not* over-engineered (do not cut corners here):**
- Capture rate and robustness: Foresight claims 99.99% capture; TrackMan admits >90% club pickup. Missed or garbage club reads destroy trust faster than slightly worse accuracy **[INFERENCE]**.
- Off-center-strike handling (gear effect): this is where radar and inferred systems measurably degrade ([Golf Laboratories via PlayBetter](https://www.playbetter.com/blogs/golf-simulator-comparisons/foresight-sports-vs-trackman-launch-monitors)). A product that infers face angle from ball flight will be wrong exactly on the shots golfers most want diagnosed.
- Outdoor sunlight robustness for cameras (illumination power, exposure, filtering) and the strict mounting geometry: Uneekor warns that mis-mounting "will result in accuracy issues."

---

## 4. Open questions and follow-ups (need fresh search budget)
1. MyGolfSpy 2025–26 launch monitor test results (403 on fetch).
2. FlightScope Fusion Tracking patent number and how X3C measures face-to-target (imaged vs inferred).
3. TrackMan 4 indoor behaviour without RCT balls: measured vs "normalized" or calculated spin (TrackMan support center returned 403).
4. ProTee VX US price and any independent validation; Golfin IDRA Pro specs and price; TruGolf LaunchBox markerless claims.
5. GCQuad exact frame rate and sensor; the Leach et al. 2017 full-text numbers.
6. TrackMan OERT patent number(s), likely the "coordinating radar data and image data" family. Google Patents returned 503 for US20160074704A1.
