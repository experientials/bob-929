# Chargers & Cells

Picking the battery arrangement and the charger. Read this when deciding 1S/2S/2P and which
charge IC. Pairs with `architecture-and-power-path.md` (topology) — this file is the parts.

## Cell arrangement first — it dictates the charger

| Arrangement | Voltage | Capacity | Balancing? | To 3V3 | To 5 V out | Complexity |
|---|---|---|---|---|---|---|
| **1S** | 3.0–4.35 V | 1× | no | buck | **boost** | lowest |
| **2P** (parallel) | 3.0–4.35 V | 2× | no | buck | **boost** | = 1S |
| **2S** (series) | 6.0–8.7 V | 1× energy, 2× V | **yes** | buck | buck | higher |

- **2P is the safe way to "use two cells."** Electrically it *is* 1S at double capacity — same
  charger, same rails, no balancing, no new protection. The bob-929 "dual NCR18650B 6800 mAh"
  option is this: two 3400 mAh cells in parallel keeping 1S voltage. Prefer 2P unless peak power
  forces 2S.
- **2S** halves trunk current for a given power (I = P/V), which eases routing and connector
  heating on higher-power devices — but it costs you a **balancing charger**, a **2S protection
  IC**, and a buck to reach logic rails. Series cells drift apart in state-of-charge and *must*
  be balanced or one cell over/under-charges over time. Don't take 2S on without balancing.
- **Consumer-product angle:** cell selection also drives your safety certification story (UN38.3
  transport, IEC 62133, and pack-level protection). A single-cell or 2P pack with a protected
  cell + a charger with safety timers/JEITA thermal profile is the well-trodden path. 2S packs
  need a proper BMS and more scrutiny. Factor this into the choice, not just the electronics.

## JEITA / thermal — non-negotiable for a shipping product

Any consumer Li-ion product must throttle or stop charging by temperature (the JEITA guidelines:
reduced current when cold, reduced voltage/current when hot, no charge outside ~0–45 °C). Use a
charger with a **TS/thermistor input** and wire an NTC to the pack (several bob-929 candidate
cells have embedded thermistors — use them). A dev prototype can skip this on the bench; a
product cannot. This is a common gap in hobby-grade designs that blocks certification.

## Charger classes and specific parts

### Standalone linear — PROTOTYPE ONLY
- **MCP73831**, **TP4056** (~$0.2–0.5). One cell, no SYS node, no power path. Fine to bring a
  board up on the bench; **not** for a run-while-charging consumer product (see
  `architecture-and-power-path.md` on why the battery-in-the-path topology is wrong).

### 1S switching with power path (NVDC) — the product baseline
- **TI BQ24250** (the bob-929 part, ~$2) — 2 A switch-mode single-cell charger with **integrated
  power-path/system node**, input DPM, safety timers, NTC. Solid, proven, JLCPCB-stocked. Good
  default for a 1S run-while-charging device.
  - **Application values (from the datasheet in `Hardware/292/datasheets/`):** switches at **3 MHz**
    → small **~1 µH** inductor (pick saturation current ≥ your programmed ICHG). **CBOOT 33 nF**,
    **CPMID 1 µF**, **CIN 2.2 µF** at VBUS. Charge current is set by **RISET**: `ICHG = KISET/RISET`
    (KISET ≈ 250 A·Ω, V_ISET ≤ 0.42 V, RISET ≥ 75 Ω); input limit by **RILIM** on the ILIM pin.
    Both ICHG and ILIM programmable **up to 2 A**. **VREF_DPM 1.2 V** sets input-voltage DPM via a
    divider. **VOVP is register-programmable 6.0–10.5 V** — set it just above your max input so a
    hostile source can't push the SYS/BAT path. JEITA thermal via **RNTC** on the TS pin.
  - *Note the erratum in the datasheet:* the **ISET resistor must be connected** (not floated) or
    the charger enters an unstable state — an easy footgun on a first spin.
- **The cheap I2C switching family — consider these first for bob-929.** All 1S, NVDC power path,
  I2C, integrated **OTG boost (5 V out)**, BC1.2 D+/D− detection, JEITA — differing mainly in
  current and input tolerance. LCSC-stocked and inexpensive:

  | Part | Charge / input | Extra | Notes |
  |---|---|---|---|
  | **BQ25601 / BQ25601D** | 3 A, up to 6.2 V in | OTG boost, D+/D−/BC1.2, VINDPM | The mainstream cheap workhorse |
  | **BQ25618 / BQ25619** | 1.5 A | OTG, lower-power tuned | Cheapest; fine if charge rate is modest |
  | **BQ25628 / BQ25629** | 2 A, **up to 18 V in** | NVDC, OTG, TS_BIAS | Newer; wide-input tolerance is a nice safety margin |
