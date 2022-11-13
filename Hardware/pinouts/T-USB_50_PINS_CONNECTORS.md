Two connectors tie the daughterboard to the bridge board. Both are of a 50 pin Highrose B2B type.

- [JLCPCB plug](https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt=DF40C-50DP-0.4V)
- [JLCPCB socket](https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt=DF40C-50DS-0.4V)

default height 1.5mm

Connector 1: High Speed Data
Connector 2: PD Controller, Debug, USB 2.0

| Power   |  Max Current | Pins |
|---------|--------------|------|
| VSOM    | 3.0 A        | 10   |
| GND     | 3.0 A        | 12   |
| VCC_RTC | 300 mA       | 1    |
| 3V3     | 600 mA       | 2    |
| 5V      | 300 mA       | 1    |
| LDO_3V3 | 300 mA       | 1    |


#### Connector 1 high-speed data, close to Alt Mode Breakout connectors

- 8 * GND
- 7 * VSOM

One side

| Pin | Code             | Type     | Details                              | Voltage | to Baseboard | Misc         | MCU pin. |
|-----|------------------|----------|--------------------------------------|---------|--------------|--------------|----------|
| 1   | VSOM             | Power    | Main power for board 3.5V - 4.5V     |         | VSOM         | Conn. detect |          |
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
| 16  | GND              | Power    | Ground                               |         |              |          |
| 17  | STEM SCL         | I2C      | STEM SCL                             |         | P1.94        | GP21 I2C0   |
| 18  | STEM SDA         | I2C      | STEM SDA                             |         | P1.96        | GP20 I2C0   |
| 19  | STEM INT         | I2C      | Sensor interrupts                    |         | P1.98        |          |
| 20  | GND              | Power    | Ground                               |         |              |          |
| 21  |                  |          |                                      |         |              |          |
| 22  |                  |          |                                      |         |              |             | 
| 23  | GND              | Power    | Ground                               |         |              |          |
| 24  |                  |          |                                      |         |              |          |
| 25  |                  |          |                                      |         |              |          |



Other side

| Pin | Code       | Type     | Details                              | Voltage | to Baseboard | Misc         | MCU pin. |
|-----|------------|----------|--------------------------------------|---------|--------------|--------------|----------|
| 50  | reserved   | LVDS     | LVDS CLK+                            |         | P1.80        |          |
| 49  | reserved   | LVDS     | LVDS CLK-                            |         | P1.82        |          |
| 48  | VSOM       | Power    | Main power for board 3.5V - 4.5V     |         | VSOM         |          |
| 47  | reserved   | LVDS     | LVDS D0+                             |         | P1.42        |          |
| 46  | reserved   | LVDS     | LVDS D0-                             |         | P1.44        |          |
| 45  | VSOM       | Power    | Main power for board 3.5V - 4.5V     |         | VSOM         |          |
| 44  | reserved   | LVDS     | LVDS D1+                             |         | P1.46        |          |
| 43  | reserved   | LVDS     | LVDS D1-                             |         | P1.48        |          |
| 42  | VSOM       | Power    | Main power for board 3.5V - 4.5V     |         | VSOM         |          |
| 41  | reserved   | LVDS     | LVDS D2+                             |         | P1.50        |          |
| 40  | reserved   | LVDS     | LVDS D2-                             |         | P1.52        |          |
| 39  | VSOM       | Power    | Main power for board 3.5V - 4.5V     |         | VSOM         |          |
| 38  | reserved   | LVDS     | LVDS D3+                             |         | P1.56        |          |
| 37  | reserved   | LVDS     | LVDS D3-                             |         | P1.58        |          |
| 36  | VSOM       | Power    | Main power for board 3.5V - 4.5V     |         | VSOM         |          |
| 35  |            |          |                                      |         |              |          |
| 34  |            |          |                                      |         |              |          |
| 33  | GND        | Power    | Ground                               |         |              |          |
| 32  | CAN_RX     |          | CAN1_RX                              |         | P1.51        | P21.12       |
| 31  | CAN_TX     |          | CAN1_TX                              |         | P1.53        | P21.14       |          |
| 30  | PWR_CHARGE |          |                                      |         |              |              |
| 29  |            |          |                                      |         |              |          |
| 28  |            |          |                                      |         |              |          |
| 27  |            |          |                                      |         |              |          |
| 26  | VSOM       | Power    | Main power for board 3.5V - 4.5V     |         | VSOM         |          |

Could also take in HDMI or PCIe lanes instead of LVDS


#### Connector 2 PD controller, close to power connectors

- 2 * VSOM, 3 * GND, 1 * VCC_RTC, 2 * 3V3
- 1 * VSOM, 1 * GND, 1 * 5V

One side

