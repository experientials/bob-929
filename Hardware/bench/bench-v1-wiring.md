# bench-V1 — full pin connection plan (external lines & modules)

**Derivation of the CANONICAL objectives** in [`bench-v1.md`](bench-v1.md) (top block). That block is
source of truth; if this disagrees, it wins. Pin facts verified against
[`boards/sb-ucm-carrier.yaml`](../../../ziloo/Hardware/pinmux/boards/sb-ucm-carrier.yaml). Every objective's every external line is
assigned to a named carrier pin below; the master occupancy table guarantees no double-book.

## Decisions baked in (confirm — each changes wiring)

- **D1 — two distinct nRF roles.** *Product BLE radio* = nRF52840 **NCP on ECSPI2/P21** (SPI, per R1).
  *BBC micro:bit* = a generic **I²C** MCU peer on I²C3 (nRF-based, but incidental). They are NOT the
  same device. → keeps ECSPI2 on P21 AND micro:bit on I²C3.
- **D2 (revised 2026-09-20) — nRF on ECSPI2 = a 3.3 V USB-bootloader dev board + one TXB0108 SPI
  shifter.** Use a **Seeed XIAO nRF52840** or **Adafruit Feather nRF52840** (breadboard-friendly, flash
  over USB), shifted 6 lines 1.8↔3.3 V on ECSPI2. *A bare 1.8 V module would skip the shifter but is
  the wrong tool for a bench (castellated SMD → adapter PCB + **SWD-only** flashing); the nRF-at-1.8 V
  power/RF validation belongs on the **product faceboard (BLE_MOD)**, not this eval carrier.* The
  **dongle stays on USB → objective 3.**
- **D3 — M7-ENET (obj 8) is V1b**, pin-mapped & reserved now but wired later: needs an external RGMII
  PHY breakout + a 12-line 1.8↔3.3 V shift on P20.15–.30, and depends on M7 (Track M).
- **D4 — MCU peers are I²C slaves on ONE bus** (I²C3) behind ONE 1.8↔3.3 V shifter; distinct addresses
  (map below).
- **D5 — OLED is MSP430-driven, off-carrier** (per objective "OLED module controlled by MSP430") — it
  hangs on MSP430 #1's own I²C, consuming no carrier pins.
- **D6 — MSP430 runs at 1.8 V** (FR2476 supports it) → sits on the LV side of the I²C shifter and needs
  NO UART shifter for the M7 BSL link. MCUs (Pico/Pico4ML/micro:bit) run 3.3 V on the HV side.

## Power & ground distribution (wire once, to the breadboard rails)

| Rail | Carrier source | Feeds |
|---|---|---|
| **3V3** | **P20.7** (or P10.1) | HV side of I²C shifter, MAX98357A VIN, MCUs, 3.3 V sensors |
| **5V** | **P20.6** | (optional MAX98357A VIN for more output) |
| **1V8** | **P10.2** | LV ref of I²C shifter, MSP430 VCC, nRF module VDD |
| **GND** | **P20.31, P20.32, P21.6, P21.9, P10.10, P7.4, P7.6** | common ground — tie ALL modules |

## Buses & fixed interfaces

| Bus | Carrier pins | Level | Objective |
|---|---|---|---|
| **I²C3** (sensor+MCU+supervisor) | SCL **P20.33**, SDA **P20.34** | 1.8 V (LV) | 1,2,5,6,13 |
| **ECSPI2** (nRF BLE NCP) | SCLK **P21.26**, MOSI **P21.28**, MISO **P21.22**, CS **P21.24** | 1.8 V | 2 |
| **SAI3-TX** (speaker) | DIN **P21.11**, BCLK **P21.13**, LRC **P21.21** | 3.3 V | 5 |
| **UART4** (M7→MSP430 BSL) | TXD **P20.8**, RXD **P20.10** | 1.8 V | 7 |
| **UART1** (A53→MSP430, optional) | TXD **P20.9**, RXD **P20.11** | 1.8 V | 7 (alt) |
| **ENET/RGMII** (M7→PC, V1b) | see ENET block below (**P20.15–.30**) | 1.8 V | 8 |
| **JTAG** (M7 debug/FW) | TMS **P7.1**, TCK **P7.3**, TDO **P7.5**, TDI **P7.7**, VREF **P7.2**, MOD **P7.8**, GND **P7.4/.6** | 1.8 V | 10 |
| **MIPI/LVDS** | FPC (P11/P22/P49/P45) | — | 12 |

## Control / handshake GPIO ledger (all non-ENET-block → config-independent)

