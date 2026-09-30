# Datasheet & dev-resource index (bob-929 hardware)

Canonical home for chip datasheets, board user guides, and reference docs. Save resources here (and
mirror firmware-relevant ones into `stem/datasheets/`). Skills reference this index:
`msp-fw-dev`, `prove-firmware-on-hardware`, `msp430-macos-dev`.

| File | Doc | Covers | Key facts we rely on |
|---|---|---|---|
| `msp430fr2355.pdf` | MSP430FR235x/FR215x datasheet (Rev. D) | FR2355/FR2155 chip: memory map, pin-mux, peripherals | FR2355: 32 KB code FRAM `0x8000–0xFFFF`, **4 KB RAM** `0x2000–0x2FFF`, 512 B info FRAM `0x1800–0x19FF`. UCA0=P1.6/P1.7, UCA1=P4.2(RXD)/P4.3(TXD), UCB0 I2C=P1.2/P1.3, UCB1 I2C=P4.6/P4.7. **Timer_B only** (no Timer_A). id=0x01ff. |
| `slau680-msp-exp430fr2355-launchpad.pdf` | MSP-EXP430FR2355 LaunchPad user guide (SLAU680) | The FR2355 LaunchPad board: eZ-FET, isolation jumpers, backchannel | **⚠ §2.2.4: the eZ-FET backchannel UART is on `eUSCI_A1`** (target side) — NOT A0 like the FR2476 LaunchPad. Cost a long silent-console detour (2026-09-25). Grove connector = P1.1/P1.4. |
| `msp430-family-ug-slau144j.pdf` | MSP430x2xx family user guide (SLAU144) | Core/peripheral programming reference | eUSCI/CS/timer register semantics. |
| `msp430-bsl-slau319ae.pdf` | MSP430 BSL user guide (SLAU319) | Bootloader (BSL) over UART/I2C | Ties to the SoM-reflashes-MSP root-of-trust path. |

## Related (elsewhere in the tree)
- `stem/datasheets/`: `msp430fr2422.pdf`, `msp430fr2433.pdf`, `msp430fr2476.pdf` (+ a copy of
  SLAU680), `slau445i` (FR2xxx family UG), `slau550ab` (FRAM BSL).

## Hard-won lessons (don't re-learn)
- **Backchannel UART module differs per LaunchPad:** FR2476 LaunchPad = **eUSCI_A0**;
  FR2355 LaunchPad = **eUSCI_A1** (SLAU680 §2.2.4). Porting diag/prod between boards must switch the
  UART peripheral + pins, not just the PAC. See `stem/diag/FR2355-SCOPE.md`.
