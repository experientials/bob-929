
Removed:
| EX3.9     | O1.1  |  T_USB_ALERT    |
| EX3.0     | I0.0  | PD_CTL_INT_1 (this belongs to SYS I2C)    |




RUN_RP - Suspend the RP ?
BOOTSEL - Boot select
BAT_CE

PD Controller GPIOs


Power Management IC PCA9450

| 16  | SYS_RST_PMIC | Reset    | PMIC reset input pin. Internally pulled up with LDO1 power rail. Once low, PMIC performs reset. |         | P10.9   |
| 17  | POR_B_3P3    | Reset    | Power On reset output pin. Open drain output requiring external pull up resistor. |    | P10.7 |
| 18  | PMIC_ON_REQ  | Reset    | PMIC ON input from Application processor. When high, the device starts power on sequence. |     | P10.5   |
| 19  | PMIC_STBY_REQ| Reset    | Standby mode input from Application processor. When high, device enters STANDBY mode. |     | P10.3  |

Processor:

| 21  | PWRBTN       | Boot     | Power button trigger                 |         |   |
| 22  | ALT_BOOT     | Boot     | Alternate boot                       |         |   |
| 23  | QSPI_BOOT_EN_3P3| Boot  | SPI boot                             |         |  P21.18   |
| 24  | BAT_CE#      | Charger  | Charge Enable Active-Low. Connect CE to a high logic level to place the battery charger in standby mode.  |      |    |
| 25  | PD_VIN_EN    | Future   | Enable VIN_5V/3V3 from PWR_SYS (TBD) |         |    |


