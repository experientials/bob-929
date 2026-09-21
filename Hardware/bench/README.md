# Big Bob Bench

*"**bench**" is the basic shorthand (hence `Hardware/bench/`); "**Big Bob Bench**" is the charming nickname.*

> **Location settled (2026-09-21):** lives at **`bob-929/Hardware/bench/`** — a cross-cutting **topic
> dir** under `Hardware/`, peer to `pinmux/`, `stem/`, `testing/`, following the repo's
> `Hardware/<topic>/` convention (compatible with the other branches). The bench is the successor to the
> `Hardware/testing/` Testing-Shim / RPi-probe HIL precedent. Filenames use `pinmux/`'s lowercase-hyphen
> style. The **internal file arrangement may still evolve** in a final alignment pass before merge, but
> the location and naming convention are fixed.

The **Big Bob bench** — a scaled-up Bob-929 prototype with the **carrier boards + MCU dev boards mounted
on the back** — is where we build and run the bench lab. This directory (branch `feat/big-bob-bench`)
is the home for **everything about building and operating the bench**: bench-V1 & V2 definitions, the
physical/practical bench-lab setup, CI hardware, and tech demos.

## Contents

| File | What |
|---|---|
| [`bench-v1.md`](bench-v1.md) | **bench-V1** — the unmodified-carrier bench: its **CANONICAL objectives** (verbatim, source of truth), capability→phase table, level caveats. |
| [`bench-v1-wiring.md`](bench-v1-wiring.md) | **Full pin-connection plan** for bench-V1 — every module & line → named carrier pin, master occupancy ledger, I²C address map, level-shifter parts, USB physical topology. |
| [`bench-v2.md`](bench-v2.md) | **bench-V2** — the hardware-modified bench (camera, U10 rework, more breakouts) + the RPi CI-lab supervisor. |
| [`spikes.md`](spikes.md) | **Bench validation spikes** (pinmux model → silicon): SPIKE-1 (WM8731/ADCDAT), SPIKE-2 (analog mic array), etc. |
| [`BOM.md`](BOM.md) | **Bill of materials** — per-bench parts (boards, shifters, amp, probe, mounting), have/need + phase, derived from the wiring plan. |

## Cross-repo layout (sibling checkouts under `…/Talki/`)

These bench docs **derive from** — but do not contain — the product pin model and firmware, which live
in other repos checked out beside `bob-929`:

- **Pinmux MODEL** (`model.yaml`, `boards/`, `audio-architecture.md`, `challenges.md`): the **ziloo**
  repo → `../../../ziloo/Hardware/pinmux/`. The canonical objectives block in `bench-v1.md` is the source
  of truth; the model is what the wiring is validated against.
- **Firmware planning** (SoM-as-USB-host programmer, image build): **ziloo-firmware** →
  `../../../ziloo-firmware/docs/`.
- **Board-access workflow / roadmap:** the **ucm-dev** skill → `../../../.claude/skills/ucm-dev/`.

Relative links in these files assume that sibling-checkout layout.

## Discipline

Per `../../../.claude/rules/objectives-tracking.md`: the **CANONICAL objectives** block at the top of
`bench-v1.md` is source of truth — capture new objectives there verbatim, drive plans from them, and if
a derived table disagrees, the canonical block wins.
