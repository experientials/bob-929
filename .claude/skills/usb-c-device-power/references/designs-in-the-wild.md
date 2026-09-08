# USB-C Device-Side Designs in the Wild

A ladder of real device-side architectures, ordered by cost and sophistication — what actual
shipping products use. Read this to place your design against precedent and to borrow a proven
pattern instead of inventing one. "Front-end BOM" = the power/USB-C parts only (charger, PD,
protection, muxes), not the whole product.

**Sophistication is not linear with part count.** The cheapest designs and some of the most
capable are both *single-chip* — the difference is whether that chip is a dumb charger or a
fully-integrated PD SoC. The ladder below tracks capability + price together; where they diverge
it's called out.

## The ladder

| # | Architecture | Representative silicon | Real-world examples | ~Front-end BOM |
|---|---|---|---|---|
| 1 | 5 V charge only, no data, no power path | TP4056 / MCP73831 + Rd resistors | cheap toys, LED gadgets, vape pens, disposable earbuds cases | ~$0.30 |
| 2 | 5 V charge + USB2 data, no PD | TP4056 + Rd + D± straight to MCU | Arduino/ESP32 dev boards, cheap wearables | ~$0.50 |
| 3 | 5 V charge **with power path** + USB2 | BQ21080 / BQ24250 / single-cell NVDC + Rd | fitness bands, small IoT, smartwatches (low end) | ~$1.5 |
| 4 | Autonomous PD **sink** for >5 V (no data nego) | STUSB4500 / CH224K + buck or charger | DIY laptop-power boards, monitors, power-tool chargers, e-bike accessories | ~$2 |
| 5 | Fixed PD trigger + charger | HUSB238 / IP2721 / CH224K → charger | fast-charge gadgets, portable projectors, mini PCs | ~$2 |
| 6 | Kernel-managed Type-C + PD PHY + power-path charger | FUSB302 / PTN5110 + BQ2589x | Android SBCs, Linux handhelds, mid phones, **← bob-929 sits here** | ~$4–6 |
| 7 | Integrated charger+boost+PD "power-bank SoC" | Injoinic IP5306 / IP2365 / IP2366, Southchip SW6306 | almost every USB-C power bank, portable chargers | ~$1–3 (!) |
| 8 | Phone-class PMIC + discrete TCPC | Qualcomm/MediaTek PMIC + TCPC (e.g. PM8150 + FUSB302-class) | mainstream smartphones | ~$8–15 |
| 9 | Full single-port PD controller **with Alt Mode** | TI TPS65987D / Infineon CCG6SF + charger + DP mux | tablets w/ video-out, game handhelds, premium devices | ~$8–12 |
| 10 | Multi-cell buck-boost charger + PD | BQ25792/98 (1–4S) or BQ25703 + embedded controller | laptops, high-end tablets, portable power stations | ~$12–20 |
| 11 | Dual-port / integrated PD + Alt Mode / Thunderbolt | Infineon CCG6DF/CCG7D, ~~TPS65988~~ (NRND), SoC-native PD | docks, laptops, monitors, Thunderbolt devices | ~$15–40+ |

## Notes and real teardown references per rung

**1–2 (dumb 5 V).** The floor. A TP4056 clone + a USB-C receptacle with two 5.1 kΩ CC pulldowns.
No power path (battery-in-the-path), 5 V only. This is what most sub-$20 gadgets and toys ship —
and it's exactly the topology you must *not* copy for a run-while-charging product (see
`architecture-and-power-path.md`). Cautionary tale: **Raspberry Pi 4** launched with the two CC
pins tied to a *single* shared resistor — e-marked cables detected it as an audio adapter and
refused to power it; fixed in a later board rev with two separate resistors. A textbook example of
why CC termination isn't "just a pulldown."

**3 (power path, 5 V).** Add a real NVDC charger with a SYS node and you get run-while-charging and
instant-on while staying 5 V-only and cheap. Low-end smartwatches and fitness bands live here.
This is the minimum-viable *product-grade* topology when 5 V input suffices.

**4–5 (PD sink, no firmware).** When the device needs >5 V in but nobody wants a PD stack:
**STUSB4500** (negotiates up to 100 W autonomously) or a fixed **trigger** (HUSB238/CH224K) feeding
a charger. Ubiquitous in DIY and mid-volume industrial gear. Transparent to the OS — looks like a
plain higher-voltage supply.

**6 (kernel-managed, Android/Linux).** The sweet spot for an OS-driven device: a mainline-supported
Type-C PHY (**FUSB302**, or NXP **PTN5110** on i.MX designs) with the Linux **TCPM** stack doing PD,
plus a power-path charger with a `power_supply` driver (BQ2589x, or the BQ24250 in bob-929). The OS
owns role-swap, orientation, and battery reporting with no out-of-tree code. **This is where the
bob-929 toy belongs** — 1S, ~3.3/3.6 V, Android on i.MX 8, charge-in + optional low-current 5 V
source, no Alt Mode in the base design. See `android-and-safety.md`.

**7 (power-bank SoC).** A whole category worth knowing: single chips like **Injoinic IP5306**
(charge + boost + one-button, no PD) and the newer bidirectional **IP2365/IP2366** or **Southchip
SW6306** (buck-boost + PD source *and* sink + gauge, 65–100 W) run essentially every USB-C power
bank. Astonishingly cheap for what they do because they're high-volume and purpose-built. If your
device is battery-in / power-out shaped, one of these can replace a charger + boost + PD controller
with a *single* part. Downside: fixed feature set, thin English docs, less OS visibility.

