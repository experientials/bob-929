# Bench validation spikes (pinmux model → silicon)

Live-hardware validation of allocations in this model — the "check.py for silicon" idea from
`ucm-dev/references/devicetree-config.md`. Each spike is a DT variant on the **SB-UCM bench carrier**
that mux/enables an interface, with a verify ladder and a revert. The **mechanism/runbook** lives in
the skill (`devicetree-config.md`); the **plan + status + results** live here (plans are not in skills).

Board access, the spike loop (pull live dtb → decompile → edit → recompile → overwrite on
`mmcblk2p1` → reboot → revert from backup), and the `fw_setenv`-is-broken caveat: see
`ucm-dev/references/devicetree-config.md`.

---

## SPIKE-1 (IN PROGRESS, started 2026-09-20): free P21.11–23 from the WM8731 codec

**Question.** Can we take *software-only* control of P21.11–23 (the SAI3 pads = the SAI5 mic-array
lines) despite the on-carrier **WM8731 codec (U10)** being galvanically wired to those same nets?
Ties to C7 (mic array = SAI5 RX on P21.11–23) and the M7-owns-audio plan.

**Key fact (verified 2026-09-20).** Of the seven nets, **only P21.17 (SAI3_RXD = WM8731 ADCDAT) is a
codec *output*** → the sole electrical contender; the other six are codec inputs (harmless loads). The
WM8731 `simple-audio-card` doesn't even register an ALSA card here, and its driver (`wm8731` at
`i2c-1` 0x1a) is bound-but-idle. So the fix is software: release the codec + re-mux the pads. Muxing
alone does **not** disconnect the codec (same copper) — releasing/parking ADCDAT is what matters.

**Success criteria.**
1. `wm8731` unbound → 0x1a no longer `UU` on `i2c-1`; no `wm8731` bind in `dmesg`.
2. SAI3 pads claimed by our test group in `/sys/kernel/debug/pinctrl/30330000.pinctrl/pinmux-pins`.
3. **P21.17 drives a clean 0 / 1.8 V at the header** (multimeter) → codec ADCDAT is high-Z → the pins
   are ours in software, **no board mod**.

**DT variant** (built on the *currently booted* `ucm-imx8m-plus-usbdev.dtb`, which already carries the
I²C3 + UART4 spikes — preserve those):
1. `/sound` (simple-audio-card) → `status = "disabled"`.
2. WM8731 codec node (child of `i2c@30a30000` @0x1a) → `status = "disabled"`.
3. Re-mux the 7 SAI3 pads (P21.11–23) → **GPIO** in a test pinctrl group (values from
   `imx8mp-pinfunc.h`). GPIO is the test function: it proves electrical control with a multimeter and
   directly tests the ADCDAT contention.

**Verify ladder.**
- **V1 software:** `i2cdetect -y 1` (0x1a not `UU`); `dmesg | grep wm8731` (empty); `pinmux-pins`.
- **V2 electrical (needs multimeter):** `gpioset` each pad hi/lo, measure at the header. **P21.17 is
  the critical one** — HIGH ≈ 1.8 V, LOW ≈ 0 V = clean = ADCDAT high-Z. Mid-rail/stuck = contention.
- **V3 (later):** flip the group GPIO → SAI5, confirm SAI5 claims the pads; real mic capture when mics
  are wired.

**Rollback.** Restore `…usbdev.dtb.orig`, reboot.

**Escalation if V2 fails.** Single-pin lift of **U10 (WM8731) ADCDAT** — bench-only; the product has
no WM8731.

**Board access.** Via `thepia hwd exec "<cmd>"` (daemon owns the port, auto network-or-serial). Do
NOT raw-`ssh`/open `/dev/cu.*` — after a reboot eth0 DMA-races down and the daemon holds the serial;
`thepia hwd exec` still works. See `ucm-dev/references/console-access.md`.

**Status / results.**
- [x] variant built — `live-mod.dtb` md5 `02cc4659…`; edits round-trip-verified (wm8731 & sound
  `disabled`, `p21gpiotestgrp` w/ 7 SAI3 pads → GPIO, iomuxc `pinctrl-0=<0x1a 0xa0>`).
