# System Programming

The system can be programmed by the M Core of the i.MX8 module, by the Supervisor module or through the RPi connection.

## SYS-PRG mode

The Expanders are a central for controlling the system, so updating their firmware requires disabling large parts.
The update is done by the SoM or by an external Supervisor without the SoM running(or able to be debugged). 
This means that SoM UART2/4 are not used for debug output while programming the Expanders.

To enable programming the UART connection SYS_PRG#(GPIO4_17) is set to LOW.

SYS_PRG will,

- Connect UART2, and UART4 to MSP430 chips
- Connect MCLK, RXC, RXD0, RXD3, I2C5, I2C6 connected to SBW on MSP430 chips


## Switching off

Pins that will not have an effect during programming mode as the voltage level shifters are disabled.

- *_ATT_INT, *_ATT_XSHUT, RIGHT_RESET, RIGHT_PWRDN supplied to camera modules (OE_CAM)
- LEFT_SCL, LEFT_SDA, RIGHT_SCL, RIGHT_SDA (OE_CAM GPIO2_9)
- I2S_1V8_* (OE_SOUND GPIO2_8)

They will be switched off by setting OE_SOUND and OE_CAM low.


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
| P1.28 | SAI5_RXD0| F2_SBWTCK                |
| P1.26 | SAI5_RXD3| F2_SBWTDIO               |
| P1.74 | UART2_TXD| Face 2 P1.1 Data receive | 
| P1.76 | UART2_RXD| Face 2 P1.0 Data transmit | 
| P1.30 | SAI5_MCLK| T_SBWTCK                |
| P1.32 | SAI5_RXC | T_SBWTDIO               |
| P1.86 | UART4_TXD| T-USB Expander P1.1 Data receive |  
| P1.84 | UART4_RXD| T-USB Expander P1.0 Data transmit | 


Should the USB 2.0 data also be switched to Host on the SoM?


## The Bus

The SYS I2C can be used to access,

- MSP430/Expanders
- Expander 0x26
- Expander on CAM module
- PMIC Power Chip
- PCIe clock generator
- Real Time Clock

The MSP430/Expanders can be programmed using UART2/4 while in System Programming mode(pin=low).

- Faceboard MSP430 P1.0 P1.1 to UART2
- Faceboard MSP430 mode control via I2C5 pins
- CAM MSP430 P1.0 P1.1 to UART4
- CAM MSP430 mode control via I2C6 pins
(- MSP430 JTAG)


Faceboard Expander


## Firmware update with Debug Connector

The 45 pin debug connector provides access to

- SYS/STEM/POWER I2C
- PD Controller Flash directly
- PD Controller reset/access
- Faceboard MSP430 flashing & JTAG
- Faceboard MSP430 #2 flashing
- Smartcam MSP430 flashing
- Reboot the SoM
- UART for debugging the CORE-M 

The pins are direct so no mode switch is required.


## RPi connector modes

Mode switching GPIO connector can expose a variation of interfaces controlled by the Raspberry Pi(or other device)
to allow accessing more than 40 pins.


Front GPIO

| Left side                  | Function  |Pin |Pin | Function  | Right side           |
|----------------------------|-----------|----|----|-----------|----------------------|
|  When VSOM fully connected | LIVE_3V3  | 1  | 2  | VCC_FULL  | When VSOM fully connected  |
|                  STEM_SDA  | SDA       | 3  | 4  | VCC_FULL  | When VSOM fully connected |
|                  STEM_SCL  | SCL       | 5  | 6  | GND       |                      |
|                STEM_T_nINT | INT       | 7  | 8  | TxD       | UART1 TxD            |
|                            | GND       | 9  | 10 | RxD       | UART1 RxD            |
|                            |           | 11 | 12 | SWD       | SWDCLK for attached  |
|     SDIO DAT3 / GPIO2_IO18 | SDIO      | 13 | 14 | SWD       | SWDIO for attached   |
|      SDIO CLK / GPIO2_IO13 | SDIO      | 15 | 16 | SDIO      | SDIO CMD / GPIO2_IO14  |
|    When any VSOM connected | LIVE_3V3  | 17 | 18 | SDIO      | SDIO DAT0 / GPIO2_IO15 |
| ECSPI2_MOSI / GPIO5_IO11   | MOSI      | 19 | 20 | GND       |                        |
| ECSPI2_MISO / GPIO5_IO12   | MISO      | 21 | 22 | SDIO      | SDIO DAT1 / GPIO2_IO16 |
| ECSPI2_SCLK / GPIO5_IO10   | SCLK      | 23 | 24 | SPI CE0   | ECSPI2_SS0/GPIO5_IO13  |
|                            | GND       | 25 | 26 | SCL       | NIGHT SCL            |
|                    SYS I2C | SYS SDA   | 27 | 28 | SCL       | SYS I2C              |
|                  NIGHT_INT | INT       | 29 | 30 | (GND)     |                      |
|                  NIGHT_SDA | SDA       | 31 | 32 | TxD       | UART3 TX             |
|                   UART3 RX | RxD       | 33 | 34 | CAN1      | CAN1 RX / GPIO4_IO25 (RPi GND) |
|                            |           | 35 | 36 | CAN1      | CAN1 TX / GPIO4_IO22   |
|     SDIO DAT2 / GPIO2_IO17 | SDIO      | 37 | 38 | CAN2      | CAN2 RX / GPIO4_IO27  |
|                            | (GND)     | 39 | 40 | CAN2      | CAN2 TX / GPIO4_IO26  |

