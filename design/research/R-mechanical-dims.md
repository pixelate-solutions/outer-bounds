# R — Mechanical dimensions of purchased parts (Outer Bounds Pro)

Compiled 7 Oct 2026 from manufacturer datasheets and drawings. All dimensions are in mm unless noted.
Anything marked **[unverified]** is a best estimate, not read from a manufacturer drawing.
Target envelope: ~240 × 160 × 84 mm.

## Corrections to the BOM assumptions (read first)

1. **The TurboX C6490P is 39 × 33 × 2.75 mm, not 42.5 × 35.5 × 2.7 mm.** The 42.5 × 35.5 size belongs to the plain **C6490** SoM. The 2.75 mm figure *excludes a bottom shielding case*. Thundercomm's keep-out and max-component-height data is behind the docs.thundercomm.com login and is not public.
2. **The Delta BFB0405HHA-TZP4 is 40 × 40 × 10 mm**, not 50 × 50. Note that DigiKey EU flags it "Not For New Designs".
3. **The Panasonic EEE-FK1H471AM is 16 × 16.5 mm (FK size code K16)**, a much bigger can than a 10 mm or 12.5 mm part.
4. **Use the datasheet outline for the VIEWE UEED024QV-RH40-A003, not the web page.** The datasheet gives 47.32 × 62.06 × 3.41 mm (CTP cover glass outline). The web page's 51.32 × 86.61 × 2.15 is copied from the 3.5" UEED035 listing.
5. **TE keying:** 787439-1 is a **right-hand-key** receptacle and 5787441-1 is a **keyless** plug. A keyless plug should enter a keyed receptacle, but this loses polarisation protection. Confirm the pairing with TE (or use the RH-key plug 5787422-1 / 5787424-1).
6. **The VC MIPI IMX900 board drawing is the IMX296 drawing.** VC states that the IMX900 uses the same board as the IMX296. The 14.1 × 14.1 × 2.0 sensor block is drawn for the IMX296, so the IMX900 package height may differ. Get the module STEP from support@vision-components.com before freezing the bench.

---

## 1. Vision Components VC MIPI IMX900 (VK000601) + VK000057 S-mount holder

Source: VC MIPI Camera Module Hardware Operating Manual, Appendix A, drawing "VC MIPI IMX296 (same board dimensions for … IMX568, IMX900)". It is read from the drawing image `mipi_sensor_imx296_drawing.png`.

| Feature | Value |
|---|---|
| PCB outline | **23.5 (W) × 22.0 (H)**, corner R1.5 |
| PCB thickness | **1.54** |
| Front (sensor) side | Sensor block 14.1 × 14.1, **2.0 tall** above PCB front (drawn for IMX296) |
| Back side | General components **1.2** max; FPC connector stands **3.9** off the PCB back face |
| Mounting holes | **2 × Ø2.2** at (1.75, 11.0) and (21.75, 11.0) from the bottom-left corner, giving **20.00 pitch** (standard 20 mm M12-holder pattern, M2 screws) |
| Locating holes | **2 × Ø1.0** at (21.75, 13.5) and (1.75, 8.5), diagonally opposite (5.0 vertical offset from each other) |
| Sensor / optical centre | ≈ **(11.75, 11.0)**: horizontally centred and on the mounting-hole line, between the two Ø2.2 holes (measured from the drawing) |
| FPC connector | On the **back side along the top (23.5 mm) edge**. It spans x ≈ 3.5 → 20.0 in the rear view (≈16.5 long) and z ≈ 14.7 → 17.7 from the bottom edge. The cable exits **upward, in-plane, past the top edge** (photo in the manual). It is 22-pin and the cable is single-orientation, with the "sensor side" marked |
| Active area (IMX900) | 4.608 × 3.456 (2048 × 1536 @ 2.25 µm), diagonal 5.8 |
| Mass | 3.9 g |
| FPC cables | EK040001 60 mm, EK004418 100 mm, EK003260 200 mm (22–22). 200 mm max without a repeater |

