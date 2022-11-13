### PD Controller I2C

The TPS PD Controller can be accessed and master various I2C busses. 
I2C1 connects to STEM as slave or master.
I2C2 is a slave on SYS, allowing an API to be exposed to the i.MX8 CPU. 
I2C3 is on the POWER I2C bus, so it can master the other chips on the T-USB power board.
The PD Controller firmware can be patched over I2C,
or the flash can be written to directly via the 50 pin connector while the board 
is otherwise not powered or the PD Ctrl is kept in a shut down state.

By default the chipsets can be controlled by Linux Device Driver Bindings(on i.MX SoM) via the SYS I2C.
The future direction is to control them by the local MSP430 MCU, which exposes information in the STEM I2C bus.


### SYS I2C

The System I2C bus is mastered by the SoM whenever it is operating. The SoM has a M7 core that runs awareness routines while
the system is resting. This means it can in principle be operating at all times. The Awareness MCUs make themselves available
on the bus. To find other MCUs the addresses 0x200 to 0x20F are scanned.
It connects to PD Controller I2C #2, which is always a slave.


### Stem I2C

The Stem I2C bus is multi-master shared by listening on the I2C bus before claiming it. 
It connects to PD Controller I2C #1, which is either master or slave.
To find other MCUs the addresses 0x200 to 0x20F are scanned.
The master will be one of the Awareness MCUs that keep the system running under the covers and updates the awareness state.
Sensors such as Ambient Light/Sound and Motion are accessed on the Stem. LED patterns are also controlled by Stem I2C.
By default 3V3.


### Day I2C

The SoM controls the Daytime camera module with range sensor via the Day I2C5 bus. MCUs do not access this bus.
By default 1V8. The sensors on the bus are on camera modules.


### Night I2C

The SoM controls the Nightime camera module with ambient sensor via the Night I2C6 bus while the system is awake. When resting
MCUs are responsible for monitoring the visual environment by using Night I2C sensors. 
If the Night Camera Module has an MCU the T-USB MCU will assume that it will do the monitoring.
By default 1V8. The sensors on the bus are on camera modules.


### Power I2C

This bus is internal to the T-USB Power board.
It can optionally be connected to the SYS I2C.
It connects to PD Controller I2C #3, which is always a master.

