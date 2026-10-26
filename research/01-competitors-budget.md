# 01 — Competitor Landscape: Budget Tier Launch Monitors (under ~$1,500 street)

**Prepared:** October 7, 2026
**Scope:** Consumer launch monitors and simulators that sell for roughly $1,500 or less. A few just-over-threshold units (Square Omni $1,599, OpenLaunch Nova $1,500, SkyTrak+ on clearance) are included because they define the top edge of this tier and sit right at our target price.
**For:** the founding team (TrackMan-class, markerless, portable, no-subscription launch monitor).

> **How to read this.** Every number has a URL next to it. **UNVERIFIED** or **CONFLICT** marks a claim we couldn't confirm or where sources disagree. A "measured / calculated" split comes from the manufacturer where one is published. Otherwise it comes from independent reviewers, and that is noted.
>
> **Research limits (please read).**
> - The shared web-search budget for this session (200 searches) ran out partway through. After that, work continued only by fetching URLs already found.
> - MyGolfSpy (reviews and forum), GolfWRX and Reddit returned HTTP 403 or couldn't be fetched. Sentiment from those communities therefore comes from search-result snippets, from other sites quoting them, or from the r/Golfsimulator-sourced **Yardstick Golf 2026 buyer survey** spreadsheet.
> - We found no YouTube transcripts and no Carl's Place written reviews beyond one Mevo Gen2 test.
> - No teardown or bill-of-materials (BOM) data was found for any device (radar chip and image sensor are UNVERIFIED everywhere).
> - A follow-up pass, with more search budget or the FCC ID internal-photo filings, should fill these gaps.

---

## 0. Executive summary

1. **The tier has a hard "value ceiling".** No product here gives markerless measured spin, measured face angle and impact location in a portable unit that works equally well indoors and outdoors.
   - **Radar units** (Garmin R10, Swing Caddie SC4 Pro, Blue Tees Rainmaker, PRGR, Mevo) measure speeds and launch well outdoors. Indoors their spin is mostly *calculated*, or needs special balls (RCT, RPT) or metallic dots.
   - **Camera units** (Square, Square Omni, SkyTrak+, Uneekor) measure spin optically. They need stickers for club data and are weaker in bright sun.
   - **Face angle** is estimated or missing in this tier, or sits behind a paid unlock: FlightScope Pro Package $699–$1,000; Square Omni estimates it from a shaft sticker.
2. **The Square Golf Omni ($1,599, shipping since spring 2026) is the most important competitor for us.** It is the closest thing to our spec at a near-budget price:
   - Four IR cameras, side-of-ball placement, no special balls, measured ball spin.
   - Club path, attack angle and impact location, all with stickers. Face angle and dynamic loft are *estimated*.
   - No subscription and official GSPro support.
   - Its weak points are exactly our planned differentiators: club stickers, estimated face, outdoor bright-sun spin variance, thin software, and very poor customer support (1.44/5 in the owner survey for the original Square).
3. **Rapsodo is doubling down on subscriptions.** The **MLM2XPRO** launches **Oct 15, 2026** at **$899.99**:
   - Core costs $199.99/yr and adds a new $399.99/yr "Studios" tier.
   - The trial is cut from 45 days to 21.
   - Measured spin still needs RPT balls ($69.99 a dozen).
   - Third-party simulators (GSPro and others) require a paid Rapsodo membership on top of the simulator licence.
4. **Bushnell raised Gold from $499 to $599/yr (Sept 18, 2026).** Gold is required for GSPro. Meanwhile FlightScope, Square, OpenLaunch, Voice Caddie and PRGR all market "no subscription". Subscription fatigue is the loudest buyer complaint and an open opportunity.
5. **There is no first-party unit-sales data for any budget brand.**
   - The best ownership proxy is the r/Golfsimulator-sourced Yardstick survey (~650–684 responses). By share of respondents: R10 15.5%, SkyTrak 10.4%, Bushnell Launch Pro 9.9%, MLM2PRO 5.8%, Mevo+ 5.6%, Square 5.0%.
   - Market-size reports put the whole launch-monitor market at roughly **$190–310M in 2025, growing 8.5–9.8% a year**. The consumer segment is about $132M (GMI).

---

## 1. Master comparison table (budget tier + edge-of-tier)

Abbreviations:
- **DTL** = down-the-line, behind the ball.
- **Side** = beside the ball, facing the golfer.
- **M** = measured; **C** = calculated or estimated.
- **"Sub for 3rd-party"** = whether the manufacturer charges you before GSPro/E6 will connect (the simulator licence is extra in every case).

| Product | Street price (Oct 2026) | Tech | Placement / depth | Spin | Club data | Sub for 3rd-party? | GSPro |
|---|---|---|---|---|---|---|---|
| **Rapsodo MLM2XPRO** (new, Oct 15) | $899.99 | Doppler + 2 cameras | DTL, ~14.5 ft+ (UNVERIFIED for X; same as 2PRO assumed) | M **only with RPT balls** | Path, AoA (M); no face | **Yes** (Core $199.99/yr) | Yes (listed) |
| **Rapsodo MLM2PRO** | $549.99 sale / $699.99 list | Doppler + 2 cameras | DTL 6.5–8.5 ft + 8 ft flight | M only with RPT balls | Path, AoA; no face | **Yes** (Premium $199.99/yr, $599.99 lifetime) | Yes, Premium required |
| **Garmin Approach R10** | $499.99 (list $599.99); CPO $399.99 | Doppler radar only | DTL 6–8 ft + 8 ft flight | C indoors (M outdoors >20 m flight; RCT balls help) | Path, face, AoA all **C** | CONFLICT: likely no (see §3) | Yes |
| **Square Golf (Home)** | $699.99 | 2 cameras (photometric) | Side, ~10 ft room | M, **needs marked balls** | Path, face, dyn loft, AoA; club marker | No | Yes |
| **Square Golf Omni** | $1,599 | 4 IR cameras, IR illuminators | Side, no ball-flight minimum | M, **markerless** | Path, AoA, impact (M with stickers); face, dyn loft (C) | No | Yes (official) |
| **FlightScope Mevo Gen2** | $1,299 | Radar + camera "Fusion" | DTL 7–9 ft + 8 ft flight | M with metallic dots/RCT indoors | AoA, spin loft base; path/face/dyn loft = Pro Package $699–1,000; impact = $350–499 | No | Yes |
| **FlightScope Mevo+** (final sales phase) | $1,099 | Radar + camera "Fusion", 24 GHz | DTL 7–9 ft + 8–13 ft flight | M with dots/RCT indoors (disputed) | Same paywall as Gen2 | No | Yes |
| **FlightScope Mevo** (orig., discontinued) | ~$349 (2024) | 24 GHz radar | DTL 4–7 ft + 8 ft | M (claimed); dots indoors | Club speed only | No | No |
| **Swing Caddie SC4 Pro** | $499–599.99 | 24 GHz radar | DTL 5 ft + ~8–10 ft | C (per reviewers) | None (speed, smash) | No | **No** |
| **Swing Caddie SC300i** | $399.99 | 24 GHz radar | DTL 5 ft | C | None | n/a (no sim support) | No |
| **Swing Caddie SC200 Plus** | $279.99 | 24 GHz radar | DTL 4–5 ft | none | None | n/a | No |
| **PRGR HS-130A "Black"** | $199.99 | 24 GHz radar | DTL ~4.5 ft | none | Club speed only | n/a | No |
| **Ernest ESB1 REV-D** | $199.99 | Doppler | DTL 4–6 ft | C | None | n/a | No |
| **Ernest Tour Plus 2.0** | $999.99 direct (IGP $1,995) | 2 IR cameras + 4 Doppler | Side | Appears M (logo must face unit) | Path, face, AoA, dyn loft, spin loft | No | Not mentioned |
| **Bushnell LPi** | $1,999.99 (sold out; $999 briefly Sept 2026) | 3 cameras (GC3 hardware) | Side | M, markerless | Path, AoA with fiducial stickers; no face | **Yes** (Gold $599/yr for GSPro) | Yes, Gold required |
| **Golfzon WAVE** | ~$2,750 new (eBay) / ~$1,620 used | 24 GHz 3-ch radar + camera | DTL 6.5–8.2 ft + 8 ft | Unclear; weakest metric in GCQuad test | Many listed, "not reliably precise" | Own subs $19–399/yr | **No** (as of Jan 2024) |
| **Uneekor EYE MINI LITE** | $1,999 (sale; list $2,749) | 2 IR cameras | Side | M, markerless | Path, speed, AoA with stickers; no face | **Yes** (Pro $199/yr for connector) | Yes, Pro required |
| **SkyTrak+** (clearance) | $1,075–1,195 | Camera + dual Doppler | Side, 18 in from ball | M (camera), markerless | Speed, face, path (no AoA) | Plans $99.99–599.99/yr | Official ended for new buyers |
| **Blue Tees Rainmaker** (2026) | $599 | Phased-array Doppler | DTL 5 ft + ~8 ft | C (likely) | Path, AoA (C) | $79/yr after year 1 (CONFLICT) | Yes |
| **Shot Scope LM1** (2026) | $199.99 | Doppler | DTL ~5 ft | none | Club speed only | None | No |
| **Garmin Approach G82** (2026) | $599.99 | Doppler, speed-only | Side, 12 in from ball | none | Club speed, tempo | n/a | No |
| **OpenLaunch Nova** | $1,500 | UNVERIFIED (side unit) | Side | Reported, method UNVERIFIED | UNVERIFIED | No | Yes |
| **OptiShot 2** | ~$500 (discontinued) | 16 IR sensors in floor pad | Pad, any space | none (all C) | Club speed, path, face (C) | n/a | No |
| **Phigolf 2 / Flex** | $263–329 | Bluetooth motion sensor on stick | No ball | none | Speed, path, face, AoA (C) | No | No |
| **PiTrac** (DIY, open source) | ~$300–400 parts | 2 global-shutter IR cameras + IR strobe, Pi 5 | Side, indoor only | M (photometric), markerless | None | Free | Yes (OpenConnect) |

---

## 2. Rapsodo

### 2a. Rapsodo MLM2PRO (2023 – current)