The layout is kept mostly compatible with Raspberry 4 allowing emulation and easy comparison.


Back GPIO

| Left side                  | Function  |Pin |Pin | Function  | Right side           |
|----------------------------|-----------|----|----|-----------|----------------------|
|  When VSOM fully connected | 3V3_ON    | 1  | 2  | VCC_FULL  | When VSOM fully connected  |
|       I2C3 SDA / STEM_SDA  | SDA       | 3  | 4  | VCC_FULL  | When VSOM fully connected |
|       I2C3 SCL / STEM_SCL  | SCL       | 5  | 6  | GND       |                      |
|                   STEM_INT | INT       | 7  | 8  | TxD       | UART2 TxD            |
|                            | GND       | 9  | 10 | RxD       | UART2 RxD            |
|                            |           | 11 | 12 | SWD       | SWDCLK for T-USB     |
|     SDIO DAT3 / GPIO2_IO18 | SDIO      | 13 | 14 | SWD       | SWDIO for T-USB      |
|      SDIO CLK / GPIO2_IO13 | SDIO      | 15 | 16 | SDIO      | SDIO CMD / GPIO2_IO14  |
|    When any VSOM connected | 3V3       | 17 | 18 | SDIO      | SDIO DAT0 / GPIO2_IO15 |
| ECSPI2_MOSI / GPIO5_IO11   | MOSI      | 19 | 20 | GND       |                        |
| ECSPI2_MISO / GPIO5_IO12   | MISO      | 21 | 22 | SDIO      | SDIO DAT1 / GPIO2_IO16 |
| ECSPI2_SCLK / GPIO5_IO10   | SCLK      | 23 | 24 | SPI CE0   | ECSPI2_SS0/GPIO5_IO13  |
|                            | GND       | 25 | 26 | SCL       | NIGHT SCL            |
|                    SYS I2C | SYS SDA   | 27 | 28 | SCL       | SYS I2C              |
|                  NIGHT_INT | INT       | 29 | 30 | (GND)     |                      |
|                  NIGHT_SDA | SDA       | 31 | 32 | TxD       | UART4 TX             |
|                   UART4 RX | RxD       | 33 | 34 | JTAG      | SoM JTAG CLK (RPi GND) |
|    Battery measuring point | BAT_LDO   | 35 | 36 | JTAG      | SoM JTAG DIO          |
|     SDIO DAT2 / GPIO2_IO17 | SDIO      | 37 | 38 | CAN2      | CAN2 RX / GPIO4_IO27  |
|               (GND on RPi) |           | 39 | 40 | CAN2      | CAN2 TX / GPIO4_IO26  |


Testing

| Left side                  | Function  |Pin |Pin | Function  | Right side           |
|----------------------------|-----------|----|----|-----------|----------------------|
|  When VSOM fully connected | 3V3       | 1  | 2  | 5V        | When VSOM fully connected  |
|                  STEM_SDA  | SDA       | 3  | 4  | 5V        | When VSOM fully connected |
|                  STEM_SCL  | SCL       | 5  | 6  | GND       |                      |
|                   STEM_INT | INT       | 7  | 8  | TxD       | UART2 TxD            |
|                            | GND       | 9  | 10 | RxD       | UART2 RxD            |
|                            |           | 11 | 12 | SWD       | SWDCLK for T-USB     |
|     SDIO DAT3 / GPIO2_IO18 | SDIO      | 13 | 14 | SWD       | SWDIO for T-USB (GND)     |
|      SDIO CLK / GPIO2_IO13 | SDIO      | 15 | 16 | SDIO      | SDIO CMD / GPIO2_IO14  |
|                            | 3V3       | 17 | 18 | SDIO      | SDIO DAT0 / GPIO2_IO15 |
| ECSPI2_MOSI / GPIO5_IO11   | MOSI      | 19 | 20 | GND       |                        |
| ECSPI2_MISO / GPIO5_IO12   | MISO      | 21 | 22 | SDIO      | SDIO DAT1 / GPIO2_IO16 |
| ECSPI2_SCLK / GPIO5_IO10   | SCLK      | 23 | 24 | SPI CE0   | ECSPI2_SS0/GPIO5_IO13  |
|                            | GND       | 25 | 26 | SCL       | NIGHT SCL            |
|                    SYS I2C | SYS SDA   | 27 | 28 | SCL       | SYS I2C              |
|                  NIGHT_INT | INT       | 29 | 30 | (GND)     |                      |
|                  NIGHT_SDA | SDA       | 31 | 32 | TxD       | UART4 TX             |
|                   UART4 RX | RxD       | 33 | 34 | JTAG      | GND                   |
|                            |           | 35 | 36 | JTAG      |                       |
|     SDIO DAT2 / GPIO2_IO17 | SDIO      | 37 | 38 | CAN2      |                       |
|               (GND on RPi) |           | 39 | 40 | CAN2      |                       |



