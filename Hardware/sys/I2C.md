## SYS I2C

SYS I2C is local to a cluster of boards where a single MCU manages simpler parts.
The master can change. If the default master is fully suspended a lower power MCU can take over mastery.
While running the SoM masters SYS, ideally with the M7.
If a SmartCam module with an RP2040 is used, it can take over SYS mastery by suspending the SoM.
All other MCUs would be slave on SYS.

Slave Devices on the SYS bus

- PD Controller for direct control by Linux Device Driver
- 2 * TCA9534 legacy I/O Expander
- SoM Power Management & RTC
- PCIe clock generator
- LED Matrix

Master Devices on the SYS bus

- i.MX8 SoM
- RP2040


## STEM I2C

Stem I2C connects MCUs together allowing to allow working as a whole.
While running the SoM will master the Stem by default, however any MCU can negotiate to become the 
master. MCUs on the Stem are,

- i.MX8 SoM Core M
- SmartCam RP2040
- SmartCam Expander MSP430
- PD Controller
- Face Expander MSP430 #1/#2


## Segmented I2C

Power Module I2C (PD Controller is master)

- BQ
- 2 * TUSB Alt Mode
- 

SmartCam I2C (Night/Right/I2C6)
While awake the i.MX8 SoM will master.
While resting it will be mastered by the RP2040 or MSP430

- IMU
- Smart Microphone
- Ambient light sensor APDS 9960
- Right Cam SCCB
