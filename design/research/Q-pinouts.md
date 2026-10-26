# Q: Pinouts for the Outer Bounds Pro production schematic

Researched 7 Oct 2026 from manufacturer datasheets. Each table gives the source and its revision. Anything I could not check against a primary document is marked **[unverified]**.

Method: I downloaded the PDFs and converted them to text with `pdftotext`. Pin numbers were read from the datasheet pin tables, not from distributor summaries. Two exceptions: the VC MIPI manual was read from its HTML page and dimension drawing, and the VIEWE panel has no public datasheet.

---

## 1. STMicro STM32G474CET6 (LQFP48)

**Source:** DS12288 *STM32G474xB/xC/xE datasheet*, Table 12 "pin definition" (pp. 56–71) and §3.7/§3.19/§3.21. st.com (`https://www.st.com/resource/en/datasheet/stm32g474ce.pdf`, Rev 6) refused automated download. I therefore parsed the **Rev 1** copy from Farnell (`https://www.farnell.com/datasheets/2818776.pdf`). The LQFP48 pin numbers match the standard G4 LQFP48 ballout. Before release, diff Table 12 against Rev 6. **[pin-function list verified against Rev 1 only]**

The LQFP48 column is the 3rd pin-number column of Table 12: WLCSP81 | UFQFPN48 | **LQFP48** | LQFP64 … I identified it because that column has VSS at pins 19/23/35/47, which the exposed-pad UFQFPN48 does not have.

### 1a. Pin number to name (LQFP48)

| Pin | Name | Type | Key alternate / additional functions available on LQFP48 |
|---|---|---|---|
| 1 | VBAT | S | (tie to VDD if no backup cell) |
| 2 | PC13 | I/O FT | TIM1_BKIN, TIM1_CH1N, TIM8_CH4N; WKUP2, RTC_TAMP1/TS/OUT1. Low-current pin: max 2 MHz/30 pF, never a current source |
| 3 | PC14-OSC32_IN | I/O FT | OSC32_IN (same limits as PC13) |
| 4 | PC15-OSC32_OUT | I/O FT | OSC32_OUT (same limits as PC13) |
| 5 | PF0-OSC_IN | I/O FT_fa | **OSC_IN (HSE)**, I2C2_SDA, SPI2_NSS, TIM1_CH3N, ADC1_IN10 |
| 6 | PF1-OSC_OUT | I/O FT_a | **OSC_OUT (HSE)**, SPI2_SCK, ADC2_IN10, COMP3_INM |
| 7 | PG10-NRST | I/O FT | **NRST**, MCO |
| 8 | PA0 | I/O TT_a | TIM2_CH1, USART2_CTS, COMP1_OUT, TIM8_BKIN; ADC12_IN1, **COMP1_INM, COMP3_INP**, WKUP1 |
| 9 | PA1 | I/O TT_a | TIM2_CH2, USART2_RTS_DE, TIM15_CH1N; ADC12_IN2, **COMP1_INP**, OPAMP1/3_VINP |
| 10 | PA2 | I/O FT_a | TIM2_CH3, **USART2_TX**, **LPUART1_TX**, COMP2_OUT, TIM15_CH1; ADC1_IN3, **COMP2_INM**, OPAMP1_VOUT |
| 11 | PA3 | I/O TT_a | TIM2_CH4, **USART2_RX**, **LPUART1_RX**, TIM15_CH2; ADC1_IN4, **COMP2_INP** |
| 12 | PA4 | I/O TT_a | **SPI1_NSS**, **SPI3_NSS**, USART2_CK, TIM3_CH2; ADC2_IN17, **DAC1_OUT1**, COMP1_INM |
| 13 | PA5 | I/O TT_a | **SPI1_SCK**, TIM2_CH1/ETR; ADC2_IN13, **DAC1_OUT2**, COMP2_INM |
| 14 | PA6 | I/O TT_a | **SPI1_MISO**, TIM16_CH1, TIM3_CH1, TIM8_BKIN, TIM1_BKIN, COMP1_OUT, LPUART1_CTS; ADC2_IN3, **DAC2_OUT1** |
| 15 | PA7 | I/O TT_a | **SPI1_MOSI**, TIM17_CH1, TIM3_CH2, TIM8_CH1N, TIM1_CH1N, COMP2_OUT; ADC2_IN4, **COMP2_INP** |
| 16 | PB0 | I/O TT_a | **HRTIM1_FLT5**, TIM3_CH3, TIM8_CH2N, TIM1_CH2N; ADC3_IN12/ADC1_IN15, **COMP4_INP** |
| 17 | PB1 | I/O TT_a | HRTIM1_SCOUT, TIM3_CH4, TIM8_CH3N, TIM1_CH3N, COMP4_OUT, LPUART1_RTS_DE; ADC3_IN1/ADC1_IN12, **COMP1_INP** |
| 18 | PB2 | I/O TT_a | HRTIM1_SCIN, LPTIM1_OUT, TIM5_CH1, TIM20_CH1, I2C3_SMBA, RTC_OUT2; ADC2_IN12, **COMP4_INM** |
| 19 | VSSA | S | |
| 20 | VREF+ | S | VREFBUF_OUT |
| 21 | VDDA | S | |
| 22 | PB10 | I/O TT_a | **HRTIM1_FLT3**, **USART3_TX**, **LPUART1_RX**, TIM2_CH3, TIM1_BKIN; **COMP5_INM** |
| 23 | VSS | S | |
| 24 | VDD | S | |
| 25 | PB11 | I/O TT_a | **HRTIM1_FLT4**, **USART3_RX**, **LPUART1_TX**, TIM2_CH4; ADC12_IN14, **COMP6_INP** |
| 26 | PB12 | I/O TT_a | **HRTIM1_CHC1**, **SPI2_NSS**, I2C2_SMBA, USART3_CK, TIM1_BKIN, LPUART1_RTS_DE, FDCAN2_RX; ADC4_IN3/ADC1_IN11, **COMP7_INM** |
| 27 | PB13 | I/O TT_a | **HRTIM1_CHC2**, **SPI2_SCK**, TIM1_CH1N, USART3_CTS, LPUART1_CTS, FDCAN2_TX; ADC3_IN5, **COMP5_INP** |
| 28 | PB14 | I/O TT_a | **HRTIM1_CHD1**, **SPI2_MISO**, TIM15_CH1, TIM1_CH2N, USART3_RTS_DE, COMP4_OUT; ADC4_IN4/ADC1_IN5, **COMP7_INP** |
| 29 | PB15 | I/O TT_a | **HRTIM1_CHD2**, **SPI2_MOSI**, TIM15_CH2/CH1N, TIM1_CH3N, COMP3_OUT; ADC4_IN5/ADC2_IN15, **COMP6_INM** |
| 30 | PA8 | I/O FT_a | **HRTIM1_CHA1**, **I2C3_SCL**, **I2C2_SDA**, TIM1_CH1, USART1_CK, MCO, COMP7_OUT; ADC5_IN1 |
| 31 | PA9 | I/O FT_fda | **HRTIM1_CHA2**, **USART1_TX**, **I2C2_SCL**, I2C3_SMBA, TIM1_CH2, TIM2_CH3, COMP5_OUT; ADC5_IN2, UCPD1_DBCC1 |
| 32 | PA10 | I/O FT_fda | **HRTIM1_CHB1**, **USART1_RX**, SPI2_MISO, TIM1_CH3, TIM2_CH4, TIM8_BKIN, COMP6_OUT; UCPD1_DBCC2 |
| 33 | PA11 | I/O FT_u | **HRTIM1_CHB2**, SPI2_MOSI, TIM1_CH4, TIM1_BKIN2, USART1_CTS, FDCAN1_RX, COMP1_OUT; USB_DM |
| 34 | PA12 | I/O FT_u | **HRTIM1_FLT1**, TIM16_CH1, TIM1_ETR, USART1_RTS_DE, FDCAN1_TX, COMP2_OUT; USB_DP |
| 35 | VSS | S | |
| 36 | VDD | S | |
| 37 | PA13 | I/O FT_f | **SWDIO**-JTMS, I2C1_SCL, I2C4_SCL, USART3_CTS, IR_OUT (reset: AF with pull-up) |
| 38 | PA14 | I/O FT_f | **SWCLK**-JTCK, I2C1_SDA, USART2_TX, LPTIM1_OUT, TIM8_CH2 (reset: AF with pull-down) |
| 39 | PA15 | I/O FT_f | **HRTIM1_FLT2**, **I2C1_SCL**, **SPI1_NSS**, **SPI3_NSS**, **USART2_RX**, TIM2_CH1, TIM8_CH1, JTDI (reset: pull-up) |
| 40 | PB3 | I/O FT | **HRTIM1_EEV9**, HRTIM1_SCOUT, **SPI1_SCK**, **SPI3_SCK**, **USART2_TX**, TIM2_CH2, JTDO-TRACESWO |
| 41 | PB4 | I/O FT_c | **HRTIM1_EEV7**, **SPI1_MISO**, **SPI3_MISO**, **USART2_RX**, TIM3_CH1, TIM16_CH1, NJTRST (reset: pull-up); UCPD1_CC2 |
| 42 | PB5 | I/O FT_f | **HRTIM1_EEV6**, **SPI1_MOSI**, **SPI3_MOSI**, **I2C3_SDA**, USART2_CK, I2C1_SMBA, LPTIM1_IN1 |
| 43 | PB6 | I/O FT_c | **HRTIM1_EEV4**, HRTIM1_SCIN, **USART1_TX**, TIM4_CH1, TIM8_CH1, COMP4_OUT; UCPD1_CC1 |
| 44 | PB7 | I/O FT_f | **HRTIM1_EEV3**, **USART1_RX**, **I2C1_SDA**, I2C4_SDA, TIM4_CH2, COMP3_OUT; PVD_IN |
| 45 | PB8-BOOT0 | I/O FT_f | **BOOT0**, **HRTIM1_EEV8**, **I2C1_SCL**, **USART3_RX**, TIM4_CH3, TIM8_CH2, COMP1_OUT, FDCAN1_RX |
| 46 | PB9 | I/O FT_f | **HRTIM1_EEV5**, **I2C1_SDA**, **USART3_TX**, TIM4_CH4, TIM8_CH3, COMP2_OUT, FDCAN1_TX |
| 47 | VSS | S | |
| 48 | VDD | S | |

