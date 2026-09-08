# Protection & ESD

A USB-C port is a hostile interface: users plug in unknown cables and chargers, discharge static
into it, and occasionally short it. For a **consumer product** this section is not optional — it's
the difference between "survives the field" and RMA. A dev prototype can defer some of it on the
bench, but design the product with all of it. Read this when laying out any exposed port.

## The threats, and the part that handles each

| Threat | What happens | Protection |
|---|---|---|
| **ESD** (IEC 61000-4-2, ±8–15 kV) | Static zap on any exposed pin | Low-capacitance TVS on VBUS, CC1/2, SBU1/2, D+/D− |
| **VBUS over-voltage** | A faulty/hostile source puts 9–20 V on a node you designed for 5 V | VBUS OVP clamp or an OVP load-switch that disconnects downstream |
| **CC/SBU short-to-VBUS** | A bad cable shorts VBUS (up to 20 V) onto the 3.3 V CC/SBU logic | CC/SBU short-to-VBUS protection (rated to 20–22 V) |
| **Reverse current** | Battery back-drives a collapsed VBUS, or sourced VBUS gets back-fed | Reverse-current blocking in the charger/load-switch |
| **Over-current / short** | Downstream short on a sourced port | Current-limited load switch or the controller's integrated limiter |

## Combo parts do most of this in one package

- **TI TPD6S300A** (the bob-929 part) — CC + SBU **short-to-VBUS** protection **and** IEC 61000-4-2
  ESD for the whole connector in one QFN. One per USB-C port. This is the standard "protect the
  whole receptacle" part and is why it's already in the design — keep it. **From the datasheet
  (`Hardware/292/datasheets/ESD USB tpd6s300a.pdf`):** 4 channels of short-to-VBUS OVP on
  **CC1, CC2, SBU1, SBU2** (24-V DC tolerant — it puts high-voltage FETs *in series* on the CC and
  SBU lines and opens them on a fault, isolating your 5 V logic from up to 20 V on the connector);
  6 channels of IEC 61000-4-2 ESD (adds **DP, DM**); and it **integrates the CC dead-battery
  resistors**, so the port stays correctly terminated (and connected during an ESD strike) even
  with a flat battery. It sits between the connector and the CC/SBU pins of your controller/MCU.
- **TI TPD4S / onsemi ESD8 / Nexperia PRTR/IP4234** — lighter combo TVS arrays if you only need
  ESD (not the short-to-VBUS logic). Cheaper, less coverage.
- For **VBUS OVP** specifically, either a dedicated OVP switch (TPS2596, TPD1E for signal) or rely
  on a charger/PD-controller input stage rated for 20–28 V. Confirm the charger's absolute-max
  VBUS exceeds the worst PD voltage a hostile source could apply.

## Placement rules that actually matter

- **ESD parts go right at the connector**, before anything else, with the shortest possible path
  to a solid ground pour. A TVS with a long stub does nothing — the inductance ruins the clamp.
- Keep **low junction capacitance** on the high-speed pairs (D± and especially USB3): a fat TVS
  wrecks signal integrity. Use pF-class parts on data lines.
- Route **CC and SBU through the protection IC**, not around it.
- Give the connector shield a defined path to chassis/ground (often via a small cap + high-value
  resistor, or direct, per your EMC strategy).

## VCONN and dead-battery

- **VCONN**: when the non-oriented CC pin must power an e-marked/active cable (needed for 5 A
  cables and many Alt Mode cables), you supply 5 V onto it through a VCONN switch. Autonomous
  parts (STUSB4500) and full controllers integrate or drive this; a Tier-0 resistor port ignores
  it (fine for ≤3 A passive cables).
- **Dead-battery**: the port must present the correct CC state and let the system boot from input
  when the battery is flat. STUSB4500 and the TPS/CCG controllers have explicit dead-battery
  behavior; a resistor sink is dead-battery-correct by construction (Rd is always present).

## Prototype vs. product checklist

- **Prototype (bench):** ESD parts can be omitted on the very first bring-up board if you're
  careful, but populate at least VBUS OVP and CC short-to-VBUS before you plug into arbitrary
  chargers/cables — those failures are instant and destructive.
- **Product (ship):** full IEC 61000-4-2 ESD on every exposed pin, VBUS OVP, CC/SBU
  short-to-VBUS, reverse-current, over-current, JEITA thermal (see `chargers-and-cells.md`), and
  connector-shield EMC. Plan for USB-IF / regulatory (CE/FCC) testing — designing the protection
  in from the start is far cheaper than retrofitting after a failed test.
