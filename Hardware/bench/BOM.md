# Bench — Bill of Materials (BOM)

**Per-bench** parts list, derived from [`bench-v1-wiring.md`](bench-v1-wiring.md) and the CANONICAL
objectives in [`bench-v1.md`](bench-v1.md). A full lab is **N benches** (RPi-supervised at V2) — multiply
the per-bench quantities and add the shared/lab items at the bottom.

**Legend:** ✅ on hand · 🛒 to source · phase **V1a** (now) / **V1b** (M7-dependent) / **V2** (HW-mod).
Representative SKUs — verify current part numbers before ordering.

## Core platform

| Item | Qty | Role / objective | Status | Notes |
|---|---|---|---|---|
| CompuLab UCM-iMX8M-Plus SoM | 1 | the compute module under test | ✅ | non-'E' variant |
| SB-UCM carrier board | 1 | breaks out P20/P21/P10/P7, J3/J5, JTAG | ✅ | CompuLab eval carrier |
| 12 V PSU (barrel jack) | 1 | board power (all bench scenarios) | 🛒/✅ | VDC_IN ≤16 V; ≥3 A |

## MCU dev boards (I²C/SPI peers + radio)

| Item | Qty | Role / objective | Status | Notes |
|---|---|---|---|---|
| MSP430 LaunchPad **MSP-EXP430FR2433** (x33) | 2 | **product-baseline supervisor** — reflects the product's real (tight) FRAM constraints; the **fidelity reference** for the supervisor roles: I/O-expander, I²C-master-when-M7-suspended, BSL-from-M7, wake, OLED (obj 5,6,7,9,12,13). **TARGET: prod supervisor firmware fits the FR2433's 15 KB program FRAM** (15.5 KB incl. 512 B info FRAM; 4 KB SRAM) — the size gate. Verified vs TI datasheet. | ✅ | 2 in hand; can order more |
| MSP430 LaunchPad **MSP-EXP430FR2476** (x76) | 2 | **dev / diagnostics** — bigger FRAM (32 KB) to hold a larger **diag ROM** during bring-up; **not necessarily the shipped part** | ✅ | 2 in hand; use for early bring-up, then validate on the x33 baseline |
| Raspberry Pi Pico H (RP2040) | 1 | I²C MCU peer (obj 2) | ✅ | in BOOTSEL when seen |
| Arducam Pico4ML (RP2040 + cam/mic) | 1 | I²C MCU peer; on-Pico TinyML demo (obj 2) | ✅ | camera used on-Pico only (SoM camera = V2) |
| BBC micro:bit **V1.3 (nRF51822)** | 1 | I²C MCU peer (obj 2) | ✅ | nRF51 slave mode limited; needs edge breakout |
| Seeed XIAO nRF52840 (or Adafruit Feather nRF52840) | 1 | **BLE NCP on ECSPI2** (obj 2) — USB-flash, 3.3 V | 🛒 | D2: 3.3 V board + TXB0108, not a bare module |
| nRF52840 dongle (PCA10059) | 1 | **USB Bluetooth** (obj 3) — on J3, no header wiring | ✅ | detected on USB |
| CSR Bluetooth USB dongle | 1 | USB Bluetooth (obj 3, alt) | ✅ | scanning verified |

## Audio

| Item | Qty | Role / objective | Status | Notes |
|---|---|---|---|---|
| MAX98357A I²S amp breakout | 1 | **speaker output** on SAI3-TX (obj 5) | 🛒 | 3.3 V logic; VIN 3V3/5V; no MCLK |
| Small speaker (4–8 Ω, ~3 W) | 1 | amp load | 🛒 | |
| TLV320ADC5140 (EVM or JLCPCB board) | (SPIKE-2) | product analog-mic TDM ADC | 🛒 | **no hobbyist breakout** — TI EVM / JLCPCB; needs U10 rework → **V2** (see `spikes.md` SPIKE-2) |

## Level shifters & adapters