### 1b. Requested alternate functions: where they land on LQFP48

| Function | LQFP48 pins (port) | Not bonded out on LQFP48 |
|---|---|---|
| HRTIM1_CHA1 / CHA2 | 30 (PA8) / 31 (PA9) | |
| HRTIM1_CHB1 / CHB2 | 32 (PA10) / 33 (PA11) | |
| HRTIM1_CHC1 / CHC2 | 26 (PB12) / 27 (PB13) | |
| HRTIM1_CHD1 / CHD2 | 28 (PB14) / 29 (PB15) | |
| **HRTIM1_CHE1 / CHE2** | **none** | PC8 / PC9 (LQFP64+) |
| **HRTIM1_CHF1 / CHF2** | **none** | PC6 / PC7 (LQFP64+) |
| FLT1 | 34 (PA12) | |
| FLT2 | 39 (PA15) | |
| FLT3 | 22 (PB10) | |
| FLT4 | 25 (PB11) | |
| FLT5 | 16 (PB0) | also PC7 |
| **FLT6** | **none** | PC10 |
| EEV1 / EEV2 | **none** | PC12 / PC11 |
| EEV3 | 44 (PB7) | |
| EEV4 | 43 (PB6) | |
| EEV5 | 46 (PB9) | |
| EEV6 | 42 (PB5) | |
| EEV7 | 41 (PB4) | |
| EEV8 | 45 (PB8-BOOT0) | |
| EEV9 | 40 (PB3) | |
| EEV10 | **none** | PC5 / PC6 |
| SPI1 NSS/SCK/MISO/MOSI | NSS 12 (PA4), 39 (PA15); SCK 13 (PA5), 40 (PB3); MISO 14 (PA6), 41 (PB4); MOSI 15 (PA7), 42 (PB5) | |
| SPI2 NSS/SCK/MISO/MOSI | NSS 26 (PB12), 5 (PF0); SCK 27 (PB13), 6 (PF1); MISO 28 (PB14), 32 (PA10); MOSI 29 (PB15), 33 (PA11) | PF9/PF10 SCK |
| SPI3 NSS/SCK/MISO/MOSI | NSS 12 (PA4), 39 (PA15); SCK 40 (PB3); MISO 41 (PB4); MOSI 42 (PB5) | PC10/PC11/PC12 |
| USART1 TX/RX | TX 31 (PA9), 43 (PB6); RX 32 (PA10), 44 (PB7) | PC4/PC5 |
| USART2 TX/RX | TX 10 (PA2), 38 (PA14), 40 (PB3); RX 11 (PA3), 39 (PA15), 41 (PB4) | |
| USART3 TX/RX | TX 22 (PB10), 46 (PB9); RX 25 (PB11), 45 (PB8) | PC10/PC11 |
| LPUART1 TX/RX | TX 10 (PA2), 25 (PB11); RX 11 (PA3), 22 (PB10) | |
| I2C1 SCL/SDA | SCL 37 (PA13), 39 (PA15), 45 (PB8); SDA 38 (PA14), 44 (PB7), 46 (PB9) | |
| I2C2 SCL/SDA | SCL **31 (PA9) only**; SDA 30 (PA8), 5 (PF0) | PC4 |
| I2C3 SCL/SDA | SCL **30 (PA8) only**; SDA 42 (PB5) | PC8, PC9, PC11 |
| SWDIO / SWCLK | 37 (PA13) / 38 (PA14) | |
| HSE OSC_IN / OSC_OUT | 5 (PF0) / 6 (PF1) | |
| BOOT0 | 45 (PB8-BOOT0) | |
| NRST | 7 (PG10-NRST) | |
| DAC external outputs | DAC1_OUT1 12 (PA4), DAC1_OUT2 13 (PA5), DAC2_OUT1 14 (PA6) | DAC3 and DAC4 (4 ch) are internal only |
| COMPx_INP | COMP1: 9 (PA1), 17 (PB1); COMP2: 11 (PA3), 15 (PA7); COMP3: 8 (PA0); COMP4: 16 (PB0); COMP5: 27 (PB13); COMP6: 25 (PB11); COMP7: 28 (PB14) | |
| COMPx_INM (external) | COMP1: 8, 12; COMP2: 10, 13; COMP3: 6; COMP4: 18; COMP5: 22; COMP6: 29; COMP7: 26 | (each INM can also be a DAC3/DAC4 channel or VREFINT fraction, internally) |

**Hard limits from the LQFP48 package:**
- Only HRTIM timer units **A–D** (8 outputs) are bonded out. Timers E and F still exist, but their outputs cannot leave the chip.
- Only FLT1–FLT5 and EEV3–EEV9 are bonded out.
- Six HRTIM outputs fit: 8 are available, and they are paired per timer unit.

