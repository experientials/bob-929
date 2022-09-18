The USB connectors are named H (Host) and O (OTG). Host is the top of the T, OTG is the vertical base.
To specify a specific pin H or O is prefixed I.E. OTX1+, HSBU2.

Where possible data pins are not combined but carried through individually.

The GND/VBUS pins are connected to the power charging circuit as normal. The system should accept
charging power from either connector.


| No. | Pin  | Description   |      |
|-----|------|---------------|--------|
|  1  |	 A1  |	   GND 	     |        |  
|  2  |	 A2  |	   TX1+ 	 | T-USB direct, do not combine      |
|  3  |	 A3  |	   TX1- 	 | T-USB direct, do not combine      |
|  4  |	 A4  |	   VBUS 	 |       |
|  5  |	 A5  |	   CC1 	     | TPS65988      |
|  6  |	 A6  |	   D+	     | TPS65988 & T-USB direct |
|  7  |	 A7  |	   D-  	    | TPS65988 & T-USB direct      |
|  8  |	 A8	 |  SBU1        | T-USB direct      |
|  9  |	 A9	 |  VBUS 	    | TPS65988 & Power regulators      |
| 10  |	 A10 |  RX2- 	    | T-USB direct, do not combine      |
| 11  |	 A11 |  RX2+ 	    | T-USB direct, do not combine      |
| 12  |	 A12 |  GND 	    |       |
| 13  |	 B1	 |  GND  	   |       |
| 14  |	 B2	 |  TX2+        | T-USB direct, do not combine      |
| 15  |	 B3	 |  TX2-        | T-USB direct, do not combine      |
| 16  |	 B4	 |  VBUS 	    | TPS65988 & Power regulators      |
| 17  |	 B5	 | CC2  	    | TPS65988      |
| 18  |	 B6	 |  DX+         | TPS65988 & T-USB direct, do not combine      |
| 19  |	 B7	 |  DX-         | TPS65988 & T-USB direct, do not combine      |
| 20  |	 B8	 |  SBU2        | T-USB direct      |
| 21  |	 B9	 |  VBUS  	    | TPS65988 & Power regulators      |
| 22  |	 B10 |  RX1-        | T-USB direct, do not combine      |
| 23  |	 B11 |  RX1+        | T-USB direct, do not combine      |
| 24  |	 B12 |  GND 	    |       |


The USB Type-C connector has 24 pins. Figures 1 and 2, respectively, show the pins for the USB Type-C receptacle and plug.

![USB-C Receptacle](../datasheets/USB/Fig1m11292018.png)
Figure 1. The USB Type-C receptacle. Image courtesy of [Microchip](http://ww1.microchip.com/downloads/en/appnotes/00001953a.pdf).

![USB-C Plug](../datasheets/USB/Fig2m11292018.png)
Figure 1. The USB Type-C plug. Image courtesy of [Microchip](http://ww1.microchip.com/downloads/en/appnotes/00001953a.pdf).


### For later revision

Only **one side** of the connectors are connected to the matching USB connector that leads to the Dev Board.

The following pins are connected to the extras connector: TX2+, TX2-, SBU1, SBU2, RX-, RX1+, DX+, DX-

The following pins are treated as normally USB-C connection pins: A1-A7, A9-A12, B5.
