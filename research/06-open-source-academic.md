# 06 — Open-Source, DIY, Academic and Simulator-Ecosystem Prior Art

*Research date: 7 October 2026. Scope: prior art that can speed up building a markerless, TrackMan-class, subscription-free launch monitor with an open simulator API.*

> **Method and limitations.** All GitHub facts (stars, licenses, last push, file contents) come from live `gh` API calls on 2026-10-07. The web-search budget for this session ran out after the first query, and parallel research subagents were unavailable. Everything else was checked by fetching known URLs directly: vendor sites, docs.pitrac.org, gsprogolf.com, Awesome Golf docs, arXiv abstract pages, and Crossref DOI records. A few academic references come from background knowledge and could not be re-verified this session. They are marked **[unverified this session]**. Patent numbers are deliberately left out because Google Patents blocked automated fetches. A targeted follow-up web-search pass is recommended for those items. It is listed in §8.

---

## 0. Executive summary (the decisions that matter)

1. **The two biggest open-source launch monitors are copyleft, and one has a poison-pill model license.**
   - **PiTrac** (camera + IR strobe) is **GPL-2.0-only**.
   - PiTrac's trained ML models (YOLO ball detector, spin predictor) and its training data sit under a separate **proprietary, non-commercial license**. That license explicitly reaches any "Commercial Offering" that "materially depends upon" the models.
   - **OpenFlight** (radar: OPS243-A + TI IWR6843) is **AGPL-3.0**.
   - We cannot ship code from either in a closed product. We *can* learn their architecture, constants and failure modes, and re-implement clean-room from published physics.
2. **Permissive building blocks exist for the integration layer and the ball-flight model:**
   - **libgspro**: MIT, a GSPro Open Connect server plus a 731-line protocol reference.
   - **flighthook / 10over / ironsight / allsquare**: Apache-2.0. Bridges, plus reverse-engineered R10, Mevo+ and Square protocols.
   - **Flight Relay Protocol (FRP)**: a CC0 open launch-monitor event standard.
   - **OpenFairway**: MIT golf physics with Penner bounce. Its provenance needs checking.
   - **cogsys-tuebingen/spindoe**: Apache-2.0 spin estimation, table tennis.
3. **Ball-flight model: write our own, from published coefficients.**
   - Use the quadratic Cd/Cl fit of **Ferguson, McNally & McPhee (2022)**, fitted on 1,040 measured shots. OpenFlight's TrackMan regression suite shows this form gets **~2.9 yd overall carry RMSE and ~1.5–3.2 ft apex error** against a TrackMan capture.
   - Add Reynolds-number dependence, following Nathan / Lyu, Kensrud & Smith (2018).
   - Add a Penner-style bounce and roll model.
   - Equations and published coefficients are not copyrightable, so the GPL/AGPL implementations are only an issue if we copy their code.
4. **Simulator integration is mostly open for ball data and gated by business deals for "native" listing.**
   - **GSPro Open Connect v1** is public: TCP 127.0.0.1:921, unframed JSON, no auth. We can ship day one. Users buy the GSPro "OpenAPI" license tier (GSPro is $250/yr for everyone).
   - Native GSPro listing (like "Nova by OpenLaunch", Garmin, Square, Bluetees) goes through business@gsprogolf.com.
   - **E6 Connect / TruGolf (TruSimAPI, TCP 2483)** uses a handshake/challenge-authentication flow. PiTrac ships the E6 response handler only as a **closed-source object file**, which strongly suggests TruGolf protocol details are under NDA. That needs a business deal.
   - **Awesome Golf** is partner-only.
   - **OpenGolfSim** has an open local TCP API (port 3111, newline-delimited JSON).
5. **No commercially usable labelled dataset of high-speed golf-ball images with ground-truth spin was found.**
   - GolfDB is CC BY-NC.
   - PiTrac's training data is proprietary.
   - Inrange's Kaggle data cannot be redistributed.
   - Plan to build our own: synthetic rendering plus a rig co-located with a TrackMan/GCQuad.
6. **Fastest path to a working prototype** (details in §7):
   - Hardware: IMX296 global-shutter cameras plus a pulsed IR strobe, the multi-exposure-in-one-frame trick PiTrac proved at roughly $50 per camera. Optionally add an OPS243-A radar for a fast, accurate ball/club-speed channel.
   - Software: a clean-room pipeline (Hough/ellipse detection, then our own detector, then a Gabor-dimple 3D-rotation search for spin, then a learned model trained on our own data).
   - Physics: our own Ferguson-based flight + Penner bounce model.
   - Outputs: GSPro Open Connect client, OpenGolfSim client and FRP WebSocket server from day one. Conformance-test against libgspro's 115 cases and 23 fixtures.

---

## 1. Open-source and DIY launch monitors

### 1.1 PiTrac — camera + IR strobe (the most relevant prior art)