**Datasheet facts that bear on the design:**
- §3.19: there are 7 DAC channels, "3 external buffered and 4 internal unbuffered". §3.21: the comparator reference can be "External I/O, DAC output channels, internal reference".
- So a 12-bit DAC threshold for the 3 LED over-current comparators needs **no extra pins**. Use COMPx_INP on an external pin, with DAC3/DAC4 as the internal INM.
- The internal routing of COMPx_OUT to HRTIM FLTx/EEVx is defined in RM0440 (HRTIM fault/external-event source tables). I did not open RM0440, so the exact COMP to FLT pairing is **[unverified]**. Confirm it in CubeMX.
- If that routing works, the external TLV3201 comparators become a redundant second layer. Alternatively, the TLV3201 outputs can drive the FLT pins as planned.

**Footnotes from Table 12 that matter:**
- PC13–PC15: 3 mA sink limit, ≤2 MHz.
- After reset, PA13/PA15/PB4 have pull-ups and PA14 has a pull-down (debug AF).
- PB8: leave it out of analog mode after start-up.
- BOOT0 can come from the PB8 pin or from the nBOOT0 option bit, selected by nSWBOOT0 (§3.7).

### 1c. Proposed conflict-free pin assignment (STM32G474CET6, LQFP48)

**Design choice:** each camera trigger and its LED gate share one HRTIM timer unit, so the trigger-to-flash offset is set by compare registers on the same counter:
- Timer A: CAM1 / LED1
- Timer B: CAM2 / LED2
- Timer C: CAM3 / LED3

Timer D is left as a spare. SPI2 is not usable, because its pins are the HRTIM C/D outputs, so the host link uses SPI1 on PA4–PA7. I2C2 and I2C3 are also unusable: their only SCL pins are HRTIM outputs PA9 and PA8. That leaves I2C1, placed on PA15/PB9 so PB8-BOOT0 stays a clean boot strap.

| Pin | Port | AF (number **[verify in CubeMX]**) | Net | Notes |
|---|---|---|---|---|
| 1 | VBAT | – | +3V3_MCU | 100 nF (no RTC backup) |
| 2 | PC13 | GPIO | SPARE / STATUS_LED (sink only) | 3 mA, ≤2 MHz |
| 3 | PC14 | – | NC (or 32.768 kHz LSE) | |
| 4 | PC15 | – | NC (or LSE) | |
| 5 | PF0-OSC_IN | HSE | XTAL_IN | HSE crystal (e.g. 24 MHz) so HRTIM runs from a crystal-locked 170 MHz PLL |
| 6 | PF1-OSC_OUT | HSE | XTAL_OUT | |
| 7 | PG10-NRST | NRST | MCU_NRST | 100 nF to GND, to SWD header and a host GPIO (open-drain) |
| 8 | PA0 | analog | LED3_ISENSE | COMP3_INP (+ ADC12_IN1); threshold from DAC3/4 internal |
| 9 | PA1 | analog | LED1_ISENSE | COMP1_INP (+ ADC12_IN2) |
| 10 | PA2 | USART2_TX (AF7) | MCU_UART_TX → host RX | |
| 11 | PA3 | USART2_RX (AF7) | MCU_UART_RX ← host TX | |
| 12 | PA4 | SPI1_NSS (AF5) | HOST_SPI_CS_N | SPI1 slave, hardware NSS |
| 13 | PA5 | SPI1_SCK (AF5) | HOST_SPI_SCK | |
| 14 | PA6 | SPI1_MISO (AF5) | HOST_SPI_MISO | |
| 15 | PA7 | SPI1_MOSI (AF5) | HOST_SPI_MOSI | |
| 16 | PB0 | analog | LED2_ISENSE | COMP4_INP (+ ADC). FLT5 stays available if you prefer an external comparator here |
| 17 | PB1 | analog | VLED_SENSE (ADC1_IN12) | LED boost-rail monitor |
| 18 | PB2 | GPIO out | MCU_IRQ_N → host | data-ready / event interrupt |
| 19 | VSSA | – | AGND | |
| 20 | VREF+ | – | VREF+ | 1 µF + 100 nF; tie to VDDA or use VREFBUF |
| 21 | VDDA | – | +3V3A | ferrite + 1 µF + 100 nF |
| 22 | PB10 | HRTIM1_FLT3 (AF13) | LED2_OC_N | from TLV3201 #2 |
| 23 | VSS | – | GND | |
| 24 | VDD | – | +3V3_MCU | 100 nF |
| 25 | PB11 | HRTIM1_FLT4 (AF13) | LED3_OC_N | from TLV3201 #3 |
| 26 | PB12 | HRTIM1_CHC1 (AF13) | CAM3_TRIG | to VC MIPI FPC pin 17 (cam 3); 10 k pull-down |
| 27 | PB13 | HRTIM1_CHC2 (AF13) | LED3_GATE_CMD | to 74LVC1G123 / UCC27611 #3; 10 k pull-down |
| 28 | PB14 | HRTIM1_CHD1 (AF13) | SPARE_HR1 (radar ENABLE pulse or 4th trigger) | |
| 29 | PB15 | HRTIM1_CHD2 (AF13) | SPARE_HR2 | |
| 30 | PA8 | HRTIM1_CHA1 (AF13) | CAM1_TRIG | 10 k pull-down |
| 31 | PA9 | HRTIM1_CHA2 (AF13) | LED1_GATE_CMD | 10 k pull-down |
| 32 | PA10 | HRTIM1_CHB1 (AF13) | CAM2_TRIG | 10 k pull-down |
| 33 | PA11 | HRTIM1_CHB2 (AF13) | LED2_GATE_CMD | 10 k pull-down (USB_DM is not used) |
| 34 | PA12 | HRTIM1_FLT1 (AF13) | LED1_OC_N | from TLV3201 #1 (USB_DP is not used) |
| 35 | VSS | – | GND | |
| 36 | VDD | – | +3V3_MCU | 100 nF |
| 37 | PA13 | SWDIO | SWDIO | Tag-Connect / 10-pin SWD |
| 38 | PA14 | SWCLK | SWCLK | |
| 39 | PA15 | I2C1_SCL (AF4) | I2C_SCL | 2.2 k pull-up; Fm+ capable (FT_f) |
| 40 | PB3 | TRACESWO (AF0) | SWO | or HRTIM EEV9 spare |
| 41 | PB4 | GPIO / EEV7 | SPARE | reset pull-up (NJTRST); UCPD CC2 pin |
| 42 | PB5 | HRTIM1_EEV6 (AF13) | CAM3_FLASH (optional) | camera flash_from_sensor (FPC pin 18) as an exposure-active input |
| 43 | PB6 | HRTIM1_EEV4 (AF13) | CAM2_FLASH (optional) | UCPD CC1 pin; see note below |
| 44 | PB7 | HRTIM1_EEV3 (AF13) | CAM1_FLASH (optional) | |
| 45 | PB8-BOOT0 | BOOT0 | BOOT0 | 10 k to GND plus a test pad / host GPIO for the ROM bootloader |
| 46 | PB9 | I2C1_SDA (AF4) | I2C_SDA | 2.2 k pull-up |
| 47 | VSS | – | GND | |
| 48 | VDD | – | +3V3_MCU | 4.7 µF bulk + 100 nF |

**Check against the requirements:**
- 6 HRTIM outputs: PA8, PA9, PA10, PA11, PB12, PB13.
- 3 HRTIM faults: PA12 (FLT1), PB10 (FLT3), PB11 (FLT4). FLT2 (PA15) and FLT5 (PB0) remain as alternates.
- SPI slave: SPI1 on PA4–PA7.
- UART: USART2 on PA2/PA3.
- I2C master: I2C1 on PA15/PB9.
- Comparator inputs: COMP1/3/4 INP on PA1/PA0/PB0, with DAC3/DAC4 internal thresholds.
- HSE, SWD, NRST and BOOT0 are on their dedicated pins.
- No pin is used twice.