| Pin | Code         | Type     | Details                              | Voltage | to Baseboard | Misc         |
|-----|--------------|----------|--------------------------------------|---------|--------------|--------------|
| 1   | VSOM         | Power    | Main power for board 3.5V - 4.5V     |         | VSOM         | Conn. detect |
| 2   | GND          | Power    | Ground                               |         |              |
| 3   | USB1_DP      | USB      | USB1 D+                              |         | P1.12        |
| 4   | USB1_DN      | USB      | USB1 D-                              |         | P1.14        |
| 5   | GND          | Power    | Ground                               |         |              |
| 6   | USB2_DP      | USB      | USB2 D+                              |         | P1.3         |
| 7   | USB2_DN      | USB      | USB2 D-                              |         | P1.5         |
| 8   | GND          | Power    | Ground                               |         |              |
| 9   | USB1_SBU1    | OTG      | Spare pins                           |         |              |
| 10  | USB1_SBU2    | OTG      | Spare pins                           |         |              |
| 11  | GND          | Power    | Ground                               |         |              |
| 12  |SYS_PD_CTL_INT| IRQ      | PD Controller trigs INT as SYS slave |         | P20.20 P2.67 EX:P1.3 EX0.2 |             |
| 13  | SYS I2C SCL  | I2C      |                                      |         | P21.7        | GP15 I2C1.  |
| 14  | SYS I2C SDA  | I2C      |                                      |         | P21.5        | GP14 I2C1.  |
| 15  | VSOM         | Power    | Main power for board 3.5V - 4.5V     |         | VSOM | Mech. lock |
| 16  | USB_XD_OE    | Alt USB2 | USB 2.0 bus switch                   |         | P1.2   | P10.9   |
| 17  | USB_XD_SEL   | Alt USB2 | USB 2.0 bus switch                   |    | P2.66   | P10.7 |
| 18  | PMIC_ON_REQ  | Reset    | PMIC ON input from Application processor. When high, the device starts power on sequence. |   | P1.68   | P10.5   |
| 19  | PMIC_STBY_REQ| Reset    | Standby mode input from Application processor. When high, device enters STANDBY mode. |   | P1.66    | P10.3  |
| 20  | ALT_BOOT     | Boot     | Alternate boot                       |         | P1.90         |           |
| 21  | PWRBTN       | Boot     | Power button trigger                 |         | P2.64         |           |
| 22  | BAT_STAT     | Charge   | Charging state                       |         | P1.90         |           |
| 23  | BAT_INT      | Charge   | Charging interrupt                   |         | P1.95         |  P21.18   |
| 24  | BAT_CE#      | Charger  | Charge Enable Active-Low. Connect CE to a high logic level to place the battery charger in standby mode.  |      |    |
| 25  | BAT_EN       | Charger  | Enable battery charger output        |         |    |

Other side

| Pin | Code       | Type     | Details                              | Voltage    | to Baseboard |  Misc   | mcu pin |
|-----|------------|----------|--------------------------------------|------------|--------------|---------|---------|
| 50  |            |          |                                      |            |              |         |
| 49  | VCC_RTC    | Power    | Low power mode supply                | 3.3V       | P1.93        |           |
| 48  | USB1_XDP   | USB 2.0  |  OTG plug alt USB 2.0                |            |              | 
| 47  | USB1_XDN   | USB 2.0  | OTG plug alt USB 2.0                 |            |          |  
| 46  | 5V         | Power    | To drive LED matrix and HDMI         | 5V           |          |  
| 45  | USB2_XDP   | USB 2.0  | Host plug alt USB 2.0                |            |          |  
| 44  | USB2_XDN   | USB 2.0  | Host plug alt USB 2.0                |            |          |  
| 43  | 3V3        | Power    | Live from VSOM                       | 3.3V       |          |  
| 42  |            |          |                                      |            |          |  
| 41  |            |          |                                      |            |          |  
| 40  | 3V3        | Power    | Live from VSOM                       | 3.3V       |              |    |
| 39  | PD_HRESET  | PD       | PD Controller HRESET (High)          |            |              |         |
| 38  |            | I2C      |                                      |            |              |    |
| 37  | POWER_PD_CTL_INT| I2C | Interrupt from slaves                |            |              |    |
| 36  | POWER SCL  | I2C      | Power SCL                             |            |         |     |     |
| 35  | POWER SDA  | I2C      | Power SDA                             |            |         |     |     |
| 34  | FLASH_HOLD | I2C      | Override the built in flash chip     |            |              |         |          |
| 33  | SPI_CS     | PD       | Flash SPI                               | 3.3V       |              |         |   |
| 32  | SPI_CLK    | PD       | Flash SPI                               | 3.3V       |              |         |   |
| 31  | SPI_MISO   | PD       | Flash SPI                               | 3.3V       |              |         |   |
| 30  | SPI_MOSI   | PD       | Flash SPI                               | 3.3V       |              |         |   |
| 29  | BAT_LDO    | Power    | Charger LDO for status               | 3.3V 50 mA |              |         |    |
| 28  | LOCK_BTN   | Power    | Signal                               |            |              |         |     |
| 27  |SHUTDOWN_BTN| Power    | Signal                               |            |              |         |     |
| 26  | VSOM       | Power    | Main power for board 3.5V - 4.5V     |            | VSOM         |  Conn. detect |     |


