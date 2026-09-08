---
name: usb-c-device-power
description: >-
  Design the USB-C circuitry on the DEVICE side of a battery-powered product — a
  device that plugs into a charger, a PC, or a phone, runs off one or two LiPo/Li-ion
  cells, and can run while charging. Use this whenever choosing or reviewing USB-C
  port roles (sink/source/DRP), USB Power Delivery (PD) controllers, CC-pin
  termination, battery chargers with power-path, run-while-charging (NVDC) topology,
  1S vs 2S vs 2P cell choice, DisplayPort/USB Alt Mode muxing, VBUS/CC ESD protection,
  or picking chipsets and eval boards on a budget. Trigger it even when the user only
  says things like "which PD chip", "do we need a PD controller", "USB-C charging
  circuit", "power path", "run and charge at the same time", "TPS65988 / BQ25xxx /
  STUSB4500 / FUSB302 / CCGx", "Type-C sink", "OTG port", "charge a 2-cell pack over
  USB-C", or is reviewing a KiCad USB-C power schematic. This is a hardware design
  skill, not a firmware or software one.
---

# USB-C Device-Side Power & Data Design

You are designing (or reviewing) the USB-C front end of a **battery-powered device**. The
device connects to three kinds of partner:

- **A charger** — the device is a pure power **sink**, no data.
- **A PC** — the device is a **sink** for power and a USB **device (UFP)** for data.
- **A phone** — either the phone hosts the device (device = sink + UFP), or the device hosts
  the phone/peripheral (device = **source** + host/DFP, possibly with DisplayPort Alt Mode).

It runs off **one or two LiPo/Li-ion cells** and must be able to **run and charge at the same
time**. Your job is to pick a topology and a set of chips that satisfy those roles at the
lowest sane cost and risk.

This SKILL.md is the decision framework. It sends you into `references/` for the depth on any
one axis. **Read the reference file for whichever decision you're actually making** — don't
try to hold the whole design space in your head at once.

**Design each port as a single-port problem.** Even when the device has two connectors (e.g. a
sink/OTG port and a source/host port), treat them as two independent single-port designs rather
than reaching for one monolithic dual-port controller. It's cheaper, keeps each port's function
isolated, avoids the shared-firmware/shared-fault coupling of a dual-port chip, and sidesteps
the fact that the dual-port controllers are a thinning, partly-EOL market (see below). This
skill is written single-port-first; dual-port parts are noted where relevant but are not the
default. If you find yourself specifying a dual-port controller, stop and check whether two
single-port solutions (or one controller + one resistor port) are simpler.

**Separate the data plane from the management plane.** A USB-C port has two independent control
questions: *who moves the data* (D±/USB3 — the application SoC/SoM) and *who manages the port*
(CC sensing, charger, power-path, orientation, VBUS switching, wake). These do **not** have to be
the same controller. High-speed data routes to the SoM; port management can be owned by a **low-
power core** (the MSP430 here) that stays awake in deep sleep while the SoM is off. For a battery
product that spends most of its life asleep, having the low-power core own management is very
attractive: charging, attach-detect, and *wake-the-SoM-on-plug-in* all work with Android fully
powered down, and standby current stays tiny. This split is cleanest in the **no-PD / 5 V**
design (Tier 0/1) — the low-power core only has to run a Type-C CC state machine (attach /
orientation / role), not a full PD policy engine. It reshapes, rather than removes, the OS's
view of the port — see `references/android-and-safety.md` for how Android still gets battery and
USB-role state when the low-power core, not the kernel, owns the port.

## The first job: pin down requirements before choosing chips

