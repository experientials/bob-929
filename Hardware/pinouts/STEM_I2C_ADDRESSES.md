Stem I2C addresses



| Address    | Chipset  | Description                             |
|------------|----------|-----------------------------------------|
| 0x23       | TPS65988 | On chips USB Port 1 with default address      |
| 0x27       | TPS65988 | On chips USB Port 2 with default address      |
| 0x28       | BHI260AP | Motion Engine (alternate config)        |
| 0x40/0xC0 or 0x44| IS31FL3730 | LED controller                  |      
| 0x4C       | MC6470   | 9-Axis Sensor                           |
| 0x54..0x57 | EEPROM   | Faceboard EEPROM          |
| 0x60       | VM3011   | mic           |
| 0x98 0x99  | MC6470   | 9-Axis Sensor

Sensors (0x28 0x4C 0x60 0x98 0x99) will be moving to a local I2C bus that optionally joins the SYS bus.

