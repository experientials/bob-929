# Product Constraints: Android Compatibility & Children's-Toy Safety

Two product-level constraints that change *which chips you pick*, independent of the electrical
tiers. Read this early — they can veto an otherwise-fine part. Grounded in the bob-929 case: an
i.MX 8-class SoM running a variant of **Android**, powered from a **single 1S cell at ~3.3/3.6 V**
(not 5 V), at modest sustained power, in a **children's toy** that must never run hot.

## Android / mainline-Linux driver support is a first-class selection axis

The device runs Android on an i.MX 8. That means the USB-C front end must be visible to the
Android/Linux kernel through its **standard frameworks**, or you're writing and maintaining
out-of-tree drivers forever. Prefer parts with an **existing mainline kernel driver**. Concretely:

### Type-C / PD side — pick a TCPM-friendly part
Linux manages Type-C/PD through the kernel **TCPM (Type-C Port Manager)** + **TCPC** driver model.
Parts with mainline TCPC/PD drivers:
- **onsemi FUSB302** (`fusb302.c`) — the canonical kernel TCPC PHY; TCPM does the PD policy in the
  kernel. Best-supported "managed port" option and commonly used on i.MX 8 designs. If you want a
  fully OS-managed Type-C port (role swap, PD in kernel), **this is the Android-friendly choice** —
  and it's cheap silicon. The firmware cost from `pd-and-cc-controllers.md` largely goes away
  because *Android's kernel already is the PD stack*.
- **NXP PTN5110** (TCPCI-compliant, generic `tcpci.c`) — NXP's own TCPC, used on i.MX 8M EVKs.
  Native fit with NXP's BSP; a safe bet on an NXP SoM.
- **TI HD3SS3220** (`hd3ss3220.c`) — Type-C **orientation/DRP only, no PD**. Perfect companion for
  the Tier-0 "5 V only, no PD" architecture: it gives Android clean Type-C attach/orientation/role
  events without a PD engine.
- **Richtek RT1711H / RT1715**, **TI TPS6598x** (`tps6598x.c`, status/notify for the on-chip PD
  engine) — also mainlined if you go that route.
- **STUSB4500** is *autonomous* — it negotiates before the OS is even up and looks like a plain
  5–20 V supply to Android. That transparency is a feature: no driver needed, dead-battery-correct.
  Downside: the OS can't *control* the contract at runtime.

**Takeaway:** for an OS-managed port on Android, **FUSB302 (or PTN5110) + kernel TCPM** is the
sweet spot — Android-native, cheap, no on-chip firmware to license. For a dumb charge-in port,
**STUSB4500** (if >5 V) or plain resistors + **HD3SS3220** (if 5 V) keep the OS out of it.

### Who owns the port: the kernel, or the low-power core?

There's a real fork here, and it trades OS-integration against standby power:

- **Kernel owns the port (FUSB302/PTN5110 + TCPM).** Android natively manages PD, role-swap,
  orientation, and battery via its standard frameworks — zero glue. **But the SoM must be running
  to manage the port.** Charging still happens (a power-path charger is autonomous), yet role
  management and any PD are dormant while Android is off.
- **Low-power core owns the port (MSP430 controls charger + CC + power-path + wake).** The device
  can charge, detect attach, and **wake the SoM on plug-in with Android fully powered down** —
  lowest standby current, instant port response, no dependence on Android boot for basic function.
  This is the "control all things with the low-power core" architecture, and for a deep-sleep
  battery toy it's usually the better call. It works cleanly because the **data plane still goes to
  the SoM** — the low-power core owns only the *management plane*.

The low-power-core path is easy precisely in the **Tier 0/1, 5 V, no-PD** world: the MSP430 only
runs a Type-C CC state machine (attach / detach / orientation / current advertisement), which is
small, plus the charger's I2C. A full PD *policy* engine on an MSP430 is possible but heavy — if
you need PD, prefer an autonomous part (STUSB4500) that the MSP430 merely supervises over I2C, and
leave DP Alt Mode (which needs a VDM engine) to a dedicated controller on the experimental variant.

### Making Android still "see" the port when the low-power core owns it

Choosing low-power-core ownership does **not** blind Android — you bridge two things, both standard:

1. **Battery / charging state → the charger's own `power_supply` driver.** The charger IC is a real
   I2C device. Let Android's mainline `power_supply` driver (e.g. `bq24257_charger.c` for the
   BQ24250) read it so the battery UI, charge control, and thermal throttling work. Because the
   MSP430 also talks to that charger, arbitrate the I2C bus: either the MSP430 is the sole master
   and *proxies* status to the SoM, or use a two-master/segmented-I2C scheme with non-clashing
   addresses. The bob-929 design already anticipates this ("Power I2C bridged onto SYS I2C, take
   care not to clash on addresses").
2. **USB data role → an ID / VBUS-detect GPIO into the SoM.** This is the classic, pre-Type-C
   pattern and it still works: the MSP430 senses CC to decide "a host (PC) is attached — become a
   USB device" vs "act as host," and signals the SoM's USB-OTG controller via the ID/VBUS-detect
   GPIO. Android's USB gadget stack switches device/host (ADB, MTP, etc.) off that GPIO — no TCPC
   required. The high-speed D± simply route to the SoM through the orientation mux.

Net: the low-power core owns the management plane; Android sees battery via `power_supply` and USB
role via a GPIO. You give up the kernel *managing PD* (which you don't have in the no-PD design
anyway) in exchange for a device that manages its port while asleep. For bob-929 that's a good
trade.

### Charger / fuel-gauge side — use `power_supply`-class parts
Android surfaces battery/charging state through the kernel **`power_supply`** class. Pick a
charger with a mainline `power_supply` driver so the battery UI, charge control, and thermal
policy work out of the box:
- **BQ24250** → covered by `bq24257_charger.c` (bq24250/24251/24257). *The bob-929 charger already
  has a mainline driver* — a real point in its favor for Android.
- **BQ25896/BQ25890** → `bq25890_charger.c`. **BQ2560x/61x** → `bq256xx_charger.c`.
  **BQ25792/BQ2579x** → `bq2579x`/newer drivers. All mainlined.
- Fuel gauges: **MAX17048** (`max17040_battery.c`), **BQ27xxx** (`bq27xxx_battery.c`).

Verify the *specific* part and register map against the kernel version your Android BSP ships —
driver coverage varies by kernel. But staying inside these families means Android's battery
stack, charging thermal throttling, and `dumpsys battery` all just work.

## Children's-toy safety — the hard limits

A toy is one of the most safety-regulated product classes. This constrains the power design more
than any electrical spec. Design to it from day one; it's not retrofittable.

### Standards you're designing toward (confirm the exact set with a compliance house)
- **EN 71** (EU toy safety) — esp. **EN 71-1** (mechanical/physical) and **EN 71-2** (flammability).
- **IEC/EN 62115** — *electric* toys: covers temperature rise, abnormal operation, battery faults.
- **ASTM F963 + CPSIA** (US toy safety).
- **IEC 62133-2** (Li-ion cell/pack safety), **UN 38.3** (battery transport).

### What that means for this circuit
- **Surface temperature.** Accessible surfaces must stay cool to the touch — plan for roughly
  **≤ 48 °C on metal / ≤ ~60 °C on plastic** accessible parts (confirm exact limits for your
  standard/age grade). This is the dominant thermal constraint, tighter than any chip's ratings.
- **The worst-case thermal event is running WHILE charging** — charger dissipation *plus* SoC
  dissipation at the same time, exactly the mode you require. Budget for it: keep the charger,
  inductor, and any hot SoC rails away from accessible surfaces, spread heat into copper, and
  **limit charge current** so skin temperature stays in bounds even at full load. The fact that a
  single 18650 can't sustain 3 A helps you here — sustained power is inherently modest — but the
  transient/charging overlap still governs placement and current limits.
- **JEITA thermal charging is mandatory**, not optional: NTC on the pack, charger with a TS input,
  reduce/stop charge when hot or cold. Several bob-929 candidate cells have embedded thermistors —
  use them. (See `chargers-and-cells.md`.)
- **Battery safety & abuse:** protected cell/pack, robust to drop/crush (kids), no user-accessible
  battery — a **screw-secured battery compartment** is a toy-standard expectation. Keyed/asymmetric
  battery connectors so the pack can't be inserted reversed (the 292 docs already call for this).
- **1S, low voltage is your friend.** Running the SoM from a ~3.3/3.6 V (1S) rail rather than a
  boosted 5 V means less conversion loss, fewer hot nodes, and a simpler safety story. Only the
  (optional, experimental) host-source port needs a boost to 5 V, and it's low current.
- **No high accessible voltages.** VBUS can be 5 V max on this design if you take the no-PD path;
  keep any higher rails internal and protected.

## How these two constraints steer the bob-929 decision

Combined with the low-power / 1S / 5 V-in-is-enough reality:
- **Sink/charge-in port:** BQ24250 (has a mainline `power_supply` driver) + Rd. Add HD3SS3220 if
  you want Android to see clean Type-C attach/orientation without PD. No PD controller.
- **Host/source port (when present):** resistor source + 5 V boost + USB2 mux, low current.
- **DisplayPort:** experimental-only, debug/basic-screen use for the i.MX 8 — keep it a
  **populate-optional** sub-circuit on a variant, never a driver of the base architecture. If a
  variant needs it, that's the *only* place a single-port Alt-Mode controller (CCG6SF) earns its
  place; the base toy ships without it.
- **Firmware:** since it's Android, prefer the kernel to own the port (FUSB302/PTN5110 + TCPM)
  rather than an MSP430 PD stack — the MSP430 stays for low-level supervision/wake, not PD.
