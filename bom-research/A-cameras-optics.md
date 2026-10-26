# A — Cameras, lenses, filters, camera interconnect

Outer Bounds (Pro and Indoor share this sensing core). Researched 7 Oct 2026.

Conventions: **[est.]** = my estimate, not a published price. Prices in EUR are converted at **1 EUR = 1.16 USD [est. FX]**. "Quote" = vendor publishes no price. Every published price has a URL in the table or in the source list.

---

## 0. Bottom line

1. **Quad Shutter Control cannot be bought working today on any MIPI module.** No shipping Linux driver exposes it: the FRAMOS Jetson/RPi/NXP drivers, the Rockchip BSP driver, Vision Components (VC) and Leopard don't. e-con says the "100,000 fps" quad mode "requires firmware customization". Sony has never published the per-phase timing limits, the minimum spacing between phases, or whether an external trigger can start the sequence. Those are in the IMX900 datasheet and register map, which are under NDA. The "100 kfps" marketing implies about 10 µs per phase, but that is an inference. Vadzo (GigE/USB) and Basler have working quad-shutter cameras on their own FPGA/ISP, so the feature is real. **Treat Quad Shutter as unconfirmed until the NDA datasheet is in hand.** The architecture must close on single-exposure triggered frames, using either the 4×IMX296 fallback or 3×IMX900 at high frame rate.
2. **Neither sensor reaches a true 3–5 µs electronic gate through documented paths.**
   - IMX900 (constants in the FRAMOS driver): the exposure step is one line (1H) and the minimum is 1H + 2 µs. 1H = HMAX / 74.25 MHz, which is 4.55 µs in mono 8-bit full-res at 2 or 4 lanes and 8.22 µs by default. **The minimum gate is therefore about 6.6–10 µs.** In 2×-subsampled mono mode 1H is 2.28 µs, giving about 4.3 µs.
   - IMX296: on the Pi, exposure = trigger low-pulse + 14.26 µs (Raspberry Pi docs). The VC IMX296 has an 18.5 ns exposure step in fast-trigger mode, but the trigger pulse must be >10 µs and there is a 5 µs debounce delay.
   - Consequence: the 3–5 µs LED strobe sets the signal, but sunlight integrates over a gate of about 7–10 µs (IMX900) or 15–30 µs (IMX296). **The IMX900's shorter gate gives roughly 2–3× better sun rejection.** This should feed the LED-power budget.
3. **Recommended prototype camera: Vision Components VC MIPI IMX900 mono (VK000601) ×3**, with the third camera used for the club. Reasons:
   - It has a trigger input and flash output on the same 22-pin FPC at 3.3 V LVCMOS.
   - It has a shipping fast-trigger mode in open-source drivers for Jetson, Pi 5 and NXP.
   - It has the lowest published volume price: **€109.99 at 1k** (VC flyer dated 2 Jul 2026).
   - It is an industrial product built in Germany for long-term supply.
   - Alternates: **Leopard LI-IMX900-MIPI-078H** ($399, 48 in stock) is the only IMX900 module with a listed QCS6490 (RB3 Gen2) driver. **FRAMOS FSM:GO-IMX900M** has the best public documentation and open drivers, which suits an RK3588 port.
4. **No IMX900 module has a shipping RK3588 driver.** However, **Rockchip's own BSP kernel (`develop-6.1`) gained `drivers/media/i2c/imx900.c` on 6 Nov 2025.** It is 4-lane, master streaming only, RGGB10 2064×1552, with no trigger or mono support. That is a real starting point. Add the mono format and TRIGMODE (register 0x3400, values 9 and 10) by copying from the FRAMOS driver.
5. **Lens: Commonlands CIL361-F1.8-M12ANIR** (6.1 mm, f/1.8, IR-corrected 400–900+ nm, 5 MP at 2.2 µm, 7.2 mm image circle, $39). It covers both the IMX900 (5.81 mm diagonal) and the IMX296 (6.3 mm). On the IMX900 at the real ~0.52 m slant range it gives 400×300 mm. Only 15 are in stock, so order early. Alternate: CIL061-F1.9-M12BNIR.
6. **Filter: Commonlands CBP940-070S030** (7×7×0.3 mm, $9), glued behind the lens. Its passband is about 80 nm FWHM at OD3, wider than the 30–50 nm / OD4 spec, so it is fine for prototypes only. For production, specify a custom 940/40 OD4 dielectric filter placed in the lens holder where the IR-cut filter normally sits. Do not coat the sensor's cover glass (see §5).