**VK000057 S-mount holder ("MIPI LHLD12")**
- Plastic M12 × 0.5 holder for this board group. It takes the optional 15 × 15 × 1.1 mm square IR-cut filter EK004727.
- It fixes with 2 screws on the 20 mm pitch.
- **The height is not published** (no public drawing; VC supplies STEP on request). **[unverified] estimate: ~20 × 20 footprint (body ≈ 22 wide across the screw ears), ≈ 12–14 mm tall.** This is consistent with Commonlands' recommendation of a 10–13 mm tall holder for the CIL361, and with typical 20 mm-pitch plastic holders (12–14.3 mm).

## 2. Commonlands CIL361-F1.8-M12ANIR (6.1 mm, F/1.8, no IR-cut)

Source: Commonlands product-page mechanical drawing.

| Feature | Value |
|---|---|
| Cap (front) diameter | **Ø14.0** |
| Thread | **M12 × 0.5**, threaded length **12.4 ± 0.3** |
| Total track, front of lens → image plane | **23.6 ± 0.3** (reference) |
| Mechanical BFL, thread end → image plane | **6.8 ± 0.3**, designed for **0.4 mm sensor cover glass** |
| Lens body length (derived) | 23.6 − 6.8 = **16.8** (cap ≈ 4.4 + thread 12.4) |
| Image circle / FOV | 7.2 mm, 76° at 7.2 mm. On the IMX900 (5.8 mm diagonal) the FOV is ≈ 62° diagonal **[derived estimate]** |
| Mass | 5.1 g, all-glass, AL6061 barrel (M12A: no ingress seal) |

## 3. Vishay VSMA1094250 (940 nm, ±28°)

Source: Vishay datasheet doc 80299 Rev 1.4, drawing 6.550-5366.01-4.

| Feature | Value |
|---|---|
| Body | **3.4 × 3.4**, base 1.0 thick |
| Overall height (incl. dome) | **2.895** |
| Dome | Ø3.05 (silicone lens) |
| Pads (bottom) | 3 pads, all **2.7 long**. Outer pads 0.5 wide, centre pad 1.0 wide, gaps 0.35. The centre pad doubles as the thermal path |
| Polarity | **Anode = left + centre pad, cathode = right pad**. Cathode marking dot at the top-left corner of the top face ("CX" corner) |
| Tolerance | ±0.1 |
| Thermal | Rth J-SP 6–9 K/W. 1.5 A DC, 5 A pulsed |

## 4. InnoSenT SMR-333 (24 GHz)

Source: Data Sheet SMR-313/333 v2.3, p.5 "Outline dimensions".

| Feature | Value |
|---|---|
| Outline | **21.4 ± 0.3 × 15.0 ± 0.3 × 3.1 ± 0.3** |
| Antenna side | **Top face** (away from the host PCB). It is a 2 × 4 patch array; the antenna PCB is 0.9 ± 0.1 thick. The RF/shield board on the underside is 20.4 × 14.0 and carries the solder pads |
| Pads | **10 castellated pads, 5 on each short (14 mm) edge**: pins 1–5 on one side, 6–10 on the other. Pitch 2.0 ± 0.05, pad width 1.5, pad depth 0.6, half-hole 1.0 wide. Pin-1 centre is 3.0 ± 0.25 from the board edge |
| Antenna centroid | At the array centre, ≈ module centre (marked "antenna centroid / rotational pivot") |
| Beam (−10 dB system) | **43° azimuth × 116° elevation**. The narrow plane is assumed to be along the 21.4 mm (4-patch) axis **[inferred from array geometry]** |
| Radome | No keep-out given in the datasheet. Use a plastic window ≥ λ/2 (≈ 6 mm) off the patches, or tuned to half-wavelength thickness **[general practice]** |

## 5. Thundercomm TurboX C6490P SoM

| Feature | Value |
|---|---|
| Outline | **39.0 × 33.0 × 2.75** (excluding the height of the bottom shielding case). LGA |
| Not C6490 | The C6490 (non-P) is 42.5 × 35.5 × 2.7 (2.75–2.85 depending on source) |
| Pin compat. | Pin-to-pin with C5430P / C8550 SoM |
| Keep-out / max height | **Not public (login-gated docs).** **[unverified] design assumption:** reserve a 41 × 35 carrier keep-out (1 mm ring) and no carrier components under the module. Leave clearance or a carrier cut-out for the bottom shield until the hardware design guide is obtained. Allow **≤ 3.0** above the carrier plus a TIM/heat-spreader stack |