| Signal | Carrier pin | Pad/func | Dir | Objective |
|---|---|---|---|---|
| MSP430 → SoM **wake** | **P10.5** | PMIC_ON_REQ | in | 9 |
| SoM → MSP430 **"M7 active/suspended"** (I²C-master handoff) | **P20.12** | GPIO1_IO00 (SOUND_INT) | out | 6 |
| MSP430 → SoM **INT** (I/O-expander) | **P20.14** | GPIO1_IO01 (STEM_INT) | in | 13 |
| MSP430 **BSL RST** | **P20.13** | GPIO2_IO10 (SD1_RESET_B) | out | 7 |
| MSP430 **BSL TEST** | **P20.5** | GPIO (PWM1_OUT) | out | 7 |
| nRF **IRQ** | **P21.32** | GPIO4_IO20 (PCIE_WAKE_B) | in | 2 |
| nRF **RESET** | **P21.16** | GPIO2_IO19 (SD2_nRST) | out | 2 |
| PMIC standby (waking levels) | **P10.3** | PMIC_STBY_REQ | out | 14 |
| POR_B / global reset | **P10.7 / P10.9** | POR_B / SYS_RST_PMIC | out | 10,14 |

*(P20.13 repurposes SD1_RESET_B and P21.16/P21.32 repurpose SD2/M.2 pins — all free on the bench
because we boot eMMC and fit no SD1/SD2/M.2. If the NCP transport needs a req/rdy PAIR instead of a
single IRQ, the second line takes P20.12→ move M7-active to another spare and add the rdy on a freed
pin.)*

## Per-module wiring

### I²C level shifter (1.8 V ↔ 3.3 V, bidirectional — PCA9306/TXS0102)
- LV: **P10.2** (1V8), SCL **P20.33**, SDA **P20.34**, GND
- HV: **P20.7** (3V3), SCL/SDA → the 3.3 V I²C segment (all MCUs + 3.3 V sensors), GND

### MSP430 LaunchPad #1 (supervisor — I/O-expander, I²C-master-when-M7-down, MSP430-prog target)
- VCC **1V8 (P10.2)**, GND
- I²C (eUSCI B) → **LV side** (SCL P20.33 / SDA P20.34) directly (1.8 V)
- BSL UART → **UART4** (RXD←P20.8, TXD→P20.10); **RST←P20.13**, **TEST←P20.5**
- "M7 active" sense ← **P20.12**; INT to SoM → **P20.14**
- OLED (SSD1306) hangs on MSP430 #1's *second* I²C (off-carrier) — objective 12/13
### MSP430 LaunchPad #2 (second supervisor/peer)
- VCC 1V8, GND, I²C → LV side (distinct address); optional its own INT on a spare if needed

### Pico H (RP2040) — I²C MCU peer (slave)
- VSYS/3V3 ← **3V3 (P20.7)**, GND; I²C (I2C0/1 on chosen GP pins) → **HV side** of shifter
### Arducam Pico4ML (RP2040 + cam/mic) — I²C MCU peer (slave)
- 3V3, GND; I²C → **HV side**. (Onboard camera/mic used for on-Pico TinyML; NOT exposed to SoM — the
  SoM camera path is V2.)
### BBC micro:bit **V1.3 (nRF51822)** — I²C MCU peer (slave)
- **Confirmed 2026-09-20** via `/Volumes/MICROBIT/DETAILS.TXT` (board id **9900** = V1.3; HIC 97969901
  = KL26). Chip = nRF51822 (Cortex-M0, 16 KB RAM, BLE 4.1) — **NOT** a V2/nRF52833.
- Via **edge-connector breakout**: SCL **edge P19**, SDA **edge P20**, **3V**, **GND** → **HV side**
- **Caveat:** nRF51 I²C-**slave** mode is limited/errata-prone (no true TWIS like nRF52) — OK as a bus
  participant, but the Picos/an nRF52 are the robust slave choice. On V1 the edge I²C **shares the
  onboard LSM303** (≈0x19/0x1E) — keep those addresses clear when bridged onto I²C3.

### nRF52840 board (BLE NCP) — ECSPI2 via TXB0108 shifter (XIAO/Feather, 3.3 V)
- Board powered/flashed over **USB** (3.3 V logic); **all 6 lines through the TXB0108** (SoM 1.8 V ↔
  board 3.3 V): SoM **SCLK P21.26 / MOSI P21.28 / MISO P21.22 / CS P21.24 / IRQ P21.32 / RESET P21.16**
  ↔ the nRF board's chosen GPIO. nRESET = nRF **P0.18**; SPI/IRQ nRF pins = firmware-assigned (PSEL).
- Shifter V_CCA = 1.8 V (P10.2), V_CCB = 3.3 V, OE→V_CCA. *(Bare 1.8 V module rejected — see D2.)*

### MAX98357A (speaker amp) — SAI3-TX
- VIN **3V3 (P20.7)** (or 5V P20.6), GND **P21.6/.9**
- DIN←**P21.11**, BCLK←**P21.13**, LRC←**P21.21**; SD_MODE/GAIN strapped per datasheet; speaker on out
- (No MCLK. Real product speaker path per the all-audio-on-SAI3 C6 decision.)

