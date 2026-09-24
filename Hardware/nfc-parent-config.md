# NFC parent-tap config channel (product feature to support)

**Status:** design intent (2026-09-21) — a feature bob-929 products **probably want to support**. Detail &
part-choice live in `talkihw/Testy Module/NFC.md`; bench eval in [`bench/`](bench/) (BOM + wiring). This note
records the **product-level intent** and the design constraints so it isn't lost.

## What

A parent taps an **iPhone app** to the toy to **change its mode / settings** — a deliberate, proximity-gated
config action. **Explicitly not BLE pairing:** we keep radio omittable, so this must add **no transmitter to
the toy**.

## How — the polarity that makes it radio-free

The **iPhone is the active radio; the toy is a passive transponder.**

- Toy carries a **dual-interface NFC-to-I²C tag** (NXP **NTAG I²C plus** / ST **ST25DV**): RF side + I²C side
  share memory; **energy-harvesting**; a **field-detect pin (FD/GPO)** wakes the supervisor MCU on tap.
- iPhone (Core NFC **reader**) **writes** a command block over RF → the toy's MCU reads it over I²C and applies
  the mode change. Standard App Store NFC entitlement (**no special Apple deal**). Phone-as-card/HCE is
  Apple-gated → do it **phone-reads / toy-is-tag**.
- The tag sits on the product I²C bus (supervisor/STEM domain); the FD line wakes the always-on MSP430
  (~0.5 µA) so the toy need not be awake to be reconfigured.

## Security — parent-authenticated, anti-replay

- **Tag-enforced write protection** (tag password / AES) — the app holds the secret in iOS Keychain / Secure
  Enclave.
- **MCU-verified command** — a MAC'd blob + monotonic counter/nonce → firmware verifies & rejects stale
  (anti-replay).
- **Physical presence is the outer gate:** ~1–4 cm tap, app foreground → **no remote reconfiguration.**

## Why it fits the product principles

- **Radio-free base SKU preserved:** a *passive* tag is **generally outside RED radio scope** (EU/Eurosmart
  guidance; RED §1.6.3.13) — though **dynamic/dual-interface tags are the ambiguous boundary → verify with a
  Notified Body.** Far lighter than BLE (also dodges the RED 3.3 / CRA cyber regime).
- **No new connectivity obligations** (local, not networked).
- **Combines cleanly** with vision-for-mouth-objects → the whole toy stays transmitter-free while gaining a
  parent-config channel. (If a variant *does* carry an active NFC reader for the mouth, it's already in RED
  scope and this tag adds no regulatory delta.)

## Open decisions

- Part: **NTAG I²C plus** (Type 2 / 14443A) vs **ST25DV** (Type 5 / 15693, mailbox, GPO) — pick on
  wake-handshake need.
- Which config/modes are exposed via tap; key provisioning (per-unit keys?); counter storage in FRAM.
- Confirm the RED passive-tag classification for the chosen dual-interface part with a Notified Body.

## References

- Product NFC choice & the RFID→NFC crypto ladder: `talkihw/Testy Module/NFC.md`
- EU radio/toy regulation: `talkihw/Documents/EU-RADIO-REGULATION.md`; skill `child-toy-regulation`
- Bench eval: [`bench/BOM.md`](bench/BOM.md), [`bench/bench-v1-wiring.md`](bench/bench-v1-wiring.md),
  [`bench/bench-v1.md`](bench/bench-v1.md) (candidate-eval note)