**Alternatives if needed:**
- If the external DAC output pins are wanted (DAC1 on PA4/PA5), move the SPI slave to SPI1 on PA15/PB3/PB4/PB5. I2C1 then has to move to PB8(SCL)/PB9(SDA). That requires programming nSWBOOT0 = 0 so that the I2C pull-up on PB8 does not force boot-from-ROM. It is workable but riskier on first-article boards.
- The UART could go on USART1 PB6/PB7 instead. Avoid that: PB4/PB6 are UCPD CC pins with "dead battery" pull-down behaviour (strapped by DBCC1/2 = PA9/PA10, which here are HRTIM outputs). Firmware should set PWR_CR3.UCPD_DBDIS at boot whichever pins are used. **[behaviour per RM0440, unverified]**

**Schematic notes:**
- All HRTIM outputs are Hi-Z until firmware configures them. Pull-downs on every CAM_TRIG and LED_GATE line keep cameras and LEDs inert through reset and boot.
- With HSE, HRTIM resolution is 184 ps at f_HRTIM = 170 MHz (DS12288 front page).

---

## 2. TI MSPM0G3507SRHBR (VQFN-32, RHB, 5 × 5 mm)

**Source:** SLASEX6C (Rev C, Oct 2025), Fig. 6-5 and Table 6-2 "Pin Attributes", Table 6-3, §6.4, §9.1. https://www.ti.com/lit/ds/symlink/mspm0g3507.pdf

| Pin | Name | IO type | Analog | Digital functions [PINCM.PF index] |
|---|---|---|---|---|
| 1 | PA0 | 5 V-tol open-drain | – | UART0_TX[2], I2C0_SDA[3], TIMA0_C0[4], TIMA_FAL1[5], TIMG8_C1[6], FCC_IN[7]; default BSL I2C_SDA |
| 2 | PA1 | 5 V-tol open-drain | – | UART0_RX[2], I2C0_SCL[3], TIMA0_C1[4], TIMA_FAL2[5], TIMG8_IDX[6], TIMG8_C0[7]; default BSL I2C_SCL |
| 3 | **NRST** | Reset | – | active-low reset; 47 kΩ to VDD + 10 nF to GND (Fig. in §9.1) |
| 4 | **VDD** | Power | – | 10 µF + 0.1 µF |
| 5 | **VSS** | Power | – | |
| 6 | PA2 | Std | ROSC | TIMG8_C1[2], SPI0_CS0[3], TIMG7_C1[4], SPI1_CS0[5] (ROSC: 100 kΩ 0.1 % if FCL used) |
| 7 | PA3 | Std | LFXIN | TIMG8_C0[2], SPI0_CS1[3], UART2_CTS[4], TIMA0_C2[5], COMP1_OUT[6], TIMG7_C0[7], TIMA0_C1[8], I2C1_SDA[9] |
| 8 | PA4 | Std | LFXOUT | TIMG8_C1[2], SPI0_POCI[3], UART2_RTS[4], TIMA0_C3[5], LFCLK_IN[6], TIMG7_C1[7], TIMA0_C1N[8], I2C1_SCL[9] |
| 9 | PA5 | Std | HFXIN | TIMG8_C0[2], SPI0_PICO[3], TIMA_FAL1[4], TIMG0_C0[5], TIMG6_C0[6], FCC_IN[7] |
| 10 | PA6 | Std | HFXOUT | TIMG8_C1[2], SPI0_SCK[3], TIMA_FAL0[4], TIMG0_C1[5], HFCLK_IN[6], TIMG6_C1[7], TIMA0_C2N[8] |
| 11 | PA7 | Std | – | COMP0_OUT[2], CLK_OUT[3], TIMG8_C0[4], TIMA0_C2[5], TIMG8_IDX[6], TIMG7_C1[7], TIMA0_C1[8] |
| 12 | PA8 | Std | – | UART1_TX[2], SPI0_CS0[3], UART0_RTS[4], TIMA0_C0[5], TIMA1_C0N[6] |
| 13 | PA9 | High-speed | – | UART1_RX[2], SPI0_PICO[3], UART0_CTS[4], TIMA0_C1[5], RTC_OUT[6], TIMA0_C0N[7], TIMA1_C1N[8], CLK_OUT[9] |
| 14 | PA10 | High-drive | – | UART0_TX[2], SPI0_POCI[3], I2C0_SDA[4], TIMA1_C0[5], TIMG12_C0[6], TIMA0_C2[7], I2C1_SDA[8], CLK_OUT[9]; **default BSL UART_TX** |
| 15 | PA11 | High-drive | – | UART0_RX[2], SPI0_SCK[3], I2C0_SCL[4], TIMA1_C1[5], COMP0_OUT[6], TIMA0_C2N[7], I2C1_SCL[8]; **default BSL UART_RX** |
| 16 | PA12 | High-speed | – | UART3_CTS[2], SPI0_SCK[3], TIMG0_C0[4], CAN_TX[5], TIMA0_C3[6], FCC_IN[7] |
| 17 | PA13 | High-speed | COMP0_IN2− | UART3_RTS[2], SPI0_POCI[3], UART3_RX[4], TIMG0_C1[5], CAN_RX[6], TIMA0_C3N[7] |
| 18 | PA14 | High-speed | COMP0_IN2+, A0_12 | UART0_CTS[2], SPI0_PICO[3], UART3_TX[4], TIMG12_C0[5], CLK_OUT[6] |
| 19 | PA15 | Std | A1_0, DAC_OUT, OPA0/1_IN2+, COMP0/1_IN3+ | UART0_RTS[2], SPI1_CS2[3], I2C1_SCL[4], TIMA1_C0[5], TIMG8_IDX[6], TIMA1_C0N[7], TIMA0_C2[8] |
| 20 | PA16 | Std | A1_1, OPA1_OUT | COMP2_OUT[2], SPI1_POCI[3], I2C1_SDA[4], TIMA1_C1[5], TIMA1_C1N[6], TIMA0_C2N[7], FCC_IN[8] |
| 21 | PA17 | Std+wake | A1_2, OPA1_IN1−, COMP0_IN1− | UART1_TX[2], SPI1_SCK[3], I2C1_SCL[4], TIMA0_C3[5], TIMG7_C0[6], TIMA1_C0[7] |
| 22 | PA18 | Std+wake | A1_3, OPA1_IN1+, COMP0_IN1+, GPAMP_IN− | UART1_RX[2], SPI1_PICO[3], I2C1_SDA[4], TIMA0_C3N[5], TIMG7_C1[6], TIMA1_C1[7]; **BSL_invoke** (high at reset enters BSL) |
| 23 | PA19 | High-speed | – | **SWDIO**[2] |
| 24 | PA20 | Std | – | **SWCLK**[2] |
| 25 | PA21 | Std | A1_7, COMP2_IN1−, VREF− | UART2_TX[2], TIMG8_C0[3], UART1_CTS[4], TIMA0_C0[5], TIMG6_C0[6] |
| 26 | PA22 | Std | A0_7, GPAMP_OUT, OPA0_OUT | UART2_RX[2], TIMG8_C1[3], UART1_RTS[4], TIMA0_C1[5], CLK_OUT[6], TIMA0_C0N[7], TIMG6_C1[8] |
| 27 | PA23 | Std | COMP1_IN1−, VREF+ | UART2_TX[2], SPI0_CS3[3], TIMA0_C3[4], TIMG0_C0[5], UART3_CTS[6], TIMG7_C0[7], TIMG8_C0[8] |
| 28 | PA24 | Std | A0_3, OPA0_IN1− | UART2_RX[2], SPI0_CS2[3], TIMA0_C3N[4], TIMG0_C1[5], UART3_RTS[6], TIMG7_C1[7], TIMA1_C1[8] |
| 29 | PA25 | Std | A0_2, OPA0_IN1+ | UART3_RX[2], SPI1_CS3[3], TIMG12_C1[4], TIMA0_C3[5], TIMA0_C1N[6] |
| 30 | PA26 | Std | A0_1, COMP0_IN0+, OPA0_IN0+, GPAMP_IN+ | UART3_TX[2], SPI1_CS0[3], TIMG8_C0[4], TIMA_FAL0[5], CAN_TX[6], TIMG7_C0[7] |
| 31 | PA27 | Std | A0_0, COMP0_IN0−, OPA0_IN0− | RTC_OUT[2], SPI1_CS1[3], TIMG8_C1[4], TIMA_FAL2[5], CAN_RX[6], TIMG7_C1[7] |
| 32 | **VCORE** | Power | – | **0.47 µF to VSS, nothing else connected** |
| EP | Thermal pad | – | – | connect to VSS |

