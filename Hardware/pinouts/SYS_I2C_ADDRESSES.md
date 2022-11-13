SYS I2C addresses

<mark>Reduced the devices connected to SYS bus</mark>

| Address    | Chipset  | Description               |
|------------|----------|---------------------------|
| 0x20       | PCA9555  | 16 bit expander EX0       |
| 0x25       | PCA9450  | Reserved 7 bit address    |
| 0x38       | TPS65988 | On chips USB Port 1 with default address      |
| 0x3F       | TPS65988 | On chips USB Port 2 with default address      |
| 0x4A 0x4B  | PCA9450  | Power Management IC       |
| 0x68       | PI6CG18200 | PCIe clock generator    |
| 0xD2/D3    | RTC      | AM1805 real time clock (RTC) |



POWER I2C adresses which may be exposed to SYS I2C. 
When not they are exclusively mastered by the PD Controller I2C3.

| Address    | Chipset  | Description               |
|------------|----------|---------------------------|
| 0x0F       | TUSB546  | OTG Alt. Mode             |
| 0x47       | TUSB546  | Host Alt. Mode            |
| 0x67       | HD3SS3220| OTG USB C orientation and PD Controller |
| 0x6A       | BQ24250  | LiPO Battery Charger      |

1st Music Sculpture