- **TI BQ25896 / BQ25898** (~$2–3) — 1S, power path, **integrated boost (OTG 5 V out)**, D+/D−
  (BC1.2/QC/Apple) detection, **Input Current Optimizer (ICO)**, I2C, on-chip **ADC** for coarse
  gauging. The "one chip does charge-in **and** 5 V-out **and** input detect **and** gauge" part —
  attractive here because it can supply the Host-port 5 V rail *from its own boost*, deleting a
  separate boost converter, and it feeds Android a battery reading via its ADC.
- **MPS MP2731 / SGMicro SGM41511 / SGM41542** — cost-optimized 1S power-path clones of the above,
  LCSC-stocked; good for shaving BOM at volume.

**Nano-Iq LINEAR power-path (the deep-sleep angle — but mind the heat):**
- **TI BQ25155 / BQ25157** — 500 mA 1S **linear** charger, power path, **10 nA Iq**, regulated SYS,
  16-bit ADC, LDO, push-button controller. **BQ25150** is the 25155 without the ultra-low Iq.
  **BQ25120A** — nano-PMIC: charger + buck + LDO + load switch. These are built for exactly this
  product's *standby* profile — a device asleep most of its life, supervised by a low-power core —
  where a switcher's µA-class Iq would dominate the battery budget.
  - **The catch for bob-929: they're linear and only 500 mA.** A linear charger burns
    `(V_in − V_bat) × I_chg` as heat — from 5 V into a 3.7 V cell at 500 mA that's ~0.65 W, and in
    a **children's toy the accessible-surface temperature is the binding limit** (see
    `android-and-safety.md`). Worse, 500 mA into a 4000–8000 mAh pack is an **8–16 h** charge —
    too slow for these cells. So use the nano-linear parts only if the pack is small; for the
    real bob-929 packs, a **switching** power-path part (BQ24250 / BQ25601D / BQ25628) charges
    faster *and* cooler, at the cost of higher Iq — which the power-path SYS node and a good
    sleep state keep acceptable.

**Android/Linux mainline driver mapping** (so the OS sees the battery — see `android-and-safety.md`):
`bq24257_charger.c` → BQ24250/57 · `bq256xx_charger.c` → BQ25600/601/611D/618/619 ·
`bq25890_charger.c` → BQ25890/92/95/96 · `bq2515x_charger.c` → BQ25150/155/157 ⚠ (verify against
your kernel) · `bq2579x` → BQ25792/98 · `bq27xxx_battery.c` → BQ27xxx gauges.

### 1–4S buck-boost with power path — the flexible product part
- **TI BQ25792 / BQ25798** (~$3–4, EVM ~$149) — I2C, **1-to-4-cell**, 5 A **buck-boost** charger
  with power path, integrated ADC gauge, MPPT (solar), and USB-C/BC1.2 detect. The single best
  part when the product must support **1S *or* 2S** on one board, or when you want input from a
  wide range (3.6–24 V). BQ25798 adds an integrated switching **output** (dual-role). Pay for the
  buck-boost specifically to get 1S/2S flexibility and battery-above-or-below-VBUS operation.

### 2S / multi-cell
- **TI BQ25887** — 2S with **integrated cell balancing**; the clean 2S single-charger answer.
- **TI BQ25792 / BQ25798** — 1–4S buck-boost with power path (also listed above); the flexible
  choice if a board must populate as either 1S or 2S.
- **TI BQ25703A / BQ25710 / BQ25720** — host-controlled NVDC buck-boost (1–4S) with external FETs,
  SMBus/I2C, laptop/high-power class; more design work, more power.
- **MPS MP2760** — 1–4S buck-boost alternative, LCSC-stocked.

## Fuel gauging

- A charger with an **integrated ADC** (BQ2589x, BQ2579x) gives coarse voltage/current — enough
  for a battery bar.
- For an accurate **%** across temperature/age, add a dedicated gauge: **BQ27421/BQ27427/BQ27441**
  (Impedance Track, single-cell, tiny), **BQ27Z561** (1S with protection), **BQ34Z100** (multi-cell),
  or **MAX17048** (ModelGauge, no sense resistor — very few parts). All BQ27xxx are covered by the
  mainline `bq27xxx_battery.c` driver, so Android reads them for free. A consumer product that shows
  a battery percentage really wants a real gauge; a prototype can live on raw voltage.

## Sourcing note (bob-929 / cost)
Prefer parts that are **JLCPCB/LCSC basic-or-extended stock** for the charger and its passives —
it's the biggest single-chip on the power path and a stock-out there blocks the whole board. The
BQ24250 and several MPS/SGMicro parts are LCSC-listed; verify current stock before committing.
