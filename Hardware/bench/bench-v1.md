# V1 bench — definition

The **unmodified SB-UCM carrier + attached dev/breakout boards**, over interfaces already exposed.
Goal: develop and validate the maximum product **software/firmware** that needs **zero board mods**,
before committing product hardware. **V2** (see `bench-v2.md`) adds hardware mods, camera, and the RPi
CI-lab supervisor.

Grounded in the pinmux model + on-hardware findings — see `challenges.md` (C2 SAI map, C7 ECSPI2),
`spikes.md` (SPIKE-1: P21 SAI3 is a 3.3 V codec bus), and `ucm-dev/references/*`.

## Objectives — CANONICAL (verbatim, as defined by Henrik — do NOT paraphrase, reorder, or drop)

> I need a V1 bench definition which is: **Without hardware mods what can we test by attaching
> breakout/dev boards to the carrier board in terms of future product functionality. What
> software/firmware can we develop on a V1 bench.** I expect it to cover something like
>
> - I2C sensors
> - I2C MCUs (2xMSP430, RP2050, nRF module)
> - USB bluetooth modules support
> - Integrated USB CDC support
> - Speaker output (ideally on real pins)
> - MSP430 mastering I2C sensor bus when M7 is shut down/suspended
> - UART programming of MSP430 from M7
> - M7 ENET coms with PC
> - MSP430 triggering SoM wakeup
> - M7 debugging, monitoring, firmware update
> - System config patching
> - System status display using MIPI/LVDS display bundled with SoM dev kit + OLED module controlled by MSP430
> - MSP430 working as an I/O expander
> - Waking levels of the overall system. Transitions
>
> (M7 bring-up: yes — held as its own thought; prerequisite/parallel track, see Track M.)
>
> **V2 bench (later):** hardware modifications enabling additional hardware testing — more breakout
> boards incl. camera modules; also when we set up a CI-lab with a RPi supervising.