## 6. Delta BFB0405HHA-TZP4 blower

Source: Delta "Specification for Approval" Rev 01, §10 dimension drawing.

| Feature | Value |
|---|---|
| Outline | **40.0 ± 0.5 × 40.0 ± 0.5 × 10.0 ± 0.5**. **40 × 40 × 10 confirmed (not 50 × 50)** |
| Mounting holes | **4 × Ø2.4 ± 0.3 on a 35.0 ± 0.3 square** (2.5 from each edge) |
| Inlet | Circular, on the **impeller face** (the face opposite the label) |
| Outlet | On **one side edge**: **28.0 long × 7.7 high** opening, roughly centred along the 40 mm edge. The air-flow arrow on the inlet face points toward the outlet edge |
| Ears | Mounting-ear flange 2.0 / 3.5 thick (per side view) |
| Leads | 3 wires (red +, black −, blue tach), exit from the edge adjacent to the outlet, **150 ± 10 long**, 5.0 strip |
| Perf. | 3.0 CFM, 140 Pa max, 34.5 dBA, 0.16 A (label reads 0.24 A) |

## 7. VIEWE UEED024QV-RH40-A003 (2.4" transflective, CTP)

Source: VIEWE datasheet, §3 Mechanical Drawing (2023-09-04).

| Feature | Value |
|---|---|
| CTP cover-glass outline | **47.32 ± 0.05 × 62.06 ± 0.05** |
| LCM outline | 40.91 ± 0.2 × 57.71 ± 0.2 |
| CTP viewing area | 37.22 ± 0.2 × 49.41 ± 0.2 |
| Active area | **36.72 × 48.96** (240 × 320 @ 0.153) |
| AA position | Centred in X (5.30 per side). In Y it is **3.80 from the edge opposite the FPC** and ≈ 9.30 from the FPC-side edge |
| Thickness | **3.41 ± 0.2 total**: cover glass 0.70 + TP 0.95 + OCA 0.175 + LCM 2.28 ± 0.15 |
| FPC | Exits the short (47.32) edge. It extends **26.39 ± 0.5 beyond the CTP edge** (flat). The tail is **20.50 ± 0.1 wide**, with 40 gold fingers over 19.50 (≈ **0.5 pitch**, 0.30 finger width) and 0.20 thick at the fingers. Components on the FPC are **≤ 1.2 tall**. As shipped the FPC is folded to the rear (27.11 × 9.89 folded tail, 0.80 max over the back) |
| Back | Backlight / sensor OD 41.60 × 57.71 |

## 8. LG INR21700-M58T and 4S1P pack

Source: LG ES product spec (Rev 1.5, 2022-05-31).

| Feature | Value |
|---|---|
| Cell diameter | **21.30–21.80** (mid-body), 21.30–21.70 at the ends. Design to **Ø21.8** |
| Cell height | **70.50–71.00**. Design to **71.0** |
| Mass | ≤ 73.2 g |
| 4S1P, 4 cells side by side (bare) | 4 × 21.8 = **87.2 × 71.0 × 21.8** |
| 4S1P typical finished pack | **[unverified, typical]** with 22–22.5 mm-pitch holders, nickel strip, end fish-paper, BMS on one end and shrink-wrap: **≈ 92 × 78 × 24** (add ≈ 5–8 mm on one end if the BMS PCB is end-mounted, or put the BMS on top: 92 × 72 × 28) |

## 9. TE 5787441-1 (plug) / 787439-1 (receptacle): 5.0 mm-pitch battery interconnect

Source: TE catalog 1773096 pp.231–232.