**8 (phones).** Mainstream smartphones fold charging into the main **PMIC** and pair it with a
discrete or PMIC-integrated **TCPC**. High integration, high NRE — only makes sense at phone volume.

**9 (single-port + Alt Mode).** The first rung where video-over-USB-C appears: a full single-port
controller (TPS65987D / **CCG6SF**) driving a DP/USB3 mux. Game handhelds and tablets with display
output. Per teardowns, the **Nintendo Switch** is near here — a PD/charger combo (M92T36-class), a
**BQ24193** charger, and a USB/DP mux (P13USB) to drive the dock's HDMI. This is the tier the
bob-929 *experimental DisplayPort variant* would touch — and only that variant.

**10 (laptop-class).** Multi-cell (2–4S) buck-boost charging (**BQ25792/98** or **BQ25703** with an
EC) plus PD. Laptops, big tablets, portable power stations. **Framework laptop** and **Steam Deck**
class: per-port PD controllers + a buck-boost charger managed by an embedded controller.

**11 (dual-port / Thunderbolt / docks).** The top: dual-port controllers (**Infineon CCG6DF/CCG7D**;
the older **TI TPS65988** is here but NRND), or PD handled by the host SoC itself, plus retimers for
Thunderbolt. Docks, monitors, laptops. Maximum capability, maximum cost and layout risk — and, per
the single-port-first principle, the tier to *avoid* unless two ports genuinely must be co-managed.

## OEM & teardown case studies (sourced)

Real chip choices from shipping products and vendor reference designs. Where a product publishes
schematics or has a well-documented teardown, it's the best "OEM data" you'll get — copy the
proven pattern.

- **NXP i.MX 8M Mini/Plus EVK** (rung 6, *directly applicable to bob-929*). The i.MX 8M EVKs
  expose Type-C ports where **PD is realized with the NXP PTN5110 TCPC PHY** talking I2C to the
  SoC's kernel **TCPM**; out of the box one port is power-only and one is USB-data-without-PD.
  This is NXP's own reference for "how you do USB-C on an i.MX 8," and it validates the
  kernel-managed-port path (PTN5110/FUSB302 + TCPM) as the vendor-blessed pattern for this SoC.
  Reference: NXP PTN5110 product page + i.MX 8M EVK docs and the OM13587 PTN5110 demo kit.
- **Raspberry Pi 4** (rung 1, *cautionary tale*). Launched with both CC pins sharing **one** 5.1 kΩ
  resistor instead of one per pin; e-marked cables then saw a ~836 Ω network and read the Pi as an
  audio adapter, delivering 0 V. Fixed in a later board rev with two separate Rd resistors. The
  authoritative writeup is Benson Leung's "How to design a proper USB-C power sink (hint: not the
  way Raspberry Pi 4 did it)" — **required reading before you place CC resistors.** Lesson: even
  the simplest Tier-0 sink has exactly one way to terminate CC correctly (separate 5.1 kΩ per pin).
- **Nintendo Switch** (rung 9). Per iFixit/repair teardowns: a **M92T36** USB-C power/charge-control
  IC (negotiates with the dock, ~6 V native limit), a **TI BQ24193** battery charger, and a
  **PI3USB/P13USB** USB2+DP mux to drive the dock's HDMI. A battery handheld that adds video-out
  through a mux only when docked — structurally analogous to bob-929's *experimental* DP variant.
- **Steam Deck** (rung 10). Per iFixit Chip ID / Repair Wiki: a **Maxim (ADI) MAX77958** USB-C PD
  controller paired with a **MAX77961** USB-C charging IC (a single-vendor PMIC-style pairing), plus
  MPS VRMs. Shows the "one vendor's PD + charger family" approach at the handheld-PC tier.
- **Framework Laptop** (rung 11). Uses **Infineon EZ-PD CCGx** PD controllers (CCG6 → **CCG8** on
  Laptop 16, PD 3.1 up to 180/240 W) and publishes partial schematics for the DIY community. Confirms
  Infineon CCGx as the live, actively-supported high-end PD-controller line — the family this skill
  points to whenever a full controller is genuinely required.
- **Source-side contrast — Google Pixel 18 W charger** (not device-side, for reference). Teardowns
  show a Weltrend **WT6630P** integrated PD *source* controller. Useful to know the source end of the
  cable, but the *device* side is the PMIC + TCPC inside the phone, not this chip.

Sources: NXP PTN5110 / i.MX 8M EVK docs; Benson Leung, "How to design a proper USB-C power sink";
iFixit Nintendo Switch & Steam Deck teardowns / Chip ID; Infineon–Framework CCG8 announcement;
ChargerLab Pixel charger teardown.

## How to use this ladder

Find the lowest rung that meets your requirements and copy its pattern. Climbing a rung should be
forced by a *requirement* (need >5 V, need Alt Mode, need multi-cell), never by reflex. For
bob-929: the requirements (1S, low power, 5 V-in-enough, Android, toy-safe, Alt Mode
experimental-only) land squarely on **rung 6**, with a **rung-7 power-bank SoC** worth a look only
if the bill of materials needs to shrink further and OS-level control of charging can be sacrificed.