---

## 1. THE BOM (centerpiece)

### 1a. Recommended camera set for ONE unit (3× IMX900 mono: vertical stereo pair + club camera)

| Item | Manufacturer | MPN | Vendor | URL | Qty/unit | $@1 | $@100 | $@1k | $@10k | Stock/lead | Lifecycle | Notes/alternates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IMX900 mono MIPI module (stereo top, stereo bottom, club) | Vision Components | **VK000601** (VC MIPI IMX900, B&W) | Vision Components / distributors (e.g. Ampheo) | https://www.mipi-modules.com/en/vc-mipi-flyer-02-06-26-en/ | 3 | quote [est. $230] | [est. $165] | **€109.99 ≈ $128** [FX est.] | [est. $105] | "Ready for purchase" per flyer; lead time not published | Active, industrial long-term | 2/4-lane CSI-2, 1.2 Gbps/lane, 22-pin FPC, trigger in + flash out. Fast-trigger mode. Drivers: Jetson, Pi 5, i.MX8M (GitHub VC-MIPI-modules). No RK3588/QCS6490 driver. **Alt A:** Leopard LI-IMX900-MIPI-078H, $399 @1, 48 in stock, QCS6490 listed. **Alt B:** FRAMOS FSM:GO-IMX900M-M12B-PM-A1Q1 (Mouser, price not retrievable). **Alt C:** Vadzo Bolt-900MGS, $268/$249 @100/$199 @250+. |
| S-mount lens holder for VC module | Vision Components | VK000057 | Vision Components | https://www.mipi-modules.com/fileadmin/external/documentation/hardware/VC_MIPI_Camera_Module/index.html | 3 | quote [est. $12] | [est. $8] | [est. $5] | [est. $2] | Quote | Active | No IR filter fitted (correct for 940 nm). The FRAMOS and Leopard modules ship with an M12 holder. |
| M12 lens 6.1 mm f/1.8, IR-corrected, 5 MP | Commonlands | **CIL361-F1.8-M12ANIR** | Commonlands | https://commonlands.com/products/ir-corrected-6mm-m12-lens-cil361 | 3 | $39.00 | [est. $28] | [est. $18] | [est. $10] (or a Chinese OEM equivalent at $5–8) | **15 pcs US stock** | Active | 7.2 mm image circle (1/2.5"), 2.2 µm, −7% F-θ distortion (calibrated out). **Alt:** CIL061-F1.9-M12BNIR ($39, 171 in stock, 3 MP at 3 µm, −8% distortion, IP69K). **Do not use** CIL059-F1.7-M12B650: its 650 nm IR-cut filter blocks 940 nm, and the NIR variant is out of stock. |
| 940 nm bandpass filter, 7×7×0.3 mm | Commonlands (appears to be MidOpt BN940-type glass) | **CBP940-070S030** | Commonlands | https://commonlands.com/products/940nm-bandpass-filter | 3 | $9.00 | [est. $5] | [est. $2.50] | [est. $1.00] | 930 pcs | Active | About 80 nm FWHM, OD3 (<900 and >1050 nm). Wider than spec, so prototype only. Commonlands will glue it to the lens rear. **Spec-compliant alt:** MidOpt BN940 (55 nm FWHM, ±10 nm CWL), custom-cut unmounted, quote: https://midopt.com/filters/bn940/. **Avoid** CBP941 (10 nm FWHM, $15): too narrow once chief-ray-angle shift is included. |
| Camera FPC, 22→22 pin, 100 mm (stereo pair) | Vision Components | EK004418 | Vision Components | https://www.mipi-modules.com/fileadmin/external/documentation/hardware/VC_MIPI_Camera_Module/index.html | 2 | quote [est. $12] | [est. $8] | [est. $4] | custom FPC [est. $2] | Quote | Active | 22-pin carries 4 lanes plus trigger (pin 17) and flash (pin 18). |
| Camera FPC, 22→22 pin, 200 mm (club camera) | Vision Components | EK003260 | Vision Components | same as above | 1 | quote [est. $14] | [est. $9] | [est. $5] | custom FPC [est. $2.5] | Quote | Active | 200 mm is VC's limit. Repeater VK003318 extends to 400 mm. **Generic alt:** Molex Premo-Flex **0150200241** (22 pos, 0.5 mm, 203 mm, same-side contacts), $5.21 @1, 1,951 in stock: https://www.digikey.com/en/products/result?keywords=premo-flex%2022%20position%200.5mm%20203.20mm. Verify pin-1 orientation against VC's cable before swapping. |
| Carrier-side FFC connector, 22 pos 0.5 mm, R/A ZIF | Hirose | **FH12-22S-0.5SH(55)** | Digi-Key (HFJ122CT-ND) | https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/FH12-22S-0-5SH/583540 | 3 | $2.57 | [est. $1.60] | [est. $1.10] | [est. $0.85] | 18,035 | Active (the non-(55) FH12-22S-0.5SH is **Obsolete**) | Pi-5-style 22-pin. **Alt:** TE 2-2492104-2, $0.96 @1 (same Digi-Key page). FRAMOS's P22A module side uses FH12-22S-0.5SVA(54) (vertical). |
| **Subtotal per unit (3 cameras)** | | | | | | **≈ $916** [est.] | **≈ $648** [est.] | **≈ $477** [est.] | **≈ $363** (modules) / **≈ $210** (custom board, see §7) [est.] | | | |

