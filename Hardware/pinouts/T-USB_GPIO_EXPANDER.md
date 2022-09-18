| Function          | VQFN32 | LQFP | G56 | Connected to             |
|-------------------|--------|------|-----|--------------------------|
| SHUTDOWN_BTN      | 9      | 40   | 42  | P2.0. Shudown button pin on 3 pin Power Enable Connector   |
| LOCK_BTN          | 10     | 39   | 41  | P2.1. Lock button pin on 3 pin Power Enable Connector   | 
| POR_B_3P3         | 11     | 38   | 40  | P2.2. Power on reset Input from PMIC. 50 pin connector             |
| BOTH_VSOM         | 15     | 37   | 39  | P2.3. Input from faceboard. 50 pin connector    | 
| T_USB_O_ALT_POL   | 16     | 36   | 38  | P2.4. HD3SS460 (default = high-im)     |
| T_USB_O_ALT_AMSEL | 17     | 35   | 37  | P2.5. HD3SS460 (default = high-im)  |
| T_USB_H_ALT_POL   | 26     | 34   | 36  | P2.6. HD3SS460 (default = high-im) |
| T_USB_H_ALT_AMSEL | 25     | 33   | 35  | P2.7. HD3SS460 (default = high-im)  |
| T_USB_O_ALT_EN    | SH1.0  | 56   | 56  | P3.0. HD3SS460 (default = high-im) |
| T_USB_H_ALT_EN    | SH1.1  | 55   | 55  | P3.1. HD3SS460 (default = high-im) |
| HXA_SEL           | SH1.2  | 54   | 54  | P3.2. Select Host Extra A6/A7   |
| HXB_SEL           | SH1.3  | 53   | 53  | P3.3. Select Host Extra B6/B7 |
| HX_OE             | SH1.4  | 52   | 52  | P3.4. Select Host Extra Enable     |
| OXA_SEL           | SH1.5  | 51   | 51  | P3.5. Select OTG Extra A6/A7      |
| OXB_SEL           | SH1.6  | 50   | 50  | P3.6. Select OTG Extra B6/B7     |
| OX_OE             | SH1.7  | 49   | 49  | P3.7. Select OTG Extra Enable     |
| PWRBTN            | SH2.0  | 5     | 11  | P4.3. 50 pin connector    |
| ALT_BOOT          | SH2.1  | 4     | 10  | P4.4. 50 pin connector    |
|                   | SH2.2  | 3     | 9   | P4.5. 50 pin connector    |
| VSOM_LOCK_EN      | SH2.3  | 2     | 8   | P4.6. Data output enabling VSOM_LOCK(300mA VSOM). |
| SYS_RST_PMIC      | SH2.4  | 1     | 7   | P4.7. 50 pin connector   |
| PMIC_ON_REQ       | SH2.5  | 28    | 30  | P5.4. 50 pin connector  |
| PMIC_STBY_REQ     | SH2.6  | 27    | 29  | P5.5. 50 pin connector  |
|                   | SH2.7  |       |     |                 |        
| BOTH_VSOM2        |        | 48    | 48  | P6.0. 50 pin connector |
| BAT_INT           |        | 47    | 47  | P6.1. BQ24250 |
| PD_CTL_INT_1      |        | 46    | 46  | P6.2. TPS PD Controller |
| PD_CTL_INT_2      |        | 45    | 45  | P6.3. TPS PD Controller |
| T_EXTRA           | SH3.0  | 44    | 44  | P6.4. 50 pin connector |
| BAT_CE            | SH3.1  | 43    | 43  | P6.5. BQ24250 |
| BAT_EN1           | SH3.2  | 6     | 6   | P7.0. BQ24250  |
| BAT_EN2           | SH3.3  | 5     | 5   | P7.1. BQ24250  |
| PD_CTL_RESET      | SH3.4  | 4     | 4   | P7.2. TPS PD Controller  |
| PD_EXT1           | SH3.5  | 3     | 3   | P7.3. TPS PD Controller   | 
| PD_EXT2           | SH3.6  | 60    | 2   | P7.4. TPS PD Controller  |
| PD_VIN_EN         | SH3.7  | 59    | 1   | P7.5. TPS PD Controller   |

56 pin package excludes 8 pins: P8.0 P8.1 P5.6 P5.7 P6.6 P6.7 P7.6 P7.7 (only usable at 64 pin package)