### JTAG probe (M7 debug/monitor/FW-update) — P7
- 1.8 V/adaptive-Vref probe to P7.1/.2/.3/.4/.5/.6/.7/.8 as in the bus table

### ENET RGMII PHY breakout (M7→PC, **V1b** — reserved) — P20.15–.30
| RGMII | Pin | RGMII | Pin |
|---|---|---|---|
| MDC | P20.15 | TXC | P20.30 |
| MDIO | P20.17 | RXC | P20.29 |
| PHY_nRST | P20.16 | TX_CTL | P20.20 |
| PHY_INT | P20.18 | RX_CTL | P20.19 |
| TD0..3 | P20.22/.24/.26/.28 | RD0..3 | P20.21/.23/.25/.27 |
Needs a PHY breakout + magnetics/RJ45 to the PC and a 12-line 1.8↔3.3 V shift; M7 runs lwIP. Deferred.

### USB — physical connection topology (dev boards program via the SoM host, NOT the RPi)

**Architecture decision (2026-09-21):** the SoM hosts + flashes the MCU dev boards over its **own USB
host**, so the RPi supervisor manages only the SoM's one USB-C link per bench (not ~6 boards → ~30
endpoints/lab). Planning lives in `ziloo-firmware/docs/DEV-USB-HOST-PROGRAMMER.md`.

```
                          ┌─────────── carrier / UCM SoM ───────────┐
 RPi supervisor  ◀──USB-C (J5, usb0)──┤ gadget: CDC-ECM net + CDC-ACM console + SDP   │
 (V2 CI lab)                          │                                              │
                                      │ USB-A host (J3) ──▶ powered USB hub ──┬── Pico H (RP2040)   UF2/picotool
                                      │                                       ├── micro:bit V1.3     DAPLink MSC / pyocd
                                      │                                       ├── nRF board (XIAO)   nrfutil / pyocd
                                      │                                       └── MSP430 LaunchPad   mspdebug (eZ-FET)
 (break-glass) ◀── CP2104 micro-USB ──┤ UART2 console only                            │
                                      └──────────────────────────────────────────────┘
 12 V barrel jack ─▶ board power
```

- **Each MCU board has TWO connections:** USB → SoM host (**flash + console**) **and** its signal lines
  → carrier headers (**the product-bus test**: Pico/micro:bit → I²C3, nRF → ECSPI2, MSP430 → UART4/I²C3).
- **J3 (USB-A host):** powered hub → the MCU dev boards (+ BT/nRF dongle, USB-GbE for obj 3).
- **J5 (USB-C gadget):** `usb0` CDC-ECM net + CDC-ACM console + SDP recovery; `thepia hwd` (obj 4,11).
  The RPi's only per-bench link.
- **12 V barrel jack:** board power.

**Production note (do NOT lose):** in the shipped toy **only the USB-C gadget port is exposed.** The USB
**host is not exposed** — if it exists at all it's **internal board-to-board wiring that doesn't present
as USB**, not a USB-A jack. The dev USB-host programming is a **bench/CI capability, inert in production**
(kernel+tools present, no external port → no CRA/PSTI USB attack surface). See the firmware planning doc.

## I²C3 address map (assign in firmware — no collisions)

| Device | 7-bit addr | Notes |
|---|---|---|
| MSP430 #1 (I/O-expander/supervisor) | 0x40 | slave when M7 master; becomes master when M7 down |
| MSP430 #2 | 0x41 | |
| Pico H | 0x42 | RP2040 I²C-slave fw |
| Pico4ML | 0x43 | RP2040 I²C-slave fw |
| micro:bit V1.3 | 0x44 | nRF51 TWI-slave (limited); avoid its LSM303 0x19/0x1E |
| sensor breakouts | per-part | keep clear of 0x40–0x44 and reserved 0x00–0x07/0x78–0x7F |