- [x] deployed + rebooted — live dtb on `mmcblk2p1` now `02cc4659…`; **backup**
  `ucm-imx8m-plus-usbdev.dtb.pre-spike1` = `4dbf491b…` (the I²C3+UART4 state) for revert. Board boots
  the variant cleanly (model = usbdev).
- [x] **V1 software VERIFIED (2026-09-20):** `i2cdetect -y 1` shows 0x1a as plain `1a` **not `UU`**
  (WM8731 driver unbound); `dmesg | grep -c wm8731` = **0**; all 7 SAI3 pads report
  `30330000.pinctrl … function pinctrl group p21gpiotestgrp` (HOG) in `pinmux-pins`; prior spikes
  intact (`i2c-2` + `/dev/ttymxc3`).
- [x] **V2 done (2026-09-20) — uncovered a MODEL ERROR, not a clean pass.** Multimeter at the header
  (P21.17=gpio126, P21.11=gpio129, P21.15=gpio130): driving the 1.8 V SoC GPIO **HIGH → P21.11/.15 read
  3.3 V**; LOW → 0 V (they follow the drive); **P21.17 STUCK at 0 V both ways.** Reads as: (a) **mapping
  correct** — 11/.15 track the drive and schematic p6 confirms P21.11=SAI3_TXD, .15=SAI3_MCLK,
  .17=SAI3_RXD; (b) the header is a **3.3 V, level-shifted, codec+M.2-shared bus** — WM8731 (U10) @3.3 V
  + 3.3 V pull-ups + I2S shifter (`I2S_LS_OE`) + TXB0104 (U14) — **NOT the "raw 1.8 V" the model
  claimed** (corrected in `boards/sb-ucm-carrier.yaml`); (c) **P21.17 = confirmed WM8731 ADCDAT
  contention** — software can't tri-state the powered codec's output.
- **CONCLUSION: P21.11–23 is NOT a usable clean 1.8 V I²S mic header on this bench.** A 1.8 V mic here
  sees 3.3 V and fights the codec (esp. ADCDAT/P21.17). Making it work is **hardware** (3.3 V parts +
  lift U10 ADCDAT + handle the shifter), not software. The **product** (929 faceboard) routes SAI5 mic
  on its own P1 balls, not through this carrier codec/shifter — so the product isn't bound by this.
  Bench mic-array validation needs a different path — revisit C7. gpio map (kept for reference):
  RXFS/.23=124, RXC/.19=125, RXD/.17=126, TXFS/.21=127, TXC/.13=128, TXD/.11=129, MCLK/.15=130.
- [x] **V2b — actual I²C codec power-down (2026-09-20, follow-up).** V1 only *unbound the driver*; it
  never commanded the chip. This closes that gap: wrote the WM8731 control regs directly on `i2c-1`
  @0x1a (driver unbound, no `-f` needed) — **R9 Active Control → INACTIVE** (`i2cset -y 1 0x1a 0x12 0x00`,
  should tri-state ADCDAT) then **R6 Power Down → full incl. POWEROFF** (`i2cset -y 1 0x1a 0x0C 0xFF`).
  Both ACKed (`rc=0`). Observation via SoC GPIO input on gpio126/P21.17 (sysfs, no libgpiod on board):
  **baseline `0` → after R9 inactive `0` → after R6 power-down `0`.** So a *commanded* full power-down
  of the codec does **not** release ADCDAT as seen by the 1.8 V SoC input — the "software can't clear
  it" conclusion is now **earned, not assumed**. **Ambiguity left for the meter:** SoC-read `0` = either
  (a) codec/TXB0104-U14 still actively holds the net low → hardware lift of U10 ADCDAT confirmed
  necessary, or (b) codec released but the net has no strong pull to read as `1` on a 1.8 V input.
  Distinguish by measuring P21.17 with the codec commanded off (this V2b state). WM8731 ctrl regs are
  **write-only** → no register readback; electrical measurement is the only confirmation.
