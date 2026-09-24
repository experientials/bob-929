# bench — physical layout & mounting

The **physical realization** of the bench: how the carrier + dev boards + power are mounted and
interconnected. The electrical "which wire goes where" is [`bench-v1-wiring.md`](bench-v1-wiring.md);
this doc is the mechanical/physical side. (Photos shared 2026-09-21.)

## Substrate

- A **2× acrylic blow-up of the Bob-929 form factor** — a shaped, laser-cut acrylic panel that mimics
  the toy's outline (incl. the camera/lens cut-outs) at **2× scale**. Full-size dev boards mount roughly
  where the miniaturized product parts will sit → "Big Bob".
- Multiple benches exist (photo 1 carrier = **SB-UCM Rev 1.0**, photo 2 = **Rev 1.1**).

## Mounted on the panel

| Item | Status | Notes |
|---|---|---|
| SB-UCM carrier + UCM SoM | **mounted** | the DUT |
| MSP430 LaunchPad(s) | **mounting** | supervisor (x33 baseline / x76 diag) |
| Powered USB hub(s) | **mounting** | SoM USB-host → the MCU dev boards (see `DEV-USB-HOST-PROGRAMMER.md`) |
| Power / USB-PD board + battery | **planned** | product-representative power (see Power below) |
| Raspberry Pi 4 | **present, being removed** | see RPi decision below |

## Interconnect (decided by practice)

- **IDC rainbow ribbon off the P20/P21 2×17 headers** + a few discrete jumper wires — the working
  interconnect medium for V1. **No custom bench PCB** for now.
- Open for later: if ribbon+jumpers get unwieldy at N benches, graduate to a small **bench breakout PCB**
  that carries the level shifters and fans P20/P21 out to labeled connectors.

## Power — becomes product-representative

Keep **two distinct things** separate:

**Bench operating power (reality).** The bench likely **upscales to a 12 V / 5 A supply** into the
carrier's **barrel jack (VDC_IN 10–16 V, jack rated 10 A)** and **lets the board function normally** (its
onboard regulators derive V_SOM etc.). Running the whole bench — SoM + 4–6 dev boards + powered hub +
peripherals — off a single cell isn't practical, so **12 V powers everything**. (12 V goes to the barrel
jack; **never to the V_SOM pin.**)

**Product power concept (the ideal / the pending objective).** The *product* target is **a single cell
(1S, ~3.7 V) + 5 V USB input/sink, with NO 5 V rail on the board conceptually** — everything runs off the
single cell; 5 V exists only externally (PD charge / sink). Validating this **product power path** (PD +
battery + power-management chipset) is the **pending objective** — deferred pending the **chipset
revision** (see the "Pending objective" note in [`bench-v1.md`](bench-v1.md); product power tree =
`ziloo/Hardware/Power`, **chipsets TBD — not the assumed MAX77860/301**). It's validated via the product
power board on a subset, **not** by running the whole eval bench off a cell.

## Decisions / open

- **RPi dropped from the V1 bench.** Consistent with the SoM hosting its own USB dev boards, so a manned
  V1 bench doesn't need it. **The supervisor role it carried (unattended power-cycle, HIL orchestration)
  does not disappear — it returns at V2 (the CI lab).** Don't lose that requirement.
- **Power feed point** for the USB-PD/battery path — V_SOM vs 5 V — to confirm.
- **Mounting pattern / standoffs** and board placement on the panel — to formalize (currently ad hoc).