Most bad USB-C designs come from choosing a chip before answering these. Get these answered
(ask the user; don't assume) — they collapse the design space fast:

1. **Input power ceiling.** How many watts must the device pull *in* at peak? If **≤ 15 W
   (5 V × 3 A)**, you may never need to negotiate PD at all. If you need **> 15 W or any voltage
   above 5 V**, you need a PD *sink* that negotiates 9/12/15/20 V or PPS.
2. **Does the device source power out?** Only ≤ ~1 A at 5 V (e.g. power a small peripheral)? A
   plain Type-C source (Rp resistors + a 5 V rail) does it — no PD needed. Must it advertise
   PD voltages/currents to what it powers? Then you need a PD *source*.
3. **Alt Mode (DisplayPort / video over USB-C)?** This is the single biggest gate. DP Alt Mode
   *requires* a real PD controller that speaks structured VDMs and drives a high-speed mux. An
   MCU running "simple logic" cannot stand in for it. If Alt Mode stays, a PD controller stays.
4. **Data role(s).** Pure charging → no data lines at all. Act as a USB device to a PC/phone →
   route USB2 (and maybe USB3) with an orientation mux. Act as a host → same, plus you drive
   the bus.
5. **Cells: how many and in what arrangement?** 1S, 2 in parallel (2P, electrically 1S), or 2
   in series (2S). This picks your charger class and whether you need cell balancing. See
   `references/chargers-and-cells.md`.
6. **Run while charging** is a *hard* requirement here → you need a **power-path / NVDC**
   charger (a charger with a separate system output node). See below.
7. **What OS runs on the SoC, and is this a regulated product class (e.g. a toy)?** These two
   veto parts that the electrical tiers would otherwise allow — see the next section.

For the bob-929 device specifically these resolve as: **1S cell, SoM runs at ~3.3/3.6 V (not a
boosted 5 V), modest sustained power** (a single 18650 can't feed a hungry SoC for long, so it
never runs full-out), **Android** on the i.MX 8, **children's toy** (must never run hot). Those
answers push hard toward the no-PD-controller, low-voltage, thermally-conservative path.

## Two product-level constraints that can veto a chip

Independent of the electrical tiers, two things decide whether a part is even viable:

- **What OS owns the port.** If the SoC runs **Android/Linux**, prefer parts with **mainline
  kernel drivers** — a Type-C/PD PHY the kernel **TCPM** framework already supports (FUSB302,
  PTN5110, HD3SS3220) and a charger with a **`power_supply`** driver (the BQ24250/BQ2589x/BQ2579x
  families). Then Android's battery UI, charge control, thermal throttling, and role management
  work out of the box instead of via out-of-tree drivers you maintain forever. On Android, letting
  the *kernel* own PD (FUSB302 + TCPM) is usually better than an MSP430 PD stack.
- **Regulated product class.** A **children's toy** is bound by EN 71 / IEC 62115 / ASTM F963 and
  battery safety (IEC 62133, UN 38.3). The binding constraint is **accessible surface temperature**
  (~≤ 48 °C metal), and the worst-case thermal event is **running while charging** — the exact mode
  required here. This caps charge current and dictates component placement more than any datasheet.

Both are covered in depth in `references/android-and-safety.md` — read it before finalizing chip
choice for any Android or consumer/child product.

## The decision that dominates everything: do you even need a PD controller?

A full PD port controller (TPS6598x, TPS2575x, Infineon CCGx, …) is the most expensive, most
firmware-heavy, and highest-layout-risk part in a USB-C front end. Half of good device-side
design is figuring out whether you can *avoid* one. Walk this gate:

```
Need DisplayPort/Thunderbolt Alt Mode on any port?
├─ YES ─────────────────────────────► You need a full PD controller with a HS mux.
│                                      Go to references/pd-and-cc-controllers.md (Tier 3).
└─ NO
   Need to pull IN more than 15 W, or any voltage above 5 V?
   ├─ YES ──────────► You need a PD SINK, but not a full controller.
   │                  An autonomous sink (STUSB4500) or a charger with built-in PD sink
   │                  (BQ2589x/BQ2579x) negotiates high power with NO firmware.
   │                  Go to references/pd-and-cc-controllers.md (Tier 1).
   └─ NO (5 V / ≤15 W is enough in)
      Need to SOURCE more than 5 V out?
      ├─ YES ──────► You need a PD source controller. Tier 2.
      └─ NO ───────► NO PD CONTROLLER NEEDED.
                     Sink side = Rd (5.1 kΩ) + a power-path charger.
                     Source side = Rp resistors + a 5 V rail + a USB2 orientation mux.
                     An MSP430/simple MCU reading CC comparators handles orientation,
                     attach/detach, and role supervision. Tier 0.
```

The honest tradeoff: dropping the PD controller saves cost, firmware, and a hard-to-lay-out
chip, but caps you at 5 V in/out and kills Alt Mode. If the product's power budget genuinely
fits in 15 W and video-over-USB-C isn't shipping, **a BQ power-path charger + resistor
terminations + an MCU is a legitimate, cheaper, more supply-robust architecture** than a PD
controller. Don't add a PD controller by reflex. See the worked example below.

## Run-and-charge: this means a power-path (NVDC) charger

"Run and charge at the same time" is a topology requirement, not a feature you toggle. Use a
charger with **three nodes — VBUS (input), SYS (system output), BAT (battery)** — a *power-path*
or *NVDC (narrow VDC)* charger. When input is present it powers SYS directly and charges BAT
from the surplus; if the load spikes above the input budget, the battery *supplements* through
the BATFET. When input is removed, BATFET connects BAT→SYS seamlessly.

Why this matters and why the cheap chargers don't cut it: a standalone linear charger (TP4056,
MCP73831) has **no SYS node** — the system is wired straight across the battery terminals, so
load current and charge current mix at the cell, you can't do instant-on from a dead pack, and
fuel-gauging gets messy. Fine for a breadboard, wrong for a shipping run-while-charging device.
Full detail and part tiers in `references/architecture-and-power-path.md` and
`references/chargers-and-cells.md`.

