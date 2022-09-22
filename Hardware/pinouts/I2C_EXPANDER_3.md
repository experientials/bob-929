
This EX3 Combined T-USB control I/O Expander is placed on T-USB daughterboard and controlled via the Stem I2C.
The I2C address is 0x23(0x46/0x47)  assigned by hardware address pins set to 0b011.
The EX3 expander input triggers interrupt via STEM_INT (GPIO1_01).

The pins relate to USB1 OTG, USB2 Host, PD Controller
The EX3 expander allows controlling T-USB maps,

| Expander  | Pin   | Connected to    |
|-----------|-------|-----------------|
| EX3.0     | O0.0  |  BAT_CE    |
| EX3.1     | I0.1  |  BAT_INT            |
| EX3.2     | O0.2  | PD_CTL_RESET     |
| EX3.3     | I0.3  | PD_CTL_INT_2     |
| EX3.10    | O1.2  |  Select Host Extra A6/A7 (HXA_SEL)  |
| EX3.11    | O1.3  |  Select Host Extra B6/B7 (HXB_SEL)  |
| EX3.12    | O1.4  | Select Host Extra Enable (HX_OE) |
| EX3.13    | O1.5  |  Select OTG Extra A6/A7 (OXA_SEL)  |
| EX3.14    | O1.6  |  Select OTG Extra B6/B7 (OXB_SEL)  |
| EX3.15    | O1.7  | Select OTG Extra Enable (OX_OE) |



#### TS5USB41 Alt. Mode control

How to set the OTG USB 2.0 modes by enabling pins for the two TS5USB41
 
| Mode     | mode bits | A: OE  | A: SEL1/2 | B: OE  | B: SEL1/2 |
|----------|-----------|--------|-----------|--------|-----------|
| off      | 0 0       | H      |           | H      |           |
| Auto USB | 0 1       | L      | 0         | L      | 0         |
| Occi USB | 1 0       | L      | 1         | H      |           |
| Plural   | 1 1       | L      | 0         | L      | 1         |


T-USB OTG 2.0 data,
- off (Autonomous MCU USB talks to Occi MCU USB1)
- Autonomous MCU USB (A and B)
- Occi MCU USB1 (only A)
- Plural; OTG-A connects Autonomous MCU USB, OTG-B connects Extra OTG USB