| Item | Detail |
|---|---|
| Repo | https://github.com/PiTracLM/PiTrac. 426★, 73 forks, created 2024-12-17, last push 2026-10-05. Topics include `hacktoberfest`. No tagged releases. |
| Docs | https://docs.pitrac.org/ (last updated Apr 14 2026). Hackaday log: https://hackaday.io/project/195042-pitrac-the-diy-golf-launch-monitor |
| Lead | James Pilgrim (Verdant Consultants, LLC, per SPDX headers). Contributors include philtrick123, Jesse Hernandez and Mark Harman. Project started 2024-02-29. |
| License (code, docs, hardware) | **GPL-2.0-only** (SPDX `GPL-2.0-only` in each source file) |
| License (ML models + training data) | **Proprietary**: `LICENSE.MODEL.md` v1.1, August 2026 (https://github.com/PiTracLM/PiTrac/blob/main/LICENSE.MODEL.md). See below. |
| Other bundled licenses | `LICENSE.ED_LIB.md`: MIT, Cihan Topal 2019, the ellipse/edge-drawing library used for ball fitting. Also rpicam-apps and Shedskin notices. |
| Status | "Still a young project … basic features usually work reliably, but the current release needs polish" (docs home). Not sold commercially. Building one needs soldering, 3D printing and Linux compilation. |

**Hardware**, from https://docs.pitrac.org/hardware/cameras/:
- **Raspberry Pi 5 (8 GB)**, about US$134.50, the most expensive part. A single Pi 5 is now recommended; stereo may need two.
- **Two Sony IMX296 global-shutter cameras**: 1456×1088, 232 fps native, sensor 5.077 × 3.789 mm. Options:
  - **InnoMaker CAM-MIPI327RAW** (mono, trigger pins broken out)
  - **Raspberry Pi Global Shutter Camera** (color, about US$50). This one needs its IR-cut filter removed and a trigger-wire mod that includes removing an SMD resistor.
  - Rolling-shutter Pi cameras (OV5647, IMX219, IMX477) are deprecated. IMX708 is unsupported because it has no high-fps mode.
- **M12 lenses**: 6 mm (about 60° FOV) by default; 3.6 mm (about 90°) for tight spaces.
- **Near-IR strobe** LEDs driven from a small custom PCB, "a few dollars". The LED part and wavelength are not stated on the cameras page.
- Target BOM is under US$300; per Hackaday it is "over-budget by about a hundred dollars".

**How it works** (Hackaday log and docs):
- **Camera 1 (tee)** watches the teed ball in a tight loop at about 500 fps (cropped). When the ball moves, it fires a hardware sync line to Camera 2.
- **Camera 2 (flight)** takes one exposure while the IR strobe pulses several times. The result is several frozen ball images in one frame, about **3,000 "effective" fps** from a sub-$50 sensor. This is the key idea to reuse, and it is the same concept as Foresight GC2/GCQuad-style flash imaging.
- **Speed** comes from the displacement between strobe images. **HLA** comes from the change in apparent ball size, since Camera 2 sees the ball's depth movement from the side.
- **Spin** (source: `Software/LMSourceCode/ImageProcessing/ball_image_proc.cpp`, 4,410 lines):
  - Default `kSpinDetectionMethod = "ml"`: an ML spin predictor (`ml_assets/spin-predictor`).
  - Fallback is a classical pipeline: Gabor-filter the ball to isolate dimples (`ApplyGaborFilterToBall`, `ComputeGaborAccumulation`, with a white-pixel target of 38–44%), then a **coarse-to-fine 3D rotation search**.
  - The search projects ball image 1 onto a sphere, rotates it over a grid, re-projects, and compares against ball image 2 (`GetBallRotation`, `ComputeCandidateAngleImages`, `CompareRotationImage`). Search ranges: X −42..42° in 6° steps, Y −30..30° in 5° steps, Z −50..60° in 6° steps.
- **Ball detection**: OpenCV `HoughCircles` plus Fornaciari ellipse fitting. Newer builds use an NCNN-run YOLO detector (`ml_assets/yolo26-ball-detector`). The author calls Hough detection "a single point of failure that limits the system's reliability and accuracy".
- **Calibration**: ChArUco lens-distortion correction once per lens, then an auto-calibration of focal length and angles that must be redone if a camera moves. About 5–10 minutes per camera; "without calibration … completely wrong."
- **Outputs**: a web app, ActiveMQ/JMS, **GSPro Open Connect** (port 921) and **E6/TruGolf TruSimAPI** (port 2483). No club data is produced; the code sends ClubData as zeros.

**Accuracy**: no published numbers. The docs give "no numeric accuracy specifications". In March 2024 the author said high-speed driver performance was "only theoretical at this point". The author also notes that at Pi GS resolution "a one-pixel error could misplace the ball by several millimeters or more". The page says PiTrac is "very sensitive to large amounts of IR light", so it is **effectively indoor-only**. The default layout puts the unit in the ball's path ("he has hit it many times").

**The model license is the crux.** `LICENSE.MODEL.md` v1.1:
- Grants only personal, non-commercial use, on the user's own hardware, with PiTrac or a fork.
- Defines "Commercial Offering" to include anything that bundles, downloads, configures, or "**materially depends upon** the Model Materials".
- Reaches models present in *any revision in git history, any fork*, and any "converted, quantized … derived representation".
- Also covers **Training Materials** (datasets, images, labels, hyperparameters).
- Physical parts built from the GPL hardware designs may be sold *without* models.

**Implication:** a commercial product cannot use PiTrac's weights or training data at all. Using PiTrac code would make our entire linked program GPL-2.0. Treat PiTrac as a **reference architecture** only.

**Forks/derivatives:** **r87-e/LaunchTrac** (https://github.com/r87-e/LaunchTrac). 2★, GPL-2.0, Rust, last push 2026-04-15. A rewrite claiming "under $200 in parts", two GS cameras plus IR strobes, GSPro/E6/TruGolf output, synthetic test fixtures and 33 tests. Being GPL-2.0, it has the same constraint.

### 1.2 OpenFlight — Doppler radar (the most relevant radar prior art)

| Item | Detail |
|---|---|
| Repo | https://github.com/open-flight/openflight. **1,151★**, 135 forks, created 2025-12-08, pushed 2026-10-07 (very active). Docs: https://open-flight.github.io/openflight/ |
| License | **AGPL-3.0** (mobile app https://github.com/open-flight/openflight-mobile is GPL-3.0) |
| Hardware | **OmniPreSense OPS243-A** 24 GHz CW Doppler radar (~$249). Raspberry Pi 5. SparkFun SEN-14262 sound trigger. Optional **TI IWR6843LEVM** 60 GHz FMCW (~$150) for launch angle, direction and experimental club path; it needs **custom firmware** to expose the raw radar cube. Optional global-shutter camera. Deprecated: RFbeam K-LD7. Base build ~$534; with angle radar ~$684; everything ~$819. |
| Metrics | Ball speed 15–200 mph "±0.5%" (OPS243-A spec). Club speed, smash, launch angle (IWR6843). **Spin is experimental and not used for carry by default.** Carry from a ballistic model. |
| Signal chain | Sound trigger → OPS243 HOST_INT (~10 µs latency) → rolling-buffer dump of **4,096 I/Q samples at 30 ksps** (~136 ms around impact; supports ~208 mph) → FFT / multitaper. 24.125 GHz gives ~71.7 Hz of Doppler per mph. A DC mask (~15 mph) rejects body motion. |
| Spin | "Ungated multitaper estimator", constrained to 1,500–11,000 rpm, logged only. A "dechirped Doppler-sideband estimator" is in development (`scripts/analysis/replay_spin_dechirp.py`). The authors say "short indoor flight windows and multipath make individual readings unreliable." |
| Simulator | GSPro Open Connect codec (`src/openflight/gspro/`), a sim connector framework, cloud sync ("FlightWeb"). |

**What it teaches us:**
1. A $249 24 GHz module plus a sound trigger gets you trustworthy ball speed and club speed quickly. That is a useful fusion channel even for a camera product.
2. **Radar spin on short indoor flights is hard.** Commercial radar units (TrackMan, FlightScope) need a long flight or a high-SNR multi-antenna array. Our camera path should own spin.
3. Their engineering practice is excellent and copyable as *process*. Example: `tests/test_ballistics_trackman_regression.py` replays a committed TrackMan "Normalized" CSV and enforces a per-club RMSE budget that is "ratcheted down, never up".

### 1.3 Other DIY camera/radar projects

| Project | Link | ★ / last push | License | What it is | Usefulness |
|---|---|---|---|---|---|
| ronheywood/opencv | https://github.com/ronheywood/opencv | 39 / 2021 | MIT | Python OpenCV experiments: YOLOv3 "sports ball", HSV thresholding, Hough circles. Aimed at GC2-style flash imaging. | Low; early exploration |
| VGLALALA/GCFive | https://github.com/VGLALALA/GCFive | 4 / 2025-08 | MIT | HuaTeng Vision (Hikrobot-style MVS SDK) high-speed capture, YOLO ball detection, **Gabor + 3D rotation search spin** (same idea as PiTrac), and a trajectory "Python approximation of the Godot scripts from JaySimG". | Medium. Small permissive reference for the spin search. **Provenance risk**: JaySimG/OpenShotGolf is GPL-2.0, so a port may be a derivative work. |
| csoffa/golf-launchmonitor | https://github.com/csoffa/golf-launchmonitor | 7 / 2025 | none (all rights reserved) | Pi computer-vision LM build log | Inspiration only |
| thomasjhook/launch-monitor | https://github.com/thomasjhook/launch-monitor | 10 / 2025 | MIT | Pi 5 + IMX477 (rolling shutter) + **HB100-class 10.525 GHz** Doppler via MCP3008 ADC + TCRT5000 IR trigger, FFT ball speed | Low; hobby grade (10-bit ADC, rolling shutter) |
| tannu64/Golf-Launch-Monitor-Radar-DSP | https://github.com/tannu64/Golf-Launch-Monitor-Radar-DSP (+ `-DSP-Milestone2`) | 2–3 / 2025–26 | none | MATLAB DSP for **InnoSenT SMR333 24 GHz CW** radar: STFT, CFAR, Kalman, club/ball separation, "validate_against_trackman". Target ±1 mph vs TrackMan. Reads like a contracted milestone project. | Medium: algorithm outline for club/ball separation. No license, so ideas only. |
| jelis86/…Dimple-Pattern-Tracking_public | https://github.com/jelis86/Algorithm-for-Estimating-Golf-Ball-Spin-Using-Dimple-Pattern-Tracking_public | 0 / 2026-07 | none, code private | Describes a markerless spin pipeline: Hough → FAST-16 corners on dimples → 9×9 patch SSD matching → RANSAC rotation → spin axis | Useful *description* of a markerless feature-tracking alternative to rotation search |
| chase16647/golf-launch-monitor | https://github.com/chase16647/golf-launch-monitor | 0 / 2026-10 | none | iPhone 17 Pro 240 fps capture app + PWA + "tour-fitted" flight model. Author admits the native app was never run on a phone. | Shows the phone-LM direction; immature |
| alleexx/cam-putting-py | https://github.com/alleexx/cam-putting-py | 52 / 2025 | GPL-3.0 | Webcam putting: ball speed + HLA to GSPro | Shows putting via a cheap overhead/side cam is a solved hobby problem |

**"OpenLaunch"** is not an open-source project. GSPro's native list includes **"Nova by OpenLaunch"**, a commercial launch monitor (https://gsprogolf.com/). The vendor site could not be reached this session. Its relevance: a small, new LM maker obtained native GSPro listing, so a precedent exists.

### 1.4 Reverse-engineered commercial LMs and connectors (what they reveal)

| Device | Project(s) | License | Transport | Key findings |
|---|---|---|---|---|
| **Garmin Approach R10** | **mholow/gsp-r10-adapter** https://github.com/mholow/gsp-r10-adapter (93★, MIT, C#). **divotmaker/10over** https://github.com/divotmaker/10over (Apache-2.0, Rust crate `tenover`). travislang/gspro-garmin-connect-v2 https://github.com/travislang/gspro-garmin-connect-v2 (139★, no license, JS). Others per libgspro: "five independent bridges for the R10 alone". | MIT / Apache / none | BLE GATT, "GFDI" framing + **protobuf** (COBS + CRC16 utilities in gsp-r10-adapter). Service `6A4E3400-667B-11E3-949A-0800200C9A66`, measurement / control-point / status characteristics `…3401/3402/3403`. | Protobuf `BallMetrics` has `spin_calculation_type ∈ {RATIO, BALL_FLIGHT, OTHER, MEASURED}` and `golf_ball_type ∈ {UNKNOWN, CONVENTIONAL, MARKED}`. **The R10 often reports *estimated* spin, not measured spin.** That is a marketing point for us: measured markerless spin on every shot. `ClubMetrics`: head speed, face angle, path, attack angle. Second route: the R10 app's **"Play E6 Connect" mode** acts as a TruSimAPI client, and connectors pose as an E6 server to capture shots. |
| **Rapsodo MLM2PRO** | springbok/MLM2PRO-GSPro-Connector https://github.com/springbok/MLM2PRO-GSPro-Connector (97★, GPL-3.0, Python; OCR plus Mevo+). Duwaynef/MLM2PRO-BT-APP https://github.com/Duwaynef/MLM2PRO-BT-APP (26★, MIT, C#, direct BLE). rowengb/GSPro-MLM2PRO-OCR-Connector (23★, MIT, Tesseract OCR). | mixed | BLE, gated by a **Rapsodo cloud-issued third-party token**. The user must authorize "Awesome Golf" in the Rapsodo app, which writes a token to the device, and the connector needs a "Web API secret". | Shows a vendor **subscription lock enforced in device firmware via cloud tokens**: the kind of lock-in our "no subscription" positioning attacks. Early connectors simply OCR'd the vendor app's screen. |
| **FlightScope Mevo+ / Mevo Gen2** | **divotmaker/ironsight** https://github.com/divotmaker/ironsight (Apache-2.0) | Apache | Wi-Fi TCP. **Binary radar protocol on port 5100**; **"GVP" camera protocol on port 1258** (trigger, trajectory hints, ball-tracker results). | Mevo+ fuses radar with a camera channel on separate ports. Handshake, arming and keepalive state machine are documented in the crate. |
| **Square Golf Omni / Home** | divotmaker/allsquare (Apache-2.0, crate `allsquare`). chrisjack/SquareConnector (MIT). OpenGolfSim/ogs-plugin-square-omni. | Apache / MIT | BLE GATT | Budget camera LMs expose plain BLE. |
| **SkyTrak / SkyTrak+** | OpenSkyPlus https://github.com/OpenSkyPlus/OpenSkyPlus (10★, "other"). OpenSkyPlus2 (BepInEx v6 IL2CPP plugin into the Unity app). jperuggia/skytrack_gspro_connect. | various | Hooks into the vendor's Unity app | Fragile; breaks on app updates |
| **Uneekor, Foresight, Bushnell** | none open | — | Vendor-native integrations | libgspro: "Uneekor, Bushnell and Foresight's own software do NOT speak Open Connect … their connectors are closed." Uneekor is reachable only via shot-folder watching or OCR. |

**Legal note.** divotmaker's crates explicitly rely on **DMCA §1201(f)** (the interoperability exception) (https://www.law.cornell.edu/uscode/text/17/1201). We have no need to reverse-engineer competitors, but supporting *their* devices in our software would be a different product decision.

**Multi-device bridges (permissive, reusable):**
- **divotmaker/flighthook** https://github.com/divotmaker/flighthook. 12★, **Apache-2.0**, Rust, pushed 2026-10-07, "Beta 0.1.x". It connects Mevo+/Gen2, Square Omni, R10 and Uneekor (via an OpenConnect server) to GSPro, with a REST + WebSocket event bus and FRP on `ws://<host>:5880/frp`.
- **401Unauthorized/fairway-bridge** https://github.com/401Unauthorized/fairway-bridge (5★, Apache-2.0).
- **brettveenstra/gspro-bridge** (MIT).
- **kenjdavidson/gspro-connector** (MIT).
- **joebockhorst/gspro-connect** (CC0, Python).

---

## 2. Simulator ecosystem integration

### 2.1 GSPro — Open Connect v1 (open; ship on day one)

**Spec:** https://gsprogolf.com/GSProConnectV1.html

**Protocol:**
- **Transport:** TCP socket, GSPro listens on **127.0.0.1, port 0921**. No authentication. Remote LMs need a firewall rule or port forward.
- **Direction:** the LM is the *client*.
- **Root fields:** `DeviceID` (required, "unique per launch monitor / project type"; no registration), `Units` (default yards), `ShotNumber` (incremented by the LM), `APIversion` ("1").
- **`BallData`:** `Speed`, `SpinAxis`, `TotalSpin` (or `BackSpin` + `SideSpin`), `HLA`, `VLA`, optional `CarryDistance`.
- **`ClubData`:** `Speed`, `AngleOfAttack`, `FaceToTarget`, `Lie`, `Loft`, `Path`, `SpeedAtImpact`, `VerticalFaceImpact`, `HorizontalFaceImpact`, `ClosureRate`.
- **`ShotDataOptions`:** `ContainsBallData`, `ContainsClubData`, `LaunchMonitorIsReady`, `LaunchMonitorBallDetected`, `IsHeartBeat`.
- **Responses:** `200` = shot received; `201` = player info, `{"Code":201,"Message":"GSPro Player Information","Player":{"Handed":"RH","Club":"DR"}}`; `5xx` = failure.

A real client implementation, PiTrac's `gs_gspro_results.cpp` (GPL; quoted for protocol facts only):
```cpp
// Create a JSON object based on https://gsprogolf.com/GSProConnectV1.html
root.put("DeviceID", "PiTrac LM 0.1");  root.put("Units", "Yards");
root.put("ShotNumber", shot_number_);   root.put("APIversion", "1");
ball_data_child.put("Speed", ...); ("SpinAxis"); ("TotalSpin","0.0"); ("BackSpin"); ("SideSpin"); ("HLA"); ("VLA");
club_data_child: Speed, AngleOfAttack, FaceToTarget, Lie, Loft, Path, SpeedAtImpact,
                 VerticalFaceImpact, HorizontalFaceImpact, ClosureRate   (all "0.0" in PiTrac)
shot_data_options: ContainsBallData, ContainsClubData, LaunchMonitorIsReady,
                   LaunchMonitorBallDetected, IsHeartBeat
```

**Gotchas that are undocumented by GSPro and critical** (from **PinPoint-Golf/libgspro**'s `docs/protocol.md`, MIT, https://github.com/PinPoint-Golf/libgspro, which surveyed 16 real clients):
- **There is no framing.** There is no newline or length prefix; 13 of 16 clients send bare JSON objects and some send *indented* JSON. GSPro itself sometimes sends **two objects concatenated in one segment** (for example a 200 followed by a 201). Parse with a string-aware brace-depth counter. PiTrac's one-read-equals-one-message parser loses the connection when this happens.
- **Sign conventions** (inferred from clients): `SpinAxis` negative means tilted left (a draw for a right-hander). `HLA` positive means right of target.
- **Units:** clients send **mph** and **yards** under `"Yards"`. Whether `"Meters"` switches speeds to m/s is unknown.
- **201 messages** are unsolicited, sent on club change and after shots. They often include `DistanceToTarget` and sometimes `Surface`. **Club codes:** `DR, W2–W7, H2–H7, I1–I9, PW, GW, SW, LW, PT`. Use `PT` to switch the LM into putting mode.
- **A shot with `Speed: 0` resets GSPro's club selection.** Never send zero-speed shots; send a heartbeat instead.
- libgspro has **115 socket-free conformance cases and 23 byte-exact fixtures**. It is the ideal test harness for our client.

**Commercials** (https://gsprogolf.com/ FAQ):
- GSPro costs **$250/yr** (lifetime licenses are no longer sold) and runs on Windows only.
- **Native partners:** Uneekor (needs the Pro Package), FlightScope, Foresight/Bushnell (sold *through Foresight*, FSX required), Full Swing KIT, Garmin R10/R50, Rapsodo MLM2PRO (needs Premium), ProTee VX, GolfTrak, **Nova by OpenLaunch**, Square Home/Omni, VTrack, GolfJoy, Bluetees Rainmaker.
- **"Through OpenAPI" license** (same price): GolfIn Idra, NVisage, "Other (OpenAPI) for any other device or DIY connector".
- **Native integration:** "Want to officially integrate your hardware with GSPro? Reach out" → **business@gsprogolf.com**. No fees are published.
- **Takeaway:** we can sell from day one, with users choosing the OpenAPI license. A native listing (dedicated purchase link, connection guide in the KB at https://gspro.gitbook.io/gspro-knowledge-base) is a business negotiation, and Nova and Bluetees show small makers get there.

### 2.2 E6 Connect / TruGolf — TruSimAPI (business deal required)

- **Port 2483**, TCP. The LM is the *client*: PiTrac's config has `kE6ConnectAddress` = sim PC IP and `kE6ConnectPort` = 2483. In E6 you select **TruSimAPI** as the tracking system (https://docs.pitrac.org/software/simulator-integration/).
- **Message flow**, from gsp-r10-adapter (MIT), which poses as an E6 server to the R10:
  - JSON messages with `Type`: `Handshake` → `Challenge` → `Authentication` (`Success`) → `SetBallData` / `SetClubData` → shot → `Arm` → `ACK` with `SubType` → `Disconnect`.
  - The handshake carries `E6Version`, `ProtocolVersion`, `RequiredProtocolVersion` and `Challenge`.
  - The E6 side issues a **challenge** that the LM must answer.
- **Evidence the auth secret is private:**
  - PiTrac's `gs_e6_response.cpp` in the public repo is an **empty stub** that includes `<openssl/sha.h>`.
  - The real implementation is shipped as a prebuilt **`ClosedSourceObjectFiles/gs_e6_response.cpp.o`**, linked in by `create_closed_source_objects.sh`.
  - This is inside an otherwise GPL project. It strongly implies TruGolf supplied the challenge-response details under NDA or a partner agreement. That is an inference, not a published statement.
- PiTrac also ships `SimulatorAssets/TruGolf/TruSimAPICustomSettings.json`. It defines which stats E6 displays (Distance, Carry, LaunchAngle, BallSpeed, BackSpin, SideSpin, LaunchDirection, SmashFactor, ShotNumber) and the LM logo assets, installed under `c:/TruGolf/Tracking/TruSimAPI/Images/`.
- **Commercials:**
  - E6 Connect "pairs with 18+ Launch Monitors like Garmin, Rhapsodo, FlightScope" (https://trugolf.com/software/e6-connect/).
  - Tiers are Home (27 owned courses, PC or iOS) and Commercial Suite. **Prices are hidden behind login.**
  - No developer or SDK page; only a reseller program. TruGolf also sells its own LMs (Apogee, LaunchBox), so it is a competitor.
  - **Action:** contact TruGolf BD to get TruSimAPI credentials. Budget for a licensing or revenue-share ask. Unknown.

### 2.3 Awesome Golf (partner-only)

- Subscription from $14.95/month; iOS, Android and PC. Made by Great Detail Ltd (https://www.awesome-golf.com/).
- **Compatibility list** (https://insights.awesome-golf.com/docs/reference/compatibility/launch-monitor/list): Garmin R10/R50; FlightScope Mevo Gen2, Mevo+, X3/Xi family and others; Bushnell Launch Pro/LPi; Foresight Falcon/QuadMAX/GCQuad/GC3/GCHawk; Rapsodo MLM2PRO; Square Omni/Home; Uneekor EYE MINI.
- No public API. Integration happens "with some top Launch Monitor manufacturers" through partnerships, with contact at info@awesome-golf.com.
- Rapsodo's third-party token flow authorizes "Awesome Golf" specifically, which suggests bundled-subscription deals.
- **Requires a business deal.**

### 2.4 OpenGolfSim (open local API; easy win)

- Desktop/mobile sim at https://opengolfsim.com.
- Physics engine **FUSE** (https://github.com/OpenGolfSim/fuse): TypeScript/Three.js/WebGPU, **PolyForm Noncommercial 1.0.0**, so commercial use needs a deal (help@opengolfsim.com).
- The **Unity SDK** (https://github.com/OpenGolfSim/ogs-unity-developer-sdk) is GPL-3.0 and includes "open source versions of our core golf physics".
- **LM API** (https://github.com/OpenGolfSim/help.opengolfsim.com, `_includes/api-example-python.md`):
  - **TCP 127.0.0.1:3111**, newline-delimited JSON.
  - Messages: `{"type":"device","status":"ready"}` and `{"type":"shot","shot":{"ballSpeed","verticalLaunchAngle","horizontalLaunchAngle","spinAxis","spinSpeed"}}`.
  - There is also a plugin API (`bluetooth.createClient`, `network.createServer`, `shotData`).
- **Open: implement it on day one.**

### 2.5 Other open-source simulators and engines

| Project | Link | ★ / license | Notes |
|---|---|---|---|
| **OpenShotGolf** (formerly JaySimG) | https://github.com/jhauck2/OpenShotGolf | 64★, **GPL-2.0**, Godot | Listens for GSPro Open Connect v1; "officially tested with PiTrac and Square"; drag, Magnus, grass drag, friction |
| **OpenFairway** | https://github.com/digitalhand/openfairway | 18★, **MIT**, C#/Godot 4.5 / .NET 9 | "World's first open source golf physics library". Wind-tunnel polynomial Cd/Cl (Bearman/Harvey-based, Cl max 0.268–0.32), **Penner bounce with spin-dependent COR**, surface presets, check-up spin friction. v1.0.5 calibrated against "FS and GSP reference sources" (calibration history in `assets/data/calibration/history`). |
| Seneca Golf | https://github.com/csites/Seneca-Golf | 24★, GPL-3.0, Urho3D | Hobby sim |

### 2.6 TGC 2019, Creative Golf, Infinite Tees, Golfshot, others

- **The Golf Club 2019 (2K/HB Studios)** is an older title. LM support there was historically vendor-built plugins (SkyTrak, Mevo+ and others), and an `skytrak-tgc-watchdog` repo exists. It is a declining platform. **[unverified this session: current partner terms]**
- **Creative Golf 3D, Infinite Tees, ProTee VX, Golfisimo, TrackMan Virtual Golf, Uneekor Refine/View, FSX Play**: either vendor-proprietary (tied to their own hardware) or partner-only. The Infinite Tees site refused connections this session. None publish an open LM API that we could find. **Treat as BD targets after launch.**
- **Golfshot** is a GPS/scorecard app, not a simulator. Not an integration target.

### 2.7 "Open Launch Monitor API" standardization efforts

- **Flight Relay Protocol (FRP)**, https://github.com/flightrelay/spec. **CC0**, spec v0.1.0 (early draft), created 2026-03-08. A WebSocket protocol:
  - Handshake: `{kind:"start", version:["0.1.0"], name}`.
  - Events: `shot_trigger` → `ball_flight` / `club_path` / `face_impact` (any order) → `shot_finished`, plus `device_telemetry`, `alert` and detection-mode commands.
  - Shots are correlated by `shot_id`. Values use **unit-tagged strings** (`"67.2mps"`, `"197.4yd"`).
  - Rust SDK (`flightrelay/sdk-rust`, Apache/MIT). Reference implementation: flighthook.
  - Companion **Render Relay Protocol** (https://github.com/renderrelay/spec).
  - It is pitched explicitly at LM vendors: "Implementing FRP does not mean opening your software stack."
- **Recommendation:** make FRP a first-class output of our device and contribute to the spec. It is free, permissive and aligned with our "open simulator API" positioning. We could become its first hardware vendor.
- **GSPro Open Connect** is the de-facto standard. 16+ clients speak it (libgspro survey). Ship both.

---

## 3. Academic and technical literature

### 3.1 Ball-flight aerodynamics (drag/lift vs spin parameter and Reynolds number)

| Reference | What it gives us | Verified |
|---|---|---|
| **Bearman, P.W. & Harvey, J.K. (1976).** "Golf Ball Aerodynamics." *Aeronautical Quarterly* 27(2):112–122. doi:10.1017/S0001925900007617 | Classic wind-tunnel CD and CL vs spin parameter S = rω/v for conventional and hexagonal dimples, Re ~ 0.4–2.4×10⁵. Basis of most open models (OpenFairway, libgolf bins). | Crossref ✔ |
| **Smits, A.J. & Smith, D.R. (1994).** "A new aerodynamic model of a golf ball in flight." *Science and Golf II*, pp. 340–347 | Re- and S-dependent CD/CL plus a **spin-decay** model, from a spinning-ball rig over a full flight range | [unverified this session] |
| **MacDonald, W.M. & Hanzely, S. (1991).** "The physics of the drive in golf." *Am. J. Phys.* 59(3):213–218 | Simple 2D flight model; good teaching baseline | [DOI not resolved this session] |
| **Penner, A.R. (2003).** "The physics of golf." *Rep. Prog. Phys.* 66(2):131–171. doi:10.1088/0034-4885/66/2/202 | The canonical review: club-ball impact, aerodynamics, **bounce and roll**. Penner's bounce (tangential spin coupling term `2rω/7`) is used by libgolf and OpenFairway. | Crossref ✔ |
| **Aoki, K., Muto, K. & Okanaga, H. (2010).** "Aerodynamic characteristics and flow pattern of a golf ball with rotation." *Procedia Eng.* 2(2). doi:10.1016/j.proeng.2010.04.011 | CD/CL vs Re and spin, with flow visualisation | Crossref ✔ |
| **Lyu, B., Kensrud, J., Smith, L. & Tosaya, T. (2018).** "Aerodynamics of Golf Balls in Still Air." *Proceedings* 2(6):238 (ISEA 2018). doi:10.3390/proceedings2060238 | Washington State University still-air measurements of CD/CL across ball types. **This is the data behind Alan Nathan's golf trajectory calculator** (http://baseball.physics.illinois.edu/trajectory-calculator-golf.html, Excel v2, updated 2025-02-15) and behind libgolf. | Crossref ✔ |
| **Ferguson, S., McNally, W. & McPhee, J. (2022).** "Predicting the Flight of a Golf Ball: Comparing a Physics-Based Aerodynamic Model to a Neural Network." ISEA Engineering of Sport 14. doi:10.5703/1288284317493 (https://docs.lib.purdue.edu/resec-isea/2022/session05/4/) | University of Waterloo. Fits **quadratic** CD(S) and CL(S) to **1,040 measured shots** and compares against a neural network. Published coefficients as used by OpenFlight: **CD = 0.1304 + 0.9287·S − 0.8259·S²**, **CL = max(0, 0.0504 + 1.2031·S − 1.1490·S²)**, valid to S ≈ 0.75 (hold constant beyond). Lift peaks near S ≈ 0.52. | Crossref ✔; coefficients via OpenFlight docs |
| **Nathan, A.M. (2008).** "The effect of spin on the flight of a baseball." *Am. J. Phys.* doi:10.1119/1.2805242 | Methodology for CL/CD vs S from trajectory data (baseball); transferable approach | Crossref ✔ |
| Kiratidis & Leinweber (2018), *Eur. J. Phys.* doi:10.1088/1361-6404/aaa888 | OpenFlight cites this for ~4%/s spin decay. **Caution: the paper is about FIFA World Cup soccer balls.** Use Smits & Smith or TrackMan-published golf spin-decay data instead. | Crossref ✔ (topic mismatch found) |

**Sanity check of the Ferguson fit.** Take a driver at 70 m/s with 2,700 rpm: ω = 283 rad/s, so S = 283 × 0.02135 / 70 ≈ 0.086. The fit gives CD ≈ 0.204 and CL ≈ 0.145, consistent with Bearman & Harvey's post-critical-Re values.

**Reynolds dependence.** The Ferguson fit has none. libgolf uses a piecewise-linear CD through the drag crisis: CD = 0.50 for Re ≤ 0.5×10⁵, CD = 0.20 for Re ≥ 1.0×10⁵, linear in between, plus 0.18·S. Its lift is Reynolds-binned, using Bearman bins at 50k/60k/65k/70k and a Hill-saturation curve above 70k. That matters for low-speed wedges and chips, where Re falls toward ~5×10⁴ near apex.

**Spin decay** options:
- libgolf (Nathan): exponential, τ = 1/(2×10⁻⁵ · v/r) in ft units, so **τ ≈ 15 s at 160 mph** (about 6–7%/s initially, slowing as v drops).
- OpenFlight: a constant 4%/s.
- Recommendation: calibrate against our own TrackMan reference data.

**Air density:** barometric formula plus Sutherland viscosity (OpenFairway `Aerodynamics.cs`). Add humidity, which Nathan's calculator includes.

### 3.2 Bounce and roll

- **Penner (2003)** bounce model, as implemented in libgolf `docs/bounce_model.md`:
  - v_n' = −COR·v_n
  - v_t' = friction·v_t
  - spin term: v_t' *= max(0, 1 − (2rω/7)/|v_t'|)
  - ω' = retention·ω
- **OpenFairway** adds spin-dependent COR and "check-up" behaviour for high-spin wedges.
- **Roll** (libgolf): Coulomb friction with static/dynamic μ, slope decomposition, stop below 0.1 ft/s.
- Further reading: Penner, "The run of a golf ball" (*Can. J. Phys.* 2002), and Haake's turf impact studies (late 1980s–90s). **[unverified this session]**
- **Honest assessment:** every open model's *total distance* depends heavily on turf parameters. TrackMan's own "total" is also a model. Expect to tune per surface preset (firm, normal, soft) against TrackMan totals.

### 3.3 Spin estimation from images

| Reference | Relevance | Verified |
|---|---|---|
| **Tebbe, J., Klamt, L., Gao, Y. & Zell, A. (2020).** "Spin Detection in Robotic Table Tennis." ICRA 2020. arXiv:1905.07967 | Spin from high-speed images of a ball with a logo/marker. Compares optical-flow-like registration with CNN regression. | arXiv ✔ |
| **Gossard, T., Tebbe, J., Ziegler, A. & Zell, A. (2023).** "SpinDOE: A ball spin estimation method for table tennis robot." arXiv:2303.03879. Code: https://github.com/cogsys-tuebingen/spindoe (26★, **Apache-2.0**) | Dot-pattern (marked ball) orientation per frame, then robust rotation regression. **The regression and outlier stage transfers to dimple-feature orientation estimates**, and the license is permissive. | arXiv ✔ / gh ✔ |
| **Gossard, T., Krismer, J., Ziegler, A., Tebbe, J. & Zell, A. (2024).** "Table tennis ball spin estimation with an event camera." arXiv:2404.09870 | **Event cameras** give microsecond temporal resolution without strobes. A possible future sensor path for markerless spin (Prophesee/Sony IMX636-class). | arXiv ✔ |
| **PiTrac** `ball_image_proc.cpp` | Working, *markerless* golf implementation: Gabor dimple enhancement, then 3D rotation grid search, then (newer) a learned spin predictor | gh ✔ |
| **jelis86** dimple tracking | Markerless alternative: FAST corners + patch matching + RANSAC rotation center | gh ✔ (description only) |
| Commercial patents (Foresight GC2/GCQuad flash imaging; TrackMan radar spin from Doppler modulation; Uneekor/Bushnell markerless optical) | **Freedom-to-operate is the real risk for our markerless camera spin**, more than copyright | **Not fetched**: Google Patents blocked. **Run a formal FTO search.** |

**Key technical insight:** markerless spin is *registration of dimple texture on a sphere across two (or more) strobe images*. Robustness comes from:
1. high resolution on the ball (PiTrac's ~1.4 MP across a wide FOV is marginal);
2. a short strobe pulse to limit blur;
3. good 3D pose, meaning stereo or known depth for the sphere-projection;
4. multiple exposures, to fit a constant-ω model rather than a single pair.

A learned model trained on **synthetic renders** (dimple-accurate ball meshes with known ω) plus real data is the modern approach. PiTrac moved to ML as its default, which supports this.

### 3.4 3D trajectory from stereo/monocular high-speed imaging

- PiTrac uses Camera 1 + Camera 2 with known calibration. Depth comes from ball radius in Camera 2; horizontal launch angle comes from the change in apparent size.
- True stereo, with both cameras imaging the same strobe sequence, is what PiTrac's docs call the "path to stereoscopic vision". It is the GCQuad approach.
- Ball-radius-to-depth gives roughly 1 mm-per-pixel errors at Pi GS resolution (author's note). Plan for stereo plus higher-resolution ROI capture.
- The Inrange-based Kaggle entry (https://github.com/dlxky/Inrange-ball-flight) shows a hybrid **physics + Gaussian-process** model. It recovers spin and landing from radar checkpoint crossings: median landing error 3.1 m; "spin is not the bottleneck" for landing prediction. This is a useful prior for *trajectory-fitting-based spin estimation* in outdoor radar or long-track modes.

### 3.5 Club head / face / impact location from video (markerless)

- No open, permissive, production-grade club-face-angle or impact-location estimator was found this session.
- **GolfDB** (McNally et al., CVPRW 2019, arXiv:1903.06528, https://github.com/wmcnally/golfdb, 320★) covers swing *event* detection (8 events, SwingNet), not club pose. The same Waterloo group (McNally, McPhee) also co-authored the Ferguson flight paper.
- Commercial markerless club data (GCQuad needs club stickers; Uneekor EYE XO2 and Bushnell LPi claim markerless) is a differentiator **we will have to build ourselves**. Likely approach: stereo high-speed imaging of the club head at impact, then fitting a CAD/template or learned keypoints (leading edge, toe, heel, grooves), then deriving face angle, path, attack angle, dynamic loft and impact location from the multi-strobe sequence.
- **[Follow-up search needed for 2023–2026 papers on golf club-head 6-DoF pose estimation.]**

### 3.6 Radar golf ball tracking

- **Practical open prior art:** OpenFlight (OPS243-A CW Doppler rolling buffer, IWR6843 FMCW angle), tannu64 (InnoSenT SMR333 STFT/CFAR/Kalman club/ball separation), thomasjhook (HB100 FFT).
- **Spin from radar** shows up as Doppler sidebands or micro-Doppler modulation from surface features. That is TrackMan's long-standing method (Fredrik Tuxen patent family; **not fetched this session**). OpenFlight's dechirped sideband estimator is the only open attempt found, and it is unvalidated.
- See `05-tech-radar.md` for sensor-level detail.

### 3.7 Launch-monitor accuracy literature

- **Leach, R.J., Forrester, S.E., Mears, A.C. & Roberts, J.R. (2017).** "How valid and accurate are measurements of golf impact parameters obtained using commercially available radar and stereoscopic optical launch monitors?" *Measurement* 112:125–136. doi:10.1016/j.measurement.2017.08.009 (Crossref ✔).
  - Benchmarked TrackMan-class radar and GCQuad-class stereo optical units against a lab reference. It is the template for our own validation protocol.
  - Read it before setting accuracy specs. Its finding that club metrics are less accurate than ball metrics on commercial units shapes realistic targets.

---

## 4. Open ball-flight implementations (survey)

| Implementation | Link | ★ / license / lang | Aero model | Bounce/roll | Validation |
|---|---|---|---|---|---|
| **OpenFlight `ballistics.py`** | https://github.com/open-flight/openflight | 1,151★ / **AGPL-3.0** / Python | **Ferguson 2022 quadratic** CD/CL(S), spin decay 4%/s, RK4 at 500 Hz, USGA max ball (45.93 g, 42.7 mm) | Carry only | **TrackMan regression**: overall carry RMSE **2.90 yd** (driver 2.38, 7-iron 1.33, PW 4.48); apex error 1.5–3.2 ft out-of-sample |
| **libgolf** | https://github.com/gdifiore/libgolf | 12★ / **GPL-3.0** / C++20 | Nathan/Lyu-WSU: CD through the drag crisis + S term, Re-binned CL from Bearman fits, τ spin decay; pluggable `AerodynamicModel` | **Yes**: pluggable Penner bounce, Coulomb roll, 3D terrain | Unit tests; demo (https://gdifiore.github.io/libgolf/demo/); no published TrackMan comparison |
| **OpenFairway** | https://github.com/digitalhand/openfairway | 18★ / **MIT** / C# (Godot) | Wind-tunnel polynomial CD(Re), CL(Re, S) with blending; Cl max 0.268–0.32 | **Yes**: Penner bounce, spin-dependent COR, surfaces, check-up | Calibrated against "FS and GSP reference sources" (calibration CSV history in repo) |
| OpenShotGolf (JaySimG) | https://github.com/jhauck2/OpenShotGolf | 64★ / GPL-2.0 / GDScript | Drag + Magnus with Reynolds modelling | Grass drag, friction | Tested with PiTrac/Square |
| WillerZ/golf-ball-flight | https://github.com/WillerZ/golf-ball-flight | 0★ / "Other" / C++23, JS, Kotlin | `ni_slow` model with a language-agnostic spec | Flight, bounce, roll | Unknown; check license text |
| adamfrly/golf-ball-flight-sim | https://github.com/adamfrly/golf-ball-flight-sim | 0★ / **none** / Python | "Research-grade aerodynamics, calibrated against published PGA TOUR TrackMan data" | Yes | Claims calibration; no license, so reference only |
| GCFive `trajectory_simulation` | https://github.com/VGLALALA/GCFive | MIT / Python | Port of JaySimG Godot scripts | — | Provenance risk (GPL origin) |
| sebblanchet/golf | https://github.com/sebblanchet/golf | MIT / Rust + Bevy WASM | Penner/Barber references | — | CSV export for validation |
| markccchiang/Simple-Golf-Simulator | https://github.com/markccchiang/Simple-Golf-Simulator | 41★ / ISC / Python | Swing model + flight | — | Educational |
| Alan Nathan Excel calculator | http://baseball.physics.illinois.edu/trajectory-calculator-golf.html | Free spreadsheet | WSU (Lyu et al.) CD/CL, 3D, wind, temperature, elevation, humidity | — | Reference-grade physics source |
| OpenGolfSim FUSE | https://github.com/OpenGolfSim/fuse | PolyForm-NC / TS | Undisclosed in README | Yes (full sim) | — |

**Recommendation:**
- Write our own flight model as a small, permissively owned C++/Rust library, so it runs both on-device and in our app.
- Structure it like libgolf (pluggable aero, bounce and roll phases), but implement it clean-room.
- Coefficients:
  - Start from the **Ferguson 2022 quadratics**. They are published, externally fitted, and validated to about 3 yd RMSE in OpenFlight's TrackMan test.
  - Add Reynolds-dependent corrections from Bearman & Harvey / Lyu et al. for low-speed shots.
  - Use Penner bounce plus Coulomb roll with per-surface presets.
- Use **OpenFairway (MIT)** as a directly reusable reference for bounce and check-up details. **First confirm provenance**: it shares a domain and engine with GPL OpenShotGolf and has no fork relationship on GitHub, so ask the author.
- Copy OpenFlight's **"ratcheting RMSE budget vs TrackMan CSV"** test pattern. It is a process, not code.

---

## 5. Datasets

| Dataset | Link | Content | License / commercial use |
|---|---|---|---|
| **GolfDB** | https://github.com/wmcnally/golfdb ; arXiv:1903.06528 | ~1,400 YouTube-sourced swing videos with 8 event labels, bounding boxes, club type, view | Repo states **CC BY-NC 4.0**. **Not commercial**; underlying videos are third-party YouTube content. Use for research and prototyping only. |
| **SpinDOE data/code** | https://github.com/cogsys-tuebingen/spindoe | Table-tennis high-speed images with dot pattern + spin | Code **Apache-2.0**; check data terms. Marked ball, so useful only for method transfer. |
| **Inrange Student Competition (Kaggle)** | Referenced by https://github.com/dlxky/Inrange-ball-flight | Radar-tracked range shots: checkpoint crossings, launch spin, apex, landing labels | "Competition rules forbid redistributing it". **Not usable commercially without Inrange's permission.** Possible BD contact (Inrange is a UK range-radar company). |
| **OpenFlight session logs** | `session_logs/OpenFlight-Test.Normalized.csv` in https://github.com/open-flight/openflight | Paired TrackMan "Normalized" export used for regression tests | Inside an AGPL repo; data license ambiguous. Treat as **reference only**. |
| **PiTrac training materials** | — | Ball images and labels for YOLO + spin predictor | **Proprietary, explicitly excluded** (LICENSE.MODEL.md). Do not use. |
| Roboflow Universe "golf ball" detection sets | (not enumerated: web search unavailable) | Typically low-speed/broadcast images | Mixed CC-BY / custom; low value for strobed IR imagery. **[Follow-up]** |
| Garmin/R10, Mevo exports on GitHub (e.g., earl553/garminr10dataconverter, sghill/golf) | — | User shot exports | Personal data, not ground truth |

**Conclusion:** no public, commercially usable, labelled high-speed golf ball dataset with spin ground truth was found. Build our own:
1. **Synthetic:** render dimple-accurate ball meshes (several dimple patterns) under our exact optics, strobe timing, blur and noise, with known ω and axis. Domain randomization covers logos, scuffs and ball brands. LaunchTrac already does synthetic fixtures in Rust, which supports the approach.
2. **Real:** co-locate our rig with a rented or purchased **TrackMan 4 / GCQuad**. Log raw frames plus reference metrics. Also do marked-ball sessions, where markers give *our own* ground truth, without shipping markers.
3. **Club data:** high-speed stereo of club heads with a club-sticker reference system (GCQuad-style) used *only* to label training data for a markerless model.

---

## 6. License-compatibility matrix (what we can actually reuse)

| Component | License | Ship in closed product? | How to use |
|---|---|---|---|
| PiTrac code / hardware designs | GPL-2.0-only | **No** (copyleft on the linked program) | Architecture reference; read, do not copy. |
| PiTrac ML models + training data | Proprietary non-commercial | **Never** | Do not download into company systems; keep the team clean. |
| LaunchTrac | GPL-2.0 | No | Reference |
| OpenFlight (+ mobile) | AGPL-3.0 / GPL-3.0 | No | Reference; Ferguson coefficients come from the *paper*, not their code. |
| libgolf | GPL-3.0 | No | Reference for architecture and constants |
| OpenShotGolf | GPL-2.0 | No | Test sim for our GSPro output (running a GPL program as a separate test tool is fine) |
| springbok MLM2PRO connector, cam-putting-py, Seneca | GPL-3.0 | No | Reference |
| OpenGolfSim FUSE | PolyForm Noncommercial | No (without a deal) | Integration target, not a dependency |
| **libgspro** | **MIT** | **Yes** | Conformance-test server for our GSPro client; could embed if we ever act as a GSPro-compatible server. |
| **flighthook, 10over, ironsight, allsquare, flightrelay SDK** | **Apache-2.0** (SDK Apache/MIT) | **Yes** (with NOTICE) | FRP SDK; optionally bundle flighthook as a user-side bridge. |
| **FRP spec** | **CC0** | **Yes** | Implement natively. |
| **OpenFairway** | **MIT** | **Yes, after provenance check** | Bounce/roll/surface reference or port. |
| **spindoe** | **Apache-2.0** | **Yes** | Rotation-regression ideas and code for multi-frame spin fitting. |
| gsp-r10-adapter, Duwaynef MLM2PRO-BT-APP, kenjdavidson/gspro-connector | MIT | Yes | Protocol references (E6 message shapes, R10 BLE) |
| joebockhorst/gspro-connect | CC0 | Yes | Minimal Python GSPro client |
| ED_LIB (Cihan Topal ellipse/edge drawing) | MIT | Yes | Fast ellipse fitting for ball contours (independent of PiTrac's GPL code; get it from upstream) |
| GolfDB | CC BY-NC 4.0 | No | Research only |
| Ferguson 2022 / Bearman & Harvey / Lyu et al. / Penner equations and coefficients | Facts and equations (not copyrightable) | **Yes** | Implement ourselves, with citations. |

**Process recommendation:**
- Keep a written clean-room log.
- Engineers who study GPL/AGPL code write *specifications* (algorithms, constants, failure modes). Implementers code from those specs.
- Never copy PiTrac's ML artifacts.
- Run a **patent FTO** on strobe multi-exposure imaging, markerless dimple spin, and radar-sideband spin before committing the architecture.

---

## 7. Fastest path to a working prototype

**Weeks 0–2: integration and physics first (pure software, no hardware risk)**
1. Implement **GSPro Open Connect client** (TCP 921): string-aware brace-depth parser, heartbeat, never send `Speed: 0`, handle unsolicited 201 and club codes. Test against **libgspro** (115 cases, 23 fixtures, `gsplisten` tool) and against **OpenShotGolf** as a live sim.
2. Implement **OpenGolfSim client** (TCP 3111 NDJSON) and an **FRP WebSocket server** (`ws://:5880/frp`). Point flighthook at it to prove interop.
3. Write **our own flight + bounce + roll library**:
   - Ferguson quadratics + Re correction + τ spin decay + Penner bounce + Coulomb roll; atmosphere from barometric + Sutherland + humidity.
   - Create a TrackMan-CSV regression suite with ratcheting budgets. Target ≤3 yd carry RMSE, matching what OpenFlight achieved with the same published coefficients.

**Weeks 2–8: camera bring-up, learning from PiTrac without copying it**
4. Bench rig:
   - 2× **IMX296** global-shutter sensors (InnoMaker CAM-MIPI327RAW has trigger pins; mono, no IR-cut filter) on a Pi 5 or Jetson Orin Nano, M12 6 mm lenses.
   - A pulsed **NIR strobe** (pick wavelength and driver from our own optics study; PiTrac docs don't state one).
   - A cropped high-fps tee camera for trigger and launch detection.
   - Reproduce the **multi-exposure single-frame** trick.
   - For a commercial product, evaluate higher-resolution global-shutter sensors with hardware trigger (see `04-tech-camera.md`). PiTrac's own notes say 1.4 MP limits accuracy.
5. Detection: classical Hough/ellipse (ED_LIB upstream, MIT) as a baseline. Then train **our own** detector on our synthetic + real IR data.
6. Spin, v1: Gabor dimple enhancement + **3D rotation search** between strobe images (published idea, our implementation). Fit a constant-ω model over *all* strobe images using SpinDOE-style robust regression (Apache-2.0).
7. Spin, v2: learned regressor trained on synthetic dimple renders + rig data labelled by a co-located TrackMan/GCQuad.

**Weeks 4–10: optional radar channel and fusion**
8. Add an **OPS243-A** (24 GHz CW, rolling-buffer I/Q, sound/optical trigger) for independent ball and club speed. OpenFlight shows the $249 module and the sampling recipe: 30 ksps, 4,096 samples, DC mask. Use it to cross-check camera speed and to give outdoor robustness where IR sunlight saturates the camera.

**Weeks 8–12: validation**
9. Validation protocol modelled on **Leach et al. (2017)**: side by side with TrackMan/GCQuad, per-metric bias and limits of agreement, per club. Include outdoor sunlight tests early, since PiTrac's known weakness is IR sensitivity.

**Business development, in parallel**
10. Email **business@gsprogolf.com** (native listing, like Nova by OpenLaunch). Contact **TruGolf** for TruSimAPI credentials (E6 auth is non-public). Contact **Awesome Golf** (info@awesome-golf.com) and **OpenGolfSim** (help@opengolfsim.com).
11. Publish our device's open API as **FRP + GSPro Open Connect**, and contribute to the FRP spec. It is cheap credibility with the DIY and sim community, which currently routes around closed vendors with OCR hacks and DMCA-1201(f) reverse engineering.

**One-line answer:** don't fork PiTrac; reuse its *ideas*. Build the clean-room camera pipeline described in §7, steps 4–7. Use our own Ferguson-coefficient flight model with Penner bounce. Ship GSPro Open Connect, OpenGolfSim and FRP outputs on day one, tested with libgspro. Pursue E6 and Awesome Golf as business deals.

---

## 8. Open items for a follow-up search pass (blocked this session)

- Patent FTO list, with numbers and status:
  - Foresight/GC2 flash multi-exposure imaging
  - TrackMan/Tuxen radar spin
  - Uneekor/Bushnell markerless club and spin
  - Rapsodo markerless spin
- 2023–2026 papers on: markerless golf-ball spin (deep learning), golf club-head pose / face angle / impact location from video, radar micro-Doppler spin for golf.
- Smits & Smith (1994) spin-decay constants; Penner "The run of a golf ball" DOI; TrackMan's published spin-decay and normalization notes.
- GSPro native-partner terms (fees or revenue share, if any); E6/TruGolf TruSimAPI partner terms; TGC 2019, Creative Golf and Infinite Tees integration programs.
- Roboflow Universe golf-ball datasets (counts and licenses); any TrackMan-labelled public datasets on Kaggle.
- OpenLaunch / Nova: technology, price and how it obtained native GSPro support (the vendor site failed TLS this session).
- PiTrac published accuracy comparisons (Discord or YouTube); PiTrac strobe LED wavelength and driver details (`docs.pitrac.org/hardware/parts-list/`).
