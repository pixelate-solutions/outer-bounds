# 05 — Deep Technical Dive: Doppler Radar for a Markerless Golf Launch Monitor

*Prepared October 7, 2026. Scope: radar physics, competitor radar hardware, candidate chips, regulation, hybrid radar+camera architectures, and a verdict for an engineering spec. Target: a portable, markerless monitor that measures everything, works equally indoors (2.4–3.7 m of ball flight) and outdoors, retails for $1.5k–$3.5k, and has a BOM of roughly $250–$600.*

**How to read this.** Numbers with a link come from that source. Numbers marked **[calc]** are our own first-principles calculations; the formula is always shown. Statements marked **[assessment]** are engineering judgement, not sourced fact. **Research limits:** fccid.io and fcc.report blocked our fetcher (HTTP 403), so we could not open the internal photos or test reports directly. Competitor chip identities are therefore partly unverified and are flagged where so. Our web-search quota also ran out mid-task, so a few items rely on vendor pages and patents fetched directly.

---

## 0. Executive summary (TL;DR for the spec)

1. **Radar alone cannot deliver our full markerless metric suite indoors at our price.** Two parts of it need *long, clean* observation of the ball: (a) measured spin rate from Doppler sidebands, and (b) spin axis from trajectory curvature (lift direction). Indoors the ball is visible for only about 35–110 ms over 2.4–4 m, which at driver spin is just **1.4–2.4 revolutions [calc]**. TrackMan's own patent says that in an indoor setup "the modulation signal of an unmarked ball is often too weak to be useful for a spin rate measurement" ([WO2021005577A1](https://patents.google.com/patent/WO2021005577A1/en)). That is why the Mevo+ requires aluminium stickers or Titleist RCT balls indoors ([Mevo+ manual](https://hubspot.carlofet.com/hubfs/Product%20Documents/Launch%20Monitor/Mevo+/Mevo%20Plus%20User%20Manual.pdf)). It is also why TrackMan's indoor product, iO, takes spin and club data from a 4,600 fps camera and keeps its 24 GHz radar only "for optimal speed and distance measurement" ([TrackMan tech specs](https://www.trackman.com/golf/launch-monitors/tech-specs)).
2. **Face angle, dynamic loft and impact location are not really measured by consumer radar.** Radar sees the clubhead as a cluster of scatterers. It measures club speed well and, with a multi-receiver array, club path and attack angle reasonably well. Face angle and dynamic loft come mostly from inverting the D-plane from ball launch and spin data **[assessment]**. Impact location has migrated to optics at every vendor: TrackMan OERT/iO list impact height/offset as camera-era features, and FlightScope sells "Face Impact Location" as an add-on for the radar+camera Mevo Gen2 ([flightscope.com](https://flightscope.com/)).
3. **The correct role for radar in our product is a hybrid "trigger + speed + outdoor flight" subsystem next to a high-speed camera.** The camera handles spin, spin axis, club face, dynamic loft and impact location. Radar adds (i) a deterministic trigger and ball/club speed with no exposure-time ambiguity, (ii) an independent ball-speed check to cross-validate the camera, and (iii) outdoors, real measured flight over tens of metres, which grounds carry in data rather than a pure aerodynamic model. This is the direction the market leaders have taken: TrackMan OERT/iO, FlightScope Fusion Tracking (Mevo Gen2, $1,299), and the radar-plus-camera Rapsodo MLM2PRO ([rapsodo.com](https://rapsodo.com/products/mlm2pro)).
4. **Band choice.** A notable regulatory fact: since the 2023 FCC 60 GHz order, **mobile** field disturbance sensors may operate in **61.0–61.5 GHz at up to 40 dBm average EIRP** with no duty-cycle limit ([FCC 23-35 ¶22](https://docs.fcc.gov/public/attachments/FCC-23-35A1.pdf); [47 CFR 15.255(c)(2)(v)](https://www.law.cornell.edu/cfr/text/47/15.255)). They may also operate in 57.0–59.4 GHz at 20 dBm (indoor) or 30 dBm (outdoor) peak EIRP with no off-time requirement ([88 FR 47394](https://www.govinfo.gov/content/pkg/FR-2023-07-24/html/2023-15367.htm)). 60 GHz also gives 2.5× the Doppler sensitivity of 24 GHz and should give stronger spin micro-Doppler from an unmarked ball **[calc/assessment]**. However, the EU allows only 100 mW EIRP at 57–64 GHz and at 61–61.5 GHz ([ERC Rec 70-03, June 2026](https://docdb.cept.org/document/845)). **77 GHz is not available** for a handheld golf device in the US: Part 95 Subpart M allows only vehicles and airport air-operations areas ([DA 24-200](https://docs.fcc.gov/public/attachments/DA-24-200A1.pdf)). **24 GHz (15.245, 24.075–24.175 GHz)** is the proven worldwide workhorse (Mevo+, R10, TrackMan 4's short-range radar), but it allows only 100 MHz of bandwidth, so FMCW range resolution is 1.5 m and the band is effectively CW/FSK Doppler. **10.5 GHz** is what TrackMan uses for long-range flight tracking. It needs a large antenna (around 25–30 cm) to get the gain and angle accuracy, which is incompatible with a pocketable device.
5. **Recommended radar architecture for v1: "Architecture B" below.** It is a 24 GHz CW/FSK, 1-TX/3–4-RX Doppler front end (for example, Infineon BGT24MTR12/BGT24LTR22-class MMICs, or an RFbeam K-MC4/InnoSenT IPS-class I/Q module for prototyping; MMIC prices not yet verified) as a speed/trigger/outdoor-flight sensor, fused with a global-shutter high-speed camera. Estimated radar subsystem BOM is about **$25–$60** (chips, antenna PCB, ADC/MCU share). A 60 GHz variant using a single TI IWR6843AOP-class FMCW SoC (**"Architecture C"**, about $25–$45, or about $16 with an IWRL6432AOP) is a strong second option. Choose it if we want one chip with integrated DSP, range gating (to reject the screen and the golfer), and angle-of-arrival from an antenna-on-package array, accepting worse outdoor range. A "full radar" TrackMan-class design (**"Architecture A"**, 10.5 + 24 GHz, large arrays, custom RF) costs $150–$350 in radar BOM alone and still fails the markerless-indoor-spin requirement.

---

## 1. How golf radar works

### 1.1 Doppler fundamentals

The Doppler shift is f_D = 2·v_r/λ. Here v_r is the radial (line-of-sight) velocity and λ = c/f is the wavelength.

**[calc]**

| Band (centre) | λ | f_D @ 90 m/s ball | f_D @ 60 m/s club | f_D @ 5 m/s (putt/surface velocity) | ka for 42.67 mm ball |
|---|---|---|---|---|---|
| 10.525 GHz (X) | 28.5 mm | 6.3 kHz | 4.2 kHz | 0.35 kHz | 4.7 (resonance/optical) |
| 24.125 GHz (K) | 12.4 mm | 14.5 kHz | 9.7 kHz | 0.80 kHz | 10.8 (optical) |
| 61.25 GHz (V) | 4.9 mm | 36.8 kHz | 24.5 kHz | 2.0 kHz | 27 (optical) |
| 77 GHz (W) | 3.9 mm | 46.2 kHz | 30.8 kHz | 2.6 kHz | 34 (optical) |

- **Sample rates are trivial.** Even at 77 GHz the ball Doppler is below 50 kHz. A CW Doppler radar needs only a 100–200 kS/s I/Q ADC, so audio-class or MCU ADCs are sufficient.
- **The ball's radar cross-section (RCS) is roughly band-independent.** In the optical region, RCS ≈ πa² ≈ 1.43×10⁻³ m² (−28.5 dBsm) **[calc]**. For a fixed transmit EIRP and a fixed receive aperture area, received power is P_r = EIRP·σ·A_e/((4π)²R⁴), which does not depend on λ. What changes with band is (a) how much EIRP regulators allow, (b) how much antenna aperture fits in the box, and (c) Doppler/phase sensitivity, which scales with 1/λ.

**Thermal-noise-limited SNR [calc].** Assumptions: golf ball σ = 1.43e-3 m², 20 ms coherent integration, NF = 12 dB. No clutter, phase noise, atmospheric or implementation loss is included. Real systems lose a further 15–25 dB.

| Configuration | 3 m | 10 m | 30 m | 100 m | 200 m |
|---|---|---|---|---|---|
| 10.5 GHz, 25 cm panel RX, 27 dBm EIRP (TrackMan-like) | 88 dB | 67 | 48 | 27 | 15 |
| 24 GHz, 6 cm patch RX, 24 dBm EIRP (Mevo+-like) | 73 | 52 | 33 | 12 | 0 |
| 24 GHz, 12 cm array RX, 27 dBm | 82 | 61 | 42 | 21 | 9 |
| 60 GHz, ~1.2 cm antenna-on-package (AoP) RX, 20 dBm | 54 | 33 | 14 | −7 | −19 |
| 60 GHz, 4 cm array RX, 27 dBm | 72 | 51 | 32 | 11 | −1 |

After 15–25 dB of real-world loss, this matches field behaviour. A 10.5 GHz panel with roughly 25 cm aperture follows the full flight; this is TrackMan's long-range radar ([FCC SFX-TMB4A](https://fccid.io/SFX-TMB4A); forum reading of the internal photos in [GSF](https://golfsimulatorforum.com/forum/off-topic/all-off-topic/273222-new-higher-frequency-radar-sensors)). Small 24 GHz consumer units track only the first roughly 30 yd, so the R10 "calculates distance and flight direction instead of measuring them directly" ([GSF R10 thread](https://golfsimulatorforum.com/forum/golf-simulator-brands-and-types/garmin/336862-new-garmin-approach-r10-launch-monitor-simulator/page2)). A 60 GHz AoP chip at 10 dBm is a short-range (under about 15 m) ball sensor unless we add a lens or array; 60 GHz also suffers roughly 15 dB/km of O₂ absorption.

### 1.2 Modulation options

| Scheme | What it gives | Golf relevance |
|---|---|---|
| **CW Doppler** (single tone, I/Q) | Radial velocity only, with very fine resolution over a long dwell. No range. | The core of every golf radar (original Mevo: "CW carrier modulation, Doppler velocity measurement," [FCC QXP-A7310](https://fccid.io/QXP-A7310)). It fits easily inside the 50–100 MHz-wide 15.245 bands. |
| **FSK / multi-frequency CW** (2–3 tones alternated) | Range from the phase difference between tones (R = c·Δφ/(4πΔf)), with no range resolution between targets in the same Doppler bin. | Cheap range to the ball (for the 3D position and trajectory fit) within 15.245's 100 MHz. Moving ball and moving club are already separated in Doppler, so FSK range per Doppler bin works well. Likely what 24 GHz golf units do, though this is unverified for any specific competitor. |
| **FMCW** (chirps) | Range resolution ΔR = c/(2B); velocity from chirp-to-chirp phase; angle from MIMO. | ΔR is 1.5 m at 100 MHz (24 GHz, 15.245), 0.6 m at 250 MHz (24 GHz, 15.249, low power), 30 cm at 500 MHz (61.0–61.5 GHz), 6.3 cm at 2.4 GHz (57–59.4 GHz) and 2.1 cm at 7 GHz (57–64 GHz) **[calc]**. Only 60 GHz gives centimetre-class range gating, which helps separate ball, club, golfer, mat and screen. The cost is the **velocity ambiguity problem** (§3.1). |
| **Pulsed / UWB** | Range-gated. | Not used in golf. Under 15.255(c)(3) a pulse-radar mode exists at 60 GHz. |

### 1.3 Angles: multi-receiver phase comparison (interferometry)

- **Method.** One TX and N RX antennas. For a target at angle θ, the RX phase difference over a baseline d is Δφ = 2π·d·sinθ/λ. TrackMan's spin-axis family specifies "one transmitter and at least three receivers, with at least three of them not in a line." Two baselines give azimuth and elevation, so the radar measures 3D position over time ([WO2021005577A1](https://patents.google.com/patent/WO2021005577A1/en)). FlightScope's EDH patent likewise says "typically 3 or more" receivers ([US20140191896A1](https://patents.google.com/patent/US20140191896A1/en)). Consumer devices follow this: the **Mevo+ has 4 RX antennas** per a reading of its FCC internal photos ([GSF teardown thread](https://golfsimulatorforum.com/forum/flightscope/277362-mevo-teardown)), and **Garmin R10 uses a "three-receiver radar"** (Garmin support, quoted in the [GSF R10 thread](https://golfsimulatorforum.com/forum/golf-simulator-brands-and-types/garmin/336862-new-garmin-approach-r10-launch-monitor-simulator/page2)).
- **Accuracy [calc].** σ_θ ≈ λ/(2π·d·cosθ·√(2·SNR)). With d = 4λ and a per-dwell SNR of 30 dB, σ_θ ≈ 0.05° per measurement. A long baseline is ambiguous, because phase wraps every λ/d radians. The standard fix is a short baseline (about λ/2) to unwrap plus a long baseline for precision, i.e. a sparse 3–4 element array.
- **Launch angle is fitted, not read off one sample.** The radar gets angle and range-rate samples along the first metres of flight and fits a trajectory. Launch angle and direction are that trajectory's tangent at the tee.
- **Error sources indoors and outdoors [assessment]:**
  - Ground/mat multipath creates an image target below the ball, which biases elevation for low launches. This is why radars are tilted up and positioned 2–3 m behind the ball.
  - The golfer's body and arms produce strong, slowly varying clutter.
  - Indoors, the screen/net returns a strong echo, and the ball rebounding off the screen produces a negative-Doppler track.
- **Required geometry.** Down-the-line behind the ball is the dominant setup. The ball moves almost radially away, so radial velocity ≈ ball speed and the launch angle is small and close to boresight, where interferometry is most accurate. A side-of-ball radar sees ball speed mostly *tangentially*, so the Doppler is small and changing. That geometry is poor for radar and is why side-of-ball units (GCQuad, Bushnell Launch Pro, Garmin R50) are camera-based **[assessment]**.

### 1.4 How spin is measured with radar

**(a) Unmarked-ball Doppler sidebands (TrackMan).** The patent family is [US 8,845,442 B2](https://patents.google.com/patent/US8845442B2/en) and [US 9,645,235 B2](https://patents.google.com/patent/US9645235B2/en), by Fredrik Tuxen for TrackMan, priority 2005-03-03.
- **Mechanism.** Surface irregularities on the spinning ball phase- and amplitude-modulate the return. The result is sidebands around the ball-velocity Doppler line that "will have multiple harmonics and will be spaced exactly the spin frequency of the ball ω/2π."
- **Processing.** Track the velocity line, then find symmetric peaks around it, track the harmonics, require equal spacing, assign harmonic numbers, and divide the frequency offset by the harmonic number.
- **Blind spot.** There are no sidebands when the spin axis is along the radar line of sight (α = 90°).
- **Sideband strength.** The power of the m'th harmonic follows Jₘ(4πr/λ), a first-kind Bessel function. Here r is the effective radial size of the surface irregularity ([US8845442B2](https://patents.google.com/patent/US8845442B2/en)).
- **Patent status.** Google lists the adjusted expiry as **2029-05-18 for '442** and **2026-07-17 for '235**. The '235 continuation is therefore now expired, but '442 is still in force. Assume freedom-to-operate review is required. This is not legal advice.

**Band implication of the Bessel law [calc/assessment].** For a small irregularity with effective radial excursion r = 0.25 mm (the order of dimple depth or cover non-uniformity), the modulation index 4πr/λ is:

| Band | Modulation index | First-sideband power J₁² | Relative to 24 GHz |
|---|---|---|---|
| 10.5 GHz | 0.11 rad | about −25 dBc | about 7 dB weaker |
| 24 GHz | 0.25 rad | about −18 dBc | reference |
| 61 GHz | 0.64 rad | about −10 dBc | about 8 dB stronger |

Higher frequency therefore makes the *unmarked* spin signature intrinsically stronger. This is a real argument for 60 GHz if we ever want radar-measured markerless spin. There is a caveat: the dimple pattern is roughly periodic around the ball, so much of its modulation lands at high dimple-passing harmonics. The useful once-per-revolution component comes from asymmetries such as the seam, logo, paint and core eccentricity. So the absolute numbers above are illustrative, not predictive.

**(b) Seam/lens effect (FlightScope/EDH).** Source: [US20140191896A1](https://patents.google.com/patent/US20140191896A1/en), by H. Johnson et al., priority 2013.
- **Lens.** The ball's core refracts microwaves (ε_r ≈ 2.7–4.5, n ≈ 1.8), so features on the *far* side are magnified.
- **Seam.** The moulding seam modulates the Doppler signal at **twice** the spin rate. Example: a 3,300 rpm ball showed a peak near 110 Hz.
- **Embodiment.** About 10.525 GHz, about 10 mW, ≥3 receivers, analysis band 1,000–15,000 rpm. The modulation lasts only "10–25% of the overall spin period," i.e. it is pulse-like.
- **Fallback.** "Small pieces of conductive material glued to the ball surface … a small metal foil disk" are the fallback when the natural modulation is too weak.

**(c) Marked balls: metallic dots, RCT, silver ink.** TrackMan's later application [WO2021005577A1](https://patents.google.com/patent/WO2021005577A1/en) (priority 2019) explains the indoor problem in plain language:
- Unmarked modulation is "relatively weak."
- "In situations where data is available only for a very short ball flight, such as in an indoor golf setup … the modulation signal of an unmarked ball is often too weak to be useful."
- Simulator shots may travel only about 3–4 m before hitting a screen.

Its solution is conductive markers (aluminium, copper or silver ink) placed so every great circle passes near a marker. With that layout the spin plane always crosses a marker, whatever the axis. Markers are 0.25–0.5 λ in size and are deliberately unevenly spaced, to avoid an N× spin-rate alias. This is the technology behind **Titleist RCT ("Radar Capture Technology") balls** and the **Mevo+ aluminium stickers**: the manual says "Aluminum stickers required" for limited flight and "Aluminum stickers not required if using Titleist RCT golf balls" ([Mevo+ manual](https://hubspot.carlofet.com/hubfs/Product%20Documents/Launch%20Monitor/Mevo+/Mevo%20Plus%20User%20Manual.pdf)). Even the 2026 fusion-tracking Mevo Gen2 "recommends Titleist Pro V1 RCT balls or its metallic stickers" for best indoor spin ([flightscope.com](https://flightscope.com/)).

**(d) Spin axis.** Two radar routes exist:
1. **Trajectory/lift method** ([US9645235B2](https://patents.google.com/patent/US9645235B2/en)). Model the 3D acceleration as A = G + D + L (gravity, drag, lift). Lift L ⟂ spin axis, so solve L·ω̂ = 0 over many samples. "The axis is determined solely from the trajectory of the flying ball." This needs enough flight to measure the curvature, which means **outdoors**.
2. **Multi-receiver modulation geometry** (TrackMan, [US 2019/0282881](https://patents.google.com/patent/US20190282881A1/en), referenced in WO2021005577; we could not fetch it, HTTP 503). This uses the marker modulation seen across ≥3 non-collinear receivers. In practice it relies on markers indoors.

**(e) Garmin R10: calculated spin.** A small 24 GHz, 3-RX radar can measure ball speed, launch and club speed/path near the ball, but cannot track long enough to see lift. Forum consensus, consistent with Garmin's description, is that R10 *estimates* spin and computes carry and direction ([GSF R10 thread](https://golfsimulatorforum.com/forum/golf-simulator-brands-and-types/garmin/336862-new-garmin-approach-r10-launch-monitor-simulator/page2)). The R10 manual requires the tee to be at least **8 ft (2.4 m) from the net** and the unit **6–8 ft (1.8–2.4 m) behind the tee**. It lists the radar as **24 GHz @ 20 dBm max** (Garmin R10 Owner's Manual, [PDF](https://www8.garmin.com/manuals/webhelp/GUID-E2BBF6BE-4276-436F-B697-59ABEFD61933/EN-US/Approach_R10_OM_EN-US.pdf)).

**(f) Why TrackMan can measure unmarked spin outdoors.** Outdoors the ball is tracked for seconds by a high-gain 10.5 GHz long-range radar, giving hundreds to thousands of revolutions. The sideband harmonics become clean, narrow spectral lines. Frequency resolution 1/T is 1 Hz or better against spin frequencies of 30–170 Hz, and the trajectory method can also solve for the axis. **[calc]**

### 1.5 How much flight do you need? (the indoor problem, quantified) **[calc]**

Ball visible for distance d after impact. The flight time is t = d/v, the number of revolutions is n = (rpm/60)·t, and the native spectral resolution is 1/t.

| Shot (speed, spin) | 2.4 m (8 ft) | 3.0 m (10 ft) | 3.7 m (12 ft) |
|---|---|---|---|
| Driver (72 m/s, 2,600 rpm = 43 Hz) | 33 ms, **1.4 rev**, 1/t = 30 Hz | 42 ms, 1.8 rev, 24 Hz | 51 ms, 2.2 rev, 19 Hz |
| 6-iron (60 m/s, 4,500 rpm = 75 Hz) | 40 ms, 3.0 rev, 25 Hz | 50 ms, 3.8 rev | 62 ms, 4.6 rev |
| PW (48 m/s, 6,500 rpm = 108 Hz) | 50 ms, 5.4 rev | 63 ms, 6.8 rev | 77 ms, 8.4 rev |
| Wedge pitch (35 m/s, 9,000 rpm = 150 Hz) | 69 ms, 10 rev | 86 ms, 13 rev | 106 ms, 16 rev |

For driver indoors the native frequency resolution (19–30 Hz) is *comparable to the spin frequency itself* (43 Hz). Two to three sideband harmonics cannot be cleanly separated by an FFT, so you are fitting a model to 1–2 revolutions of a weak modulation.

- **Markers fix this.** A marker produces a sharp pulse once per revolution (or twice, for the seam). With pulse timing, two pulses give the period directly, so the spectral-resolution argument no longer applies.
- **Unmarked indoors**, the honest expectation is that wedges and irons can be done but driver spin is unreliable **[assessment]**. That matches the vendors' behaviour.
- **Usable flight is shorter than room length.** The radar sits 2–2.7 m behind the ball, and the ball is only cleanly visible about 0.3–0.5 m after impact, once the clubhead echo separates from it.
- **Launch angle needs less.** Angle and speed can be had from about 1–2 m of flight (around 15–40 ms) with ≥3 RX, which is why every 24 GHz consumer unit manages launch angle indoors.
- **Vendor minimums:**
  - Mevo+: 8 ft sensor-to-tee, with a 13 ft (4 m) minimum in the limited-flight setup diagram ([Mevo+ manual](https://hubspot.carlofet.com/hubfs/Product%20Documents/Launch%20Monitor/Mevo+/Mevo%20Plus%20User%20Manual.pdf)).
  - Mevo Gen2: "about 16 ft total, 8 ft ball-to-net and 8 ft behind" ([flightscope.com](https://flightscope.com/)).
  - TrackMan 4: unit at least 4.7 m (16 ft) from the net ([TrackMan](https://www.trackman.com/golf/launch-monitors/tech-specs)).
  - R10: 8 ft tee-to-net.
  - Rapsodo MLM2PRO (camera + radar): about 8 ft ball-to-net plus 6.5–8.5 ft device-to-ball ([Rapsodo](https://rapsodo.com/products/mlm2pro)).
- **Our 8–12 ft-to-screen use case is at the very bottom of what radar-based spin tolerates**, even *with* markers.

### 1.6 Club data from radar

- **Club speed.** The clubhead is the fastest target before impact, at 25–60 m/s. Its Doppler track, the peak or centroid just before the ball appears, gives club speed. This is robust and cheap; every radar unit reports it. Clubhead and ball separate cleanly because, at impact, ball speed is about 1.3–1.5× club speed (smash factor).
- **Club path and attack angle.** With ≥3 RX, the clubhead's 3D position can be tracked for the last few tens of centimetres before impact. The horizontal angle of its velocity vector is club path; the vertical angle is attack angle. TrackMan describes its short-range 24 GHz radar as "focused on putting, club and impact data" ([TrackMan tech specs](https://www.trackman.com/golf/launch-monitors/tech-specs)). Accuracy is limited because the clubhead is an extended, rotating target: hosel, toe, face and shaft give multiple scattering centres that wander during the swing, and the shaft/hands also produce Doppler. **[assessment]**
- **Face angle, dynamic loft and spin loft [assessment].** Radar cannot directly image the face orientation. Instead the physics of impact (the D-plane) is inverted:
  - Ball launch direction ≈ 75–85% face angle + 15–25% club path for irons, varying with club and impact.
  - Spin axis tilt ∝ face-to-path.
  - Launch angle ≈ f(dynamic loft, attack angle).
  - Spin rate ≈ f(spin loft = dynamic loft − attack angle, club speed, friction).

  Given measured ball launch, spin, spin axis, club path and attack angle, you can *solve* for face angle and dynamic loft. This is credible only if ball spin and axis are themselves measured well. If spin is estimated, as on the R10, the "face angle" is a model output twice removed from measurement.
- **Impact location.** Impact location produces gear-effect spin-axis tilt and a smash-factor drop, so it can be weakly inferred. No vendor credibly claims radar-only impact location. TrackMan exposes impact height/offset as part of OERT and in the camera-based iO, and FlightScope sells Face Impact Location as an add-on for its radar+camera product ([TrackMan](https://www.trackman.com/golf/launch-monitors/tech-specs); [flightscope.com](https://flightscope.com/)).
- **Market evidence.** TrackMan iO's 4,600 fps camera provides "directly measured 3D spin" and the full club-data list, while its radar is "24 GHz ultra-low-power … for optimal speed and distance measurement" ([TrackMan](https://www.trackman.com/golf/launch-monitors/tech-specs)). The radar pioneer's newest product moved spin and face measurement to optics. That is the strongest available signal on what radar cannot do at short range.

### 1.7 Indoor limitations, summarised

1. **Too few samples or revolutions** for spin (above).
2. **Multipath.**
   - The floor/mat image biases launch angle.
   - The ceiling and walls produce ghost targets at longer range but the same Doppler.
   - The screen/net returns the ball's echo, and the ball rebounds toward the radar (negative Doppler). Ball-strike vibration of the impact screen is also visible at low Doppler.

   Mitigations: range gating (FMCW at 60 GHz, or FSK range), angle gating, and Doppler-sign gating.
3. **Golfer clutter.** The torso, arms and club shaft are all strong, moving reflectors 2–3 m from a down-the-line radar.
4. **Mutual interference.** In bays with several monitors on the same 24 GHz channel, a CW unit sees the other units' carriers as Doppler-shifted tones, depending on crystal offsets. Frequency-agile or FMCW designs help.
5. **No long flight to measure lift**, so spin axis and carry in a simulator are model-derived for all radar units.

---

## 2. What competitors actually use

| Product | Radar band(s) / rule | Architecture (as known) | Spin method | Sources |
|---|---|---|---|---|
| **TrackMan 4** (TMB4A) | **10.500–10.550 GHz** and **24.075–24.175 GHz**, both 15.245; plus 2.4/5 GHz Wi-Fi | Dual radar: a long-range 10.5 GHz flight-tracking radar (TX/RX at the panel corners) and a short-range "ultra-high-resolution" 24 GHz radar for club, impact and putting (centre), plus synchronized high-speed optics (OERT) | Unmarked Doppler sidebands plus trajectory (outdoor); OERT optics assist | [fccid.io SFX-TMB4A](https://fccid.io/SFX-TMB4A); [TrackMan specs](https://www.trackman.com/golf/launch-monitors/tech-specs); [GSF internal-photo reading](https://golfsimulatorforum.com/forum/off-topic/all-off-topic/273222-new-higher-frequency-radar-sensors) |
| **TrackMan III/IIIe** | 10.5–10.55 GHz, 130 mW, 15.245 | Single X-band radar | Sidebands plus trajectory | [fccid.io SFX-TMANIII](https://fccid.io/SFX-TMANIII) |
| **TrackMan iO** (indoor) | 24 GHz "ultra-low-power" radar only | 4,600 fps camera with IR illumination (810–850 nm); radar used for speed and distance | Camera ("directly measured 3D spin") | [TrackMan specs](https://www.trackman.com/golf/launch-monitors/tech-specs) |
| **FlightScope Mevo (original)** | 24.075–24.175 GHz, 15.245; 14 dBm EIRP, 20 dBi antenna, CW | Single CW Doppler | Estimated | [fccid.io QXP-A7310](https://fccid.io/QXP-A7310) |
| **FlightScope Mevo+** (LJ361) | **24.080–24.160 GHz**, 15.245 (granted 2019-12-13); **24 dBm ±3 EIRP (US), 17 dBm (EU)**. The Japanese variant uses **10.5–10.55 GHz, indoor-only** (per the Japanese caution in the manual) | 1 TX + **4 RX** phase-comparison array; chip identity not verified (the operational description and schematics are confidential) | Sidebands (outdoor); **aluminium stickers or RCT balls required indoors** | [fcc.report QXP-LJ361](https://fcc.report/FCC-ID/QXP-LJ361); [internal photos](https://fccid.io/QXP-LJ361/Internal-Photos/Internal-Photos-4549449); [Mevo+ manual](https://hubspot.carlofet.com/hubfs/Product%20Documents/Launch%20Monitor/Mevo+/Mevo%20Plus%20User%20Manual.pdf); [GSF teardown](https://golfsimulatorforum.com/forum/flightscope/277362-mevo-teardown) |
| **FlightScope Mevo Gen2** (2025/26, $1,299) | Radar band not stated on the site (presumably 24 GHz, unverified) | "Patented Fusion Tracking" (radar + camera); Face Impact Location is an add-on | Fusion; RCT balls or stickers recommended for best indoor spin | [flightscope.com](https://flightscope.com/) |
| **Garmin Approach R10** (IPH-03985) | **24 GHz @ 20 dBm max** | **3-receiver** radar | **Calculated/estimated** spin; carry and direction computed | [R10 manual](https://www8.garmin.com/manuals/webhelp/GUID-E2BBF6BE-4276-436F-B697-59ABEFD61933/EN-US/Approach_R10_OM_EN-US.pdf); [GSF](https://golfsimulatorforum.com/forum/golf-simulator-brands-and-types/garmin/336862-new-garmin-approach-r10-launch-monitor-simulator/page2) |
| **Garmin (unannounced model A04986)** | FCC documentation from early 2026 mentions **60 GHz radar**; product type unknown (golf, Varia or other) | — | — | [Notebookcheck](https://www.notebookcheck.net/New-Garmin-device-reveals-itself-with-60-GHz-radar-capabilities.1217864.0.html) |
| **Garmin Approach R50** | Camera-based side-of-ball unit (stereo high-speed cameras); radar not the primary sensor | — | Camera | Not re-verified this session; see the companion competitor report |
| **Rapsodo MLM2PRO** ($549–$699 plus subscription) | Doppler radar (frequency not published) | Dual cameras (Impact Vision at 240 fps reads the RPT ball pattern) + radar | **Camera, and only with RPT-printed balls** | [rapsodo.com](https://rapsodo.com/products/mlm2pro) |

**Why these bands [assessment, grounded in §4]:**
- **10.5 GHz.** It is the highest-EIRP narrowband FDS allocation available in most countries (15.245: 2.5 V/m @ 3 m ≈ 32.7 dBm EIRP **[calc]**). Large, cheap-to-fabricate antennas at λ = 28.5 mm give high gain and long baselines. It suits outdoor full-flight tracking, but the box gets big (TrackMan 4 is 300 × 300 mm).
- **24 GHz.** Same 15.245 power, a worldwide SRD allocation (24.05–24.25 GHz), and 2.3× the Doppler sensitivity of X-band. A 4-RX array fits in a phone-sized box (Mevo+ is 174 × 118 mm). This is the consumer standard.
- **60 GHz.** Newly practical after the 2023 FCC order, which also opened 61.0–61.5 GHz to mobile devices at high power. Abundant cheap CMOS SoCs exist. Garmin's 2026 filing hints at someone trying it.
- **77 GHz.** Barred for this use in the US (§4).

**Chip identity (unverified).** We could not open the FCC internal photos (fccid.io returns 403 to our fetcher). Mevo+, R10 and TrackMan short-range radar chip identities should be confirmed by a human downloading the internal-photo PDFs linked above, or by buying units for teardown (Mevo+ is about $1,099 on sale, R10 about $600). Common industry belief is that 24 GHz consumer units use Infineon BGT24-family MMICs; treat this as hypothesis only.

---

## 3. Candidate radar chips and modules

Sources: TI, Infineon and Acconeer datasheets, plus Digi-Key, Mouser and Octopart, checked October 2026. A dedicated research pass collected these figures. **Every price not explicitly linked is marked NV (not verified).** TI and Infineon product pages did not render prices for our fetcher, and the search quota ran out before all parts were covered.

### 3.1 The velocity-ambiguity constraint (the key FMCW filter)

**FMCW.** With complex I/Q IF, the maximum unambiguous radial velocity is v_max = λ/(4·T_c), where T_c is the repetition period between chirps from the *same* TX. TDM-MIMO with N_TX transmitters multiplies the effective T_c by N_TX.

**CW Doppler** has no such limit beyond the IF/ADC bandwidth. The table below gives the T_c each band needs **[calc]**:

| Band | λ | T_c for 90 m/s ball | T_c for 60 m/s club | CW Doppler at 90 / 60 m/s |
|---|---|---|---|---|
| 60.5 GHz | 4.96 mm | ≤13.8 µs | ≤20.6 µs | 36.3 / 24.2 kHz |
| 77 GHz | 3.89 mm | ≤10.8 µs | ≤16.2 µs | 46 / 31 kHz |
| 24.125 GHz | 12.4 mm | ≤34.5 µs | ≤51.8 µs | 14.5 / 9.7 kHz |
| 10.525 GHz | 28.5 mm | n/a (CW) | n/a | 6.3 / 4.2 kHz |

- **TI idle time.** TI's minimum is 2 µs for sweeps under 1 GHz, rising to 3.5, 5 and 7 µs for sweeps up to 2 GHz, up to 3 GHz and above 3 GHz ([TI SWRA553A](https://www.ti.com/lit/an/swra553a/swra553a.pdf)). TI also notes that unambiguous velocity can be extended in higher-level algorithms.
- **Worked example: IWR6843 [calc].** 2 µs idle + about 2 µs ADC start + 64 complex samples at 12.5 Msps (5.1 µs) + 0.5 µs gives T_c ≈ 9.6 µs, so **v_max ≈ 129 m/s at 60 GHz with a single TX**.
- **Practical rule.** For the speed frames use **one TX per burst** (or simultaneous BPM-MIMO transmit). Get angle from 1-TX × 3–4-RX interferometry, or alternate velocity frames with MIMO frames. With 3-TX TDM at 60 GHz the required 4.6 µs per chirp is not feasible.

**Resolutions [calc]:**
- **Velocity resolution:** Δv = λ/(2·T_obs).
  - 24 GHz: 20 ms dwell gives 0.31 m/s per bin; 5 ms gives 1.24 m/s.
  - 60 GHz: 20 ms gives 0.12 m/s; 5 ms gives 0.5 m/s.
  - Peak interpolation at high SNR gets 5–20× finer.
- **Angular resolution:** about 2/N_virt rad at boresight for λ/2 spacing.
  - 3T4R (12 virtual elements): about 9.5°.
  - 1T4R: about 29°.
  - 1T3R L-shape: about 60° per axis.
- **Angular *accuracy* differs from resolution.** A single dominant scatterer (the ball) is located to a small fraction of the beamwidth: σ ≈ 0.05–0.3° at 30 dB SNR with a few-λ baseline. Golf needs accuracy, not resolution.

### 3.2 Candidate parts

| Part | Band | TX/RX | Max slope / BW | IF BW / ADC | CW mode | On-chip compute | Package | Power | Price (source, Oct 2026) | 90 m/s ball / 60 m/s club in FMCW? |
|---|---|---|---|---|---|---|---|---|---|---|
| **TI IWR6843** | 60–64 GHz | 3/4 | 250 MHz/µs; 4 GHz | 10 MHz IF; 25 Msps real / complex 2×, 12.5 Msps complex 1× | Yes, mmWaveLink continuous mode ([rl_sensor.h](https://github.com/azinke/mmwave/blob/695a1f0d50852c403a5a7added9614d73b334cc4/ti/mmwavelink/include/rl_sensor.h)) | C674x DSP 600 MHz + R4F 200 MHz + HWA | 10.4 mm FCCSP | about 1.2–1.75 W average (TI example configs) | TI 1ku **about $21.43** (from a search snippet of the [TI part page](https://www.ti.com/product/IWR6843/part-details/IWR6843ABGABLR), not seen on the page itself); Octopart about $27 @1k | **Yes** with 1 TX (T_c ≈ 9.6 µs → about 129 m/s) |
| | Sources: [datasheet SWRS219F](https://www.ti.com/lit/ds/symlink/iwr6843.pdf), [product page](https://www.ti.com/product/IWR6843) | | | | | | | | | |
| **TI IWR6843AOP** | 60–64 GHz | 3/4, antenna in package | Same die; 4 GHz | 25 Msps | Same | Same | 15 mm AoP | NV | **NV** (expect a few $ above IWR6843) | Same as IWR6843 |
| | Source: [product page](https://www.ti.com/product/IWR6843AOP) | | | | | | | | | |
| **TI IWRL6432** | 57–63.9 GHz | 2/3 | 400 MHz/µs; 7 GHz | 5 MHz, **real-only** IF; 12.5 Msps | Likely (NV) | M4F 160 MHz + HWA 1.2, no DSP | 6.45 mm FCCSP | 960 mW active (2T3R) | Mouser (via search snippet): **about $15.53 @1k** (reel); **AOP about $15.96 @1k**; about $23.95 @1; 18-week lead time. NV directly. | **Probably** (T_c about 10–12 µs, est.). Real-only IF folds ± velocities; needs care. |
| | Sources: [datasheet SWRS298B](https://www.ti.com/lit/ds/symlink/iwrl6432.pdf), [Mouser](https://www.mouser.com/c/semiconductors/wireless-rf-integrated-circuits/rf-system-on-a-chip-soc/?m=Texas+Instruments&series=IWRL6432) | | | | | | | | | |
| **TI IWRL6844** | 57–63.9 GHz | 4/4 | Slope NV; 7 GHz | 10 MHz real; 25 Msps | NV | R5F 200 MHz + C66x 450 MHz + HWA | 9.1 mm FCCSP (not AoP) | NV | NV | Probably |
| | Source: [product page](https://www.ti.com/product/IWRL6844) (new; datasheet Rev A, Dec 2025) | | | | | | | | | |
| **TI AWR1843 / AOP** | 76–81 GHz | 3/4 | 4 GHz | 25 Msps | Continuous-mode API covers 77 GHz devices | C674x + R4F + HWA | 10.4 mm / 15 mm AoP | NV | NV | Probably, 1 TX. **Not US-certifiable for our use (Part 95M).** |
| | Sources: [AWR1843](https://www.ti.com/product/AWR1843), [AWR1843AOP](https://www.ti.com/product/AWR1843AOP) | | | | | | | | | |
| **TI AWR2944** | 76–81 GHz | 4/4 | 250 MHz/µs; >4 GHz | 15 MHz IF; 37.5 Msps | As above | R5F 300 MHz + C66x 360 MHz + HWA 2.1 | 12 mm FCCSP | 1.37–1.98 W | NV | Yes (about 7.7 µs est. → about 126 m/s with 1 TX). **Excluded by regulation.** |
| | Source: [datasheet SWRS273E](https://www.ti.com/lit/ds/symlink/awr2944.pdf) | | | | | | | | | |
| **Infineon BGT60TR13C** | 58–63.5 GHz | 1/3 | 400 MHz/µs; 5.5 GHz; 5 µs PLL settle | **IF low-pass 500 kHz typ**; high-pass 20/40/70/80 kHz; ADC 4 Msps; SPI 50 MHz | **Yes, CW mode (§10.2)** | None (needs a host MCU) | AoP | about 0.36 W (201 mA @ 1.8 V) | Digi-Key: **$18.01 @1, $14.00 @500, $12.29 @4.5k** reel; 0 stock, 26-week lead time | **Marginal**: T_c ≈ 16 µs → about 77 m/s at 60 GHz; SPI can't sustain 3 × 4 Msps continuously. **CW mode works.** |
| | Sources: [datasheet](https://www.infineon.com/dgdl/Infineon-BGT60TR13CDataSheet-DataSheet-v01_00-EN.pdf?fileId=8ac78c8c7d718a49017d94bac88e5d43), [Digi-Key](https://www.digikey.com/en/products/detail/infineon-technologies/BGT60TR13CE6327XUMA1/13282953) | | | | | | | | | |
| **Infineon BGT60UTR11AIP** | 60 GHz | 1/1 AoP | — | — | — | None | AoP | — | **NV** | NV (1T1R: speed and trigger only) |
| **Infineon BGT24LTR11** | 24 GHz | 1/1 I/Q (general knowledge, NV) | Doppler MMIC | Analog I/Q out | Yes (designed for CW Doppler) | None | VQFN | — | **NV** (historically a low single-digit $ part) | CW, fine |
| **Infineon BGT24LTR22 / BGT24MTR12** | 24 GHz | 2/2 and 1/2 (general knowledge, NV) | FMCW/FSK capable | Analog I/Q | Yes | None | VQFN | — | **NV** | CW/FSK, fine |
| **Acconeer A121** | 60 GHz pulsed coherent (not FMCW) | 1/1 | n/a | 4,095-sample frame buffer | Coherent sweeps give pulsed Doppler | None (host MCU) | 29 mm² AiP | about 75 mA @ 1.8 V while measuring | Digi-Key: **$16.74 @1, $8.22 @1k, $6.49 @3k** reel; about 14k in stock. Mouser about $6.84 @1k (snippet). XM125 module $22.20 @1 → $16.49 @500. | **Probably**: sweep about 5.4 µs (profile 3, HWAAS = 1) → about 185 kHz sweep rate → about 230 m/s, but each frame covers only about 22 ms and HWAAS = 1 gives low SNR on a small ball. Not hardware-tested. |
| | Sources: [Digi-Key A121](https://www.digikey.com/en/products/detail/acconeer-ab/A121-001-T-R/17883300), [Digi-Key XM125](https://www.digikey.com/en/products/detail/acconeer-ab/XM125/17883267), [acconeer-python-exploration](https://github.com/acconeer/acconeer-python-exploration) | | | | | | | | | |
| **NXP TEF82xx** | 76–81 GHz | 3/4 | 4 GHz effective | NV | NV | None (pairs with an S32R) | 7.5 mm eWLB | 1.5 W (2 TX, 50%) | NV | NV. **Excluded (77 GHz).** |
| | Source: [product page](https://www.nxp.com/products/TEF82XX) | | | | | | | | | |
| **NXP SAF85xx** | 76–81 GHz | 4/4 | "Fast chirp"; 4 GHz | NV | NV | A53 + M7 + SPT 3.4 / BBE32 DSP | about 10.6 × 11.3 mm | NV | NV | **Excluded (77 GHz).** |
| | Source: [product page](https://www.nxp.com/products/SAF85XX) | | | | | | | | | |
| **Calterah Rhine CAL60S244-IE** | 60–64 GHz | 4/4 | 4 GHz | ADC 50 Msps | NV | ARC EM6 300 MHz + baseband accelerator | NV | NV | "Order Now" (contact only) | NV (50 Msps ADC is promising) |
| | Source: [product page](https://www.calterah.com/en/soc-products/mmwave-radar/industrial-millimeter-wave-radar-soc-chip/alps-platform/industrial-rhine/cal60s244-ie); Alps and Kunlun are 77 GHz ([calterah.com](https://www.calterah.com/en/)) | | | | | | | | | |
| **Socionext SC1233 / SC1240** | 60 GHz | — | — | — | — | — | — | — | NV (product URLs returned 404) | NV |
| **RFbeam K-LC5** | 24 GHz | 1/1 I/Q | 260 MHz VCO, FM input | Analog | CW | None | 25 × 25 mm module | NV | NV; **NRND** (not recommended for new designs) | CW fine |
| | Source: [rfbeam.ch](https://rfbeam.ch/product/k-lc5-radar-transceiver/) | | | | | | | | | |
| **RFbeam K-MC4** | 24 GHz | 1 TX / 2 RX monopulse, I/Q on both | 180 MHz FM input | Analog | CW | None | Module, 30° × 12° beam | NV | NV | CW fine, plus angle |
| | Source: [rfbeam.ch](https://rfbeam.ch/product/k-mc4-radar-transceiver/) | | | | | | | | | |
| **RFbeam K-LD2** | 24 GHz | NV | NV | NV | NV | On-board FFT, digital output | Module | NV | NV | NV (fixed firmware, probably unsuited) |
| | Source: [rfbeam.ch](https://rfbeam.ch/product/k-ld2-radar-transceiver/) | | | | | | | | | |
| **InnoSenT iSYS-4001** | 24 GHz | — | FSK | — | — | Full system, RS232 | IP67 | — | NV | **No: rated 0.8–250 km/h (69 m/s max)** |
| | Source: [innosent.de](https://www.innosent.de/en/radar-systems/isys-4001-radarsystem/) | | | | | | | | | |
| **InnoSenT IPS-280** | 24 GHz | Analog I/Q | CW | Analog | CW | None | 9° × 18° beam | — | NV | CW fine |
| | Source: [innosent.de](https://www.innosent.de/en/sensors/ips-280-cw-radarsensor/) | | | | | | | | | |
| **HLK-LD2410** | 24 GHz | — | FMCW presence sensor | — | — | Fixed firmware, UART | Module | 5–12 V | **$3.20** | **No** (presence detection only) |
| | Source: [Hi-Link](https://www.hlktech.net/index.php?id=988) | | | | | | | | | |
| HB100 / Agilsense 10.5 GHz modules | 10.525 GHz | 1/1 | CW | Analog IF (single channel, no I/Q on basic HB100) | CW | None | Module | — | NV | CW fine for speed, but no direction sign without I/Q. Trigger only. |

### 3.3 Chip-selection takeaways
1. **Do not use 77 GHz parts.** AWR1843, AWR2944, TEF82xx, SAF85xx and the Calterah Alps/Kunlun parts are excluded in the US for a portable golf device (§4).
2. **The best 60 GHz SoC for us is the TI IWR6843 / IWR6843AOP** (about $21–$27 @1k). It is the only verified part with (a) complex IF (no ±velocity folding), (b) T_c short enough for 90 m/s with 1 TX, (c) 4 GHz bandwidth, (d) an on-chip DSP to run Doppler FFT and tracking, and (e) a documented continuous-wave mode. The **IWRL6432/AOP** (about $16 @1k) is cheaper and lower power, but its real-only IF and 5 MHz IF bandwidth make 90 m/s FMCW harder. Prototype both.
3. **The BGT60TR13C (about $12–$14 @1k)** is FMCW-marginal at ball speed, but it is a clean **60 GHz CW Doppler front end** with 3 RX for angle, provided a host MCU samples it.
   - Its high-pass corner (≥20 kHz) attenuates Doppler below about 50 m/s at 60 GHz in CW mode. Slow clubs, chips and putts would be lost unless the HPF can be bypassed (to verify).
   - Lead time is long (26 weeks).
4. **The Acconeer A121 (about $6.5–$8 @1k)** is the cheapest 60 GHz option and is in stock. It is a credible **trigger + ball-speed** sensor. Its pulsed-coherent, single-channel, 22 ms-frame architecture makes it unsuitable as the primary flight or angle radar.
5. **For Architecture B, use a 24 GHz Infineon BGT24-family MMIC.** BGT24LTR11 for 1T1R, or BGT24MTR12 / LTR22 for multi-RX. Pricing is NV, but 24 GHz MMICs are typically low-$ parts. Note that RFbeam's K-LC5 is **NRND**.
   - **Do not use** HLK-LD2410-class presence modules or iSYS-4001-class traffic sensors; they are capped well below ball speed or fixed-function.

---

## 4. Regulatory constraints and what they mean for band choice

### 4.1 United States (47 CFR Part 15)

| Rule | Band | Limit | Converted EIRP **[calc]** | Implication |
|---|---|---|---|---|
| **§15.245** field disturbance sensors | **10.500–10.550 GHz**; **24.075–24.175 GHz** | **2,500 mV/m @ 3 m** (average detector) fundamental; harmonics 25 mV/m; out-of-band −50 dBc or §15.209; peak limits per §15.35 ([Cornell LII](https://www.law.cornell.edu/cfr/text/47/15.245)) | EIRP = E²r²/30 → **≈ 32.7 dBm (1.9 W)** | Plenty of power. Bandwidth 50 MHz (X) or 100 MHz (K) means CW/FSK only; FMCW ΔR ≥ 1.5 m. TrackMan, Mevo and Mevo+ certify here. The 2nd/3rd harmonics of 24 GHz devices may be 25 mV/m even in restricted bands (§15.245(b)(1)(i)). |
| **§15.249** | 24.0–24.25 GHz | 250 mV/m @ 3 m | ≈ 12.7 dBm | 250 MHz bandwidth but 20 dB less power. Usable for a low-power FMCW short-range club/ball sensor; poor for outdoor tracking. |
| **§15.255** (amended by **FCC 23-35**, ET Docket 21-264; adopted May 18, 2023; published 88 FR 47394, July 24, 2023; effective Aug 23, 2023) | **57–71 GHz** | See the mode table below | — | Mobile FDS are now allowed throughout the band and the SRIMS concept is removed. Google Soli-style waivers were terminated six months after the effective date ([FR summary](https://www.govinfo.gov/content/pkg/FR-2023-07-24/html/2023-15367.htm); [FCC 23-35](https://docs.fcc.gov/public/attachments/FCC-23-35A1.pdf)). |
| **Part 95 Subpart M** | 76–81 GHz | Vehicular radars, or fixed/mobile radars in **airport air-operations areas** only; "fixed radar use outside of airport areas" prohibited ([DA 24-200, Mar 2024](https://docs.fcc.gov/public/attachments/DA-24-200A1.pdf); [KDB 653005](https://apps.fcc.gov/kdb/GetAttachment.html?id=kNG5zIS4SpD2PVoP9uNgyQ%3D%3D&desc=653005+D01+76-81+GHz+Radars+v01r02&tracking_number=230830)) | — | **A handheld/tripod golf launch monitor cannot certify at 77 GHz in the US** without a waiver. That rules out AWR1843, AWR2944, TEF82xx and Calterah 77 GHz parts for a US product. Note also that **§15.256** (level-probing radar at 75–85 GHz) is restricted to level measurement. |

**§15.255 FDS modes after 2023** ([Cornell LII §15.255](https://www.law.cornell.edu/cfr/text/47/15.255); [88 FR 47394](https://www.govinfo.gov/content/pkg/FR-2023-07-24/html/2023-15367.htm)). A device must stay in one mode for at least 33 ms before switching.

| Mode | Band | Peak EIRP | Transmit-time constraint | Usable by a portable golf unit? |
|---|---|---|---|---|
| Baseline | 57–71 GHz | 10 dBm (−10 dBm conducted) | None | Yes |
| Wideband low power | 57.0–61.56 GHz | 3 dBm | None | Yes |
| 50% mode | 57.0–61.56 GHz | 20 dBm | Off-time ≥16.5 ms per 33 ms (counting gaps ≥2 ms) | Yes. About 16 ms bursts could cover the whole impact window. |
| General | 57–64 GHz | 14 dBm | Off-time ≥25.5 ms per 33 ms (≈23% duty) | Yes. Each burst gives at most about 7.5 ms on, which is too short to cover impact plus flight reliably unless triggered. |
| WiGig ch. 1 | **57.0–59.4 GHz** | **20 dBm indoor / 30 dBm outdoor** | **None** | **Yes** (mobile and fixed alike). 2.4 GHz bandwidth gives ΔR = 6 cm. This is the best FMCW mode for us. "Indoor/outdoor" is undefined, so get a TCB opinion. |
| Outdoor fixed / vehicular | 57–64 GHz | 20 dBm | 50% | Unclear. A tripod outdoors *might* count as a "temporary … fixed application." |
| **ISM narrowband** | **61.0–61.5 GHz** (≤500 MHz occupied) | **40 dBm average / 43 dBm peak**; ≤10 dBm average outside 61.0–61.5 GHz | None | **Yes. The order explicitly removed the "fixed" restriction** ("we remove the 'fixed' restriction applicable to FDS operation in section 15.255(c)(2)," [FCC 23-35 ¶22](https://docs.fcc.gov/public/attachments/FCC-23-35A1.pdf)). This mode is ideal for high-power CW/FSK Doppler. Watch RF-exposure (MPE/SAR) limits for a hand-held 10 W EIRP device; a tripod-mounted unit at >20 cm is easier. |
| Pulse | 57–64 GHz | 13 dBm average | ≤10% in any 0.3 µs | Not useful |

### 4.2 Europe (CEPT ERC Rec 70-03, edition of June 2026, [docdb.cept.org/document/845](https://docdb.cept.org/document/845))

**Annex 6 (radiodetermination), all under ETSI EN 300 440:**

| Band | EIRP limit | Notes |
|---|---|---|
| 9.2–9.5 GHz | 25 mW | — |
| 9.5–9.975 GHz | 25 mW | — |
| **10.5–10.6 GHz** | **500 mW** | Hungary limits this to 25 mW (national remark) |
| 13.4–14 GHz | 25 mW | — |
| **24.05–24.25 GHz** | **100 mW** | No duty-cycle requirement. National exceptions below. |

Every 24 GHz limit above is lower than the US 15.245 figure of about 1.9 W, which is why the EU Mevo+ runs 17 dBm ±3 versus 24 dBm in the US ([Mevo+ manual](https://hubspot.carlofet.com/hubfs/Product%20Documents/Launch%20Monitor/Mevo+/Mevo%20Plus%20User%20Manual.pdf)).

**National remarks that matter for a portable CW Doppler product:**
- **France.** "No restriction for fixed installations. Otherwise limited to 0.1 mW e.i.r.p. in 24.10–24.15 GHz." FMCW is limited to 20 mW mean / 50 mW peak EIRP, with a minimum sweep speed of 5 MHz/ms.
- **United Kingdom.** "To protect police speed meters devices operating in 24.05–24.15 GHz must employ a minimum sweep rate of 2 MHz/ms."

So in those markets a pure-CW portable 24 GHz carrier should sit in roughly 24.15–24.25 GHz. That overlaps the US 15.245 band (24.075–24.175 GHz) only at 24.15–24.175 GHz. A 24.16 GHz ±10 MHz carrier would satisfy the US, France and the UK. **Firmware-selectable carrier per region is required.**

**Annex 1 (non-specific SRD), under ETSI EN 305 550:**
- **57–64 GHz:** 100 mW EIRP and 10 mW output power.
- **61–61.5 GHz:** 100 mW EIRP.

100 mW is 20 dBm. That equals the US 57–59.4 GHz *indoor* limit but is 10 dB below the US outdoor limit (30 dBm) and 20 dB below the US 61.0–61.5 GHz limit (40 dBm). **A design that relies on high-power US 60 GHz modes needs a reduced-power EU SKU.** 76–77 GHz appears in Annex 6 only for ground-based SAR.

**Assessment, from general knowledge and not re-verified:** the EU sunset of 24 GHz *wideband* automotive UWB short-range radar does not affect 24.05–24.25 GHz narrowband use. 70-03 notes that "the regulation in the bands d1) to d5) for the band 24.05–24.25 GHz for automotive radars is without any plans for a time limit."
- **Japan.** The Mevo+ Japanese label shows a **10.5–10.55 GHz, indoor-only** "moving body detection sensor" variant (Japanese caution text in the [Mevo+ manual](https://hubspot.carlofet.com/hubfs/Product%20Documents/Launch%20Monitor/Mevo+/Mevo%20Plus%20User%20Manual.pdf)). This suggests the 24 GHz SRD rules in Japan did not suit them. Market-by-market SKUs are normal in this category.

### 4.3 Band-choice consequences for us

| Band | Bandwidth → ΔR | Max EIRP (US) | Portable OK (US)? | Doppler @ 90 m/s | Fit |
|---|---|---|---|---|---|
| 10.5 GHz | 50 MHz → CW only | ≈32.7 dBm | Yes | 6.3 kHz | Outdoor flight tracking with a big antenna. Wrong form factor for us. |
| 24.075–24.175 GHz | 100 MHz → 1.5 m | ≈32.7 dBm | Yes | 14.5 kHz | **Best power-per-dollar for outdoor ball tracking in a small box.** Proven, global. |
| 24.0–24.25 GHz (15.249) | 250 MHz → 0.6 m | ≈12.7 dBm | Yes | 14.5 kHz | Short-range only |
| 57.0–59.4 GHz | 2.4 GHz → 6 cm | 20 dBm indoor / 30 dBm outdoor, no duty limit | Yes | 36.8 kHz | **Best for FMCW: range-gated indoor ball, club and golfer separation** |
| 61.0–61.5 GHz | 500 MHz → 30 cm | 40 dBm average | Yes (since 2023) | 36.8 kHz | **High-power CW/FSK at 60 GHz** (US only); strongest unmarked micro-Doppler |
| 76–81 GHz | 4 GHz | — | **No** (vehicles/airports) | 46 kHz | Excluded for a US product |

---

## 5. Hybrid radar + camera

### 5.1 What radar adds to a camera system
1. **Trigger.** A CW Doppler radar detects the clubhead approaching at 25–60 m/s, tens of milliseconds before impact, with negligible false triggers from practice swings (no ball line appears after the club) **[assessment]**. That lets the camera burst-capture exactly the right ~5–20 ms with a short-exposure IR strobe, saving power and enabling very high frame rates in a windowed region of interest. Rapsodo patent prior art explicitly uses "radar feedback to determine that a golf club has moved in to the field at a sufficient speed" ([US7497780B2](https://patents.google.com/patent/US7497780B2/en)).
2. **Ball and club speed** with essentially no model dependence. Doppler gives speed to about 0.1–0.3 m/s precision within a few milliseconds of dwell **[calc: Δv_res = λ/(2T); 24 GHz, T = 20 ms gives 0.31 m/s raw bin, refined by peak interpolation at high SNR]**. Camera speed depends on pixel calibration and the inter-frame interval. Radar speed is an independent cross-check that catches camera calibration drift.
3. **Outdoor flight.** At 24 GHz with 24–30 dBm EIRP and a modest array, measured ball tracking to roughly 30–60 m is plausible **[calc, §1.1]**. That gives real drag and lift estimates for the early trajectory, so we can (a) validate the camera-measured spin and axis against the observed curvature, and (b) correct the aero model per ball type and per altitude/temperature. TrackMan's 10.5 GHz radar does this for the full flight; we cannot in a small box, but even 30 m of measured flight greatly reduces carry error outdoors **[assessment]**.
4. **Club speed and path** independent of camera occlusion by the golfer's body (relevant for down-the-line camera placement).
5. **Light-independent operation** in full sun, where camera exposure and IR strobe contrast suffer.

### 5.2 What the camera adds to radar
- Markerless spin rate and axis at short range (a high-speed global-shutter camera reading dimple and logo texture), which radar cannot do indoors (§1.5).
- Face angle, dynamic loft, face-to-path and impact location, measured from images of the clubhead at impact rather than inferred.
- Absolute launch geometry independent of multipath, and target alignment.
- **Market proof:** TrackMan OERT/iO (camera for spin and club, radar for speed and distance), FlightScope Fusion Tracking in Mevo Gen2 and X3C ([flightscope.com](https://flightscope.com/)), and Rapsodo MLM2PRO (radar + dual cameras, [rapsodo.com](https://rapsodo.com/products/mlm2pro)). Garmin's own premium unit, the R50, is camera-based.

### 5.3 Minimum radar cost by role (estimates; see §3 for chip prices)

| Role | Required radar capability | Minimum realistic radar BOM (10k units) |
|---|---|---|
| **Trigger only** | 1 TX/1 RX CW Doppler, I/Q, any band | **$5–$15.** For example, a 24 GHz K-band module or a single MMIC with a patch antenna, sampled by the main MCU's ADC. An Acconeer A121 (about $6.5–$8.2 @1k, in stock at Digi-Key) is also feasible. At high sweep rates it can reach roughly 230 m/s unambiguous, but its 22 ms frames and low SNR at HWAAS = 1 make it trigger/speed-class only (see §3). |
| **Trigger + ball/club speed** | 1 TX/1–2 RX CW (I/Q), ≥100 kS/s ADC, about 20 dBm EIRP | **$10–$25** |
| **Trigger + speed + outdoor flight (direction, launch angle cross-check, 30–60 m track)** | 1 TX/3–4 RX phase-comparison array, 24 GHz at 24–30 dBm EIRP (external PA if needed), 4-channel simultaneous ADC, FSK for range | **$25–$60** (MMIC(s) $8–$25, 4-channel ADC/MCU share $5–$10, Rogers/hybrid RF PCB area $5–$15, PA/LNA $0–$8, shielding/radome $3–$5) |
| **"Full radar" (TrackMan-class: club data, sideband spin, long-range flight)** | Dual band (10.5 GHz long-range with about 25 cm aperture plus 24 GHz short-range), ≥4 RX each, high-dynamic-range ADCs, FPGA/DSP | **$150–$350** in radar alone (two RF boards, large low-loss antennas, PAs, 8+ ADC channels, DSP), plus a size and weight penalty. Still needs markers indoors. |

---

## 6. Verdict and candidate architectures

### 6.1 Can radar alone deliver our markerless suite at our price?

| Metric | Radar-alone outdoors | Radar-alone indoors (8–12 ft to screen) |
|---|---|---|
| Ball speed | **Yes**, excellent | **Yes**, excellent |
| Club speed | **Yes** | **Yes** |
| Launch V/H | **Yes** (≥3 RX) | **Yes**, with some floor-multipath bias |
| Attack angle, club path | Approximate | Approximate |
| Spin rate (measured, unmarked) | Possible with long dwell (TrackMan-class sensitivity; a small 24 GHz box is marginal beyond about 30 m) | **No for driver/woods** (1.4–2.4 rev). Marginal for irons, plausible for wedges. Every vendor requires markers or RCT balls. |
| Spin axis (measured) | Yes, from lift/trajectory if tracked long enough | **No** (no curvature to observe); markers plus multi-RX at best |
| Carry/total/apex/descent | Measured (if tracked) plus model | Model only |
| Face angle, dynamic loft, face-to-path | **Derived** via D-plane inversion, not measured | Derived from estimated inputs, so weak |
| Impact location | **No** (weak inference only) | **No** |

**Answer: No.** Radar alone cannot deliver markerless measured spin, spin axis, face angle, dynamic loft and impact location in a small indoor room. Spending more does not fix this: it is set by how long the ball is visible and how strong the unmarked modulation is. TrackMan, the inventor of radar spin, uses cameras for its indoor product.

### 6.2 Candidate radar architectures

#### Architecture A — "Full radar" (TrackMan-like). *Not recommended.*
- **Hardware.**
  - 10.5 GHz CW/FSK long-range radar: 1 TX + 4 RX, about 25 × 25 cm array, about 27–30 dBm EIRP.
  - 24 GHz short-range radar: 1 TX + 4 RX, FSK, for club and impact.
  - 8-channel simultaneous 16–24-bit ADC; Zynq-class FPGA or application processor DSP.
- **Radar BOM:** $150–$350. Device size about 30 × 30 cm.
- **Expected performance:**
  - Outdoors: TrackMan-like ball tracking, including unmarked sideband spin with good SNR and measured carry.
  - Indoors: speed/launch good, but spin needs markers, and club face, dynamic loft and impact location are inferred.
- **Why not.** It fails the markerless-indoor requirement and the portability and BOM targets. It also carries the most IP exposure: the TrackMan sideband patent family is still partly in force, and US 8,845,442 runs to 2029-05-18.

#### Architecture B — "24 GHz speed/trigger/flight radar + high-speed camera" (**recommended for v1**)
- **Radar.**
  - 24.075–24.175 GHz (15.245), CW + 2–3-tone FSK.
  - 1 TX + 3 RX (L-shaped, with one short and one long baseline) or 4 RX.
  - Transmit power: MMIC output plus array gain, giving about 24–30 dBm EIRP in the US; the EU SKU is capped at 20 dBm.
  - 4-channel simultaneous I/Q sampling at about 200 kS/s, via the MCU or an external audio-class ADC.
  - Optional external 24 GHz PA for outdoor range.
- **Radar BOM:** about $25–$60.
- **Camera.** A global-shutter high-frame-rate sensor with an 850 nm strobe, triggered by the radar, measures spin, axis, face and impact location. This is out of scope here; see the camera report.
- **Expected radar performance [assessment]:**
  - Ball speed ±0.3–0.5 mph and club speed ±1 mph.
  - Launch direction and angle ±0.3–0.5° (outdoors and indoors with ≥2 m of flight; used to cross-check the camera).
  - Outdoor ball track 30–60 m, used to fit drag and lift, validate camera spin and axis, and anchor carry.
  - Rejects practice swings.
- **Limitations.** Range resolution is 1.5 m even with FSK range per Doppler bin. The screen echo is separated by Doppler sign and magnitude rather than by range. Antennas need a Rogers-class laminate section.
- **Why.** Lowest risk, mature 24 GHz parts, global regulatory path, and it directly mirrors where FlightScope (Fusion) and TrackMan (iO/OERT) landed.

#### Architecture C — "60 GHz FMCW SoC + high-speed camera" (**strong alternative; prototype in parallel**)
- **Radar.**
  - A single-chip 60 GHz FMCW radar SoC with antenna-on-package (3 TX / 4 RX; see §3). The primary candidate is the **TI IWR6843AOP**: complex IF, 1-TX T_c ≈ 9.6 µs → v_max ≈ 129 m/s, on-chip DSP, about $21–$27 @1k. The lower-cost alternative is the TI IWRL6432AOP (about $16 @1k; real-only IF). Avoid the BGT60TR13C for FMCW at ball speed (v_max ≈ 77 m/s).
  - Run in the **57.0–59.4 GHz mode** (2.4 GHz bandwidth, 20 dBm indoor / 30 dBm outdoor, no duty limit) for 6 cm range gating.
  - Optionally switch to **61.0–61.5 GHz CW/narrowband** at higher EIRP for an outdoor flight-tracking mode (US only), observing the 33 ms mode-dwell rule.
- **Radar BOM:** about $25–$45 (IWR6843AOP about $21–$27 + PMIC/LDOs $3–$6 + QSPI flash $1 + passives/radome $2–$5; no RF laminate needed with AoP). The US-only high-power 61 GHz mode adds an external antenna/lens and possibly a PA, roughly $10–$25 more.
- **Pros.**
  - Range gating separates ball, club, golfer, mat and screen.
  - 2.5× Doppler sensitivity versus 24 GHz.
  - About 8 dB stronger unmarked spin modulation by the Bessel argument (§1.4), which is the best chance at a radar spin *cross-check* for irons and wedges indoors.
  - One chip with an on-board DSP/MCU; smallest PCB.
- **Cons.**
  - **Velocity ambiguity.** For a 90 m/s ball, v_max = λ/(4·T_c) requires a chirp repetition period of ≤13.6 µs at 61 GHz (complex IF, single TX) **[calc]**. With TDM-MIMO over 3 TX this becomes ≤4.5 µs per TX, which is not achievable. Mitigations: single-TX bursts for velocity with MIMO bursts for angle; staggered chirp periods with Chinese-remainder unwrapping; or using the known club→ball smash prior.
  - Small AoP aperture means short outdoor range (about 10–20 m at 10–20 dBm) **[calc]**.
  - EU power is lower.
  - Low-power parts may not meet the needed chirp rate (see the §3 table).

### 6.3 Recommendation for the engineering spec
1. Spec the product as **camera-primary, radar-assisted**. Radar requirements: trigger latency under 5 ms before impact; ball speed ±0.5 mph; club speed ±1 mph; launch direction ±0.5° (for cross-check); outdoor ball track ≥30 m; operation with 2.4 m (8 ft) of ball flight; rejection of the screen rebound and adjacent-bay interference.
2. **Build two radar prototypes in parallel** (each is weeks of work with eval kits): B (24 GHz CW/FSK, 1T3R) and C (60 GHz FMCW SoC). Measure on real hitting bays (a) speed and launch agreement against a reference unit (GCQuad / TrackMan) and (b) the unmarked spin-sideband SNR per club at 8–12 ft. If C shows usable unmarked spin for irons and wedges, it becomes a valuable second spin estimator for the fusion filter.
3. **Do not plan any radar-only path to face angle, dynamic loft or impact location.**
4. **Before freezing the design:**
   - Commission an FTO review on the TrackMan spin family (US 8,845,442 to 2029), the FlightScope/EDH fusion and spin patents, and the TrackMan marker patents.
   - Get a TCB opinion on the §15.255 "indoor/outdoor" mode definitions and on RF exposure for any 61 GHz high-power mode.
   - Design the 24 GHz carrier to be region-selectable. The France and UK constraints in §4.2 push a CW carrier to about 24.15–24.175 GHz to satisfy all three markets.

---

### Source index
- 47 CFR §15.245: https://www.law.cornell.edu/cfr/text/47/15.245
- 47 CFR §15.255: https://www.law.cornell.edu/cfr/text/47/15.255
- FCC 23-35 (60 GHz Report & Order): https://docs.fcc.gov/public/attachments/FCC-23-35A1.pdf
- 88 FR 47394 (Federal Register summary): https://www.govinfo.gov/content/pkg/FR-2023-07-24/html/2023-15367.htm
- FCC DA 24-200 (76–81 GHz compliance guide): https://docs.fcc.gov/public/attachments/DA-24-200A1.pdf
- FCC KDB 653005: https://apps.fcc.gov/kdb/GetAttachment.html?id=kNG5zIS4SpD2PVoP9uNgyQ%3D%3D&desc=653005+D01+76-81+GHz+Radars+v01r02&tracking_number=230830
- TrackMan 4 FCC: https://fccid.io/SFX-TMB4A ; TrackMan III: https://fccid.io/SFX-TMANIII
- TrackMan specs: https://www.trackman.com/golf/launch-monitors/tech-specs
- Mevo FCC: https://fccid.io/QXP-A7310 ; Mevo+ FCC: https://fcc.report/FCC-ID/QXP-LJ361 ; internal photos: https://fccid.io/QXP-LJ361/Internal-Photos/Internal-Photos-4549449
- Mevo+ manual: https://hubspot.carlofet.com/hubfs/Product%20Documents/Launch%20Monitor/Mevo+/Mevo%20Plus%20User%20Manual.pdf
- FlightScope site (Mevo Gen2, Fusion): https://flightscope.com/
- GSF Mevo+ teardown thread: https://golfsimulatorforum.com/forum/flightscope/277362-mevo-teardown
- GSF TrackMan frequencies thread: https://golfsimulatorforum.com/forum/off-topic/all-off-topic/273222-new-higher-frequency-radar-sensors
- GSF R10 thread: https://golfsimulatorforum.com/forum/golf-simulator-brands-and-types/garmin/336862-new-garmin-approach-r10-launch-monitor-simulator/page2
- Garmin R10 manual: https://www8.garmin.com/manuals/webhelp/GUID-E2BBF6BE-4276-436F-B697-59ABEFD61933/EN-US/Approach_R10_OM_EN-US.pdf
- Garmin 60 GHz filing (Notebookcheck): https://www.notebookcheck.net/New-Garmin-device-reveals-itself-with-60-GHz-radar-capabilities.1217864.0.html
- Rapsodo MLM2PRO: https://rapsodo.com/products/mlm2pro
- Patents: US8845442B2 https://patents.google.com/patent/US8845442B2/en ; US9645235B2 https://patents.google.com/patent/US9645235B2/en ; US8912945B2 https://patents.google.com/patent/US8912945B2/en ; WO2021005577A1 https://patents.google.com/patent/WO2021005577A1/en ; US20140191896A1 https://patents.google.com/patent/US20140191896A1/en ; US7497780B2 https://patents.google.com/patent/US7497780B2/en ; US20190282881A1 https://patents.google.com/patent/US20190282881A1/en
- Chip datasheets and distributors: TI IWR6843 https://www.ti.com/lit/ds/symlink/iwr6843.pdf ; TI IWRL6432 https://www.ti.com/lit/ds/symlink/iwrl6432.pdf ; TI AWR2944 https://www.ti.com/lit/ds/symlink/awr2944.pdf ; TI SWRA553A https://www.ti.com/lit/an/swra553a/swra553a.pdf ; Infineon BGT60TR13C https://www.infineon.com/dgdl/Infineon-BGT60TR13CDataSheet-DataSheet-v01_00-EN.pdf?fileId=8ac78c8c7d718a49017d94bac88e5d43 ; Digi-Key BGT60TR13C https://www.digikey.com/en/products/detail/infineon-technologies/BGT60TR13CE6327XUMA1/13282953 ; Digi-Key A121 https://www.digikey.com/en/products/detail/acconeer-ab/A121-001-T-R/17883300 ; Digi-Key XM125 https://www.digikey.com/en/products/detail/acconeer-ab/XM125/17883267 ; RFbeam https://rfbeam.ch/ ; InnoSenT https://www.innosent.de/en/ ; Calterah https://www.calterah.com/en/ ; NXP TEF82xx https://www.nxp.com/products/TEF82XX
- CEPT ERC Rec 70-03 (June 2026 edition): https://docdb.cept.org/document/845
