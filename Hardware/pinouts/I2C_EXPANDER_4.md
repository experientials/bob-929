
This 919 EX4 Faceboard sensor I/O Expander is placed on faceboard and controlled via the Stem I2C.
The I2C address is 0x48/0x49 assigned by hardware address pins set to 0b100.

- LED Controller
- Motion Sensor
- Sound Sensor
- Nighttime camera attached sensors
- 

The EX4 expander input triggers interrupt via STEM_INT (GPIO1_01).

| Expander  | Pin   | Connected to                |
|-----------|-------|-----------------------------|
| EX4.0     |       |    |
| EX4.1     | O0.1  | SD Card Chip Select SPI     |
| EX4.2     | O0.2  | SD Card Chip Select SDIO    |
| EX4.3     | I0.3  | IMU_INTM - MC6470 INTM      |
| EX4.4     | I0.4  | IMU_IRQ - MC6470 INTA / Motion Controller  |
| EX4.5     | O0.5  | IMU_RESETN  - Motion Controller    |
| EX4.6     | O0.6  | IMU_MODE  - Motion Controller        |
| EX4.7     | O0.7  | LED_SHUTDOWN - SDB         |
| EX4.8     | I1.0  | MIC VM3011 DOUT            |
| EX4.9     | O1.1  | W_DISABLE2# on m.2 Key E   |
| EX4.10    | O1.2  | W_DISABLE1# on m.2 Key E   |
| EX4.11    | O1.3  | M2E_PWROFF on m.2 Key E    |
| EX4.12    | O1.4  | M2B_PWROFF on m.2 Key B    |
| EX4.13    | O1.5  | DEVSLP 3V3 on m.2 Key B    |
| EX4.14    | I1.6  | RIGHT_ATT_INT              |
| EX4.15    | O1.7  | RIGHT_ATT_XSHUT            |

Enable CS SD Card connector
LCD CS SPI
MMC CS 
m.2 WiFi CS SDIO