| Feature | Value |
|---|---|
| 5787441-1 | Keyless, right-angle, straight solder tails, 5 positions on a 5.00 pitch. The family drawing (5796078-1, same keyless RA body) gives **27.02 ± 0.2 long**, tails 3.05 ± 0.3. **[unverified for this exact P/N]** depth ≈ 14.85 (blade projection, from the RA family) and height ≈ 9.95 |
| 787439-1 | Right-hand key, surface mount, 12 V. **33.00 ± 0.05 long × 10.05 deep × 8.00 ± 0.03 high**. Contact window 6.30 ± 0.08 typ, blade slots 9.10 deep, 2.20 ± 0.05 key slot, dovetail locator on the base |

## 10. GCT USB4720-03-A (USB-C 2.0, IP67, mid-mount)

Source: GCT drawing USB4720 Rev B (2023-10-26, PCN 02/01/25).

| Feature | Value |
|---|---|
| Shell OD | **8.34 × 2.56** (mating face), profile 2.13 above / 1.13 offset (mid-mount), body length ≈ 6.50 |
| Gasket | LIM silicone (60A), integral, on the shell behind the face |
| Panel spec | Outer through-slot **8.44 ± 0.03 × 2.66 ± 0.03**, corner R1.05. Inner gasket pocket **9.14 ± 0.03 × 3.35 ± 0.03**, flaring at 10° to 9.64 × 3.86. Pocket depth 0.50 / 0.67 ± 0.03. Wall ≈ **1.80 (ref)**. Gasket compression ≥ 0.20, with ≥ 0.10 radial clearance |
| PCB cut-out | Slot ≈ 9.05 wide between the shell-tab pads (11.30 over the pads). Shell tabs 4 × 1.00 slots |
| Mating plug | Overmold ≤ 6.5 thick. 6.65 clearance to panel face |

## 11. Panasonic capacitors

| Part | Size | Notes |
|---|---|---|
| EEE-FK1H471AM | **Ø16 × 16.5** (code K16) | 470 µF 50 V FK SMD. Seated height ≈ 17 max. Base plate ≈ 17 × 17 **[standard Panasonic K16, unverified]** |
| EEH-ZA1H101P | **Ø10 × 10.2** (code G) | 100 µF 50 V ZA hybrid polymer. Base plate ≈ 10.3 × 10.3 **[standard, unverified]** |

## 12. C&K KSC241JLFS (KSC2, IP67 sealed tact)

| Feature | Value |
|---|---|
| Body | **6.2 × 6.2**, J-lead SMT. ≈ 6.8 over the leads **[unverified]** |
| Height | **3.5 to the actuator top** from the PCB. The soft actuator dome stands ≈ 0.6 above the body |
| Travel / force | 0.5 / 3.5 N (350 gf) |

## 13. Amphenol LTW VENT-PS1YBK-N8001

Source: ALTW drawing VENT-PS1XXX Rev D.

| Feature | Value |
|---|---|
| Thread | **M12 × 1.5**, thread length **10.0** |
| Head | **Ø17.0 cap**, 16 hex. Overall length **15.8** (head ≈ 5.8) |
| Seal | O-ring 10 × 2 (silicone) under the head |
| Panel hole (with nut) | **Ø12.2 ± 0.1 through, panel 2.0–3.5 thick**. Nut APTP-ABKPA012-001 (M12 × 1.5, 18 A/F), 6–8 kgf·cm |
| Threaded alternative | M12 × 1.5 tapped, 10 deep, 60° polished entry chamfer to Ø14.30 ± 0.20 |
| Orientation | Mount vertically or facing down (per drawing) |

## 14. 3M Bumpon SJ5302

**Ø7.9 (0.312") × 2.2 (0.085") high**, clear hemisphere, polyurethane, 75 Shore M.

## 15. Nanuk 920

- **Interior: 381 × 267 × 157** (15.0 × 10.5 × 6.2 in). Lid depth 53, base depth 104.
- Exterior: 424 × 340 × 173.
- **Fit check:** the 240 × 160 × 84 unit fits with 141 × 107 × 73 spare. Laid flat in the base, the 84 mm height uses 81% of the 104 mm base depth. Leave ≥ 10 mm foam on all sides; this fits easily.

## 16. M12 optical-bench stack depth (VC MIPI IMX900 + CIL361)

