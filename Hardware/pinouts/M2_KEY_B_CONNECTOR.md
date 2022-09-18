### M.2 Key B Pin allocations

| Pin id.	| Upper     | Lower      | Description                        | Counterpoint   | Voltage Level | Spec Feature |
|-----------|-----------|------------|------------------------------------|----------------|---------------|--------------|
| 1         | CONFIG_3  |		     | Defines Module Type	              | FACE-EX        |               |
| 2         |           | +3.3V	     | 3.3 V power supply from main board |  			   | 3.3V          |
| 3	        | GND		|            | Ground	                          |                |  GND		   |
| 4	        | 	        | +3.3V	     | 3.3 V power supply from main board |                | 3.3V          |
| 5	        | GND		|            | Ground (available?)                |                | GND	       |
| 6	        | 	        | M2B_PWROFF | FULL_CARD_POWER_OFF                |	FACE-EX P6.4   | 3.3V          |
| 7	        | USB D+	|            | USB data pair positive	USB D+    | USB D+         |     |			
| 8	        | 	        | W_DIS1     | Wireless disable 1				  | EXB.3          |               |
| 9	        | USB D-	|            | USB data pair negative	USB D-    | USB D-         |     |			
| 10        | 	        | LED_1      | GPIO9 / WWAN LED_1 / BCLK / SCK    | SAI5_TXC/P2.55 | 3.3V          |
| 11	    | GND		|            | Ground (available?)	              |                | GND          |
| 12 - 19   |			|            |                                    |                |            |   		
| 20        |           | M2_I2S_TXFS| GPIO5 / SPK I2S LRC                | SAI5_TXFS/P2.53| 1.8V          |
| 21	    | CONFIG_0	|            |		  			                  | FACE-EX        |              |
| 22	    |           | M2_I2S_TXD0| GPIO6 / SPK I2S DAT                | SAI5_TXD0/P2.60| 1.8V         |
| 23	    | GPIO11    |            | 	WAKE_ON_WWAN		              |                | 1.8V         |
| 24	    |           | M2_I2S_RXFS| GPIO7 / MIC I2S LRC			      | SAI5_RXFS/P1.34| 1.8V         |
| 25        | DPR       | 	         | WWAN Dynamic Power Reduction       |                | 1.8V         |
| 26	    |           | GPIO10     | SOUND_INT?                         | INT pin?       | 1.8V         |
| 27	    | GND		|            | Ground	                          |                | GND          |
| 28        |           | M2_I2S_RXD0| GPIO8 / MIC I2S DAT			      | SAI5_RXD0/P1.28| 1.8V         |
| 29	    | USB3 RX-	|            | PER-1 / SSIC	M2_USB3_SSRXN		  | M2_USB3_SSRX-  |              |	
| 30	    |           | SIM_RST    | UIM RESET			              | -              |              |
| 31        | USB3 RX+  |            | PER+1 / SSIC	M2_USB3_SSRXP		  | M2_USB3_SSRX+  |              |	
| 32		|           | SIM_CLK    | UIM CLK			                  | -              |              |
| 33        | GND		|            | Ground                             |                | GND	      |
| 34		|           | SIM_DATA	 | UIM DATA			                  | -              |              |
| 35        | USB3 TX-	|            | PET-1 / SSIC	M2_USB3_SSTX-	      | M2_USB3_SSTX-  |              |
| 36        |           | SIM_PWR    | UIM PWR			                  | -              |              |
| 37        | USB3 TX+  |            | PET+2 / SSIC	M2_USB3_SSTX+		  | M2_USB3_SSTX+  |              |
| 38        | 	        | (DEVSLP)   | Device Sleep, input. high=sleep    | -              | 3.3V         | SATA only |
| 39        | GND       |            | Ground	                          |                | GND          |
| 40        | 	        | GNSS_SCL   | GPIO_0 / GNSS / STEM / SCL         | I2C3 SCL       | 1.8V         |
| 41        | PCIE RXN-	|            | PCIE RXN- / PER-0 / SATA-B+        | PCIE RXN-      |          |			
| 42        | 	        | GNSS_SDA   | GPIO_1 / GNSS / STEM / SDA         | I2C3 SDA       | 1.8V         |
| 43        | PCIE RXN+ |            | PCIE RXN+ / PER+0 / SATA-B-        |	PCIE RXN+      | 1.8V          |
| 44        | 	        | GNSS_IRQ   | GPIO_2 / IRQ / ALERT               | FACE-EX        | 1.8V          |
| 45        | GND		|            | Ground	                          |                | GND           |
| 46        | 	        | GPIO3      | GNSS_0                             | PWM2_OUT       | 1.8V          |
| 47        | PCIE TXN- |            | PCIE TXN- / PET-0 / SATA-A-        | PCIE TXN-      | 1.8V      |			
| 48        | 	        | GPIO4      | GNSS_1                             | PWM3_OUT       | 1.8V          |
| 49        | PCIE TXN+	|            | PCIE TXN+ / PET-0 / SATA-A+        | PCIE TXN+      | 1.8V      |			
| 50        |           | PERST	     | PCI Reset	                      | mPCIe_PERST    | 3.3V              |
| 51        | GND		|            | Ground                             |                | GND           |
| 52        | 	        | CLKREQ     | Reference clock request		      | PCIE_CLKREQ_B  | 3.3V         |
| 53        | REFCLK-   |            | PCIE REFCLK-	                      | REFCLK-        |              |
| 54        | 	        | WAKE       | PCIe WAKE# Active Low.	          | B_PCIE_WAKE    | 3.3V        |		
| 55        | REFCLK+   |            | PCIE REFCLK+				          | REFCLK+        |              |
| 56        | 	        | MFG_DAT    | SYS/MFG SDA                        | SYS I2C SDA    |               |	
| 57        | GND		|            | Ground                             |                |               |
| 58        | 	        | MFG_CLK    | SYS/MFG SCL                        | SYS I2C SCL    |               |
| 59        | DATA0     |            | Key M                              | SD2_DATA0      | 3.3V          |
| 60        | 	        | COEX3      | Key M                              | GPIO4_IO21     |               |
| 61        | DATA1     |            | Key M                              | SD2_DATA1      | 3.3V          |
| 62        | 	        | COEX_TXD   | Key M/Access to LoRa/ Debug Output | UART2_TXD      | 1.8V          |
| 63        | DATA2     |            | Key M                              | SD2_DATA2      | 3.3V          |
| 64        | 	        | COEX_RXD   | Key M/Access to LoRa/ Debug Output | UART2_RXD      | 1.8V          |
| 65        | DATA3     |            | Key M                              | SD2_DATA3      | 3.3V          |
| 66        | 	        |SDCMD/SIMCD | Key M / SDIO CMD / SIM DETECT      | SD2_CMD        | 3.3V          |
| 67        | RESET#	|            | RESET			                  | FACE-EX        | 1.8V         | WWAN
| 68        |           |SDCLK/SUSCLK| SDIO CLK/32.768 kHz prov. by Platform    | SD2_CLK  | +3.3V         |   			
| 69        | CONFIG_1	|            | Defines module type			+	  | FACE-EX P6.1   |               |
| 70        |           | VBAT       | VSOM/VBAT when SoM powered         |                | +3.1V - +4.4V |
| 71        | GND		|            | Ground				              |                | GND           |
| 72        |           | VBAT       | VSOM/VBAT when SoM powered         |                | +3.1V - +4.4V |
| 73        | GND		|            | Ground				              |                | GND           |
| 74        | 	        | VBAT       | VSOM/VBAT when SoM powered         |                | +3.1V - +4.4V |
| 75        | CONFIG_2  |            | Defines Module Type	NC	          | FACE-EX        |               |

3.3V is used by card to generate signals.

<mark>Sound pins are changed to pass DATA0 and use SAI5 instead of SAI3</mark>