## Chipset selection, in tiers

Pick the lowest tier that meets the requirements. Each references file has the parts, prices,
and tradeoffs.

Pick per port. Each of a device's ports gets its own tier — a common pattern here is a Tier-0/1
sink port plus a Tier-0 resistor source port, with no controller anywhere.

| Tier | What it is | Representative parts | When |
|---|---|---|---|
| 0 | Resistors + MCU logic, **no PD** | Rd/Rp + optional FUSB302 (if you want CC events in firmware) | 5 V only, no Alt Mode |
| 1 | Autonomous PD **sink**, no firmware | STUSB4500, HUSB238, CH224K, or a charger with PD-sink built in (BQ2589x) | Need >5 V in, no Alt Mode |
| 2 | Full **single-port** PD controller | TPS25750 (no Alt Mode), TPS65987D / Infineon CCG6SF (single-port, Alt Mode) | Negotiated source, or one smart port |
| 3 | Dual-port / integrated (**avoid unless justified**) | Infineon CCG6DF / CCG7D (active); ~~TPS65988~~ (NRND) | Only if two ports genuinely must share one controller |

Single-port is the default; Tier 3 dual-port parts are documented for completeness but reach for
them only when two single-port solutions clearly can't do the job. Details, current lifecycle
status, and per-part tradeoffs: `references/pd-and-cc-controllers.md`.

## Don't skip protection

Every exposed USB-C port needs ESD + fault protection or the first bad cable/charger kills it.
At minimum: IEC 61000-4-2 ESD on VBUS/CC/SBU/D±, VBUS over-voltage protection (a hostile or
faulty source can put 20 V on a node you designed for 5 V), and CC/SBU short-to-VBUS protection.
A combo part like **TI TPD6S300A** covers CC+SBU short-to-VBUS + IEC ESD in one package.
See `references/protection-esd.md`.

## The target is a shippable consumer product — prototypes are just the ladder to it

Design every decision for a **proper end-consumer product**: full ESD/OVP protection, JEITA
thermal charging, in-stock JLCPCB/LCSC parts, DFM-clean layout, and a path through USB-IF/CE/FCC
certification. That's the bar the final design is held to.

Prototypes exist only to de-risk that design cheaply, and they're *allowed* to cut corners the
product can't. On the bench you may use breakout boards, a standalone TP4056-class charger, or
skip some ESD — to answer "is this architecture right?" before committing a PCB. Just never let a
prototype shortcut silently become the product: a TP4056 (no power path) proves nothing about
run-while-charging, and a breakout with no ESD says nothing about field survival. The
prototype→product ladder and what to spend at each rung is in `references/eval-boards-and-cost.md`.

## Eval boards on a budget

The user has flagged eval-board cost as a real constraint. The strategy: **buy the vendor EVM
only for the one genuinely hard chip** (the PD controller or the switching charger — where you
need the reference layout and the config/GUI tooling), and prototype everything cheap around it
with $4–$15 breakouts. A full breakout-based sink+charge loop can be proven for ~$30 total,
versus $150–$250 for a single TI EVM. Full option list with current prices:
`references/eval-boards-and-cost.md`.

## Worked example: the bob-929 "292" power module

This skill lives in a real project. The 292 power module has two USB-C ports — an **OTG** port
(sink: charge in, act as USB device) and a **Host** port (source: ≤ 900 mA out, act as USB
host, *experimental* DisplayPort Alt Mode) — one Li-ion cell (optionally 2P), a BQ24250
power-path charger, TPD6S300A protection, and originally a **TPS65988** dual-port PD controller.

The TPS65988 is now **NRND (the whole family — TI has no active dual-port successor)**, forcing
a rearchitecture. The clean move is to stop treating this as a *dual-port* problem: split it
into two single-port designs. Run each port through the gate above:

