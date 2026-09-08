# MCM vs UCM Pinout Comparison task

> Deferred — do in a dedicated session. This is a pin-by-pin diff against the existing 2022 UCM
> design, not a quick check.

## Aim

The 929 Faceboard pin design was done in 2022 against the **Compulab UCM-iMX8M-Plus**. We are
considering the smaller/cheaper **Compulab MCM-iMX8M-Plus** to reduce module size and cost (other
vendors' i.MX 8M Plus modules — Variscite, Toradex — were ruled out as too big and too expensive,
and Compulab + Yocto/Linux is the committed stack; Android was dropped as Compulab does not ship a
maintained Android BSP for the Plus).

Smaller modules expose fewer pins. Before switching to the MCM we must confirm it still breaks out
**every signal the UCM design and the injector/supervisor architecture depend on**, and produce a
migration delta for anything that moved or is missing.

## Baseline: the existing UCM 2022 pin design

The UCM mapping lives across:
- [929-MODULE.md](./929-MODULE.md) — carrier derived from the SB-UCMIMX8PLUS ref board
- [929-DEVICE-TREE.md](./929-DEVICE-TREE.md), [929-BOM.md](./929-BOM.md)
- `../pinouts/*.md` — connector/pin maps (T-USB 50-pin, M.2 Key B, debug breakout, GPIO/I2C expanders)
- `../sys/*.md` — I2C busses, SYS/STEM messaging
- KiCad schematics under `../292/292-power/` and the 929 design
- UCM reference: `./datasheets/i.MX8/sb-ucmimx8plus_1v1/` and `../refs/Compulab/DESIGN_GUIDELINES.md`

## What to produce

1. Pull the **MCM-iMX8M-Plus reference guide / pinout** and enumerate its exposed signals.
2. A **pin-by-pin diff** of MCM-exposed signals vs the UCM mapping above.
3. Flag every UCM signal that is **not exposed / moved / renumbered** on the MCM.
4. A go/no-go recommendation: MCM (with migration deltas) vs stay on UCM.

## Must-verify pin budget (acceptance criteria)

The MCM must simultaneously expose all of the below, or the switch is blocked / requires rework:

**Injector / supervisor (see architecture below):**
- A **UART routable to the Cortex-M7 domain** → MSP430 **UART BSL** (program + verify). Fallback:
  I2C-BSL if no M7-assignable UART.
- **GPIO on banks that can be assigned wholesale to the M7** → nRF **SWD** (SWDIO/SWCLK) + MSP430
  **RST/TEST** for BSL entry. Avoid pins scattered across banks Linux also needs (bank-level RDC
  ownership / RMW hazard).
- **USB dual-role / OTG brought to the USB-C connector** → i.MX ROM **SDP** (`uuu`) recovery + the
  phone-facing USB gadget. Must enumerate for SDP **firmware-free** (passive CC `Rd` + a working
  cable orientation) so a blank/bricked MSP430 (the PD/CC controller) can't lock out i.MX recovery.

**Core product (from README / 929-MODULE):**
- **2× 2-lane MIPI CSI-2** (stereo cameras) — P3/P4.
- **SYS / STEM / sensor I2C busses** (I2C3, I2C5, I2C6, SYS).
- Anything else the UCM design routes that the product needs: Ethernet, I2S sound, HDMI, PCIe (if
  used), power-control lines, the RPi-compatible header.

## Architecture context (why the injector pins matter)

Settled this session: single external interface (**USB-C → i.MX SDP**), single custom injector
(**i.MX**). The **M7 runs the RTOS supervisor + satellite injection** (MSP430 via UART BSL, nRF via
SWD bitbang with OpenOCD `linuxgpiod`); the **A53 cluster runs Yocto Linux**. Injection tooling
(`openocd`, `mspdebug`, `libgpiod`, `uuu`) is baked into the Yocto rootfs. Linked work:
[FIRMWARE-SUPPORT-TASK.md](./FIRMWARE-SUPPORT-TASK.md), [SoM programming in 929-MODULE](./929-MODULE.md#programming-the-board),
[msp-fw STEM-MSG](../sys/STEM-MSG.md).

## References

- Compulab UCM-iMX8M-Plus: https://mediawiki.compulab.com/w/index.php?title=UCM-iMX8M-Plus_NXP_iMX8M-Plus_Yocto_Linux
- Compulab MCM-iMX8M-Plus: https://www.compulab.com/products/computer-on-modules/mcm-imx8m-plus-nxp-i-mx-8m-plus-som-system-on-module/
- meta-bsp-imx8mp (Yocto, both modules): https://github.com/compulab-yokneam/meta-bsp-imx8mp