- [x] **Measured 2026-09-20: P21.17 = 0.00 V with codec commanded off** (multimeter). Hard 0 V, not
  floating → the codec **actively holds ADCDAT low**; software path is exhausted. Freeing it needs
  U10 removed/isolated (**hardware, V2**). **No solder-jumper/`E`-link or power-enable exists for U10**
  on the carrier (sheet 5 verified): power is hard-wired off `3V3_PER`, control is I²C-only, and
  ADCDAT (U10 pin 10 → SAI3_RXD) is a direct net with no series R. U10 is QFN (exposed pad, pin 29) →
  no single-pin lift; it's a trace-cut or whole-part removal. Compulab support draft raised: ask for a
  **codec-DNP carrier build** to avoid rework.
- **BENCH IMPACT (see `bench-v1.md`):** the split is by **direction** — **SAI3 TX/output (speaker amp
  on P21.11/.13/.21) works on unmodified V1**; **SAI3 RX/input (any mic ADC on P21.17) is blocked**.
  So **SPIKE-2 (analog mic array) is NOT benchable on an unmodified carrier** — it requires the U10
  surgery (V2). Output-only audio validation is fine on V1.

**Revert if needed:** `thepia hwd exec "cp …/ucm-imx8m-plus-usbdev.dtb.pre-spike1 …/ucm-imx8m-plus-usbdev.dtb && sync"` then `thepia hwd reboot` (hold a lease first).

---

## SPIKE-2 (PLANNED): analog mic-array validation on SAI3 — the analog-vs-MEMS tiebreaker

**Question.** Do **differential, equal-length 10 cm** analog mic runs into a multi-channel TDM ADC
give clean, phase-matched channels good enough for beamforming — **in the real EMI environment (nRF
radio + a motor running)?** This is the one risk that could flip the analog-default decision
(`audio-architecture.md`) to the MEMS fallback.

**Setup.**
- **TLV320ADC5140** breakout on the **SAI3 bus** — bench = **P21 (3.3 V)**, the WM8731's pins.
  **PREREQ (confirmed by SPIKE-1 V2b): the ADC's data output lands on SAI3_RXD/P21.17, which the
  WM8731 ADCDAT holds low and software cannot release — so this spike REQUIRES the U10 hardware
  removal/isolation (a V2 mod) before it can run. It is not benchable on an unmodified carrier.**
- 2–4 analog capsules on **10 cm matched differential** runs → ADC differential inputs (mic bias +
  PGA from the ADC).
- SAI3 in **TDM RX**; capture all channels (Linux/ASoC first; M7-side once Track M is up).

**Measure.** Inter-channel **noise floor** + **phase/delay alignment**, quiet vs **nRF TX + motor
running nearby**. Optionally a rough GCC-PHAT DoA on a known source.

**Pass/fail.** Matched + low-noise under EMI → **analog confirmed**. Degraded → **MEMS fallback**
(central board + firmware already support both — `audio-architecture.md`).

**Notes.** SAI3/P21 bus, **ENET untouched**; access via `thepia hwd`. Needs the U10 removal (per the
SPIKE-1 prereq above) **and** an ADC5140 on a board; optionally M7 bring-up (Track M) for M7-side capture.

**Sourcing — the ADC5140 has NO hobbyist breakout (2026-09-20).** The **TLV320ADC5140** is a
professional design-in part (32-WQFN, 0.4 mm pitch, careful analog layout) — it is **not** in the maker
canon, so there is **no AliExpress/clone breakout** (those cluster around WM8960/ES8388/PCM5102 and I²S
MEMS mics). Get the ADC5140 onto a board by one of:
- **TI TLV320ADC5140 EVM** — the official eval module (correct layout, mic bias, headers); TI /
  DigiKey / Mouser. The legit "breakout."
- **Spin a JLCPCB/LCSC board** — check **LCSC** for TLV320ADC5140 stock, lay out a small breakout, have
  **JLCPCB** assemble it. The right way to get the *exact* part cheaply.
- **Concept proxy (not the real part):** a **Seeed ReSpeaker 4-Mic Array** (uses the **AC108** 4-ch
  analog→I²S/TDM ADC) — cheap and available; validates the *multi-ch analog → TDM → beamforming*
  concept now, but **not** the ADC5140-specific EMI/noise/phase answer this spike is about.
- **Decision impact:** because the spike's whole point is *the chosen design* under EMI, a proxy
  de-risks but does not close it — the pass/fail needs the real ADC5140 (EVM or JLCPCB board), which
  can be built in parallel with the U10 removal.
