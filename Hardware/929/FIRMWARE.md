todo move to device drivers/tree


Use GPIO descriptors -> https://www.youtube.com/watch?v=lQRCDl0tFiQ

Mapping GPIO to expanders is defined in device tree


#### SYS I2C

400KHz
status okay

EEPROM 0x50, atmel, 24c08, page 16
EEPROM 0x54, atmel, 24c08, page 16
PCA9555 @ 0x20, 2 cells

#### STEM/I2C3 

100KHz
status disabled


#### Cam SBBC/I2C5

400KHz
status okay

configured image sensor AR1335AF 
mipi_csi, mclk 24MHz


### IO Expander defined as

i2c2 bus (SYS ?)

+	pca9555:pca9555@20 {
+		compatible = "nxp,pca9555";
+		gpio-controller;
+		#gpio-cells = <2>;
+		reg = <0x20>;
+	};