| Item | Qty | Role | Status | Notes |
|---|---|---|---|---|
| BSS138 4-ch bidir level converter (or PCA9306) | 1 | **I²C3 1.8↔3.3 V** — open-drain (SparkFun BOB-12009 / Adafruit 757) | 🛒 | **required**; NOT a TXB for I²C |
| TXB0108 (8-ch, push-pull) | 1 | **nRF SPI 6 lines 1.8↔3.3 V** | 🛒 | V_CCA 1.8 V / V_CCB 3.3 V, OE→V_CCA |
| micro:bit edge-connector breakout | 1 | reach micro:bit I²C on edge P19/P20 | 🛒 | Kitronik 5601B / SparkFun BOB-11349 |

## Sensors & display

| Item | Qty | Role / objective | Status | Notes |
|---|---|---|---|---|
| I²C sensor breakouts (distance/color/light etc.) | few | I²C sensors (obj 1) | ✅/🛒 | 3.3 V → via the I²C shifter |
| SSD1306 OLED (I²C) | 1 | status display, MSP430-driven (obj 12,13) | ✅ | on MSP430's own I²C (off-carrier) |
| Dev-kit MIPI/LVDS display (SoM kit) | 1 | status display via FPC (obj 12) | ✅ | on the FPC connectors |

## USB, power, networking

| Item | Qty | Role | Status | Notes |
|---|---|---|---|---|
| Powered USB hub | 1 | SoM **USB-A host (J3)** → the MCU dev boards | 🛒 | see `DEV-USB-HOST-PROGRAMMER.md` |
| ASIX USB-GbE dongle | 1 | quick bench LAN / obj | ✅ | |
| USB-C cable (data) | 1 | SoM gadget (J5) ↔ RPi/host — net+console+SDP | ✅/🛒 | the RPi's only per-bench link |
| USB cables (micro-USB / USB-C / USB-A) | per board | flash+console for each MCU board | 🛒 | one per dev board |

## Debug / programming

| Item | Qty | Role / objective | Status | Notes |
|---|---|---|---|---|
| JTAG/SWD probe, **1.8 V / adaptive-Vref** | 1 | **M7 debug** on P7 (obj 10) | 🛒 | J-Link (EDU/BASE) or level-shifted CMSIS-DAP |
| 2×17 0.1″ ribbon/IDC + jumpers for P20/P21 | 1 set | tap the expansion headers | 🛒 | or F-F jumper leads |

## Wiring & passives

| Item | Qty | Role | Status |
|---|---|---|---|
| Breadboard(s) + power rails | 1–2 | mount shifters/amp/sensors | 🛒 |
| Jumper wires (M-M / M-F / F-F) | packs | header ↔ breakout wiring | 🛒 |
| Pull-up resistors 2.2–4.7 kΩ | few | I²C pull-ups each side of the shifter | 🛒 |
| Bulk/decoupling caps | few | rails, amp VIN | 🛒 |

## Physical bench ("Big Bob Bench" — boards mounted on the back)

| Item | Qty | Role | Status |
|---|---|---|---|
| Mounting panel / back plate | 1 | mount carrier + dev boards on the back | 🛒 |
| Standoffs, M2.5/M3 screws, spacers | sets | board mounting | 🛒 |
| Cable management / labels | — | tidy the USB + signal harness | 🛒 |

## Shared / lab-level (V2 CI lab)

| Item | Qty | Role | Status | Phase |
|---|---|---|---|---|
| Raspberry Pi 4/5 (bench supervisor) | 1/lab | CI supervisor over the SoM's USB-C link | 🛒 | **V2** |
| RGMII PHY breakout + magnetics/RJ45 | 1 | **M7 ENET→PC** (obj 8) on P20.15–.30 | 🛒 | **V1b** — needs 12-line shift |
| WM8731 U10 rework tooling (hot-air) | — | free SAI3-RX for the analog mic array | 🛒 | **V2** — SPIKE-2 prereq |