**SPI controller options on RHB:**
- **SPI0:**
  - SCK: 10 (PA6), 15 (PA11), 16 (PA12)
  - PICO: 9 (PA5), 13 (PA9), 18 (PA14)
  - POCI: 8 (PA4), 14 (PA10), 17 (PA13)
  - CS0: 6 (PA2), 12 (PA8)
  - CS1: 7 (PA3); CS2: 28 (PA24); CS3: 27 (PA23)
- **SPI1:**
  - SCK: 21 (PA17); PICO: 22 (PA18); POCI: 20 (PA16)
  - CS0: 6 (PA2), 30 (PA26); CS1: 31 (PA27); CS2: 19 (PA15); CS3: 29 (PA25)

**UART options:**
- UART0: TX 1/14, RX 2/15
- UART1: TX 12/21, RX 13/22
- UART2: TX 25/27, RX 26/28
- UART3: TX 18/30, RX 17/29

**Debug and boot pins:**
- SWD: SWDIO 23 (PA19), SWCLK 24 (PA20).
- NRST: pin 3.
- BSL: UART on PA10/PA11; I2C on PA0/PA1; invoke on PA18.

**Suggested use (radar ADC front-end, ADS131M02):**
- SPI0 controller on the high-speed pins: SCK 16 (PA12), POCI 17 (PA13), PICO 18 (PA14), CS0 12 (PA8).
- ADS131M02 CLKIN at 8.192 MHz from CLK_OUT on 11 (PA7, PF 3) or a timer output.
- DRDY to any GPIO, e.g. 13 (PA9).
- UART0 on 14/15 to the host. This is also the ROM BSL path, so the host can reflash the part.
- Keep PA18 pulled low (BSL_invoke) unless entering the bootloader.

---

## 3. TI ADS131M02IPWR (TSSOP-20, PW)

**Source:** SBAS853A (Apr 2021), Table 5-1. https://www.ti.com/lit/ds/symlink/ads131m02.pdf

| Pin | Name | Type | Description |
|---|---|---|---|
| 1 | AVDD | Supply | Analog supply; 1 µF to AGND |
| 2 | AGND | Supply | Analog ground |
| 3 | AIN0P | Analog in | Ch0 + |
| 4 | AIN0N | Analog in | Ch0 − |
| 5 | AIN1N | Analog in | Ch1 − |
| 6 | AIN1P | Analog in | Ch1 + |
| 7–10 | NC | – | No connect |
| 11 | SYNC/RESET | Digital in | Sync / reset, active low |
| 12 | CS | Digital in | Chip select, active low |
| 13 | DRDY | Digital out | Data ready, active low |
| 14 | SCLK | Digital in | Serial clock |
| 15 | DOUT | Digital out | Serial data out |
| 16 | DIN | Digital in | Serial data in |
| 17 | CLKIN | Digital in | Master clock (8.192 MHz nominal, 0.3–8.4 MHz in HR mode) |
| 18 | CAP | Analog out | Digital LDO output; 220 nF to DGND |
| 19 | DGND | Supply | Digital ground |
| 20 | DVDD | Supply | Digital I/O supply; 1 µF to DGND |

Note that the order is AIN1**N** at pin 5 and AIN1**P** at pin 6, which is the reverse of channel 0. Rev A explicitly "corrected analog input pin numbering", so use Rev A or later.

---

## 4. TI TLV9064IPWR (TSSOP-14)

**Source:** SBOS839N (Rev N, Jul 2026), Table 5-5. https://www.ti.com/lit/ds/symlink/tlv9064.pdf

| Pin | Name | Pin | Name |
|---|---|---|---|
| 1 | OUT1 | 8 | OUT3 |
| 2 | IN1− | 9 | IN3− |
| 3 | IN1+ | 10 | IN3+ |
| 4 | V+ | 11 | V− (GND) |
| 5 | IN2+ | 12 | IN4+ |
| 6 | IN2− | 13 | IN4− |
| 7 | OUT2 | 14 | OUT4 |

Supply is 1.8–5.5 V.

---

## 5. TI UCC27611DRVR (WSON-6, DRV, 2 × 2 mm)

**Source:** SLUSBA5F (Mar 2018), Pin Functions. https://www.ti.com/lit/ds/symlink/ucc27611.pdf

| Pin | Name | I/O | Description |
|---|---|---|---|
| 1 | VDD | I | Bias supply 4–18 V (abs max 20 V); ceramic cap to GND |
| 2 | IN− | I | Inverting input. Tie to GND to use IN+ non-inverting |
| 3 | IN+ | I | Non-inverting input. Tie to VDD to use IN− inverting |
| 4 | OUTL | O | 6 A sink output |
| 5 | OUTH | O | 4 A source output |
| 6 | VREF | O | Internal 5 V regulated drive rail (4.75–5.15 V); ceramic cap to GND (the EC table uses 2 µF) |
| 7 (pad) | GND | – | Exposed pad is the only ground; all signals are referenced to it |

The split OUTH/OUTL allows separate turn-on and turn-off gate resistors. The gate drive swing is VREF (5 V), not VDD.

---

## 6. Nexperia 74LVC1G123DC (VSSOP-8, SOT765-1, marking "Y3")

**Source:** 74LVC1G123 Product data sheet Rev 8 (14 Aug 2023), Fig. 3, Table 3, Table 8 (dynamic characteristics) and note [3]. https://assets.nexperia.com/documents/data-sheet/74LVC1G123.pdf

| Pin | Name | Description |
|---|---|---|
| 1 | A | Negative-edge trigger input (B must be HIGH) |
| 2 | B | Positive-edge trigger input (A must be LOW) |
| 3 | CLR | Direct reset, active LOW; a rising edge also triggers |
| 4 | GND | Ground |
| 5 | Q | Active-HIGH output pulse |
| 6 | CEXT | External capacitor (−) |
| 7 | REXT/CEXT | External R to VCC and capacitor (+) node |
| 8 | VCC | 1.65–5.5 V |

**Pulse-width formula (note [3]):** tW = K × REXT × CEXT, where tW is in ns, REXT in kΩ, CEXT in pF, and K ≈ 1. The data sheet says the formula is valid **only for CEXT > 10 nF**; below that, use the curves in Fig. 11–13.

- REXT minimum is 1 kΩ at VCC ≥ 3.0 V (5 kΩ at 2.0 V).
- Datasheet anchor points at VCC 3.0–3.6 V:

| REXT | CEXT | tW typ | tW max |
|---|---|---|---|
| 10 kΩ | 100 pF | 1.2 µs | 1.8 µs |
| 10 kΩ | 10 nF | 100 µs | 110 µs |
| 10 kΩ | 0.1 µF | 1.0 ms | 1.05 ms |

- The device is **retriggerable**: a new trigger edge restarts tW.

