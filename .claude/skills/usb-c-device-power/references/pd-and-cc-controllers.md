# CC Termination & PD Controllers

Single-port-first. How the CC pins work, when you need a PD controller vs. when you don't, and
part-by-part options with lifecycle status. Read this when deciding *how a port negotiates*.

## CC pins in one screen

Every USB-C port signals its role through the two CC pins:

- **Source** presents a pull-**up** (**Rp**) on CC. The Rp value *advertises* how much 5 V
  current it offers: 56 kΩ→Default USB (~500–900 mA), 22 kΩ→1.5 A, 10 kΩ→3.0 A.
- **Sink** presents a pull-**down** (**Rd = 5.1 kΩ**) on CC.
- **Orientation:** only one CC line connects through the cable. Whichever CC pin sees the valid
  Rp/Rd pairing tells you which way the plug went in; the other CC pin becomes **VCONN** (powers
  e-marked cables / active cables).
- **DRP** (dual-role) toggles Rp/Rd to attach either way.
- **Data role (host/DFP vs device/UFP) is independent of power role.** A device can sink power
  while being a USB host, etc. PD can swap either role after attach.

Passive Rp/Rd get you **5 V only**. Anything above 5 V (9/12/15/20 V, PPS) is USB-PD and needs
BMC communication on CC — i.e. a PD-capable IC.

### Exact termination values (copyable — put these on the schematic)

**Sink — one Rd per CC pin, never shared:**

```
CC1 ──[5.1 kΩ ±20%]── GND
CC2 ──[5.1 kΩ ±20%]── GND
```

Two independent resistors. **This is the single most-copied USB-C mistake** — the Raspberry Pi 4
tied both CC pins to *one* shared 5.1 kΩ. With an **e-marked cable** (which puts Ra ≈ 1 kΩ on its
CC line for the e-marker), the shared node becomes 5.1 k ∥ 1 k ≈ **836 Ω**, which lands in the Ra
detection window — so a spec-correct source reads the device as an **audio accessory and applies
0 V to VBUS**. Dumb chargers "worked," compliant ones didn't. One 5.1 kΩ per pin avoids it.

**Source — one Rp per CC pin; the value advertises the 5 V current:**

| Advertised @ 5 V | Rp to 5 V (VBUS) | Rp to 3.3 V | Current-source alt |
|---|---|---|---|
| Default USB (500/900 mA) | 56 kΩ ±20% | 36 kΩ ±20% | 80 µA |
| 1.5 A | 22 kΩ ±5% | 12 kΩ ±5% | 180 µA |
| 3.0 A | 10 kΩ ±5% | 4.7 kΩ ±5% | 330 µA |

(±5% on the 1.5/3 A rows because the detection thresholds sit closer together. Verify against the
USB Type-C spec Table 4-26 / your controller datasheet before silk.)

- **VCONN** (nominal 5 V, range 3.0–5.5 V) is driven onto the *non-oriented* CC pin only when an
  e-marked / 5 A / active cable needs to power its e-marker. A simple ≤3 A passive-cable source can
  skip it.
- **Dead-battery:** the 5.1 kΩ Rd must exist *passively* (discrete resistors, or a controller whose
  Rd defaults connected when unpowered) so a flat device still advertises "sink present" and can
  start charging. This is a big reason to keep discrete Rd even when a PD chip is fitted.
- **SBU1/SBU2 unused → leave floating / no-connect** (they carry only the DP AUX/sideband in Alt
  Mode). Optionally add ESD if exposed.

### USB2 data & orientation — the free trick for a sink

A **USB 2.0-only UFP sink needs no orientation mux for data.** In the receptacle D+ appears on both
A6 and B6, D− on both A7 and B7; in any plug flip only one of each pair is actually connected
through the cable. So **tie A6+B6 together (D+) and A7+B7 together (D−)** and run one pair to the
USB2 PHY — the unconnected contact is a harmless short stub at 480 Mbps. Zero orientation logic.

A **source/host** should not blindly tie them: if it also carries USB3 or DP those high-speed lanes
can't be stubbed and need a **2:1 orientation mux/redriver** (TS3USB221 / TUSB1046) steered by the
CC orientation result. USB2-only source can still use the tie trick but most designs mux anyway for
clean SI. (Sources: Benson Leung "How to design a proper USB-C power sink"; USB Type-C spec R2.0;
Microchip AN1914.)

## Tier 0 — Resistors only (+ optional CC PHY), no PD

The cheapest port. Covers "5 V is enough" for both directions.

**Sink (charge/receive):** an Rd (5.1 kΩ) on each CC to GND. Your power-path charger takes VBUS.
Done. If you want the MCU to *know* about attach/detach/orientation and current advertisement,
either read the CC voltages with MCU ADC/comparators, or add a **CC logic/PHY**:

- **Onsemi FUSB302** (~$0.60) — a Type-C CC controller / BMC PHY. It does **not** negotiate PD by
  itself; it exposes CC events and the raw BMC channel to an MCU running a USB-PD stack (TCPM —
  e.g. the Chromium EC stack, Zephyr's USB-C stack, or a vendor TCPM). Cheapest silicon, **most
  firmware**. Only worth it if you already have a capable MCU *and* actually want PD in firmware.
  For a plain 5 V port an FUSB302 is overkill — resistors + MCU GPIO are enough.

**Source (provide 5 V):** Rp on both CC (value = the current you advertise), a 5 V rail, and a
**USB2 orientation mux** so D+/D− route to whichever side the cable used. A small comparator or
the MCU reads which CC has the Rd (the sink) and steers the mux + enables VBUS. The
**TS5USBC410** (dual 2:1 USB2 mux, already in the bob-929 BOM) or a TS3USB221 does the muxing.
Add reverse-current and OVP on the sourced VBUS.

This Tier-0 source is a legitimate, controller-free way to power a peripheral or phone at 5 V and
act as its USB host — an MSP430 reading CC comparators is entirely sufficient supervision.

**Prefer a Type-C port controller (no PD) over discrete comparators when the OS should see the
port.** The **TI HD3SS3220** (in `Hardware/292/datasheets/USB Mux hd3ss3220.pdf`) is a **Type-C
DRP port controller with an integrated SuperSpeed 2:1 mux** — no PD engine. It does the CC logic
for you: **current advertisement + detection, attach detection, cable-orientation detection, role
detection (DFP/UFP/DRP), VBUS detection, 5 V VCONN sourcing, Try.SRC/Try.SNK**, configured over
**GPIO or I2C**. It reports attach/orientation/role to the SoC or MCU, and it's supported by the
mainline `hd3ss3220.c` driver — so on Android you get clean Type-C events (and the SuperSpeed mux
for orientation) **without** a PD stack. This is the ideal Tier-0 companion when 5 V is enough but
you want the port to be first-class to the OS, sitting between the resistor approach and a full
PD controller.

## Tier 1 — Autonomous PD sink (need >5 V in, no firmware)

When the device must pull **more than 15 W or a voltage above 5 V** but you don't want a PD stack:

- **STMicro STUSB4500** (~$1.5–2) — stand-alone USB-PD **sink** controller. You program up to
  three sink PDOs into its NVM; on attach it negotiates the best available contract (up to 100 W,
  20 V/5 A) **with no MCU**. Handles dead-battery. The default "give me high-power input with zero
  firmware" part. **From the datasheet:** dual supply — it runs from **VSYS (3.0–5.5 V)** and/or
  **VDD (4.1–22 V, from VBUS)**, so it powers itself even from a dead battery. **Integrated PMOS
  gate drivers** switch the sink path through an **external PMOS** enabled by **VBUS_EN_SNK**;
  internal and/or external **VBUS discharge** (DISCH pin); an **A_B_SIDE** pin reports orientation;
  POWER_OK/ALERT status outputs. **I2C is optional** (address 0x28 default, strappable 0x28–0x2B,
  ≤400 kHz) for runtime PDO reconfig — it runs fine fully strapped.
- **Cheap fixed-voltage PD "triggers"** — **HUSB238** (I2C/resistor-select, Adafruit breakout),
  **Injoinic IP2721**, **WCH CH224K** (~$0.3–0.5). These request one fixed PD voltage. Great for
  "I just need a clean 12 V or 20 V in" with essentially no BOM. Less flexible than STUSB4500 but
  a fraction of the cost.
- **Charger with PD-sink built in** — some chargers detect high-voltage sources themselves:
  BQ2589x do D+/D− (BC1.2/Apple/QC) detection; pairing a charger with an STUSB4500 lets the
  charger's input-current-limit track the negotiated contract. See `chargers-and-cells.md`.

## Tier 2 — Full single-port PD controller

When a port must **negotiate as a source**, present multiple PDOs, do PPS, or drive Alt Mode.
This is the tier to use when you genuinely need a "smart" port — one chip per port.

- **TI TPS25750** — single-port Type-C + PD with **integrated power switches**, no external FETs.
  Configured over I2C or from an on-board EEPROM ("dead-battery"/host-less boot). Bi-directional
  path: source up to ~60 W, sink up to 100 W. **No Alt Mode** — TI positions it exactly for "you
  don't need DisplayPort." Much less firmware than FUSB302 because the PD engine is on-chip. The
  single-port workhorse when you need negotiated power but not video.
- **TI TPS65987D** — single-port full controller **with Alt Mode** mux control and HS routing.
  Needs external power FETs. Use for one smart port that must do DisplayPort.
- **Infineon EZ-PD CCG6SF** — single-port controller, DRP, PD 3.x, **integrated VBUS provider/consumer
  FETs**, DP Alt Mode capable. The single-port sibling of the CCG6DF. Actively promoted (good
  longevity). **32-bit 48-MHz Arm Cortex-M0, 64-KB flash + 96-KB ROM, and a complete integrated
  Type-C transceiver including the Rp, Rd, and dead-battery Rd terminations** — so it needs very few
  external CC parts. Configured with Infineon's EZ-PD Configuration Utility. (Part example:
  CYPD6227-96BZXI.) **From the datasheet:** integrated **provider VBUS load switch (5 V/3 A,
  slew-controlled, 24 V tolerant)** with hardware OVP/UVP/OCP/short/reverse-current protection;
  **integrated VCONN FETs** (with OCP) for EMCA cables; **integrated high-voltage short-to-VBUS
  protection on CC and a pass-through SBU switch (20 V)** — so it can replace a separate TPD6S300A
  on that port; and a **high-voltage LDO good to 21.5 V** for dead-battery operation. Note the
  *sink* (consumer) path uses an **external N-FET** the controller drives, while the *source*
  (provider) switch is on-chip. VSYS 2.75–5.5 V; 4× reconfigurable SCBs (I2C/SPI/UART), hot-swap I2C.