**Price**
- List $699.99. On sale for **$549.99** "through October 7th" 2026 ([Rapsodo](https://rapsodo.com/products/mlm2pro-mobile-launch-monitor-golf-simulator)).
- Retailers still commonly show $599.99, or $699.99 bundled with Premium ([Golfie Shop](https://golfieshop.com/products/rapsodo-mlm2pro-premium-membership), [Bighorn Golfer](https://bighorngolfer.com/products/rapsodo-mlm2pro%E2%84%A2-plus-premium-membership)).
- Europe: €599.99, down from €749.99 ([Rapsodo EU](https://rapsodo.eu/products/mlm2pro-mobile-launch-monitor-golf-simulator)).
- Launch: 2023 at $699.99. MyGolfSpy named it "best value personal launch monitor for 2023" ([MyGolfSpy](https://mygolfspy.com/reviews/golf-technology/rapsodo-mlm2pro-personal-launch-monitor-review/), page 403; quote via search snippet). The exact launch month is UNVERIFIED.

**Technology** ([Rapsodo](https://rapsodo.com/products/mlm2pro-mobile-launch-monitor-golf-simulator))
- "Two advanced cameras plus Doppler Radar": one camera for shot and swing video, one for ball and Impact Vision.
- Impact Vision runs at **240 fps**.
- Radar frequency and chip are not published (UNVERIFIED). The sensing frame rate for spin is not published.
- Spin is read optically from the printed **RPT** pattern on the ball.

**Placement and space**
- DTL, **6.5–8.5 ft behind the ball, plus 8 ft ball-to-net**, for "a little more than 14 total feet" ([Rapsodo](https://rapsodo.com/products/mlm2pro-mobile-launch-monitor-golf-simulator); [24/7 Golf help](https://help.247.golf/en-US/how-much-room-do-i-need-to-set-up-my-mlm2pro-(indoornet)-223758)).
- PlayBetter recommends 13 ft ball-to-screen, for a comfortable room of **10 W × 21.5 D × 9 H ft** ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-space/rapsodo-mlm2pro-home-golf-simulator-space-requirements)).

**Metrics: 15** ([Rapsodo](https://rapsodo.com/products/mlm2pro-mobile-launch-monitor-golf-simulator))

| Measured (8) | Calculated (7) |
|---|---|
| Ball speed | Carry |
| Club speed | Total |
| Launch angle | Side carry |
| Launch direction | Smash factor |
| Spin rate (RPT only) | Descent angle |
| Spin axis (RPT only) | Apex |
| Club path | Shot type |
| Angle of attack | |

- **Spin needs special balls.** "Golf balls with RPT are required to show spin numbers." Standard balls get no spin at all ([Rapsodo](https://rapsodo.com/products/mlm2pro-mobile-launch-monitor-golf-simulator)).
- Three RPT balls come in the box; a dozen costs **$69.99**.
- The FAQ references "Callaway RPT Chrome Soft X" while the product copy lists Pro V1 and Chrome Tour RPT, a minor inconsistency.

**Club data**
- Path and attack angle only, and both are Premium-gated.
- **No face angle, face-to-path, dynamic loft or impact location** ([Yardstick survey sheet](https://docs.google.com/spreadsheets/d/1XnXNXh4zo4ugafKzMNKTl7Kbtrdg4ewAqiBHX7vQwAE/edit?gid=1954495530)).
- Impact Vision is a 240 fps video of impact, not a measured impact-location metric.

**Accuracy**
- **Plugged In Golf (vs GCQuad):**
  - Ball speed "always +/- 1 MPH and was often an exact match".
  - Carry "never more than +/- 3 yards".
  - Launch "almost always within 1 degree".
  - With RPT balls, spin was within 200 rpm of the Foresight on every shot ([Plugged In Golf](https://pluggedingolf.com/rapsodo-mlm2pro-launch-monitor-review/)).
- **Breaking Eighty (vs TrackMan, indoors, RPT):** wedge and 7-iron carry differed by under 2 yd on average; driver by about 5 yd ([Breaking Eighty via search](https://breakingeighty.com/rapsodo-mlm-2-pro-review)).
- **Golf Simulator Nerd:** driver spin varies "up to 10 to 15%" on high-spin shots ([GSN](https://www.golfsimulatornerd.com/blog/rapsodo-mlm2-pro-review-2026)).
- **MyGolfSpy forum tester (vs TrackMan):** launch angle "seemed to have a large delta" ([MGS forum via search](https://forum.mygolfspy.com/topic/65788-rapsodo-mlm2pro-2024-forum-review/)).
- **Owner survey** (out of 10): distance 8.44, shot shape 8.59, chipping 6.4, putting 0.7 ([Yardstick](https://docs.google.com/spreadsheets/d/1XnXNXh4zo4ugafKzMNKTl7Kbtrdg4ewAqiBHX7vQwAE/edit?gid=1954495530)).

**Subscription (Premium)** ([Rapsodo Premium](https://rapsodo.com/pages/rapsodo-golf-mlm2pro-premium-membership))

| Plan | Price | Notes |
|---|---|---|
| 1-year | **$199.99/yr** | Auto-renews |
| 2-year | **$329.99** | "Offer ends 10/14" |
| Lifetime | **$599.99** | "Offer ends 10/14"; lifetime has been priced at $300–$500 in past promotions ([GolfWRX via search](https://forums.golfwrx.com/topic/2029058-rapsodo-mlm2-pro-lifetime-subscription/)) |

- A 45-day trial requires a card.
- **Premium-gated:** "speed training, club data and full-course access". The list includes spin rate and spin axis, club path, AoA, Impact Vision, 30K+ courses, R-Cloud and third-party compatibility.
- **Free tier:** an owner says "I can only get 3 readouts per swing" without Premium ([Rapsodo reviews](https://rapsodo.com/products/mlm2pro)).
- **Third-party simulators need Premium.** GSPro's site says "The MLM2Pro requires a Premium Membership from Rapsodo" ([GSPro](https://gsprogolf.com/)).
- **GSPro running cost:** Premium plus GSPro is about **$450/yr**, and you must sign in through the Rapsodo app every 24 hours before launching GSPro ([Top Shelf](https://topshelfgolf.com/blogs/golf/how-to-set-up-mlm2pro-with-gspro)).

**Simulator compatibility:** GSPro, E6 Connect/Apex and Awesome Golf, all via Premium ([Rapsodo](https://rapsodo.com/products/mlm2pro-mobile-launch-monitor-golf-simulator)). GSPro and E6 bridge through the phone app, which adds some latency ([GSN](https://www.golfsimulatornerd.com/blog/rapsodo-mlm2-pro-review-2026)).

**Battery and outdoor**
- Rapsodo publishes no battery spec. GSN says about 4 hours, over USB-C ([GSN](https://www.golfsimulatornerd.com/blog/rapsodo-mlm2-pro-review-2026)); UNVERIFIED.
- Works outdoors. Bright sun and low-contrast backgrounds hurt camera tracking (GSN).

**Complaints**
- **Subscription is the #1 complaint.** 92% of survey owners say a sub is required ([Yardstick](https://docs.google.com/spreadsheets/d/1XnXNXh4zo4ugafKzMNKTl7Kbtrdg4ewAqiBHX7vQwAE/edit?gid=1954495530)).
  - "The additional $200 annually isn't worth it" ([Rapsodo reviews](https://rapsodo.com/products/mlm2pro)).
  - "your LIFETIME subscription is only transferable before the end of the year" ([Trustpilot](https://www.trustpilot.com/review/rapsodo.com)).
- **RPT ball cost and durability:** "poor performance and durability from the new proV1 RPT balls" ([Trustpilot](https://www.trustpilot.com/review/rapsodo.com)).
- **Connectivity:**
  - "always a challenge to get it connected" ([Rapsodo reviews](https://rapsodo.com/products/mlm2pro)).
  - "Even with the bluetooth extender it is not useable for sim golf. It will constantly disconect" (May 2026, [Trustpilot](https://www.trustpilot.com/review/rapsodo.com)).
- **Lefty: CONFLICT among owners.** One says it lets "left or right handed players play without any adjustment"; another says it "will not pick up some shots… most for left handers" ([Rapsodo reviews](https://rapsodo.com/products/mlm2pro)).
- **Spin trust:** a Trustpilot reviewer calls the "measured" spin "completely fabricated".
- **Would buy again:** 75% of survey owners.

### 2b. Rapsodo MLM2XPRO (NEW: orders open Oct 15, 2026)

**Price**
- **$899.99**, including 12 RPT balls (Titleist 2025 Pro V1 or Callaway 2026 Chrome Tour) ([Rapsodo](https://rapsodo.com/products/mlm2xpro-golf-launch-monitor-simulator); [GlobeNewswire, Oct 1 2026](https://www.globenewswire.com/news-release/2026/10/01/3373058/0/en/rapsodo-unveils-new-golf-ecosystem-led-by-as-real-as-it-gets-rapsodo-studios-and-mlm2xpro.html)).
- Pre-orders at [PlayBetter](https://www.playbetter.com/products/rapsodo-mlm2xpro-golf-launch-monitor-simulator).
- No trade-in programme ([Golficity](https://golficity.com/first-look-rapsodo-mlm2xpro-adds-putting-faster-performance-more/)).

**Technology** ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/10/01/3373058/0/en/rapsodo-unveils-new-golf-ecosystem-led-by-as-real-as-it-gets-rapsodo-studios-and-mlm2xpro.html); [Rapsodo](https://rapsodo.com/products/mlm2xpro-golf-launch-monitor-simulator))
- Same "dual-camera and Doppler radar" architecture as the MLM2PRO.
- Impact Vision at 240 fps; retailer copy claims "2X more detailed Impact Vision".

**What's new**
- Simulation **putting**, a first for Rapsodo.
- "2X faster shot-to-show".
- A top LED/LCD screen showing level, connection and battery.
- A new adjustable tripod and a revised Wi-Fi connection flow.

**Metrics:** 15, the same split as the MLM2PRO. Spin rate and spin axis are measured "with RPT balls" ([Rapsodo](https://rapsodo.com/products/mlm2xpro-golf-launch-monitor-simulator)). Still no face angle.

**Memberships (new structure)** ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/10/01/3373058/0/en/rapsodo-unveils-new-golf-ecosystem-led-by-as-real-as-it-gets-rapsodo-studios-and-mlm2xpro.html))

| Tier | Price | Includes |
|---|---|---|
| Free | $0 | "Basic outdoor range practice, 11 metrics" |
| Core | **$199.99/yr** | 15 metrics, 30K+ courses on mobile and PC, 2 profiles |
| Studios | **$399.99/yr** | Adds 25 4K PC courses (Bethpage Black, Tobacco Road, Quail Hollow) and 4 profiles |

- The trial is cut to **21 days**, from the MLM2PRO's 45.

**Simulator compatibility:** GSPro, E6 Apex/Connect and Awesome Golf ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/10/01/3373058/0/en/rapsodo-unveils-new-golf-ecosystem-led-by-as-real-as-it-gets-rapsodo-studios-and-mlm2xpro.html)). Membership gating for the X is UNVERIFIED but almost certainly the same as for the 2PRO.

**Not published:** space requirements, battery life, lefty handling.

**Strategic read:** Rapsodo is moving *up* in software (a PC app, 4K courses, a $399.99 tier) while keeping RPT-ball spin. It is trying to become a platform with recurring revenue, not a hardware vendor.

---

## 3. Garmin

### 3a. Garmin Approach R10 (2021 – current; no successor announced)

**Price**
- List **$599.99**; usually **$499.99** ([Breaking Eighty, Aug 2026](https://breakingeighty.com/garmin-approach-r10-review); [Rain or Shine](https://rainorshinegolf.com/blogs/product-comparisons-reviews/garmin-r10-launch-monitor-review)).
- Certified pre-owned **$399.99** ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/certified-pre-owned-garmin-r10-plus-home-tee-hero-upgrades)).
- Launched 2021 ([Nasdaq, Aug 2021](https://www.nasdaq.com/articles/garmin-grmn-strengthens-outdoor-segment-with-approach-r10-2021-08-11)).
- No R10 successor as of Oct 2026. Garmin's 2026 golf launches were the G82 handheld and R10 software updates ([Garmin newsroom](https://www.garmin.com/en-US/newsroom/press-release/outdoor/introducing-the-approach-g82-the-ultimate-warmup-tool-with-garmins-largest-golf-handheld-display-and-new-putting-metrics/); [Golf Monthly](https://www.golfmonthly.com/news/garmin-has-revealed-two-clever-new-golf-gps-devices-for-2026)).

**Technology**
- Doppler radar only, no camera. Band and chip are UNVERIFIED.
- 88.5 × 70 × 25 mm, 148 g, IPX7 ([MyGolfSimulator](https://mygolfsimulator.com/garmin-r10-data/)).

**Placement and space**
- DTL **6–8 ft behind the tee, tee at least 8 ft from the net** ([Garmin manual](https://www8.garmin.com/manuals/webhelp/GUID-E2BBF6BE-4276-436F-B697-59ABEFD61933/EN-US/GUID-88F65277-47D4-403D-8F79-719CAA256D6B.html)).
- Rain or Shine says at least 15 ft of room length and a 9 ft ceiling ([Rain or Shine](https://rainorshinegolf.com/blogs/product-comparisons-reviews/garmin-r10-launch-monitor-review)).
- Indoors, the unit must sit level with the ball on a raised mat ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/garmin-approach-r10-review-golf-launch-monitor-under-1000)).

**Metrics**
- **Directly measured (4):** club speed, ball speed, launch angle, launch direction ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/garmin-approach-r10-review-golf-launch-monitor-under-1000)).
- **Calculated:** spin rate, spin axis, carry, total, club path, face angle, face-to-path, AoA, apex, smash, deviation ([MyGolfSimulator](https://mygolfsimulator.com/garmin-r10-data/)).
- **Stated tolerances:** ball speed ±1 mph, club speed ±3 mph (some sources say ±5), launch ±1°, carry ±5 yd, face ±2°.

**Spin behaviour**
- Spin is measured only when the radar sees the ball for more than about 20 m and above about 90 mph. Otherwise a machine-learned model estimates it ([MyGolfSimulator](https://mygolfsimulator.com/garmin-r10-data/)).
- Italic values in the app mark estimated numbers.
- Indoors, "every R10 spin number is calculated" ([Fore-ward Thinking](https://forewardthinking.com/learn/garmin-r10-reads-short-indoors.html)).
- Firmware 4.30 added **Titleist RCT** ball support. Garmin claims "up to 30x better spin accuracy and 50% better carry accuracy indoors"; this is a manufacturer claim.
- Garmin says metallic dots can *hurt* accuracy; some users disagree. CONFLICT ([search summary of Garmin forum threads](https://forums.garmin.com/outdoor-recreation/golf/f/approach-r10/318374/is-ball-spin-calculated-or-directly-measured)).

**Club data:** path, face and AoA are all calculated. There is no dynamic loft and no impact location. No markers are used.

**Accuracy**
- **MyGolfSpy:** with normal balls, R10 spin was off by "hundreds of rpm on drivers and thousands on irons and wedges… almost meaningless". Carry still came within 3–4% of a GCQuad (search snippet; [MyGolfSpy](https://mygolfspy.com/reviews/golf-technology/garmin-approach-r10-launch-monitor-review/), page 403).
- **PlayBetter (vs GC3):**
  - Short clubs within 1–2 yd; driver sometimes 8–10 yd off.
  - Deviation "consistently off by about 10 or 15 yards".
  - Under 3% missed shots ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/garmin-approach-r10-review-golf-launch-monitor-under-1000)).
- **Garmin forum user (RCT balls vs GCQuad):** backspin within ±50 rpm, but **sidespin reads ½ to ⅔ low** (search summary).
- **Owner survey** (out of 10): distance 7.57, shot shape 5.89, chipping 5.52, **putting 0.99**. Shot delay 2–4 s ([Yardstick](https://docs.google.com/spreadsheets/d/1XnXNXh4zo4ugafKzMNKTl7Kbtrdg4ewAqiBHX7vQwAE/edit?gid=1954495530)).

**Subscription**
- Garmin Golf membership costs **$9.99/mo or $99.99/yr**.
- It unlocks Home Tee Hero (43K+ courses, 15 "Enhanced" courses, on-course practice). A standalone HTH app for the R10 shipped in Jan 2026 ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/certified-pre-owned-garmin-r10-plus-home-tee-hero-upgrades); [Breaking Eighty](https://breakingeighty.com/garmin-approach-r10-review)).
- Five E6 Connect courses are included.
- **CONFLICT: is the membership needed for third-party simulators?**
  - HomeGolfHero says no ([HomeGolfHero](https://homegolfhero.com/guides/garmin-home-tee-hero-review/)).
  - Breaking Eighty and Rain or Shine say yes ([B80](https://breakingeighty.com/garmin-approach-r10-review); [Rain or Shine](https://rainorshinegolf.com/blogs/product-comparisons-reviews/garmin-r10-launch-monitor-review)).
  - GSPro lists no extra prerequisite for the R10 ([GSPro](https://gsprogolf.com/)).
  - Only 6% of R10 owners in the survey say a sub is required.
  - Best evidence: **not required for GSPro**. Verify on a unit before relying on it.

**Simulators:** GSPro (official), E6 Connect/Apex, Awesome Golf, TGC 2019, Creative Golf ([GSPro](https://gsprogolf.com/); [Breaking Eighty](https://breakingeighty.com/garmin-approach-r10-review)). The most-used software among survey owners is E6.

**Battery and outdoor**
- Up to **10 hours**; works outdoors ([MyGolfSimulator](https://mygolfsimulator.com/garmin-r10-data/)).
- **CONFLICT on charging port:** MyGolfSimulator says micro-USB; Rain or Shine says USB-C.

**Complaints**
- The app is "in desperate need of an overhaul" (B80).
- You "eyeball" the alignment; there is no camera aid.
- Spin and deviation can't be trusted without RCT balls, and none are included.
- The case is "10 times larger than the device".
- Only three metrics show at once (PlayBetter).
- Driver distance reads short indoors (Fore-ward Thinking).
- **Would buy again:** 65% of survey owners. **Customer support:** 3.85/5.

**Sales proxy**
- About **1,000 units/month on Amazon US** at $399.98 (April 2026, AsInsight scraper estimate, low confidence) ([AsInsight](https://www.asinsight.com/report/US/launch-monitor-golf)).
- 4.2★ from about 1.1K Amazon reviews ([Amazon](https://www.amazon.com/Garmin-Approach-Portable-Monitor-Indoors/dp/B095QX1FSR)).
- The most-owned device in the r/Golfsimulator survey, at 15.5% of respondents.

### 3b. Garmin Approach G82 (Jan 2026)

**Price:** **$599.99** ([Garmin newsroom](https://www.garmin.com/en-US/newsroom/press-release/outdoor/introducing-the-approach-g82-the-ultimate-warmup-tool-with-garmins-largest-golf-handheld-display-and-new-putting-metrics/); [PlayBetter](https://www.playbetter.com/products/garmin-approach-g82-launch-monitor-golf-gps)).

**Technology and placement**
- A GPS handheld with speed-only Doppler radar.
- Sits on a magnetic stand **12 in from the ball**, perpendicular to the line. For putting, 6 in off the line ([Plugged In Golf](https://pluggedingolf.com/garmin-approach-g82-gps-launch-monitor-review/)).

**Metrics**
- **Measured:** club speed, ball speed, tempo, putting stroke.
- **Calculated:** carry and total.
- No spin and no launch angle.
- Garmin's tolerances: ±5 mph club, ±2 mph ball, ±5 yd carry.

**Accuracy and use**
- Driver reads about 10 yd short vs a Mevo Gen2 (Plugged In).
- No simulator support. Battery: 25 h GPS / 8 h radar.
- Not a simulator competitor; it shows Garmin moving radar into on-course devices.

---

## 4. Square Golf (Korea)

### 4a. Square Golf launch monitor ("Home", original)

**Price:** **$699.99** ([Shop Indoor Golf](https://shopindoorgolf.com/products/square-golf-launch-monitor)). Average price paid in the survey: $704 ([Yardstick](https://docs.google.com/spreadsheets/d/1XnXNXh4zo4ugafKzMNKTl7Kbtrdg4ewAqiBHX7vQwAE/edit?gid=1954495530)).

**Technology and placement**
- Photometric, with **two** cameras ([Golf Online UK](https://www.golfonline.co.uk/square-golf-omni-launch-monitor-review)).
- Side of the ball. Hitting zone 15 × 15 cm. **Indoor only** ([Shop Indoor Golf](https://shopindoorgolf.com/products/square-golf-launch-monitor)).
- About 10 ft total depth per the survey sheet.

**Metrics** ([Shop Indoor Golf](https://shopindoorgolf.com/products/square-golf-launch-monitor))
- **Ball:** ball speed, direction, launch angle, spin, apex, carry, run, total.
- **Club:** path, face angle, dynamic loft, AoA.
- **Needs marked balls** (3 dotted balls included) and a club marker.
- No club speed or smash. Those came with the Omni ([Golf Online UK](https://www.golfonline.co.uk/square-golf-omni-launch-monitor-review)).

**Subscription and simulators**
- No subscription.
- GSPro (official, free connection) and E6 Connect ([GSPro](https://gsprogolf.com/); [PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/square-omni-indoor-outdoor-launch-monitor-review)).
- Native app with about 10 courses.

**Battery:** about 8 h, removable.

**Owner sentiment** ([Yardstick](https://docs.google.com/spreadsheets/d/1XnXNXh4zo4ugafKzMNKTl7Kbtrdg4ewAqiBHX7vQwAE/edit?gid=1954495530))
- **Would buy again: 97%**, the highest of any device.
- **Customer support: 1.44/5**, the lowest of any device.
- Accuracy scores out of 10: distance 8.29, shape 7.97, **chipping 8.62, putting 8.21**. These are the best short-game scores in the survey, a camera-unit advantage.
- "Square Golf is notoriously hard to reach" ([Breaking Eighty](https://breakingeighty.com/square-omni-launch-monitor)).

### 4b. Square Golf Omni (unveiled at the 2026 PGA Show, shipping 2026)

**Price and availability**
- **$1,599** US ([Shop Indoor Golf / PlayBetter / Rain or Shine via search](https://www.playbetter.com/products/square-golf-omni-indoor-outdoor-launch-monitor); [northcourse](https://northcourse.golf/products/square-golf-omni)); **£1,599.99** UK.
- Preorders opened Mar 16, 2026; units were shipping by Oct 2026 (search summary).
- **CONFLICT:** one PlayBetter listing still says "Late Fall 2026" preorder ([PlayBetter](https://www.playbetter.com/products/square-golf-omni-indoor-outdoor-launch-monitor)).

**Technology**
- **Four high-speed infrared cameras, stacked vertically on the front, with IR illuminators.** Photometric, no radar ([Golf Online UK](https://www.golfonline.co.uk/square-golf-omni-launch-monitor-review); [Golf Monthly](https://www.golfmonthly.com/reviews/golf-tech-and-training-aids/square-golf-omni-launch-monitor-review)).
- Frame rate not published.
- Built-in LCD (about 1 s delay), aluminium chassis, IP44, operating range 0–40 °C ([Golfers Authority](https://golfersauthority.com/square-omni-launch-monitor/); [Lasco Press](https://www.thelascopress.com/2026/05/square-golf-omni-review/)).

**Placement and space**
- Side of the ball. **Ready zone 10 × 10 in**, and the ball must sit in the front half (about 5 in of depth) for club data.
- **No minimum ball-flight distance** ([Friendly Golfer](https://friendlygolfer.com/square-golf-omni-review/); [Lasco Press](https://www.thelascopress.com/2026/05/square-golf-omni-review/)).
- One retailer says 12 ft room depth minimum (search summary; UNVERIFIED).

**Metrics (20+)**

| Group | Metrics | How obtained |
|---|---|---|
| Ball | Ball speed, launch angle, launch direction, backspin, sidespin, total spin, spin axis | Measured from images, **no marked balls** |
| Ball flight | Apex, carry, roll, total, descent, hang time, side carry | Modelled |
| Club (shaft sticker) | Club path, AoA | **Measured** |
| Club (both stickers) | Club speed, impact point | **Measured** |
| Club (shaft sticker) | **Face angle, dynamic loft** | **Estimated**; Square discloses this ([Lasco Press](https://www.thelascopress.com/2026/05/square-golf-omni-review/)) |

- Sources: [Golf Online UK](https://www.golfonline.co.uk/square-golf-omni-launch-monitor-review); [Golfers Authority](https://golfersauthority.com/square-omni-launch-monitor/); [Lasco Press](https://www.thelascopress.com/2026/05/square-golf-omni-review/).
- **Club stickers are required for all club data;** there is no stickerless option ([Friendly Golfer](https://friendlygolfer.com/square-golf-omni-review/)). Golfers Authority calls stickering a full bag a "real inconvenience".

**Specified ranges** ([Lasco Press](https://www.thelascopress.com/2026/05/square-golf-omni-review/))
- Ball speed 4–200 mph (putting 1–45).
- Backspin −4,000 to 12,000 rpm; sidespin ±7,000.
- Launch −10° to 70°; launch direction ±15°.
- Club speed 0–140 mph; path and AoA ±20°; impact ±40 mm.

**Accuracy**
- **Friendly Golfer (vs GCQuad):**
  - Backspin "generally within about 200 RPM"; sidespin "usually within about 300 RPM".
  - Wedge path sometimes read out-to-in when the GCQuad said in-to-out.
  - AoA sometimes "off by a few degrees" ([Friendly Golfer](https://friendlygolfer.com/square-golf-omni-review/)).
- **Breaking Eighty:** spin within "300 RPM at most on well-struck shots", with more variance on driver indoors ([B80](https://breakingeighty.com/square-omni-launch-monitor)).
- **Golfstead:** spin axis "a bit wonky", club data "less reliable" ([Golfstead](https://golfstead.com/square-golf-omni-launch-monitor-review)).
- **Lasco Press:** wrong launch angle on fully-open flop and sand shots; desktop crashes (an early unit) ([Lasco Press](https://www.thelascopress.com/2026/05/square-golf-omni-review/)).
- **Outdoors:** spin "may be less consistent in bright sun" ([Golf Online UK](https://www.golfonline.co.uk/square-golf-omni-launch-monitor-review)). Golf Monthly would recommend it "only to people who will use it solely indoors" (search summary of [Golf Monthly](https://www.golfmonthly.com/reviews/golf-tech-and-training-aids/square-golf-omni-launch-monitor-review)).

**Cost structure**
- **No subscription.** Practice modes are free.
- Native course play uses **credits**: 1,000 included (1 credit per hole per player, about 55 rounds). About 1,000 more cost about $20 ([Golfstead](https://golfstead.com/square-golf-omni-launch-monitor-review); [Golf Online UK](https://www.golfonline.co.uk/square-golf-omni-launch-monitor-review)).
- **Third-party simulators:** GSPro (official, "seamless" auto-connect), E6 Connect, Awesome Golf. No Square unlock fee.
- **3-year cost with GSPro:** about $2,350 ([Golfers Authority](https://golfersauthority.com/square-omni-launch-monitor/)).

**Battery:** removable Li-ion, about **6 h**.

**Lefty:** a button switches L/R mode ([Lasco Press](https://www.thelascopress.com/2026/05/square-golf-omni-review/)), but the unit must be moved to the other side ([Friendly Golfer](https://friendlygolfer.com/square-golf-omni-review/)).

**Complaints** ([Golf Monthly](https://www.golfmonthly.com/reviews/golf-tech-and-training-aids/square-golf-omni-launch-monitor-review); [Friendly Golfer](https://friendlygolfer.com/square-golf-omni-review/); [Golfers Authority](https://golfersauthority.com/square-omni-launch-monitor/))
- Stickers, and shaft stickers peel.
- Screen too low and small.
- No case.
- Basic or "clunky" software.
- Light sensitivity.
- "Limited lateral range".
- Typos in packaging and manual.

**Verdict:** reviewers call it a "genuine market disruptor" ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/square-omni-indoor-outdoor-launch-monitor-review)) and "Outstanding Accuracy for the Money" ([Breaking Eighty](https://breakingeighty.com/2026-launch-monitors)).

---

## 5. FlightScope (Mevo family)

### 5a. Mevo (original, 2017)

**Price and status**
- Launched **2017 at $499** ([FlightScope guide](https://flightscope.com/blogs/blogs/the-complete-guide-to-flightscope-launch-monitors)).
- Its product page now returns 404; the unit appears only as a trade-in.
- About $349 street in 2024 testing ([MyGolfSpy via search](https://mygolfspy.com/buyers-guides/all/best-launch-monitors-under-500/)).

**Technology and placement**
- 3D Doppler at **24.075–24.175 GHz**, per its FCC filing ([fccid.io QXP-A7310](https://fccid.io/QXP-A7310)). Bluetooth 4.0.
- DTL, 4–7 ft behind the ball plus 8 ft of flight. Practical Golf says accuracy suffers below about 12–15 ft total ([Practical Golf](https://practical-golf.com/flightscope-mevo-review)).

**Metrics:** 8 — carry, ball speed, club speed, smash, spin, launch, apex, flight time.
- No horizontal launch and no spin axis.
- Metallic stickers are needed indoors ([FlightScope FAQ](https://flightscope.com/pages/faq)).

**Accuracy:** high driver carry and spin; launch angle the weakest metric ([Practical Golf](https://practical-golf.com/flightscope-mevo-review)).

**Subscription and battery:** none; no simulator courses. Battery about 2 h.

### 5b. Mevo+ (2020; "final sales phase" in 2026)

**Price**
- Launched Jan 2020 at **$1,999** ([FlightScope PR](https://flightscope.com/flightscope-to-introduce-mevo-at-2020-pga-merchandise-show/)); later $2,299.
- Now **$1,099** ([FlightScope](https://flightscope.com/products/mevo-plus)).
- **CONFLICT:** a July 2026 Breaking Eighty update says it's no longer sold, but FlightScope still lists it.

**Technology:** "Fusion Tracking" (3D Doppler plus synchronized image processing), 24.08–24.16 GHz ([manual PDF](https://cdn.shopify.com/s/files/1/0041/6386/2626/files/Top-Shelf-Golf-FlightScope-Mevo-Plus-User-Manual.pdf?87163=)). Channel count unpublished.

**Placement and space**
- DTL 7–9 ft plus 8–13 ft of flight ([FlightScope](https://flightscope.com/products/mevo-plus)).
- Breaking Eighty uses 15–16 ft minimum ([B80](https://breakingeighty.com/flightscope-mevo-plus-review)). The survey sheet lists 16 ft.

**Metrics:** ball and club speed, smash, carry, launch, spin, apex, flight time, AoA, spin loft, launch direction, spin axis, roll, total, lateral, shot type, plus putting.

**Spin and markers**
- Indoors, **aluminium dots or RCT balls are "required for accurate spin"**; 100 dots are included.
- Measured-vs-calculated is not published. Italic values in the app indicate estimates.
- Forum users report:
  - Measured spin on only about 30–40% of shots with one dot.
  - RCT balls sometimes reading double the true spin.
  - Spin axis possibly calculated indoors.
  - Disputed; patent US10775492B2 claims direct measurement ([Golf Simulator Forum](https://golfsimulatorforum.com/forum/flightscope/360576-mevo-spin-measured-vs-calculated)).

**Club data:** base unit gives club speed, AoA and spin loft. Path, face and dynamic loft need the **Pro Package** (see 5d).

**Subscription and simulators**
- No subscription.
- Lifetime E6 bundle (12 courses).
- GSPro, TGC 2019, Awesome Golf, Creative ([FlightScope](https://flightscope.com/products/mevo-plus)).

**Battery:** about 3 h (1.5 h in simulator use), mini-USB.

**Survey:** would buy again **60%**, the lowest of the major devices ([Yardstick](https://docs.google.com/spreadsheets/d/1XnXNXh4zo4ugafKzMNKTl7Kbtrdg4ewAqiBHX7vQwAE/edit?gid=1954495530)).

### 5c. Mevo Gen2 (Aug 4, 2025)

**Price**
- Launched at **$1,199** ([FlightScope PR](https://flightscope.com/blogs/news/flightscope-releases-mevo-gen2-the-most-complete-launch-monitor-and-simulator-on-the-market-and-its-under-1-200)).
- Now **$1,299** ([FlightScope](https://flightscope.com/products/mevo-gen2); [PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/flightscope-mevo-gen2-review)).

**Technology**
- The same Fusion engine as the Mevo+ and the X3C ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/flightscope-mevo-gen2-review)).
- Portrait chassis with kickstand; the app shows tilt and roll.
- Wi-Fi. USB-C, about **6 h** battery ([FAQ](https://flightscope.com/pages/faq)).

**Placement and space**
- DTL 7–9 ft plus 8 ft of flight ([FlightScope](https://flightscope.com/products/mevo-gen2)).
- Home Performance Lab: **16 ft minimum, 21 ft for rated accuracy** ([HPL](https://homeperformancelab.com/square-omni-vs-mevo-gen-2/)).

**Metrics:** 20 parameters, the Mevo+ set plus 3 putting metrics.
- FlightScope markets "no calculated estimates". Indoors, carry and apex are necessarily modelled, so treat this as marketing.
- **Metallic dots or RCT balls are required for accurate indoor spin.**

**Club data**
- Base unit: club speed, AoA, spin loft.
- Path, face, face-to-path and dynamic loft: **Pro Package**.
- Impact location: **Face Impact Location** add-on. Needs at least 300 lux; no club markers ([FAQ](https://flightscope.com/pages/faq)).

**Accuracy**
- **GolfBusters (vs GCQuad), as quoted by FlightScope:** 98–99% carry and spin accuracy; zero no-reads in 1,500 shots. Manufacturer-curated ([FlightScope blog](https://flightscope.com/blogs/blogs/best-golf-launch-monitor-comparison-2026)).
- **Breaking Eighty (vs TrackMan, indoors):** about 70% of shots within 1–2 yd and 200 rpm; some drives 5–7 yd and up to about 3,000 rpm off ([B80](https://breakingeighty.com/flightscope-mevo-gen-2)).
- **Carl's Place (outdoors, range markers):** stated average error 1.33%, worst drive 15.1 yd. Our recompute gives driver about 2.7%; the dealer gives no disclosure ([Carl's Place](https://www.carlofet.com/blog/carls-place-puts-flightscope-mevo-gen2-to-test-at-the-driving-range)).
- **MyGolfSpy:** 2025 Staff Pick ([FlightScope](https://flightscope.com/blogs/news/flightscope-mevo-gen2-named-mygolfspy-s-staff-pick-for-best-personal-launch-monitor-of-2025)).

**Subscription and simulators**
- **No subscription.**
- Lifetime E6 bundle (8 courses); 12-course pack $250 one-time.
- GSPro (official), Awesome Golf, Creative.
- **No public OpenAPI** for FlightScope ([FAQ](https://flightscope.com/pages/faq)).

**Complaints**
- About every 5–6 shots the status drops from "Ready" to "Connected" and stops reading ([B80](https://breakingeighty.com/flightscope-mevo-gen-2)).
- Constant disconnects (Apr–May 2026) ([GSF](https://golfsimulatorforum.com/forum/flightscope/418210-flightscope-mevo-gen-2-is-constantly-disconnecting)).
- Dated app; hard-to-level stand; phone overheating outdoors.
- Ball-less speed training reads 15–20 mph low ([GSF](https://golfsimulatorforum.com/forum/flightscope/417501-low-swing-speed-in-speed-training-mode-mevo-gen2)).

### 5d. FlightScope paid unlocks (one-time, non-transferable)

| Unlock | List price | Current price |
|---|---|---|
| **Pro Package** | $1,000 | **$699** ([FlightScope](https://flightscope.com/products/pro-package)); $599 in the Nov 2025–Jan 2026 sale |
| **Face Impact Location** | $499 | $350 at IGO; $299 in sale |
| Bundle (both) | $1,499 | $975 at IGO; $850 in sale |

- **Pro Package adds 11 parameters:** club path, face-to-path, face-to-target, dynamic loft, vertical and horizontal swing plane, low point, vertical descent angle, curve, club speed profile and club acceleration profile.
- Sources: [PlayBetter](https://www.playbetter.com/blogs/golf-tech-news/flightscope-golf-sale); [IGO](https://indoorgolfoutlet.com/products/flightscope-mevo-gen2-launch-monitor).
- **Fully loaded Gen2 costs about $2,274** ([FlightScope blog](https://flightscope.com/blogs/blogs/best-golf-launch-monitor-comparison-2026)). That is FlightScope's version of a subscription: an upfront software paywall on club data.
- **CONFLICT:** whether FIL requires the Pro Package (FAQ says no; B80 says yes).

---

## 6. Swing Caddie / Voice Caddie (Korea)

Voice Caddie is the company; Swing Caddie is the launch-monitor line. Branding is confusing even to reviewers ([B80](https://breakingeighty.com/voice-caddie-sc4-pro)).

### 6a. SC4 (2023)

**Price and status**
- Launched at **$549.99** ([PlayBetter 2023](https://www.playbetter.com/blogs/golf-simulator-reviews/swing-caddie-sc4-golf-launch-monitor-review)); later $449.
- No longer listed standalone; likely superseded (UNVERIFIED).

**Technology and placement:** Doppler radar with screen, voice and remote. DTL 5 ft plus at least 8 ft of flight.

**Metrics:** carry, total, swing speed, ball speed, smash, apex, launch, launch direction, spin. No AoA and no putting.

**Accuracy**
- **PlayBetter (vs GC3):** irons "nearly identical", but iron spin 600–700 rpm off and driver sometimes 20+ yd off (one drive read about 7,700 rpm vs about 3,300 true).
- **Breaking Eighty (vs Bushnell LP):** irons within 2–3 yd; drivers up to 20 yd off ([B80](https://breakingeighty.com/swing-caddie-sc4-review)).

**Simulators:** E6 (1 course) and OptiShot Orion.

### 6b. SC4 Pro (late 2024; current flagship)

**Price:** **$599.99** MSRP with stand ([Voice Caddie](https://voicecaddie.com/products/sc4-pro)). Street $499 at [Top Shelf](https://topshelfgolf.com/collections/swing-caddie-golf-launch-monitors) and $509.99 at [Grips4Less](https://www.grips4less.com/products/swing-caddie-sc4-pro-launch-monitor-3d-driving-range-simulator).

**Technology**
- **K-band 24 GHz Doppler, no camera.**
- Same hardware as the SC4; the "ProMetricS" software is described as machine learning ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/swing-caddie-sc4-pro-review); [B80](https://breakingeighty.com/voice-caddie-sc4-pro)).

**Placement and space**
- DTL 5 ft, about 10 ft to the net ([Voice Caddie](https://voicecaddie.com/products/sc4-pro)).
- Minimum ball speed about 22 mph, so short chips are not read ([Plugged In](https://pluggedingolf.com/swing-caddie-sc4-pro-launch-monitor-review/)).

**Metrics**
- On-device: carry/total, launch direction, swing speed, ball speed, smash, launch angle, apex, spin.
- App: back spin, side spin, spin axis, dispersion.
- **Spin is calculated, not measured,** per reviewers ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/swing-caddie-sc4-pro-review); Rain or Shine FAQ via search). No special balls needed.

**Club data:** none beyond speed and smash ([Top Shelf](https://topshelfgolf.com/blogs/golf/swing-caddie-sc4-pro-review-2026)).

**Accuracy**
- **Golfer's Authority (vs TrackMan, 7-iron):** 2.1 yd carry and 1.8 mph ball speed average error (via search).
- **PlayBetter (vs Foresight Hawk):** about 1 in 15 obvious misreads; indoor spin "all over the map".
- **Breaking Eighty:** driver noticeably off about 25% of the time; occasional 2,000–3,000 rpm spin misses.
- **GolfWRX user:** launch direction 8–12° right on more than 70% of shots (snippet).

**Subscription and simulators**
- Free app. E6 with 5 courses; more needs an optional E6 subscription.
- **No GSPro support** ([GSPro](https://gsprogolf.com/)). No Awesome Golf, TGC or OpenAPI evidence.

**Battery:** **about 10 h** (7,500 mAh). Standalone outdoors with screen and remote.

**Complaints:** finicky alignment, no case, remote fails in sun, weak app stats, slow support.

### 6c. SC300i

- **Price:** **$399.99** ([Voice Caddie](https://voicecaddie.com/products/swing-caddie-sc300i)).
- **Technology and placement:** 24 GHz radar plus barometric sensor; DTL 5 ft.
- **Metrics:** carry, smash, swing and ball speed, launch, apex, spin (app). Carry is derived from speeds and launch.
- **Claimed accuracy:** ±2% ball speed, ±3 yd carry.
- **Simulators:** "No" ([VC FAQ](https://voicecaddie.com/products/swing-caddie-sc300i)).
- **Battery:** up to 20 h.

### 6d. SC200 Plus

- **Price:** **$279.99** (launched at $399) ([Voice Caddie](https://voicecaddie.com/products/swing-caddie-sc200-plus); [Practical Golf](https://practical-golf.com/swing-caddie-sc200-plus-review/)).
- **Technology and metrics:** 24 GHz radar. Carry, total, swing and ball speed, smash. No launch, no spin.
- **Simulators:** none.
- **Power:** 4×AAA, about 20 h.

**Other 2025–26 Voice Caddie:** no new launch monitor. The VC300SE is a voice GPS and the SL Mini is a rangefinder ([VC](https://voicecaddie.com/collections/simulator-launch-monitors)).

---

## 7. PRGR (Japan) portable launch monitor

**Models**
- Japan: "Red Eyes Pocket" HS-110, HS-120, then HS-130 (Apr 2021) ([PRGR JP](https://www.prgr-golf.com/information/news/210315-1.html)).
- International: "Black" HS-130A.
- Japan-only HS-130_BLE (May 2024) adds Bluetooth and an iOS app with a ¥500/month video tier ([PRGR JP](https://www.prgr-golf.com/information/news/240422-1.html)).
- No "Home Edition" and no 2025–26 model found ([Top Shelf, Apr 2026](https://topshelfgolf.com/blogs/golf/prgr-launch-monitor-review-best-pocket-lm-2026)).

**Price**
- Launched at **$229** ([Practical Golf](https://practical-golf.com/prgr-launch-monitor-review)).
- Street **$199.99** ([SuperSpeed](https://superspeedgolf.com/products/prgr-black-pocket-launch-monitor)).

**Technology and placement**
- 24 GHz Doppler, described as "dual radar".
- DTL about 4.5 ft, at least 6.5 ft to the net.
- Readings drop to 94% of true at 20° misalignment ([Top Shelf](https://topshelfgolf.com/blogs/golf/prgr-launch-monitor-review-best-pocket-lm-2026)).

**Metrics**
- **Measured:** club and ball speed.
- **Calculated:** smash, carry and total, from PRGR's average launch and spin per club.
- No spin and no launch.

**Accuracy:** ball speed within 1–2 mph of TrackMan/GCQuad; distance 5–7% optimistic; mishits 30+ yd off ([Golfers Authority](https://golfersauthority.com/prgr-black-pocket-launch-monitor/)).

**Subscription, simulators, power**
- No subscription and no simulator support.
- 4×AAA (sources say AA or AAA; CONFLICT), about a month of use.

---

## 8. Bushnell Launch Pro / LPi (Foresight GC3 hardware)

**Models**
- **No "Launch Pro Lite" exists.**
- Lineup: Launch Pro (Circle B Edition, battery and screen) and **LPi** (Launch Pro Indoor, AC power, no screen).
- The ball-only tier is discontinued ([Bushnell](https://www.bushnellgolf.com/products/launch-monitors/launch-pro/); [B80](https://breakingeighty.com/bushnell-launch-pro-circle-b)).

**Price**
- Launch Pro **$2,999.99**.
- LPi: announced Jan 2025 at $2,799 ([Golf Wire](https://thegolfwire.com/bushnell-launch-pro-indoor/)), later $1,499, now **$1,999.99** and **sold out**.
- Briefly $999 at Golf Galaxy in Sept 2026. B80 suspects the LPi "may be on its way out" ([B80](https://breakingeighty.com/bushnell-launch-pro-circle-b); [Bushnell LPi](https://www.bushnellgolf.com/products/launch-monitors/lpi-personal-launch-monitor/)).
- **Only under $1,500 on clearance.**

**Technology and placement**
- **Three cameras ("Triscopic")** plus IR. Frame rate unpublished.
- Side, about 2 ft from the ball; 7 × 10 in zone.
- Lefties must move the unit ([Golfible](https://golfible.com/bushnell-launch-pro/)).

**Metrics**
- **Ball (13):** carry, speed, total, back and side spin, spin axis, vertical and horizontal launch, apex, descent, offline, curve, hang time. All camera-measured or modelled; **no marked balls**.
- **Club:** speed, smash, path, AoA, **with fiducial stickers** ($49.99 per 192).
- **No face angle, face-to-path, dynamic loft or impact location** ([Golfible](https://golfible.com/bushnell-launch-pro/)).

**Accuracy**
- **Golfible (vs TrackMan, indoors, RCT):** ball speed under 1 mph off; spin within 100 rpm; launch within 1°; driver carry +5.9 yd; path and AoA within 1–2° ([Golfible](https://golfible.com/bushnell-launch-pro/)).
- The strongest independent accuracy evidence of any edge-of-tier unit.

**Subscription (Foresight+, from Sept 18, 2026)** ([Bushnell](https://www.bushnellgolf.com/products/launch-monitors/launch-pro/); [B80](https://breakingeighty.com/bushnell-launch-pro-circle-b))

| Tier | Price | Includes |
|---|---|---|
| Free | $0 | Ball data, 10 sessions of history |
| Silver | **$199/yr** | Unlimited history, drills, dispersion |
| Gold | **$599/yr** (was $499) | Swing video, profiles, AI coaching, **third-party integrations** |
| Course Pass | $295/yr (35 courses) | Requires Silver or Gold |
| Course Pass Pro | $595/yr (111 courses) | Requires Silver or Gold |

- **GSPro requires Gold** ([GSPro](https://gsprogolf.com/)), so Gold plus GSPro is about **$849/yr**.
- The club-data tier is inconsistent on Bushnell's own page (CONFLICT).

**Other**
- The unit must check in from a US connection every 45 days.
- 2.4 GHz Wi-Fi only; no Bluetooth; 20% restocking fee.
- Survey: average paid $2,381; **67% say a sub is required**; 83% would buy again ([Yardstick](https://docs.google.com/spreadsheets/d/1XnXNXh4zo4ugafKzMNKTl7Kbtrdg4ewAqiBHX7vQwAE/edit?gid=1954495530)).

---

## 9. Golfzon WAVE / WAVE Play (Korea)

**WAVE Play**
- A sensor club with a sliding magnetic impact ball. It is **not a launch monitor**.
- About ¥32,890 JP (UNVERIFIED) or about $201 used ([Golfzon](https://www.golfzonwave.com/products/WavePlay); [eBay](https://www.ebay.com/p/28067863364)).

**WAVE price**
- Launched at **$3,995–4,000** ([Garage Golf](https://mygaragegolf.com/blogs/buying-guides/golfzon-wave-launch-monitor-review); [Plugged In](https://pluggedingolf.com/golfzon-wave-launch-monitor-review/)).
- US street price UNVERIFIED. About $2,748 new from a JP eBay seller; about $1,621 used ([eBay](https://www.ebay.com/p/20067213314)).
- UK £2,799.99, out of stock.
- **Not under $1,500 new.**

**Technology**
- **"24GHz 3ch Radar"** plus a camera (video and alignment) ([Golfzon](https://www.golfzonwave.com/products/Wave)).
- Putt mat with 7 IR sensor pairs.
- Firmware 196 added RCT detection ([Golfzon](https://www.golfzonwave.com/)).

**Placement:** DTL 6.5–8.2 ft, at least 8 ft of flight (down from 11.5 ft via firmware).

**Metrics:** 34 (26 swing + 8 putt), including path, face, face-to-path, dynamic loft, spin loft, swing plane. Measured-vs-calculated is not disclosed.

**Accuracy (Plugged In, vs GCQuad)**
- Ball speed good; launch up to 2.5° off; spin weakest; club speed high.
- Club data "not reliably precise"; would "not use it for club fitting" ([Plugged In](https://pluggedingolf.com/golfzon-wave-launch-monitor-review/)).

**Subscriptions:** Premium $199/yr (on sale; normally $399), Basic $99, Light $19 ([Golfzon](https://www.golfzonwave.com/products/Subscription)).

**Simulators:** E6 yes; GSPro and Awesome Golf no (as of Jan 2024). Battery 4 h, IPX3.

**Lesson for us:** a radar unit that *lists* face, dynamic loft and so on is not credible if its accuracy doesn't hold up.

---

## 10. Ernest Sports (US)

**Lineup:** ES14, ES16, original Tour Plus and ES 20/20 are no longer on the site. Current: ESB1 REV-D, ESB2 ($495), Tour Plus 2.0, ES Eagle Sim ($5,000 overhead) ([Ernest](https://ernestsports.com/)).

**ESB1 REV-D**
- **Price:** **$199.99** (was $275).
- **Technology and placement:** Doppler; DTL 4–6 ft.
- **Metrics:** measures ball and club speed only; estimates the rest.
- **Battery:** 20 h.
- **Fees:** optional AI at $8.99/mo ([ESB1](https://www.ernestsports.com/product/esb1/)).

**Tour Plus 2.0**
- **Price:** **$999.99** direct (was $1,795); Indoor Golf Pros lists $1,995 ([IGP](https://www.indoorgolfpros.com/collections/ernest-sports)).
- **Technology:** **two high-speed IR cameras plus four 3D Doppler sensors**; side placement.
- **Metrics:** 20, including path, face, face-to-path, AoA, dynamic loft, spin loft. No club markers mentioned. Measured-vs-calculated not disclosed.
- **Spin:** indoors it needs the ball's straight logo facing the unit, which suggests camera-read spin ([WiscoGolfAddict](https://wiscogolfaddict.com/2024/04/02/ernestsports_launchmonitors/)).
- **Outdoors:** sunlight blocks the cameras.
- **Accuracy:** no independent TrackMan or GCQuad test. "Within 5–6%" anecdotally; about 1 in 20 misreads. Company claims 99.4%.
- **Simulators:** E6 ($300/$600/yr; $250 5-course perpetual pack). GSPro not mentioned.
- **Lesson for us:** on paper this is the closest spec match to our goal in this tier (camera + radar, side, face data). It gets almost no review coverage or community traction, which shows that specs without credible independent validation and distribution don't sell.

---

## 11. Uneekor EYE MINI LITE / EYE MINI

**Price**
- **EYE MINI LITE:** list $2,749 (2024 launch); **sale $1,999** ([Uneekor](https://uneekor.com/en-us/products/eye-mini-lite-standalone); [Top Shelf](https://topshelfgolf.com/products/uneekor-eye-mini-lite-launch-monitor-golf-simulator)). **Not under $1,500.**
- **EYE MINI:** $2,999 sale (list $4,500).
- MySimSetup lists an "EYE MINI CORE" at $999 ([MySimSetup](https://www.mysimsetup.com/reviews/compare/launch-monitor)); UNVERIFIED, not on the Uneekor pages fetched.

**Technology and placement**
- **Two high-speed IR cameras.** "Dimple Optix" reads dimples, so no marked balls.
- Side; 12 × 8 in zone.
- LITE: AC power, Ethernet to a Windows PC, indoor only. Recommended PC: RTX 4070 Ti, 32 GB.

**Metrics**
- **Ball (15):** all camera-measured or modelled.
- **Club (4):** path, speed, smash, AoA, with stickers.
- **Explicitly not measured:** impact point, face angle, face-to-path, dynamic loft, lie ([Uneekor](https://uneekor.com/en-us/products/eye-mini-lite-standalone)).

**Accuracy:** no numeric independent test found; about 1 misread per 40 shots ([Golfible](https://golfible.com/uneekor-eye-mini-lite/)).

**Memberships** ([Uneekor](https://uneekor.com/en-us/discover/software-and-memberships/software-memberships))

| Tier | Price | Includes |
|---|---|---|
| Player | Free | All data |
| Pro | **$199/yr** | **Required for the GSPro/third-party connector** |
| Champion | $399/yr | |
| Ultimate | $599/yr | |

---

## 12. OptiShot (US) and Phigolf (Korea): non-ball-tracking simulators

**OptiShot 2**
- **Technology:** **16 IR sensors at 48 MHz in a floor pad**; tracks the club only, never the ball. USB to PC/Mac ([InTheHoleGolf](https://www.intheholegolf.com/OPTISHOT2/OptiShot-2-Golf-Simulator.html)).
- **Price:** $499.99 at [Golf Galaxy](https://www.golfgalaxy.com/p/optishot-2-swingpad-golf-simulator-15dgguptsht2glfsmtch/15dgguptsht2glfsmtch); marked "Discontinued" elsewhere; historically $299; about $99–175 used.
- **Metrics:** measures club speed, path, face and contact; **every ball metric is calculated**.
- **Accuracy:** an 8-iron read anywhere from 140 to 170; path showed out-to-in when it was 5–12° in-to-out ([Practical Golf](https://practical-golf.com/optishot-2-review)).
- **Software:** no GSPro, E6 or Awesome Golf. Software is effectively end-of-life ([MySimSetup](https://www.mysimsetup.com/reviews/products/optishot-2)).
- The brand has split. Red Stakes Golf (RSG One camera unit, $1,999–3,650) and "OptiShot Orbit" (= Voice Caddie SC4 hardware with Orion software, about $549) ([rsgolf](https://rsgolf.com/); [Amazon](https://www.amazon.com/OPTISHOT-Simulator-Monitor-Simulators-Software/dp/B0CBT5LMWK)).

**Phigolf 2 / Phigolf2 Flex**
- **Technology:** 9.8 g Bluetooth motion sensor on a 27.6 in swing stick or a real club. No ball.
- **Price:** **$263.20 sale / $329 list** ([phigolf.com](https://www.phigolf.com/); [Walmart](https://www.walmart.com/ip/18054771849), 3.8★ / 58 reviews).
- **Metrics:** head speed, tempo, path, face, AoA, "estimated distance". All ball metrics calculated; no spin.
- **Accuracy (vs TrackMan):** consistent path error; face changes not detected; "10+ yards of error"; not useful under a 20 handicap ([Golf Insider UK](https://golfinsideruk.com/phigolf-review/)).
- **Software:** WGT and E6 via subscription; no GSPro.
- No "Phigolf 3" hardware exists. 2025 news was software and Web3 ([GlobeNewswire](https://www.globenewswire.com/news-release/2025/01/21/3012997/0/en/PhiNetworks-Announces-Innovative-Smartwatch-Integration-and-Web3-Golf-to-Earn-Platform-at-PGA-SHOW-2025.html)).

---

## 13. 2025–26 newcomers and edge-of-tier units

### Blue Tees Rainmaker (2026 PGA Show; shipping by Aug 2026)

**Price:** **$599–599.99** ([PlayBetter](https://www.playbetter.com/products/blue-tees-golf-rainmaker-golf-launch-monitor); [Plugged In Golf](https://pluggedingolf.com/blue-tees-rainmaker-launch-monitor-review/)).

**Technology:** "phased array Doppler radar" (band not stated). 4.3" screen, remote, IPX4, 719 g, 7 h battery, 1,000-shot on-device storage ([Golfers Authority](https://golfersauthority.com/blue-tees-rainmaker-launch-monitor-review/)).

**Placement:** DTL 5 ft; works with just under 8 ft of flight.

**Metrics**
- **Measured:** ball speed, club speed, launch, direction.
- **Calculated:** spin (back, side, axis), apex, carry, path, AoA. Spin measurement method is UNCERTAIN; treat as calculated.
- No special balls.

**Accuracy (Plugged In, vs GCQuad)**
- Outdoors: ball speed within 1 mph (max 3); carry within 2–3 yd; **spin read low throughout the bag**.
- Indoors: wedge spin erratic.
- About 2–5 s data lag. Rated "same ballpark as MLM2 Pro".

**Subscription:** year 1 free, then **$79/yr**. A $99 / 3-year option was mentioned in previews ([Breaking Eighty](https://breakingeighty.com/blue-tees-rainmaker)).

**Simulators:** GSPro (officially listed) ([GSPro](https://gsprogolf.com/)). E6 "coming soon" vs "supported": CONFLICT.

**Complaints:** tablet-only app, tedious bag setup, 3.4/5 on Blue Tees' own store.

### Shot Scope LM1 (Apr 2026)

- **Price:** **$199.99, no subscription** ([Shot Scope](https://shotscope.com/us/shop/products/golf-launch-monitors/lm1-launch-monitor/)).
- **Technology:** Doppler; 3.5" screen; 300 g; IPX3; about 5 h battery; DTL about 5 ft.
- **Metrics:** measures club and ball speed; calculates smash, carry, total. No launch, no spin.
- **Simulators:** none ([Golf Digest](https://www.golfdigest.com/story/shot-scope-lm1-launch-monitor-release)).
- Breaking Eighty: "the most accurate launch monitor you'll find under $300" ([B80](https://breakingeighty.com/2026-launch-monitors)).

### SkyTrak+ (clearance)

**Price**
- **$1,195** at [PlayBetter](https://playbetter.com/products/skytrak) (was $2,495), "while promotional inventory remains"; $1,075 with a code ([B80](https://breakingeighty.com/best-golf-launch-monitors)).
- Successor ST MAX **$1,695** ([SkyTrak](https://www.skytrakgolf.com/)); B80 calls it "pretty much the exact same thing".

**Technology:** photometric camera plus dual Doppler. Side, **18 in from the ball** with a laser dot.

**Metrics**
- Camera-measured ball speed, launch and spin, markerless.
- Club speed, face, path, smash, face-to-path.
- **No AoA, no impact location.**

**Accuracy:** vs TrackMan, club speed, carry and spin "right in line"; side carry about double ([B80](https://breakingeighty.com/skytrak-plus-review)).

**Subscription:** plans **$99.99–$599.99/yr**; pricing in flux across sources (CONFLICT) ([Top Shelf](https://topshelfgolf.com/blogs/golf/skytrak-membership-plans-basic-essential-core-elite-2026); [PlayBetter](https://playbetter.com/products/skytrak)).

**Simulators:** **official GSPro/E6 support ended for new buyers**. An unofficial OpenSkyPlus connector exists (UNVERIFIED).

**Other**
- Wi-Fi only, about 4 h battery, poor on grass.
- Survey: 88% would buy again; 50% say a sub is required.

### OpenLaunch Nova (US; about 2025)

- **Price:** **$1,500**; no subscription; free "Anniversary Update" for owners ([OpenLaunch](https://openlaunch.io/)).
- **Technology:** sensing technology not stated on the page (UNVERIFIED); photos show a floor unit beside the ball.
- **Software:**
  - GSPro (official, no fee), TGC 2019, Infinite Tees, Fitness Golf.
  - Free open-source sims (Open Golf Sim, Muni Golf Sim).
  - Video tools (OBS, Kinovea).
- **Owner sentiment:** cites the 2026 r/Golfsimulator survey with 100% would-buy-again, 5/5 support, 9.7/10 putting realism (self-reported on vendor site).
- **Why it matters:** this is the closest existing analogue to our *business model* (no sub, open-ecosystem positioning, community-friendly). A follow-up on its sensor stack is needed.

### GolfJoy (China)

- Five devices are on GSPro's official list: Spica 3, GDS Pro, GR2, GR3, GR3 Pro ([GSPro](https://gsprogolf.com/)).
- Cheapest found: GDS Pro, $2,199 ([MySimSetup](https://www.mysimsetup.com/reviews/compare/launch-monitor)).
- No sub-$1,500 GolfJoy found; specs UNVERIFIED.

### Others surfaced, not researched

From [MySimSetup](https://www.mysimsetup.com/reviews/compare/launch-monitor), all UNVERIFIED:

| Product | Price | Technology |
|---|---|---|
| Spectrum Golf Tech Element | $1,000 | Camera |
| Exputt RG | $469 | Camera putting/sim |
| Ernest ES12/ES14/ESB1 | $199–495 | Radar |
| Uneekor EYE MINI CORE | $999 | Camera |

Tittar, GolfBuddy LM-1, AceTee and Nexgolf could not be checked; search budget ran out and tittargolf.com does not resolve. **This gap should be filled in a follow-up.** Amazon is where Chinese 24 GHz radar clones will compete with the PRGR, SC4 and LM1 at $150–400.

### Open-source DIY: PiTrac and OpenFlight (relevant as tech references)

**PiTrac** ([GitHub](https://github.com/PiTracLM/PiTrac); [docs](https://docs.pitrac.org/); [Hackaday](https://hackaday.io/project/195042-pitrac-the-diy-golf-launch-monitor))
- **Licence and maturity:** GPL-2.0; 426 stars; self-described "really immature".
- **Compute:** one Raspberry Pi 5.
- **Cameras:** **two Innomaker IMX296 mono global-shutter cameras** (1456×1088, 6 mm lenses) with ≥700 nm long-pass filters.
- **Illumination:** **10 Vishay VSMA1085400 IR LEDs strobed** via MOSFET plus MCP1407 driver.
- **Capture:**
  - Camera 1 watches the tee at about 500 fps and triggers on ball movement.
  - Camera 2 captures a multi-exposure strobed image of the ball in flight, about "3,000 effective fps".
- **Measured:** ball speed, vertical and horizontal launch, **3-axis spin, markerless**.
- **Not available:** no club data; indoor only (sun swamps the IR).
- **Cost and validation:** about $300–400 in parts. No independent validation.
- **Simulators:** GSPro (OpenConnect) and E6.

**OpenFlight**
- **Hardware:** OmniPreSense OPS243-A **24 GHz** radar plus Pi 5 plus K-LD7 angle radars, about $540.
- Spin estimated; about 530 stars; GSPro ([MySimSetup](https://www.mysimsetup.com/reviews/products/openflight)).

**Takeaway for us:** markerless photometric spin with a strobed global-shutter pair is achievable on commodity parts. The hard problems are ball detection robustness ("HoughCircles… still kinda sucks"), outdoor sunlight rejection, club and face measurement, and validation.

---

## 14. Market size, share and sales data

### Market size (definitions vary widely; low confidence)

| Source | 2025 | Forecast | CAGR |
|---|---|---|---|
| [GMI](https://www.gminsights.com/industry-analysis/golf-launch-monitor-market) | $234.4M | $523.5M (2035) | ~8.6% |
| [Reportprime](https://www.reportprime.com/golf-launch-monitor-r883) | $190.3M | $342.6M (2032) | 8.76% |
| [Dataintelo](https://dataintelo.com/report/golf-ball-launch-monitors-market) | $312.6M | | 9.8% |
| [Wiseguy](https://www.wiseguyreports.com/reports/golf-launch-monitor-market) | $1.02B | | (outlier) |

- **GMI detail:**
  - Consumer/personal grade $132.45M in 2025, reaching $313M by 2035 (~9.25%).
  - North America $92.6M, of which the US is $78.6M.
  - Company shares: TrackMan 29.7%, Foresight 23.1%, FlightScope 12.6%, Golfzon 7.0%, SkyTrak 3.7%. Garmin, Rapsodo and Square are only "other players", so the table likely understates budget brands and GMI is internally inconsistent.
- **Participation:**
  - US simulator players: **9M+ in 2025** (NGF via FT) ([The Wedge](https://thewedgegolf.substack.com/p/ft-home-simulator-surge)); 8.1M in 2024, up 126% vs 2019 ([NGF](https://www.ngf.org/wp-content/uploads/2025/04/2025-NGF-White-Paper-The-Golf-Simulator-Opportunity.pdf)).
  - NGF has "no estimate on the size of the home simulator space" ([NGF](https://www.ngf.org/short-game/simulator-golf-sees-real-surge/)).
- **TrackMan:** 300% revenue growth from 2019 to 2025 (FT via The Wedge).

### Unit and revenue proxies

- **Garmin R10:** about 1,000 units a month on Amazon US (AsInsight estimate, low confidence) ([AsInsight](https://www.asinsight.com/report/US/launch-monitor-golf)).
  - Garmin calls golf launch monitors a "halo product" (Q4 2024 call) ([Investing.com](https://uk.investing.com/news/transcripts/earnings-call-transcript-garmin-q4-2024-earnings-surge-stock-jumps-127-93CH-3933049)).
  - The Outdoor segment did $2.05B at a 34% operating margin; golf is not broken out ([Garmin ARS](https://www.sec.gov/Archives/edgar/data/0001121788/000119312526169264/grmn-ars-20251227.pdf)).
- **Rapsodo:**
  - FY2024 revenue SGD 50–100M (about US$37–75M), covering all sports ([Tracxn](https://tracxn.com/d/companies/rapsodo/__TTRfsH_WzAugUrrRL6M96HdirlIUhbdPgio9JlA85O0)).
  - Golf is "the largest segment of the now 300-person company" ([Sportico, 2024](https://sportico.com/personalities/athletes/2024/shohei-ohtani-endorsement-rapsado-baseball-tech-1234776153/amp)).
- **Others:** no unit data found for Square, FlightScope, Voice Caddie or Bushnell.

### Enthusiast ownership: Yardstick Golf 2026 survey (r/Golfsimulator, ~684 rows)

Source: [methodology](https://yardstickgolf.com/launch-monitor-survey/), [sheet](https://docs.google.com/spreadsheets/d/1XnXNXh4zo4ugafKzMNKTl7Kbtrdg4ewAqiBHX7vQwAE/edit?gid=1954495530). Shares were computed by us.

| Device | Share | Avg paid | "Sub required" | Would buy again | Support /5 |
|---|---|---|---|---|---|
| Garmin R10 | 15.5% | $501 | 6% | 65% | 3.85 |
| SkyTrak/+ | 10.4% | $2,362 | 50% | 88% | 3.9 |
| Bushnell LP | 9.9% | $2,381 | 67% | 83% | 3.82 |
| MLM2PRO | 5.8% | $679 | **92%** | 75% | 3.8 |
| Mevo+ | 5.6% | $1,960 | 3% | **60%** | 3.8 |
| Square (orig.) | 5.0% | $704 | 0% | **97%** | **1.44** |
| SC4 (2024 data) | 1.5% | $500 | 0% | 100% | 4.0 |

Self-selected enthusiasts; the sample skews premium.

---

## 15. Analysis

### 15.1 The "value ceiling": what this tier consistently can't do

| Capability (our target) | Budget-tier reality | Evidence |
|---|---|---|
| **Markerless measured spin, indoors** | Radar units **calculate** spin indoors or need RCT/RPT balls or metallic dots. Only camera units measure it markerless: Square Omni ($1,599), SkyTrak+ (clearance), Bushnell/Uneekor (over $1,500), PiTrac (DIY). | R10 "every indoor spin number is calculated" ([Fore-ward](https://forewardthinking.com/learn/garmin-r10-reads-short-indoors.html)); MLM2PRO "RPT required" ([Rapsodo](https://rapsodo.com/products/mlm2pro-mobile-launch-monitor-golf-simulator)); Mevo dots "required" ([FlightScope](https://flightscope.com/products/mevo-gen2)); SC4 Pro calculated ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/swing-caddie-sc4-pro-review)); Rainmaker spin reads low ([Plugged In](https://pluggedingolf.com/blue-tees-rainmaker-launch-monitor-review/)) |
| **Accurate sidespin / spin axis** | Even with special balls, sidespin is weak: R10 reads ½–⅔ low; Mevo+ axis possibly calculated; Omni axis "wonky". | Garmin forum (search summary); [GSF](https://golfsimulatorforum.com/forum/flightscope/360576-mevo-spin-measured-vs-calculated); [Golfstead](https://golfstead.com/square-golf-omni-launch-monitor-review) |
| **Measured face angle** | **No budget unit measures face angle well without markers.** R10 calculates it; MLM2PRO, Uneekor and Bushnell don't offer it; Mevo charges $699–1,000; Omni *estimates* it from a shaft sticker; SkyTrak+ reports it but accuracy is unproven. | [Lasco Press](https://www.thelascopress.com/2026/05/square-golf-omni-review/); [Uneekor](https://uneekor.com/en-us/products/eye-mini-lite-standalone); [FlightScope](https://flightscope.com/products/pro-package) |
| **Dynamic loft / spin loft** | Paid (Mevo), estimated (Omni), or absent. | Same |
| **Impact location** | Only Omni (face sticker) and Mevo (FIL add-on $350–499, needs at least 300 lux). | [FlightScope FAQ](https://flightscope.com/pages/faq) |
| **Markerless club data of any kind** | Camera units all need stickers (Omni, Uneekor, Bushnell fiducials). Radar club data is calculated (R10) or paywalled (Mevo). | §§4, 8, 11 |
| **Low point / lie** | Only the Mevo Pro Package (low point). Lie: none. | [FlightScope](https://flightscope.com/products/pro-package) |
| **Short game and putting** | Radar is poor at short range: R10 putting 0.99/10; SC4 Pro misses chips under 22 mph ball speed. Camera units excel (Square chipping 8.6, putting 8.2). | [Yardstick](https://docs.google.com/spreadsheets/d/1XnXNXh4zo4ugafKzMNKTl7Kbtrdg4ewAqiBHX7vQwAE/edit?gid=1954495530); [Plugged In](https://pluggedingolf.com/swing-caddie-sc4-pro-launch-monitor-review/) |
| **Equal indoor + outdoor performance** | A trade-off nobody has solved at this price. Radar is good outdoors but weak indoors (space, spin). Cameras are good indoors but sun hurts them: Omni spin varies in bright sun; Ernest is blocked by sunlight; original Square, PiTrac and LPi are indoor-only. | [Golf Online UK](https://www.golfonline.co.uk/square-golf-omni-launch-monitor-review); [Wisco](https://wiscogolfaddict.com/2024/04/02/ernestsports_launchmonitors/) |
| **Small indoor footprint** | DTL radar needs **14–21 ft** depth (MLM2PRO 14.5–21.5; Mevo Gen2 16–21; R10 about 15). Side cameras need only swing room. | §§2, 3, 5 |
| **Low latency** | R10 2–4 s; Rainmaker 2–6 s; Mevo, MLM2PRO, Omni about 0–1 s. | Yardstick; [Plugged In](https://pluggedingolf.com/blue-tees-rainmaker-launch-monitor-review/) |

**Bottom line:** below about $1,000 you buy measured speeds, launch angles, direction and modelled everything else. From $1,000 to $1,600 (Omni, Mevo Gen2, SkyTrak+ clearance) you can get measured ball spin, but **club-face data stays estimated, sticker-dependent or paywalled, and no unit is equally good indoors and outdoors.** That gap is our opportunity.

### 15.2 Best value story

- **Best value overall (just over the threshold): Square Golf Omni at $1,599.**
  - It measures markerless ball spin (backspin within about 200 rpm and sidespin within about 300 rpm of GCQuad ([Friendly Golfer](https://friendlygolfer.com/square-golf-omni-review/))).
  - It adds path, AoA, club speed and impact location (sticker), a built-in screen, and works in a shallow room.
  - No subscription and no fee to connect GSPro, E6 or Awesome Golf.
  - About $2,350 over 3 years with GSPro ([Golfers Authority](https://golfersauthority.com/square-omni-launch-monitor/)), versus about $1,450+ just in Rapsodo plus GSPro fees over 3 years on top of MLM2PRO hardware.
  - Weaknesses: stickers, estimated face and loft, bright-sun spin, software polish, support.
- **Best strict under-$1,500, simulator-on-a-budget: Garmin R10 ($399–499).**
  - The most-owned device, broad simulator compatibility, 10 h battery, likely no subscription needed for GSPro (CONFLICT).
  - But spin, face and path are all calculated, it needs about 15 ft of depth, and its putting is unusable.
- **Most data per dollar if you accept a subscription and special balls: Rapsodo MLM2PRO ($549.99).** Excellent ball-speed, carry and RPT-spin accuracy. Lifetime cost runs higher than the Omni's, and the paywall is the most-complained-about in the tier.
- **Best no-subscription radar: Mevo Gen2 ($1,299).** Strong accuracy, but full club data lifts it to about $2,274, and it needs 16–21 ft of depth.

### 15.3 How budget players make money

| Model | Who | Mechanics |
|---|---|---|
| **Hardware plus recurring software subscription** | Rapsodo, Bushnell/Foresight, SkyTrak, Uneekor, Golfzon | Rapsodo Core $199.99/yr, Studios $399.99/yr, and the trial cut to 21 days on the XPRO ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/10/01/3373058/0/en/rapsodo-unveils-new-golf-ecosystem-led-by-as-real-as-it-gets-rapsodo-studios-and-mlm2xpro.html)). Bushnell Gold up $499 to $599 (Sept 2026). Uneekor Pro $199 for the connector. SkyTrak $99.99–599.99. **Third-party connectivity is held hostage to the subscription.** |
| **Hardware plus one-time software unlocks** | FlightScope | Pro Package $699–1,000, FIL $350–499; full Gen2 about $2,274 ([FlightScope blog](https://flightscope.com/blogs/blogs/best-golf-launch-monitor-comparison-2026)). |
| **Hardware plus pay-per-use content** | Square | Free practice and third-party; native course credits about $20 per 1,000 ([Golfstead](https://golfstead.com/square-golf-omni-launch-monitor-review)). |
| **Ecosystem membership halo** | Garmin | Garmin Golf $99.99/yr covers watches, handhelds and Home Tee Hero; the R10 is a "halo product" ([Investing.com](https://uk.investing.com/news/transcripts/earnings-call-transcript-garmin-q4-2024-earnings-surge-stock-jumps-127-93CH-3933049)). |
| **Pure hardware margin** | PRGR, Voice Caddie, Ernest, Shot Scope, OpenLaunch | No subscription; low price or premium-on-value. OpenLaunch markets "no fees, no subscription" explicitly ([OpenLaunch](https://openlaunch.io/)). |
| **Consumables** | Rapsodo, Bushnell, Square | RPT balls $69.99/dozen; Bushnell fiducials $49.99/192; Square stickers (replacement price UNVERIFIED). |

**Margins:** no device-level margin, BOM or subscription-revenue disclosures were found for any brand (UNVERIFIED). The only hard number is Garmin's Outdoor segment at a 34% operating margin, which isn't golf-specific. Our inference: subscription-gated players price hardware aggressively (MLM2PRO at $549.99 on sale) and recover margin through $200–600 a year in software. Square, FlightScope and OpenLaunch must make their money on hardware gross margin.

**Trend:** the market is splitting. Incumbents (Rapsodo, Bushnell) are *raising* subscription prices and tightening trials. Challengers (Square, OpenLaunch, FlightScope, Voice Caddie) use "no subscription" as their headline marketing weapon.

### 15.4 What buyers complain about most (ranked)

1. **Subscriptions and paywalls, especially on third-party simulator access.**
   - MLM2PRO: 92% of owners say a sub is required.
   - "The additional $200 annually isn't worth it"; GSPro needs Premium plus a daily app login ([Rapsodo reviews](https://rapsodo.com/products/mlm2pro); [Top Shelf](https://topshelfgolf.com/blogs/golf/how-to-set-up-mlm2pro-with-gspro)).
   - Bushnell requires Gold at $599 for GSPro.
2. **Spin accuracy: calculated vs measured, and special balls.**
   - R10 indoor spin "almost meaningless" (MyGolfSpy snippet).
   - RPT and RCT balls are an ongoing cost, with durability complaints ([Trustpilot](https://www.trustpilot.com/review/rapsodo.com)).
   - Mevo dots give measured spin on only 30–40% of shots for some users ([GSF](https://golfsimulatorforum.com/forum/flightscope/360576-mevo-spin-measured-vs-calculated)).
3. **Indoor space for DTL radar.** 14.5–21.5 ft depth is a garage-killer; side cameras win here.
4. **Club data missing, unreliable or sticker-dependent.**
   - No face on MLM2PRO, Uneekor or Bushnell; Mevo's face data is paywalled.
   - Omni needs "not one but two stickers on your clubs" ([B80](https://breakingeighty.com/square-omni-launch-monitor)).
   - Omni wedge path disagrees with GCQuad.
5. **Connectivity and app quality.**
   - MLM2PRO disconnects; Mevo Gen2 drops to "Connected" every 5–6 shots.
   - R10 app "in desperate need of an overhaul".
   - Omni desktop crashes and a "bare bones" app.
6. **Setup and alignment.**
   - R10: "eyeball it"; offline numbers 10–15 yd off.
   - Mevo: "precise setup is critical".
   - SC4 Pro: finicky alignment.
7. **Customer support.** Square scores 1.44/5 despite 97% would-buy-again; Rapsodo support allegedly blames users ([Trustpilot](https://www.trustpilot.com/review/rapsodo.com)).
8. **Left-handed support.**
   - Rear radar (R10, Mevo, SC4) needs no change.
   - Side camera units must physically move (Omni, Bushnell, SkyTrak, Uneekor), which is "not ideal for frequent righty-lefty switching" ([Friendly Golfer](https://friendlygolfer.com/square-golf-omni-review/)).
   - MLM2PRO owners disagree.
   - This trade-off is relevant to our side-of-ball vs DTL form factor decision.
9. **Misreads and latency.** SC4 Pro misreads about 1 in 15; R10 about 3% missed; Rainmaker 2–6 s lag; Omni loses club data on fat shots. Hosel and shank misread data was not found (forums blocked).

---

## 16. Implications for our product (short)

These implications are scoped to this slice; the full strategy belongs in the synthesis doc.

1. **Square Omni is the benchmark to beat at about $1,600.** To justify a price of $1,999–2,999, we must clearly win on:
   - **(a) markerless club data**: measured face, dynamic loft, impact with no stickers;
   - **(b) outdoor-in-sun performance** equal to indoor;
   - **(c) published independent accuracy** against TrackMan and GCQuad;
   - **(d) software and support quality.**
2. **"No subscription + open API" is necessary but no longer unique.** Square, FlightScope, OpenLaunch and Voice Caddie already claim it. Our version needs to be stronger: a documented public API (FlightScope has none), and native GSPro, E6 and Awesome Golf at launch.
3. **Form factor:** side-of-ball cameras win indoor space and short game. DTL radar wins outdoor full flight and lefty-agnostic setup. A hybrid (side cameras plus radar) is the only architecture that addresses "indoor AND outdoor equally". Ernest's Tour Plus tried it without validation or traction, so credibility matters as much as specs.
4. **Validation is the moat in this tier.** The products with the best reputations (Bushnell, Mevo Gen2, MLM2PRO) have independent head-to-head numbers. Plan third-party test campaigns (MyGolfSpy, Plugged In Golf, Breaking Eighty, Golf Simulator Videos, PlayBetter) into launch.

---

## 17. Open items / to verify in a follow-up pass

- Radar chips and image sensors (FCC internal photos) for R10, MLM2PRO, Mevo Gen2, SC4 Pro, Rainmaker. Square Omni camera model and frame rate.
- Whether Garmin requires a Garmin Golf membership for GSPro, E6 and Awesome Golf (CONFLICT).
- MLM2XPRO space requirements, battery life, and confirmation that third-party simulators need Core.
- OpenLaunch Nova sensing technology and metrics.
- Chinese and Amazon brands (Tittar, GolfBuddy, others), Spectrum Golf Tech Element, Uneekor EYE MINI CORE.
- MyGolfSpy 2025/2026 launch-monitor test data, plus GolfWRX and Reddit sentiment (blocked this pass).
- Square Omni independent *outdoor* numbers and whether firmware fixed the flop-shot launch errors.
