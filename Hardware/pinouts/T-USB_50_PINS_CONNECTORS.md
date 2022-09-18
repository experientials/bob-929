Two connectors tie the daughterboard to the bridge board. Both are of a 50 pin Highrose B2B type.

- [JLCPCB plug](https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt=DF40C-50DP-0.4V)
- [JLCPCB socket](https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt=DF40C-50DS-0.4V)

default height 1.5mm

Connector 1: High Speed Data
Connector 2: PD Controller, Debug, USB 2.0

| Power   |  Max Current | Pins |
|---------|--------------|------|
| VSOM    | 3.0 A        | 10   |
| GND     | 3.0 A        | 10   |
| VCC_RTC | 600 mA       | 2    |
| VIN_3V3 | 300 mA       | 1    |
| VIN_5V  | 600 mA       | 2    |
| LDO_3V3 | 300 mA       | 1    |


#### Connector 1 high-speed data, close to Alt Mode Breakout connectors

- 6 * GND
- 7 * VSOM

One side

| Pin | Code             | Type     | Details                              | Voltage | to Baseboard | Misc         | MCU pin. |
|-----|------------------|----------|--------------------------------------|---------|--------------|--------------|----------|
| 1   | VSOM             | Power    | Main power for board 3.45V - 4.5V    |         | VSOM         | Conn. detect |          |
| 2   | USB1_RX_DP       | USB      | USB1 RX D+ (OTG)                     |         | P1.6         | HD3SS460 SSRX     |
| 3   | USB1_RX_DN       | USB      | USB1 RX D- (OTG)                     |         | P1.8         | HD3SS460 SSRX     |
| 4   | GND              | Power    | Ground                               |         |              |          |
| 5   | USB1_TX_DP       | USB      | USB1 TX D+ (OTG)                     |         | P1.16        | HD3SS460 SSTX     |
| 6   | USB1_TX_DN       | USB      | USB1 TX D- (OTG)                     |         | P1.18        | HD3SS460 SSTX         |
| 7   | GND              | Power    | Ground                               |         |              |          |
| 8   | USB2_RX_DP       | USB      | USB2 RX D+  (Host)                   |         | CBTL04083 A0 | HD3SS460 SSRX         |
| 9   | USB2_RX_DN       | USB      | USB2 RX D-  (Host)                   |         | CBTL04083 A0 | HD3SS460 SSRX         |
| 10  | GND              | Power    | Ground                               |         |              |          |
| 11  | USB2_TX_DP       | USB      | USB2 TX D+  (Host)                   |         | CBTL04083 A1 | HD3SS460 SSTX         |
| 12  | USB2_TX_DN       | USB      | USB2 TX D-  (Host)                   |         | CBTL04083 A1 | HD3SS460 SSTX         |
| 13  | GND              | Power    | Ground                               |         |              |          |
| 14  |                  |          |                                      |         |              |             | 
| 15  |                  |          |                                      |         |              |             | 
| 16  |                  |          |                                      |         |              |             | 
| 17  | STEM SCL         | I2C      | STEM SCL                             |         | P1.94        | GP21 I2C0   |
| 18  | STEM SDA         | I2C      | STEM SDA                             |         | P1.96        | GP20 I2C0   |
| 19  | STEM INT         | I2C      | Sensor interrupts                    |         | P1.98        |          |
| 20  | GND              | Power    | Ground                               |         |              |          |
| 21  | T_SBWTCK         | MSP430   | SBWTCK / TEST / RTS                  |         |              |          |
| 22  | T_EXTRA          | MSP430   |                                      |         |              |             | 
| 23  | T_SBWTDIO        | MSP430   | SBWTDIO / RST / NMI / DTR            |         |              |          |
| 24  | PWR_CHARGE       | Battery  | Internal charge current for testing  |         |              |          |
| 25  | BAT_STAT         | Battery  | Internal charging status for testing |         |              |          |



Other side

