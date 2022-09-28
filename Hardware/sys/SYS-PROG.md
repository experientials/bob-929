# System Programming

The system can be programmed by the M Core of the i.MX8 module, by the Supervisor module or through the RPi connection.

## SYS-PRG mode

The Expanders are a central for controlling the system, so updating their firmware requires disabling large parts.
The update is done by the SoM or by an external Supervisor without the SoM running(or able to be debugged). 
This means that UART2/4 are not used for debug output while programming the Expanders.

To enable programming SYS_PRG#(GPIO4_17) is set to LOW.


## Switching off

Pins that will not have an effect during programming mode as the voltage level shifters are disabled.

- *_ATT_INT, *_ATT_XSHUT, RIGHT_RESET, RIGHT_PWRDN supplied to camera modules (OE_CAM)
- LEFT_SCL, LEFT_SDA, RIGHT_SCL, RIGHT_SDA (OE_CAM GPIO2_9)
- I2S_1V8_* (OE_SOUND GPIO2_8)

They will be switch off be setting OE_SOUND and OE_CAM low.


## SoM Pins

An 8-bit switch enables the SN74CB3Q3245PW system programming signals driven by SYS_PRG#

|SoM pin| SoM code | Function / counterpoint |
|-------|----------|-------------------------|
| P2.69 | GPIO4_17 | SYS_PRG#                | 
| P1.100| I2C5_SCL | F_SBWTCK                |
| P1.96 | I2C5_SDA | F_SBWTDIO               |
| P1.74 | UART2_TXD| Face Expander P1.1 Data receive |
| P1.76 | UART2_RXD| Face Expander P1.0 Data transmit |
| P1.87 | I2C6_SCL | C_SBWTCK                |
| P1.89 | I2C6_SDA | C_SBWTDIO               |
| P1.86 | UART4_TXD| CAM P1.6 Data receive |
| P1.84 | UART4_RXD| CAM P1.7 Data transmit |

A second switch does the same for the Power Module 

|SoM pin| SoM code | Function / counterpoint |
|-------|----------|-------------------------|
| P1.36 | SAI5_RXD2| T_SBWTCK                |
| P1.26 | SAI5_RXD3| T_SBWTDIO               |
| P1.72 | UART1_TXD| T-USB Expander P1.1 Data receive |  
| P1.19 | UART1_RXD| T-USB Expander P1.0 Data transmit | 


Should the USB 2.0 data also be switched to Host on the SoM?


## The Bus

The SYS I2C can be used to access,

- MSP430/Expanders
- Expander #0
- PMIC Power Chip
- PCIe clock generator
- Real Time Clock

The MSP430/Expanders can be programmed using UART2/4 while in System Programming mode(pin=low).

- Faceboard MSP430 P1.0 P1.1 to UART2
- Faceboard MSP430 mode control via I2C5 pins
- T-USB MSP430 P1.0 P1.1 to UART4
- T-USB MSP430 mode control via I2C6 pins


Faceboard Expander