**(a) 8 µs maximum-pulse cut-off** (Q gates the LED drive; the LED is enabled only while Q is high):
- CEXT must be < 10 nF here, because 8 µs with CEXT ≥ 10 nF would need REXT < 1 kΩ, which is below the minimum. So the value comes from the small-C curves, not the formula.
- **Nominal 8 µs:** REXT = 10.0 kΩ 1 %, CEXT = 750 pF C0G. R·C = 7.5 µs; expect about 7.7–8 µs typ (the small-C region runs above R·C, e.g. 1.2 µs at R·C = 1 µs).
- **Guaranteed ≤ 8 µs worst case:** REXT = 10.0 kΩ, CEXT = 560 pF C0G. R·C = 5.6 µs, about 6 µs typ. Applying the datasheet's max/typ spread (up to 1.5× at 100 pF, 1.1× at 10 nF) gives roughly 7–8 µs max. Use this if the longest commanded LED pulse is ≤ 5 µs.
- Both are **[estimated from the datasheet anchor points and curves; trim on the bench]**.

**(b) 300 µs minimum-off hold-off** (triggered on the falling edge of each LED pulse; Q blocks re-arming):
- This is in the CEXT ≥ 10 nF region, where the formula is valid.
- **REXT = 30.1 kΩ 1 %, CEXT = 10 nF C0G** gives tW = 301 µs typ. The max is about +10 % (≈330 µs), scaling from the 100/110 µs anchor.
- If 300 µs must be a guaranteed *minimum*, use **REXT = 33.2 kΩ, CEXT = 10 nF**, giving about 332 µs typ. The minimum tW is not specified, so allow roughly −10 %.
- Because the part retriggers, a burst of pulses holds Q high until 300 µs after the *last* pulse.

---

## 7. TI TLV3201AIDCKR (SC70-5, DCK)

**Source:** TLV3201/TLV3202 datasheet, "Pin Functions: TLV3201" (DCK and DBV share the pinout). https://www.ti.com/lit/ds/symlink/tlv3201.pdf

| Pin | Name | Description |
|---|---|---|
| 1 | OUT | Push-pull output |
| 2 | GND | Negative supply / ground |
| 3 | IN+ | Non-inverting input |
| 4 | IN− | Inverting input |
| 5 | VCC | Positive supply (2.7–5.5 V) |

---

## 8. TI TPS7A2033PDBVR (SOT-23-5, DBV)

**Source:** TPS7A20 datasheet, "Pin Functions: X2SON, SOT-23" and Device Nomenclature. https://www.ti.com/lit/ds/symlink/tps7a20.pdf

| Pin (DBV) | Name | Description |
|---|---|---|
| 1 | IN | Input 1.6–6.0 V; C_IN ≥ 1 µF |
| 2 | GND | Ground |
| 3 | EN | Enable, active high; internal 500 kΩ pull-down (off by default) |
| 4 | NC | No internal connection |
| 5 | OUT | 3.3 V output, 300 mA, ±1.5 %; C_OUT 1–200 µF |

The "P" in the part number is the active output discharge (150 Ω typ pull-down on OUT when disabled). "33" means 3.3 V.

---

## 9. Sensors

### 9a. Murata SCL3300-D01 (12-pin pre-molded, 8.6 × 7.6 × 3.3 mm)

**Source:** SCL3300-D01 datasheet Doc 4921 Rev 4, Table 6 and the component table. https://www.murata.com/~/media/webrenewal/products/sensor/pdf/datasheet/datasheet_scl3300-d01.ashx?la=en-us

| Pin | Name | Type | Description |
|---|---|---|---|
| 1 | AVSS | GND | Analog ground |
| 2 | A_EXTC | AOUT | Analog-core cap: 100 nF X7R to GND |
| 3 | RESERVED | – | Factory use, **connect to GND** |
| 4 | VDD | Supply | 3.0–3.6 V analog supply; 100 nF |
| 5 | CSB | DIN | SPI chip select (internal pull-up) |
| 6 | MISO | DOUT | SPI data out |
| 7 | MOSI | DIN | SPI data in |
| 8 | SCK | DIN | SPI clock (internal pull-down) |
| 9 | DVIO | Supply | SPI I/O supply, 3.0–3.6 V; **must never exceed VDD**; 100 nF |
| 10 | D_EXTC | AOUT | Digital-core cap: 100 nF X7R to GND |
| 11 | DVSS | GND | Digital ground; never float |
| 12 | EMC_GND | GND | EMC ground, connect to GND |

The interface is SPI only: 4-wire, mode 0, no 3-wire mode. CSB must stay high for ≥ 10 µs between frames.

### 9b. Bosch BMI323 (LGA-14, 2.5 × 3.0 × 0.83 mm)

**Source:** BST-BMI323-DS000-13, Table 56. https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi323-ds000.pdf

| Pin | Name | Function (SPI-4w / I²C) |
|---|---|---|
| 1 | SDO | SPI SDO / I²C address LSB (GND = 0x68, VDDIO = 0x69) |
| 2 | NC | do not connect |
| 3 | NC | do not connect |
| 4 | INT1 | Interrupt 1 |
| 5 | VDDIO | 1.08–3.63 V; 100 nF |
| 6 | GNDIO | I/O ground |
| 7 | GND | Ground |
| 8 | VDD | 1.71–3.63 V; 100 nF |
| 9 | INT2 | Interrupt 2 |
| 10 | NC | do not connect |
| 11 | NC | do not connect |
| 12 | CSB | SPI CS (tie to VDDIO for I²C) |
| 13 | SCx | SCK / SCL |
| 14 | SDx | SDI / SDA |

### 9c. Bosch BMP585 (8-pin metal-lid LGA, 3.25 × 3.25 mm)

**Source:** BST-BMP585-DS003-02, Table 26 and §5 (I²C). https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp585-ds003.pdf

| Pin | Name | Function |
|---|---|---|
| 1 | SCX | I²C SCL / SPI SCK |
| 2 | SDX | I²C SDA / SPI SDI (SDIO in 3-wire) |
| 3 | SDO | I²C address LSB (0 = **0x46**, 1 = **0x47**; must not float in I²C) / SPI SDO |
| 4 | VDDIO | 1.08–3.6 V |
| 5 | INT | Interrupt / data-ready (tie to GND if unused) |
| 6 | VSSIO/VSS | Ground |
| 7 | CSB | SPI CS, active low (tie to VDDIO for I²C) |
| 8 | VDD | 1.71–3.6 V |
| 9 | L/M pad | Laser-mark pad, **no connection** |

The BMP585 at 0x46 collides with nothing on the I²C bus here: SHT45 is 0x44, BMI323 0x68.

### 9d. Sensirion SHT45-AD1F (DFN-4, 1.5 × 1.5 × 0.5 mm)

**Source:** SHT4x datasheet Version 7.3 (June 2026), §5.4 "Pin Assignment", §9 Nomenclature and §10 Ordering (SHT45-AD1F-R2 = 3.000.886). https://sensirion.com/resource/datasheet/sht4x

| Pin | Name | Description |
|---|---|---|
| 1 | SDA | Serial data, bidirectional |
| 2 | SCL | Serial clock, input |
| 3 | VDD | Supply, 1.08–3.6 V |
| 4 | VSS | Ground |
| (centre) | die pad | Not connected to any pin; Sensirion does **not** recommend soldering it |

**I²C address: 0x44.** "A" in "AD1F" fixes the address at 0x44; SHT45 is only offered at 0x44. "F" = factory-fitted membrane. Rev 7.3 changed the membrane description from "PTFE" to **polyimide**, with an IP68 rating. Many distributor pages still say PTFE/IP67.

---

## 10. InnoSenT SMR-333 (24 GHz CW I/Q Doppler, SMT)

