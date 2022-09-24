# 292 T-USB Module

You will revise my PCB design done with KiCAD v6. I have a schematic and basic PCB layout with the outline. 
The board takes data and power from two USB Type C connectors and routes it to two 50 pin connectors. 
In addition it has a 45 pin connector to enable extending the board with an Alt Mode signal. 

I will send you a link to the GitHub branch with the existing design. You must fork this and deliver a
Pull Request with the corrections.

You will review and fix:

- Schematic
- Component choice
- Resistor, Capacitor, Inductor, Diode sizes
- High speed signals
- PCB tolerances appropriate for JLCPCB/PCBWay manufacturing
- Footprints vs Datasheets
- good ESD/noise reduction circuits
- Update/Resolve Design checklist
- Ensure that differential pairs are routed together and balanced correctly
- Mounting half hole between the two three pin connectors
- 3D shapes

Route the board Symbols and footprints are found in https://github.com/experientials/kicad-lib.
I will need your GitHub username to give you read access.
For any changes to symbols, footprints and 3D shapes please create a GitHub Pull Request against the library.