*(Addresses are a proposed starting map — set each MCU's slave address in its firmware to match.)*

## Master carrier-pin occupancy (used pins only — the anti-double-book ledger)

**P20:** .5 BSL-TEST · .6 5V · .7 3V3 · .8 UART4-TX · .9 UART1-TX* · .10 UART4-RX · .11 UART1-RX* ·
.12 M7-active→MSP430 · .13 BSL-RST · .14 MSP430-INT · **.15–.30 ENET RGMII (V1b, reserved)** ·
.31/.32 GND · .33 I²C3-SCL · .34 I²C3-SDA. *(.9/.11 optional alt prog path.)*
**P21:** .6/.9 GND · .11 spk-DIN · .13 spk-BCLK · .16 nRF-RESET · .21 spk-LRC · .22 nRF-MISO ·
.24 nRF-CS · .26 nRF-SCLK · .28 nRF-MOSI · .32 nRF-IRQ. **Off-limits: .5/.7 SYS_I2C, .17/.19/.23 SAI3-RX.**
**P10:** .1 3V3 · .2 1V8 · .3 STBY_REQ · .5 ON_REQ(wake) · .7 POR_B · .9 SYS_RST · .10 GND.
**P7:** .1/.2/.3/.4/.5/.6/.7/.8 JTAG. **FPC:** MIPI/LVDS. **J3:** USB dongles. **J5:** USB-C. **Jack:** 12 V.

## Level shifters — required parts, topology, and the traps

The bench has a **1.8 V SoM domain** and a **3.3 V peripheral domain**. Shifters bridge them. The part
class depends on the signal type — **open-drain (I²C) vs push-pull (SPI/UART/GPIO)** — and mixing them
up is the classic failure.

| # | Domain crossing | Signal type | Shifter needed? | Part class |
|---|---|---|---|---|
| 1 | **I²C3 1.8↔3.3 V** (Pico H, Pico4ML, micro:bit, 3.3 V sensors) | open-drain, bidir | **REQUIRED** | I²C translator |
| 2 | **MSP430 UART/I²C** | — | **No** — MSP430 @ **1.8 V** (D6), sits on LV side directly | — |
| 3 | **nRF on ECSPI2 (SPI+IRQ+RST)** | push-pull | **REQUIRED** — bench nRF is a 3.3 V board (D2) | push-pull translator |
| 4 | **SAI3 speaker** (MAX98357A) | push-pull | **No** — header already 3.3 V, amp @ 3V3 | — |
| 5 | **ENET RGMII (obj 8, V1b)** | push-pull | Deferred — 12-line | push-pull / 1.8 V-RGMII PHY |
| 6 | **JTAG (P7)** | — | **No** — adaptive-Vref probe | — |

### #1 I²C shifter — the one you must buy (open-drain!)
- **Use a bidirectional I²C-capable translator:** **PCA9306** breakout (cleanest — SparkFun BOB-11955 /
  Adafruit) **or** a **BSS138 4-channel** "logic level converter" (SparkFun BOB-12009 / Adafruit #757 —
  cheap, gives 2 spare channels for slow GPIO). 2 channels = SDA+SCL.
- **TRAP: do NOT use a TXB-series board (TXB0104/0108) for I²C** — they are *push-pull* and fight I²C's
  open-drain pull-downs; the bus won't work. (TXS0102/0108 *is* I²C-capable but its internal pull-ups
  can clash with strong bus pull-ups — PCA9306 is less fussy.)
- **Topology:** LV ref = **1.8 V (P10.2)**, HV ref = **3.3 V (P20.7)**; I²C3 SCL/SDA (**P20.33/.34**) on
  LV; all 3.3 V peers on HV; **pull-ups to each side's own rail** (BSS138 boards include them; with a
  PCA9306 add ~2.2–4.7 kΩ per side).

### #3 nRF SPI shifter — REQUIRED (bench nRF is a 3.3 V board, D2)
- Bench nRF on ECSPI2 = a **3.3 V dev board (XIAO / Feather nRF52840)** → **shift 6 lines** 1.8↔3.3 V:
  SCLK/MOSI/CS/RESET (host→nRF) + MISO/IRQ (nRF→host). **Push-pull → TXB0108 (8-ch; V_CCA to 1.2 V, so
  1.8 V-capable), or a directional SN74LVC** for robustness at higher SPI clocks (SPI directions fixed).
- Wire: V_CCA = **1.8 V (P10.2)** (SoM side), V_CCB = **3.3 V** (nRF board side), OE→V_CCA.
- *(A bare 1.8 V module would need no shifter but is rejected for the bench — see D2; the 1.8 V path is
  a product-faceboard concern. The dongle stays on USB → objective 3.)*

### #5 ENET RGMII (V1b, deferred)
- 12-line 1.8↔3.3 V push-pull shift to a 3.3 V RGMII PHY breakout, **or** pick a PHY that accepts 1.8 V
  RGMII. Design when M7-ENET is wired.

### Bench shopping list (V1a)
- **1× BSS138 4-ch level converter** (or **PCA9306** breakout) — the required I²C shifter. *(Consider a
  2nd for spare GPIO headroom.)*
- **micro:bit edge-connector breakout** — to reach the micro:bit's I²C on edge P19/P20.
- **1× Seeed XIAO nRF52840** (or Adafruit Feather nRF52840) — the ECSPI2 BLE NCP (3.3 V, USB-flash).
- **1× TXB0108** (push-pull, 8-ch) — the 6-line nRF SPI shifter (D2). *(Not for I²C.)*
- Assorted 2.2–4.7 kΩ pull-ups; a powered USB hub (many peers time-share USB — see notes).
