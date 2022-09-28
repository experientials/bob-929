Power is received from the 292 module as VSOM, SLEEP_3V3 and 5V.

VSOM will be supplied unless the system is suspended or in deep sleep.
SLEEP_3V3 will be supplied if the 292 has power regardless of the system state.
5V is a low current supply meant for HDMI.

CAM_3V3 and CAM_1V8 is supplied from SLEEP_3V3 as the camera must be able to interpret while the system sleeps.
It drives the camera system and motion sensor.

LIVE_3V3 is supplied from VSOM to be used for components with higher consumption.

