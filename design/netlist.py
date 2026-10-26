"""Outer Bounds Pro: complete production netlist (rev A, 2026-10-07).

Every IC uses the datasheet pinout gathered in design/research/Q-pinouts.md and P-power.md.
The "✔ pinout:" note on each IC records where its pinout comes from; "⚠" means the pinout or
values must be confirmed with the vendor (see the open-items list in the design page).

Boards:  CB = main carrier (160x92, 10L)   LB = LED strobe board (x3, identical, drawn once)
         RH = radar head (x2, identical, drawn once)   BP = battery pack board (in the smart pack)
"""
from schematic import Design

D = Design()
R, C, L, FB = (lambda *a, **k: D.two("R", *a, **k)), (lambda *a, **k: D.two("C", *a, **k)), (lambda *a, **k: D.two("L", *a, **k)), (lambda *a, **k: D.two("FB", *a, **k))
DI, LED = (lambda *a, **k: D.two("D", *a, **k)), (lambda *a, **k: D.two("LED", *a, **k))
OK = "✔ pinout: "

# =====================================================================================================
D.sheet("CB-01", "USB-C 65 W PD input · battery connector", "USB-C PD sink, VBUS protection, battery pack interface")
S = "CB-01"; K = "USB-C receptacle & ESD"
D.ic("J1", "USB-C receptacle IP67 (USB 2.0)", "USB4720-03-A", "GCT", "USB4720 mid-mount", S, K,
     [("A4", "VBUS", "VBUS_C"), ("A9", "VBUS", "VBUS_C"), ("B4", "VBUS", "VBUS_C"), ("B9", "VBUS", "VBUS_C"), ("A5", "CC1", "CC1"), ("B5", "CC2", "CC2")],
     [("A6", "D+", "USB_DP"), ("B6", "D+", "USB_DP"), ("A7", "D-", "USB_DN"), ("B7", "D-", "USB_DN"), ("A8", "SBU1", "NC"), ("B8", "SBU2", "NC"),
      ("A1", "GND", "GND"), ("A12", "GND", "GND"), ("B1", "GND", "GND"), ("B12", "GND", "GND"), ("SH", "SHELL", "GND")],
     note=OK + "GCT drawing USB4720 rev B", price=1.46)
D.ic("D1", "22 V flat-clamp TVS", "TVS2200DRVR", "TI", "WSON-6", S, K, [("1", "IN", "VBUS_C")], [("2", "GND", "GND")], note="✔ TI ref. design (TPS25751 Fig. 9-26)", price=0.38)
D.ic("U3", "USB2 + CC ESD array", "TPD4E05U06DQAR", "TI", "USON-10", S, K, [("1", "IO1", "USB_DP"), ("2", "IO2", "USB_DN"), ("4", "IO3", "CC1"), ("5", "IO4", "CC2")], [("3", "GND", "GND")], note="⚠ confirm USON-10 pin map", price=0.22)
for i in range(4):
    C(f"C{100+i}", "10nF 50V", "VBUS_C", "GND", S, K, fp="0402", mpn="GRM155R71H103KA88D", mfr="Murata", price=0.01)
K = "USB-C PD sink controller (TPS25751D, integrated 5 A load switch)"
D.ic("U1", "USB PD 3.1 sink controller, 20 V/5 A switch", "TPS25751DREFR", "TI", "WQFN-38 4x6", S, K,
     [("23", "VBUS_IN", "VBUS_C"), ("24", "VBUS_IN", "VBUS_C"), ("25", "VBUS_IN", "VBUS_C"), ("32", "VBUS", "VBUS_C"), ("33", "VBUS", "VBUS_C"),
      ("28", "CC1", "CC1"), ("29", "CC2", "CC2"), ("26", "GPIO4/USB_P", "GND"), ("27", "GPIO5/USB_N", "GND"),
      ("34", "PP5V", "5V0"), ("35", "PP5V", "5V0"), ("38", "VIN_3V3", "3V3"), ("2", "ADCIN1", "PD_LDO3V3"), ("3", "ADCIN2", "PD_LDO1V5"),
      ("8", "I2Ct_SDA", "I2C_SYS_SDA"), ("9", "I2Ct_SCL", "I2C_SYS_SCL"), ("10", "I2Ct_IRQ", "PD_IRQ_N")],
     [("20", "PPHV", "VBUS_SNK"), ("21", "PPHV", "VBUS_SNK"), ("22", "PPHV", "VBUS_SNK"), ("1", "LDO_3V3", "PD_LDO3V3"), ("4", "LDO_1V5", "PD_LDO1V5"),
      ("16", "I2Cc_SDA", "PD_EE_SDA"), ("17", "I2Cc_SCL", "PD_EE_SCL"), ("18", "I2Cc_IRQ", "PD_EE_IRQ"),
      ("15", "DRAIN", "PD_DRAIN"), ("30", "DRAIN", "PD_DRAIN"), ("40", "DRAIN_PAD", "PD_DRAIN"),
      ("5", "GPIO0", "GND"), ("6", "GPIO1", "GND"), ("7", "GPIO2", "GND"), ("13", "GPIO11", "GND"), ("19", "GPIO3", "GND"), ("36", "GPIO7", "GND"), ("37", "GPIO6", "GND"),
      ("11", "GND", "GND"), ("12", "GND", "GND"), ("14", "GND", "GND"), ("31", "GND", "GND"), ("39", "GND_PAD", "GND")],
     note=OK + "SLVSH93A Table 5-1 · strap AlwaysEnableSink (SoM hosts charger)", price=1.80)
D.ic("U4", "512 kbit I2C EEPROM (PD firmware patch)", "24LC512T-I/SN", "Microchip", "SOIC-8", S, K,
     [("1", "A0", "GND"), ("2", "A1", "GND"), ("3", "A2", "GND"), ("7", "WP", "GND")], [("5", "SDA", "PD_EE_SDA"), ("6", "SCL", "PD_EE_SCL"), ("8", "VCC", "PD_LDO3V3"), ("4", "VSS", "GND")],
     note=OK + "Microchip 24LC512 DS · addr 0x50", price=0.95)
for ref, v, n1, n2, fp, mpn in [("C110", "10uF 10V", "3V3", "GND", "0603", "GRM188R61A106KE69D"), ("C111", "10uF 10V", "PD_LDO3V3", "GND", "0603", "GRM188R61A106KE69D"),
                                ("C112", "10uF 10V", "PD_LDO1V5", "GND", "0603", "GRM188R61A106KE69D"), ("C113", "4.7uF 35V", "VBUS_C", "GND", "0805", "GRM21BR6YA475KE15L"),
                                ("C114", "22uF 35V", "VBUS_SNK", "GND", "1206", "GRM31CR6YA226ME11L"), ("C115", "10uF 10V", "5V0", "GND", "0805", "GRM21BR61A106KE19L"),
                                ("C116", "390pF C0G", "CC1", "GND", "0402", "GRM1555C1H391JA01D"), ("C117", "390pF C0G", "CC2", "GND", "0402", "GRM1555C1H391JA01D")]:
    C(ref, v, n1, n2, S, K, fp=fp, mpn=mpn, mfr="Murata", price=0.03)
for ref, v, n1, n2 in [("R100", "2.2k", "PD_EE_SDA", "PD_LDO3V3"), ("R101", "2.2k", "PD_EE_SCL", "PD_LDO3V3"), ("R102", "10k", "PD_EE_IRQ", "PD_LDO3V3"), ("R103", "10k", "PD_IRQ_N", "3V3")]:
    R(ref, v, n1, n2, S, K, mpn="RC0402FR-07" + v.replace(".", "K").replace("k", "K") + "L", mfr="Yageo", price=0.003)
K = "Battery pack connector (smart pack: SMBus, presence)"
D.ic("J3", "Battery interconnect header 5-pos 5.0 mm", "5787441-1", "TE", "TH R/A", S, K,
     [("1", "PACK+", "VBAT_PACK"), ("2", "SMBC", "SMB_CLK"), ("3", "SMBD", "SMB_DAT")], [("4", "PRES", "BAT_PRES_N"), ("5", "PACK-", "GND")],
     note="⚠ TE: confirm keyed mate for 787439-1 (polarisation)", price=4.71)
