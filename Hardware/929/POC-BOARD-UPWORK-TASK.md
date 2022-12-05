# Small batch of PoC boards

The aim of the job is to create a small batch(around 10 pcs) of partly populated Faceboard PCBs to test mechanical
design and development setups. The input will be a partial design in KiCad and create a variant that maintains physical
dimensions and connector locations. The boards must also be usable for testing functionality when connected to a
[Compulab UCM i.MX8M Plus](https://mediawiki.compulab.com/w/index.php?title=UCM-iMX8M-Plus_NXP_iMX8M-Plus_Yocto_Linux) 
development board.

The work should end in a delivery of populated boards and a pull request against the GitHub repository with the existing
KiCad designs and documentation.

Milestones

1. Review and correct schema $200
2. Review and correct PCB $400
3. Produce initial batch of assembled boards $300


## The 929 Board

![Bob face](../../Face/929%20bob%20front%20straight.png)

[The 929 is a baseboard a.k.a. Faceboard](./929-MODULE.md) for joining submodules for Smart Cameras, m.2 Supervisor, 
Power Delivery and System Module. It is the eventual base for the full product.


## PoC Board

The PoC board must have the same connectors as the 929, but they don't have to be 100% functional. 98% is good enough.

Target Working functionality

- Power Delivery from Power module to components and connectors
- Power input from SW4 6-Pin Power connector as alternative to Power Module to drive the board
- Power bridging from T-USB Power module by shorting SW4 pins.
- [I2C SYS/Stem/Night/Day](../sys/I2C-BUSSES.md) between connectors
- Debugging and Firmware programming lines
- USB1 and USB2 routed from System Module to T-USB Power (and M.2 optionally)
- Wiring from SmartCam connector to System Module
- Wiring from HDMI connector to System Module
- Wiring from RJ45 Ethernet connector to System Module
- Wiring for Debug Connector
- Connecting to P20 / P21 on development board
- Some of the pins on the RPi connector should be sorted out
- Buttons for PWRBTN, RESET, ALT_BOOT
- Simple way to power the board using Micro USB instead of the power module(just for early dev)

I'd like to get suggestions for potential mechanical M2 standoff for the M.2 socket companion screw socket for tying 
the board down. I will need to screw a backplane and battery pack on to the board, so picking some good M2 screw sockets
to mount/glue on the board is quite important to me.

The board has 4 cutouts for 2 camera modules and two vertical USB-C female sockets. It also has 7 holes for fixing
submodules and a backplane to the board. 
Ideally the board will not have any other througholes to maintain an estethic look on the front.
It is also worth noting that the frontfacing copper plane on the 929 is meant to work estethicaly with some gold-plated copper exposed for decoration. A brain like layout around a Raspberry Pi compatible pinout is part of the plan.


## After the PoC Board

After the producing the PoC board we would want to used it to test the Firmware intended for the full 929 board by either
plugging in a system module or a development board.