**Source:** InnoSenT *Data Sheet SMR-313/333* Version 2.2 (28 Jul 2020), pp. 2, 4, 5. https://media.digikey.com/pdf/Data%20Sheets/InnoSenT/200728_Data_Sheet_SMR-3X3_2.2.pdf. Product page: https://www.innosent.de/en/sensors/smr-333/

| Pin | Name | Dir | Comment |
|---|---|---|---|
| 1 | d.n.c. | – | do not connect |
| 2 | d.n.c. | – | do not connect |
| 3 | IF1 | out | **I** (in-phase) IF signal |
| 4 | IF2 | out | **Q** (quadrature) IF signal |
| 5 | enable | in | TX power enable, active high (off 0–0.8 V, on 2–3.3 V). It cuts TX power by about 30 dB but does **not** reduce current |
| 6 | GND | – | analog ground |
| 7 | Vcc | in | supply |
| 8 | d.n.c. | – | do not connect |
| 9 | d.n.c. | – | do not connect |
| 10 | GND | – | analog ground |

**Electrical:**
- VCC is 3.2 / 3.3 / 3.4 V (min/typ/max), a tight ±3 % window, so it needs a dedicated LDO.
- **ICC is 47 mA typ, 57 mA max.**
- TX frequency is 24.150–24.250 GHz with 12.7 dBm EIRP.
- IF bandwidth is DC–1 MHz.
- IF signal is 120–360 µVrms (RCS 0.5 m² at 5 m); noise is 20 µVrms (100 Hz–1 kHz).
- Gain is 29 dB; the −10 dB beam is 43° az × 116° el.
- Operating range is −40 to +85 °C.

**There is no VCO/Vtune pin.** The SMR-333 is fixed-frequency CW. The FMCW variant with Vtune is the SMR-334.