| Pin | Code       | Type     | Details                              | Voltage | to Baseboard | Misc         | MCU pin. |
|-----|------------|----------|--------------------------------------|---------|--------------|--------------|----------|
| 50  | LVCLK+     | LVDS     | LVDS CLK+                            |         | P1.80        |          |
| 49  | LVCLK-     | LVDS     | LVDS CLK-                            |         | P1.82        |          |
| 48  | VSOM       | Power    | Main power for board 3.45V - 4.5V    |         | VSOM         |          |
| 47  | LVD0+      | LVDS     | LVDS D0+                             |         | P1.42        |          |
| 46  | LVD0-      | LVDS     | LVDS D0-                             |         | P1.44        |          |
| 45  | VSOM       | Power    | Main power for board 3.45V - 4.5V    |         | VSOM         |          |
| 44  | LVD1+      | LVDS     | LVDS D1+                             |         | P1.46        |          |
| 43  | LVD1-      | LVDS     | LVDS D1-                             |         | P1.48        |          |
| 42  | VSOM       | Power    | Main power for board 3.45V - 4.5V    |         | VSOM         |          |
| 41  | LVD2+      | LVDS     | LVDS D2+                             |         | P1.50        |          |
| 40  | LVD2-      | LVDS     | LVDS D2-                             |         | P1.52        |          |
| 39  | VSOM       | Power    | Main power for board 3.45V - 4.5V    |         | VSOM         |          |
| 38  | LVD3+      | LVDS     | LVDS D3+                             |         | P1.56        |          |
| 37  | LVD3-      | LVDS     | LVDS D3-                             |         | P1.58        |          |
| 36  | VSOM       | Power    | Main power for board 3.45V - 4.5V    |         | VSOM         |          |
| 35  |            |          |                                      |         |              |          |
| 34  |            |          |                                      |         |              |          |
| 33  | GND        | Power    | Ground                               |         |              |          |
| 32  | CAN_RX     |          | CAN1_RX                              |         | P1.51        | P21.12       |
| 31  | CAN_TX     |          | CAN1_TX                              |         | P1.53        | P21.14       |          |
| 30  | BAT_LDO    | Battery  | 4.9V 50mA LDO for STAT LED           |         |              |              |
| 29  | BOTH_VSOM2 | MSP430   | High if any VSOM pin on this connector supplies on Faceboard side. |         |              |          |
| 28  | UART_T_TXD | MSP430   |                                      |         |              |          |
| 27  | UART_T_RXD | MSP430   |                                      |         |              |          |
| 26  | VSOM       | Power    | Main power for board 3.45V - 4.5V    |         | VSOM         |          |

Could also take in HDMI or PCIe lanes instead of LVDS


#### Connector 2 PD controller, close to power connectors

- 2 * VSOM, 3 * GND, 1 * VCC_RTC, 1 * VIN_3V3
- 1 * VSOM, 1 * GND, 2 * VIN_5V

One side

| Pin | Code         | Type     | Details                              | Voltage | to Baseboard | Misc         |
|-----|--------------|----------|--------------------------------------|---------|--------------|--------------|
| 1   | VSOM         | Power    | Main power for board 3.45V - 4.5V    |         | VSOM         | Conn. detect |
| 2   | GND          | Power    | Ground                               |         |              |
| 3   | USB1_DP      | USB      | USB1 D+                              |         | P1.12        |
| 4   | USB1_DN      | USB      | USB1 D-                              |         | P1.14        |
| 5   | GND          | Power    | Ground                               |         |              |
| 6   | USB2_DP      | USB      | USB2 D+                              |         | P1.3         |
| 7   | USB2_DN      | USB      | USB2 D-                              |         | P1.5         |
| 8   | GND          | Power    | Ground                               |         |              |
| 9   | PD_SWD_CLK   | Debug    | PD Controller GPIO12                 |         |              |
| 10  | PD_SWD_DAT   | Debug    | PD Controller GPIO13                 |         |              |
| 11  | BOTH_VSOM    | Enable   | Bridge board signal;VSOM connected on both sides | 3V3        |   |
| 12  | MCU_SYS_INT  | IRQ      | When state of MCUs change -> SoM     |         | P20.20 P2.67 EX:P1.3 EX0.2 |             |
| 13  | SYS I2C SCL  | I2C      |                                      |         | P21.7        | GP15 I2C1.  |
| 14  | SYS I2C SDA  | I2C      |                                      |         | P21.5        | GP14 I2C1.  |
| 15  | VSOM_LOCK    | Power    | Main power for board 3.45V - 4.5V, if mechanical lock shorted    |         | VSOM | Mech. lock |
| 16  | SYS_RST_PMIC | Reset    | PMIC reset input pin. Internally pulled up with LDO1 power rail. Once low, PMIC performs reset. |         | P1.2   | P10.9   |
| 17  | POR_B_3P3    | Reset    | Power On reset output pin. Open drain output requiring external pull up resistor. |    | P2.66   | P10.7 |
| 18  | PMIC_ON_REQ  | Reset    | PMIC ON input from Application processor. When high, the device starts power on sequence. |   | P1.68   | P10.5   |
| 19  | PMIC_STBY_REQ| Reset    | Standby mode input from Application processor. When high, device enters STANDBY mode. |   | P1.66    | P10.3  |
| 20  | VCC_RTC      | Power    | Low power mode supply                |         | P1.93         |           |
| 21  | PWRBTN       | Boot     | Power button trigger                 |         | P2.64         |           |
| 22  | ALT_BOOT     | Boot     | Alternate boot                       |         | P1.90         |           |
| 23  | QSPI_BOOT_EN_3P3| Boot  | SPI boot                             |         | P1.95         |  P21.18   |
| 24  | BAT_CE#      | Charger  | Charge Enable Active-Low. Connect CE to a high logic level to place the battery charger in standby mode.  |      |    |
| 25  | PD_VIN_EN    | Future   | Enable VIN_5V/3V3 from PWR_SYS (TBD) |         |    |

