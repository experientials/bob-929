### Stem MSG

The MSG pin uses a 1-Wire ASYNC protocol compatible with UARTs. 
The protocol is used for slave MCUs to send notifications and requests to the current master MCU.

The main challenge is to settle on wiring between the MCUs. According to [onewire-over-uart](https://github.com/dword1511/onewire-over-uart) if the host has open-drain UART you can simply tie TX and RX together. However since MSP430 doesn't seem
to have open drain, perhaps the transistor setup is the best way to go.

The MCUs that must be connected on the Stem MSG bus is

- i.MX8 SoM UART1
- Raspberry Pi GPIO header on ?
- Faceboard MSP430 FR2032
- SmartCam MSP430 FR2355
- SmartCam RP2040
- m.2 module MCU

