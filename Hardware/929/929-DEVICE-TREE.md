## Device Tree

The 929 is a modification of the UCM i.MX8M Plus base board([Device tree, seen here](https://github.com/compulab-yokneam/meta-bsp-imx8mp/blob/8ecdaf17a8f86ab514a262d561aeddd298009f4d/recipes-kernel/linux/compulab/5.15.32/imx8mp/0003-compulab-dts-Add-device-trees.patch)).

The device tree makes the GPIOs for RESET, PWRDN and INT# on system components easily configurable.

There are multiple board definitions,

- som-imx8m-plus.dts
- som-imx8m-plus_mipi-csi1.dts
- som-imx8m-plus_mipi-csi2.dts
- ucm-imx8m-plus.dts

We should make a new board Device tree file based that includes ucm-imx8m-plus.dts and modifies or is based on imx8mp.dtsi.

Relevant Linux drivers

- [PCA953x](https://github.com/torvalds/linux/blob/master/drivers/gpio/gpio-pca953x.c)
- 

### UCM Board pin configuarations (vendor board)

This describes the original dev board behavior and the change for the 909/919/929 board.


#### UART1..4

UART1 is configured with RX TX CTS(3) RTS(3)
UART2 is configured with RX TX
UART3 is configured with RX TX CTS RTS that overlap with SPI1
UART4 doesn't seem to be configured in tree, it would be using UART2 CTS RTS

#### LVDS0 panel

Compatible with boe,hv070wsa-100
Backlit
Sets PCA9555 pin 6 to high

```
+	lvds0_panel {
+		compatible = "boe,hv070wsa-100";
+		backlight = <&lvds_backlight>;
+		enable-gpios = <&pca9555 6 GPIO_ACTIVE_HIGH>;
+
+		port {
+			panel_lvds_in: endpoint {
+				remote-endpoint = <&lvds_out>;
+			};
+		};
+	};
```

#### ECSPI2

Device name spidev1
Comptible with rohm, dh2228fv  500KHz
SPI CS uses P2.91 / GPIO5_IO13


#### Ethernet

Device as &fec / ethphy1
ENET1 nRST / GPIO4_IO4
Compatible with ethernet-phy-ieee802.3-c22


#### PCA9450

Controlled via I2C1 on address 0x25
Interrupts GPIO1_IO3 PMIC_nINT


#### Touchscreen driver GT911

It seems that the touchscreen driver supported is a [Goodix Touchscreen Linux Driver](https://gitlab.com/AdyaAdya/goodix-touchscreen-linux-driver)
[Touchscreen Controller for Tablets](https://www.goodix.com/en/product/touch_screen_control_chip).
[Linux Drivers for Generic Goodix FingerPrint Device](https://developers.goodix.com/en/bbs/detail/5134c01266c142bc88b066bf10ddc71e) no reply...
[Goodix FP Dump](https://github.com/mpi3d/goodix-fp-dump).
IRQ via USB1_TYPEC_EN_B
Reset is done via PCA9555
The device is connected to I2C5 at 400KHz

A second Goodix driver is installed for use over MIPI


#### Camera Drivers CSI1 and CSI2

Device drivers(AR1335) are set up for I2C5 and I2C6 using mipi_csi with csi_id 0x00 and 0x01
The drivers are disabled.


#### PCIe

Drivers are set up without external oscilator
Reset is done via PCA9555 0.0


#### mPCIe_PERST#

SYS I2C2 PCA9555 addr 0x20 pin 0.0

New Board: On I/O Expander 0x25 under the name M2B_PERST


#### M2_PCIE_CLKREQ# / PCIE_CLKREQ_B#

from SoM P2.90 / GPIO5_20
from M2 pin 52

#### USB1_TCPC_nINT

to SoM P1.60 / GPIO4_IO19

This is triggered by the insertion of USB-C OTG connector. Affects device driver for hd3ss3220
It is part of typec1grp

New Name: PD_USBC_INT


#### USB1_SS_SEL (Wake M2 Key B)

Triggers WAKE# on M2 Key B module
This doesn't seem to be related to USB1
Conditional config for muxing USB1 __TYPE_C__

SoM P2.52 / GPIO4_20

New Board: Changed functionality, Wake is done via Face Expander MCU


#### LVDS_DISP_RESET

SYS I2C2 PCA9555 addr 0x20 pin 0.6


#### LVDS_TOUCH_RESET

SYS I2C2 PCA9555 addr 0x20 pin 0.7


#### USB1_TYPEC_EN_B

SoM P2.49 / GPIO2_20

Is output on touch connector
Triggers Goodix interrupt

New Name: TOUCH_nINT


#### CSI1_PWR_DWN_B

SYS I2C2 PCA9555 addr 0x20 pin 1.0

#### CSI1_B_RST

SYS I2C2 PCA9555 addr 0x20 pin 1.1


#### CSI2_PWR_DWN_B

SYS I2C2 PCA9555 addr 0x20 pin 1.4


#### CSI2_B_RST

SYS I2C2 PCA9555 addr 0x20 pin 1.5


#### Various

A heartbeat LED is connected to GPIO1_12 and active LOW (is this on the SOM board?)

CAN standby pins are GPIO2_6 and GPIO2_7

A WM8731 sound chip is connected to SYS I2C2

EEPROM is connected to SYS I2C2 at 0x50 and 0x54

The definition for I2C3(STEM) is disabled.


#### SD2_nCD

How would SD Card use chip select? It only seems relevant via DATA3 or as SPI

SoM P2.92 / GPIO2_IO12
Device: usdhc2

### New Board Added GPIOs

#### M2B_PERST

This is P0 on TCA9534 Expander 0x25



#### SOUND_INT

GPIO1_IO0

#### OE_SOUND

GPIO2_IO18

#### OE_CAM

GPIO2_IO9

#### SYS_PRG# 

GPIO4_IO17 / ENET1_TXC

#### MCU_SYS_INT

GPIO4_IO16 / ENET1_TX_CTL


#### STEM_INT

to SoM P1.98 / GPIO1_IO1