- **Infineon CCG3 / CCG3PA** — older, cheaper single-port; CCG3PA is common in chargers/power
  banks (source/sink), CCG3 supports DP Alt Mode. Fine if you want low cost and don't need the
  newest compliance.

## Tier 3 — Dual-port controllers (avoid unless truly justified)

Documented for completeness. **Prefer two single-port designs.** Reach here only if two ports
must be co-managed by one PD engine (shared power budget arbitration, shared Alt Mode mux, board
area). Note the market is thin:

- ~~**TI TPS65988**~~ — dual-port, integrated switches, Alt Mode, HS mux. **NRND — the entire
  TPS65988x family (DH/DJ/DK) is Not Recommended for New Design; TI has no active dual-port
  successor.** It won't be hard-EOL'd immediately and still ships, but gets no new features/PD
  compliance and limited support. Do not design it into anything new.
- **Infineon EZ-PD CCG6DF** (CYPD6228-96BZXI) — the live dual-port + single-port controller with
  DP Alt Mode, integrated VBUS FETs, PD 3.x. This is the migration target *if* you must stay
  dual-port with Alt Mode.
- **Infineon EZ-PD CCG7D** (CYPD729x) — dual-port + integrated buck-boost DC-DC, wide input
  (4–24 V, 40 V tolerant), automotive-grade. Heavier than most device-side needs but the most
  capable active dual-port part.

## Data & Alt Mode muxing

- **USB2 only:** a 2:1 orientation mux is all you need to handle plug flip. The **TI TS5USBC410**
  (bob-929 BOM; datasheet local) is a **dual 2:1 USB 2.0 mux/demux** with **9 Ω max Ron**, and —
  usefully for a USB-C port — it's **20 V/24 V short-to-VBUS tolerant** with powered-off protection
  (VCC = 0), so it doubles as fault protection on D±. Two select pins (**SEL1/SEL2**) + **OE**,
  driven by a CC comparator or MCU GPIO. Cheap, no controller required. (TS3USB221 is a simpler
  single 2:1 alternative.)
- **USB3 / SuperSpeed:** you need a SuperSpeed 2:1 crosspoint mux/redriver (TUSB546, TUSB1046,
  PI3DBS16) steered by the orientation output. USB3 signal integrity is real work — length-match,
  keep the pairs together, mind AC-coupling caps.
- **DisplayPort Alt Mode:** requires (a) a PD controller that runs the DP VDM handshake
  (Discover Identity → Discover SVIDs → Enter Mode → DP Status/Config), and (b) a **DP/USB3 HS
  mux/redriver** that the controller reconfigures between USB3 and DP lane maps. The **TI TUSB546-DCI**
  (bob-929 BOM; datasheet local) is exactly this: a **USB Type-C DP-Alt-Mode linear redriver
  crosspoint** — USB 3.1 up to 5 Gbps **and DisplayPort 1.4 up to 8.1 Gbps (HBR3)**, up to 14 dB
  EQ, transparent to DP link training, handles **FLIP/orientation, HPD, and AUX↔SBU** routing,
  single **3.3 V** supply, configured over **GPIO or I2C** (supports DP configs C/D/E/F). **An MCU
  running "simple logic" cannot substitute for the Alt Mode VDM engine** in the controller — this
  is the whole reason Alt Mode forces a Tier-2/3 controller; the TUSB546 is only the muxing muscle
  the controller drives. If Alt Mode is only "experimental," keep the controller **and** the TUSB546
  on a separate, populate-optional sub-circuit so they don't dictate the whole port architecture.

## Choosing, in one paragraph

Per port: if 5 V in/out is enough and no Alt Mode → **Tier 0** (resistors + MCU, optional
FUSB302). If you need >5 V *in* only → **Tier 1** (STUSB4500 or a fixed trigger). If the port
must negotiate as a source or do Alt Mode → **Tier 2** single-port controller (TPS25750 without
video, CCG6SF/TPS65987D with video). Only bond two ports into **Tier 3** when single-port
composition genuinely can't work — and if you do, it's Infineon CCGx, not TI.