*(RP2050 as written = **RP2040** — confirmed 2026-09-20: the on-hand board is a **Raspberry Pi Pico
H** (RP2040 + pre-soldered headers). There is no "RP2050"; the RP2040's successor is the RP2350.) The
concrete I²C-MCU-bus roster (Henrik, 2026-09-20): **2× MSP430 LaunchPad · Pico H (RP2040) · Arducam
Pico4ML (RP2040 + cam/mic — camera is a V2 topic) · BBC micro:bit **V1.3 (nRF51822)** (confirmed
2026-09-20, board id 9900; added as an I²C MCU peer — nRF51 slave mode is limited)**. The derived
capability/phase table and the pin-allocation plan below are DERIVATIONS of this list — this block is
the source of truth; if they disagree, this wins.*

## Phasing — M7 bring-up is a PARALLEL track, not a gate

The hardware-config spikes (attach breakouts, mux buses, wire audio) do **not** depend on the M7.
Run them (**V1a**) now, in parallel with M7 bring-up (**Track M**). M7 then *unlocks* the
ownership / supervisor / wake items (**V1b**). Do not sequence V1a behind M7.

## Interface allocation (no mods)

| Interface | Bench pins | Level | Used for |
|---|---|---|---|
| **I²C3** (`i2c-2`) | P20.33/.34 | **1.8 V** ✓ | shared sensor + MCU + OLED bus |
| **ECSPI2** | P21.22/.24/.26/.28 | 1.8 V | nRF module (SPI / BLE_MOD) |
| **UART1** (`ttymxc0`) | P20.9/.11 | 1.8 V, 5 M | MSP430 BSL (A53), general |
| **UART4** (`ttymxc3`) | P20.8/.10 | 1.8 V | M7 console + M7→MSP430 BSL |
| **audio (SAI3)** | P21.11–23 | **3.3 V** | WM8731 codec bus. **TX (speaker/amp) usable; RX (mic ADC) BLOCKED** by codec ADCDAT contention on P21.17 without U10 removal — see `spikes.md` SPIKE-1 V2b |
| **USB2 host** (J3) | — | — | BT dongle, nRF dongle, USB-GbE, RP2040-USB |
| **USB-C** (J5, usb0) | — | — | CDC-Ethernet gadget to PC (Linux net) |
| **eth0 / ENET pads** | P6 / P20 | 1.8 V | **RESERVED: M7↔PC diagnostic ethernet** — why SAI6/7 aren't available for sound |
| **JTAG** (P7) | — | 1.8 V | M7 debug (1.8 V / adaptive probe) |
| **MIPI-DSI / FPC** | P11/… | — | dev-kit status display |
| free GPIO on P20/P21 | — | 1.8 V | MSP430 wake line, IRQ/reset/handshakes |

## Audio on the carrier — SAI3/SAI5 on P21 only (SAI6/7 are EXCLUDED)

**Hard constraint: on V1 the ENET pads are committed to the M7↔PC diagnostic ethernet, and V1 has NO
SOUND/SUPERVISOR connector/module to alternatively route them to sound — so SAI6/SAI7 (only ALTs on
those pads) are NOT available.** That removes the one clean 1.8 V SAI. (The ENET-*or*-Sound XOR is a
product/faceboard feature: the SND_MOD-style **SOUND/SUPERVISOR connector** carries the ENET pads for
eth-*xor*-SAI7-speaker + SAI5 mic + the supervisor. That connector is a **V2** addition — see the
boundary below.) What remains for carrier audio is **SAI3 / SAI5_RX on P21.11–23 — a 3.3 V bus** (SAI2
and SAI1 are CAN-transceiver- / USB1-encumbered). So carrier audio is defined entirely by the two
WM8731 scenarios above:

**V1 audio uses the P21 SAI3 pins (the WM8731's pins), one of two ways** — both 3.3 V:

- **(A) Onboard sound (smoke test)** — use the WM8731 codec as-is (SAI3 → jack). Zero wiring; proves
  the audio software stack (ASoC → SAI → codec; later M7-owned SAI playback, Track M).
- **(B) Own breakout — the PRODUCT-relevant path, but only the TX/output half on unmodified V1.**
  Wire your own 3.3 V I²S/TDM parts to the SAI3 pins, per **`audio-architecture.md`**: a **MAX98357A**
  (speaker out) and/or a **TLV320ADC5140** (analog 5-mic TDM in). **The direction split is the hard
  rule (SPIKE-1 V2/V2b):**
  - **Speaker / TX path WORKS** — `SAI3_TXD` + `BCLK` + `LRCLK` are SoC *outputs*; the WM8731 only
    loads them as inputs (harmless). They drive out through the shifter at **3.3 V** (use a
    3.3 V-capable amp; MAX98357A @ 3V3 is fine).
  - **Mic / RX path is BLOCKED** — a mic ADC drives `SAI3_RXD` = **P21.17**, the same net the powered
    WM8731 **ADCDAT** actively holds (measured **0 V**, survives a full I²C power-down). Contention
    corrupts capture. Freeing it needs **U10 removed/isolated = a hardware mod (V2)**.

  So on **unmodified V1: audio OUTPUT is benchable, audio INPUT is not.** **SPIKE-2 (analog mic array)
  therefore requires the V2 U10 surgery — it is NOT benchable on an unmodified carrier.** ENET stays
  free either way.

**Still V2** (needs the SOUND/SUPERVISOR connector **or** U10 surgery): the **analog mic-array capture
(SPIKE-2)** on `SAI3_RXD`, the **1.8 V** product levels, the **SAI7 speaker option** (ENET pads), and
the **digital-MEMS 5-way array on SAI5**.

## Attached dev/breakout boards

2× MSP430 LaunchPad (supervisor role) · **Pico H (RP2040) · Arducam Pico4ML (RP2040+cam/mic) · BBC
micro:bit V1.3 (nRF51822)** — the I²C-MCU-bus peers (all **3.3 V** → shifter) · nRF52840 (dongle on USB2 +
DK/module on ECSPI2, product BLE NCP) · CSR BT dongle (USB2, present) · ASIX USB-GbE (USB2, present) ·
I²C sensor breakouts · SSD1306 OLED (I²C, verified) · MAX98357A I²S amp · dev-kit MIPI/LVDS display ·
**1.8↔3.3 V level-shifter breakouts** (for 3.3 V parts on the 1.8 V I²C3) · **micro:bit edge-connector
breakout** (to reach its I²C on edge pins P19/P20) · 1.8 V/adaptive JTAG probe (P7).

## Capabilities

| # | Capability | Interface + board | Software/firmware | Phase |
|---|---|---|---|---|
| 1 | I²C sensors | I²C3 + breakout | sensor drivers, sampling | **V1a** |
| 2 | I²C/SPI MCUs (2×MSP430, RP2040, nRF) | I²C3 + ECSPI2 | comms protocols, addressing | **V1a** |
| 3 | USB Bluetooth modules | USB2 + CSR/nRF dongle | BlueZ/HCI/BLE (CSR ✓) | **V1a** |
| 4 | Integrated USB CDC | usb0 + CDC-ACM | gadget config, CDC net/serial | **V1a** ✓ |
| 5 | MSP430 as I/O expander | I²C3 + MSP430 | MSP430 I²C-slave-GPIO fw + SoM driver | **V1a** |
| 6 | Status display (MIPI/LVDS + OLED) | FPC + I²C OLED | DRM/weston, OLED fb, MSP430-OLED fw | **V1a** (OLED ✓) |
| 7 | System config patching | `thepia hwd dt` | DT patch/revert loop | **V1a** ✓ |
| 8 | Speaker output (amp, e.g. MAX98357A) | **SAI3/P21 @3.3 V — TX pins .11(TXD)/.13(TXC)/.21(TXFS), GND .6/.9, VIN off-header 3V3** (no mod); SAI7/P20 is V2 | ASoC now; M7-SAI later | **V1a** |
| 9 | UART programming of MSP430 | UART1 (A53) → UART4 (M7) | MSP430 BSL protocol | **V1a→V1b** |
| M | **M7 bring-up + debug/monitor/FW-update** | P7 JTAG + UART4 + remoteproc | M7 build/debug/OTA | **Track M** |
| 10 | M7 ENET coms with PC | eth0 (RDC→M7) | M7 lwIP + ENET driver | **V1b** |
| 11 | MSP430 hands off I²C sensor bus when SoM boots | shared I²C + MSP430 | **sequential handoff** (MSP430 releases master on detecting SoM up — NOT multi-master) | **V1b** |
| 12 | MSP430 triggers SoM wakeup | GPIO/PMIC_ON_REQ + MSP430 | wake-source cfg, MSP430 fw | **V1b** |
| 13 | Waking levels & transitions | integration of 10–12 + PMIC/suspend | full power state-machine | **V1b (capstone)** |

## Total pin budget — every objective → exact pins (verified from `boards/sb-ucm-carrier.yaml`)

> **Full wiring plan (every module, every line, master occupancy ledger, address map):**
> [`bench-v1-wiring.md`](bench-v1-wiring.md). The table below is the summary; that doc is the buildable
> plan.

**Rails available** (wire these once): **3V3** = P20.7 / P10.1 · **5V** = P20.6 · **1V8** = P10.2 ·
**GND** = P20.31, P20.32, P21.6, P21.9, P10.10.

**Always-on infra** (not an "objective" but always wired): **A53 console** = CP2104 USB debug port
(UART2 also on P20.1 TXD / P20.3 RXD) · **usb0 CDC net + SDP recovery** = USB-C (J5) · **USB host for
dongles** = USB3-A (J3) · **power in** = 12 V barrel jack.

| Cap | Objective | Signal → pin | Level | Notes / conflicts |
|---|---|---|---|---|
| 1,5,6,11 | **I²C3 bus** (sensors, SSD1306 OLED, MSP430 I/O-expander + handoff) | SCL=**P20.33**, SDA=**P20.34** | 1.8 V | one shared bus — watch addr collisions; 3.3 V parts need a shifter; MSP430 handoff = sequential mastering |
| 2 | **ECSPI2** → nRF52840 (BLE) | MISO=**P21.22**, MOSI=**P21.28**, SCLK=**P21.26**, SS0=**P21.24** | 1.8 V | + nRF IRQ/RESET on free GPIO |
| 3 | USB Bluetooth | USB3-A **J3** | — | CSR/nRF dongle |
| 4 | USB CDC (Linux net) | USB-C **J5** (usb0) | — | ✓ working |
| 8 | **Speaker amp** (MAX98357A) on SAI3 **TX** | DIN=**P21.11**, BCLK=**P21.13**, LRC=**P21.21**; VIN=**P20.7**(3V3)/P20.6(5V); GND=**P21.6/.9** | **3.3 V** | no MCLK. **RX/mic P21.17 BLOCKED** by codec (SPIKE-1 V2b) |
| 9 | **MSP430 BSL** programming | UART1(A53) TXD=**P20.9**/RXD=**P20.11**; UART4(M7) TXD=**P20.8**/RXD=**P20.10** | 1.8 V | + MSP430 RST/TEST BSL-entry on free GPIO |
| 6 | Status display | MIPI-DSI/LVDS = **FPC (P11/P22/P49/P45)**; OLED = on I²C3 | mixed | |
| M | **M7 bring-up** (JTAG + console) | TMS=**P7.1**, TCK=**P7.3**, TDO=**P7.5**, TDI=**P7.7**, VREF=**P7.2**, MOD=**P7.8**, GND=**P7.4/.6**; console=UART4 **P20.8/.10** | 1.8 V | adaptive-Vtref probe |
| 10 | **M7 ENET-to-PC** (V1b) | ENET_* pads = **P20.15–.30** block | 1.8 V | **triple-booked**: SD1 (SDIO) *xor* M7-diag-ENET *xor* SAI5/6/7 audio — pick per test. Free here because speaker is on SAI3/P21, not SAI5/P20 |
| 12,13 | **Wake / power-state** (supervisor) | PMIC_ON_REQ=**P10.5**, PMIC_STBY_REQ=**P10.3**, POR_B=**P10.7**, SYS_RST_PMIC=**P10.9**; handshakes = SOUND_INT **P20.12**, STEM_INT **P20.14**, MCU_SYS_INT **P20.20**, SYS_PRG# **P20.30** | 1.8 V | + one free GPIO as MSP430 wake line |

**Off-limits on the headers:** **P21.17** (SAI3_RXD = codec ADCDAT, held), **P21.5/.7** (SYS_I2C =
RTC/EEPROM/codec system bus — don't add devices). **Free-GPIO pool is tight** — P20.5 (PWM1) + a few
spares; inventory before assigning nRF-CE/IRQ, MSP430 RST/TEST, OLED-INT, and the wake line.

**The four real contentions to plan around:** (1) the **P20.15–.30 ENET-pad block** is SD1 *xor*
M7-ENET *xor* SAI5-audio — one at a time; (2) **I²C3** is a single shared bus; (3) **SAI3 speaker is a
3.3 V island** in an otherwise 1.8 V bench; (4) **SAI3 RX is dead** (codec) so mic capture isn't in V1.

## Cross-cutting caveats

- **Level domains.** I²C3 = **1.8 V**; RP2040 + many sensors + nRF-DK default = **3.3 V** → use
  level-shifter breakouts, or run parts at 1.8 V (MSP430 can). Carrier I²C5/6 are **3.3 V-suspect**
  (behind the I2C shifter). Plan a 1.8 V domain and a shifted 3.3 V domain deliberately.
- **I²C sensor-bus handoff (#11) is sequential, not multi-master.** The MSP430 masters the sensor
  bus while the SoM is off/booting and **releases mastering when it detects the SoM is up**. So no
  bus arbiter/switch is needed — just a clean detect-and-release protocol on the MSP430 + a bus-idle
  handshake. (Simpler than the multi-master case.)
- **eth0 vs SAI7 vs M7-ENET.** The ENET pads are one resource: gigabit `eth0` **XOR** SAI7 audio
  **XOR** M7-diag-ethernet. Pick per test; Linux nets over usb0/USB-GbE when the ENET pads are used
  for audio or handed to the M7.
- **GPIO/pin budget.** MSP430 wake line, MCU IRQ/reset/handshakes, OLED INT need free P20/P21 GPIO —
  inventory against the free pins before wiring.

## V1 → V2 boundary (deferred)

- **Any mic capture on SAI3 (incl. analog mic-array = SPIKE-2)** — the RX line `SAI3_RXD` (P21.17) is
  actively held by the WM8731 ADCDAT; needs U10 removed/isolated (surgery). **Speaker/output on SAI3
  is fine on unmodified V1** — only capture is deferred.
- **5-mic digital I²S array on SAI5** (product mic bus) — needs a clean multi-lane SAI-RX = faceboard
  or a carrier hardware mod.
- **Camera modules** (MIPI-CSI on the FPC connectors).
- **RPi CI-lab supervisor** (HIL automation over `thepia hwd`).
- Any WM8731 ADCDAT-lift / SAI-repurpose hardware surgery.
