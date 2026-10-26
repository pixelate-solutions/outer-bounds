# 07 — IP / Patent Landscape, Litigation, Design-Around, Regulatory Certification, Trademark

**Project:** Outer Bounds (working name). A portable, battery-powered golf launch monitor. It uses global-shutter cameras with pulsed IR illumination, possibly fused with a small radar, and measures spin and club data without markers. It connects over Wi-Fi/BLE to a PC or iPad and has no subscription.
**Prepared:** 7 October 2026
**Status of this document:** This is landscape groundwork, not legal advice. **Before launch you need a freedom-to-operate (FTO) opinion from a registered US patent attorney, plus EU/UK/JP/KR counsel for those markets.**
- Expiry dates below are estimates: 20 years from the earliest US non-provisional or PCT filing, plus patent term adjustment (PTA) where it is printed on the patent. Where Google Patents shows an "anticipated expiration", that date is used.
- Maintenance-fee lapses, terminal disclaimers and continuations can change any date.
- Every patent number below was read either from a fetched Google Patents page or from the OCR'd USPTO front page and claims PDF (`image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/<number>`). Anything not confirmed is marked **[UNVERIFIED]**.

> **Research limits (be aware):** Partway through, the shared web-search quota ran out, Google Patents returned HTTP 503, and Justia, fccid.io and FCC EAS returned 403. I worked around this by OCR-ing USPTO PDFs and querying the CourtListener and USPTO trademark-search back ends directly. Coverage of **Uneekor, SkyTrak, Garmin, ProTee, Voice Caddie, Bushnell's own filings, Sumitomo/Bridgestone, and Korean court cases** is therefore thin or missing. The checklist in §6 lists what still needs to be pulled.

---

## 0. Executive summary

1. **The foundational markerless photometric-spin patents have expired in the US.**
   - Wintriss Engineering filed them in 2002–03; WAWGD/Foresight Sports acquired them in 2013.
   - They cover a single smart camera, unmodified balls (dimples, scuffs, logos), finding spin by repeatedly rotating, scaling and correlating ball images, and triggering from the camera's own images.
   - **US 7,292,711 expired 2025-04-16; US 7,324,663 expired 2025-08-07** ("Expired – Lifetime" on Google Patents).
   - The Acushnet/Gobush marker-based stereo patents from the 1990s (US 5,471,383; US 5,501,463; US 6,241,622 and family) are also expired.
   - This gives us a strong, free-to-practise prior-art base for camera spin.
