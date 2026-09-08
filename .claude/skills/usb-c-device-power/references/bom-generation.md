# Producing the USB / Data / Power BOM

How to generate a bill of materials for the USB-C connectivity, data, and power section of a
board whose central SoM is an **i.MX 8M Plus** (or same-class NXP SoM). Read this when the task is
"give me the BOM," "cost this front-end," or "what parts do I need for the USB/power side."

The BOM is not a guess — it's a **deterministic roll-up of the architecture decisions** made in the
other reference files. Decide the tiers first (port roles, PD-or-not, cells, muxing), then this
file turns those decisions into line items.

## Scope & assumptions

- **Central SoM: i.MX 8M Plus class.** The SoM brings the USB *PHYs* and (usually) its own PMIC for
  core rails. **This BOM covers the carrier/power board's job:** the USB-C receptacle(s), port
  protection, CC/PD management, data orientation/Alt-Mode muxing, the battery charger + power path,
  the system rail (**VSOM**) that feeds the SoM, and the supporting passives. It does **not** cover
  the SoM's internal DDR/core rails.
- **i.MX 8M Plus USB mapping** (drives which port carries what):
  - **USB1 = USB 3.0 (SuperSpeed) + USB 2.0 combo**; **USB2 = USB 2.0 only.**
  - A port that needs **USB3 or DisplayPort Alt Mode → route to USB1** (SS lanes go through a
    TUSB546/redriver). A **charge-in / device port** that only needs USB 2.0 → **USB2**.
  - NXP's own i.MX 8M reference does USB-C PD with a **PTN5110 TCPC + kernel TCPM**; include a
    PTN5110/FUSB302 only if you want the OS to manage the port (see `android-and-safety.md`).
- **Power baseline** (per the bob-929 decisions): **1S Li-ion** (or 2P), run-while-charging via a
  **power-path charger**, 5 V-in sufficient → **no PD controller** in the base design; DisplayPort
  is a **populate-optional (DNP)** variant.

## Method: walk the functional blocks

Every block below contributes parts. Go block by block; for each, pull the specific part from the
matching reference file, then add its **mandatory support components** (the passives are where BOMs
get under-counted). Skip a block only if the architecture doesn't use it.

| # | Block | Core part(s) | Mandatory support parts | Ref file |
|---|---|---|---|---|
| 1 | USB-C receptacle | 16- or 24-pin USB-C socket (per port) | shield/mounting, optional shield cap+R | `designs-in-the-wild.md` |
| 2 | Port protection | TPD6S300A (per port) | decoupling 100 nF; VBUS TVS | `protection-esd.md` |
| 3 | CC / PD mgmt | **Tier 0:** 2×5.1 kΩ Rd (sink) or 2×Rp (source); **Tier 0+:** HD3SS3220; **Tier 1:** STUSB4500 + VBUS PMOS; **Tier 2:** CCG6SF/TPS25750 | CC caps, VCONN cap, controller decoupling, config EEPROM if needed | `pd-and-cc-controllers.md` |
| 4 | Data orientation mux | USB2: TS5USBC410; USB3/DP: TUSB546 (DNP) | AC-coupling caps on SS pairs, decoupling | `pd-and-cc-controllers.md` |
| 5 | Charger + power path | BQ24250 / BQ25601D / BQ25896 | **inductor 1 µH**, RISET, RILIM, CIN 2.2 µF, CPMID 1 µF, CSYS/CBAT 10 µF, CBOOT 33 nF, NTC 10 k (103AT) + bias R | `chargers-and-cells.md` |
| 6 | 5 V source-out (if host sources) | dedicated boost, **or** use BQ25896's integrated OTG boost | boost inductor + caps (if dedicated) | `architecture-and-power-path.md` |
| 7 | VSOM system rail | bulk caps on SYS; optional load switch | 10–22 µF bulk, ferrite/π-filter | `architecture-and-power-path.md` |
| 8 | Fuel gauge (optional) | MAX17048 / BQ27441 | sense R (if used), decoupling | `chargers-and-cells.md` |
| 9 | Supervisor interface | I2C pull-ups (4.7 kΩ ×2 per bus), level shift if needed; STAT LED + R | — | `android-and-safety.md` |
| 10 | Battery connector | JST SH/PH (keyed) | — | project docs |

