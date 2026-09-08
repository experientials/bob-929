# Eval Boards, Prototyping Strategy & Cost

The goal of these designs is a **proper consumer product**, but you get there through cheap
prototypes. This file is about spending eval money where it buys risk reduction and cutting
corners where it's safe to. Read it when planning bring-up or budgeting eval hardware.

## The core strategy: buy the EVM for the one hard chip, breakout the rest

A full vendor EVM is $99–$249. You rarely need more than one. The rule:

- **Buy the EVM only for the genuinely hard chip** — the switching charger or the PD controller.
  What you're paying for isn't the silicon, it's (a) a **proven reference layout** you can copy
  into your board, and (b) the **config/GUI tooling and firmware image** (TI's GUI Composer /
  Application Customization Tool, Infineon's EZ-PD Configuration Utility) that turns a blank part
  into a working one. That tooling is the real time-saver.
- **Breakout everything else** — CC termination, sink triggers, protection, muxes, gauges — with
  $4–$15 modules. Wire them together to prove the *system* (does it negotiate, does it charge,
  does it run while charging) long before you commit a PCB.

A complete sink-and-charge prototype loop can be stood up for **~$30** in breakouts versus
$150–$250 for a single EVM. Prove the interactions cheaply; use the EVM only for the part whose
layout/config you can't afford to get wrong.

## Cheap breakouts (prototype-grade — expect to redesign for product)

| Part / function | Board | ~Price | Notes |
|---|---|---|---|
| STUSB4500 autonomous PD sink | SparkFun Power Delivery Board | ~$13 | Solder-jumper or I2C PDO config; great for "give me 9/12/20 V in, no firmware" |
| HUSB238 fixed-voltage PD sink | Adafruit HUSB238 breakout | ~$4 | Dial in one PD voltage; dead-simple |
| FUSB302 CC PHY | Adafruit / generic breakout | ~$6–8 | Only if you're writing a PD stack on your MCU |
| 1S power-path charger | BQ25896/BQ24296 module (AliExpress) | ~$3–6 | Power-path + boost; closest cheap analog to the product topology |
| 1S linear charger | TP4056 module | ~$1 | Bench only — no system node, wrong topology for product |
| Fuel gauge | MAX17048 / BQ27441 breakout (SparkFun) | ~$15 | Prove gauging early; it's model-dependent |
| USB-C breakout w/ CC pins broken out | generic | ~$2 | For probing CC/orientation on the bench |

These get you to "the negotiation and charge loop work" fast. **None of them are the product** —
they skip the ESD/OVP/thermal a shipping device needs (see `protection-esd.md`).

## Vendor EVMs (reference-layout grade)

| EVM | For | ~Price |
|---|---|---|
| **TI BQ25792EVM** | 1–4S buck-boost charger + power path (the flexible charger) | ~$149 |
| **TI TPS25750EVM** | Single-port PD controller, integrated switches, no Alt Mode | ~$99–199 |
| ~~TI TPS65988EVM~~ | Dual-port PD controller — **NRND, don't design in** | ~$249 |
| **Infineon CY4531 / CCG-series EVK** | CCGx PD controller bring-up + EZ-PD config tooling | ~$50–150 |
| TI BQ24250EVM | The bob-929 1S power-path charger reference | ~$99 |

Get the EVM for whichever of {charger, PD controller} you're least confident laying out. If
you're doing the Tier-0 "no PD controller" architecture, you may not need *any* PD EVM — just the
charger EVM (or even just the AliExpress power-path module) plus breakouts.

## Prototype → product ladder

Match your spend and rigor to the stage; don't gold-plate stage 1 or cut corners at stage 3.

1. **Concept / interaction proof (~$30–50).** Breakouts on a bench: does it negotiate the voltage
   I need, charge the pack, and keep running when I pull the battery? Skip ESD, skip final
   layout. Answer "is this architecture right?" cheaply.
2. **Integrated prototype (1 EVM + a spin of your own PCB).** Copy the EVM reference layout for
   the hard chip onto your board; add the real protection, real connectors, real mechanical.
   Bring up firmware/config against the vendor tooling. Answer "does *my* board work?"
3. **Product / DFM (JLCPCB/PCBWay-manufacturable).** Full protection and JEITA thermal, all parts
   chosen for **in-stock LCSC/JLCPCB** availability, differential pairs routed and length-matched,
   footprints verified against datasheets, ESD parts at the connector, EMC/regulatory (CE/FCC,
   USB-IF) planned in. This is where the bob-929 review checklist lives (see the 292 power-module
   docs). Answer "can this ship and pass certification?"

## Cost discipline reminders

- Favor charger/PD parts that are **LCSC basic or extended stock** — a stock-out on the power-path
  chip halts the whole board. Verify stock before committing, not after.
- The cheapest *product* architecture is often the one with the **fewest active parts**: the
  Tier-0 "resistors + power-path charger + MCU, no PD controller" path (when 5 V in/out suffices)
  beats a PD-controller design on BOM cost, layout risk, firmware, *and* supply resilience. Don't
  pay for a PD controller you can design out — see `pd-and-cc-controllers.md`.
