SYS I2C addresses

<mark>Reduced the devices connected to SYS bus</mark>

| Address    | Chipset  | Description               |
|------------|----------|---------------------------|
| 0x20       | PCA9555  | 16 bit expander EX0       |
| 0x25       | PCA9450  | Reserved 7 bit address    |
| 0x26       | PCA9555  | 16 bit expander EX6       |
| 0x47       | TUSB546  | Power I2C - Host Alt. Mode|
| 0x4A 0x4B  | PCA9450  | Power Management IC       |
| 0x68       | PI6CG18200 | PCIe clock generator    |
| 0x6A       | BQ24250  | LiPO Battery Charger      |
| 0x70 0x71  | TPS65988 |  RESERVED for PD Controller Port 1 / SYS |
| 0xD2/D3    | RTC      | AM1805 real time clock (RTC) |

HD3SS3220

| No 0x25 on faceboard or power module !! |