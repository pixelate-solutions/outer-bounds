# 04 — Camera / Photometric Launch Monitor: Engineering Deep Dive

*Prepared October 2026. Scope: markerless (no club stickers, no marked balls, any ball), side-of-ball / portable, indoor and outdoor in direct sun, BOM target about $250–600, so the camera subsystem needs to be about $200–450.*

> **How to read this document.** Each number is tagged with one of three markers:
> - **[cited]**: from a linked source.
> - **[calc]**: derived in this document. The math is shown, and the core numbers were checked with a short Python script.
> - **[est.]**: an engineering estimate or a recalled value I could not re-verify in this session.
>
> The research session ran out of its web-search budget before every component price could be confirmed. These items are still **[est.]** and need distributor quotes: bare-die sensor prices, OV9281/AR0144/OG01A1B module prices, i.MX8M Plus, Kria K26, and Lattice FPGA prices, and 60 GHz radar module prices. The list is repeated in §8.

---

## 0. Executive summary (the engineering conclusions)

1. **Outdoors, exposure gating matters more than wavelength or filter.** In the 50 nm band around 940 nm, the sun puts about **22 W/m²** on the ball (ASTM G173 global, [calc] from the [reference data](https://raw.githubusercontent.com/pvlib/pvlib-python/main/pvlib/data/ASTMG173.csv)). With a **5 µs exposure matched to the strobe**, sunlight adds only about **4%** of the strobe signal [calc §1.6]. With a **1 ms "open shutter, multiple strobes in one frame" exposure** (SkyTrak/PiTrac style), sunlight is **about 8× the strobe signal** and the image fails. Even a 10 nm VCSEL-grade filter does not rescue the long exposure. **So every ball and club image must be its own gated exposure, roughly 3–10 µs long.** This is why PiTrac says plainly it cannot work outdoors ([Hackaday](https://hackaday.io/project/195042-pitrac-the-diy-golf-launch-monitor)), why the original Square was indoor-only, and why Square's 2026 Omni still shows "less consistent outdoor spin in bright sun" ([GolfOnline](https://www.golfonline.co.uk/square-golf-omni-launch-monitor-review)).
2. **Motion blur sets the strobe pulse width.** At 90 m/s, keeping blur under 0.5 mm needs ≤5.6 µs, and keeping it under 1 px (0.275 mm/px) needs ≤3 µs [calc]. PiTrac-style 10–20 µs pulses ([US12401909](https://patents.google.com/patent/US12401909B2/en)) smear a driver-speed ball by 0.9–1.8 mm, or 3–7 px. Short pulses need high peak power: roughly **24 × 5 A, 940 nm LEDs (about 400 W peak, about 2 mJ per flash)** for a 3.45 µm-pixel sensor at 0.45 m [calc §1.6].
3. **Spin needs ≥3–8 ball images spread over ≥1.5–3 ms, each ≤1.25 ms apart for wedges.** At 12,000 rpm the ball turns 72°/ms, and aliasing sets in at 180° per interval [calc]. A driver spinning 2,500 rpm turns only 15°/ms, so ±100 rpm needs a **long time baseline**, not a high frame rate. With per-image orientation error σθ = 0.5°, 8 images over 3 ms give σ ≈ 30 rpm, while 2 images 1.5 ms apart give σ ≈ 79 rpm [calc §1.4].
4. **The Sony IMX900's "Quad Shutter Control" is the most interesting 2026 component for this product.** It captures **four separately timed, separately exposed sub-images in one frame** (each 2×2 pixel phase is its own image, giving 1032×776 per phase), at "microsecond intervals … effective 100,000 fps" ([Sony](https://www.sony-semicon.com/en/products/is/industry/gs/imx900.html), [e-con](https://www.e-consystems.com/usb-cameras/sony-imx900-global-shutter-hdr-monochrome-camera.asp)). Each phase can be gated to its own µs strobe. That gives the outdoor-safe multi-exposure that cheap strobe monitors lack, without a 1,000 fps data pipeline. **It needs datasheet and NDA confirmation of external-trigger control per phase before we commit.**
5. **Markerless spin is solved in the literature and in products. Markerless face angle and impact location are not.** In October 2026, every camera monitor that reports measured face angle or impact location still needs stickers:
   - Foresight 4-dot ([Foresight help](https://help.foresightsports.com/hc/en-us/articles/4408197030035-How-to-Apply-and-Maintain-Club-Markers-for-Foresight-Sports-Devices))
   - Uneekor XO2 ([manual](https://download.uneekor.com/docs/EYEXO2_Manual.pdf))
   - Square Omni ([GolfOnline](https://www.golfonline.co.uk/square-golf-omni-launch-monitor-review))
   - Garmin R50 ([Garmin](https://www.garmin.com/en-US/newsroom/press-release/outdoor/meet-the-garmin-approach-r50-the-only-portable-golf-launch-monitor-with-a-built-in-simulator/))

   Uneekor's sticker-free EYE XR *calculates* face angle "using a proprietary mathematical formula" ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/first-look-uneekor-eye-xr-overhead-launch-monitor)). This is both our biggest technical risk and our clearest differentiator. The best public prior art is Rapsodo's model-fit patent (<1° RMS, [US11583746](https://patents.google.com/patent/US11583746B2/en)).
6. **Recommended direction:**
   - **Architecture B** (§6): 2× IMX900 mono in vertical stereo, quad-shutter gated 940 nm strobes, MCU timing, RK3588 or QCS6490. Estimated camera-subsystem BOM is about **$440 at 1k units and about $310 at 10k** [est.].
   - **Architecture A** (4× IMX296 in time-staggered stereo pairs) is the low-risk fallback and MVP path at about $425 / $305.
   - **Architecture C** (high-speed ROI ring buffer on IMX273-class sensors with an FPGA) gives the best data but runs about $620–870 / $440–690.

---

## 1. Physics and requirements (with math)

### 1.1 Inputs

| Quantity | Value | Notes |
|---|---|---|
| Ball diameter D | 42.67 mm (r = 21.34 mm) | USGA minimum |
| Dimple diameter | about 3.5–4.5 mm | [est.] typical |
| Max ball speed | 90 m/s (201 mph) | spec |
| Max club speed | 58 m/s (130 mph) | spec |
| Spin range | 1,500–12,000 rpm | spec |
| Impact (contact) duration | about 0.45 ms | [est.] standard figure |
| Ball–sensor distance Z (side-of-ball) | 0.45 m nominal, ±0.1 m | design choice |

Spin kinematics [calc]: ω[°/ms] = rpm × 0.006.

| rpm | rad/s | °/ms | surface speed ωr | time to rotate 180° |
|---|---|---|---|---|
| 1,500 | 157 | 9 | 3.4 m/s | 20 ms |
| 2,500 (driver) | 262 | 15 | 5.6 m/s | 12 ms |
| 6,000 | 628 | 36 | 13.4 m/s | 5 ms |
| 9,000 | 942 | 54 | 20.1 m/s | 3.3 ms |
| 12,000 (wedge) | 1,257 | 72 | 26.8 m/s | 2.5 ms |

For a cross-check, Imai et al. describe a markerless golf ball "which rotates up to 60 degrees in a 1-millisecond frame" ([IEEE SII 2016](https://ieeexplore.ieee.org/document/7844057/)). That is 10,000 rpm at 1,000 fps, consistent with the table.

### 1.2 Exposure time (motion blur)

Blur b = v · t_exp, so t_exp ≤ b / v [calc]:

| Case | v | b ≤ 0.5 mm | b ≤ 1 px @ 0.275 mm/px |
|---|---|---|---|
| Driver ball | 90 m/s | **5.6 µs** | **3.1 µs** |
| Avg. tour driver ball | 70 m/s | 7.1 µs | 3.9 µs |
| Club head | 58 m/s | 8.6 µs | 4.7 µs |
| Wedge ball | 45 m/s | 11 µs | 6.1 µs |

Rotational blur at the limb at 12k rpm is 26.8 m/s × 5 µs = 0.13 mm, which is negligible next to translation.

**Requirement: strobe pulses of 3–5 µs** (≤8 µs as the floor). Blur from translation runs only along the direction of travel, so edges perpendicular to the motion (the ball's top and bottom) stay sharp. This becomes an argument for a vertical stereo baseline (§2.3).

For comparison:
- PiTrac / US12401909 use 10–20 µs pulses ([patent](https://patents.google.com/patent/US12401909B2/en)).
- Wang et al.'s high-speed stereo golf tracker used 35 µs exposures at 810 fps with *marked* balls ([IEEE TIM 2018](https://www.researchgate.net/publication/327922724_Tracking_a_Golf_Ball_With_High-Speed_Stereo_Vision_System)). At 70 m/s that is 2.5 mm of blur, acceptable for markers but not for dimples.

### 1.3 Field of view, resolution, depth of field

**FOV along the flight line (x):** The FOV has to hold the hitting-zone tolerance plus at least 250–300 mm of post-impact flight plus about 100 mm of club approach.
- Competitor hitting zones for reference: SkyTrak+ 4.5″ (vs 2″ for the original) ([Golfible](https://golfible.com/skytrak-plus-review/)); Uneekor EYE MINI 12″×8″ ([Uneekor](https://uneekor.com/en-us/products/eye-mini-standalone)); GCQuad "six times larger than GC2" ([Golf Digest](https://www.golfdigest.com/story/foresights-gcquad-launch-monitor-expands-to-four-cameras-wider-view-20-times-the-information)).

**Vertical (y):** A lob wedge launched at 45° rises as far as it travels, about 150–250 mm within the useful window.

**Proposed FOV at the ball plane: 400 mm × 300 mm.**

**Lens focal length:** f = sensor_width × Z / W.

| Sensor (full width across 400 mm) | mm/px | Ball diameter (px) | Dimple (px) | f @ Z=450 mm | f in px |
|---|---|---|---|---|---|
| IMX296 1456 px, 3.45 µm | 0.275 | 155 | 14.6 | 5.65 mm | 1638 |
| AR0234 1920 px, 3.0 µm | 0.208 | 205 | 19.2 | 6.5 mm | 2160 |
| IMX900 2064 px, 2.25 µm | 0.194 | 220 | 20.6 | 5.2 mm | 2322 |
| IMX900 quad-phase 1032 px (4.5 µm effective) | 0.388 | 110 | 10.3 | 5.2 mm | 1161 |
| IMX287 728 px, 6.9 µm | 0.549 | 78 | 7.3 | 5.65 mm | 819 |

[calc]. As a lower bound from prior art: Strokeplay's dimple-capable stereo patent images at 14 px/cm, about a **60 px ball** ([US10564250](https://patents.google.com/patent/US10564250B2/en)). So about 100–160 px per ball is comfortable, and about 60–80 px is the minimum. PiTrac's 6 mm, 3 MP M12 lens on the IMX296 matches our 5.65 mm figure ([PiTrac parts list](https://docs.pitrac.org/hardware/parts-list/)).

**Depth of field** [calc] (f = 5.65 mm, circle of confusion = 2 px = 6.9 µm, focus 450 mm):

| f-number | Near limit | Far limit | DoF |
|---|---|---|---|
| f/1.4 | 396 mm | 521 mm | ±60 mm |
| f/2.0 | 377 mm | 559 mm | about ±90 mm |
| f/2.8 | 354 mm | 618 mm | about ±130 mm |

**f/1.8–2.0 is the sweet spot.** Ball-placement tolerance toward and away from the unit sets this choice, trading against the photon budget (§1.6).

### 1.4 Frame rate / strobe timing

**Images in FOV.** Usable window W_use ≈ 300 mm. N images at speed v need an interval Δt ≤ W_use / ((N−1)·v) [calc]:

| v | N = 2 | N = 3 | N = 4 | N = 8 |
|---|---|---|---|---|
| 90 m/s | 3.3 ms | 1.67 ms (600 fps-equiv) | 1.1 ms (900 fps) | 0.48 ms (2,100 fps) |
| 45 m/s (wedge) | 6.7 ms | 3.3 ms | 2.2 ms | 0.95 ms |

**Spin aliasing.** The rotation between consecutive images must be under 180°, and under about 60–90° for robust texture matching. At 12,000 rpm, 90° takes **1.25 ms**, so **Δt ≤ about 1.25 ms (≥800 fps-equivalent) for wedges.** This agrees with:
- Strokeplay: ">500 fps… above 1,000 fps a ball at maximum speed and spin is captured two to three times… about 60° rotation per frame at max spin" ([US10564250](https://patents.google.com/patent/US10564250B2/en)).
- The common observation that cameras below about 200 fps alias at the high end (summarized from the [deep-learning spin patent](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12582870)).

**Use non-uniform intervals.** For example 0.5, 1.2, 2.5 ms (cf. PiTrac's 0.5/2/6/12/15/40 ms schedule in [US12401909](https://patents.google.com/patent/US12401909B2/en)). This works like a vernier, resolving aliasing because a wrong 360°-wrap hypothesis cannot fit every interval at once. A related idea, coded **M-sequence multi-exposures** in a single frame, was demonstrated for table tennis spin by Kagami's group ([SICE JCMSI 2025](https://www.tandfonline.com/doi/full/10.1080/18824889.2025.2466881)).

**Spin precision vs. time baseline** [calc]. Model: least-squares fit of orientation θ(t) at N equally spaced instants over span T, with per-image orientation error σθ. Then σω = σθ / √Σ(tᵢ − t̄)².

| σθ | N | T | σω | rpm |
|---|---|---|---|---|
| 0.5° | 2 | 1.5 ms | 0.47°/ms | **79** |
| 0.5° | 4 | 2.5 ms | 0.27°/ms | 45 |
| 0.5° | 8 | 3.0 ms | 0.18°/ms | **30** |
| 1.0° | 2 | 1.5 ms | 0.94°/ms | 157 |
| 0.3° | 8 | 3.0 ms | 0.11°/ms | 18 |

The target is ±100 rpm or ±5%. For a 2,500 rpm driver that means ±100 rpm, which **needs σθ ≲ 0.5° with ≥4 images, or ≤0.6° with 2 images ≥1.5 ms apart.** This is why GCQuad grabs "up to 200 images of the golf ball within the first 30 cm" ([Foresight EU](https://foresightsports.eu/launch-monitors/gcquad/)) and why Foresight describes it as 10,000 fps ([Golf.com](https://golf.com/gear/how-it-works-foresight-sports-gcquad-launch-monitor/)).

**Can we reach σθ ≈ 0.3–0.5°?** [calc]
- Angular resolution ≈ σ_pos / R_px.
- With R_px = 77 px (IMX296 layout) and an aggregate texture registration error of 0.2–0.5 px, σθ ≈ 0.15–0.37°. So the hardware is capable.
- In practice the limits are lighting changes as dimples rotate under fixed strobes, blur, and the accuracy of the 3D ball center and radius.

**Spin axis ±1–2°** [calc]. Tilt α = atan(ω_side / ω_back), so δα ≈ δω_side / |ω|.
- At 2,500 rpm (15°/ms), a ±1° budget allows δω_side ≤ 0.26°/ms, which is ≤0.52° of out-of-plane rotation error over 2 ms.
- At 1,500 rpm the budget falls to 0.31°. **Low-spin drivers are the hardest case** for spin axis, and they again call for a long time baseline.

**Geometry note: what the side camera actually sees.** With the unit beside the ball and looking across the target line, the backspin axis points roughly at the camera. So **backspin is in-plane image rotation** (easiest; this matches the SkyTrak teardown, "backspin = counterclockwise rotation", [GSF](https://golfsimulatorforum.com/forum/skytrak/360729-reveal-the-secrets-of-skytrak-in-the-dark)). **Sidespin and rifle spin are out-of-plane** and need sphere back-projection.

**Perspective must be corrected.** As the ball moves Δx across the FOV at Z = 450 mm, the line of sight swings atan(Δx/Z): 6.3° for 50 mm, 12.5° for 100 mm, 31° for 270 mm [calc]. That is comparable to the entire 15°/ms driver spin signal, so it must be removed using the measured 3D ball position. This is one reason accurate 3D (stereo) matters for spin, not only for horizontal launch angle (HLA).

### 1.5 Launch angles, speed, depth / stereo

**Vertical launch angle (in-image).** σ ≈ √2·σ_pos / B.
- With a ball-center fit of 0.2 px (0.055 mm) over B = 200 mm: σ ≈ **0.02°** [calc].
- So the real error budget is set by **device leveling** (an IMU is needed; ±0.1° class) and calibration, not by pixels.

**Horizontal launch angle (depth axis for a side-of-ball unit).** ±0.5° over 200 mm needs per-point depth σ_Z ≲ 1.2 mm.

*Mono, from apparent ball size* (PiTrac's method, where "ball size changes mostly with Z" ([Hackaday](https://hackaday.io/project/195042-pitrac-the-diy-golf-launch-monitor))): σ_Z = Z·σ_d / d.
- With d = 155 px: σ_d = 0.2 px gives 0.58 mm, and a realistic σ_d = 0.5 px gives 1.45 mm, so **HLA σ ≈ 0.59°** [calc].
- That is marginal, and it is sensitive to edge bias that changes with illumination across the FOV.

*Stereo:* σ_Z = Z² · σ_disp / (f_px · B) [calc, Z = 450 mm, f_px = 1638]:

| Baseline B | σ_disp 0.1 px | 0.25 px | 0.5 px |
|---|---|---|---|
| 40 mm | 0.31 mm | 0.77 mm | 1.55 mm |
| 60 mm | 0.21 mm | 0.52 mm | 1.03 mm |
| 100 mm | 0.12 mm | 0.31 mm | 0.62 mm |

With B = 60–100 mm and σ_disp ≈ 0.25 px, σ_Z ≈ 0.3–0.5 mm, so **HLA σ ≈ 0.1–0.2°** [calc]. This also covers the club-face needs in §1.7. Practical stereo requirements:
- **Mechanical stability.** A 0.01° relative camera rotation creates a 0.29 px disparity bias, about 0.6 mm at 450 mm [calc]. Most of that is common-mode and cancels in angles, but scale and impact-location accuracy still need a rigid optical bench plus online self-calibration on the teed ball (PiTrac already has auto-calibration, [docs](https://docs.pitrac.org/)).
- **Alignment.** HLA is only as good as the unit's aim at the target. That needs an alignment procedure (camera view of the target, or an app-assisted method).

**Ball speed.** σ_v/v = √2·σ_pos/Δx ≈ 0.04% over 200 mm. Strobe timing jitter in the ns range from an MCU or FPGA is negligible. **±0.2 mph is easily reachable** [calc].

### 1.6 Photon budget and sunlight (the outdoor problem, quantified)

**Signal per pixel:**

e⁻ = ρ·T·E / (4N²) · A_px · t · QE / (hc/λ)

with ball reflectance ρ ≈ 0.8, optics T = 0.9, f/1.8, and t = 5 µs [calc]:

| Sensor @ λ | QE assumed | e⁻ per (W/m²) on ball | Irradiance needed for 1,000 e⁻ |
|---|---|---|---|
| IMX296 @ 940 nm | 0.12 [est.] | 1.88 | **533 W/m²** |
| IMX296 @ 850 nm | 0.25 [est.] | 3.54 | 283 W/m² |
| IMX900 @ 940 nm | 0.24 [est.: Sony claims about 2× NIR vs IMX296 at 850 nm, [Sony](https://www.sony-semicon.com/en/products/is/industry/gs/imx900.html)] | 1.60 | 626 W/m² |
| IMX287 @ 940 nm (6.9 µm) | 0.12 [est.] | 7.51 | **133 W/m²** |

QE context:
- Silicon QE is "typically 50% to 100% higher at 850nm than at 940nm" ([Lumileds WP35](https://lumileds.com/wp-content/uploads/files/WP35.pdf)).
- A distributor sheet gives the OG02B1B as 114 ke⁻/(µW·cm⁻²·s) at 850 nm and 54 at 940 nm ([Sunnywale](https://en.sunnywale.com/show-75-24356-1.html)). That works out to roughly 30% and 13% QE [est.].

**Target: about 1,000 e⁻.** Dimple contrast is perhaps 10–20%, so texture SNR ≈ 3–6 per pixel before aggregation.

**Strobe sizing** [calc]:
- The SFH 4727AS A01 (940 nm) gives 1.48 W/sr typ. at 1.5 A / 100 µs, and is rated for 5 A pulses, ≤450 µs, D ≤ 0.005 ([datasheet](https://www.mouser.com/datasheet/2/588/SFH_4727AS_A01_EN-3560414.pdf)).
- Assume about 4.4 W/sr at 5 A [est.: sub-linear scaling]. That gives 21.7 W/m² per LED on-axis at 0.45 m.
- **About 24 LEDs** are needed for the IMX296 case, and about 6 for IMX287.
- Electrical: 24 × 5 A × 3.3 V ≈ **400 W peak, 2 mJ per 5 µs flash**. A 470 µF / 24 V reservoir holds 135 mJ, enough for a dozens-of-flash burst [calc].
- Sanity check against prior art: Acushnet's fitting-monitor strobe uses a **24-LED** array ([US12382156](https://patents.google.com/patent/US12382156B2/en)), and PiTrac uses 10 LEDs with longer pulses.

**Sunlight in band** (computed from ASTM G173 global tilt, [data](https://raw.githubusercontent.com/pvlib/pvlib-python/main/pvlib/data/ASTMG173.csv)) [calc]:

| Filter | 850 nm center | 940 nm center |
|---|---|---|
| 10 nm FWHM | 9.6 W/m² | **3.05 W/m²** |
| 20 nm | 19.5 | 6.1 |
| 30 nm | 29.5 | 11.1 |
| 50 nm | 48.2 | **22.2** |

At 940 nm the band holds less than half the solar energy of 850 nm, which agrees with Lumileds: "a dip in the 920nm to 960nm region, where the solar IR levels are less than half compared to 850nm" ([WP35](https://lumileds.com/wp-content/uploads/files/WP35.pdf)).

**Sun vs. strobe on an IMX296 at 940 nm** [calc] (strobe signal = 1,000 e⁻):

| Exposure | Sun e⁻ (50 nm filter) | Sun e⁻ (10 nm filter) | Verdict |
|---|---|---|---|
| **5 µs gated to strobe** | **42 (4%)** | 6 (0.6%) | ✅ works in full sun |
| 1 ms open (multi-strobe frame) | 8,336 (8×) | 1,145 (1.1×) | ❌ fails; likely saturates |
| 3 ms open | 25,000 | 3,436 | ❌ |

**Conclusions:**
- (a) **Gating each image is mandatory.**
- (b) Once images are gated, a 30–50 nm LED-matched filter is enough. LED FWHM is about 50 nm at 940 nm, and LED wavelength drifts 0.29 nm/°C vs 0.07 nm/°C for VCSELs, whose FWHM is 0.8 nm ([WP35](https://lumileds.com/wp-content/uploads/files/WP35.pdf)).
- (c) **940 nm gives about 4.5× more sun margin than 850 nm** for about 2× more LED power. We pick 940 nm (it is also invisible to the golfer) and keep 850 nm as the fallback if photon-starved.
- (d) VCSEL plus a 10 nm filter is the upgrade path if we ever need longer exposures.

**Remaining outdoor failure modes to design for:**
- Specular sun glints on the glossy ball and on chrome clubs. These are point-like and saturating, so mask them as outliers.
- The sun in or near the lens FOV. Use a hood, and orientation guidance in the app.
- **Global-shutter parasitic light sensitivity (PLS).** The storage node keeps collecting stray sunlight during the ms-long readout. Check the PLS spec, where Pregius S is strong.
- Any optical break-beam trigger, which sunlight blinds unless it is modulated.
- Auto-exposure on any continuously running "watch" camera.

### 1.7 Club metrics requirements [calc]

- **Club speed** (58 m/s): ≥2 club images within about 150 mm before impact, so Δt ≤ about 1.3 ms. Position σ of about 0.1 mm over 100 mm gives about 0.1% speed accuracy.
- **Attack angle** (vertical): in-image from a side-of-ball unit. Easy.
- **Path** (horizontal): needs depth. ±0.5° over 100 mm of travel needs σ_Z ≈ 0.6 mm per point. Stereo can do this (§1.5).
- **Face angle ±0.5°.** Over a 100 mm face width, 0.5° is a heel-to-toe depth difference of only **0.87 mm**. Per-point σ_Z of 0.2 / 0.35 / 0.6 mm gives σ_face of 0.16° / 0.28° / 0.49° [calc]. Two things make this hard:
  - **Face closure rate.** Drivers close at roughly 1,500–3,000°/s near impact [est.: typical range of Foresight's "closure rate" metric], so a **1 ms timing error means 1.5–3° of face error**. We need club samples within about ±0.2 ms of impact, or a smooth rotation fit through several pre-impact samples, plus impact time from back-extrapolating the ball. Rapsodo gets impact time to about 0.1 ms this way ([US11583746](https://patents.google.com/patent/US11583746B2/en)).
  - **Face curvature.** Bulge changes the face normal by about 2° per 10 mm on an 11-inch radius (same patent), so "face angle" has to be defined at the impact point.
- **Dynamic loft / spin loft:** the face line in profile is visible in the side view, so this is mostly in-image.
- **Impact location (±2–3 mm useful):** intersection of the ball center at separation with the fitted face model.
- **Viewing geometry problem:** a camera directly across from the golfer sees the face nearly edge-on (toe view). Shifting the cameras about 100–200 mm *forward* of the ball and yawing them back 15–30° makes the face visible. This is presumably why Foresight's face fiducials are readable at all. A wider stereo baseline also helps.

---

## 2. Architectures used in industry

### 2.1 Taxonomy

| Approach | How motion is sampled | Examples | Outdoor | Cost |
|---|---|---|---|---|
| **Single/dual low-speed camera + IR strobe, multi-exposure in one frame** | Long shutter, 2+ µs strobes produce 2+ ball images in one frame | SkyTrak (orig.) teardown: "not high speed. Just cheap imagers… IR strobes fired at a very precise time", laser-curtain trigger ([GSF](https://golfsimulatorforum.com/forum/skytrak/360729-reveal-the-secrets-of-skytrak-in-the-dark)); PiTrac (2× IMX296, about 3,000 "effective fps", [Hackaday](https://hackaday.io/project/195042-pitrac-the-diy-golf-launch-monitor)); Acushnet (two flashes per shutter, [US12382156](https://patents.google.com/patent/US12382156B2/en)) | ❌ unless gated | Lowest |
| **High-speed ROI video, stereo** | 500–1,000+ fps on small ROIs, ROI moved predictively | Strokeplay: 1,000 fps, 320×240 ROI on a 1280×1024 sensor, FPGA prediction ([US10564250](https://patents.google.com/patent/US10564250B2/en)); Wang et al. 810 fps stereo ([TIM 2018](https://www.researchgate.net/publication/327922724_Tracking_a_Golf_Ball_With_High-Speed_Stereo_Vision_System)) | ✅ if each frame is strobe-gated | Medium |
| **Stereo / tri / quad "ultra-high-speed" with own LEDs per camera** | Hundreds of images in the first 30 cm | Foresight GC3 (3 cams, "triscopic") / Bushnell Launch Pro (same hardware), GCQuad (4 cams, "each … has its own LED light source", 10,000 fps, custom fish-eye) ([Golf.com](https://golf.com/gear/how-it-works-foresight-sports-gcquad-launch-monitor/), [Golf Digest](https://www.golfdigest.com/story/foresights-gcquad-launch-monitor-expands-to-four-cameras-wider-view-20-times-the-information), [Top Shelf](https://topshelfgolf.com/blogs/golf/bushnell-launch-pro-vs-foresight-gc3)) | ✅ (Foresight units are used on ranges) | High |
| **Camera + radar hybrids** | Cameras for ball/spin, radar for club or flight | SkyTrak+ (dual Doppler for sticker-free club data, [SkyTrak](https://www.skytrakgolf.com/pages/technology), [Friendly Golfer](https://friendlygolfer.com/skytrak-plus-review/)); Rapsodo MLM2PRO (2 cams + radar, spin only with RPT marked balls, [Rapsodo FAQ](https://rapsodo.com/pages/frequently-asked-golf-questions-faq)) | ✅ | Low–Med |
| **Event cameras** | Asynchronous per-pixel events | Research only: Nakabayashi CVPRW 2024 (synthetic, up to 500 rps), Gossard 2024 table tennis | (research) | — |

### 2.2 What specific companies do (public information)

**Foresight Sports / Bushnell**
- Lineage: the Wintriss patents ([US7324663](https://patents.google.com/patent/US7324663B2/en), "Expired – Lifetime, 2025-08-07"; [EP1509781B1](https://patents.google.com/patent/EP1509781B1/en), whose preferred embodiment is a *single* camera taking 2+ high-resolution images).
- **New GC2 (announced Oct 1 2026):** 2 cameras, ball data only, $1,699 ([Foresight](https://www.foresightsports.com/pages/gc2), [FirstCallGolf](https://www.firstcallgolf.com/industry-news/release/2026-10-01/foresight-sports-unveils-gc2-launch-monitor-incredible-accuracy-at-entry-level-price)). This sits right in our price band.
- **GC3 / Launch Pro:** 3 cameras, $5,999, ball data markerless, club data needs **1 sticker** ([Foresight GC3](https://www.foresightsports.com/products/gc3), [support](https://support.foresightsports.com/gc3-club-feature-addon)).
- **GCQuad / QuadMAX / Falcon / GCHawk:** 4 cameras with **4-dot photoluminescent fiducials** for face angle, impact location and closure rate ([Foresight help](https://help.foresightsports.com/hc/en-us/articles/4408197030035-How-to-Apply-and-Maintain-Club-Markers-for-Foresight-Sports-Devices), [Golf.com](https://golf.com/gear/rory-sabbatini-foresight-gcquad-launch-monitor-dq/)).
- **Spin method:** "spherical correlation" of the dimple pattern across the image set ([Foresight EU](https://foresightsports.eu/launch-monitors/gcquad/)).
- **Club method:** a stereoscopic, marker-based club patent ([US20130190098A1](https://patents.google.com/patent/US20130190098A1/en)).

**Uneekor**
- **EYE MINI ($2,999, portable, indoor/outdoor):** 2 high-speed IR cameras; Dimple Optix gives markerless ball data; club stickers "recommended"; **no face angle or impact point** ([Uneekor](https://uneekor.com/en-us/products/eye-mini-standalone)).
- **EYE MINI LITE:** "1.3 Megapixel, Monochrome, CMOS × 2EA", which gives a sensor-class hint ([spec PDF](https://download.uneekor.com/docs/EYE_MINI_LITE_Overview.pdf)).
- **XO2 (overhead, 3 cams):** impact point needs bar and dot stickers ([manual](https://download.uneekor.com/docs/EYEXO2_Manual.pdf)).
- **EYE XR (overhead, 2 cams, "Club AI", no stickers):** measures speed and path; face angle is computed from a formula ([PlayBetter](https://www.playbetter.com/blogs/golf-simulator-reviews/first-look-uneekor-eye-xr-overhead-launch-monitor), [Uneekor XR](https://uneekor.com/en-us/products/eye-xr-standalone)).

**Square Golf**
- **Original:** IR high-speed camera; *spin measured only with marked balls* and otherwise "estimated" from club data; indoor only ([Plugged In Golf](https://pluggedingolf.com/square-golf-launch-monitor-review/), [GolfWRX](https://forums.golfwrx.com/topic/2021896-square-golf-launch-monitor/)).
- **Omni (2026, $1,599, our most direct competitor):** **4 IR cameras stacked vertically**; any ball for ball data; claims to work in direct sunlight; club and impact data need face and shaft stickers; testers saw *outdoor spin less consistent in bright sun* ([GolfOnline](https://www.golfonline.co.uk/square-golf-omni-launch-monitor-review), [PlayBetter](https://www.playbetter.com/products/square-golf-omni-indoor-outdoor-launch-monitor), [NCG](https://www.nationalclubgolfer.com/reviews/launch-monitors/square-golf-omni-launch-monitor-review/)).
- Inference [est.]: stacking 4 cameras vertically is consistent with two vertical stereo pairs that are time-staggered or have different roles. This is Architecture A below.

**Garmin Approach R50 ($4,999):** 3 cameras, purely photometric, measured spin with any ball, club data with stickers ([Garmin](https://www.garmin.com/en-US/newsroom/press-release/outdoor/meet-the-garmin-approach-r50-the-only-portable-golf-launch-monitor-with-a-built-in-simulator/)).

**SkyTrak+:** an improved photometric camera plus dual Doppler radar for "Club Head Speed… Face Angle… Dynamic Loft without reflective stickers" ([SkyTrak](https://www.skytrakgolf.com/pages/technology)). This is the only sub-$3k sticker-free club data, and it comes from radar, not vision.

**Rapsodo:** spin needs RPT marked balls ([FAQ](https://rapsodo.com/pages/frequently-asked-golf-questions-faq)). However, Rapsodo's patent ([US11583746](https://patents.google.com/patent/US11583746B2/en)) describes a fast low-resolution stereo pair for impact plus a slow high-resolution pair, a radar trigger, FPGA synchronization, and **markerless club pose by fitting a 3D club model to stereo silhouettes, <1° RMS**.

### 2.3 Baseline geometry: inline vs. staggered vs. vertical (engineering rationale)

**Horizontal (inline) baseline.** The epipolar lines run parallel to the ball's travel. Two problems follow:
- In a multi-exposure frame, *several ball images lie on the same epipolar line*, so correspondence becomes ambiguous.
- Disparity is measured on the left and right ball edges, which are exactly the edges motion blur degrades.

**Vertical baseline.** The epipolar lines run perpendicular to travel:
- Every ball image has a unique match.
- Disparity uses the top and bottom edges, which stay sharp under x-blur.
- The unit stays narrow (a tall "tower" that fits a portable, tripod-mounted product).

Square Omni's vertical stack fits this reasoning. **Recommendation: vertical baseline, 60–100 mm.**

**Staggered / triangular (3–4 cameras).** This setup:
- gives two independent baselines, so there is no degenerate direction for club edges such as the shaft, leading edge and top-line, which have all orientations;
- adds redundancy against occlusion;
- adds time diversity if the cameras fire at different instants.

This is the GC3/GCQuad direction. A third camera mainly pays for itself in club-pose robustness.

### 2.4 Multi-exposure strobe vs. high-fps video

| | Multi-exposure in one frame | High-fps ROI video | **Quad-shutter (IMX900)** |
|---|---|---|---|
| Sensor cost | Lowest (60 fps parts) | High-speed parts (IMX273/287) | Mid |
| Data rate | Tiny | 0.5 GB/s per camera (1456×320 at 1 kfps, 8-bit = 3.7 Gbit/s) [calc] | Tiny (4 images per frame) |
| Outdoor | ❌ (integrates sun over ms) | ✅ (gate each frame) | ✅ (gate each phase) |
| Overlapping ball images | Problem at low speed (PiTrac uses variable gaps to avoid it) | None | None (separate phase images) |
| Pre-impact club frames | Needs a predictive trigger | Ring buffer, retroactive | Needs a predictive trigger, or a 2nd frame |

### 2.5 Illumination and beating the sun (summary of §1.6)

- **Global shutter is mandatory.** Rolling shutter skews a 90 m/s ball.
- **Gate exposure to the strobe** (3–5 µs). Short pulses also shrink sun-integrated noise; Lumileds: "the amount of collected sunlight is proportional to the duration of the burst" ([WP35](https://lumileds.com/wp-content/uploads/files/WP35.pdf)).
- **940 nm with a 30–50 nm bandpass filter.** Filtering removes "90–95%" of the roughly 1,000 W/m² of full sun (WP35); our G173 integration says about 97.8% for a 50 nm band at 940 nm.
- **High peak power at low duty.** LED pulsed ratings use D ≤ 0.5%, which is exactly a 5 µs pulse at 1 kHz ([SFH 4727AS A01](https://www.mouser.com/datasheet/2/588/SFH_4727AS_A01_EN-3560414.pdf)).
- **Optional ambient frame** (an unlit exposure right after) for background subtraction.
- **Grazing light angles** (LEDs 20–40° off the optical axis) bring out dimple shading. Coaxial light flattens it.
- **Eye safety:** a 400 W-peak IR array at about 1 m from the golfer needs an IEC 62471 (LED) analysis, or IEC 60825-1 if we use VCSELs or lasers. VCSELs are Class IV-capable and "need additional safety measures" (WP35). Budget a diffuser and an interlock.

---

## 3. Markerless spin measurement

### 3.1 Prior art

**Academic, golf**
- **Imai, Kagami, Hashimoto, "Estimation of a large relative rotation between two images of a fast spinning marker-less golf ball," IEEE/SICE SII 2016** ([IEEE](https://ieeexplore.ieee.org/document/7844057/)).
  - Input: two consecutive IR frames at 1 ms, up to 60° of rotation.
  - Method: align dimple *centers* to narrow candidate poses, then choose the pose that best matches dimple *edge pixels*. It relies on "slight irregularity" of the dimple layout.
  - Result: **99% success, 0.5 s per estimate.**
  - Follow-up: Gabor-filter edge detection for dimples ([Kagami lab list](https://sites.google.com/view/kagami-lab-tohoku-u/members/kagami/publications)).
- **RoboCup:** spin estimated from dimple-induced blur texture using co-occurrence matrices ([Springer 2015](https://link.springer.com/chapter/10.1007/978-3-319-18615-3_42)). This is a low-fps fallback idea.

**Patents, golf**
- **Foresight "spherical correlation"** of dimples across GCQuad image sets ([Foresight EU](https://foresightsports.eu/launch-monitors/gcquad/)).
- **US12401909 (Leary)** ([patent](https://patents.google.com/patent/US12401909B2/en)): Gabor filter plus binary threshold; back-project image 1 onto a hemisphere; brute-force X/Y/Z rotations (hundreds); re-project and compare with image 2. It also covers variable strobe gaps and **ratio matching** to identify which pulse produced which ball image. Its hardware example is the Pi GS camera, a 6 mm lens, an ≥50 W 850 nm LED array, and 10–20 µs pulses, i.e. the PiTrac design. This is a FTO flag (§7).
- **Strokeplay US10564250:** dimples are "analyzed by an image processing method" but the method is not disclosed ([patent](https://patents.google.com/patent/US10564250B2/en)).
- **Other spin patents found (owner not verified this session):**
  - "Estimating spin rate and axis of a ball using deep learning": CNN plus FC head that outputs spin and *confidence*; features can be "a dot, scratch, dimple or seam" ([US 12582870](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12582870))
  - "Spin calculation method for golf ball moving by being hit" ([US 12599828](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12599828))
  - "Determination of spin rate and spin axis of a ball in flight" ([US 12685898](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12685898))
  - "Ball spin rate measurement system" ([US 11083951](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11083951))
  - marking-based spin ([US11673029](https://patents.google.com/patent/US11673029))

**Other sports (methods transfer)**
- **Baseball, markerless:** spin rate from the periodicity of similar ball images, axis from 3D rigid registration ([ResearchGate](https://www.researchgate.net/publication/314252590_Automatic_spin_measurements_for_pitched_Baseballs_via_consumer-grade_high-speed_cameras); open-source [SpinTracker](https://github.com/TakashiIjiri/SpinTracker_Python)).
- **Baseball, deep learning:** ResNet–LSTM trained end-to-end at 960 fps, validated against TrackMan ([SPIE 2025](https://proceedings.spiedigitallibrary.org/conference-proceedings-of-spie/14072/1407230/Joint-markerless-estimation-of-ball-spin-axis-and-rotation-speed/10.1117/12.3102472.full)).
- **Event cameras:**
  - Nakabayashi et al., contrast maximization, ball-agnostic, up to 500 rps on synthetic data ([CVPRW 2024](https://openaccess.thecvf.com/content/CVPR2024W/CVsports/papers/Nakabayashi_Event-based_Ball_Spin_Estimation_in_Sports_CVPRW_2024_paper.pdf)).
  - Gossard et al., table tennis logo, 10.7 rps / 32.9° errors ([arXiv 2404.09870](https://arxiv.org/abs/2404.09870)).
  - A 2026 ResNet-18 spin-vector-plus-variance regressor with 8.8% magnitude and 6.4° axis error, 3 ms latency ([arXiv 2606.26780](https://arxiv.org/html/2606.26780v1)). This paper also restates the frame-camera Nyquist and aliasing limit.
- **Table tennis, sim-to-real from broadcast video** ([Kienzle CVPRW 2025](https://openaccess.thecvf.com/content/CVPR2025W/CVSPORTS/papers/Kienzle_Towards_Ball_Spin_and_Trajectory_Analysis_in_Table_Tennis_Broadcast_CVPRW_2025_paper.pdf)). This validates the synthetic-training strategy.

### 3.2 Recommended spin pipeline (where a software-strong team wins)

1. **Ball geometry:** sub-pixel circle fit on each gated image, plus a stereo 3D center and a known radius. This removes the radius and depth ambiguity that PiTrac calls its main bottleneck ([Hackaday](https://hackaday.io/project/195042-pitrac-the-diy-golf-launch-monitor)).
2. **Photometric normalization:** a flat-field and shading model for each LED geometry, then local-contrast and Gabor band-pass filtering at the dimple scale (as in Imai and US12401909). Mask specular glints, especially sun glints outdoors.
3. **Sphere unwrapping:** back-project each image onto the sphere using the calibrated camera and the 3D center. This also removes the perspective "parallax rotation" of up to 31° (§1.4).
4. **Coarse rotation (global, robust):** pick one of these, using non-uniform Δt to reject aliases:
   - dimple-center point sets with RANSAC on SO(3) (Imai);
   - SO(3) cross-correlation via spherical harmonics (SOFT-style FFT);
   - a learned descriptor network.
5. **Fine joint refinement:** direct photometric alignment of *all* images jointly under a constant-ω model (plus a small spin-decay term), with Gauss–Newton on SO(3). Use any logo or print opportunistically as extra high-contrast features, but never depend on it: "any ball" includes logos on the hidden hemisphere and plain range balls.
6. **Learned prior / verifier:**
   - Train a CNN on **synthetic renders** of scanned dimple patterns (many ball models, wear, scuffs, logos) under our exact IR lighting, across the 1.5–12k rpm and full-axis range.
   - Output ω and a confidence value (as in US 12582870).
   - Use it to initialize step 5 and to flag low-confidence shots instead of reporting a guess.
7. **Ground truth data engine:** marked balls with a high-speed reference camera, plus a borrowed or rented GCQuad, to collect thousands of labeled shots. Do this indoors first, then outdoors.

**Requirements this pipeline places on hardware:**
- ≥80–100 px ball diameter (≥7–10 px per dimple)
- ≤5 µs gated exposures
- ≥4 images over ≥2–3 ms (with ≥1 pair ≤1.25 ms apart)
- known Δt to sub-µs
- stereo 3D position

---

## 4. Markerless club measurement

### 4.1 State of the art (October 2026)

- **No shipping camera monitor reports *measured* face angle or impact location without stickers.** The evidence is in §0.5 and §2.2. The sticker-free options get there other ways:
  - SkyTrak+ uses radar.
  - Uneekor EYE XR estimates face angle by formula.
- **Rapsodo US11583746** ([patent](https://patents.google.com/patent/US11583746B2/en)):
  - Scan the user's club head once (about 3 s of rotation under structured light) to get a sub-mm 3D model.
  - At impact, fit the model to stereo silhouettes and the hosel–ferrule shaft segment.
  - Result: **<1° RMS, lie within 1°**.
  - With a shaft phase-pattern sticker: FFT registration at 0.1 px gives about 0.5–1° face orientation.
  - Impact time is extrapolated from ball speed to about 0.1 ms.
- **Hosel localization:** the contour-width jump between shaft and head ([US11229824](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11229824); owner unverified, Korean prior art cited).
- **Leading-edge contour plus lie correction** gives face angle ([US10213645](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10213645)).
- **Face normal from a reference pose and rotation** ([KR101525411B1](https://patents.google.com/patent/KR101525411B1/ko)).
- **Foresight's 4-dot geometry** shows which points define the face plane. Toe-top and toe-bottom spread defines the plane; toe and heel define lie and center ([US8951138](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8951138)). Our keypoint set should mirror it: heel, toe, top-line, leading edge, and groove ends.

### 4.2 Recommended approach

1. **Geometry:** cameras offset forward of the ball and yawed back (§1.7), vertical stereo, plus an optional 3rd camera with a horizontal offset.
2. **Club model:**
   - Default: a parametric head template per club category (driver, fairway, hybrid, iron, wedge, putter).
   - Better: a one-time *passive* "show the club to the camera" calibration, i.e. a multi-view reconstruction, as Rapsodo does with structured light. Our strobes could project a simple pattern through a cheap DOE [est.].
3. **Detection:** a keypoint and edge network trained on synthetic renders of hundreds of club CAD-like models with domain randomization (IR reflectance, scratches, glare), fine-tuned on real data. Keypoints: heel, toe, top-line endpoints, leading-edge endpoints, hosel, crown–face boundary, and **iron grooves**. Grooves are natural fiducial lines that give face orientation directly on irons.
4. **Pose:** stereo PnP initialization, then refine by minimizing silhouette, edge-distance and keypoint reprojection error across all views and all pre-impact samples, under a smooth SE(3) motion model (constant-acceleration translation, constant-rate rotation). This estimates closure rate and interpolates the pose to the impact time t₀ derived from the ball.
5. **Impact location:** the ball center at t₀ projected onto the fitted face (bulge and roll modeled). Cross-check with gear-effect physics (ball HLA and spin axis vs. path and face). Physics-based cross-checks double as a "measured vs. inferred" confidence flag.
6. **Ground truth:** collect data with Foresight 4-dot stickers on a GCQuad or QuadMAX *as the reference* while our unit ignores the stickers. Mask them in our images, or use IR-invisible markers in a separate wavelength band. This is the fastest path to a labeled dataset.
7. **Fallback (honest labeling):** if markerless face error exceeds about 1°, report face angle as *derived* from D-plane physics (start line ≈ 0.75–0.85 face + remainder path [est.]) and say so in the UI.

**Expected markerless accuracy** [est.]:

| Metric | Expected | Basis |
|---|---|---|
| Club speed, attack angle | ±1 mph / ±0.5° | easy |
| Path | ±0.5–1° | |
| Dynamic loft | ±1° | |
| Face angle | ±0.7–1.5° | needs ≥2–3 pre-impact samples within about 0.5 ms; Rapsodo's <1° RMS is the existence proof |
| Impact location | ±3–5 mm | |

---

## 5. Components shortlist (October 2026)

### 5.1 Global-shutter sensors

| Sensor | Res / pixel | Max fps (full) | ROI / fast modes | NIR | Module price | Fit |
|---|---|---|---|---|---|---|
| **Sony IMX296** (Pregius gen2, standard speed) | 1456×1088, 3.45 µm, 1/2.9″ | 60 | 720×540 at about 203 fps; 128×96 at about 535 fps on Pi ([RPi forum](https://forums.raspberrypi.com/viewtopic.php?t=348642&start=25)); Jetson driver 1280×720 at 90 ([GitHub](https://github.com/peclatj/jetson-orin-nano-devkit-imx296-rpi-global-shutter)). Line time about 15 µs [calc] | moderate | Arducam mono MIPI **$64.99** ([Arducam](https://www.arducam.com/1-58mp-imx296-mono-global-shutter-camera-module-with-m12-lens-for-raspberry-pi.html)); Pi GS cam about $50 ([PiTrac](https://hackaday.io/project/195042-pitrac-the-diy-golf-launch-monitor)); USB3 $219.99 ([Arducam](https://www.arducam.com/arducam-1-58mp-imx296-color-global-shutter-usb-3-0-camera-module.html)) | Gated snapshot (Arch A). Too slow for ROI video |
| **Sony IMX273** (gen2 high speed) | 1456×1088, 3.45 µm | 276 (8-bit) / 226.5 (10-bit) ([VA Imaging](https://va-imaging.com/en-us/blogs/camera-image-sensors/cameras-with-sony-imx273-sensor-specs-prices-life-cycle), [LUCID](https://thinklucid.com/tech-briefs/sony-4th-generation-pregius-s/)) | about 3.3 µs per line, so about 1,000 fps at about 300 rows [calc, est.]; multi-ROI ([IMVE](https://www.imveurope.com/press-releases/imx273-and-imx287)) | moderate | MIPI module not verified [est. $150–300 single] | ROI ring buffer (Arch C) |
| **Sony IMX287** | 728×544, **6.9 µm** | 523.5 (8-bit) / 436.9 (10-bit) ([FRAMOS](https://framos.com/products/sensors/area-sensors/imx287llr-c-19038/)) | higher with ROI | big pixels, about 4× photons | not verified | Photon-cheap high-speed. Ball only 78 px over 400 mm, so use a narrower FOV |
| **Sony IMX900** (Pregius S, stacked) | 2064×1552, 2.25 µm, 1/3.1″, M12-friendly | 125 / 117 / 72 (8/10/12-bit) ([Sony](https://www.sony-semicon.com/en/products/is/industry/gs/imx900.html)) | **Quad Shutter: 4 independently timed exposures per frame, "µs intervals, effective 100,000 fps"**; custom ROI up to 838 fps (custom firmware) ([e-con](https://www.e-consystems.com/usb-cameras/sony-imx900-global-shutter-hdr-monochrome-camera.asp)); XTRIG1/2 inputs ([FRAMOS](https://docs.framos.com/en/latest/FSMEcosystem/ProductDocumentation/FSMGO/IMX900.html)) | "nearly double" vs IMX296 at 850 nm | e-con MIPI or USB **$249** single ([e-con](https://www.e-consystems.com/camera-modules/3mp-sony-pregius-imx900-global-shutter-camera-module.asp)); FRAMOS FSM:GO (Jetson, i.MX8MP, Pi 5) | **Primary candidate (Arch B)** |
| **onsemi AR0234** | 1920×1200, 3 µm | 120 | 1280×720 at 120 (Pi module) | moderate | e-con USB **$99 volume / $184 single** ([e-con](https://www.e-consystems.com/industrial-cameras/ar0234-usb3-global-shutter-camera.asp)); Arducam MIPI **$109.99** ([Arducam](https://www.arducam.com/arducam-full-hd-color-global-shutter-camera-for-raspberry-pi-2-3mp-ar0234-wide-angle-pivariety-camera-module-b0353.html)), Jetson version with external trigger ([Arducam](https://www.arducam.com/arducam-2-3mp-ar0234-global-shutter-camera-for-nvidia-jetson.html)) | | Arch A alternative (more pixels) |
| **OmniVision OG02B1B / OG02B10** | 1600×1300, 3 µm | 60 | 640×480 at 180 (module) ([VisionMeta](https://www.visionmeta.com/product/2mp-og02b10-high-speed-motion-capture-camera-module-180fps/)) | about 13% QE at 940 nm [est. from [Sunnywale](https://en.sunnywale.com/show-75-24356-1.html)] | low-cost Chinese modules | Arch A cost-down |
| OmniVision OV9281 | 1280×800, 3 µm | 120 [est.] | — | — | about $30–40 modules [est., not verified] | Trigger / ball-watch cam |
| onsemi AR0144 / AR0145; OmniVision OG01A1B | about 1 MP class | — | — | — | not verified this session | Cost-down candidates; get quotes |
| onsemi AF0130 (Hyperlux ID) | depth-oriented GS sensor [est.] | — | — | — | not verified | Not recommended without datasheet review |
| Sony IMX992 | **SWIR InGaAs** (SenSWIR) [est.] | — | — | — | about $1k+ class [est.] | **Out of budget.** Silicon NIR is sufficient |
| Gpixel (GMAX / GSPRINT) | industrial high-speed | — | — | — | not verified | Industrial pricing; skip for consumer |

**Bare-sensor volume prices were not verified this session.** For BOM math I use custom sensor-board costs of **IMX296 board about $30 / $22, IMX900 board about $70 / $50, IMX273 board about $85 / $60 (1k / 10k)** [est.]. These are anchored on the retail module prices above. **Get quotes from Sony distributors (FRAMOS, Macnica, Arrow) and module houses (Arducam, Leopard, e-con, Vision Components).**

### 5.2 Optics and filters

- **M12 lenses:** 5–6 mm, f/1.8–2.0, 3 MP-rated, low distortion. PiTrac uses a 6 mm 3 MP lens ([parts list](https://docs.pitrac.org/hardware/parts-list/)). FRAMOS offers M12 lenses with 33°, 76° and 102° HFOV ([FRAMOS](https://docs.framos.com/en/latest/FSMEcosystem/ProductDocumentation/FSMGO/IMX900.html)). Budget $8–20 at 1k and $4–10 at 10k [est.].
- **Bandpass filters:**
  - Commonlands CBP940: T>90%, OD3, about 80 nm FWHM, **$9**; 10 nm FWHM OD4 version **$15**; can be glued onto their M12 lenses ([Commonlands](https://commonlands.com/products/940nm-bandpass-filter)).
  - MidOpt BN940: 928–955 nm, ≥85% T, **$114–293** depending on size ([FJW](https://fjwoptical.com/products/narrow-nir-bandpass-filter-928-955nm-midopt-bn940), [RMA](https://www.rmaelectronics.com/midwest-optical-bn940/)). This is a lab reference, not a production part.
  - In production, use a coated cover glass or window at about $1–4 [est.].
  - **Spec: a 940 nm center and 30–50 nm FWHM bandpass coating.** Use OD4 out of band, account for angle-of-incidence shift at the field edges, and include visible blocking.

### 5.3 IR emitters and drivers

**ams OSRAM SFH 4727AS / A01 (OSLON Black):**
- 950 / 940 nm; standard version 1,150 mW/sr typ. at 1 A.
- A01: 1,480 mW/sr at 1.5 A / 100 µs; 5 A pulse test point; t_p ≤ 450 µs, D ≤ 0.005; 10 / 15 ns rise / fall.
- Price: **$1.30–1.90 at reel quantities** ([datasheet](https://look.ams-osram.com/m/4a33854827e56279/original/SFH-4727AS.pdf), [A01 datasheet](https://www.mouser.com/datasheet/2/588/SFH_4727AS_A01_EN-3560414.pdf), [DigiKey](https://www.digikey.com/en/products/detail/ams-osram-usa-inc/SFH-4727AS-A01/16399983), [Octopart](https://octopart.com/sfh4727as-osram-90619970)).
- ⚠ **Both are marked "not for new designs."** Ask ams OSRAM for the successor part.

**Other emitters:**
- PiTrac uses Vishay VSMA1085400 ([parts list](https://docs.pitrac.org/hardware/parts-list/)).
- **VCSEL arrays** (0.8 nm FWHM, 0.07 nm/°C) allow 10 nm filters, but raise laser-safety obligations ([WP35](https://lumileds.com/wp-content/uploads/files/WP35.pdf)).

**µs pulse driver:**
- Use low-side switching of LED strings from a 24–48 V capacitor bank.
- **TI LMG1020** gate driver: 7 A / 5 A, 1 ns minimum pulse, 2.5 ns propagation, 400 ps edges, built for LiDAR / ToF ([TI](https://www.ti.com/product/LMG1020)).
- Pair it with logic-level MOSFETs or GaN FETs, for example EPC's LiDAR parts (not price-verified).
- PiTrac's lower-cost version uses IRLU024N MOSFETs with an MCP1407 driver ([parts list](https://docs.pitrac.org/hardware/parts-list/)).
- Add current-sense resistors and a hardware **pulse-width watchdog** (a monostable or comparator) so that a software bug can never hold the LEDs on. PiTrac redesigned its circuit for exactly this reason ([PiTrac](https://hackaday.io/project/195042-pitrac-the-diy-golf-launch-monitor)).

**Timing:** a small MCU or FPGA generates camera triggers and strobes with ns jitter (for example an RP2350 PIO or an STM32 timer, about $1–3 [est.]). Linux user space should never be in the timing loop. PiTrac and US12401909 bit-bang I²C or SPI to get ≤10 µs pulses, which works but is fragile.

### 5.4 Edge compute (2026 prices, after the DRAM shock)

**Context:** DRAM prices have pushed SBC and SOM costs up sharply in 2026. Raspberry Pi made three to four price increases, citing "a seven-fold increase… in the price of LPDDR4" ([CNX](https://www.cnx-software.com/2026/04/01/raspberry-pi-4-3gb-launched-for-83-75-further-price-increases-announced-across-the-board-for-4gb-ram-hardware/), [Tom's HW](https://www.tomshardware.com/raspberry-pi/component-shortages-drive-raspberry-pi-prices-up-by-up-to-23-percent-escalating-lpddr4-lpddr5-costs-trigger-the-third-price-hike-of-the-year), [Geerling](https://www.jeffgeerling.com/blog/2026/dram-pricing-is-killing-the-hobbyist-sbc-market/)). **Choose the smallest RAM that works (4 GB).**

| Option | Price | Camera I/O | Notes |
|---|---|---|---|
| **NVIDIA Jetson Orin Nano 8 GB** | **$399 at 1ku** (up from $299, July 2026); 4 GB $349 ([CNX](https://www.cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101/)) | multi-CSI; e-con and FRAMOS IMX900 drivers exist | Best GPU and tooling. Takes most of the BOM |
| **Rockchip RK3588 SOM** | $115 at 1k / $101 at 10k tier listing ([Made-in-China](https://szpretech.en.made-in-china.com/product/zfvpiSJVhCkP/China-Rockchip-8nm-Rk3588-Som3588-Core-Module-Android-Linux-Support-Octa-Core-6-Tops-Npu-450-Gflops-GPU-Som.html)); Radxa CM5 8 GB launched at $75–89 and now lists at $119 (sold out) ([Radxa](https://radxa.com/blog/CM5-Official-Announcement/), [ALLNET](https://shop.allnetchina.cn/products/radxa-cm5-1)). Expect 1.5–2× due to DRAM [est.] | multiple MIPI CSI (count to confirm per SOM) | 6 TOPS NPU; good value; BSP quality varies |
| **Qualcomm QCS6490** | Thundercomm C6490P SOM **$286.52 at 1, $219.80 at 500+, $149.18 at 30k+** ([Arrow](https://www.arrow.com/en/products/c6490p-u8a-3690000-qcs6490/thundercomm)); Radxa Dragon Q6A SBC from $59.50 (4 GB) ([CNX](https://www.cnx-software.com/2025/10/27/radxa-dragon-q6a-a-qualcomm-qcs6490-edge-ai-sbc-with-gbe-wifi-6-three-camera-connectors/)); RUBIK Pi 3 $179 ([Hackster](https://www.hackster.io/news/thundercomm-s-rubik-pi-3-edge-ai-board-developed-with-qualcomm-goes-on-sale-for-179-529c9a8384c2)) | up to 5 CSI (TurboX); Q6A has 3 CSI, 4 cameras ([Radxa docs](https://docs.radxa.com/en/dragon/q6a/hardware-use/mipi-csi)) | 12 TOPS; Wi-Fi 6E; phone-grade power; long-term supply |
| Raspberry Pi 5 / CM5 + Hailo-8L | Pi 5 4 GB about $110, 8 GB about $175 after the April 2026 increases [calc from [Phoronix](https://www.phoronix.com/news/Raspberry-Pi-2026-DRAM-Pricing), [Tom's HW](https://www.tomshardware.com/raspberry-pi/component-shortages-drive-raspberry-pi-prices-up-by-up-to-23-percent-escalating-lpddr4-lpddr5-costs-trigger-the-third-price-hike-of-the-year)]; Hailo-8L M.2 $89–99 ([UP Shop](https://up-shop.org/default/hailo-8ltm-m-2-2230-a-e-key.html)); AI HAT+ 2 now $200 ([RPi](https://www.raspberrypi.com/products/ai-hat-plus-2/)) | 2× 4-lane CSI | PiTrac reference; great for the prototype phase |
| NXP i.MX8M Plus | not verified this session [est. about $60–120 SOM] | 2 CSI, 2 ISPs | FRAMOS IMX900 support ([FRAMOS](https://docs.framos.com/en/latest/FSMEcosystem/ProductDocumentation/FSMGO/IMX900.html)); weak compute for heavy ML |
| AMD Kria K26 / Lattice CrossLink-NX or ECP5 | not verified [est. K26 about $250+; Lattice bridge FPGA about $10–30] | FPGA MIPI | Use only as a **capture bridge** for Arch C (ROI management, ring buffer, timestamps), as Strokeplay and Rapsodo do with FPGAs |

**Compute need:**
- Per shot: about 8–20 ROI images of about 256×256 px, SO(3) registration, plus a small CNN. That is about 50–300 ms on an A76 CPU plus NPU or GPU [est.].
- **NPU is not essential. CSI lane count and reliable raw capture are.**
- RK3588 or QCS6490 is the right class. Orin Nano only if we want GPU training and inference parity.

### 5.5 Trigger methods

| Method | Latency / issue | Verdict |
|---|---|---|
| IR break-beam / laser curtain (SkyTrak) | ball crosses about 50 mm ahead, about 0.55 ms at 90 m/s; **sunlight susceptible** unless modulated | OK indoors |
| **Audio / impact mic** (Acushnet patent) | sound travels 0.5 m in **1.46 ms**, by which time a driver ball has moved **131 mm** [calc]; noisy at ranges with adjacent bays | ❌ alone; OK as a veto |
| **Camera ROI "ball-watch"** (PiTrac cam1 at about 500 fps; US12401909 crops to under 100×100 at ≥250 fps) | detects ball motion within about 1–2 ms; cannot predict the club | ✅ for ball; misses pre-impact club |
| **mm-wave radar** (Rapsodo patent: swing start and club speed, triggers cameras; SkyTrak+) | predicts impact time tens of ms ahead; also gives a club-speed cross-check | ✅ best for pre-impact club frames; module price not verified [est. $8–20] |
| **Continuous ring buffer** (high-fps ROI, always strobing while armed) | no prediction needed, impact found retroactively; 5 µs at 1 kHz is 0.5% duty, inside LED ratings, about 2 W average [calc] | ✅ Arch C; best data |

---

## 6. Candidate reference architectures

All three share:
- 940 nm gated strobes (3–5 µs) with a hardware pulse watchdog;
- an MCU timing master;
- a 30–50 nm bandpass;
- a vertical stereo baseline of 60–100 mm, with cameras offset forward of the ball and yawed back about 20°;
- an IMU for leveling;
- target-alignment UX.

### Architecture A — "Gated Quad-Snapshot" (low risk, cheapest sensors)

**Design:**
- 4× IMX296 mono (or AR0234 or OG02B1B) as **two vertical stereo pairs**.
- Pair 1 fires at about t₀ + 0.6 ms, pair 2 at about t₀ + 2.0 ms. Each exposure is a single 4 µs strobe.
- One camera also runs a 128×96 ROI ball-watch at about 535 fps for triggering, plus an optional radar for a pre-impact club snapshot.
- **Indoors** (when ambient is low, detected automatically), each camera may add 2–3 extra strobes within its exposure, giving up to 8–12 ball images. That is the SkyTrak/PiTrac trick, used only when it is safe.

**Camera-subsystem BOM** [est.; sources in §5]:

| Item | @1k | @10k |
|---|---|---|
| 4× IMX296 sensor boards | $120 | $88 |
| 4× M12 lens + 940 nm filter | $60 | $36 |
| 24× 940 nm LEDs + optics | $46 | $34 |
| Strobe driver (FETs, LMG1020-class, boost, caps, watchdog) | $18 | $12 |
| Timing MCU + 60 GHz radar | $15 | $9 |
| Compute: RK3588 4–8 GB SOM | $150 | $115 |
| IR window, hood, thermal | $15 | $10 |
| **Total** | **≈ $424** | **≈ $304** |

**Expected accuracy (outdoor-capable mode)** [est.]:
- Ball speed ±0.5 mph
- Vertical launch ±0.2°
- HLA ±0.3–0.5°
- Spin ±5–8% from 2 time samples (better indoors with multi-strobe)
- Spin axis ±2–3°
- Club speed, attack angle and path OK if a radar-timed pre-impact snapshot is used
- Face angle about ±1.5° markerless (few samples)

**Limitations:**
- Only 2 gated time samples outdoors, so spin and spin axis are marginal on low-spin drivers.
- 4 cameras need 4 CSI ports (QCS6490 has 5; on RK3588, verify).
- The trigger-to-pair-1 timing has to absorb the ball-watch latency.

### Architecture B — "IMX900 Quad-Shutter Stereo" (recommended)

**Design:**
- 2× IMX900 mono in vertical stereo (an optional 3rd camera offset horizontally for club robustness).
- **Frame 1:** 4 gated phases at about t₀ − 0.4, −0.15 ms (club, radar-timed) and +0.5, +1.1 ms (ball).
- **Frame 2:** 4 phases at about +1.8, +2.4, +3.0, +3.6 ms if the sensor allows back-to-back quad frames. Otherwise use the next frame about 8 ms later for trajectory only.
- Each phase is 1032×776 (0.39 mm/px, 110 px ball, about 10 px per dimple).
- Full-resolution frames (2064×1552) are available at address for calibration, ball placement and club scanning.

**Camera-subsystem BOM** [est.]:

| Item | @1k | @10k |
|---|---|---|
| 2× IMX900 sensor boards | $140 | $100 |
| 2× lens + filter | $36 | $20 |
| 32× LEDs + optics (more energy for 4 phases × 2 views) | $61 | $44 |
| Driver | $22 | $15 |
| MCU + radar | $15 | $9 |
| RK3588 SOM (or QCS6490 at $210 / $165) | $150 | $115 |
| Mechanical | $15 | $10 |
| **Total** | **≈ $439** | **≈ $313** |
| *3rd camera option* | *+$88* | *+$60* |

**Expected accuracy** [est.]:
- Ball speed ±0.3 mph; vertical launch ±0.1°; HLA ±0.2°
- **Spin ±3–4% / ±60–100 rpm** (4–8 samples over about 3 ms)
- Spin axis ±1.5–2°
- Club: face angle ±1° markerless target, path ±0.7°, impact location ±4 mm
- Works in full sun (§1.6)

**Risks / unknowns, to resolve before committing:**
1. Confirm in the Sony datasheet (NDA via FRAMOS or e-con) that each quad phase's exposure start and width can be **externally triggered** at µs resolution, and get the minimum inter-phase spacing. e-con says firmware customization is required.
2. Each phase uses 1/4 of the pixels, so check aliasing of fine dimple edges.
3. Find the minimum time between consecutive quad frames.
4. Measure QE at 940 nm.
5. Measure PLS under sun.

Fallback if (1) fails: use the IMX900's custom-ROI high-fps mode (up to 838 fps, [e-con](https://www.e-consystems.com/usb-cameras/sony-imx900-global-shutter-hdr-monochrome-camera.asp)), which turns this into Architecture C on the same hardware.

### Architecture C — "High-speed ROI ring-buffer trinocular" (premium data)

**Design:**
- 3× IMX273 (or IMX287 with a narrower FOV, or IMX900 in ROI mode) streaming 1456×300 ROIs at about 800–1,000 fps.
- Every frame is gated to a 4 µs strobe, continuously while armed (0.4–0.5% duty).
- A Lattice bridge FPGA timestamps frames and keeps a 0.5 s DDR ring buffer (about 0.5 GB/s per camera [calc]). Impact is found retroactively.
- Output per camera: about 6–10 ball images plus 3–6 club images.

**Camera-subsystem BOM** [est.]:

| Item | @1k | @10k |
|---|---|---|
| 3× IMX273 boards | $255 | $180 |
| Lenses + filters | $45 | $27 |
| 40 LEDs + optics + driver | $104 | $74 |
| FPGA bridge + DDR | $35 | $25 |
| MCU | $8 | $5 |
| Jetson Orin Nano 8 GB | $399 | about $360 [est.] |
| Mechanical / thermal | $25 | $15 |
| **Total** | **≈ $871** | **≈ $686** |
| With RK3588 instead of Jetson | ≈ $622 | ≈ $441 |

**Expected accuracy** [est.]:
- Spin ±2–3%, spin axis ±1–1.5°
- Face angle ±0.7°, impact location ±3 mm
- Best club data (closure rate available)

**Limitations:**
- Exceeds the camera-subsystem budget at 1k units.
- Higher power and heat (continuous strobing plus 3 Gbit/s+ capture), which hurts battery portability.
- Raw 1 kfps capture through SoC ISPs is a driver risk; hence the FPGA.
- FTO overlap with Strokeplay's ROI-prediction patent (§7) if we also move ROIs predictively.

### Comparison

| | A Quad-Snapshot | **B IMX900 Quad-Shutter** | C ROI ring buffer |
|---|---|---|---|
| Camera-subsystem BOM 1k / 10k [est.] | $424 / $304 | **$439 / $313** | $622–871 / $441–686 |
| Outdoor full sun | ✅ (2 samples) | ✅ (4–8 samples) | ✅ (many samples) |
| Spin (driver) | ±5–8% | ±3–4% | ±2–3% |
| Markerless face angle | ±1.5° | ±1° | ±0.7° |
| Tech risk | Low | **Medium (sensor-mode confirmation)** | Medium-high (data path) |
| Power / portability | Best | Good | Worst |

**Plan:**
1. Prototype on Pi 5 + 2–4 IMX296 (cheap, PiTrac-adjacent) with our own gated strobe board to validate the §1.6 photon and sun math outdoors in the first 6–8 weeks.
2. In parallel, get IMX900 quad-shutter samples and documentation from e-con or FRAMOS.
3. Down-select to B or A by month 3.

---

## 7. IP / freedom-to-operate flags (not legal advice)

- **Expired:** the Wintriss/Foresight core "flight parameter measurement" patent [US7324663](https://patents.google.com/patent/US7324663B2/en) expired in 2025. The basic multi-image photometric approach is now freer to use.
- **Active and relevant:**
  - **Strokeplay** [US10564250](https://patents.google.com/patent/US10564250B2/en): ROI high-fps with predicted second capture area. Expires about 2037.
  - **Acushnet** [US12382156](https://patents.google.com/patent/US12382156B2/en): LED strobe with steerable wedges.
  - **Rapsodo** [US11583746](https://patents.google.com/patent/US11583746B2/en): club 3D model fit, scanning, shaft phase marker.
  - **Leary** [US12401909](https://patents.google.com/patent/US12401909B2/en): variable-interval strobe with ratio matching; Gabor plus hemisphere spin search. ⚠ This overlaps PiTrac's published methods. GPL code does **not** automatically give us freedom to commercialize a patented method, and PiTrac is GPLv2 with separately licensed ML models ([GitHub](https://github.com/PiTracLM/PiTrac)). **Do not copy PiTrac code into a proprietary product.**
  - Foresight club measurement [US20130190098A1](https://patents.google.com/patent/US20130190098A1/en) (marker-based).
  - The deep-learning spin patent [US 12582870](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12582870).
- **Action:** commission an FTO search on Golfzon, Creatz, Uneekor, Square Golf, Foresight (WAWGD), Rapsodo, Trackman and Garmin before the architecture freeze. Searches this session did not surface Golfzon or Creatz markerless-club patents.

---

## 8. Open items / not verified in this session

The web-search budget was exhausted mid-research. These need follow-up quotes or datasheets:

1. Bare-sensor prices at 1k and 10k for IMX296, IMX273, IMX287 and IMX900; Sony QE curves at 940 nm. All are under NDA via FRAMOS, Macnica or Arrow.
2. IMX900 quad-shutter external-trigger semantics and the minimum inter-quad-frame interval. This is the critical item for Architecture B.
3. OV9281, AR0144/AR0145, OG01A1B and AF0130 module prices and specs; confirm the IMX992 (SWIR) exclusion.
4. Volume prices for NXP i.MX8M Plus SOMs, AMD Kria K26, Lattice CrossLink-NX/ECP5, and 60 GHz radar modules (Infineon BGT60 / TI IWR6243-class).
5. The SFH 4727AS successor part (NRND), and the radiant intensity actually achieved at 5 A / 4 µs. Bench-measure it.
6. Typical driver face closure rate (I used about 1,500–3,000°/s) and D-plane coefficients. Pull these from fitting literature or Foresight data.
7. Bench validation of σθ (per-image orientation error) on real dimpled balls under our strobe geometry. Every spin-accuracy number above scales with it.

---

## Sources (consolidated)

**Products / companies:**
- Foresight: [GCQuad EU](https://foresightsports.eu/launch-monitors/gcquad/), [Golf.com how-it-works](https://golf.com/gear/how-it-works-foresight-sports-gcquad-launch-monitor/), [Golf Digest](https://www.golfdigest.com/story/foresights-gcquad-launch-monitor-expands-to-four-cameras-wider-view-20-times-the-information), [club markers](https://help.foresightsports.com/hc/en-us/articles/4408197030035-How-to-Apply-and-Maintain-Club-Markers-for-Foresight-Sports-Devices), [QuadMAX manual](https://support.foresightsports.com/quadmax-user-manual), [GC3](https://www.foresightsports.com/products/gc3), [GC3 club add-on](https://support.foresightsports.com/gc3-club-feature-addon), [GC2 2026](https://www.foresightsports.com/pages/gc2), [FirstCallGolf GC2](https://www.firstcallgolf.com/industry-news/release/2026-10-01/foresight-sports-unveils-gc2-launch-monitor-incredible-accuracy-at-entry-level-price), [Sabbatini stickers](https://golf.com/gear/rory-sabbatini-foresight-gcquad-launch-monitor-dq/), [GCHawk review](https://homeperformancelab.com/foresight-gchawk-review/), [Launch Pro vs GC3](https://topshelfgolf.com/blogs/golf/bushnell-launch-pro-vs-foresight-gc3)
- SkyTrak: [technology](https://www.skytrakgolf.com/pages/technology), [teardown](https://golfsimulatorforum.com/forum/skytrak/360729-reveal-the-secrets-of-skytrak-in-the-dark), [Friendly Golfer](https://friendlygolfer.com/skytrak-plus-review/), [Golfible](https://golfible.com/skytrak-plus-review/)
- Uneekor: [EYE MINI](https://uneekor.com/en-us/products/eye-mini-standalone), [MINI LITE spec](https://download.uneekor.com/docs/EYE_MINI_LITE_Overview.pdf), [XO2 manual](https://download.uneekor.com/docs/EYEXO2_Manual.pdf), [XO2](https://uneekor.com/en-us/products/eye-xo2-standalone), [XR](https://uneekor.com/en-us/products/eye-xr-standalone), [PlayBetter XR](https://www.playbetter.com/blogs/golf-simulator-reviews/first-look-uneekor-eye-xr-overhead-launch-monitor)
- Square Golf: [Plugged In Golf](https://pluggedingolf.com/square-golf-launch-monitor-review/), [SimSpace](https://simspacegolf.com/products/square-golf-launch-monitor), [GolfWRX](https://forums.golfwrx.com/topic/2021896-square-golf-launch-monitor/), [Omni GolfOnline](https://www.golfonline.co.uk/square-golf-omni-launch-monitor-review), [Omni NCG](https://www.nationalclubgolfer.com/reviews/launch-monitors/square-golf-omni-launch-monitor-review/), [Omni PlayBetter](https://www.playbetter.com/products/square-golf-omni-indoor-outdoor-launch-monitor), [CenterFace](https://centerfacegolf.com/square-omni-launch-monitor-review/)
- Garmin and Rapsodo: [Garmin R50](https://www.garmin.com/en-US/newsroom/press-release/outdoor/meet-the-garmin-approach-r50-the-only-portable-golf-launch-monitor-with-a-built-in-simulator/), [Rapsodo FAQ](https://rapsodo.com/pages/frequently-asked-golf-questions-faq)
- PiTrac: [GitHub](https://github.com/PiTracLM/PiTrac), [Hackaday](https://hackaday.io/project/195042-pitrac-the-diy-golf-launch-monitor), [docs](https://docs.pitrac.org/), [parts](https://docs.pitrac.org/hardware/parts-list/)

**Patents:** [US7324663](https://patents.google.com/patent/US7324663B2/en), [EP1509781B1](https://patents.google.com/patent/EP1509781B1/en), [US20130190098A1](https://patents.google.com/patent/US20130190098A1/en), [US8951138](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8951138), [US10564250 Strokeplay](https://patents.google.com/patent/US10564250B2/en), [US11583746 Rapsodo](https://patents.google.com/patent/US11583746B2/en), [US12401909](https://patents.google.com/patent/US12401909B2/en), [US12382156 Acushnet](https://patents.google.com/patent/US12382156B2/en), [US11229824](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11229824), [US10213645](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10213645), [KR101525411B1](https://patents.google.com/patent/KR101525411B1/ko), [US12582870](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12582870), [US12599828](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12599828), [US12685898](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12685898), [US11083951](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11083951), [US11673029](https://patents.google.com/patent/US11673029)

**Papers:** [Imai et al. SII 2016](https://ieeexplore.ieee.org/document/7844057/), [Kagami publications](https://sites.google.com/view/kagami-lab-tohoku-u/members/kagami/publications), [M-sequence multi-exposure TT spin](https://www.tandfonline.com/doi/full/10.1080/18824889.2025.2466881), [Wang et al. stereo golf](https://www.researchgate.net/publication/327922724_Tracking_a_Golf_Ball_With_High-Speed_Stereo_Vision_System), [RoboCup dimple blur](https://link.springer.com/chapter/10.1007/978-3-319-18615-3_42), [baseball markerless](https://www.researchgate.net/publication/314252590_Automatic_spin_measurements_for_pitched_Baseballs_via_consumer-grade_high-speed_cameras), [SpinTracker](https://github.com/TakashiIjiri/SpinTracker_Python), [SPIE ResNet-LSTM](https://proceedings.spiedigitallibrary.org/conference-proceedings-of-spie/14072/1407230/Joint-markerless-estimation-of-ball-spin-axis-and-rotation-speed/10.1117/12.3102472.full), [Nakabayashi CVPRW24](https://openaccess.thecvf.com/content/CVPR2024W/CVsports/papers/Nakabayashi_Event-based_Ball_Spin_Estimation_in_Sports_CVPRW_2024_paper.pdf), [Gossard arXiv 2404.09870](https://arxiv.org/abs/2404.09870), [Event gaze 2026](https://arxiv.org/html/2606.26780v1), [Kienzle CVPRW25](https://openaccess.thecvf.com/content/CVPR2025W/CVSPORTS/papers/Kienzle_Towards_Ball_Spin_and_Trajectory_Analysis_in_Table_Tennis_Broadcast_CVPRW_2025_paper.pdf)

**Components:**
- Sensors: [Sony IMX900](https://www.sony-semicon.com/en/products/is/industry/gs/imx900.html), [e-con IMX900 module](https://www.e-consystems.com/camera-modules/3mp-sony-pregius-imx900-global-shutter-camera-module.asp), [e-con IMX900 USB](https://www.e-consystems.com/usb-cameras/sony-imx900-global-shutter-hdr-monochrome-camera.asp), [FRAMOS IMX900](https://docs.framos.com/en/latest/FSMEcosystem/ProductDocumentation/FSMGO/IMX900.html), [FRAMOS IMX287](https://framos.com/products/sensors/area-sensors/imx287llr-c-19038/), [LUCID Pregius](https://thinklucid.com/tech-briefs/sony-4th-generation-pregius-s/), [VA Imaging IMX273](https://va-imaging.com/en-us/blogs/camera-image-sensors/cameras-with-sony-imx273-sensor-specs-prices-life-cycle), [IMVE IMX273/287](https://www.imveurope.com/press-releases/imx273-and-imx287), [Arducam IMX296 mono](https://www.arducam.com/1-58mp-imx296-mono-global-shutter-camera-module-with-m12-lens-for-raspberry-pi.html), [Arducam IMX296 OAK](https://www.arducam.com/product/1-58mp-imx296-color-global-shutter-camera-module-for-depthai-oak/), [RPi GS ROI fps](https://forums.raspberrypi.com/viewtopic.php?t=348642&start=25), [IMX296 Jetson driver](https://github.com/peclatj/jetson-orin-nano-devkit-imx296-rpi-global-shutter), [e-con AR0234](https://www.e-consystems.com/industrial-cameras/ar0234-usb3-global-shutter-camera.asp), [Arducam AR0234](https://www.arducam.com/arducam-full-hd-color-global-shutter-camera-for-raspberry-pi-2-3mp-ar0234-wide-angle-pivariety-camera-module-b0353.html), [OVT OG02B1B](https://www.ovt.com/products/og02b1b/), [OG02B1B brief](https://www.ovt.com/wp-content/uploads/2024/09/OG02B1B-PB-v1.5-WEB.pdf), [Sunnywale OG02B1B](https://en.sunnywale.com/show-75-24356-1.html), [VisionMeta OG02B10](https://www.visionmeta.com/product/2mp-og02b10-high-speed-motion-capture-camera-module-180fps/)
- Illumination and optics: [SFH 4727AS DS](https://look.ams-osram.com/m/4a33854827e56279/original/SFH-4727AS.pdf), [SFH 4727AS A01 DS](https://www.mouser.com/datasheet/2/588/SFH_4727AS_A01_EN-3560414.pdf), [DigiKey A01](https://www.digikey.com/en/products/detail/ams-osram-usa-inc/SFH-4727AS-A01/16399983), [Octopart](https://octopart.com/sfh4727as-osram-90619970), [Lumileds WP35](https://lumileds.com/wp-content/uploads/files/WP35.pdf), [ASTM G173 data (pvlib)](https://raw.githubusercontent.com/pvlib/pvlib-python/main/pvlib/data/ASTMG173.csv), [Commonlands 940 BP](https://commonlands.com/products/940nm-bandpass-filter), [MidOpt BN940 FJW](https://fjwoptical.com/products/narrow-nir-bandpass-filter-928-955nm-midopt-bn940), [RMA BN940](https://www.rmaelectronics.com/midwest-optical-bn940/), [TI LMG1020](https://www.ti.com/product/LMG1020)
- Compute: [Jetson price increase](https://www.cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101/), [RPi DRAM pricing](https://www.phoronix.com/news/Raspberry-Pi-2026-DRAM-Pricing), [Tom's HW Pi prices](https://www.tomshardware.com/raspberry-pi/component-shortages-drive-raspberry-pi-prices-up-by-up-to-23-percent-escalating-lpddr4-lpddr5-costs-trigger-the-third-price-hike-of-the-year), [CNX Pi April 2026](https://www.cnx-software.com/2026/04/01/raspberry-pi-4-3gb-launched-for-83-75-further-price-increases-announced-across-the-board-for-4gb-ram-hardware/), [Geerling DRAM](https://www.jeffgeerling.com/blog/2026/dram-pricing-is-killing-the-hobbyist-sbc-market/), [RK3588 tiered](https://szpretech.en.made-in-china.com/product/zfvpiSJVhCkP/China-Rockchip-8nm-Rk3588-Som3588-Core-Module-Android-Linux-Support-Octa-Core-6-Tops-Npu-450-Gflops-GPU-Som.html), [Radxa CM5](https://radxa.com/blog/CM5-Official-Announcement/), [ALLNET CM5](https://shop.allnetchina.cn/products/radxa-cm5-1), [Thundercomm C6490P Arrow](https://www.arrow.com/en/products/c6490p-u8a-3690000-qcs6490/thundercomm), [Dragon Q6A](https://www.cnx-software.com/2025/10/27/radxa-dragon-q6a-a-qualcomm-qcs6490-edge-ai-sbc-with-gbe-wifi-6-three-camera-connectors/), [Q6A CSI](https://docs.radxa.com/en/dragon/q6a/hardware-use/mipi-csi), [RUBIK Pi 3](https://www.hackster.io/news/thundercomm-s-rubik-pi-3-edge-ai-board-developed-with-qualcomm-goes-on-sale-for-179-529c9a8384c2), [Hailo-8L](https://up-shop.org/default/hailo-8ltm-m-2-2230-a-e-key.html), [AI HAT+ 2](https://www.raspberrypi.com/products/ai-hat-plus-2/)