D.ic("D2", "Pack-side TVS 24 V", "SMBJ20A", "Littelfuse", "SMB", S, K, [("1", "K", "VBAT_PACK")], [("2", "A", "GND")], note="✔ uni-directional TVS", price=0.12)
D.ic("U5", "SMBus ESD 2-ch", "TPD2E2U06DRLR", "TI", "SOT-5X3", S, K, [("1", "IO1", "SMB_CLK"), ("3", "IO2", "SMB_DAT")], [("2", "GND", "GND")], note="⚠ confirm SOT-5X3 pin map", price=0.15)
R("R104", "10k", "BAT_PRES_N", "3V3", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
R("R105", "2.2k", "SMB_CLK", "3V3", S, K, mpn="RC0402FR-072K2L", mfr="Yageo", price=0.003)
R("R106", "2.2k", "SMB_DAT", "3V3", S, K, mpn="RC0402FR-072K2L", mfr="Yageo", price=0.003)

# =====================================================================================================
D.sheet("CB-02", "Battery charger & system power path (BQ25730, 4S, 400 kHz)", "Buck-boost NVDC charger, BATFET, current sense")
S = "CB-02"; K = "BQ25730 charger controller"
D.ic("U2", "1-5S buck-boost NVDC charger", "BQ25730RSNR", "TI", "WQFN-32 4x4", S, K,
     [("1", "VBUS", "CHG_VBUSF"), ("3", "ACP", "CHG_ACP"), ("2", "ACN", "CHG_ACN"), ("20", "SRP", "CHG_SRP_F"), ("19", "SRN", "CHG_SRN"),
      ("6", "ILIM_HIZ", "CHG_ILIM"), ("18", "CELL_BATPRESZ", "CHG_CELL"), ("8", "IADPT", "CHG_IADPT"), ("9", "IBAT", "CHG_IBAT"), ("10", "PSYS", "CHG_PSYS"),
      ("12", "SDA", "I2C_SYS_SDA"), ("13", "SCL", "I2C_SYS_SCL"), ("4", "CHRG_OK", "CHRG_OK"), ("11", "PROCHOT", "PROCHOT_N"),
      ("5", "OTG/VAP/FRS", "CHG_OTG"), ("14", "CMPIN", "GND"), ("15", "CMPOUT", "NC"), ("16", "COMP1", "CHG_COMP1"), ("17", "COMP2", "CHG_COMP2")],
     [("31", "HIDRV1", "CHG_HD1"), ("32", "SW1", "CHG_SW1"), ("30", "BTST1", "CHG_BT1"), ("29", "LODRV1", "CHG_LD1"),
      ("24", "HIDRV2", "CHG_HD2"), ("23", "SW2", "CHG_SW2"), ("25", "BTST2", "CHG_BT2"), ("26", "LODRV2", "CHG_LD2"),
      ("22", "VSYS", "VSYS"), ("21", "BATDRV", "CHG_BATDRV"), ("28", "REGN", "REGN"), ("7", "VDDA", "VDDA_CHG"), ("27", "PGND", "GND"), ("EP", "PAD", "GND")],
     note=OK + "SLUSE65A Table 6-1 · I2C 0x6B · hosted by SoM", price=2.80)
K = "Power stage (4x N-FET, P-FET BATFET, inductor, sense)"
R("R110", "5mR 1W", "VBUS_SNK", "CHG_VIN", S, K, fp="1206", mpn="WSLP12065L000FEA", mfr="Vishay", price=0.35, note="RAC input sense")
D.fet("Q1", "30V 6.3mR buck HS", "CSD17578Q3A", "TI", "SON3x3", "CHG_VIN", "CHG_HD1", "CHG_SW1", S, K, price=0.25)
D.fet("Q2", "30V 6.3mR buck LS", "CSD17578Q3A", "TI", "SON3x3", "CHG_SW1", "CHG_LD1", "GND", S, K, price=0.25)
D.fet("Q3", "30V 6.3mR boost LS", "CSD17578Q3A", "TI", "SON3x3", "CHG_SW2", "CHG_LD2", "GND", S, K, price=0.25)
D.fet("Q4", "30V 6.3mR boost HS", "CSD17578Q3A", "TI", "SON3x3", "VSYS", "CHG_HD2", "CHG_SW2", S, K, price=0.25)
L("L1", "4.7uH 13A", "CHG_SW1", "CHG_SW2", S, K, fp="10x10", mpn="BMQADY1010404R7MA1", mfr="Chilisin", price=0.95)
D.fet("Q5", "-30V BATFET (P-ch) · S=VSYS, D=battery", "AON6407", "AOS", "DFN5x6", "CHG_SRP", "CHG_BATDRV", "VSYS", S, K, price=0.42, ptype=True)
R("R111", "5mR 1W", "CHG_SRP", "VBAT_PACK", S, K, fp="1206", mpn="WSLP12065L000FEA", mfr="Vishay", price=0.35, note="RSR charge sense")
K = "Charger passives (values per P-power.md §2)"
for ref, v, a, b, fp, mpn in [
    ("R112", "4.99R", "VBUS_SNK", "CHG_ACP", "0603", "CRCW06034R99FKEA"), ("R113", "4.99R", "CHG_VIN", "CHG_ACN", "0603", "CRCW06034R99FKEA"),
    ("R114", "1R", "VBUS_SNK", "CHG_VBUSF", "0805", "CRCW08051R00JNEA"), ("R115", "10R", "REGN", "VDDA_CHG", "0603", "CRCW060310R0JNEA"),
    ("R116", "10R", "CHG_SRP", "CHG_SRP_F", "1206", "ERJ-8ENF10R0V"), ("R117", "10R", "VBAT_PACK", "CHG_SRN", "1206", "ERJ-8ENF10R0V"),
    ("R118", "191k 1%", "CHG_IADPT", "GND", "0603", "CRCW0603191KFKEA"), ("R119", "30.1k 1%", "CHG_PSYS", "GND", "0603", "CRCW060330K1FKEA"),
    ("R120", "300k 1%", "VDDA_CHG", "CHG_ILIM", "0603", "CRCW0603300KFKEA"), ("R121", "113k 1%", "CHG_ILIM", "GND", "0603", "CRCW0603113KFKEA"),
    ("R122", "100k 1%", "VDDA_CHG", "CHG_CELL", "0603", "CRCW0603100KFKEA"), ("R123", "301k 1%", "CHG_CELL", "GND", "0603", "CRCW0603301KFKEA"),
    ("R124", "40.2k", "CHG_COMP1", "CHG_C1N", "0402", "CRCW040240K2FKED"), ("R125", "15.0k", "CHG_COMP2", "CHG_C2N", "0402", "CRCW040215K0FKED"),
    ("R126", "10k", "CHRG_OK", "3V3", "0402", "RC0402FR-0710KL"), ("R127", "10k", "PROCHOT_N", "3V3", "0402", "RC0402FR-0710KL"),
    ("R128", "100k", "CHG_OTG", "GND", "0402", "RC0402FR-07100KL")]:
    R(ref, v, a, b, S, K, fp=fp, mpn=mpn, mfr="Vishay/Yageo", price=0.01)
for ref, v, a, b, fp, mpn in [
    ("C120", "33nF 50V", "CHG_ACP", "GND", "0603", "GRM188R71H333KA61D"), ("C121", "33nF 50V", "CHG_ACN", "GND", "0603", "GRM188R71H333KA61D"),
    ("C122", "10nF 50V", "CHG_ACP", "CHG_ACN", "0603", "C0603C103J5RACTU"), ("C123", "0.47uF 50V", "CHG_VBUSF", "GND", "0805", "C2012X7R1H474K125AB"),
    ("C124", "47nF 25V", "CHG_BT1", "CHG_SW1", "0603", "GRM188R71E473KA01D"), ("C125", "47nF 25V", "CHG_BT2", "CHG_SW2", "0603", "GRM188R71E473KA01D"),
    ("C126", "2.2uF 35V", "REGN", "GND", "0603", "GRM188R6YA225KA12D"), ("C127", "1uF 35V", "VDDA_CHG", "GND", "0603", "CGA3E1X7R1V105K080AC"),
    ("C128", "0.1uF 50V", "CHG_SRP_F", "CHG_SRN", "0603", "CGA3E2X7R1H104K080AA"), ("C129", "100pF C0G", "CHG_IADPT", "GND", "0603", "C0603C101J5GAC"),
    ("C130", "100pF C0G", "CHG_IBAT", "GND", "0603", "C0603C101J5GAC"), ("C131", "100pF C0G", "CHG_PSYS", "GND", "0603", "C0603C101J5GAC"),
    ("C132", "4.7nF", "CHG_C1N", "GND", "0402", "GRM155R71H472KA01D"), ("C133", "33pF C0G", "CHG_COMP1", "GND", "0402", "GRM1555C1H330JA01D"),
    ("C134", "680pF C0G", "CHG_C2N", "GND", "0402", "GRM1555C1H681JA01D"), ("C135", "15pF C0G", "CHG_COMP2", "GND", "0402", "GRM1555C1H150JA01D"),
    ("C136", "10nF+1nF", "CHG_VIN", "GND", "0603", "C0603C103J5RACTU")]:
    C(ref, v, a, b, S, K, fp=fp, mpn=mpn, mfr="Murata/KEMET/TDK", price=0.02)
for i in range(6):
    C(f"C{140+i}", "10uF 35V", "VBUS_SNK", "GND", S, K, fp="0805", mpn="GRM21BR6YA106KE43L", mfr="Murata", price=0.06)
for i in range(7):
    C(f"C{150+i}", "10uF 35V", "VSYS", "GND", S, K, fp="0805", mpn="GRM21BR6YA106KE43L", mfr="Murata", price=0.06)
C("C157", "33uF 35V Ta-poly", "VSYS", "GND", S, K, fp="7343", mpn="T521D336M035ATE065", mfr="KEMET", price=0.85)
C("C158", "33uF 35V Ta-poly", "VSYS", "GND", S, K, fp="7343", mpn="T521D336M035ATE065", mfr="KEMET", price=0.85)
C("C159", "10uF 35V", "VBAT_PACK", "GND", S, K, fp="0805", mpn="GRM21BR6YA106KE43L", mfr="Murata", price=0.06)
C("C160", "10uF 35V", "VBAT_PACK", "GND", S, K, fp="0805", mpn="GRM21BR6YA106KE43L", mfr="Murata", price=0.06)

# =====================================================================================================
D.sheet("CB-03", "System rails: 3V8 SoM · 5V0 · 3V3 · camera 3V3", "Bucks off VSYS (12.3–16.8 V)")
S = "CB-03"

def buck56637(ref, out, rtop, lref, sfx, cluster, pg, en):
    D.ic(ref, f"6 A D-CAP3 buck → {out}", "TPS56637RPAR", "TI", "VQFN-HR 3x3", S, cluster,
         [("8", "VIN", "VSYS"), ("1", "EN", en), ("10", "MODE", "GND"), ("3", "AGND", "GND")],
         [("6", "SW", f"SW_{sfx}"), ("7", "BOOT", f"BT_{sfx}"), ("2", "FB", f"FB_{sfx}"), ("4", "PG", pg), ("5", "NC", "NC"), ("9", "PGND", "GND")],
         note=OK + "SLVSEG1A · fsw 500 kHz, VREF 0.6 V", price=1.41)
    L(lref, "3.3uH 10A", f"SW_{sfx}", out, S, cluster, fp="8.6x8.6", mpn="IHLP3232DZER3R3M11", mfr="Vishay", price=0.70)
    C(f"C{lref[1:]}0", "0.1uF", f"BT_{sfx}", f"SW_{sfx}", S, cluster, fp="0402", mpn="GRM155R71H104KE14D", mfr="Murata", price=0.01)
    R(f"R{lref[1:]}0", rtop, out, f"FB_{sfx}", S, cluster, mpn="CRCW0402" + rtop.split()[0].replace(".", "K").replace("k", "K") + "FKED", mfr="Vishay", price=0.01)
    R(f"R{lref[1:]}1", "10.0k 1%", f"FB_{sfx}", "GND", S, cluster, mpn="CRCW040210K0FKED", mfr="Vishay", price=0.01)
    for i in range(3):
        C(f"C{lref[1:]}{i+1}", "10uF 50V", "VSYS", "GND", S, cluster, fp="1206", mpn="CGA5L1X7R1H106K160AC", mfr="TDK", price=0.12)
    for i in range(2):
        C(f"C{lref[1:]}{i+4}", "22uF 25V", out, "GND", S, cluster, fp="1210", mpn="GRM32ER71E226KE15L", mfr="Murata", price=0.15)

K = "3V8_SOM: Qualcomm VPH_PWR, 6 A"
buck56637("U15", "3V8_SOM", "53.6k 1%", "L20", "3V8", K, "PG_3V8", "EN_3V8")
R("R203", "115k 1%", "VSYS", "EN_3V8", S, K, mpn="CRCW0402115KFKED", mfr="Vishay", price=0.01)
R("R204", "14.3k 1%", "EN_3V8", "GND", S, K, mpn="CRCW040214K3FKED", mfr="Vishay", price=0.01)
R("R202", "100k", "PG_3V8", "3V3", S, K, mpn="RC0402FR-07100KL", mfr="Yageo", price=0.003)
K = "5V0: blower, PD PP5V, display backlight, 3 A"
buck56637("U11", "5V0", "73.2k 1%", "L21", "5V0", K, "PG_5V0", "EN_5V0")
R("R213", "115k 1%", "VSYS", "EN_5V0", S, K, mpn="CRCW0402115KFKED", mfr="Vishay", price=0.01)
R("R214", "14.3k 1%", "EN_5V0", "GND", S, K, mpn="CRCW040214K3FKED", mfr="Vishay", price=0.01)
R("R212", "100k", "PG_5V0", "3V3", S, K, mpn="RC0402FR-07100KL", mfr="Yageo", price=0.003)

def buck62933(ref, out, rtop, lref, sfx, cluster):
    D.ic(ref, f"3 A buck → {out}", "TPS62933DRLR", "TI", "SOT-583", S, cluster,
         [("3", "VIN", "VSYS"), ("2", "EN", f"EN_{sfx}"), ("1", "RT", "NC"), ("7", "SS", f"SS_{sfx}")],
         [("5", "SW", f"SW_{sfx}"), ("6", "BST", f"BT_{sfx}"), ("8", "FB", f"FB_{sfx}"), ("4", "GND", "GND")],
         note=OK + "SLUSEA4D · 500 kHz (RT open), VREF 0.8 V", price=0.85)
    L(lref, "6.8uH 10A", f"SW_{sfx}", out, S, cluster, fp="6030", mpn="74439346068", mfr="Würth", price=0.55)
    C(f"C{lref[1:]}0", "100nF", f"BT_{sfx}", f"SW_{sfx}", S, cluster, fp="0402", mpn="GRM155R71H104KE14D", mfr="Murata", price=0.01)
    C(f"C{lref[1:]}1", "15nF", f"SS_{sfx}", "GND", S, cluster, fp="0402", mpn="GRM155R71H153KA12D", mfr="Murata", price=0.01)
    R(f"R{lref[1:]}0", rtop, out, f"FB_{sfx}", S, cluster, mpn="RT0402DRE0731K2L", mfr="Yageo", price=0.02)
    R(f"R{lref[1:]}1", "10.0k 0.5%", f"FB_{sfx}", "GND", S, cluster, mpn="RT0402DRE0710KL", mfr="Yageo", price=0.02)
    R(f"R{lref[1:]}2", "464k 1%", "VSYS", f"EN_{sfx}", S, cluster, mpn="CRCW0402464KFKED", mfr="Vishay", price=0.01)
    R(f"R{lref[1:]}3", "57.6k 1%", f"EN_{sfx}", "GND", S, cluster, mpn="CRCW040257K6FKED", mfr="Vishay", price=0.01)
    for i in range(2):
        C(f"C{lref[1:]}{i+2}", "10uF 50V", "VSYS", "GND", S, cluster, fp="1206", mpn="CGA5L1X7R1H106K160AC", mfr="TDK", price=0.12)
    for i in range(3):
        C(f"C{lref[1:]}{i+5}", "22uF 16V", out, "GND", S, cluster, fp="1206", mpn="C3216X5R1V226M160AC", mfr="TDK", price=0.10)

K = "3V3: MCUs, sensors, I/O pull-ups, PD VIN_3V3"
buck62933("U12", "3V3", "31.2k 0.5%", "L22", "3V3", K)
K = "3V3_CAM: three IMX900 modules (3x 230 mA max) — separate quiet rail"
buck62933("U13", "3V3_CAM", "31.2k 0.5%", "L23", "3V3C", K)
FB("FB230", "600R@100MHz 3A", "3V3_CAM", "3V3_CAM_F", S, K, fp="0805", mpn="BLM21PG601SN1D", mfr="Murata", price=0.04)

# =====================================================================================================
D.sheet("CB-04", "Compute module: Thundercomm C6490P (QCS6490) · interfaces", "SoM pin-level detail is under NDA (Thundercomm HW design guide); carrier nets shown by function")
S = "CB-04"; K = "SoM U10 — carrier-side interface (functional pin groups)"
NDA = "⚠ ball numbers per Thundercomm C6490P HW design guide (NDA); nets final"
D.ic("U10.A", "QCS6490 SoM — power, boot, USB, RF", "C6490P-U8A-3690000", "Thundercomm", "LGA 39x33", S, K,
     [("VPH", "VPH_PWR (3.4–4.5 V)", "3V8_SOM"), ("PON", "KYPD_PWR_N", "PWR_BTN_N"), ("RST", "RESIN_N", "TP_SOM_RESIN_N"), ("DP", "USB2_DP", "USB_DP"), ("DM", "USB2_DM", "USB_DN"),
      ("FB", "FORCE_USB_BOOT", "TP_SOM_EDL")],
     [("ANT0", "WLAN/BT ANT0", "RF_ANT0"), ("ANT1", "WLAN ANT1", "RF_ANT1"), ("DBGTX", "DEBUG_UART_TX", "TP_SOM_DBG_TX"), ("DBGRX", "DEBUG_UART_RX", "TP_SOM_DBG_RX"), ("GND", "GND (all)", "GND")],
     note=NDA, price=189.60)
D.ic("U10.B", "QCS6490 SoM — MIPI CSI ×3 + CCI", "C6490P-U8A-3690000", "Thundercomm", "LGA 39x33", S, K,
     [(f"C{c}{x}", f"CSI{c}_{x}", f"CSI{c}_{x}") for c in range(3) for x in ("D0P", "D0N", "D1P", "D1N", "CKP", "CKN")],
     [(f"C{c}{x}", f"CSI{c}_{x}", f"CSI{c}_{x}") for c in range(3) for x in ("D2P", "D2N", "D3P", "D3N")] + [("CCISDA", "CCI_I2C_SDA0", "I2C_CAM_SDA"), ("CCISCL", "CCI_I2C_SCL0", "I2C_CAM_SCL")],
     note=NDA)
D.ic("U10.C", "QCS6490 SoM — QUP serial engines", "C6490P-U8A-3690000", "Thundercomm", "LGA 39x33", S, K,
     [("S0CK", "QUP SPI0_CLK", "HOST_SPI_SCK"), ("S0MO", "QUP SPI0_MOSI", "HOST_SPI_MOSI"), ("S0MI", "QUP SPI0_MISO", "HOST_SPI_MISO"), ("S0CS", "QUP SPI0_CS0", "HOST_SPI_CS_N"),
      ("U1TX", "QUP UART1_TX", "MCU_UART_RX"), ("U1RX", "QUP UART1_RX", "MCU_UART_TX"), ("U2TX", "QUP UART2_TX", "RAD_UART_RX"), ("U2RX", "QUP UART2_RX", "RAD_UART_TX")],
     [("I1SDA", "QUP I2C1_SDA", "I2C_SYS_SDA"), ("I1SCL", "QUP I2C1_SCL", "I2C_SYS_SCL"), ("I3SDA", "QUP I2C3_SDA (SMBus pack)", "SMB_DAT"), ("I3SCL", "QUP I2C3_SCL (SMBus pack)", "SMB_CLK"),
      ("S4CK", "QUP SPI4_CLK", "UI_SCK"), ("S4MO", "QUP SPI4_MOSI", "UI_MOSI"), ("S4MI", "QUP SPI4_MISO", "UI_MISO"), ("S4CS0", "QUP SPI4_CS0", "DISP_CS_N"), ("S4CS1", "QUP SPI4_CS1", "INCL_CS_N")],
     note=NDA)
D.ic("U10.D", "QCS6490 SoM — GPIO, PWM, ADC", "C6490P-U8A-3690000", "Thundercomm", "LGA 39x33", S, K,
     [("G1", "GPIO in", "MCU_IRQ_N"), ("G2", "GPIO in", "PD_IRQ_N"), ("G3", "GPIO in", "CHRG_OK"), ("G4", "GPIO in", "PROCHOT_N"), ("G5", "GPIO in", "IMU_INT1"),
      ("G6", "GPIO in", "BAT_PRES_N"), ("G7", "GPIO in", "STROBE_FLT_N"), ("G8", "GPIO in", "STROBE_PG"), ("G9", "GPIO in", "FAN_TACH"), ("G10", "GPIO in", "BTN_MODE_N"),
      ("G11", "GPIO in", "BTN_LR_N"), ("A1", "PMIC ADC (IBAT)", "CHG_IBAT"), ("A2", "PMIC ADC (PSYS)", "CHG_PSYS")],
     [("G20", "GPIO out (OD)", "MCU_NRST"), ("G21", "GPIO out", "MCU_BOOT0"), ("G22", "GPIO out", "STROBE_EN_SOM"), ("G23", "PWM", "FAN_PWM"), ("G24", "GPIO out", "DISP_DC"),
      ("G25", "GPIO out", "DISP_RST_N"), ("G26", "PWM", "BL_PWM"), ("G27", "GPIO out", "LED_R_DRV"), ("G28", "GPIO out", "LED_G_DRV"), ("G29", "GPIO out", "LED_B_DRV"),
      ("G30", "GPIO out", "BZ_GATE"), ("G31", "GPIO out", "CAM_MUX_RST_N"), ("G32", "GPIO out (OD)", "RAD_NRST"), ("G33", "GPIO out", "RAD_BSL")],
     note=NDA)
for i in range(4):
    C(f"C{300+i}", "22uF 10V", "3V8_SOM", "GND", S, K, fp="0805", mpn="GRM21BR61A226ME44L", mfr="Murata", price=0.08, note="≤100 µF total incl. SoM (TPS56637 D-CAP3 limit)")
D.ic("J4", "U.FL receptacle ×2 (antennas EFB2455A3S-20MHF1)", "U.FL-R-SMT-1(10)", "Hirose", "U.FL", S, K, [("1", "ANT0", "RF_ANT0")], [("2", "ANT1", "RF_ANT1")], note="✔ Hirose U.FL", price=2.04)
K = "I2C system bus fan-out (TCA9546A mux isolates camera CCI addresses)"
D.ic("U14", "4-ch I2C mux (3 camera CCI + spare)", "TCA9546APWR", "TI", "TSSOP-16", S, K,
     [("15", "SDA", "I2C_CAM_SDA"), ("14", "SCL", "I2C_CAM_SCL"), ("1", "A0", "GND"), ("2", "A1", "GND"), ("13", "A2", "GND"), ("3", "RESET", "CAM_MUX_RST_N"), ("16", "VCC", "3V3")],
     [("4", "SD0", "CAM1_SDA"), ("5", "SC0", "CAM1_SCL"), ("6", "SD1", "CAM2_SDA"), ("7", "SC1", "CAM2_SCL"), ("9", "SD2", "CAM3_SDA"), ("10", "SC2", "CAM3_SCL"),
      ("11", "SD3", "NC"), ("12", "SC3", "NC"), ("8", "GND", "GND")], note=OK + "SCPS205B · addr 0x70", price=0.62)
for ref, n in [("R310", "CAM1_SDA"), ("R311", "CAM1_SCL"), ("R312", "CAM2_SDA"), ("R313", "CAM2_SCL"), ("R314", "CAM3_SDA"), ("R315", "CAM3_SCL"),
               ("R316", "I2C_CAM_SDA"), ("R317", "I2C_CAM_SCL"), ("R318", "I2C_SYS_SDA"), ("R319", "I2C_SYS_SCL"), ("R320", "CAM_MUX_RST_N")]:
    R(ref, "2.2k" if "RST" not in n else "10k", n, "3V3", S, K, mpn="RC0402FR-072K2L", mfr="Yageo", price=0.003)
C("C320", "100nF", "3V3", "GND", S, K, mpn="GRM155R71H104KE14D", mfr="Murata", price=0.01)
K = "Power button, status, buzzer, blower"
D.ic("SW1", "IP67 tact switch — POWER", "KSC241JLFS", "C&K", "6.2x6.2 J-lead", S, K, [("1", "A", "PWR_BTN_N")], [("2", "B", "GND")], note=OK + "C&K KSC2", price=0.28)
D.ic("SW2", "IP67 tact switch — MODE", "KSC241JLFS", "C&K", "6.2x6.2 J-lead", S, K, [("1", "A", "BTN_MODE_N")], [("2", "B", "GND")], note=OK + "C&K KSC2", price=0.28)
D.ic("SW3", "IP67 tact switch — L/R handedness", "KSC241JLFS", "C&K", "6.2x6.2 J-lead", S, K, [("1", "A", "BTN_LR_N")], [("2", "B", "GND")], note=OK + "C&K KSC2", price=0.28)
D.ic("LED1", "RGB status LED (common anode)", "150141M173100", "Würth", "PLCC-4", S, K, [("1", "A", "3V3")], [("2", "R", "LED_R_K"), ("3", "G", "LED_G_K"), ("4", "B", "LED_B_K")], note="⚠ confirm Würth PLCC-4 pin order", price=0.34)
for ref, n, d in [("R330", "LED_R_K", "LED_R_DRV"), ("R331", "LED_G_K", "LED_G_DRV"), ("R332", "LED_B_K", "LED_B_DRV")]:
    R(ref, "220R", n, d, S, K, mpn="RC0402FR-07220RL", mfr="Yageo", price=0.003, note="drive low = on (open-drain)")
D.ic("BZ1", "SMT magnetic buzzer 4 kHz", "CMT-8540S-SMT-TR", "Same Sky", "8.5x8.5", S, K, [("1", "+", "5V0")], [("2", "-", "BZ_DRV")], note=OK + "Same Sky CMT-8540S", price=1.92)
D.fet("Q30", "Buzzer driver", "2N7002K", "Nexperia", "SOT-23", "BZ_DRV", "BZ_GATE", "GND", S, K, price=0.03)
DI("D30", "BAS16 flyback", "BZ_DRV", "5V0", S, K, fp="SOD-323", mpn="BAS16J", mfr="Nexperia", price=0.02)
D.ic("J5", "Blower connector JST GH 4-pos (Delta BFB0405HHA-TZP4)", "BM04B-GHS-TBT", "JST", "GH 1.25", S, K,
     [("1", "+5V", "5V0"), ("2", "GND", "GND")], [("3", "TACH", "FAN_TACH"), ("4", "PWM", "FAN_PWM")], note=OK + "Delta spec: 4-wire 5 V PWM", price=0.25)
R("R333", "10k", "FAN_TACH", "3V3", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)

# =====================================================================================================
D.sheet("CB-05", "Camera connectors ×3 (VC MIPI IMX900) · trigger/flash routing", "22-pin 0.5 mm FPC, Raspberry Pi pinout; trigger from STM32 HRTIM")
S = "CB-05"
for n, (ref, csi, trig, flash, sda, scl) in enumerate([("J10", "CSI0", "CAM1_TRIG", "CAM1_FLASH", "CAM1_SDA", "CAM1_SCL"),
                                                       ("J11", "CSI1", "CAM2_TRIG", "CAM2_FLASH", "CAM2_SDA", "CAM2_SCL"),
                                                       ("J12", "CSI2", "CAM3_TRIG", "CAM3_FLASH", "CAM3_SDA", "CAM3_SCL")], start=1):
    K = f"{ref}: camera {n} ({['stereo top CAM-T', 'stereo bottom CAM-B', 'club CAM-C'][n-1]}) — VK000601 IMX900 mono"
    D.ic(ref, "FFC/FPC 22-pos 0.5 mm R/A, bottom contact", "FH12-22S-0.5SH(55)", "Hirose", "FH12", S, K,
         [("2", "D0-", f"{csi}_D0N"), ("3", "D0+", f"{csi}_D0P"), ("5", "D1-", f"{csi}_D1N"), ("6", "D1+", f"{csi}_D1P"), ("8", "CK-", f"{csi}_CKN"), ("9", "CK+", f"{csi}_CKP"),
          ("11", "D2-", f"{csi}_D2N"), ("12", "D2+", f"{csi}_D2P"), ("14", "D3-", f"{csi}_D3N"), ("15", "D3+", f"{csi}_D3P")],
         [("17", "TRIGGER_IN", f"{trig}_C"), ("18", "FLASH_OUT", flash), ("20", "SCL", scl), ("21", "SDA", sda), ("22", "VCC 3V3", "3V3_CAM_F"),
          ("1", "GND", "GND"), ("4", "GND", "GND"), ("7", "GND", "GND"), ("10", "GND", "GND"), ("13", "GND", "GND"), ("16", "GND", "GND"), ("19", "GND", "GND")],
         note=OK + "VC MIPI manual §1.4.1 = RPi 22-pin; order pin-n→pin-n cable", price=1.10)
    R(f"R5{n}0", "33R", trig, f"{trig}_C", S, K, mpn="RC0402FR-0733RL", mfr="Yageo", price=0.003, note="series termination, 100 mm FPC")
    R(f"R5{n}1", "10k", f"{trig}_C", "GND", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003, note="trigger low through reset")
    C(f"C5{n}0", "10uF", "3V3_CAM_F", "GND", S, K, fp="0603", mpn="GRM188R61A106KE69D", mfr="Murata", price=0.03)
    C(f"C5{n}1", "100nF", "3V3_CAM_F", "GND", S, K, mpn="GRM155R71H104KE14D", mfr="Murata", price=0.01)
# =====================================================================================================
D.sheet("CB-06", "Timing master: STM32G474CET6 (HRTIM 184 ps) · camera & strobe timing", "Pin assignment per Q-pinouts.md §1c")
S = "CB-06"; K = "STM32G474CET6 — LQFP48"
D.ic("U20", "Arm Cortex-M4 170 MHz, HRTIM", "STM32G474CET6", "ST", "LQFP-48", S, K,
     [("5", "PF0-OSC_IN", "XTAL_IN"), ("6", "PF1-OSC_OUT", "XTAL_OUT"), ("7", "PG10-NRST", "MCU_NRST"), ("45", "PB8-BOOT0", "MCU_BOOT0"),
      ("9", "PA1 COMP1_INP", "LED1_ISNS"), ("16", "PB0 COMP4_INP", "LED2_ISNS"), ("8", "PA0 COMP3_INP", "LED3_ISNS"), ("17", "PB1 ADC1_IN12", "VLED_SNS"),
      ("12", "PA4 SPI1_NSS", "HOST_SPI_CS_N"), ("13", "PA5 SPI1_SCK", "HOST_SPI_SCK"), ("14", "PA6 SPI1_MISO", "HOST_SPI_MISO"), ("15", "PA7 SPI1_MOSI", "HOST_SPI_MOSI"),
      ("10", "PA2 USART2_TX", "MCU_UART_TX"), ("11", "PA3 USART2_RX", "MCU_UART_RX"), ("18", "PB2", "MCU_IRQ_N"),
      ("39", "PA15 I2C1_SCL", "I2C_SYS_SCL"), ("46", "PB9 I2C1_SDA", "I2C_SYS_SDA"), ("37", "PA13 SWDIO", "SWDIO"), ("38", "PA14 SWCLK", "SWCLK"), ("40", "PB3 SWO", "SWO"),
      ("1", "VBAT", "3V3"), ("24", "VDD", "3V3"), ("36", "VDD", "3V3"), ("48", "VDD", "3V3"), ("21", "VDDA", "3V3A"), ("20", "VREF+", "3V3A")],
     [("30", "PA8 HRTIM_CHA1", "CAM1_TRIG"), ("31", "PA9 HRTIM_CHA2", "LED1_GATE_CMD"), ("32", "PA10 HRTIM_CHB1", "CAM2_TRIG"), ("33", "PA11 HRTIM_CHB2", "LED2_GATE_CMD"),
      ("26", "PB12 HRTIM_CHC1", "CAM3_TRIG"), ("27", "PB13 HRTIM_CHC2", "LED3_GATE_CMD"), ("28", "PB14 HRTIM_CHD1", "STROBE_HB"), ("29", "PB15 HRTIM_CHD2", "TP_HRTIM_D2"),
      ("34", "PA12 HRTIM_FLT1", "LED1_OC_N"), ("22", "PB10 HRTIM_FLT3", "LED2_OC_N"), ("25", "PB11 HRTIM_FLT4", "LED3_OC_N"),
      ("44", "PB7 HRTIM_EEV3", "CAM1_FLASH"), ("43", "PB6 HRTIM_EEV4", "CAM2_FLASH"), ("42", "PB5 HRTIM_EEV6", "CAM3_FLASH"),
      ("41", "PB4", "STROBE_EN_MCU"), ("2", "PC13", "TP_PC13"), ("3", "PC14", "NC"), ("4", "PC15", "NC"),
      ("19", "VSSA", "GND"), ("23", "VSS", "GND"), ("35", "VSS", "GND"), ("47", "VSS", "GND")],
     note=OK + "DS12288 Table 12 (Rev 1) — re-check AF numbers vs Rev 6 in CubeMX", price=5.70)
D.ic("Y20", "24 MHz crystal 10 ppm (HRTIM time base)", "ABM8-24.000MHZ-B2-T", "Abracon", "3.2x2.5", S, K, [("1", "XI", "XTAL_IN")], [("3", "XO", "XTAL_OUT"), ("2", "GND", "GND"), ("4", "GND", "GND")], note=OK + "Abracon ABM8", price=0.32)
for ref, v, a, b in [("C600", "10pF C0G", "XTAL_IN", "GND"), ("C601", "10pF C0G", "XTAL_OUT", "GND"), ("C602", "100nF", "MCU_NRST", "GND"),
                     ("C603", "4.7uF", "3V3", "GND"), ("C604", "100nF", "3V3", "GND"), ("C605", "100nF", "3V3", "GND"), ("C606", "100nF", "3V3", "GND"),
                     ("C607", "1uF", "3V3A", "GND"), ("C608", "100nF", "3V3A", "GND")]:
    C(ref, v, a, b, S, K, mpn="GRM155R71C104KA88D", mfr="Murata", price=0.01)
FB("FB600", "600R ferrite", "3V3", "3V3A", S, K, fp="0402", mpn="BLM15AG601SN1D", mfr="Murata", price=0.02)
R("R600", "10k", "MCU_BOOT0", "GND", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
for ref, n in [("R601", "CAM1_TRIG"), ("R602", "CAM2_TRIG"), ("R603", "CAM3_TRIG"), ("R604", "LED1_GATE_CMD"), ("R605", "LED2_GATE_CMD"), ("R606", "LED3_GATE_CMD"), ("R607", "STROBE_EN_MCU")]:
    R(ref, "10k", n, "GND", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003, note="safe-off through reset")
R("R608", "10k", "MCU_IRQ_N", "3V3", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
D.ic("J6", "SWD/Tag-Connect (MCU + MSPM0)", "TC2050-IDC-NL footprint", "Tag-Connect", "pads", S, K,
     [("1", "VCC", "3V3"), ("2", "SWDIO", "SWDIO"), ("4", "SWCLK", "SWCLK")], [("6", "SWO", "SWO"), ("3", "NRST", "MCU_NRST"), ("5", "GND", "GND")], note="✔ footprint only (no part)", price=0.0)
K = "Strobe enable AND gate (STM32 && SoM && watchdog heartbeat all required)"
D.ic("U21", "3-input AND, strobe master enable", "74LVC1G11GW,125", "Nexperia", "SOT-363", S, K,
     [("1", "A", "STROBE_EN_MCU"), ("3", "B", "STROBE_EN_SOM"), ("6", "C", "WDOG_OK")], [("4", "Y", "STROBE_EN"), ("5", "VCC", "3V3"), ("2", "GND", "GND")], note=OK + "Nexperia 74LVC1G11", price=0.08)
D.ic("U22", "Heartbeat watchdog (retriggerable one-shot, 2 ms)", "74LVC1G123DC,125", "Nexperia", "VSSOP-8", S, K,
     [("1", "A", "GND"), ("2", "B", "STROBE_HB"), ("3", "CLR", "3V3"), ("7", "REXT/CEXT", "WD_RC")], [("5", "Q", "WDOG_OK"), ("6", "CEXT", "WD_C"), ("8", "VCC", "3V3"), ("4", "GND", "GND")],
     note=OK + "Nexperia 74LVC1G123 rev 8", price=0.22)
R("R610", "20.0k 1%", "WD_RC", "3V3", S, K, mpn="RC0402FR-0720KL", mfr="Yageo", price=0.003)
C("C610", "100nF C0G", "WD_C", "WD_RC", S, K, fp="0603", mpn="GRM1885C1H104JA01D", mfr="Murata", price=0.05, note="tW ≈ 2 ms: HB must toggle or strobe disables")
R("R611", "10k", "STROBE_EN_SOM", "GND", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)

# =====================================================================================================
D.sheet("CB-07", "Strobe bus: eFuse inrush/10 W limit → LM5155 boost 30–38 V → 940 µF", "Eye-safety-critical: average optical power capped by input current limit")
S = "CB-07"; K = "TPS259470L eFuse — inrush + hard 10 W input ceiling (latch-off)"
D.ic("U30", "2.7–23 V 5.5 A eFuse, adj. ILIM, latch-off", "TPS259470LRPWR", "TI", "VQFN-HR 2x2 (RPW-10)", S, K,
     [("5", "IN", "VSYS"), ("1", "EN/UVLO", "STROBE_EN"), ("2", "OVLO", "EF_OVLO"), ("7", "DVDT", "EF_DVDT")],
     [("6", "OUT", "VBST_IN"), ("9", "ILM", "EF_ILM"), ("10", "ITIMER", "EF_ITIMER"), ("3", "AUXOFF", "NC"), ("4", "FLT", "STROBE_FLT_N"), ("8", "GND", "GND")],
     note=OK + "SLVSFC9C Table 5-1 · RILM=3334/ILIM", price=0.95)
R("R700", "3.92k 1%", "EF_ILM", "GND", S, K, mpn="CRCW04023K92FKED", mfr="Vishay", price=0.01, note="ILIM = 3334/3920 = 0.85 A → 10.2 W @12 V")
C("C700", "22nF", "EF_DVDT", "GND", S, K, mpn="GRM155R71H223KA12D", mfr="Murata", price=0.01)
C("C701", "2.2nF", "EF_ITIMER", "GND", S, K, mpn="GRM155R71H222KA01D", mfr="Murata", price=0.01)
R("R701", "10k", "STROBE_FLT_N", "3V3", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
R("R702", "0R (OVLO off: tie low)", "EF_OVLO", "GND", S, K, mpn="RC0402JR-070RL", mfr="Yageo", price=0.003)
K = "LM5155 boost controller (1 MHz, 22 µH option B per P-power.md §5)"
D.ic("U31", "Wide-VIN boost controller", "LM5155DSSR", "TI", "WSON-12", S, K,
     [("1", "BIAS", "VBST_IN"), ("12", "UVLO/EN/SYNC", "BST_UVLO"), ("10", "RT", "BST_RT"), ("9", "SS", "BST_SS"), ("8", "FB", "BST_FB"), ("6", "COMP", "BST_COMP"), ("7", "AGND", "GND")],
     [("3", "GATE", "BST_GATE"), ("5", "CS", "BST_CSF"), ("4", "PGND", "GND"), ("2", "VCC", "BST_VCC"), ("11", "PGOOD", "STROBE_PG"), ("EP", "PAD", "GND")],
     note=OK + "SNVSB75E Table 7-1", price=1.22)
D.fet("Q31", "60V 8.1mR", "CSD18543Q3A", "TI", "SON3x3", "BST_SW", "BST_GATE_R", "BST_CS", S, K, price=0.45)
L("L31", "22uH 3.5A", "VBST_IN", "BST_SW", S, K, fp="7.3x6.6", mpn="SRP7028A-220M", mfr="Bourns", price=0.61)
DI("D31", "PMEG10030ELP 100V 3A", "BST_SW", "STROBE_BUS", S, K, fp="CFP5", mpn="PMEG10030ELPX", mfr="Nexperia", price=0.18)
for ref, v, a, b, mpn in [
    ("R710", "82mR 1%", "BST_CS", "GND", "WSL1206R0820FEA"), ("R711", "1.00k", "BST_CSF", "BST_CSR", "RC0402FR-071KL"), ("R712", "100R", "BST_CSR", "BST_CS", "RC0402FR-07100RL"),
    ("R713", "2.2R", "BST_GATE", "BST_GATE_R", "RC0402FR-072R2L"), ("R714", "21.0k 1%", "BST_RT", "GND", "CRCW040221K0FKED"),
    ("R715", "200k 0.1%", "STROBE_BUS", "BST_FB", "ERA-3AEB204V"), ("R716", "5.76k 0.1%", "BST_FB", "GND", "ERA-3AEB5761V"), ("R717", "82.5k 0.1%", "STROBE_TRIM", "BST_FB", "ERA-3AEB8252V"),
    ("R718", "237k", "BST_COMP", "BST_CMPN", "CRCW0402237KFKED"), ("R719", "130k 1%", "VBST_IN", "BST_UVLO", "CRCW0402130KFKED"), ("R720", "21.5k 1%", "BST_UVLO", "GND", "CRCW040221K5FKED"),
    ("R721", "24.9k", "STROBE_PG", "3V3", "RC0402FR-0724K9L"), ("R722", "10k 2W bleeder (switched)", "STROBE_BUS", "BLEED_D", "CRCW251210K0FKEG")]:
    R(ref, v, a, b, S, K, mpn=mpn, mfr="Vishay/Yageo/Panasonic", price=0.02)
D.fet("Q32", "Bleeder switch 60V", "2N7002K", "Nexperia", "SOT-23", "BLEED_D", "STROBE_EN_N", "GND", S, K, price=0.03)
D.ic("U32", "Inverter (bleeder ON when strobe disabled)", "74LVC1G04GW,125", "Nexperia", "SOT-353", S, K, [("2", "A", "STROBE_EN")], [("4", "Y", "STROBE_EN_N"), ("5", "VCC", "3V3"), ("3", "GND", "GND")], note=OK + "Nexperia 74LVC1G04", price=0.06)
for ref, v, a, b, fp, mpn in [
    ("C710", "100pF C0G", "BST_CSR", "GND", "0402", "GRM1555C1H101JA01D"), ("C711", "0.1uF", "VBST_IN", "GND", "0402", "GRM155R71H104KE14D"),
    ("C712", "2.2uF 16V", "BST_VCC", "GND", "0603", "GRM188R71C225KE11D"), ("C713", "0.47uF", "BST_SS", "GND", "0603", "GRM188R71C474KA88D"),
    ("C714", "4.7nF", "BST_CMPN", "GND", "0402", "GRM155R71H472KA01D"), ("C715", "120pF C0G", "BST_COMP", "GND", "0402", "GRM1555C1H121JA01D"),
    ("C716", "10nF", "BST_UVLO", "GND", "0402", "GRM155R71H103KA88D"), ("C717", "10uF 50V", "VBST_IN", "GND", "1206", "CGA5L1X7R1H106K160AC"),
    ("C718", "10uF 50V", "VBST_IN", "GND", "1206", "CGA5L1X7R1H106K160AC"), ("C719", "2.2uF 100V", "STROBE_BUS", "GND", "1210", "C1210C225K1RACTU"),
    ("C720", "2.2uF 100V", "STROBE_BUS", "GND", "1210", "C1210C225K1RACTU")]:
    C(ref, v, a, b, S, K, fp=fp, mpn=mpn, mfr="Murata/KEMET/TDK", price=0.04)
C("C31", "470uF 50V", "STROBE_BUS", "GND", S, K, fp="16x16.5", mpn="EEE-FK1H471AM", mfr="Panasonic", price=1.05)
C("C32", "470uF 50V", "STROBE_BUS", "GND", S, K, fp="16x16.5", mpn="EEE-FK1H471AM", mfr="Panasonic", price=1.05)
K = "Bus voltage trim DAC (STM32 DAC1_OUT not bonded with this pin map → external 12-bit DAC)"
D.ic("U33", "12-bit I2C DAC (bus 30–38 V trim)", "DAC80501ZDQFR", "TI", "WSON-10", S, K,
     [("1", "VDD", "3V3"), ("8", "SDA", "I2C_SYS_SDA"), ("7", "SCL", "I2C_SYS_SCL")], [("4", "VOUT", "STROBE_TRIM"), ("2", "GND", "GND"), ("5", "REF", "NC")],
     note="⚠ confirm DAC80501Z WSON-10 pin numbers & addr", price=1.85)
R("R730", "200k", "STROBE_BUS", "VLED_DIV", S, K, mpn="CRCW0402200KFKED", mfr="Vishay", price=0.01)
R("R731", "16.9k", "VLED_DIV", "GND", S, K, mpn="CRCW040216K9FKED", mfr="Vishay", price=0.01)
R("R732", "0R", "VLED_DIV", "VLED_SNS", S, K, mpn="RC0402JR-070RL", mfr="Yageo", price=0.003)

# =====================================================================================================
D.sheet("CB-08", "Radar capture: MSPM0G3507 + ADS131M02 ×2 · radar head connectors", "Separate sensor: own MCU, data never fused with cameras (patent design-around)")
S = "CB-08"; K = "MSPM0G3507 radar MCU (VQFN-32)"
D.ic("U40", "Arm M0+ 80 MHz, radar capture + FFT", "MSPM0G3507SRHBR", "TI", "VQFN-32 5x5", S, K,
     [("4", "VDD", "3V3"), ("3", "NRST", "RAD_NRST"), ("32", "VCORE", "RAD_VCORE"), ("23", "PA19 SWDIO", "RAD_SWDIO"), ("24", "PA20 SWCLK", "RAD_SWCLK"),
      ("14", "PA10 UART0_TX", "RAD_UART_TX"), ("15", "PA11 UART0_RX", "RAD_UART_RX"), ("22", "PA18 BSL_INVOKE", "RAD_BSL"), ("5", "VSS", "GND"), ("EP", "PAD", "GND")],
     [("16", "PA12 SPI0_SCK", "ADC_SCK"), ("17", "PA13 SPI0_POCI", "ADC_DOUT"), ("18", "PA14 SPI0_PICO", "ADC_DIN"), ("12", "PA8 SPI0_CS0", "ADC1_CS_N"),
      ("6", "PA2 SPI0_CS0alt→GPIO", "ADC2_CS_N"), ("13", "PA9 GPIO", "ADC_DRDY_N"), ("11", "PA7 CLK_OUT", "ADC_CLKIN"),
      ("21", "PA17 GPIO", "RADR_EN"), ("25", "PA21 GPIO", "RADF_EN"), ("26", "PA22 GPIO", "ADC_SYNC_N"),
      ("28", "PA24 A0_3", "LED1_NTC"), ("29", "PA25 A0_2", "LED2_NTC"), ("19", "PA15 A1_0", "LED3_NTC")],
     note=OK + "SLASEX6C Table 6-2", price=1.43)
for ref, v, a, b in [("C800", "10uF", "3V3", "GND"), ("C801", "0.1uF", "3V3", "GND"), ("C802", "0.47uF", "RAD_VCORE", "GND"), ("C803", "10nF", "RAD_NRST", "GND")]:
    C(ref, v, a, b, S, K, fp="0603" if "10uF" in v else "0402", mpn="GRM155R71C104KA88D", mfr="Murata", price=0.01)
D.ic("J7", "SWD/Tag-Connect (MSPM0 radar MCU)", "TC2030-IDC-NL footprint", "Tag-Connect", "pads", S, K,
     [("1", "VCC", "3V3"), ("2", "SWDIO", "RAD_SWDIO"), ("4", "SWCLK", "RAD_SWCLK")], [("3", "NRST", "RAD_NRST"), ("5", "GND", "GND")], note="✔ footprint only (no part)", price=0.0)
R("R800", "47k", "RAD_NRST", "3V3", S, K, mpn="RC0402FR-0747KL", mfr="Yageo", price=0.003)
R("R801", "10k", "RAD_BSL", "GND", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
for n, (ref, cs, ip, iq) in enumerate([("U41", "ADC1_CS_N", "RADR_I", "RADR_Q"), ("U42", "ADC2_CS_N", "RADF_I", "RADF_Q")], start=1):
    K = f"{ref}: ADS131M02 — {'rear head (club / wake)' if n == 1 else 'down-range head (ball speed)'}"
    D.ic(ref, "2-ch simultaneous 24-bit ΔΣ ADC, 64 kS/s", "ADS131M02IPWR", "TI", "TSSOP-20", S, K,
         [("3", "AIN0P", ip + "_A"), ("4", "AIN0N", "RAD_VCM"), ("6", "AIN1P", iq + "_A"), ("5", "AIN1N", "RAD_VCM"), ("1", "AVDD", "3V3A_RAD"), ("2", "AGND", "GND"),
          ("7", "NC", "NC"), ("8", "NC", "NC"), ("9", "NC", "NC"), ("10", "NC", "NC")],
         [("12", "CS", cs), ("14", "SCLK", "ADC_SCK"), ("15", "DOUT", "ADC_DOUT"), ("16", "DIN", "ADC_DIN"), ("13", "DRDY (DRDY_HiZ=1)", "ADC_DRDY_N"), ("17", "CLKIN", "ADC_CLKIN"),
          ("11", "SYNC/RESET", "ADC_SYNC_N"), ("18", "CAP", f"ADC{n}_CAP"), ("20", "DVDD", "3V3"), ("19", "DGND", "GND")],
         note=OK + "SBAS853A Table 5-1 (AIN1N=5, AIN1P=6)", price=2.53)
    C(f"C8{n}0", "1uF", "3V3A_RAD", "GND", S, K, fp="0402", mpn="GRM155R61C105KA12D", mfr="Murata", price=0.01)
    C(f"C8{n}1", "1uF", "3V3", "GND", S, K, fp="0402", mpn="GRM155R61C105KA12D", mfr="Murata", price=0.01)
    C(f"C8{n}2", "220nF", f"ADC{n}_CAP", "GND", S, K, fp="0402", mpn="GRM155R71C224KA12D", mfr="Murata", price=0.01)
    for j, sig in enumerate((ip, iq)):
        R(f"R8{n}{2*j+4}", "4.7k 0.1%", sig, sig + "_A", S, K, mpn="ERA-2AEB472X", mfr="Panasonic", price=0.08, note="×0.68: ±1.65 V head swing → ±1.12 V < ±1.2 V FS")
        R(f"R8{n}{2*j+5}", "10.0k 0.1%", sig + "_A", "RAD_VCM", S, K, mpn="ERA-2AEB103X", mfr="Panasonic", price=0.08)
R("R804", "10k", "ADC_DRDY_N", "3V3", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003, note="wired-AND DRDY: both ADCs set MODE.DRDY_HiZ = 1")
K = "ADC analog supply & mid-rail reference"
FB("FB800", "600R ferrite", "3V3", "3V3A_RAD", S, K, mpn="BLM15AG601SN1D", mfr="Murata", price=0.02)
R("R802", "10k 0.1%", "3V3A_RAD", "RAD_VCM", S, K, mpn="ERA-2AEB103X", mfr="Panasonic", price=0.08)
R("R803", "10k 0.1%", "RAD_VCM", "GND", S, K, mpn="ERA-2AEB103X", mfr="Panasonic", price=0.08)
C("C805", "10uF", "RAD_VCM", "GND", S, K, fp="0603", mpn="GRM188R61A106KE69D", mfr="Murata", price=0.03)
for n, (ref, pfx, en) in enumerate([("J30", "RADR", "RADR_EN"), ("J31", "RADF", "RADF_EN")], start=1):
    K = f"{ref}: radar head connector ({'rear' if n == 1 else 'down-range'}) JST SH 6-pos"
    D.ic(ref, "JST SH 6-pos R/A (cable A06SR06SR30K152A)", "SM06B-SRSS-TB(LF)(SN)", "JST", "SH 1.0", S, K,
         [("1", "VSYS_RAD (5V0)", "5V0"), ("2", "GND", "GND"), ("3", "EN", en)], [("4", "I_OUT", f"{pfx}_I"), ("5", "Q_OUT", f"{pfx}_Q"), ("6", "AGND", "GND")],
         note=OK + "JST SH", price=0.35)

# =====================================================================================================
D.sheet("CB-09", "Sensors & UI: SCL3300 inclinometer · BMP585 · SHT45 · BMI323 · display", "Leveling ±0.1°, air density, shot shock, 2.4\" transflective display")
S = "CB-09"; K = "Murata SCL3300-D01 inclinometer (SPI, on display/UI SPI bus)"
D.ic("U50", "3-axis inclinometer ±0.1°", "SCL3300-D01-1", "Murata", "12-pin SMD", S, K,
     [("4", "VDD", "3V3"), ("9", "DVIO", "3V3"), ("5", "CSB", "INCL_CS_N"), ("8", "SCK", "UI_SCK"), ("7", "MOSI", "UI_MOSI")],
     [("6", "MISO", "UI_MISO"), ("2", "A_EXTC", "INCL_AEXT"), ("10", "D_EXTC", "INCL_DEXT"), ("1", "AVSS", "GND"), ("11", "DVSS", "GND"), ("3", "RESERVED", "GND"), ("12", "EMC_GND", "GND")],
     note=OK + "Murata doc 4921 rev 4 Table 6", price=30.47)
for ref, a in [("C900", "3V3"), ("C901", "3V3"), ("C902", "INCL_AEXT"), ("C903", "INCL_DEXT")]:
    C(ref, "100nF X7R", a, "GND", S, K, mpn="GRM155R71C104KA88D", mfr="Murata", price=0.01)
K = "Air density: BMP585 (0x46) + SHT45-AD1F (0x44) · motion: BMI323 (0x68) — I2C_SYS"
D.ic("U51", "Barometric pressure", "BMP585", "Bosch", "LGA-8 3.25x3.25", S, K, [("8", "VDD", "3V3"), ("4", "VDDIO", "3V3"), ("7", "CSB", "3V3"), ("3", "SDO", "GND")],
     [("1", "SCX", "I2C_SYS_SCL"), ("2", "SDX", "I2C_SYS_SDA"), ("5", "INT", "GND"), ("6", "VSS", "GND")], note=OK + "BST-BMP585-DS003 Table 26", price=3.05)
D.ic("U52", "Temp/RH ±0.1 °C, membrane", "SHT45-AD1F-R2", "Sensirion", "DFN-4 1.5x1.5", S, K, [("3", "VDD", "3V3")], [("1", "SDA", "I2C_SYS_SDA"), ("2", "SCL", "I2C_SYS_SCL"), ("4", "VSS", "GND")],
     note=OK + "SHT4x DS v7.3", price=4.53)
D.ic("U53", "6-axis IMU (shot shock, motion wake)", "BMI323", "Bosch", "LGA-14", S, K,
     [("8", "VDD", "3V3"), ("5", "VDDIO", "3V3"), ("12", "CSB", "3V3"), ("1", "SDO", "GND"), ("2", "NC", "NC"), ("3", "NC", "NC"), ("10", "NC", "NC"), ("11", "NC", "NC")],
     [("13", "SCx", "I2C_SYS_SCL"), ("14", "SDx", "I2C_SYS_SDA"), ("4", "INT1", "IMU_INT1"), ("9", "INT2", "NC"), ("6", "GNDIO", "GND"), ("7", "GND", "GND")],
     note=OK + "BST-BMI323-DS000-13 Table 56", price=2.60)
for ref in ("C910", "C911", "C912", "C913", "C914"):
    C(ref, "100nF", "3V3", "GND", S, K, mpn="GRM155R71C104KA88D", mfr="Murata", price=0.01)
K = "2.4\" transflective TFT 240x320 (ST7789-T3, 4-wire SPI) + backlight"
D.ic("J40", "Display FPC 40-pos 0.5 mm (VIEWE UEED024QV-RH40-A003)", "FH12-40S-0.5SH(55)", "Hirose", "FH12", S, K,
     [("CS", "CSX", "DISP_CS_N"), ("DC", "DCX", "DISP_DC"), ("SCL", "WRX/SCL", "UI_SCK"), ("SDA", "SDA", "UI_MOSI"), ("RES", "RESX", "DISP_RST_N"),
      ("IM0", "IM0", "GND"), ("IM1", "IM1", "3V3"), ("IM2", "IM2", "3V3")],
     [("VDD", "VDD/VDDI", "3V3"), ("LEDA", "LED-A", "BL_A"), ("LEDK", "LED-K", "BL_K"), ("GND", "GND", "GND")],
     note="⚠ FPC pin numbers: VIEWE spec sheet (not public) — nets final, IM straps per ST7789 4-line serial I", price=2.26)
D.ic("U54", "Backlight constant-current boost (WLED)", "TPS61169DCKR", "TI", "SC70-5", S, K,
     [("1", "VIN", "5V0"), ("4", "CTRL", "BL_PWM")], [("5", "SW", "BL_SW"), ("3", "FB", "BL_FB"), ("2", "GND", "GND")], note="⚠ confirm TPS61169 SC70 pin map", price=0.42)
L("L54", "10uH", "5V0", "BL_SW", S, K, fp="4x4", mpn="LQH3NPN100MJ0L", mfr="Murata", price=0.12)
DI("D54", "Schottky 40V", "BL_SW", "BL_A", S, K, fp="SOD-323", mpn="BAT46WJ", mfr="Nexperia", price=0.05)
R("R954", "10R (20 mA)", "BL_FB", "GND", S, K, mpn="RC0402FR-0710RL", mfr="Yageo", price=0.003)
R("R955", "0R", "BL_K", "BL_FB", S, K, mpn="RC0402JR-070RL", mfr="Yageo", price=0.003)
C("C954", "1uF 50V", "BL_A", "GND", S, K, fp="0603", mpn="GRM188R71H105KA12D", mfr="Murata", price=0.03)
for ref, n, tgt in [("R950", "DISP_RST_N", "3V3"), ("R951", "INCL_CS_N", "3V3"), ("R952", "DISP_CS_N", "3V3"), ("R953", "BTN_MODE_N", "3V3"), ("R956", "BTN_LR_N", "3V3")]:
    R(ref, "10k", n, tgt, S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)

# =====================================================================================================
D.sheet("CB-10", "SoM I/O level translation: 1.8 V SoM ↔ 3.3 V carrier", "QCS6490 I/O is 1.8 V; every SoM digital signal crosses here")
S = "CB-10"
NDA18 = "⚠ 1.8 V I/O-reference output ball per Thundercomm C6490P HW design guide (NDA)"
OUT = ["HOST_SPI_SCK", "HOST_SPI_MOSI", "HOST_SPI_CS_N", "MCU_UART_RX", "RAD_UART_RX", "UI_SCK", "UI_MOSI", "DISP_CS_N",
       "INCL_CS_N", "MCU_BOOT0", "STROBE_EN_SOM", "FAN_PWM", "DISP_DC", "DISP_RST_N", "BL_PWM", "LED_R_DRV",
       "LED_G_DRV", "LED_B_DRV", "BZ_GATE", "CAM_MUX_RST_N", "RAD_BSL"]                                 # SoM drives (A → B)
INP = ["HOST_SPI_MISO", "MCU_UART_TX", "RAD_UART_TX", "UI_MISO", "MCU_IRQ_N", "PD_IRQ_N", "CHRG_OK", "PROCHOT_N",
       "IMU_INT1", "BAT_PRES_N", "STROBE_FLT_N", "STROBE_PG", "FAN_TACH", "BTN_MODE_N", "BTN_LR_N"]       # SoM reads (B → A)
OD = [("I2C_SYS_SDA", "I2C_SYS_SCL"), ("I2C_CAM_SDA", "I2C_CAM_SCL"), ("SMB_DAT", "SMB_CLK"), ("MCU_NRST", "RAD_NRST")]   # open-drain, bidirectional
lv = {n: n + "_1V8" for n in OUT + INP + [x for pr in OD for x in pr]}
for p in D.parts:                       # the SoM side of every translated signal becomes a 1.8 V net
    if p.ref.startswith("U10."):
        p.pins = [(a, b, lv.get(net, net), sd) for a, b, net, sd in p.pins]
D.parts[[p.ref for p in D.parts].index("U10.A")].pins.append(("V18", "VREG_1P8 (I/O ref out)", "1V8_SOM", "R"))
for i, a in enumerate(("CHG_IBAT", "CHG_PSYS")):   # charger analog monitors → PMIC ADC (≤ 1.8 V)
    p = next(q for q in D.parts if q.ref == "U10.D")
    p.pins = [(x, y, a + "_S" if net == a else net, sd) for x, y, net, sd in p.pins]
K = "Charger monitor outputs scaled for the 1.8 V PMIC ADC"
for i, a in enumerate(("CHG_IBAT", "CHG_PSYS")):
    R(f"R10{60+2*i}", "10.0k 0.1%", a, a + "_S", S, K, mpn="ERA-2AEB103X", mfr="Panasonic", price=0.08, note="÷2: 3.3 V max → 1.65 V")
    R(f"R10{61+2*i}", "10.0k 0.1%", a + "_S", "GND", S, K, mpn="ERA-2AEB103X", mfr="Panasonic", price=0.08)
K = "Push-pull translators (SN74LVC8T245, VCCA = 1V8_SOM, VCCB = 3V3; outputs Hi-Z if either supply is off)"
groups = [("U60", OUT[0:8], "1V8_SOM"), ("U61", OUT[8:16], "1V8_SOM"), ("U62", OUT[16:21], "1V8_SOM"), ("U63", INP[0:8], "GND"), ("U64", INP[8:15], "GND")]
for ref, sigs, dirn in groups:
    sigs = sigs + ["NC"] * (8 - len(sigs))
    D.ic(ref, "8-bit dual-supply translator, " + ("SoM → 3.3 V" if dirn != "GND" else "3.3 V → SoM"), "SN74LVC8T245PWR", "TI", "TSSOP-24", S, K,
         [("1", "VCCA", "1V8_SOM"), ("2", "DIR", dirn), ("22", "OE", "GND")] + [(str(3+i), f"A{i+1}", lv[n] if n != "NC" else ("NC" if dirn == "GND" else "GND")) for i, n in enumerate(sigs)],
         [("23", "VCCB", "3V3"), ("24", "VCCB", "3V3"), ("11", "GND", "GND"), ("12", "GND", "GND"), ("13", "GND", "GND")] +
         [(str(21-i), f"B{i+1}", n if n != "NC" else ("GND" if dirn == "GND" else "NC")) for i, n in enumerate(sigs)],
         note=OK + "SCES584 (SN74LVC8T245 PW)", price=0.62)
    C(f"C1{ref[1:]}0", "100nF", "1V8_SOM", "GND", S, K, mpn="GRM155R71C104KA88D", mfr="Murata", price=0.01)
    C(f"C1{ref[1:]}1", "100nF", "3V3", "GND", S, K, mpn="GRM155R71C104KA88D", mfr="Murata", price=0.01)
K = "Open-drain translators (PCA9306 pass-gate): I2C_SYS, camera CCI, battery SMBus, MCU / radar resets"
for k, (ref, (a, b)) in enumerate(zip(("U65", "U66", "U67", "U68"), OD)):
    D.ic(ref, "2-bit bidirectional I2C/OD translator", "PCA9306DCUR", "TI", "VSSOP-8", S, K,
         [("2", "VREF1", "1V8_SOM"), ("4", "SDA1", lv[a]), ("3", "SCL1", lv[b]), ("1", "GND", "GND")],
         [("7", "VREF2", f"PCA_EN{k}"), ("8", "EN", f"PCA_EN{k}"), ("5", "SDA2", a), ("6", "SCL2", b)], note=OK + "SCPS113 (PCA9306 DCU)", price=0.38)
    R(f"R10{k}0", "200k", f"PCA_EN{k}", "3V3", S, K, mpn="RC0402FR-07200KL", mfr="Yageo", price=0.003, note="VREF2 bias per PCA9306 DS")
    C(f"C10{k}0", "100nF", f"PCA_EN{k}", "GND", S, K, mpn="GRM155R71C104KA88D", mfr="Murata", price=0.01)
    for j, n in enumerate((a, b)):
        R(f"R10{k}{j+1}", "2.2k" if k < 3 else "10k", lv[n], "1V8_SOM", S, K, mpn="RC0402FR-072K2L" if k < 3 else "RC0402FR-0710KL", mfr="Yageo", price=0.003)
K = "USB VBUS detect for the SoM (device mode / factory flashing), 5–20 V tolerant"
D.ic("Q10", "NPN level shift", "MMBT3904LT1G", "onsemi", "SOT-23", S, K, [("1", "B", "VBUS_DET_B")], [("3", "C", "USB_VBUS_DET_N_1V8"), ("2", "E", "GND")], note=OK + "SOT-23 B-E-C", price=0.02)
R("R1070", "100k", "VBUS_C", "VBUS_DET_B", S, K, mpn="RC0402FR-07100KL", mfr="Yageo", price=0.003, note="20 V → 0.19 mA base")
R("R1071", "22k", "VBUS_DET_B", "GND", S, K, mpn="RC0402FR-0722KL", mfr="Yageo", price=0.003, note="off below ≈ 3.9 V")
R("R1072", "10k", "USB_VBUS_DET_N_1V8", "1V8_SOM", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
p = next(q for q in D.parts if q.ref == "U10.A")
p.pins.append(("VBD", "GPIO in: USB VBUS detect (active low)", "USB_VBUS_DET_N_1V8", "L"))

# =====================================================================================================
D.sheet("LB-01", "LED strobe board (×3 identical, LED-A/B/C) · 8× VSMA1094250 · 5 A linear current sink · hardware safety", "One string per board: 8× VF 2.9–4.2 V = 23–34 V at 5 A; regulated 5.0 A sink, 3–5 µs; pulse cap 8 µs; 300 µs hold-off; latched 6.5 A trip")
S = "LB-01"; K = "LED string (8 in series, VF 2.9 / 3.7 / 4.2 V min/typ/max each at 5 A, 100 µs pulse)"
nodes = ["STROBE_BUS_L"] + [f"LS{i}" for i in range(1, 8)] + ["LED_DRAIN"]
for i in range(8):
    LED(f"D{i+1}", "VSMA1094250 940nm", nodes[i], nodes[i+1], S, K, fp="3.4x3.4", mpn="VSMA1094250", mfr="Vishay", price=1.379)
D.fet("Q1", "60V 8.5mR linear-mode sink FET", "CSD18543Q3A", "TI", "SON3x3", "LED_DRAIN", "SINK_G", "LED_SRC", S, K, price=0.38)
R("RS1", "0.1R 1% 2010", "LED_SRC", "GND", S, K, fp="2010", mpn="WSL2010R1000FEA", mfr="Vishay", price=0.315, note="5 A → 0.5 V")
K = "Local energy (hot loop < 15 mm²)"
C("C5", "100uF 50V hybrid", "STROBE_BUS_L", "GND", S, K, fp="10x10.2", mpn="EEH-ZA1H101P", mfr="Panasonic", price=0.655)
for i in range(4):
    C(f"C{i+1}", "2.2uF 100V X7R", "STROBE_BUS_L", "GND", S, K, fp="1210", mpn="C1210C225K1RACTU", mfr="KEMET", price=0.326)
K = "Constant-current loop: I = V(ISET) / RS1 = 0.50 V / 0.1 Ω = 5.0 A, independent of string VF and bus voltage"
D.ic("U1", "70 MHz RRO op-amp (current-loop amplifier)", "OPA810IDBVR", "TI", "SOT-23-5", S, K,
     [("3", "IN+", "ISET"), ("4", "IN-", "ISNS_FB"), ("5", "V+", "VDRV_L"), ("2", "V-", "GND")], [("1", "OUT", "SINK_DRV")],
     note="⚠ confirm OPA810 DBV pin map (SBOS799)", price=1.35)
R("R1", "56.2k 0.1%", "GATE_OK", "ISET", S, K, mpn="ERA-2AEB5622X", mfr="Panasonic", price=0.08, note="GATE_OK (3V3_L) → 0.50 V set-point")
R("R2", "10.0k 0.1%", "ISET", "GND", S, K, mpn="ERA-2AEB103X", mfr="Panasonic", price=0.08)
C("C6", "22pF C0G", "ISET", "GND", S, K, mpn="GRM1555C1H220JA01D", mfr="Murata", price=0.01, note="≈ 200 ns set-point edge")
R("R13", "1k", "LED_SRC", "ISNS_FB", S, K, mpn="RC0402FR-071KL", mfr="Yageo", price=0.003)
C("C13", "33pF C0G", "SINK_DRV", "ISNS_FB", S, K, mpn="GRM1555C1H330JA01D", mfr="Murata", price=0.01, note="loop compensation")
R("R14", "10R", "SINK_DRV", "SINK_G", S, K, mpn="RC0402FR-0710RL", mfr="Yageo", price=0.003)
R("R15", "10k", "SINK_G", "GND", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003, note="FET off when the driver is unpowered")
C("C7", "1uF", "VDRV_L", "GND", S, K, fp="0603", mpn="GRM188R71H105KA12D", mfr="Murata", price=0.03)
D.ic("U5", "LDO 12 V → driver VDD (from strobe bus)", "TPS7A4101DGNR", "TI", "MSOP-8", S, K, [("8", "IN", "STROBE_BUS_L"), ("5", "EN", "STROBE_EN_L")], [("1", "OUT", "VDRV_L"), ("3", "FB", "DRV_FB"), ("4", "GND", "GND")],
     note="⚠ confirm TPS7A4101 MSOP pin map", price=0.98)
R("R10", "1.13M", "VDRV_L", "DRV_FB", S, K, mpn="CRCW04021M13FKED", mfr="Vishay", price=0.01)
R("R11", "120k", "DRV_FB", "GND", S, K, mpn="CRCW0402120KFKED", mfr="Vishay", price=0.01)
K = "Hardware safety chain (no firmware can hold the LEDs on)"
D.ic("U2", "One-shot: max pulse cap 8 µs", "74LVC1G123DC,125", "Nexperia", "VSSOP-8", S, K,
     [("2", "B", "GATE_CMD_L"), ("1", "A", "GND"), ("3", "CLR", "HOLDOFF_OK")], [("5", "Q", "PW_WIN"), ("7", "REXT/CEXT", "PW_RC"), ("6", "CEXT", "PW_C"), ("8", "VCC", "3V3_L"), ("4", "GND", "GND")],
     note=OK + "Nexperia rev 8 · tW from Fig. 11–13", price=0.22)
R("R3", "10.0k 1%", "PW_RC", "3V3_L", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
C("C8", "560pF C0G", "PW_C", "PW_RC", S, K, mpn="GRM1555C1H561JA01D", mfr="Murata", price=0.01, note="≈6 µs typ / ≤8 µs max — bench trim")
D.ic("U3", "One-shot: 300 µs minimum off (hold-off)", "74LVC1G123DC,125", "Nexperia", "VSSOP-8", S, K,
     [("1", "A", "GATE_CMD_L"), ("2", "B", "3V3_L"), ("3", "CLR", "3V3_L")], [("5", "Q", "HOLDOFF"), ("7", "REXT/CEXT", "HO_RC"), ("6", "CEXT", "HO_C"), ("8", "VCC", "3V3_L"), ("4", "GND", "GND")],
     note=OK + "Nexperia rev 8 · tW = Rext·Cext", price=0.22)
R("R4", "33.2k 1%", "HO_RC", "3V3_L", S, K, mpn="RC0402FR-0733K2L", mfr="Yageo", price=0.003)
C("C9", "10nF C0G", "HO_C", "HO_RC", S, K, fp="0603", mpn="GRM1885C1H103JA01D", mfr="Murata", price=0.02, note="≈332 µs")
D.ic("U6", "Inverter (hold-off → OK)", "74LVC1G04GW,125", "Nexperia", "SOT-353", S, K, [("2", "A", "HOLDOFF_DLY")], [("4", "Y", "HOLDOFF_OK"), ("5", "VCC", "3V3_L"), ("3", "GND", "GND")], note=OK + "Nexperia 74LVC1G04", price=0.06)
R("R12", "1k", "HOLDOFF", "HOLDOFF_DLY", S, K, mpn="RC0402FR-071KL", mfr="Yageo", price=0.003)
C("C12", "1nF", "HOLDOFF_DLY", "GND", S, K, mpn="GRM1555C1H102JA01D", mfr="Murata", price=0.01, note="1 µs delay so the current pulse is not self-clipped")
D.ic("U4", "Over-current comparator (6.5 A trip, fault only)", "TLV3201AIDCKR", "TI", "SC70-5", S, K, [("3", "IN+", "LED_SRC"), ("4", "IN-", "OC_REF")], [("1", "OUT", "OC_TRIP"), ("5", "VCC", "3V3_L"), ("2", "GND", "GND")],
     note=OK + "TLV3201 DS pin functions", price=0.906)
D.ic("U11", "D flip-flop: latches the trip until the gate command ends", "74LVC1G74DC,125", "Nexperia", "VSSOP-8", S, K,
     [("1", "CP", "OC_TRIP"), ("2", "D", "3V3_L"), ("6", "RD", "GATE_CMD_L"), ("7", "SD", "3V3_L")], [("5", "Q", "OC_LATCH"), ("3", "Q", "NC"), ("8", "VCC", "3V3_L"), ("4", "GND", "GND")],
     note=OK + "Nexperia 74LVC1G74 · cleared while GATE_CMD is low", price=0.09)
R("R5", "30.1k", "3V3_L", "OC_REF", S, K, mpn="RC0402FR-0730K1L", mfr="Yageo", price=0.003)
R("R6", "7.15k", "OC_REF", "GND", S, K, mpn="RC0402FR-077K15L", mfr="Yageo", price=0.003, note="0.65 V = 6.5 A × 0.1 Ω")
D.ic("U7", "4-input gate: CMD ∧ PW_WIN ∧ EN ∧ ¬OC → GATE_OK", "74LVC1G11GW,125", "Nexperia", "SOT-363", S, K,
     [("1", "A", "GATE_CMD_L"), ("3", "B", "PW_WIN"), ("6", "C", "EN_NOT_OC")], [("4", "Y", "GATE_OK"), ("5", "VCC", "3V3_L"), ("2", "GND", "GND")], note=OK + "Nexperia 74LVC1G11", price=0.08)
D.ic("U8", "NOR: EN ∧ ¬OC", "74LVC1G02GW,125", "Nexperia", "SOT-353", S, K, [("1", "A", "OC_LATCH"), ("2", "B", "STROBE_EN_N_L")], [("4", "Y", "EN_NOT_OC"), ("5", "VCC", "3V3_L"), ("3", "GND", "GND")], note=OK + "Nexperia 74LVC1G02", price=0.06)
D.ic("U9", "Inverter (STROBE_EN → active-low)", "74LVC1G04GW,125", "Nexperia", "SOT-353", S, K, [("2", "A", "STROBE_EN_L")], [("4", "Y", "STROBE_EN_N_L"), ("5", "VCC", "3V3_L"), ("3", "GND", "GND")], note=OK + "Nexperia 74LVC1G04", price=0.06)
R("R7", "10k", "GATE_CMD_L", "GND", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003, note="cable unplugged → off")
R("R8", "10k", "STROBE_EN_L", "GND", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
D.ic("U10", "LDO 3.3 V logic (from 5V0 on cable)", "TPS7A2033PDBVR", "TI", "SOT-23-5", S, K, [("1", "IN", "5V0_L"), ("3", "EN", "5V0_L")], [("5", "OUT", "3V3_L"), ("2", "GND", "GND"), ("4", "NC", "NC")],
     note=OK + "TPS7A20 DS", price=0.16)
C("C10", "1uF", "5V0_L", "GND", S, K, mpn="GRM155R61C105KA12D", mfr="Murata", price=0.01)
C("C11", "1uF", "3V3_L", "GND", S, K, mpn="GRM155R61C105KA12D", mfr="Murata", price=0.01)
R("RT1", "NTC 10k B3380", "LED_NTC", "GND", S, K, mpn="NCU15XH103F60RC", mfr="Murata", price=0.064)
R("R9", "10k 1%", "3V3_L", "LED_NTC", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
K = "Board connector JST GH 10-pos (to carrier J20/J21/J22)"
D.ic("J1", "JST GH 10-pos (cable GHR-10V-S)", "BM10B-GHS-TBT", "JST", "GH 1.25", S, K,
     [("1", "STROBE_BUS", "STROBE_BUS_L"), ("2", "STROBE_BUS", "STROBE_BUS_L"), ("3", "GND", "GND"), ("4", "GND", "GND"), ("5", "NTC", "LED_NTC")],
     [("6", "5V0", "5V0_L"), ("7", "GATE_CMD", "GATE_CMD_L"), ("8", "STROBE_EN", "STROBE_EN_L"), ("9", "ISNS", "ISNS_OUT"), ("10", "ISNS_RTN", "ISNS_KELVIN")], note=OK + "JST GH", price=0.31)
R("R16", "100R", "LED_SRC", "ISNS_OUT", S, K, mpn="RC0402FR-07100RL", mfr="Yageo", price=0.003, note="Kelvin tap at RS1 top")
R("R17", "0R Kelvin tap at RS1 GND pad", "ISNS_KELVIN", "GND", S, K, mpn="RC0402JR-070RL", mfr="Yageo", price=0.003)

# carrier-side LED connectors (on CB-07 sheet)
S = "CB-07"; K = "LED board connectors J20–J22 (carrier) and over-current fault return (sense referenced to its Kelvin return, not cable GND)"
for n, ref in enumerate(("J20", "J21", "J22"), start=1):
    D.ic(ref, f"JST GH 10-pos → LED board {'ABC'[n-1]}", "BM10B-GHS-TBT", "JST", "GH 1.25", S, K,
         [("1", "STROBE_BUS", "STROBE_BUS"), ("2", "STROBE_BUS", "STROBE_BUS"), ("3", "GND", "GND"), ("4", "GND", "GND"), ("5", "NTC", f"LED{n}_NTC")],
         [("6", "5V0", "5V0"), ("7", "GATE_CMD", f"LED{n}_GATE_CMD"), ("8", "STROBE_EN", "STROBE_EN"), ("9", "ISNS", f"LED{n}_ISNS_R"), ("10", "ISNS_RTN", f"LED{n}_KELVIN")], note=OK + "JST GH", price=0.31)
    D.ic(f"U7{n}", f"OC comparator LED{n} (to HRTIM FLT)", "TLV3201AIDCKR", "TI", "SC70-5", S, K, [("3", "IN+", f"LED{n}_OCREF"), ("4", "IN-", f"LED{n}_ISNS")], [("1", "OUT", f"LED{n}_OC_N"), ("5", "VCC", "3V3"), ("2", "GND", "GND")],
         note=OK + "TLV3201 DS", price=0.906)
    R(f"R74{2*n}", "30.1k", "3V3", f"LED{n}_OCREF", S, K, mpn="RC0402FR-0730K1L", mfr="Yageo", price=0.003)
    R(f"R74{2*n+1}", "7.15k", f"LED{n}_OCREF", f"LED{n}_KELVIN", S, K, mpn="RC0402FR-077K15L", mfr="Yageo", price=0.003, note="6.5 A threshold referenced to the LED board's RS1 ground")
    R(f"R75{n}", "1k", f"LED{n}_ISNS_R", f"LED{n}_ISNS", S, K, mpn="RC0402FR-071KL", mfr="Yageo", price=0.003)
    C(f"C75{n}", "220pF C0G", f"LED{n}_ISNS", f"LED{n}_KELVIN", S, K, mpn="GRM1555C1H221JA01D", mfr="Murata", price=0.01, note="differential RC, 220 ns")
for n in (1, 2, 3):
    C(f"C74{n}", "100nF", f"LED{n}_NTC", "GND", S, K, mpn="GRM155R71C104KA88D", mfr="Murata", price=0.01, note="NTC filter; read by MSPM0 ADC (temperature only)")

# =====================================================================================================
D.sheet("RH-01", "Radar head board (×2 identical) · InnoSenT SMR-333 · IF amplifier", "24.150–24.250 GHz CW I/Q, FCC UXS-SMR3X3 module grant reused")
S = "RH-01"; K = "SMR-333 24 GHz I/Q transceiver (module grant)"
D.ic("U1", "24 GHz CW I/Q radar module", "80.00000346 (SMR-333)", "InnoSenT", "SMD 21.4x15", S, K,
     [("7", "Vcc 3.3V", "3V3_RF"), ("5", "enable", "RF_EN"), ("6", "GND", "GND"), ("10", "GND", "GND")],
     [("3", "IF1 (I)", "IF_I"), ("4", "IF2 (Q)", "IF_Q"), ("1", "d.n.c.", "NC"), ("2", "d.n.c.", "NC"), ("8", "d.n.c.", "NC"), ("9", "d.n.c.", "NC")],
     note=OK + "SMR-3X3 DS v2.2 · 3.2–3.4 V, 47 mA", price=13.80)
D.ic("U2", "LDO 3.3 V low-noise (RF supply)", "TPS7A2033PDBVR", "TI", "SOT-23-5", S, K, [("1", "IN", "5V0_R"), ("3", "EN", "5V0_R")], [("5", "OUT", "3V3_RF"), ("2", "GND", "GND"), ("4", "NC", "NC")],
     note=OK + "TPS7A20 DS", price=0.16)
C("C1", "1uF", "5V0_R", "GND", S, K, mpn="GRM155R61C105KA12D", mfr="Murata", price=0.01)
C("C2", "4.7uF", "3V3_RF", "GND", S, K, fp="0603", mpn="GRM188R61A475KE15D", mfr="Murata", price=0.02)
C("C3", "100nF", "3V3_RF", "GND", S, K, mpn="GRM155R71C104KA88D", mfr="Murata", price=0.01)
K = "IF amplifier: AC-coupled, 40 dB, band-pass 20 Hz – 20 kHz (I and Q identical)"
D.ic("U3", "Quad RRIO op-amp", "TLV9064IPWR", "TI", "TSSOP-14", S, K,
     [("3", "IN1+", "IFI_B"), ("2", "IN1-", "IFI_N1"), ("5", "IN2+", "IFI_S2B"), ("6", "IN2-", "IFI_N2"), ("10", "IN3+", "IFQ_B"), ("9", "IN3-", "IFQ_N1"),
      ("12", "IN4+", "IFQ_S2B"), ("13", "IN4-", "IFQ_N2"), ("4", "V+", "3V3_RF"), ("11", "V-", "GND")],
     [("1", "OUT1", "IFI_S1"), ("7", "OUT2", "I_OUT"), ("8", "OUT3", "IFQ_S1"), ("14", "OUT4", "Q_OUT")], note=OK + "SBOS839N Table 5-5", price=0.93)
for ch in ("I", "Q"):
    p = f"IF{ch}"
    C(f"C1{0 if ch=='I' else 5}", "4.7uF (AC couple, 20 Hz HP)", f"IF_{ch}", f"{p}_B", S, K, fp="0603", mpn="GRM188R61A475KE15D", mfr="Murata", price=0.02)
    R(f"R1{0 if ch=='I' else 5}", "1.65k (to VREF)", f"{p}_B", "IF_VREF", S, K, mpn="RC0402FR-071K65L", mfr="Yageo", price=0.003)
    R(f"R1{1 if ch=='I' else 6}", "1k", f"{p}_N1", "IF_VREF", S, K, mpn="RC0402FR-071KL", mfr="Yageo", price=0.003)
    R(f"R1{2 if ch=='I' else 7}", "10k (×11)", f"{p}_S1", f"{p}_N1", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
    C(f"C1{1 if ch=='I' else 6}", "680pF (24 kHz LP)", f"{p}_S1", f"{p}_N1", S, K, mpn="GRM1555C1H681JA01D", mfr="Murata", price=0.01)
    R(f"R1{3 if ch=='I' else 8}", "1k", f"{p}_S1", f"{p}_S2B", S, K, mpn="RC0402FR-071KL", mfr="Yageo", price=0.003)
    R(f"R1{4 if ch=='I' else 9}", "10k (×10)", f"{ch}_OUT", f"{p}_N2", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
    R(f"R2{0 if ch=='I' else 1}", "1k", f"{p}_N2", "IF_VREF", S, K, mpn="RC0402FR-071KL", mfr="Yageo", price=0.003)
    C(f"C1{2 if ch=='I' else 7}", "680pF", f"{ch}_OUT", f"{p}_N2", S, K, mpn="GRM1555C1H681JA01D", mfr="Murata", price=0.01)
R("R22", "10k", "3V3_RF", "IF_VREF", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
R("R23", "10k", "IF_VREF", "GND", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003)
C("C20", "10uF", "IF_VREF", "GND", S, K, fp="0603", mpn="GRM188R61A106KE69D", mfr="Murata", price=0.03)
K = "Head connector JST SH 6-pos (to carrier J30/J31)"
D.ic("J1", "JST SH 6-pos R/A", "SM06B-SRSS-TB(LF)(SN)", "JST", "SH 1.0", S, K, [("1", "5V0", "5V0_R"), ("2", "GND", "GND"), ("3", "EN", "RF_EN")], [("4", "I_OUT", "I_OUT"), ("5", "Q_OUT", "Q_OUT"), ("6", "AGND", "GND")],
     note=OK + "JST SH", price=0.35)
R("R24", "10k", "RF_EN", "GND", S, K, mpn="RC0402FR-0710KL", mfr="Yageo", price=0.003, note="TX off unless MCU enables")

# =====================================================================================================
D.sheet("BP-01", "Smart battery pack OB-BAT-4S81 (inside pack, built by pack OEM to this schematic)", "4S1P LG M58T · BQ40Z50-R2 gauge/protector · BQ771807 2nd-level OVP")
S = "BP-01"; K = "Cells (4S1P 21700, 5.65 Ah, 81 Wh)"
cells = ["BAT_N", "VC1", "VC2", "VC3", "VC4"]
for i in range(4):
    D.ic(f"B{i+1}", "Li-ion 21700 5.65 Ah", "INR21700-M58T", "LG Energy Solution", "21700", S, K, [("-", "−", cells[i])], [("+", "+", cells[i+1])], note="✔ LG M58T spec (Ø21.8 × 71)", price=6.27)
K = "BQ40Z50-R2 fuel gauge + protection (SMBus to host)"
D.ic("U1", "1–4S gauge + protector, Impedance Track", "BQ40Z50RSMR-R2", "TI", "VQFN-32 4x4", S, K,
     [("BAT", "BAT", "VC4"), ("VC4", "VC4", "VC4"), ("VC3", "VC3", "VC3"), ("VC2", "VC2", "VC2"), ("VC1", "VC1", "VC1"), ("SRP", "SRP", "SNS_P"), ("SRN", "SRN", "SNS_N"),
      ("TS1", "TS1", "NTC1"), ("TS2", "TS2", "NTC2"), ("TS3", "TS3", "NTC_FET")],
     [("CHG", "CHG", "CHG_G"), ("DSG", "DSG", "DSG_G"), ("PACK", "PACK", "PACK_P"), ("FUSE", "FUSE", "FUSE_G"), ("SMBC", "SMBC", "SMBC_P_I"), ("SMBD", "SMBD", "SMBD_P_I"),
      ("PRES", "PRES", "PRES_P"), ("VSS", "VSS", "BAT_N")],
     note="⚠ pin numbers per BQ40Z50-R2 DS — pack OEM layout (reference design SLUUBK0)", price=2.40)
D.ic("U2", "2nd-level overvoltage protector (4S)", "BQ771807DPJR", "TI", "WSON-8", S, K, [("VDD", "VDD", "VC4"), ("V4", "V4", "VC4"), ("V3", "V3", "VC3"), ("V2", "V2", "VC2"), ("V1", "V1", "VC1")],
     [("OUT", "OUT", "FUSE_G"), ("VSS", "VSS", "BAT_N")], note="⚠ pin numbers per BQ7718xx DS", price=0.62)
D.fet("Q1", "CHG FET 30V", "CSD17578Q5A", "TI", "SON5x6", "BATP_MID", "CHG_G", "PACK_P", S, K, price=0.35)
D.fet("Q2", "DSG FET 30V", "CSD17578Q5A", "TI", "SON5x6", "BATP_MID", "DSG_G", "VC4_F", S, K, price=0.35)
D.ic("F1", "Self-control protector (chemical fuse) 12 A", "SFJ-1212", "Dexerials", "SMD", S, K, [("1", "IN", "VC4")], [("2", "OUT", "VC4_F"), ("3", "HEATER", "FUSE_G")], note="⚠ Dexerials SCP pin map", price=0.85)
R("RS1", "1mR 1% 2512 (in series: cell stack − → PACK−)", "BAT_N", "PACK_N", S, K, fp="2512", mpn="WSLP25121L000FEA", mfr="Vishay", price=0.45,
  note="All pack current flows through RS1 (SLUUBK0 topology)")
R("R4", "100R", "BAT_N", "SNS_P", S, K, mpn="RC0402FR-07100RL", mfr="Yageo", price=0.003, note="SRP filter, cell side of RS1")
R("R5", "100R", "PACK_N", "SNS_N", S, K, mpn="RC0402FR-07100RL", mfr="Yageo", price=0.003, note="SRN filter, pack side of RS1")
C("C1", "0.1uF", "SNS_P", "SNS_N", S, K, mpn="GRM155R71C104KA88D", mfr="Murata", price=0.01, note="differential coulomb-counter filter")
for i, n in enumerate(("NTC1", "NTC2", "NTC_FET")):
    R(f"RT{i+1}", "NTC 10k B3435", n, "BAT_N", S, K, mpn="NCU15XH103F60RC", mfr="Murata", price=0.064)
K = "Pack plug TE 787439-1 (mates J3 on carrier)"
D.ic("J1", "Battery receptacle 5-pos (right-hand key)", "787439-1", "TE", "SMD", S, K, [("1", "PACK+", "PACK_P"), ("2", "SMBC", "SMBC_P"), ("3", "SMBD", "SMBD_P")], [("4", "PRES", "PRES_P"), ("5", "PACK-", "PACK_N")],
     note=OK + "TE catalog 787439-1", price=3.49)
R("R1", "0R (PRES to PACK- in pack)", "PRES_P", "PACK_N", S, K, mpn="RC0603JR-070RL", mfr="Yageo", price=0.003)
for ref, n in [("R2", "SMBC_P"), ("R3", "SMBD_P")]:
    R(ref, "100R series", n, n + "_I", S, K, mpn="RC0402FR-07100RL", mfr="Yageo", price=0.003)

if __name__ == "__main__":
    print(len(D.parts), "parts,", len(D.nets()), "nets")
    for i in D.erc():
        print(i[0], i[1], i[2][:3])