The stack is built along the optical axis from the camera rear. Image-plane height above the PCB front is **[unverified]** ≈ 1.4 mm (2.0 package minus cover glass and gap). Confirm it with the IMX900 STEP file.

| Element | Δ | Cumulative |
|---|---|---|
| FPC connector rear → PCB back face | 3.9 | 3.9 |
| PCB | 1.54 | 5.4 |
| PCB front → image plane | ≈ 1.4 | 6.8 |
| Image plane → lens front (CIL361, ∞ focus) | 23.6 ± 0.3 | **≈ 30.4** |
| Air gap to window + 2 mm window (assumed) | ≈ 1 + 2 | **≈ 33.5** |

- **PCB back → lens front ≈ 26.5.** **Connector rear → lens front ≈ 30.4.** **Budget a 35 mm optical bench depth** (connector rear to outer window face), plus cable bend room *above* the module (not behind it, because the FPC exits in-plane).
- Generic M12 board-camera stacks run 20–35 mm (holders 6–16.5 mm tall plus lens TTL 15–30). The CIL361 is mid-range.
- The holder must keep its top face below the lens cap: cap underside ≈ 19.2 above the image plane, ≈ 20.6 above the PCB front. This leaves at least 5 mm of thread engagement, so a **10–14 mm holder** is compatible.

---

## Summary table