The @1 subtotal depends on VC's single-unit quote. With Leopard modules instead (no separate holder), @1 is about $1,390.

### 1b. Fallback set (IMX296 mono, 4 cameras as two time-staggered stereo pairs) plus optional club camera

| Item | Manufacturer | MPN | Vendor | URL | Qty/unit | $@1 | $@100 | $@1k | $@10k | Stock/lead | Lifecycle | Notes/alternates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IMX296 mono MIPI module with trigger | Vision Components | **VK000434** (VC MIPI IMX296, B&W) | Vision Components | https://www.mipi-modules.com/en/vc-mipi-flyer-02-06-26-en/ | 4 (+1 club) | quote [est. $150] | [est. $110] | **€76.99 ≈ $89** | [est. $70] | Ready for purchase | Active (VC calls it best-selling) | 1 lane RAW10, 60 fps. Fast trigger: 18.5 ns exposure step, 5 µs trigger delay, 18.5 ns jitter, trigger >10 µs. Drivers: Jetson, Pi, NXP. |
| IMX296 mono, Pi-native, with trigger + strobe | InnoMaker | CAM-IMX296Mono-GS (ex CAM-MIPI296RAW-Trigger) | inno-maker.com | https://www.inno-maker.com/product/cam-mipi296raw-trigger/ | (alt) | $69.00 (1–119) | $69.00 | $45.00 (120+) | quote [est. $35] | In stock | Active | Pi drivers only (libcamera, mainline `imx296`). The Jetson version is $58 but its trigger works on Raspberry Pi only: https://www.inno-maker.com/product/imx296-mono-jetson-orin-nano/ |
| IMX296 mono, Pi-native, M12, trigger | Arducam | **B0619** | arducam.com | https://www.arducam.com/1-58mp-imx296-mono-global-shutter-camera-module-with-m12-lens-for-raspberry-pi.html | (alt) | $64.99 | quote | quote | quote | In stock | Active | 1-lane, Pi only, ships with a 96° M12 lens (swap it). |
| Lens for IMX296 (1/2.9") | Commonlands | CIL361-F1.8-M12ANIR | Commonlands | https://commonlands.com/products/ir-corrected-6mm-m12-lens-cil361 | 4–5 | $39.00 | [est. $28] | [est. $18] | [est. $10] | 15 pcs | Active | 6.3 mm diagonal < 7.2 mm image circle. HFOV 44° → 407×306 mm at 0.50 m. |
| Filter | Commonlands | CBP940-070S030 | Commonlands | https://commonlands.com/products/940nm-bandpass-filter | 4–5 | $9.00 | [est. $5] | [est. $2.5] | [est. $1] | 930 | Active | Same as 1a. |
| Cable + connector | as 1a | EK003260 / 0150200241 + FH12-22S-0.5SH(55) | | | 4–5 | as 1a | | | | | | The IMX296 needs only 1 lane, so the 15-pin variant (EK003261) also works. |

**Not suitable:** the Raspberry Pi Global Shutter Camera ($50). It uses a colour IMX296 with a C/CS mount and a fixed Hoya CM500 IR-cut filter, and there is no NoIR version (https://www.raspberrypi.com/documentation/accessories/camera.html).

---

## 2. IMX900 module survey (Q1)

| Vendor / MPN | $@1 | Volume | Interface | Ext. trigger | Quad Shutter | Shipping Linux drivers |
|---|---|---|---|---|---|---|
| **Vision Components** VC MIPI IMX900, VK000601 mono / VK000609 colour | Quote | **€109.99 @1k** (flyer 2 Jul 2026; was €124.99 in May 2024) | CSI-2 2 or 4 lanes, 1.2 Gbps/lane, 22-pin FPC | **Yes.** Trigger in and flash out, 3.3 V. Modes: streaming and fast trigger. The Jetson driver also lists external, pulse-width, self, single, sync, stream_edge, stream_level and overlap | Not exposed | Jetson Nano…Orin NX (L4T), Pi incl. Pi 5 (bcm2712 overlays), NXP i.MX8M Mini/Nano/Plus (Toradex, Variscite). **No RK3588 or Qualcomm.** |
| **FRAMOS** FSM:GO-IMX900M-M12B-PM-A1Q1 (mono, no lens, PixelMate). Interface options: PM, MC50A, FFC40A, P22A, GMSL3A | Mouser listing; **price could not be retrieved** (Mouser/Octopart block automated fetch) | Quote | CSI-2 4 lanes at 2.5 Gbps, D-PHY 2.1 | **Yes.** XTRIG1/XTRIG2 (1.8 V), XVS/XHS, XMASTER. Driver modes: Normal, **Fast Trigger** (master, TRIGMODE=10), **Sequential Trigger** (slave, TRIGMODE=9). On P22A, trigger pins are on Molex Microblade connectors | **Not in any FRAMOS driver.** FRAMOS docs page doesn't mention it | Jetson Orin/Thor, i.MX8MP, Pi 5 (all open source on GitHub `framosimaging`). **No RK3588 or Qualcomm.** |
| **e-con Systems** e-CAM37M_CUONX (mono, Jetson). Core module e-CAM315_CUMI900M_MOD | "Contact us". The colour e-CAM37_CUONX is USD 249 | Quote | CSI-2 2 or 4 lanes, 15 cm FFC | Trigger and strobe controls listed; "External Trigger and Strobe Setup Guide" | "100,000 fps" quad mode **requires firmware customization** | Jetson Orin NX/Nano, JetPack 6.2. Colour variants for i.MX8 and Renesas RZ/V2H. Qualcomm claimed in prose but has no SKU. **No RK3588.** |
| e-con See3CAM_37CUGM (USB 3, mono) | **$249** | "from $99" | USB 3 UVC | Self-trigger | **Quad HDR only on this USB SKU** | Any UVC host. Useful as a cheap bench tool for the sensor, not for the product. |
| **Leopard Imaging** LI-IMX900-MIPI-078H (mono, 3.6 mm lens) | **$399** | Quote | CSI-2 over I-PEX (lanes not stated) | Not stated | Not stated | Compatibility table: **Orin NX, Orin Nano, Pi 5, RB3 Gen2 (QCS6490)**. Drivers on request. |
| **Vadzo** Bolt-900MGS | from **$268** | **$249 @100–249, $199 @250+** (no lens or cable) | CSI-2 2 or 4 lanes | Not stated | Listed as a feature, no timing given | Jetson Nano/Xavier NX/Orin; Raspberry Pi (model not stated) |
| **Arducam** | — | — | No IMX900 CSI module found; only RoAD USB3/GMSL | — | — | — |
| Bare sensor IMX900-AMR-C (mono), 114-pin LGA | Gray-market broker $35.5–45.5 (Alibaba, MOQ 1) | Authorized via Macnica, RESTAR FRAMOS or Sony: quote | MIPI / SLVS-EC | — | Register-level (NDA) | — |

**RK3588:** the Rockchip BSP has `drivers/media/i2c/imx900.c` (develop-6.1, added 2025-11-06): 4 lanes at 2376 Mbps, RGGB10 2064×1552, no trigger. **QCS6490:** only Leopard lists support.

### Quad Shutter Control: what is confirmed and what is not

- **Confirmed (Sony, FRAMOS, e-con):** each pixel in a 2×2 unit has its own exposure start and integration time, all within one frame, and all four are read out together. Each phase is therefore an approximately 1032×776 sub-image. Resolution per phase is my inference from the 2×2 structure.
- **Confirmed (e-con blog):** the exposure window can be as short as about 10 µs per pixel ("100,000 fps").
- **Not confirmed anywhere public:**
  1. whether XTRIG (fast-trigger mode) can start the quad sequence;
  2. the minimum spacing between phase starts and its step size;
  3. whether phases may overlap or abut.
  - Vadzo says its GigE implementation holds "a consistent interval between exposure windows", without giving a number. Basler says "four exposures within microseconds of one another" from one trigger, synchronised to four lights, but this is a custom implementation.
- **Action:** request the IMX900 datasheet and application note from Macnica ATD or RESTAR FRAMOS under NDA. Alternatively, contract FRAMOS, VC or e-con to implement it, since e-con already states that firmware customization is required. Do not commit the spin-measurement architecture to Quad Shutter until this is answered.

---

## 3. IMX296 fallback (Q2)

- Mainline Linux has `drivers/media/i2c/imx296.c`, which is portable to RK3588 and QCS6490. The Rockchip BSP has **no** IMX296 driver.
- External trigger on the Pi uses the downstream `imx296.trigger_mode` parameter, a 1.8 V XTR input, and exposure = low-pulse + 14.26 µs.
- VC's IMX296 does fast trigger on its own module logic (18.5 ns step), at 3.3 V.
- Four IMX296s need four 1-lane CSI ports.
- Gate limitation: at least about 15 µs, and in practice 25–30 µs. That gives roughly 2–4× more sunlight integration than the IMX900. This is the main reason the IMX296 is the fallback, not the primary.

## 4. Club camera (Q3)

**Recommendation: a third VC MIPI IMX900 mono (VK000601), identical to the stereo cameras.**

- **Cost:** the 2026 VC flyer prices the VC OV9281 at **€63.99/1k** (it was €37.99 in 2024). The IMX900 is €109.99, so the saving from a cheaper sensor is only about €46 per unit.
- **Resolution:** at 400 mm field of view, the IMX900 gives 0.19 mm/px and the OV9281 gives 0.31 mm/px. The finer sampling helps the face-plane fit.
- **Commonality:** one SKU, lens, filter, driver, trigger path, gate time and calibration model.
- **Upside:** if Quad Shutter is later confirmed, it gives 4 club poses per frame.
- **Cost-down to evaluate at the custom-board stage:** OV9281 (Rockchip BSP has `ov9281.c`; the sensor has an FSIN trigger). Do not use the IMX296 for the club camera: it has the longest gate and needs a separate lens choice.

## 5. Lenses and filters (Q4, Q5)

**Focal length check.** The IMX900 active area is 4.644×3.492 mm. 400×300 mm at exactly 0.45 m needs f = 5.2 mm. At the real 0.5–0.6 m slant range (camera 45–60 cm to the side and yawed), **6.1 mm gives 381–457 mm horizontal**, which is correct. For the IMX296 (4.97×3.73 mm), 6.1 mm gives 407×306 mm at 0.50 m.

**Lens candidates (all M12, no IR-cut filter):**

| Lens | EFL / F# | Image circle | Rating | NIR | Distortion | $@1 | Stock | Verdict |
|---|---|---|---|---|---|---|---|---|
| Commonlands **CIL361-F1.8-M12ANIR** | 6.1 / 1.8 | 7.2 mm | 5 MP, 2.2 µm | IR-corrected 400–900+ nm (no 940 nm focus-shift figure) | −7% F-θ | $39 | 15 | **Primary** |
| Commonlands CIL061-F1.9-M12BNIR | 6.0 / 1.9 | 7.0 mm | 3 MP, 3 µm | Not stated | −8% rect | $39 | 171 | Alternate. Soft for 2.25 µm pixels. |
| Commonlands CIL059-F1.7-M12BNIR | 5.9 / 1.7 | 9.0 mm | 4–6 MP, 3 µm | Not corrected | −4% | $49 | **Out of stock** | Good if restocked |
| Commonlands CIL052 | 5.2 / **3.4** | 9.0 mm | 10 MP+ | — | −0.1% | $79 | 84 | Too slow |
| Commonlands CIL056 | 5.5 / 2.4 | 9.3 mm | 4 MP | — | −20% | $49 | 113 | Too distorted |
| Sunex DSL115C-NIR-F1.5 | 4.5 / 1.5 | 1/3" | — | Hybrid, no IR-cut filter | — | $69 | — | Too wide (56° H) |
| Evetar M13B0618IR (1/3", 6 mm f/1.8) | 6 / 1.8 | 1/3" | — | "IR" means no IR-cut filter only; visible design | — | about $15–17 at Machine Vision Store | — | Cheap backup; verify focus and MTF at 940 nm |

**MTF at 940 nm.** At f/1.8 the Airy diameter at 940 nm is 2.44·λ·N ≈ 4.1 µm, larger than the 2.25 µm IMX900 pixel. The diffraction MTF at the 222 lp/mm Nyquist frequency is about 0.5, which is acceptable. Stopping down below f/2.4 will visibly soften dimple texture.

**Focus.** Set and lock focus at 940 nm. In production, use active alignment under 940 nm illumination. Visible-light focus will not transfer to a lens that is not IR-corrected.

No published MTF curves were found for any of these lenses. Commonlands offers Trioptics MTF testing as a service.

**Filters.**
- **Prototype:** CBP940-070S030 ($9, 7×7 mm, 0.3 mm thick), glued behind the lens. Behind the lens, the chief-ray angle is about 12–20°, which blue-shifts the passband by about 10–15 nm. An 80 nm passband tolerates this.
- **Spec-grade:** MidOpt BN940 (55 nm FWHM, ±10 nm, ≥85% T), custom-cut, quote. MidOpt has no M12 size; its smallest thread is M13.25.
- **Do not use 10 nm filters (CBP941).**

**Production filter.** Specify a **custom 940 nm, 40 nm FWHM, OD4 (400–1100 nm) hard-coated dielectric filter on 0.3–0.5 mm glass, about 6.5–7 mm square**. Have the module or lens house fit it in the lens holder's IR-cut seat, or have the lens vendor put it in the barrel in place of the IR-cut filter. Commonlands, Sunex and Evetar all already offer BP850/BP940 slots. Centre the filter design about 8 nm red of 940 to pre-compensate the CRA shift.

Do not try to coat the Sony sensor cover glass. It is Sony's part and only Sony can change it.

Cost at 10k is about $0.80–1.50 [est.]. One filter per camera.

## 6. Cabling (Q6)

| Option | Module-side connector | Cable | Carrier connector | Notes |
|---|---|---|---|---|
| **VC 22-pin (recommended prototype)** | 22-pin 0.5 mm (on module) | EK004418 100 mm / EK003260 200 mm (VK000676 with trigger breakout) | Hirose FH12-22S-0.5SH(55), $2.57 | 4 lanes plus trigger and flash in one FFC. 200 mm max without repeater VK003318. |
| Generic 22-pin FFC | — | Molex 0150200241 (22p, 203 mm, same-side), $5.21 @1, 1,951 in stock | FH12-22S-0.5SH(55) or TE 2-2492104-2 ($0.96) | Check pin-1 orientation. Opposite-side 0151660242 has a 2k MOQ. |
| FRAMOS P22A (Pi 5-style) | Hirose FH12-22S-0.5SVA(54) | FRAMOS FMA-CBL-FFC22-0.2m | FH12-22S-0.5SH(55) | Trigger and sync are **not** on the 22-pin connector; they use Molex Microblade side connectors. |
| FRAMOS FFC40A | Molex 5051104091 | **Molex 0150200440** (40p, 203 mm, opposite-side): Digi-Key shows only the 2k-piece break at $4.00, non-stock, 9-week lead. GCT 05-40-D-0203-A-4-06-4-G is a similar part at $1.94, 477 in stock | **Molex 5051104091**: $2.25 @1, $1.62 @100, $1.38 @1k, 23,629 in stock | 40-pin has room for trigger and grounds. |
| FRAMOS MC50A (micro-coax) | I-PEX 20525-050E-02 | FMA-CBL-MC50-0.3m | FFA-MC50/A | Best signal integrity beyond 200 mm or through a hinge. |

**Production recommendation:**
- Use a custom impedance-controlled (100 Ω differential) FPC, about 150 mm long, with a ground plane.
- Use the same 22-pin 0.5 mm pinout at both ends, carrying trigger, flash and I²C.
- Run each IMX900 on **2 lanes**. That is 2.4 Gbps, which is ample for triggered bursts, and 3 cameras then use 6 lanes. This fits the RK3588 and QCS6490 CSI budgets; check with the compute agent.
- Use 4 lanes only if full-frame >60 fps is needed.

## 7. Path from modules to a custom sensor board

1. **Now to EVT (1–20 units):** VC (or Leopard for QCS6490) modules, Commonlands lenses, glued CBP940 filters. In parallel, sign a Sony NDA through Macnica or RESTAR FRAMOS for the IMX900 datasheet, Quad Shutter timing and the trigger-mode register map.
2. **DVT (100–1k):** ask VC, FRAMOS or e-con for a **customer-specific variant**: your FPC outline and pinout, a 2-lane 22-pin connector, a BP940 filter in the holder, and an active-aligned, glued 6 mm lens.
   - All three advertise OEM customization. e-con already says Quad Shutter needs "firmware customization", which is the hook for getting it implemented.
   - NRE **[est. $15–50k]**, MOQ **[est. 500–1,000]**.
   - Unit price **[est. $80–110]** with lens.
3. **PVT/MP (≥5–10k):** build your own sensor board. Buy the IMX900-AMR-C at **[est. $40–60 authorized]** (gray market $35–45, Alibaba).
   - Board content: a 114-LGA sensor, 3 regulators, a 37.125/74.25 MHz oscillator and an FPC.
   - Assembly: cleanroom SMT, then active alignment of lens and filter at a camera-module house such as Sunny, Q-Tech, Arducam/UCTronics OEM or Leopard's module line.
   - Board, holder and assembly cost **[est. $8–12]**, lens **[est. $5–8]**, filter **[est. $1]**, so about **$60–80 per camera at 10k [est.]**.
   - NRE **[est. $30–80k]**, including AA fixtures and Sony support.
   - Sony sensors are sold in trays through authorized channels; MOQ is **[est. 1 tray, a few hundred pcs]**.

## 8. Key risks

1. **Quad Shutter is unconfirmed:** no external-trigger or per-phase spec has been published. Mitigate with the NDA datasheet now and a fallback plan.
2. **Minimum gate of about 6.6–10 µs (IMX900) or 15–30 µs (IMX296)**, against a 3–5 µs strobe. Sunlight integrates over the whole gate. Budget the LED peak power or the filter OD accordingly.
3. **No shipping RK3588 or QCS6490 IMX900 driver with trigger,** except Leopard's QCS6490 claim (drivers on request). Budget driver work: port the Rockchip BSP imx900.c and add the mono format and TRIGMODE.
4. **IMX900 QE at 940 nm is not published.** VC describes it as "sensitive into NIR". Verify against the datasheet; it could need more LED power.
5. **Lens stock:** only 15 CIL361 are in stock. The F/1.7 NIR CIL059 is out of stock.
6. **Price visibility:** the FRAMOS (Mouser) and VC single-unit prices could not be retrieved, so the @1 figures for those are estimates.

## Sources

- FRAMOS IMX900 docs (pins, connectors, cables): https://docs.framos.com/en/latest/FSMEcosystem/ProductDocumentation/FSMGO/IMX900.html
- FRAMOS mono module: https://framos.com/products/modules/fsmgo-modules/fsmgo-with-imx900-mono-sensor-28639/
- FRAMOS drivers: https://github.com/framosimaging/framos-jetson-drivers (fr_imx900.c), https://github.com/framosimaging/framos-rpi-drivers, https://github.com/framosimaging/framos-nxp-drivers
- Rockchip BSP IMX900 driver: https://github.com/rockchip-linux/kernel/blob/develop-6.1/drivers/media/i2c/imx900.c
- FRAMOS Quad Shutter article: https://framos.com/articles/imx900-great-for-high-speed-applications/
- Sony Pregius S: https://www.sony-semicon.com/en/technology/industry/pregius.html
- e-con Jetson mono: https://www.e-consystems.com/nvidia-cameras/jetson-orin-nx-cameras/sony-imx900-global-shutter-monochrome-camera.asp
- e-con module family and prices: https://www.e-consystems.com/camera-modules/3mp-sony-pregius-imx900-global-shutter-camera-module.asp
- e-con Quad Shutter blog: https://www.e-consystems.com/blog/camera/uncategorized/unlocking-the-power-of-100000-fps-how-quad-pixel-shutter-control-works/
- e-con See3CAM_37CUGM: https://www.e-consystems.com/usb-cameras/sony-imx900-global-shutter-hdr-monochrome-camera.asp
- VC flyer, 2 Jul 2026 prices: https://www.mipi-modules.com/en/vc-mipi-flyer-02-06-26-en/
- VC hardware manual: https://www.mipi-modules.com/fileadmin/external/documentation/hardware/VC_MIPI_Camera_Module/index.html
- VC drivers: https://github.com/VC-MIPI-modules/vc_mipi_nvidia
- Leopard IMX900: https://leopardimaging.com/product/robotics-cameras/cis-2-mipi-modules/i-pex-mipi-camera-modules/global-shutter-mipi-cameras/3-2mp-imx900/li-imx900-mipi-078h/
- Vadzo Bolt-900MGS: https://www.vadzoimaging.com/product-page/sony-pregius-imx900-monochrome-mipi-camera
- Vadzo GigE Quad Shutter: https://finance.yahoo.com/technology/articles/vadzo-imaging-validates-quad-shutter-163000613.html
- Basler use case: https://www.baslerweb.com/en/use-cases/photometric-stereo-quad-shutter-control/
- Bare sensor (broker): https://www.alibaba.com/product-detail/IMX900-AQR-C-IMX900-AMR-C_1601578752603.html
- Bare sensor (authorized): https://www.macnica.com/eu/atd-europe/en/products-support/suppliers/sony/sony-imx900-amr/
- InnoMaker IMX296: https://www.inno-maker.com/product/cam-mipi296raw-trigger/
- Arducam B0619: https://www.arducam.com/1-58mp-imx296-mono-global-shutter-camera-module-with-m12-lens-for-raspberry-pi.html
- Raspberry Pi GS trigger: https://www.raspberrypi.com/documentation/accessories/camera.html
- Commonlands lenses:
  - CIL361: https://commonlands.com/products/ir-corrected-6mm-m12-lens-cil361
  - CIL061: https://commonlands.com/products/fast-6mm-m12-lens-cil061
  - CIL059: https://commonlands.com/products/low-distortion-6mm-m12-lens-cil059
  - CIL052: https://commonlands.com/products/low-distortion-5mm-m12-lens-cil052
  - CIL056: https://commonlands.com/products/5mm-m12-lens-cil056
- Commonlands filters:
  - CBP940: https://commonlands.com/products/940nm-bandpass-filter
  - CBP941: https://commonlands.com/products/940nm-bandpass-filter-10nm-fwhm-od4
- MidOpt BN940: https://midopt.com/filters/bn940/
- Sunex 1/3" list: https://www.optics-online.com/dsl_third.asp?sort=Fnum
- Evetar 1/3" lenses: https://machinevisionstore.com/catalog/bycategory?category=4&group=92
- Digi-Key parts:
  - Molex 0150200241: https://www.digikey.com/en/products/result?keywords=premo-flex%2022%20position%200.5mm%20203.20mm
  - Molex 0150200440: https://www.digikey.com/en/products/result?keywords=0150200440
  - Molex 5051104091: https://www.digikey.com/en/products/result?keywords=5051104091
  - Hirose FH12-22S-0.5SH(55): https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/FH12-22S-0-5SH/583540
