# 929 Bob (Purple, yellow and gold)

The 929 is a baseboard a.k.a. Faceboard for joining submodules for Smart Cameras, m.2 Supervisor, 
Power Delivery and System Module. It is largely derived from the [UCM i.MX8 reference board](./datasheets/i.MX8/sb-ucmimx8plus_1v1/sb-ucmimx8plus_1v1.pdf).


:[BOM](./929-BOM.md)


## Carrier Board Design Guidelines

:[UCM Design Guidelines](../refs/Compulab/DESIGN_GUIDELINES.md)


## Board Configurations

The board can be used in different configuations

1. With the Smart Camera module inserted and an i.MX8 SoM development board connected externally via cables
2. With a Power Delivery module inserted, an i.MX8 SoM development board connected that is powered from the PD module via the Faceboard.
3. With a System module, but no Power Delivery module
4. With a System module and a Power Delivery module 
5. With power passed through Misc connectors
6. With power passed through Raspberry Pi connector  

The configuration options allows development, testing and programming of individual modules

The board features to complete are

- Connecting T-USB Power Module 50 pin connectors to SoM/Dev connectors
- Smart Cam connector to SoM connector
- SD Card on Smart Cam connector
- Ethernet connector
- Temporary Micro USB power in
- [SoM UART1 - 1-Wire STEM MSG](../sys/STEM-MSG.md) - [msp-fw STEM-MSG](https://github.com/experientials/msp-fw/blob/main/STEM-MSG.md)
- SoM programming 

Features to finish in later revisions

- Sound output
- m.2 Supervisor connector
- HDMI connector
- Small e-Paper connector


## Programming the Board

How to wire up the board without a SoM.

Should UART3 be used to program the different MCUs?

SWB pins
UARTs
I2C for SYS/STEM

Over USB?


## Hardware design directions

An option is needed for embedding screw hole standoff in the PCB. Perhaps good advice can be found in [M.2 for Hackers](https://hackaday.com/2022/11/03/m-2-for-hackers-connectors/).
Would this [In-saiL standoff surface mount](https://www.alibaba.com/product-detail/SMTSO-M3-6ET-Surface-Mount-Standoffs_1600307343772.html?spm=a2700.galleryofferlist.normal_offer.d_title.6eac2e79FE5EyA) be an option?
The current design has M2.5 holes, perhaps it is better to go for M2.

Other notes

- [1.5mm hole round head LED light pipe transparent PC material light guide](https://www.alibaba.com/product-detail/1-5mm-hole-round-head-LED_62220660402.html?spm=a2700.galleryofferlist.normal_offer.d_title.54206815cLFhbL)
- [Vertical right angle 3.5mm plastic PC transparent vertical light guide](https://www.alibaba.com/product-detail/Vertical-right-angle-3-5mm-plastic_1600145498793.html?spm=a2700.galleryofferlist.normal_offer.d_title.54206815cLFhbL)
- [Factory price m2 m2.5 m3 small hex socket flat countersunk head machine thread screw for tablet pc screw](https://www.alibaba.com/product-detail/Factory-price-m2-m2-5-m3_1600676556742.html?spm=a2700.galleryofferlist.normal_offer.d_title.5c7647c3BPWJb7)
- [PC transparent Phillips round head plastic screw used to fasten the chassis ](https://www.alibaba.com/product-detail/PC-transparent-Phillips-round-head-plastic_1600476694945.html?spm=a2700.galleryofferlist.normal_offer.d_title.144d47c3mZJgkI)
- [Ultra Low Profile Hex Socket Thin Head Cup Screw](https://www.alibaba.com/product-detail/Ultra-Low-Profile-Hex-Socket-Thin_1600551446204.html?spm=a2700.galleryofferlist.normal_offer.d_title.610347c36lbkEp)



## Notes

- P1 100 pin
- P2 100 pin
- P3 Left Cam 34 pin
- P4 Right Cam 34 pin
- P5 PWR CTL
- P6 HIGH SPEED
- J3 Debug Connector
- U10 USB 3.0 mux
- U11 USB 2.0 mux
- U12 Face Expander
- U13 PCA9555 Expander
- Voltage shift U16 U17 U19 U20 U21 U22 U23 U24
- U18 Switch 8bit
- Most recent capacitor C143
- Most recent resistor R16
- Most recent diode D11
- Y1 Clock
- Q1 NPN transistor
- JP1 .. JP4 face expander jtag pads

Annotated CAP as C1.
Annotated 10128793-001RLF as U1.
Annotated 10128793-001RLF as U2.
Annotated SN74CB3Q3245PW as U3.
Annotated RT8272GSP as U4.
Annotated RT8272GSP as U5.
Annotated Supervisor M2 10128793-001RLF as U6.
Error: Duplicate items C128A 


Error: Cannot add U11 (footprint 'DSBGA_2YFFT_TEX' not found).
Error: Cannot add U10 (footprint 'HVQFN42_SOT1144-1_NXP' not found).
Error: Cannot add C102 (no footprint assigned).
Error: Cannot add C129 (no footprint assigned).
Error: Cannot add JP4 (no footprint assigned).
Error: Cannot add JP3 (no footprint assigned).
Error: Cannot add JP2 (no footprint assigned).
Error: Cannot add JP1 (no footprint assigned).
Error: Cannot add C143 (no footprint assigned).
Error: Cannot add Y1 (no footprint assigned).


## Without Power Module

When the power module isn't connected the board can be powered by VSOM or 5V downregulated.
Header pins and a regulator is added to the board to support this mode.


## Without SoM

When the SoM isn't connected to the board a development board can be connected via

- CSI1 and CSI2 connector
- USB1 and USB2 connector
- Power output 5V to USB A female
- Connecting SYS I2C, I2C3, I2C5, I2C6
- OE_CAM, OE_SOUND, SYS_EX_nINT/PD_USBC_INT, SYS_PRG
- I2S_D1, I2S_D2, I2S_SCK, I2S_LRCLK

Connecting the headers on Dev Board
