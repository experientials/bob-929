
The Sensors on these expansion triggers interrupt via EX_OH_nINT / SOUND_INT (GPIO1_IO0).
The pins connect directly to the i.MX module.

| Pin | Code       | Function   | Description               | 
|-----|------------|------------|---------------------------|
|  1  | GND        |            |                           |
|  2  | SAI5_MCLK  | SAI5_MCLK  | Master Clock              |
|  3  |	SPK_BCLK   | SAI5_TXC   | I2S BCLK	/ SCK           |
|  4  | SPK_LRCLK  | SAI5_TXFS  | I2S LRCLK                 | 
|  5  | SPK_DATA0  | SAI5_TXD0  | I2S DATA                  | 
|  6  | SPK_DATA1  | SAI5_TXD1  | I2S DATA                  | 
|  7  | SPK_DATA2  | SAI5_TXD2  | I2S DATA                  | 
|  8  | SPK_DATA3  | SAI5_TXD3  | I2S DATA                  | 
|  9  | VIN        | 1V8 / 3V3  | Power at signal level     |
| 10  | 3V3        | 3V3        | Power         |
| 11  |	MIC_BCLK   | SAI5_RXC   | I2S BCLK	/ SCK           |
| 12  | MIC_LRCLK  | SAI5_RXFS  | I2S LRCLK                 | 
| 13  | MIC_DATA0  | SAI5_RXD0  | I2S DATA                  | 
| 14  | MIC_DATA1  | SAI5_RXD1  | I2S DATA                  | 
| 15  | MIC_DATA2  | SAI5_RXD2  | I2S DATA                  | 
| 16  | MIC_DATA3  | SAI5_RXD3  | I2S DATA                  | 
| 17  | SCL        | I2C6_SCL   | I2C                       |
| 18  | SDA        | I2C6_SDA   | I2C                       |
| 19  | GPIO1_IO0  | EX_OH_nINT / SOUND_INT | Interrupt pin GPIO1_IO0        |
| 20  | GND        | GND        | Power         |

(?) Rename EX_OH_nINT

A future bigger/alternate connector would include:

- SCLK
- MISO
- MOSI
- ECSPI2_SS0
- CAN1_RX / CAN1_TX
- CAN2_RX / CAN2_TX
- PWM1..3
- VCC_RTC / Suspended Power
- 5 * GPIO