The IF outputs have a DC bias that must be AC-coupled into the TLV9064 gain stage. One secondary source gives it as about 1.4/1.8/2.2 V (min/typ/max), taken from the SMR-3X3 User Manual (FCC filing https://fcc.report/FCC-ID/UXS-SMR3X3/3425359.pdf). It is not stated in the v2.2 data sheet. **[unverified]**

**Power saving:** pulse VCC. VCC must be up for > 3 µs before enable, with enable high for > 1 µs (p. 4 timing diagram).

**Dimensions:**
- 21.4 ± 0.3 × 15.0 ± 0.3 mm, height 3.1 ± 0.3 mm.
- Pad pattern spans 20.4 × 14 mm with 10 pads; pins 1/5 and 6/10 are at the corners.
- Footprint drawing on p. 5: pad 2.2 × 1.05 mm copper, 1.5 mm solder.

---

## 11. Vision Components VC MIPI IMX900 (VK000601 mono; VK000609 colour)

**Source:** *VC MIPI Camera Module Hardware Operating Manual* (online), §1.4.1 "FPC Cable Signals", Technical Data table (IMX568/IMX585C/IMX900), §2.1 order numbers and Appendix A §3.1 dimension drawing. https://www.mipi-modules.com/fileadmin/external/documentation/hardware/VC_MIPI_Camera_Module/index.html

### Module 22-pin FPC connector (sensor-module numbering)

| Pin | Signal | Pin | Signal |
|---|---|---|---|
| 1 | GND | 12 | CSI_DAT2_P |
| 2 | CSI_DAT0_N | 13 | GND |
| 3 | CSI_DAT0_P | 14 | CSI_DAT3_N |
| 4 | GND | 15 | CSI_DAT3_P |
| 5 | CSI_DAT1_N | 16 | GND |
| 6 | CSI_DAT1_P | 17 | **trigger_to_sensor** (input, 3.3 V LVCMOS) |
| 7 | GND | 18 | **flash_from_sensor** (output, 3.3 V LVCMOS) |
| 8 | CSI_CLK_N | 19 | GND |
| 9 | CSI_CLK_P | 20 | I2C_SCL (3.3 V) |
| 10 | GND | 21 | I2C_SDA (3.3 V) |
| 11 | CSI_DAT2_N | 22 | **Vcc3V3** |

**Lanes:**
- 2 or 4 lanes (DAT0–DAT3); 4 lanes are not available through 15-pin cables.
- Up to 1.2 Gbps/lane.
- RAW8/10/12; 2048 × 1536 at 122 fps (8-bit, 4-lane).
- The IMX900 supports "fast trigger mode", with trigger input = Yes and flash output = Yes.

**Processor-side numbering (VC table):**
- With a VC "regular" cable, the processor end is mirrored: sensor pin 1 (GND) lands on processor pin 22, and sensor pin 22 (3V3) on processor pin 1.
- With an "inverse" cable, processor pin n = sensor pin n.
- VC warns that the RPi CMIO 3.0 and Pi Zero 1.3 schematics number the connector the "inverse" way.
- **For our carrier:** draw the connector symbol with RPi numbering (1 = GND … 22 = 3V3). Then order the VC cable variant that maps pin n to pin n, and confirm the contact side with VC before layout. **[cable variant to confirm]**

**Supply:**
- 3.3 V ± 5 %, measured at the module input (excludes cable drop).
- **230 mA max active**, 25 mA standby. Size the 3.3 V camera rail for 3 × 230 mA = 0.69 A plus margin.
- Mass 3.9 g; CRA 8°; −30 to +75 °C operating.

**Board** (Appendix A §3.1 drawing; the IMX900 "same board dimensions" as the IMX296 drawing):
- 23.5 × 22.0 mm, R1.5 corners, PCB 1.54 mm thick.
- **Two Ø2.2 mm mounting holes on a 20.00 mm pitch.** They sit at 1.75 mm and 21.75 mm from the left edge, both 11.0 mm from the bottom edge.
- Two Ø1.0 mm holes at 13.5 mm and 8.5 mm from the bottom, 5.0 mm apart in Y. From the drawing they appear to be at the same X as the mounting holes. **[X position read off drawing, unverified]**
- Sensor package is 14.1 × 14.1 mm; stack is about 2.0 mm above the board.
- Back-side FPC connector depth is 3.9 mm.
- The drawing is for the IMX296; VC states the IMX900 board is identical. **[confirm with the VK000601 STEP model]**

**Trigger timing:** the IMX900 row of the §1.6 trigger-timing table (min trigger width, trigger delay, jitter) was not on the page. The table only lists the OV9281, IMX250 and IMX296 (IMX296: > 10 µs trigger, 5 µs debounce delay, 18.5 ns jitter). **[IMX900 values unverified; ask VC]**

### Match against the Raspberry Pi 22-pin camera connector

**Source:** Raspberry Pi documentation, "Camera connector pinout (22-pin)", https://www.raspberrypi.com/documentation/accessories/camera.html, cross-checked with Arducam https://docs.arducam.com/Raspberry-Pi-Camera/raspberry-pi-camera-pinout/.

**Pinout:**
- RPi 22-pin (0.5 mm, Amphenol F32Q-1A7H1-11022-compatible) is:
  - 1 GND; 2/3 D0−/+; 4 GND; 5/6 D1−/+; 7 GND; 8/9 CK−/+; 10 GND
  - 11/12 D2−/+; 13 GND; 14/15 D3−/+; 16 GND
  - 17 CAM_IO0 (power enable); 18 CAM_IO1 (LED/GPIO); 19 GND; 20 SCL; 21 SDA; 22 3V3
- **This is identical to the VC module numbering.** VC repurposes IO0 → trigger_to_sensor and IO1 → flash_from_sensor.

**Design consequences:**
- On our board, pin 17 must be driven by the STM32 HRTIM (CAM_TRIG), **not** by the host SoC's camera power-enable GPIO.
- Pin 18 goes to an STM32 EEV input (optional) or a test point.
- I²C pull-ups are on the host side; the RPi pulls up to 3.3 V on its own board.

---

## 12. GCT USB4720-03-A (USB-C receptacle)

**Source:** GCT customer drawing USB4720, Rev B (drawing date 26 Oct 2023, PCN 02/01/25), sheet 1. https://gct.co/files/drawings/usb4720.pdf

**Product description:** "Type C Receptacle **For USB2.0**, SMT Type, Mid-Mount, Horizontal, IP67, **16 Pin**". "-03" = 3 µ" gold; "-A" = tape and reel (1300 per reel).

| Pin | Signal | Mating | Pin | Signal | Mating |
|---|---|---|---|---|---|
| A1 | GND | First | B12 | GND | First |
| A4 | VBUS | First | B9 | VBUS | First |
| A5 | CC1 | Second | B8 | SBU2 | Second |
| A6 | Dp1 (D+) | Second | B7 | Dn2 (D−) | Second |
| A7 | Dn1 (D−) | Second | B6 | Dp2 (D+) | Second |
| A8 | SBU1 | Second | B5 | CC2 | Second |
| A9 | VBUS | First | B4 | VBUS | First |
| A12 | GND | First | B1 | GND | First |
| SHELL | GND | | SHELL | GND | |

**USB 2.0 only: yes.** There are no TX/RX SuperSpeed pairs (A2/A3/A10/A11/B2/B3/B10/B11 are absent). SBU1/SBU2 *are* present.

**Ratings:**
- 5 A total on VBUS; 1.25 A on the A5/B5 (CC) pins; 0.25 A on other pins.
- 48 V DC, 240 W rated; IP67 with silicone gasket; 20,000 cycles.

**Layout:**
- It is **mid-mount**, so it sits in a PCB cut-out (8.20 mm wide pad field, 11.30 mm body).
- The drawing's "Recommended PCB Layout" carries a note "Thickness 0.6 ± 0.10 mm". That reads as a mid-mount PCB-thickness requirement. **[confirm with GCT before choosing board thickness]**

**Schematic:**
- Tie A6/B6 (D+) together and A7/B7 (D−) together.
- Give CC1 and CC2 separate 5.1 kΩ Rd resistors (sink).

---

## 13. TE 5787441-1

**Sources:**
- TE product page https://www.te.com/en/product-5787441-1.html
- DigiKey A115527-ND https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/5787441-1/2135744
- TE customer drawing ENG_CD_5787441 (link on the TE page)

**What it is:** a **battery interconnect header**. TE files it under "PCB Connectors > Battery Connector Types". The drawing title is "BATTERY INTERCONNECT". DigiKey lists it as connector style "Battery" in category "Blade Type Power Connectors".

| Attribute | Value |
|---|---|
| Positions | 5, single row |
| **Pitch** | **5.00 mm (0.197")** |
| Orientation / mount | Right-angle, through-hole, straight solder tails, no PCB retention |
| Gender | Male blades (header assembly, "HDR ASY,RA,NO KEY,STR TAIL"), unkeyed |
| Rating | 50 V DC. Current: 8.8 A/contact (TE), 7 A (DigiKey) |
| Temperature | −30 to +70 °C |
| Specs | Product spec 108-1501, application spec 114-24005 |
| Status | It replaces the obsolete 787441-1. TE says "Active" but also "not currently available"; DigiKey shows an 8-week lead time |

It is a laptop/portable battery-pack header from TE catalog section 1773096 SEC09 "Laptops/Portables". **The mating receptacle part number is not on the product page [unverified]**; get it from the customer drawing. Pin-function assignment (e.g. B+, B+, SMBus CLK/DAT or thermistor, B−) is ours to define. With 5 mm pitch, a 5-pin footprint is about 20 mm wide.

---

## 14. Sitronix ST7789 2.4" SPI panel (VIEWE UEED024QV-RH40-A003)

**Confirmed from the VIEWE product page** (https://viewedisplay.com/product/2-4-inch-240320-transflective-sunlight-readable-and-super-low-power-tft-lcd-module-with-mcu-8-16bit-spi-interface/):
- Model UEED024QV-RH40-A003, 2.4", 240 × 320, transflective, normally black.
- Driver **ST7789-T3**.
- Interface MCU 8/16-bit or SPI-3/SPI-4.
- White-LED backlight, −20 to 70 °C.
- A secondary search snippet gave a 36.72 × 48.96 mm active area and a 51.32 × 86.61 × 2.15 mm outline. **[unverified]**

**FPC pin list: [unverified, not published].** The VIEWE spec sheet is behind the product page's "Resource" tab and the VIEWE datasheet centre, and neither could be fetched. The VIEWESMART GitHub (https://github.com/VIEWESMART/STM32_Project) only has firmware for related 2.4" panels (UE024QV-RB40-A038A, GC9307 driver). It drives IM0/IM1/IM2 as GPIOs but does not show this panel's pin numbers. **Do not draw the panel symbol until the VIEWE spec sheet (FPC pin table, LED count and If/Vf) is in hand.**

**The ST7789 interface mode table can be used now.** Source: Sitronix ST7789V datasheet §6.2/§8.1 Table 10, https://newhavendisplay.com/content/datasheets/ST7789V.pdf. Assumed to be the same for ST7789-T3. **[unverified for T3]**

| IM3 | IM2 | IM1 | IM0 | Mode | Data pins |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 0 | **4-line 8-bit serial I** | SDA bidirectional (SDO unused) |
| 1 | 1 | 1 | 0 | **4-line 8-bit serial II** | SDA in, SDO out |
| 0 | 1 | 0 | 1 | 3-line 9-bit serial I | SDA in/out |
| 1 | 1 | 0 | 1 | 3-line 9-bit serial II | SDA in, SDO out |
| 0 | 0 | 0 | 0 | 8080 8-bit parallel | DB[7:0] |
| 0 | 0 | 0 | 1 | 8080 16-bit parallel | DB[15:0] |

**For 4-wire SPI:**
- The nets are: CSX, DCX (D/C), SCL (WRX pin), SDA, optional SDO, RESX, VDD/VDDI (IOVCC), GND, LEDA (backlight anode), LEDK (cathode, often several pins), and IM0–IM2 (IM3 is often not brought out and is internally 0).
- On panels that expose only IM2..IM0, 4-wire SPI is normally **IM2 = 1, IM1 = 1, IM0 = 0**.
- Some vendors re-encode these pins (e.g. Winstar 3-bit tables, or IM1/IM2 merged on one pin), so confirm against the VIEWE sheet.
- If they are not hard-strapped on the FPC, bring the IM pins to straps with 0 Ω options.

---

## Items still [unverified]
1. STM32G474 Table 12 was checked against DS12288 **Rev 1**. Diff it against Rev 6 (st.com blocked automated download). The AF numbers (AF13 for HRTIM, AF5 for SPI1, AF7 for USART2, AF4 for I2C1) and the COMP→HRTIM-fault internal routing must be confirmed in CubeMX / RM0440.
2. The UCPD dead-battery behaviour of PB4/PB6 with PA9/PA10 used as HRTIM outputs (RM0440).
3. The 74LVC1G123 8 µs component values are curve-based estimates; trim on the bench.
4. SMR-333 IF DC bias (≈1.8 V) is from a secondary source, not the v2.2 data sheet.
5. VC MIPI IMX900:
   - trigger timing figures;
   - exact X position of the Ø1.0 holes;
   - which FPC cable variant gives straight-through RPi numbering.
6. GCT USB4720: whether "Thickness 0.6 ± 0.10 mm" is a PCB-thickness requirement.
7. TE 5787441-1: the mating receptacle part number.
8. VIEWE UEED024QV-RH40-A003:
   - the entire FPC pin list;
   - backlight LED count and current;
   - whether the ST7789-T3 IM table matches the ST7789V.
