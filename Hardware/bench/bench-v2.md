# V2 bench — definition

V2 = V1 + **hardware modifications and product-representative connectors/modules** that V1 can't do.
It's where product audio, the mic array, camera, and the automated CI-lab come online. V1 framing in
`bench-v1.md`; product pin allocations in `bob.yaml` / `929-faceboard.yaml`.

## What V2 adds over V1

1. **SOUND/SUPERVISOR connector + module** (SND_MOD-style) — the key unlock. Carries the ENET pads so
   they route **eth XOR SAI7-speaker**, plus the **SAI5 mic array** and the **MSP430 supervisor**.
   Enables product-representative audio that V1 structurally can't:
   - **Stereo speaker @ 1.8 V on SAI7** — the product's actual output SAI + level.
   - **5-way mic array @ 1.8 V on SAI5** — independent digital MEMS mics (see the chipset decision).
   - The ENET-or-Sound XOR (V1 has ENET committed to M7↔PC, so it can't express this).
2. **P21 audio hardware mods** (optional, if reusing the carrier for 1.8 V audio) — lift the WM8731
   (U10) to clear the codec + ADCDAT contention, and/or **bypass the `I2S_LS_OE` level shifter** to
   bring P21 SAI3/SAI5 down to 1.8 V. *Verify the shifter part/topology first.*
3. **Camera modules** — MIPI-CSI on the FPC connectors (P11/P22/P49/P45) + the ISP/NPU vision
   pipeline. The device's actual purpose (`camera-connectors` skill).
4. **RPi CI-lab supervisor** — a Raspberry Pi driving the bench over `thepia hwd` for **unattended
   HIL**: power control (hard-reset backstop — roadmap A4), the gated `bench-hardware` environment,
   the `stem/hil.yml`-style build+test gating (roadmap B3).
5. **More breakouts** — the mic-array module, speaker amp, camera, and product-representative sensors.

## Depends on

- **Track M** (M7 platform) — M7-owned audio / ENET / supervisor.
- **Track R** (radio) — nRF module on ECSPI2 (`BLE_MOD`).
- The **product audio chipset decisions** (mic-array parts + speaker amp — independent MEMS mics +
  separate amp, NOT a single codec).

## Boundary

V2 is the last **carrier-based** stage that de-risks the product. Full 929-faceboard bring-up is
product hardware, not a bench; once the faceboard exists, HIL moves onto it.
