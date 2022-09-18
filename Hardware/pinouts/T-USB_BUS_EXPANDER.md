| Function          | VQFN32 | LQFP | G56 | Connected to             |
|-------------------|--------|------|-----|--------------------------|
| STEM INT          | 31     |  24  | 28  | P1.0. 1-Wire event raising line between MCUs  |
| UART3 RX          | 1      |  23  | 27  | P1.1. USCI_A0. UCA0RXD.                        |
| UART3 TX          | 2      |  22  | 26  | P1.2. USCI_A0. UCA0TXD.                        |
| MCU SYS INT       | 3      |  21  | 25  | P1.3. 1-Wire event raising line between MCUs   |
| SYS SCL           | 4      |  20  | 24  | P1.4. 50 pin connector. TCK. JTAG test clock, input terminal for device programming and test    |
| SYS SDA           | 5      |  19  | 23  | P1.5. 50 pin connector. TMS. JTAG test clock, input terminal for device programming and test  |
| MSP_TDI/analog    | 21     | 18   | 22  | P1.6 TDI/TCLK. Host Alt. JTAG test data input or test clock input during programming and test.   |
| MSP_TDO/analog    | 22     | 17   | 21  | P1.7 TDO/TDI. Host Alt. JTAG test data output terminal or test data during programmign and test |
| UCB0_CE           | nc     | 32   | 34  | P5.0. nc |
| UCB0_CLK          | nc     | 31   | 33  | P5.1. nc |
| STEM SCL          |        | 29   | 31  | P5.3. USCI_B0.     |
| STEM SDA          |        | 30   | 32  | P5.2. USCI_B0.   |
| TA1.1/Cp          | nc     | 12   | 18  | P4.0  / Host Alt connector          |
| XIN               | nc     | 7    | 13  | P4.1/XIN / Host Alt connector         |
| XOUT              | nc     | 6    | 12  | P4.2/XOUT / Host Alt connector       |
| TA1CLK/Compare    | nc     | 14   | 20  | P8.2 TA1CLK / Host Alt connector           |
| TA1.2/Compare     | nc     | 13   | 19  | P8.3  / Host Alt connector           |