| Part | L × W × H (mm) | Key features / holes | Source |
|---|---|---|---|
| VC MIPI IMX900 VK000601 | 23.5 × 22.0 × 1.54 PCB. Sensor +2.0 front, FPC conn +3.9 back | 2 × Ø2.2 @ 20.0 pitch on y = 11.0. 2 × Ø1.0 locators. Optical centre ≈ (11.75, 11.0). 22-pin FPC on back, top edge, cable exits up | [VC manual](https://www.mipi-modules.com/fileadmin/external/documentation/hardware/VC_MIPI_Camera_Module/index.html) |
| VK000057 S-mount holder | ≈ 22 × 20 × 12–14 **[unverified]** | M12 × 0.5, 20 mm screw pitch, 15 × 15 × 1.1 filter seat | [VC manual](https://www.mipi-modules.com/fileadmin/external/documentation/hardware/VC_MIPI_Camera_Module/index.html), [Mouser](https://www.mouser.fr/en/ProductDetail/Vision-Components/MIPI-LHLD12?qs=Znm5pLBrcAJI2%2BzumslyRA%3D%3D) |
| Commonlands CIL361-F1.8-M12ANIR | Ø14.0 × 16.8 body. 23.6 front → image plane | M12 × 0.5 × 12.4 thread. MBFL 6.8 (0.4 CG). 7.2 image circle | [Commonlands](https://commonlands.com/products/ir-corrected-6mm-m12-lens-cil361) |
| Vishay VSMA1094250 | 3.4 × 3.4 × 2.895 | Ø3.05 dome. 3 pads × 2.7 L (0.5 / 1.0 / 0.5 W, 0.35 gaps). A = left + centre, K = right | [Vishay 80299](https://www.vishay.com/docs/80299/vsma1094250.pdf) |
| InnoSenT SMR-333 | 21.4 × 15.0 × 3.1 | Antenna on top. 10 castellated pads, 5 per short edge, 2.0 pitch. 43° × 116° | [SMR-3x3 v2.3](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/2525/220201_Data_Sheet_SMR-3X3%20_2.3.pdf) |
| Thundercomm C6490P SoM | **39 × 33 × 2.75** (+ bottom shield) | LGA. Keep-out / max height not public **[unverified: 41 × 35 KO, ≤ 3.0 top]** | [Thundercomm](https://www.thundercomm.com/product/c6490p-som/) |
| Delta BFB0405HHA-TZP4 | **40 × 40 × 10** | 4 × Ø2.4 on 35 sq. Inlet on face, side outlet 28.0 × 7.7. 150 mm leads | [Delta spec](https://www.delta-fan.com/Download/Spec/BFB0405HHA-TZP4.pdf) |
| VIEWE UEED024QV-RH40-A003 | 47.32 × 62.06 × 3.41 (CTP). LCM 40.91 × 57.71 | AA 36.72 × 48.96 (3.80 from non-FPC edge). FPC 20.5 W, 26.39 beyond edge, 40p ≈ 0.5 | [VIEWE datasheet](https://viewedisplay.com/download/73/smart-display-datasheet/6633/ueed024qv-rh40-a003.pdf) |
| LG INR21700-M58T | Ø21.8 × 71.0 (max) | Flat top, ≤ 73.2 g | [LG spec via DNK](https://www.dnkpower.com/wp-content/uploads/2025/09/INR21700M58T-5800mah-datasheet.pdf) |
| 4S1P 21700 pack (side by side) | 87.2 × 71 × 21.8 bare. ≈ 92 × 78 × 24 finished **[unverified]** | BMS on end or top | derived |
| TE 5787441-1 plug | ≈ 27.0 × 14.9 × 10 **[partly unverified]** | Keyless RA, 5p @ 5.00, tails 3.05 | [TE cat. 1773096](https://datasheet.octopart.com/120591-1-TE-Connectivity-datasheet-11547906.pdf) |
| TE 787439-1 receptacle | 33.00 × 10.05 × 8.00 | RH key, SMT, 5p @ 5.00, dovetail locator | [TE cat. 1773096](https://datasheet.octopart.com/120591-1-TE-Connectivity-datasheet-11547906.pdf) |
| GCT USB4720-03-A | 8.34 × 2.56 shell. ≈ 6.5 long. Mid-mount 2.13 / 1.13 | Panel slot 8.44 × 2.66 R1.05. Gasket pocket 9.14 × 3.35 × 0.5–0.67 deep. Wall 1.8. Compression ≥ 0.2 | [GCT drawing](https://gct.co/connector/usb4720) |
| Panasonic EEE-FK1H471AM | Ø16 × 16.5 | Base plate ≈ 17 × 17 **[unverified]** | [Arrow](https://www.arrow.com/en/products/eee-fk1h471am/panasonic) |
| Panasonic EEH-ZA1H101P | Ø10 × 10.2 | Base plate ≈ 10.3 × 10.3 **[unverified]** | [Panasonic](https://na.industrial.panasonic.com/products/capacitors/aluminum-electrolytic-capacitors/lineup/conductive-polymer-hybrid-aluminum-electrolytic/series/79/model/93) |
| C&K KSC241JLFS | 6.2 × 6.2 × 3.5 | J-lead (≈ 6.8 over leads **[unverified]**), IP67, 0.5 travel | [C&K](https://www.ckswitches.com/products/switches/product-details/Tactile/KSC2/KSC241JLFS/) |
| Amphenol LTW VENT-PS1YBK-N8001 | Ø17.0 (16 hex) × 15.8 | M12 × 1.5 × 10 thread. Ø12.2 ± 0.1 hole, 2.0–3.5 wall. O-ring 10 × 2 | [ALTW drawing](https://www.cdiweb.com/datasheets/altw/vent-ps1nbk-n8001%20(d).pdf) |
| 3M Bumpon SJ5302 | Ø7.9 × 2.2 | Hemispherical, clear PU | [3M](https://www.3m.com/3M/sl_SI/p/d/v101668000/) |
| Nanuk 920 | Interior 381 × 267 × 157 (ext. 424 × 340 × 173) | Base depth 104, lid 53. Unit fits | [Nanuk](https://nanuk.com/products/nanuk-920) |
| M12 optical stack (IMX900 + CIL361) | ≈ 26.5 PCB back → lens front. ≈ 30.4 from FPC conn rear | Budget 35 mm bench incl. window | derived from above |

## Open items to close with vendors
- VC: STEP of VK000601 + VK000057 (holder height, IMX900 package / image-plane height).
- Thundercomm: C6490P hardware design guide (LGA land pattern, bottom-shield height, keep-out).
- TE: confirm 5787441-1 body dims and keyless ↔ RH-key mating.
- Commonlands: DocSend STEP for CIL361 (confirm the 23.6 TTL at the chosen focus distance; the golf ball is at ~2–4 m, so the focus shift is ≈ +0.01–0.02 mm).