- **If Alt Mode stays a real requirement on the Host port** → give *that one port* a single-port
  Alt-Mode controller (Infineon **CCG6SF** single-port, or TI TPS65987D), and leave the OTG/sink
  port as a Tier-0/1 resistor-or-autonomous-sink design. That already removes the dual-port
  chip. Only if the two ports must be co-managed would you consider a dual-port CCG6DF/CCG7D.
- **Alt Mode is experimental-only** (the 45-pin connector is explicitly for experimentation; if
  fitted it's for the i.MX 8 to render a basic debug screen, on some variants only), and the SoM
  runs at ~3.3/3.6 V from a 1S cell at modest power → **delete the PD controller from the base
  design**:
  - OTG port: Rd + the BQ24250 power-path charger handles charge-in (and BQ24250 has a mainline
    `power_supply` driver, so Android sees the battery cleanly). Add an STUSB4500 *only if* a
    variant genuinely needs >5 V in — the low-power 1S toy almost certainly doesn't.
  - Host port: Rp resistors advertise 5 V source + a low-current 5 V boost; the SoM's USB host
    drives data; the existing TS5USBC410 USB2 mux handles orientation.
  - Because it's **Android**, let the **kernel own the Type-C port**: an FUSB302 or HD3SS3220
    (both mainline-supported) gives clean attach/orientation/role events without a PD engine,
    rather than pushing PD onto the MSP430. The MSP430 stays for low-level supervision/wake.
  - The experimental DisplayPort variant is the *only* place a single-port Alt-Mode controller
    (CCG6SF) earns a spot — as a populate-optional sub-circuit, never in the base toy.

This is the live decision to help the user reason through — see the message thread. The
reference files give you the parts and tradeoffs to make the case either way with evidence.

## Producing a BOM for the USB / data / power section

When the task is "give me the BOM" or "cost this front-end," the BOM is a deterministic roll-up of
the architecture decisions — **decide the tiers first, then generate**. Assume the central SoM is
an **i.MX 8M Plus** class part (it brings the USB PHYs and its own core-rail PMIC; this board
provides the receptacle, protection, CC/PD, muxing, charger + power path, and the **VSOM** system
rail that feeds the SoM). Route a USB3/Alt-Mode port to the SoM's **USB1** (SS-capable) and a
charge-in/device port to **USB2**.

Walk the functional blocks, pull each part from the matching reference file, and **don't
under-count the passives** (decoupling, I2C pull-ups, charger inductor/sense/NTC/caps). Mark
Alt-Mode and other optional parts **DNP** so one board serves two build variants. Full method,
the CSV column spec, passive-count rules, and a worked i.MX 8M Plus example are in
`references/bom-generation.md`. Fill `assets/usb-power-bom-template.csv` and run
`python3 scripts/bomcost.py <bom.csv>` for a per-block/total cost roll-up that also flags
Extended-part feeder fees and single-source ICs. Always report the cost **with its assumptions**
(cells, 5 V-only, Alt-Mode optional) — a number without them misleads.

## Reference files

- `references/architecture-and-power-path.md` — topologies, NVDC/power-path deep dive,
  run-while-charging, where each rail comes from, block diagrams for each architecture.
- `references/pd-and-cc-controllers.md` — CC termination, PD controller tiers, part-by-part
  with lifecycle status, the "no PD controller" pattern in detail, data/Alt Mode muxing.
- `references/chargers-and-cells.md` — 1S vs 2S vs 2P, charger classes, cell balancing, gauging,
  buck-boost vs buck vs boost, specific charger parts.
- `references/protection-esd.md` — ESD, VBUS OVP, CC/SBU protection, VCONN, dead-battery.
- `references/android-and-safety.md` — Android/mainline-kernel driver support as a chip-selection
  axis (TCPM/`power_supply` parts), and children's-toy safety limits (surface temp, JEITA, battery
  compartment, run-while-charging thermal). Read before finalizing chip choice.
- `references/eval-boards-and-cost.md` — eval board and breakout options with current prices,
  cheap-prototyping strategy, where to spend and where to save.
- `references/designs-in-the-wild.md` — a cost/sophistication ladder of real device-side
  architectures, plus **sourced OEM/teardown case studies** (NXP i.MX 8M EVK + PTN5110, Raspberry
  Pi 4's CC-resistor flaw, Nintendo Switch, Steam Deck, Framework). Read to place your design
  against precedent and copy a proven pattern.
- `references/bom-generation.md` — how to produce the USB/data/power **BOM** assuming an i.MX 8M
  Plus SoM: block-by-block method, CSV column spec, passive-count rules, and a worked example.
  Uses `assets/usb-power-bom-template.csv` and `scripts/bomcost.py` (per-block/total cost roll-up).