2. **The live risks are newer, narrower patents. There is no single blocking patent on markerless camera spin, but there are several minefields:**
   - **TrackMan's camera club-data family (US 10,953,303; 11,439,886; 11,612,801; 12,263,393; to around 2038–2039).** It covers markerless, single-imager impact location, club movement direction and "fix line" (shaft) angle at impact. This is the **highest-risk area for markerless club data.**
   - **TrackMan event detection with an imager (US 12,586,211, to around 2044)** and the pending **US 2024/0420346.** They cover switching the imager's operating state (frame rate or crop) once the ball is at address or the club moves, and spin via dense optical flow. These bear directly on side-of-ball triggering and on our spin pipeline.
   - **Rapsodo:**
     - **US 9,171,211 (to 2034):** natural-feature spin via polar transform and fit.
     - **US 12,582,870 (to 2044):** deep-learning spin using a 2D-ellipse model.
     - **US 10,754,025 / 11,747,461 (to around 2039):** a radar detects and tracks the ball, triggers the camera, and the data are fused into a trajectory. The continuation claims a Doppler track pool.
   - **Creatz (Square Golf's maker):**
     - **US 10,217,228 and 11,191,998:** mark-based spin, plus a fallback model that blends estimated and measured spin.
     - **US 11,946,734:** club measurement from two differently shaped club markers.
   - **Golfzon:**
     - **US 12,599,828:** marker-based spin.
     - **US 12,605,593:** ROI prediction from a projected physically reachable 3D volume.
   - **Foresight:**
     - **US 8,951,138 (to 2033):** stereo club tracking with three or more face markers.
     - **US 9,737,757 (to 2037):** stereo alignment-stick detection.
   - **Acushnet "launch monitor" family (US 7,837,572 to 2027-10; US 8,475,289 to around 2032-12; others).** These are narrow but have odd claims to avoid, such as a remote device telling the unit to reduce battery draw, or a teeing aid that measures the distance from the trigger to the ball.
3. **Radar is the most heavily patented layer.** It includes:
   - TrackMan spin from Doppler harmonic spacing (US 8,845,442, to 2029), spin axis from three or more receivers (US 10,850,179 / 11,446,546, to around 2039), radar+imager fusion (US 10,989,791 / 11,828,867, to 2037) and radar–camera calibration (to 2041).
   - EDH/FlightScope spin axis and spin rate (to 2034–2035).
   - Full Swing CW+FMCW (to 2039).
   - Rapsodo radar-triggered fusion (to 2039).
   - **Recommendation:** v1 should be camera-only with camera self-triggering. If radar is added, it should measure only ball and club speed from Doppler (1990s art, expired) and wake the system, with no radar–camera geometric fusion, no radar spin, and no radar-to-camera calibration loop. Get a written FTO before shipping any fusion feature.
4. **Litigation pattern.** The incumbents have rarely sued each other on patents in US federal court, and I found none on CourtListener. The visible US activity is of three kinds:
   - **Patent assertion entities (NPEs)** suing on broad "sensor plus coaching" patents. Wyoming IP Holdings sued TrackMan and lost on §101 with prejudice in 2024, then sued Vista Outdoor/Bushnell (Launch Pro) and dismissed voluntarily after a settlement notice.
   - **Software copyright fights:** *TrackMan v. GSPro*, S.D.N.Y., still in discovery in 2026.
   - **Contract disputes** in the SkyTrak/SkyHawke orbit.
   - Expect NPE demand letters once we have revenue. Budget for it, and keep a §101/IPR defence playbook ready.
5. **Regulatory path (US first).**
   - Choose a **pre-certified Wi-Fi/BLE module**, so the host needs only Part 15B SDoC plus a KDB 996369 integration check.
   - If radar is included, **it is the only intentional radiator needing its own FCC certification.** Use §15.245 at 24.075–24.175 GHz, roughly +32.7 dBm EIRP average allowed. Avoid 60 GHz §15.255 unless you can live with its EIRP and off-time limits.
   - **IR strobes need an IEC 62471 risk-group assessment.** Design them to be Exempt or RG1 at the closest user distance. If you use VCSELs (lasers) instead of LEDs, you take on IEC 60825-1 and FDA 21 CFR 1040.10, so prefer LEDs.
   - **Battery:** UN 38.3, IEC 62133-2, and a 30% state of charge for packed-with-equipment air shipping since 1 Jan 2026.
   - **EU:** the Battery Regulation makes portable batteries **user-removable and replaceable from 18 Feb 2027**, so design for it now. Also the RED cybersecurity rules (EN 18031, applied since 1 Aug 2025) and the CRA (vulnerability reporting from 11 Sep 2026, full application 11 Dec 2027).
   - **Rough all-in certification budget:** US + Canada **$25–60k** (camera-only) or **$40–85k** (with radar); EU + UK adds **$25–60k**; JP, KR and AU/NZ add **$25–60k**. Timeline is about **3–5 months** from a design freeze to US/CA/EU marks if pre-scans are done early.
6. **Name.** "OUTER BOUNDS" has **no live US registration** (four dead ones in classes 18, 24, 25 and 28).
   - The closest live conflict is **OUTERBOUNDS (Reg. 6,997,555, Step Computing Inc.)** in classes **9, 35, 41 and 42** for data-science and MLOps software. That company is Outerbounds/Metaflow, which is being acquired by Anaconda. It owns outerbounds.com.
   - **OUTTA BOUNDS GOLF (Reg. 7,986,926, class 41, driving range)** is a golf-specific near-homophone.
   - Risk is **low for class 28 and class 9 hardware**, and **moderate for class 9/42 software and apps.** The domain and SEO collision is significant. Get an attorney clearance search and consider a compound mark such as "Outer Bounds Golf" or a coined name.

---

## 1. Patent landscape

**Risk scale (for our design: markerless photometric camera, optional small radar, side-of-ball or down-the-line, battery):**
- **H**: likely to read on a plausible implementation; needs claim-by-claim FTO and a deliberate design-around.
- **M**: reads on some implementation choices; avoidable with care.
- **L**: narrow or off-architecture.
- **Free**: expired or lapsed; usable as practice and prior art.

### 1.1 Expired foundational patents (free to practise; strong prior art)

| Patent | Title / assignee | Priority / filing | Status / expiry | What it teaches (plain English) | Use for us |
|---|---|---|---|---|---|
| **US 7,324,663 B2** | Flight parameter measurement system — Wintriss Engineering → **WAWGD Newco (Foresight Sports)** | Prio. 2002-06-06; filed 2003-06-06 | **Expired – Lifetime, 2025-08-07** (Google Patents) | Claim 1: capture several images of a moving ball. Rotate one ball image through sets of 3D rotations, scale it to the next image, correlate, and refine stepwise to the best score, which gives spin. Compute 3D coordinates and elevation/azimuth. An **accelerometer** corrects camera misalignment. The specification uses **"non-precision marks, surface blemishes … dimples"** and **triggers from the camera's own images**. | **Core markerless-spin method, now free in the US.** EP1509781B1 was filed in 2003 and has passed 20 years; confirm it has lapsed. https://patents.google.com/patent/US7324663B2/en |
| **US 7,292,711 B2** | Flight parameter measurement system — same family | Prio. 2002-06-06; filed 2004-08-03 | **Expired – Lifetime, 2025-04-16** | System version: camera, memory, trigger, and a processor that rotates, scales and correlates the reference image to the target image to find the best rotation set. Audio output. Radar and microphone triggers are described. | Free. https://patents.google.com/patent/US7292711B2/en |
| **US 5,471,383** | Monitoring systems to measure and display flight characteristics of moving sports object — **Acushnet** (Gobush) | Prio. 1992-01-22; granted 1995-11-28 | Expired (well over 20 years) | Two cameras triangulate retro-reflective markers on the ball and club; portable. | Free stereo-triangulation prior art. https://patents.google.com/patent/US5471383A |
| **US 5,501,463** | Method and apparatus to determine object striking instrument movement conditions — Acushnet | Prio. 1992-11-20; granted 1996-03-26 | Expired | Club kinematics from markers using stereo. | Free club-tracking prior art. |
| **US 6,241,622 B1** (+ family: US 6,533,674; 6,286,364; 6,500,073; 6,781,621; 6,488,591; 6,616,543; 6,764,412; 7,086,955; 7,369,158) | Method and apparatus to determine golf ball trajectory and flight — Acushnet (Gobush et al.) | Filed 1998-09-18 | **Expired – Fee related**; anticipated expiry 2018-09-18. Family members filed 1998–2003 have all passed 20 years; confirm 7,369,158 individually. | A portable two-camera system with an **aperture/reflector lighting unit**. **Two flash images about 800 µs apart**, a sound trigger, and a calibration fixture. Ball has dot markers. | **Free** multi-exposure strobe and stereo prior art. https://patents.google.com/patent/US6241622B1/en |
| US 4,136,387 | Golf club impact and golf ball monitoring system | 1979 | Expired | Six cameras, pre- and post-impact. | Prior art. |
| US 5,342,051 (Rankin) | Ball/club monitoring (cited against Golfzon) | Early 1990s | Expired | Camera-based ball tracking. | Prior art. |
| **Radar (from the radar sub-study):** US 5,092,602 (Witler, 1990); US 5,138,322 (Matrix Eng., 1991); US 5,246,232 (Colorado Time Systems, 1992); **US 5,700,204** (Teder, 1996; off-axis wide-beam Doppler; expired 2016); **US 6,244,971** and **US 6,547,671** (Distancecaddy, 1999; radar spin from a modulated-reflection ball, and launch angle from Doppler at an offset) | — | 1990–1999 | Expired | Doppler ball speed and carry; launch angle from an off-axis Doppler model; radar spin with special balls. | **Free basis for a "radar = speed/trigger only" design.** |
| **TrackMan expired or lapsed** | US 8,912,945 (deviation family), US 9,857,459, US 10,471,328; **all EP spin-family members** (EP1698380, EP1853362, EP2218483: lapsed or expired 2025–2026); EP1763683 (2025) | — | Expired or lapsed per Google Patents | — | In Europe, TrackMan's original 2005 radar-spin family is **dead**. |

> **Caveat on "Expired – Lifetime":** this is Google's estimate. Confirm in USPTO Patent Center that there is no pending reissue or reexamination, and no extension or terminal-disclaimer quirk.

### 1.2 Live camera / photometric patents

| # | Patent | Assignee | Priority / filing | Est. expiry | Core independent claim (plain English) | Risk |
|---|---|---|---|---|---|---|
| C1 | **US 9,171,211 B2**, "Image processing for launch parameters measurement of objects in flight" | **Rapsodo** | 2013-09-20 | **2034-06-05** (Google Patents, active) | From the abstract and summary (claims text not loaded): find the ball's radius and centre in each frame using a threshold tuned for bright conditions; compute velocity and angles from pre-measured camera alignment; crop to the smallest bounding square; **unwrap the spherical image to Cartesian, then polar coordinates over candidate rotation centres**; get spin axis and rate from the fit of the polar image pair. Uses natural markers (dimples, logo). Continuation US 2016/0110880. https://patents.google.com/patent/US9171211B2/en | **M–H** if we use a polar-transform spin fit. **Avoid that pipeline;** use 3D rotation search or registration on a sphere model, as in the expired Wintriss art. |
| C2 | **US 12,582,870 B2**, "Estimating spin rate and axis of a ball using deep learning" | **Rapsodo** | 2024-05-20 | **2044-12-20** | Train a DL network on spinning balls whose feature point traces a **3D circle that projects to a 2D ellipse**. Predict spin measurements from image sequences, compute spin rate, fit **2D ellipse-model coefficients**, and derive the 3D spin axis. Feature point can be a "dot, scratch, dimple or seam". US-only family. https://patents.google.com/patent/US12582870B2/en | **H** if we use learned spin with an ellipse model. **M** for any DL spin: write the ML pipeline to regress rotation directly, for example a quaternion/SO(3) between frames, with **no ellipse-model step**. |
| C3 | **US 12,530,796 B2**, "Spin estimation for marked objects" (+ cont. US 2026/0112058; EP4510085A1; JP7821848B2; KR20250020359A) | **Rapsodo** | 2023-08-03 | **2044-01-07** | Abstract-inferred: set frame rate from the minimum spin; **print an orientation marker** (cuboid-face patterns); segment markers, then estimate spin with DL. https://patents.google.com/patent/US12530796B2/en | **L** for markerless. **H** if we ever ship a printed "premium ball" mode. |
| C4 | **US 2024/0420346 A1** (pending; EP4728473A1; WO2024256969A1), "System and method for spin rate and orientation using an imager" | **TrackMan** | 2023-06-14 | Pending (would run to about 2043+) | Independent groupings: (a) an imager in low-power mode; when ball or club motion conditions are met (address, takeaway), **change imager operating state** (frame rate, resolution, crop) and capture a second sequence; (b) **dense optical flow (DOF) model → pixel displacement → 3D spin**, with a DL ball segmentation. Single imager, radar optional. https://patents.google.com/patent/US20240420346A1/en | **H (watch).** Track prosecution. Avoid a DOF-based spin pipeline and an "operating-state change on motion" trigger. |
| C5 | **US 12,586,211 B2**, "Event detection using an imager" | **TrackMan** | ~2023–24 | **2044-03-15** | Abstract-inferred (radar sub-study): detect the ball at rest and the club moving away, then switch to a higher frame rate or crop. https://patents.google.com/patent/US12586211B2/en | **H for side-of-ball triggering.** See the design-around in §3.3. |
| C6 | **US 10,953,303 B2**, "Determining impact characteristics of sports ball striking element" | **TrackMan** | 2017-12-22 | **2039-03-23** | Claim 1: track a reference point on the club in two frames near impact; find impact time, ball position and imager-to-impact distance; output **impact location on the face**. **Single camera, no markers.** https://patents.google.com/patent/US10953303B2/en | **H** for markerless impact location. |
| C7 | **US 11,439,886 B2** | **TrackMan** | 2017-12 | **2039-03-10** | Rate of change of distance to the club plus impact distance gives **3D club movement direction**. Dependent claim 2 covers attack angle. https://patents.google.com/patent/US11439886B2/en | **H** for club path and attack angle. |
| C8 | **US 11,612,801 B2 / US 12,263,393 B2** | **TrackMan** | 2017-12 | **2039-03-24 / 2038-12-18** | Find a **"fix line"** (for example the shaft) in images near impact; its angle at impact gives an impact characteristic such as dynamic loft or lie. https://patents.google.com/patent/US11612801B2/en | **H** if we derive loft or lie from shaft or line angle. |
| C9 | **US 8,951,138 B2**, "Golf club head measurement system" (EP2815384B1, CA2862818C, KR101930914B1 active) | **WAWGD (Foresight)** | 2012-01-25 | **2033-05-14** | Claims 1 and 21 require **at least three markers on the club face**: two on a heel-toe line parallel to the score lines and one off-line. At least two cameras; threshold the images, get 3D marker positions, label markers by geometric rules, compute club position. https://patents.google.com/patent/US8951138B2/en | **L** for truly markerless. **H** if we ever use face stickers in this geometry. |
| C10 | **US 9,737,757 B1**, "Golf ball launch monitor target alignment method and system" (+ US 2018/0133578, WO2018093415, KR102248980B1) | **WAWGD (Foresight)** | Prov. 2016-11-16; filed 2017-04-29 | ~**2037-04-29** | Claim 1: **two image sensors** detect horizontal edges of an **alignment stick**; project edges to vectors; best-fit a plane per sensor; **intersect the planes** to get the azimuth offset. (USPTO OCR) | **M** if we build an alignment-stick auto-aim. Use a single-camera or IMU-plus-target-tap alternative. |
| C11 | **US 10,639,537 B2**, "Golf ball tracking system" | **WAWGD** | 2018-01-23 | ~2038-12-31 | Fusing launch-monitor-predicted flight with an observed range-camera trajectory and landing event. (USPTO OCR) | **L** (range product). |
| C12 | **US 10,217,228 B2**, "… measuring ball spin" | **Creatz** | KR 2016-06-29; US filed 2017-06-29 (+14 d PTA) | ~**2037-07-13** | Detect a "mark" on the ball across frames; build a mark sequence; spin from that sequence. **Requires** compensating each mark for the camera **line-of-sight vs. a virtual gravity-aligned camera**, rotating mark coordinates on a spherical coordinate system. (USPTO OCR) | **M.** "Mark" is not limited to printed markers and could read on logos. Avoid the specific line-of-sight compensation step, or do the compensation differently. |
| C13 | **US 11,191,998 B2**, "… measuring ball spin" | **Creatz** | KR 2018-10-29; US filed 2019-10-29 | ~**2039-10-29** | Detect marks; **decide whether spin is directly calculable**. If not, **estimate spin from ball or club speed and angle**. If it is, **use the estimated spin to correct the mark-measured spin.** (USPTO OCR) | **M–H.** A "fallback spin model when spin is not measurable" is a very natural feature. Do not *blend or correct* measured spin with model spin, or report a model value as a fallback without counsel review. |
| C14 | **US 11,946,734 B2**, "… measuring physical quantities associated with a golf club" | **Creatz** | PCT 2021-01-12 (KR 2020-01-16); +477 d PTA | ~**2042-05-04** | **First and second markers of different shapes** on the club head define a target area. Club quantities (direction, attack, lie, face) come from the target area's properties and its **size change** between frames. (USPTO OCR) | **L** for markerless. |
| C15 | **US 9,605,960 B2** (+ US 9,329,037; 9,448,067; 9,752,875; 10,247,553), "… acquiring actual movement trajectory …" | **Creatz** | KR 2011-09-23 | **2032-09-24** | Trajectory from the ball's image positions (which fix a plane) plus image **diameters** via a pre-stored size-to-trajectory database. https://patents.google.com/patent/US9605960B2/en | **L** (overhead/screen-golf geometry). |
| C16 | **US 12,599,828 B2**, "Spin calculation method for golf ball … " | **Golfzon** | KR 2021-03-30 | **2043-03-14** | Ball **with a plurality of markers**: match a reference and surrounding markers between frames by relative slope angles; spin from the centres of matched marker pairs (plane intersections), with a gaze-rotation correction. https://patents.google.com/patent/US12599828B2/en | **L** for markerless. |
| C17 | **US 12,605,593 B2**, "Image analysis method for sensing moving ball …" | **Golfzon** | KR 2021-07-22; PCT 2022-07-08; +267 d | ~**2043-04-01** | Detect the ball, then set the **analysis area** for the next frame by **computing the 3D region the ball can physically reach (preset limit physical quantities, optionally per club type) and projecting it into the camera view**. (USPTO OCR) | **M.** A common ROI-tracking idea. Use 2D image-space prediction (Kalman or optical flow) or fixed sensor windows instead of projecting a physically bounded 3D volume. |
| C18 | Golfzon older US family: US 9,514,379; US 9,333,409 (2011 prio.); CN111465434B (2017) | Golfzon | 2011–2017 | 2031–2038 | Screen-golf sensing devices (not fetched in detail). | **L–M**; review in FTO. |
| C19 | **US 7,837,572 B2**, "Launch monitor" | **Acushnet** | 2004-06-07 | **2027-10-05** (Google Patents) | **Every** independent claim (1, 15, 27, 36, 48) requires a networked camera launch monitor **and a remote data-processing device that instructs the processor to reduce power consumption from the battery.** | **M until Oct 2027.** Keep the power policy on the device; the app must not command low-power modes. |
| C20 | **US 8,475,289 B2**, "Launch monitor" | Acushnet | Filed 2004-06-07; **+3,116 d PTA** | ~**2032-12-18** (if fees paid; the 12-year fee was due around Jan 2025, so check) | Claim 1: a camera system plus a **teeing aid that helps place the ball in the field of view and determines the distance between a trigger and the placement of the ball.** (USPTO OCR) | **M.** Ball-placement guidance UIs are common. Avoid measuring or claiming "trigger-to-ball distance", or confirm the patent has lapsed. |
| C21 | **US 8,500,568 B2**, "Launch monitor" | Acushnet | Filed 2004-06-07; +2,139 d; **terminal disclaimer** | ≤2030-04-16 (the terminal disclaimer may make it earlier) | Automatic club identification by **eigenvalues** of images vs. stored references, in about 6 s or less. | **L** (avoid eigenvalue club ID). |
| C22 | **US 8,622,845 B2**, "Launch monitor" | Acushnet | Filed 2004-06-07; +1,578 d | ~2028-10-02 | A **pivoting trigger** angled left or right for handedness, plus a handheld remote. | **L.** |
| C23 | **US 10,668,350 B2**, "Launch monitor using three-dimensional imaging" | Acushnet | Filed 2017-12-22 (+16 d) | ~2038-01-07 | Camera system with a **light-field (plenoptic) camera** generates 3D images and kinematics. | **L** unless we use light-field optics. |
| C24 | **US 2024/0123314 A1** (pending; AU, CN, WO), "Golf ball trajectory monitor" | **Open Launch LLC** | 2022-10-18 | Pending | Radar detects club or ball motion and **triggers camera 1, then camera 2**; the images are fused with radar data into a trajectory and displayed. | **Watch.** Directly on point for a radar-triggered two-camera design. |

**Not yet covered (fetch before FTO):**
- **Uneekor** (EYE XO/QED/EYE MINI; Korean assignee). No results on Google Patents under "Uneekor"; filings may be under founders or a former entity name. **[UNVERIFIED]**
- **SkyTrak** (SkyHawke/Golf Labs/GolfTec).
- **Garmin** (R50 is camera-based).
- **ProTee Labs**, **Full Swing camera filings**, **Bushnell**.
- **Sumitomo Rubber / Bridgestone / Yokohama** ball-spin imaging (mostly 2000s; likely expired or expiring; good prior art).
- **TrackMan US 11,935,? spin-from-imager continuations.**
- **Topgolf Callaway / Topgolf Sweden** (Toptracer) imaging patents: US 11,918,863; US 12,285,656; US 12,361,570; US 11,995,846 (seen only as citations in US 12,582,870).
- **Foresight** filings after 2018 (e.g., QuadMAX/Falcon), and **US 7,641,565** (ball-placement detection; seen only).

### 1.3 Live radar and radar+camera patents (from the radar sub-study; all verified on Google Patents unless noted)

| Patent(s) | Assignee | Est. expiry | Core claim | Risk for "camera + small radar" |
|---|---|---|---|---|
| **US 8,845,442** (Determination of spin parameters of a sports ball) | TrackMan | **2029-05-18** | Spin from the **frequency spacing of Doppler modulation harmonics** around the ball-speed line. | **H** if the radar measures spin. **Don't.** |
| US 9,645,235 / US 10,393,870 (continuations) | TrackMan | 2026-07-17 (expired) / **2026-12-21** | Same, for unmarked balls. | Expires within about 2 months. |
| **US 10,850,179 / 11,446,546** (+ US 11,938,375; US 2024/0316402 pending) | TrackMan | **2038-12 / 2039-01** | Spin axis: **three or more non-collinear receivers**; split the Doppler spread into frequency bands; angle per band from phase; axis perpendicular to the fitted line. | **H** if radar spin axis is used. |
| **US 9,958,527** (Direction of arrival) | TrackMan | **2034-02-01** | A **parallelogram of 3+ antennas plus an offset antenna** for single-pulse 3D direction of arrival (≤6 antennas). | **M.** Use a different array geometry. |
| **US 10,989,791 / 11,828,867** (+ US 2024/0045021 pending) | TrackMan | **2037** | **Radar range (or range-rate) plus imager-only angular positions**, fused into a 2D/3D track. | **H** for any radar–camera geometric fusion. |
| **US 11,619,708 / 12,517,218** | TrackMan | **2041** | Inter-sensor calibration: radar-only track vs. camera-angle plus radar-range track gives correction parameters. | **H** if the radar and camera self-calibrate against each other. |
| **US 11,748,985 / 12,067,775** | TrackMan | 2040–2041 | A radar-detected event (impact) picks the nearest camera frame by synchronized clock for a composite image. | **M.** Avoid radar-timestamped frame selection. |
| US 8,085,188 (deviation from target line); US 10,690,764; **US 10,473,778** | TrackMan | 2027-06 / 2026-07 / 2026-09 | Radar trajectory relative to a target picked in an image; radar correlated with an image of the launch area. | Expiring or expired. **L–M**; 8,085,188 runs to mid-2027. |
| **US 9,855,481; US 11,135,495; US 10,052,542** | TrackMan | 2029–2030 | Radar trajectory **overlaid on the camera image** using known radar/camera coordinate frames. | **M** if we draw tracer video from radar data. |
| US 11,673,029 / 12,179,068 | TrackMan | 2040 | **A ball** with radar-contrasting markers on every great circle. | **L** (ball product). |
| **US 10,151,831 / 10,775,492** (US only; EP withdrawn) | EDH (FlightScope) | **2035** | Spin axis from the **time delays of spin modulation between perpendicular receiver pairs**. | **H** if radar spin axis is used. |
| **US 9,868,044** | EDH | **2034-04-05** | Spin rate from **seam/feature modulation of the Doppler phase**. | **H** if radar spin rate is used. |
| **US 11,940,525 / 12,146,945** | Rapsodo | **2042** | Radar time-frequency image to a **neural network** for spin. | **H** if ML radar spin is used. |
| **US 10,754,025** (exp. 2039-01-18) / **US 11,747,461** (~2039-04) | Rapsodo | 2039 | '025 cl. 1: **radar detects and tracks the object, triggers the camera, the object is detected in images, radar and camera data are combined to estimate position, the radar track is identified, and the trajectory is estimated.** '461 cl. 1: Doppler-frequency **radar track pool** used to predict the next Doppler frequency and trajectory. (USPTO OCR) | **H** for radar-trigger-plus-fusion. '461 is broad on radar track management. |
| **US 11,311,789** (+ US 11,844,990; US 2024/0216777; EP3877061B1) | Full Swing | **2039-11-08** | **CW + FMCW** radar (FMCW range ≥75 m; time-division CW speed/spin and FMCW range; non-uniform array plus deep learning). | **M–H** if we use CW/FMCW time-division. |
| Range products: US 10,379,214 family; US 10,444,339 family; US 11,452,911 | TrackMan | 2037+ | Multi-bay, skid/roll, missed-shot recovery. | **L.** |
| **TrackMan's patent-marking page** lists 47 US patents, at https://www.trackman.com/legal/patents (fetched by the sub-study, page dated 2026-08-11). | | | | Use it as the TrackMan FTO checklist. |

---

## 2. Litigation history (what is actually on the record)

Sources: CourtListener RECAP dockets, read directly. PACER-derived documents were read where available.

| Case | Forum / No. | Dates | What happened | Lesson |
|---|---|---|---|---|
| **Wyoming Intellectual Property Holdings LLC v. TrackMan Inc.** | D. Ariz. 2:23-cv-02518 (Judge Tuchi) | Filed 2023-12-06; **dismissed with prejudice 2024-11-07** | NPE asserted **US 9,384,671 "Instruction Production"** (priority 2013) against TrackMan 4. The patent covers a sensor capturing an action, comparing it with standard actions, selecting the closest, and instructing the user. TrackMan's Rule 12(b)(6) motion argued **§101 ineligibility (abstract idea)**, and the court granted it with prejudice. Willfulness allegations had already been dismissed with prejudice by stipulation. TrackMan also filed a statement of attorney fees (Doc 24). https://www.courtlistener.com/docket/68068135/ ; order: https://storage.courtlistener.com/recap/gov.uscourts.azd.1354641/gov.uscourts.azd.1354641.34.0.pdf | **NPEs target launch monitors with generic "measure and coach" patents.** Early §101 motions work. |
| **Wyoming IP Holdings v. Vista Outdoor Inc. (dba Bushnell)** | E.D. Tex. 2:24-cv-00340 (Judge Gilstrap) | Filed 2024-05-08; **notice of settlement and stay 2024-08-27; voluntary dismissal 2024-09-10** | Same '671 patent asserted against the **Bushnell Launch Pro** (claim chart, Exhibit 2). Settled within about 4 months, before the Arizona §101 ruling. https://www.courtlistener.com/docket/68512344/ | The same NPE monetises by **quick, small settlements.** Expect a letter once we have sales. |
| **TrackMan, Inc. v. GSP Golf AB (GSPro), Bogavac, SimulatorGolfTour LLC, Cooke** | S.D.N.Y. 1:23-cv-00598 (Judge Buchwald) | Filed 2023-01-24; **active** (discovery 2025–26; counsel filings Sep–Oct 2026) | Copyright claims (direct and secondary), breach of EULA, and false advertising. TrackMan says defendants copied **Perfect Golf / Course Forge** (Perfect Parallel, a TrackMan affiliate) and converted courses for GSPro. The **2024-09-24 Memorandum & Order** dismissed the contract claim but **kept the copyright and false-advertising claims.** Defendants have counterclaimed. https://www.courtlistener.com/docket/66755222/ ; M&O: https://storage.courtlistener.com/recap/gov.uscourts.nysd.592874/gov.uscourts.nysd.592874.62.0.pdf | Our product will rely on third-party sim software (GSPro, E6, Awesome Golf, TGC). **Use only published or licensed connector APIs**, never reverse-engineered code or course assets. TrackMan litigates hard over its software ecosystem. |
| **SkyHawke Technologies, LLC v. GolfTec ST LLC** | S.D. Miss. 3:23-cv-03157 | Filed 2023-12-14; active (entries through 2026-04-30) | No documents available on RECAP. "GolfTec ST" is presumably the GolfTec entity that acquired **SkyTrak**. **[Nature of the claims UNVERIFIED; likely contract or acquisition-related.]** https://www.courtlistener.com/docket/68092224/ | Supplier and acquirer disputes are common in this segment. |
| SkyHawke v. DECA International (GolfBuddy) | C.D. Cal. 2:18-cv-01234, 2:18-cv-10408 | 2018–2020 | Patent suits over GPS rangefinders (not launch monitors). Related antitrust case: SkyHawke v. GolfzonDeca, C.D. Cal. 8:19-cv-01692 (2019–2021). | The SkyCaddie/SkyTrak group uses its patents aggressively. |
| Battery Conservation Innovations v. SkyHawke | S.D. Miss. 3:19-cv-00327 | 2019; terminated 2019-09-19 | NPE suit on a battery-conservation patent. | **Battery-powered golf devices attract NPEs.** |
| EDH (South Africa) (Pty) Ltd v. AboutGolf Ltd | M.D. Fla. 6:09-cv-00444 | 2009-03 to 2009-09 | Trademark case (nature of suit 840) brought by FlightScope's maker; terminated within 6 months. **[Details UNVERIFIED]** | Trademarks are actively policed in this niche. |
| Sportvision/SMT v. MLB Advanced Media | S.D.N.Y. 1:18-cv-03025 | 2018 to present (summary judgment briefing 2026) | Trade secret and patent claims over PITCHf/x vs. its replacement, **TrackMan** (baseball). TrackMan was a subpoenaed third party. | Shows how deep TrackMan's radar IP runs in adjacent sports. |

**What I did not find in US federal dockets on CourtListener (as of 2026-10-07):**
- No patent suits by **TrackMan, Foresight/WAWGD, Rapsodo, FlightScope/EDH, Uneekor, Golfzon, Creatz, Full Swing, Garmin, Ernest Sports, or Voice Caddie** against a competitor.
- Party-name searches for Rapsodo and Uneekor returned zero cases.
- I **could not verify** reported **Korean** disputes, for example Golfzon v. Kakao VX or Golfzon v. Creatz over screen-golf sensing patents. Commission Korean counsel to search Korean court and KIPO/IPTAB records.
- I **could not verify** EU or UK proceedings (UPC, German courts) or PTAB IPRs; the PTAB API has moved.
- TrackMan's own marking page describes its fusion and club-data technology as patented. Marking is a pre-suit notice tool, not evidence of suits.

**Implications for a new entrant:**
1. **Competitor-on-competitor patent wars have been rare in the US, but the incumbents hold large, current portfolios** (TrackMan has 47 marked US patents). A low-priced, visible entrant that copies TrackMan or Rapsodo *club-data or fusion features* is the likeliest trigger for a first suit. Product positioning and FTO hygiene both matter.
2. **NPEs are the most likely first plaintiff.** Keep about $50–150k for early-dismissal defence or nuisance settlement in year 1–2 of sales. Consider joining a defensive pool or carrying IP-defence insurance.
3. **§101 is a strong shield for "measure, compare, coach" claims** (*WIPH v. TrackMan*). It does **not** protect against hardware or signal-processing claims such as TrackMan's radar spin or Rapsodo's polar-transform spin.
4. **Software and content IP is enforced** (*TrackMan v. GSPro*). Build our own course and sim content, or license it. Interoperate only through documented open APIs such as the GSPro Open Connect API. Keep clean-room records.
5. **File our own patents early** (provisionals before any public demo or crowdfunding) to build cross-licence leverage, and have counsel write an **invalidity/prior-art file** around the expired Wintriss and Acushnet art.

---

## 3. Design-around strategy (lowest-risk technical choices)

### 3.1 Markerless spin (camera)
**Lowest risk:** practise the expired Wintriss/Foresight method (US 7,292,711 / 7,324,663).
- Several frames of the ball, either strobed multi-exposure or a burst.
- Back-project each ball image onto a **3D sphere model**.
- Search over 3D rotations (coarse to fine), score by correlation of dimple/feature texture (photometric registration), and refine.
- Calibrate the camera to gravity with an accelerometer.

Then **avoid** these later, narrower claim hooks:
- Polar-coordinate unwrapping over candidate rotation centres with a 1D fit (Rapsodo '211, to 2034).
- A DL pipeline that fits a **2D ellipse model** of a feature-point trajectory (Rapsodo '870). If we use ML, regress SO(3) rotation or quaternion directly from image pairs, or use ML only for ball segmentation.
- **Dense optical flow → pixel displacement → 3D spin** (TrackMan pending '346). Use sphere-model rotation search instead of DOF.
- Line-of-sight compensation of marks to a virtual gravity-aligned camera (Creatz '228).
- **Blending model-estimated spin into measured spin** (Creatz '998). If spin can't be measured, report "spin unavailable" or a clearly separate estimate with no correction step, and get counsel sign-off.

**Hardware:**
- Multiple strobed exposures in one global-shutter frame, or 2–4 synchronized frames.
- The two-flash approach (Acushnet 1998) is expired art.

### 3.2 Club data without markers
This is **the highest-risk part of our feature set.** The TrackMan '303/'886/'801/'393 family (to about 2039) covers single-imager markerless impact location, club direction from the rate of change of distance, and shaft "fix-line" angle at impact.

**Candidate design-arounds (FTO counsel to validate against the claims):**
- **Stereo dense 3D reconstruction** of the club-head surface or silhouette (two or more synchronized cameras, structured or strobed IR). Fit a face-plane model to get face angle, loft and lie, instead of tracking one reference point and the imager-to-impact distance. TrackMan's claims are framed around a reference point or line and imager distance; a full-surface, multi-view model fit is structurally different.
- **Impact location inferred from ball launch** (gear effect: ball spin-axis tilt and launch direction vs. face/path) instead of from club imaging near impact. This builds on old physics models and is not tied to TrackMan's impact-imaging claims.
- **Don't compute loft or lie from shaft-line angle.** Use the face-plane normal instead.
- **Avoid face stickers** in Foresight's three-marker heel/toe geometry ('138) and two-shape markers (Creatz '734). If an optional marker mode is ever offered, use a different marker design and get FTO.

### 3.3 Triggering (side-of-ball)
- **Lowest risk:** self-triggering from a continuously running camera, in particular a **ring buffer of a fixed ROI at constant high frame rate**. Trigger *on ball departure* (ball pixels leave the tee region), then pull the pre- and post-trigger frames from the buffer. Camera self-triggering is taught by the expired Wintriss patents. Acoustic and sound triggers are 1990s Acushnet art (expired).
- **Avoid:** the TrackMan '211 and pending '346 pattern of *changing the imager's operating state (frame rate, resolution, crop) upon detecting address or takeaway.* If power saving needs a low-rate preview mode, have counsel review the claims. Use a hardware wake source (PIR, IMU tap, or user "ready" button) rather than image-detected address/takeaway, or keep one constant capture mode.
- **Avoid:** the radar-detects → radar-tracks → triggers camera → fuses data chain (Rapsodo '025, Open Launch pending).
- **Avoid:** a teeing aid that computes the distance between the trigger and the ball (Acushnet '289, to about 2032).

### 3.4 Radar (if any)
**Recommendation:** ship **v1 camera-only.** If radar is added in v2, restrict it to:
- **Doppler ball and club speed** (1990s art, expired), and
- **wake-up / shot-detect**,
- with **no** geometric fusion into camera tracks, **no** radar spin, **no** radar–camera mutual calibration, and **no** radar-picked frame selection.

Even "radar track → trigger camera" sits near Rapsodo '025 claim 1, which requires *combining* radar and camera data to estimate position and the trajectory. A radar used purely as a wake and speed sensor, whose data never enter the position estimate, appears outside it, but **get an FTO opinion.** Avoid TrackMan's parallelogram antenna array ('527) and Full Swing's CW/FMCW time-division ('789).

### 3.5 Other product details that touch claims
- Have the **device decide its own sleep and low-power states.** Do not let the iPad/PC send "reduce power" commands until Acushnet '572 expires on 2027-10-05.
- Do not use **eigenvalue club identification** (Acushnet '568).
- For **alignment**, avoid two-sensor alignment-stick plane intersection (Foresight '757). Prefer target-pick in a single camera view, or IMU heading plus a user tap on the target.
- For **ROI tracking**, avoid projecting a physically bounded 3D reachable volume (Golfzon '593). Use 2D predictive tracking.

### 3.6 Process
1. Patent counsel produces a **claim chart for the roughly 25 "H/M" patents above** against our actual architecture, about 8–12 weeks before tooling. Budget: **$40–120k** for a focused FTO with written opinions on the top 5–10 patents.
2. Keep **engineering notebooks** and dated design docs that record the design-around reasoning. They help defend willfulness and support our own filings.
3. **File provisionals** on our own innovations, such as sphere-registration speed-ups, IR strobe timing and multi-view face fitting. A US provisional costs about $3–8k with counsel; a PCT costs about $5–10k at 12 months.
4. Set **monitoring alerts** on TrackMan US 2024/0420346, the 2024/0045021 fusion continuation and 2024/0316402, Rapsodo continuations, Open Launch 2024/0123314, and Golfzon/Creatz US filings.

---

## 4. Regulatory and certification

### 4.1 Architecture choices that drive cost
| Choice | Lower cost / risk | Higher cost / risk |
|---|---|---|
| Wi-Fi/BLE | **Pre-certified module** with FCC, ISED, CE-RED reports, MIC (JP), KC (KR) and RCM support. Examples: u-blox, Murata, Laird/Ezurio, Espressif modules with full certification packages. Keep the module's antenna as certified. | Chip-down radio design: full intentional-radiator testing in every market. |
| 5 GHz Wi-Fi | 2.4 GHz only, which avoids EN 301 893 DFS testing. | 5 GHz (better for video) adds EN 301 893 (DFS) in the EU and UNII rules (15.407) in the US, unless fully covered by the module grant. |
| Radar | None (v1) | 24 GHz under FCC **§15.245** (24.075–24.175 GHz) or **§15.249** (24.0–24.25 GHz); or 60 GHz under **§15.255**. |
| IR illumination | **LEDs**, designed to IEC 62471 **Exempt/RG1** at the closest user position. | **VCSEL/laser** illumination: a laser product under IEC 60825-1, plus a **US FDA CDRH product report** (21 CFR 1040.10/1040.11). |
| Battery | ≤100 Wh pack, which keeps UN3481 Section II shipping where applicable. Use a cell supplier with UN 38.3 and IEC 62133-2 reports. | >100 Wh: fully regulated Class 9 air shipping. A custom pack still needs its own UN 38.3. |
| Accessories | No coin cells. | A coin cell in a remote triggers US **Reese's Law** (16 CFR 1263) and Australia's mandatory button-battery standards. |

### 4.2 United States
- **FCC Part 15 Subpart B** (unintentional radiator, digital device).
  - Class B (consumer) uses **Supplier's Declaration of Conformity (SDoC)**: test at an accredited lab, no FCC filing, keep records, and include the compliance statement in the manual.
  - The strobe driver switches tens of amps in µs pulses. Plan **pre-compliance scans** early for radiated emissions from the strobe loop and the camera MIPI links.
- **Wi-Fi/BLE via a modular grant** (47 CFR §15.212; FCC KDB 996369).
  - The host carries the "Contains FCC ID: XXX" label and follows the module integration guide.
  - The host does Part 15B testing with the radio active and a spurious-emission check.
  - No new grant is needed unless antenna or trace changes break the modular conditions; a Class II permissive change or new FCC ID is needed if they do.
- **Radar (intentional radiator) needs FCC *Certification* via a TCB.** Rules, verified on eCFR via Cornell LII:
  - **§15.245 field disturbance sensors:** 24,075–24,175 MHz. Fundamental **2,500 mV/m at 3 m** (average), which is about **+32.7 dBm EIRP**. Harmonics 25 mV/m. Other out-of-band emissions −50 dBc or §15.209. Also 10,500–10,550 MHz at the same limits (X-band, used by older pro radars). https://www.law.cornell.edu/cfr/text/47/15.245
  - **§15.249:** 24.0–24.25 GHz, any use. Fundamental **250 mV/m at 3 m** (about +12.7 dBm EIRP), harmonics 2.5 mV/m, peak no more than 20 dB above average. https://www.law.cornell.edu/cfr/text/47/15.249
  - **§15.255 (57–71 GHz):**
    - Default limit: −10 dBm peak conducted and **10 dBm peak EIRP**.
    - **57–61.56 GHz:** up to **20 dBm EIRP only with off-times totalling ≥16.5 ms in every 33 ms.**
    - **57–64 GHz:** **14 dBm with ≥25.5 ms off per 33 ms.**
    - **61.0–61.5 GHz narrowband:** 40 dBm average / 43 dBm peak.
    - **Pulsed radar:** ≤6 ns pulses, ≤10% duty in any 0.3 µs window.
    - **Engineering consequence:** the off-time rules stop continuous observation of a 50–100 ms shot window at the higher EIRP levels. Either stay at ≤10 dBm EIRP (continuous allowed) or use the 61.0–61.5 GHz narrowband option (no range resolution). 24 GHz §15.245 is the better fit for a Doppler speed and trigger sensor.
    - https://www.law.cornell.edu/cfr/text/47/15.255
  - Comparable products: the FCC IDs of existing launch-monitor radars could not be pulled (fccid.io and FCC EAS returned 403). **[TO DO: look up Garmin Approach R10 (grantee IPH), FlightScope Mevo/Mevo+, Rapsodo MLM2PRO, Full Swing KIT, and TrackMan 4/iO on FCC EAS to see which rule part each used. Industry understanding is that consumer launch-monitor radars are 24 GHz K-band and TrackMan uses X-band around 10.5 GHz; this is unverified.]**
- **RF exposure:** §1.1307 / §2.1093 portable-device evaluation. The radar and Wi-Fi are low power, so an MPE or SAR exemption calculation is usually enough.
- **IR LEDs:** no FCC issue.
  - **FDA:** LED-only products are generally not subject to laser performance standards. VCSELs/lasers require 21 CFR 1040.10 compliance and an FDA product report (an accession number before import).
  - **UL/NRTL listing is not legally required** for a battery-powered consumer device. Amazon, Best Buy and Costco typically ask for **IEC/UL 62368-1, IEC 62133-2 and UN 38.3** reports, an SDS, and the UN 38.3 test summary.
- **Battery transport:** UN 38.3 (UN Manual of Tests and Criteria, T.1–T.8). A **UN 38.3 test summary** must be available down the supply chain.
  - **IATA DGR 67th ed. / ICAO TI 2025–26, from 1 Jan 2026:** Li-ion batteries **packed with equipment (UN3481, PI 966)** must ship at **≤30% state of charge**. Section II applies to batteries >2.7 Wh, unless State approval is given.
  - Batteries **contained in equipment (PI 967)**: ≤30% SoC (or ≤25% indicated) is **strongly recommended, not mandatory.**
  - Source: IATA Lithium Battery Guidance Document 2026, pp. 13–14, https://www.iata.org/contentassets/05e6d8742b0047259bf3a700bc9d42b9/lithium-battery-guidance-document.pdf
  - **Recommendation:** ship the battery installed (PI 967), set to 30% SoC at end of line.
- **Environmental and chemical:**
  - **California Prop 65:** warn if any listed chemical is present, for example DEHP in cables, lead in brass, or BPA. Easiest is to specify a phthalate-free BOM.
  - **California SB 1215:** battery-embedded products enter the covered electronic waste program from 2026. **[Verify fee and retailer obligations.]**
  - **State PFAS laws:** Maine and Minnesota reporting and bans. Get supplier PFAS declarations.
  - **California SB-327 IoT security:** unique per-device credentials.
  - Voluntary: FCC **"Cyber Trust Mark"**.

### 4.3 Canada (ISED)
- **ICES-003** (digital apparatus; label "CAN ICES-003(B)/NMB-003(B)"). This is the equivalent of FCC 15B, and the same lab can often test both together.
- **Radio:**
  - Module **IC certification** (RSS-247 for Wi-Fi/BLE, RSS-Gen) is reused with a host label "Contains IC: XXXX".
  - **Radar requires an ISED certification** (RSS-210 annex for field disturbance sensors; 24 GHz and 57–71 GHz). **[Verify the exact RSS-210 annex and limits.]**
  - **RSS-102** RF exposure.
- **Other:** bilingual (French) labelling and manual; provincial battery stewardship (e.g., Call2Recycle).
- **Cost:** usually **+$3–8k** on top of US testing if done at the same lab; ISED radar certification through a Certification Body is about +$3–6k.

### 4.4 European Union (CE)
- **Radio Equipment Directive 2014/53/EU (RED)** covers safety, EMC and radio. Typical harmonised standards:
  - **EN 300 328** (2.4 GHz). Add **EN 301 893** if 5 GHz is used.
  - **EN 301 489-1 / -17** (Wi-Fi/BT EMC), plus **-3** (SRD radar) if radar is fitted.
  - **EN 300 440** (SRD 1–40 GHz, including 24.05–24.25 GHz) or **EN 305 550** (40–246 GHz, for 60 GHz radar).
  - **EN 62368-1** (safety).
  - **EN 62311 / EN 62479** (RF exposure).
  - **EN 55032 / EN 55035** (multimedia EMC, applied under RED Art 3.1(b)).
- **RED cybersecurity, Delegated Regulation (EU) 2022/30:** **applies from 1 Aug 2025.** Standards **EN 18031-1** (internet-connected) and **-2** (personal data) are almost certainly in scope for an app-connected device with user data.
  - The OJEU citation carries **restrictions**: for example, where users may skip setting a password, there is no presumption of conformity.
  - The Commission has adopted **Delegated Regulation (EU) 2026/339**, published in the OJEU 29 Apr 2026, which **repeals 2022/30 effective 11 Dec 2027** as the **Cyber Resilience Act** takes over. https://single-market-economy.ec.europa.eu/sectors/electrical-and-electronic-engineering-industries-eei/radio-equipment-directive-red_en
- **Cyber Resilience Act (EU) 2024/2847:** entered into force 10 Dec 2024. Vulnerability and incident **reporting obligations apply from 11 Sep 2026** (now in force). Full obligations apply from **11 Dec 2027**: secure by design, SBOM, security updates for the support period, conformity assessment. A launch monitor with an app is a "product with digital elements" in the default category, so self-assessment is acceptable.
- **EU Battery Regulation (EU) 2023/1542:** in force 17 Aug 2023, applies from 18 Feb 2024 with phased dates.
  - **Producer registration and EPR in each Member State: 18 Aug 2025.**
  - **Labelling (Art 13): 18 Aug 2026.**
  - **QR code: 18 Feb 2027.**
  - **Art 11: portable batteries must be readily removable and replaceable by the end user from 18 Feb 2027.** Exemptions are narrow (e.g., devices designed to operate mainly in splashing or immersion environments; certain professional or medical continuity cases). → **Design a user-swappable battery pack now.**
  - Removability guidelines: Commission Notice C/2025/214 (8 Jan 2025). https://environment.ec.europa.eu/topics/waste-and-recycling/batteries_en
  - *Dates other than the general ones are from the regulation text as recalled. Confirm against Art 96 on EUR-Lex.*
- **RoHS 2011/65/EU + (EU) 2015/863** (10 restricted substances).
- **REACH:** SVHC Candidate List (more than 250 entries; check ECHA for the current count). Art 33 duty to communicate if more than 0.1% w/w in any article, plus a **SCIP** database notification.
- **WEEE 2012/19/EU:** registration in each Member State where we sell. An **authorised representative** is needed if we have no establishment there.
- **General Product Safety Regulation (EU) 2023/988** (applies 13 Dec 2024): an EU responsible economic operator, traceability, and a SafetyGate accident-reporting process.
- **Packaging and Packaging Waste Regulation (EU) 2025/40:** applies from **12 Aug 2026**. Packaging EPR registration in each country (e.g., LUCID in Germany).
- **EU Data Act (EU) 2023/2854** (applies 12 Sep 2025; Art 3 "access by design" for connected products placed on the market from **12 Sep 2026**). A shot-data-generating connected launch monitor must let users access and export their data. This fits the "no subscription" promise. **[Verify scope with counsel.]**
- **Radio spectrum:**
  - 24.05–24.25 GHz is an SRD band under ERC Rec 70-03 / Decision (EU) 2019/1345 (about 100 mW EIRP).
  - 57–64 GHz non-specific SRD (about 100 mW EIRP, with PSD limits). **[Verify current limits.]**
- **Notified Body:** not needed if harmonised standards are fully applied. The Technical File and EU Declaration of Conformity are produced in-house.

### 4.5 United Kingdom (UKCA / CE)
- **CE marking continues to be recognised in Great Britain** under the Product Safety and Metrology (Amendment) Regulations 2024. This covers the Radio Equipment Regulations 2017, Electrical Equipment (Safety) Regulations 2016, EMC Regulations 2016 and RoHS 2012. No end date is published (GOV.UK, updated 21 Aug 2026). https://www.gov.uk/guidance/using-the-ukca-marking → **ship CE, and add UKCA optionally.**
- **PSTI Act and regulations (in force 29 Apr 2024):** for connectable products: **no universal default passwords**, a published **vulnerability disclosure policy**, and a stated **minimum security-update period** at point of sale.
- UK WEEE and battery producer registration. A UK importer or authorised representative address on the product or packaging (packaging allowed until 31 Dec 2027 for EEA imports).

### 4.6 Australia / New Zealand (RCM)
- **ACMA:** EMC (AS/NZS CISPR 32) and radio (**AS/NZS 4268** SRD). Radar operates under the **Radiocommunications (Low Interference Potential Devices) Class Licence**; check the 24 GHz and 60 GHz entries.
- Responsible-supplier registration on the national database, and an RCM label.
- **EESS:** a USB-powered device is generally out of scope, but a bundled AC adapter is in scope.
- If any coin cell is shipped: **mandatory button-battery safety and information standards.**
- NZ accepts the Australian RCM framework (supplier declaration).
- Typical extra cost: **$2–6k** (mostly paperwork, reusing CE/FCC reports with AS/NZS deviations).

### 4.7 Japan
- **Radio Law, MIC "Giteki" certification (技適):** use a module with Japanese certification and label it.
  - **Radar:** 24.05–24.25 GHz "specified low-power radio for moving-object detection sensors". The 60 GHz band (57–66 GHz) is permitted for some sensing uses. **[Verify the ARIB standard and current MIC rules.]** Expect a separate Giteki certification through a Registered Certification Body.
- **VCCI** (voluntary EMC, expected by retailers).
- **PSE/DENAN:** a **standalone Li-ion battery** (for example, a spare swappable pack sold separately) is a "specified product" needing the round PSE mark. A **bundled AC adapter needs the diamond PSE mark** → ship USB-C only, no adapter.
- **Cost:** about **$5–15k** (radio, with radar about $10–20k); 4–8 weeks.

### 4.8 South Korea
- **KC (RRA, Radio Waves Act):** radio plus EMC conformity assessment. A Korean applicant or importer of record is needed. Module certification helps, but the host normally still needs KC EMC and radio registration.
- **KC safety for Li-ion batteries** (KC 62133). **[Verify whether a pack built into a host is exempt.]**
- **Cost:** about **$6–15k**; 6–10 weeks. Note that Golfzon, Creatz and Uneekor are home-market incumbents.

### 4.9 Others (brief)
- **China:** SRRC radio type approval (radar and Wi-Fi); CCC generally not required for this product category. **[Verify.]**
- **Taiwan:** NCC (low-power RF).
- **Singapore:** IMDA registration.
- **India:** WPC/ETA and BIS CRS for some electronics.

### 4.10 Photobiological safety of the IR strobe (IEC 62471 / EN 62471)
- **IEC 62368-1 clause 10.4** points to **IEC 62471** for LED radiation. Classify the system into **Exempt, RG1, RG2 or RG3**.
  - RG2 needs warning labels.
  - RG3 is generally unacceptable in a consumer product.
- **Hazards for 850/940 nm:**
  - **Retinal thermal, weak visual stimulus (IR-A, 780–1400 nm):** the eye has little aversion response to IR, so this limit is the binding one.
  - **Cornea/lens IR exposure:** exempt-group limit **E_IR ≤ 100 W/m²** (1000 s), with a time-dependent limit for short exposures.
- **Evaluate:**
  - at the **closest reasonably foreseeable eye distance**. A golfer at address may be 0.3–1.0 m from a side-of-ball unit, and users bend down to tee up. IEC 62471 commonly uses **200 mm** for non-general-lighting sources.
  - for both **single-pulse peak** and **time-averaged** exposure, at the worst-case strobe duty (e.g., continuous standby illumination for ball detection plus shot bursts).
- **Design levers:**
  - Diffusers to increase apparent source size, which lowers retinal radiance.
  - Duty-cycle limiting and a firmware interlock, for example strobes disabled when a proximity sensor sees a face within X cm, or only on trigger.
  - Prefer **940 nm** (lower retinal hazard weighting and less visible red glow) **if** camera quantum efficiency allows.
- **Test cost:** about **$3–8k** at an optical lab (e.g., UL, TÜV, Intertek, SGS, or specialist photometric labs). Do an engineering pre-measurement on the EVT build.
- Keep a separate **IEC 60825-1** track only if lasers or VCSELs are used.

### 4.11 Battery safety standards
- **UN 38.3:** per cell and per battery design. Use cells already tested; the pack still needs its own UN 38.3 (T.1–T.8). About **$6–15k**; 6–8 weeks (T.6/T.8 apply to cells only).
- **IEC 62133-2:2017 (+A1:2021):** cell and pack safety; CB scheme. About **$6–12k**; 4–8 weeks. Required by EU retailers, KC, and many importers.
- **UL 2054 / UL 62133** (US retail asks for these).
- **Pack design:** BMS with over-charge, over-discharge, over-current and over-temperature protection, plus an NTC. **IEC 62368-1 Annex M** requirements for battery-powered equipment.

### 4.12 Cost and timeline table (small startup; USD; 2026 estimates)

**These are estimates from typical lab pricing, not quotes.** I could not fetch published lab price lists in this session. Get 3 quotes from labs such as TÜV SÜD, UL Solutions, Intertek, SGS, Element, Bureau Veritas, Nemko, Eurofins E&E, MET Labs, Compliance Testing, or Rhein Tech.

| Market | Marks / approvals | Main tests | Camera-only (module radio) | + 24 GHz radar | Timeline |
|---|---|---|---|---|---|
| Pre-compliance (all) | — | Chamber rental for pre-scans at EVT and DVT, conducted and radiated emissions, ESD | $3–10k (about $1–2.5k per day, 2–4 days) | +$2–4k | Rolling |
| **US** | FCC SDoC (15B); FCC ID for radar (TCB) | 15B; KDB 996369 host check; 15.245/15.249 radio; RF exposure | **$5–12k** | **+$10–20k** (test plus TCB grant about $1.5–3k) | 3–6 wks (radar grant +2–4 wks) |
| **Canada** | ICES-003; ISED certification for radar | Same lab | **$2–5k** | +$3–6k | Parallel with the US |
| **Product safety (global base)** | IEC/EN/UL 62368-1 CB report and certificate | Safety, including Annex M and the 10.4 photobiological reference | **$10–25k** | — | 6–10 wks |
| **Photobiological** | IEC/EN 62471 report | Radiance/irradiance at the worst-case distance | **$3–8k** | — | 2–4 wks |
| **Battery** | UN 38.3; IEC 62133-2; (UL 2054) | Pack tests; cell reports from the supplier | **$12–30k** | — | 6–10 wks (long lead; start at DVT) |
| **EU** | CE (RED + RoHS); EN 18031 assessment; WEEE, battery, packaging registrations | EN 300 328, 301 489-1/-17/(-3), 62368-1 (from the CB report), 62311/62479, 55032/55035, 18031-1/-2 | **$12–30k** (+$5–15k for EN 18031 consultancy and pen-test) | **+$6–12k** (EN 300 440 / EN 305 550) | 6–10 wks |
| **UK** | CE accepted; PSTI statement | Paperwork | $0–2k | — | — |
| **AU/NZ** | RCM; supplier registration | Reuse of CE/FCC reports plus AS/NZS 4268 | $2–6k | +$1–3k | 2–4 wks |
| **Japan** | MIC Giteki (radar); VCCI; (PSE if spare packs or adapter) | — | $3–8k | +$6–12k | 4–8 wks |
| **Korea** | KC (RRA radio and EMC); KC battery | — | $6–15k | +$4–8k | 6–10 wks |
| **Compliance programme overhead** | EPR registrations (EU WEEE, battery, packaging × countries; UK; CA provinces), EU/UK representative, Prop 65 review | — | $5–20k per year | — | Ongoing |

**Rough totals:** US + CA + base safety/battery/62471 = **$35–80k** (camera-only), or **$50–110k** with radar. Adding EU/UK/AU/JP/KR brings the total to **$70–170k**. Typical critical path from DVT samples to US/EU marks is **10–16 weeks**. Start UN 38.3 and the 62368-1 CB report earliest.

**Recommendations to save money:**
1. Use a fully certified Wi-Fi/BLE module and keep its reference antenna.
2. Launch v1 with no radar.
3. Use 2.4 GHz only, or 5 GHz only if fully covered by the module.
4. Test once at a lab that can issue FCC, ISED and CB, with CE reports from the same data.
5. Pre-scan the strobe driver at EVT.
6. Design to IEC 62471 Exempt.
7. Use a user-replaceable ≤100 Wh pack built from cells that already have UN 38.3 and IEC 62133 reports.

---

## 5. Trademark / brand: "Outer Bounds"

**USPTO search** (queried the tmsearch.uspto.gov back end directly, 2026-10-07):

| Mark | Status | Reg./Serial | Classes / goods | Owner | Conflict risk for us |
|---|---|---|---|---|---|
| OUTER BOUNDS | **Dead** (cancelled §8) | RN 2,652,649 | 28: toys, games, action figures | McCafferty | None (dead), but it shows the mark was registrable in class 28. |
| OUTER BOUNDS | Dead | SN 74517451, SN 74489761 | 18/25: bags, apparel | Creative Enterprises | None |
| OUTER BOUNDS | Dead (cancelled) | RN 3,353,496 | 24: textile fabric | Tullahoma Industries | None |
| **OUTERBOUNDS** | **LIVE, registered 2023-03-07** | **RN 6,997,555** (SN 90687603) | **9** (downloadable software for data integration, analytics, **data visualization**, ML/MLOps, HPC), **35, 41, 42** (SaaS platforms for data processing and analytics) | **Step Computing, Inc.** (= Outerbounds, the Metaflow company; per outerbounds.com, "joining Anaconda") | **Moderate for class 9/42 software.** Identical sound and appearance. An examiner could cite it against "OUTER BOUNDS" for *downloadable software for analysing golf performance data* under §2(d). **Low for class 28 / class 9 hardware** (launch monitors) because the trade channels differ. A strong owner (Anaconda) may oppose. |
| OUTTA BOUNDS GOLF | LIVE | RN 7,986,926 | 41: golf driving range services | Van-Tas-Dyke Co. (MT) | **Low–moderate.** Golf-specific near-homophone. Matters if we offer class 41 services (instruction or events); less so for goods. |
| OUT OF BOUNDS | LIVE | RN 3,147,391 | 14/16/28 (toys, puzzles, party favours; not golf) | Westminster, Inc. | Low (different goods), but class 28 overlap is noted. |
| OUT OF BOUNDS | LIVE | RN 2,238,242 | 25: apparel | Grillo | Low for products; matters for merchandise. |
| OB GOLF CO | LIVE | RN 6,759,115 | 18/25: bags, apparel | OB Golf LLC (CA) | Matters only if we brand as "OB". |
| B OUTBOUNDS | LIVE | RN 8,447,091 | 35/42: software development | Outbounds Inc. | Low. |
| META BOUNDS / META-BOUNDS | Pending (some opposed) | various | 9/42: AR glasses | Meta-Bounds Inc. | Low. |
| No live "OUTER BOUNDS" or "OUTERBOUNDS" in class 28, and no "*BOUNDS" mark in classes 9/28 covering sporting goods. | | | | | |

**Other observations:**
- **"Out of bounds" is a golf rules term** (OB). "Outer Bounds" is **suggestive**, not descriptive, so it is registrable, but the mark will be relatively weak against "-bounds" variants. A compound or stylised mark plus a distinctive logo gives better protection.
- **Domain and SEO:** outerbounds.com belongs to Outerbounds/Anaconda (fetched). Search results will be dominated by the ML company. Plan on outerboundsgolf.com or similar **[availability not checked]**.
- **Not checked (do before filing):**
  - **EUIPO/TMview, UKIPO, CIPO, IP Australia, JPO, KIPO.** Outerbounds may have Madrid extensions.
  - Common-law and Amazon/App Store usage.
  - Launch-monitor brand names already in use, to avoid confusing similarity: TrackMan; Foresight GC3/GCQuad/QuadMAX/Falcon; Bushnell Launch Pro; FlightScope Mevo/Mevo+/X3; Rapsodo MLM2PRO; SkyTrak/SkyTrak+; Uneekor EYE XO/QED/EYE MINI; Square Golf; Garmin Approach R10/R50; Full Swing KIT; ProTee VX; Swing Caddie SC4; Voice Caddie; Ernest Sports ES16; Golfzon; Toptracer; OptiShot; PiTrac (open source).

**Costs and process (US):**
- **TEAS base application $350 per class** (fee rule effective 18 Jan 2025).
- **Surcharges** per class: insufficient information, free-form ID text instead of the ID Manual, and each extra 1,000 characters (about $100–200 each).
- Intent-to-use filings add a Statement of Use and possible extensions.
- About 12–18 months to registration if unopposed.
- **Madrid Protocol:** a WIPO base fee (653 CHF b/w) plus individual country fees.
- **Attorney clearance search:** about $1.5–5k (full search plus opinion).

**Recommendation:**
1. Commission a **full clearance search and opinion** for "OUTER BOUNDS" in classes **9, 28, 42 (and 41)**.
2. If you proceed, file **intent-to-use** applications now for the **class 9 hardware** (golf launch monitors) and **class 28** (golf training aids and simulators) to secure a priority date. Draft the class 9/42 software descriptions tightly ("for measuring golf ball and club launch parameters") to separate them from Outerbounds' MLOps/data-science identification.
3. Have backup names cleared in parallel, in case of a §2(d) refusal or an Anaconda opposition.

---

## 6. Open items and verification checklist

1. **Patents to pull and claim-chart** (Google Patents was rate-limited in this session):
   - Uneekor (all US/KR); SkyTrak/SkyHawke/Golf Labs; Garmin (R50); ProTee; Full Swing camera filings; Bushnell.
   - Foresight post-2018 filings and US 7,641,565.
   - Toptracer imaging (US 11,918,863; 12,285,656; 12,361,570; 11,995,846).
   - Sumitomo/Bridgestone/Yokohama spin imaging (likely expired prior art).
   - Claims text for TrackMan US 12,586,211, Rapsodo US 9,171,211 and US 12,530,796 (abstract-inferred above).
   - Status of Acushnet US 8,475,289 (12-year maintenance fee).
   - EP/JP/KR equivalents for every "H" patent.
2. **Litigation:**
   - Korean cases (Golfzon v. Kakao VX; Golfzon/Creatz/Uneekor), German/UPC cases, and PTAB IPRs on TrackMan, Foresight and Rapsodo patents.
   - Complaint text for SkyHawke v. GolfTec ST (PACER).
3. **FCC IDs of competitor radars** (FCC EAS was blocked here) to confirm rule parts and test plans.
4. **Regulatory specifics to confirm with the lab:**
   - RSS-210 annex for 24 GHz and 60 GHz sensors.
   - Japan MIC rules for 24 GHz and 60 GHz sensors.
   - KC battery exemption for built-in packs.
   - EU 57–64 GHz SRD limits.
   - California SB 1215 battery-embedded product obligations.
   - Current REACH SVHC count.
5. **FTO opinion from a patent attorney before tooling.** Engage now; the opinion depends on the frozen architecture.

---

### Key source URLs
- Google Patents pages (verified this session):
  - Expired foundational: https://patents.google.com/patent/US7324663B2/en ; https://patents.google.com/patent/US7292711B2/en ; https://patents.google.com/patent/US6241622B1/en ; https://patents.google.com/patent/US5471383A
  - Foresight club markers: https://patents.google.com/patent/US8951138B2/en
  - Acushnet: https://patents.google.com/patent/US7837572B2/en
  - Rapsodo: https://patents.google.com/patent/US9171211B2/en ; https://patents.google.com/patent/US12582870B2/en ; https://patents.google.com/patent/US12530796B2/en ; https://patents.google.com/patent/US10754025B2/en
  - TrackMan: https://patents.google.com/patent/US20240420346A1/en ; https://patents.google.com/patent/US11673029B2/en
  - EDH (FlightScope): https://patents.google.com/patent/US10775492B2/en
  - Golfzon: https://patents.google.com/patent/US12599828B2/en
  - Creatz: https://patents.google.com/patent/US9605960B2/en
  - Open Launch: https://patents.google.com/patent/US20240123314A1/en
- USPTO full-text PDFs (OCR'd), pattern `https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/<n>`: US 11,946,734; 11,191,998; 10,217,228; 10,639,537; 12,605,593; 9,737,757; 8,500,568; 8,622,845; 8,475,289; 7,395,696; 10,668,350; 11,747,461.
- TrackMan patent marking: https://www.trackman.com/legal/patents
- Radar patents (from the sub-study): https://patents.google.com/patent/US8845442B2/en ; https://patents.google.com/patent/US10850179B2/en ; https://patents.google.com/patent/US10989791B2/en ; https://patents.google.com/patent/US11828867B2/en ; https://patents.google.com/patent/US11619708B2/en ; https://patents.google.com/patent/US9958527B2/en ; https://patents.google.com/patent/US10953303B2/en ; https://patents.google.com/patent/US11439886B2/en ; https://patents.google.com/patent/US11612801B2/en ; https://patents.google.com/patent/US12586211B2/en ; https://patents.google.com/patent/US11311789B2/en ; https://patents.google.com/patent/US11940525B2/en ; https://patents.google.com/patent/US9868044B2/en ; https://patents.google.com/patent/US10151831B2/en
- Court dockets:
  - *WIPH v. TrackMan*: https://www.courtlistener.com/docket/68068135/
  - *WIPH v. Vista Outdoor*: https://www.courtlistener.com/docket/68512344/
  - *TrackMan v. GSP Golf*: https://www.courtlistener.com/docket/66755222/
  - *SkyHawke v. GolfTec ST*: https://www.courtlistener.com/docket/68092224/
- Regulations:
  - 47 CFR 15.245 / 15.249 / 15.255: https://www.law.cornell.edu/cfr/text/47/15.245 , /15.249 , /15.255
  - RED cybersecurity and repeal: https://single-market-economy.ec.europa.eu/sectors/electrical-and-electronic-engineering-industries-eei/radio-equipment-directive-red_en
  - UK CE recognition: https://www.gov.uk/guidance/using-the-ukca-marking
  - EU batteries: https://environment.ec.europa.eu/topics/waste-and-recycling/batteries_en
  - IATA 2026 lithium guidance: https://www.iata.org/contentassets/05e6d8742b0047259bf3a700bc9d42b9/lithium-battery-guidance-document.pdf
- Trademarks: USPTO Trademark Search (tmsearch.uspto.gov): SN 90687603 (OUTERBOUNDS), SN 98384735 (OUTTA BOUNDS GOLF), SN 76277718 (OUTER BOUNDS, dead). Company site: https://outerbounds.com/

*Not legal advice. Freedom-to-operate, validity, and trademark clearance opinions must come from qualified patent and trademark counsel in each jurisdiction.*
