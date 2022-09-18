Stem I2C addresses

| Address    | Chipset  | Description                             |
|------------|----------|-----------------------------------------|
| 0x28       | BHI260AP | Motion Engine (alternate config)        |
| 0x40/0xC0 or 0x44| IS31FL3730 | LED controller                  |      
| 0x42/0x43  | PCA9555  | 16 bit expander EX1 on T-USB daughterboard (bits = 001) |
| 0x46/0x47  | PCA9555  | 16 bit expander EX3 on T-USB daughterboard (bits = 011) |
| 0x48/0x49  | PCA9555  | 16 bit expander EX4 on faceboard  (bits = 100)         |
| 0x4C       | MC6470   | 9-Axis Sensor                           |
| 0x54..0x57 | EEPROM   | Faceboard EEPROM          |
| 0x60       | VM3011   | mic           |
| 0x6A       | BQ24250  | LiPO Battery Charger      |
| 0x7E 0x7F  | TPS65988 |  PD Controller Port 2                   |
| 0x98 0x99  | MC6470   | 9-Axis Sensor