**Passive-count rules of thumb** (so you don't under-BOM):
- Every active IC: **1×100 nF decoupling minimum**, plus its bulk cap where the datasheet shows one.
- Every I2C bus: **2× pull-ups** (4.7 kΩ typical; compute per `slva689` for bus capacitance).
- Switching charger: the inductor's **saturation current ≥ programmed ICHG**, and DCR low for
  efficiency/heat (toy thermal limit).
- Mark **populate-optional** parts **DNP** (Do Not Populate) rather than deleting — one board, two
  build variants (base vs Alt-Mode).

## BOM column spec (use this exact header)

Produce the BOM as CSV with these columns — it imports cleanly into JLCPCB/spreadsheets and carries
everything sourcing and costing need:

```
RefDes, Qty, Block, Function, Value, MPN, Manufacturer, Package, LCSC, BasicExt, UnitUSD, ExtUSD, AltMPN, DNP, Notes
```

- **BasicExt** = JLCPCB `Basic` or `Extended` (Extended parts add a per-part feeder fee — prefer
  Basic where possible; note when you couldn't).
- **DNP** = `Y` for populate-optional (Alt-Mode variant) lines.
- **AltMPN** = a second source, because a single-source charger/PD chip is a supply risk.

A ready-to-fill template with example rows is in `assets/usb-power-bom-template.csv`. The roll-up
script `scripts/bomcost.py` totals it per block and flags Extended-part fees.

## Worked example — bob-929 base build (1S, 5 V, no PD controller, i.MX 8M Plus)

Charge-in on a USB2 device port + optional 5 V host-out, kernel-managed via HD3SS3220. Prices are
rough LCSC qty-1 for scale, not quotes.

| Block | Part | Qty | ~Unit | ~Ext |
|---|---|---|---|---|
| Receptacle | USB-C 16P socket | 1–2 | $0.18 | $0.36 |
| Protection | TPD6S300A | 1–2 | $0.80 | $1.60 |
| CC mgmt | HD3SS3220 (or 2×5.1 kΩ for pure resistor) | 1 | $0.70 | $0.70 |
| Charger | BQ24250 (or BQ25601D ~$0.6) | 1 | $1.80 | $1.80 |
| Charger passives | 1 µH ind, RISET/RILIM, CIN/CPMID/CSYS/CBAT/CBOOT, NTC | ~12 | — | $0.60 |
| Data mux | TS5USBC410 | 1 | $0.40 | $0.40 |
| VSOM bulk | 22 µF + 10 µF | 2–3 | $0.05 | $0.15 |
| Gauge (opt) | MAX17048 | 1 | $1.10 | $1.10 |
| Supervisor | I2C pull-ups, STAT LED+R | ~5 | — | $0.10 |
| Battery conn | JST SH 2-pin keyed | 1 | $0.10 | $0.10 |
| **Base total** | | | | **≈ $6–8** |

**DisplayPort Alt-Mode variant (all DNP):** add CCG6SF (~$2.0) + TUSB546 (~$1.5) + SS AC-coupling
caps and decoupling (~$0.3) → **+ ≈ $4–5** on the variant build only. If you also want the
kernel to manage PD on the base build, add a **PTN5110 (~$1.0)** instead of / alongside HD3SS3220.

## Output & workflow

1. Confirm the tiers (ports, PD-or-not, cells, muxing) — the BOM is meaningless without them.
2. Fill `assets/usb-power-bom-template.csv` block by block using the table above; put real LCSC part
   numbers and prices (extract them prompt-free with the `collect-pdf-info` skill from datasheets,
   or pull from LCSC/JLCPCB parts search).
3. Run `python3 scripts/bomcost.py <your-bom.csv>` for per-block and total cost, part count, and an
   Extended-part-fee flag.
4. Report: the CSV, the cost roll-up, single-source risks (charger/PD), and which lines are DNP for
   which build variant. Always state assumptions (cells, 5 V-only, Alt-Mode optional) alongside the
   number — a BOM cost without its architecture assumptions is misleading.