Other side

| Pin | Code       | Type     | Details                              | Voltage    | to Baseboard |  Misc   | mcu pin |
|-----|------------|----------|--------------------------------------|------------|--------------|---------|---------|
| 50  | PD_HRESET  | Future   | PD Controller HRESET (High)          |            |              |         |
| 49  | GND        | Power    | Ground                               |            |              |         |
| 48  | UART1_TXD  | UART     |  UART1 Tx                            |            | P1.72        | P20.9   | GP4 UART1    |
| 47  | UART1_RXD  | UART     | UART1 Rx                             |            | P1.19        | P20.11  | GP5 UART1    |
| 46  | UART2_TXD  | UART     | UART2 Tx                             |            | P1.74        | P20.1   | GP8 UART1.   |
| 45  | UART2_RXD  | UART     | UART2 Rx                             |            | P1.76        | P20.3   | GP9 UART1    |
| 44  | UART3_TXD  | UART     | UART3 Tx                             |            | P1.61        | P20.2   | GP12 UART0   |
| 43  | UART3_RXD  | UART     | UART3 Rx                             |            | P1.21        | P20.4   | GP13 UART0   |
| 42  | UART4_TXD  | UART     | UART4 Tx                             |            | P1.86        | P20.8   | GP20 UART1 |
| 41  | UART4_RXD  | UART     | UART4 Rx                             |            | P1.84        | P20.10  | GP21 UART1 |
| 40  | MIC_CLK    | Sensor   | frontboard mic                       |            |              |    |
| 39  | MIC_DATA   | Sensor   |                                      |            |              |    |
| 38  | PD_USBC_INT| PD ctl   | USB insertion state etc changed      |            |              |    |
| 37  | MOTION_INT | Sensor   | Spare interrupt pin for future       |            |              |    |
| 36  | NIGHT SCL  | I2C      | I2C6 SCL                             |            | P1.87        | P21.2   | GP19 I2C1.   |
| 35  | NIGHT SDA  | I2C      | I2C6 SDA                             |            | P1.89        | P21.4   | GP18 I2C1.   |
| 34  | NIGHT INT  | I2C      | Sensor interrupts                    |            |              |         |          |
| 33  | SPI_CS     | RP2040   | RP SPI                               | 3.3V       |              |         | GP29 SPI1 |
| 32  | SPI_CLK    | RP2040   | RP SPI                               | 3.3V       |              |         | GP10 SPI |
| 31  | SPI_MISO   | RP2040   | RP SPI                               | 3.3V       |              |         | GP28 SPI |
| 30  | SPI_MOSI   | RP2040   | RP SPI                               | 3.3V       |              |         | GP11 SPI |
| 29  | VIN_3V3    |          | Supply for TPS64988 circuitry and I/O| 3.3V 50 mA |              |         |    |
| 28  | VIN_5V     | Power    | System 5V src (PPHV1/2, PP1/2_CABLE) | 5V 500 mA  |              |         |     |
| 27  | VIN_5V     | Power    | System 5V src (PPHV1/2, PP1/2_CABLE) | 5V 500 mA  |              |         |     |
| 26  | VSOM       | Power    | Main power for board 3.45V - 4.5V    |            | VSOM         |  Conn. detect |     |

SPI pins will be exchanged for SDIO (MIC_INT / MOTION_INT / PD_HRESET likely to go away)

Consider SPI for PD Controller
PD Controller IRQ I2C1
