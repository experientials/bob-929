The development board uses a single Expander. The 909 and 801 uses 2x PCA9555 to control more states

The system expander #0 is used by the SoM via SYS I2C.
The system expander input triggers interrupt via SYS_EX_nINT (GPIO4_IO19).
This expander deals with activity relevant during waking state.

This first expander, which is also on the dev. board maps,

| Expander  | Connected to    |
|-----------|-----------------|
| EX0.0     | IO0_0 mPCIe_PERST on M2 Key B    |
| EX0.1     | - reserved for second mPCIe -   |
| EX0.2     | IO0_2 MCU_SYS_INT from T-USB module or other MCUs               |
| EX0.3     |                       |
| EX0.4     |                       |
| EX0.5     |                       |
| EX0.6     | IO0_6 LVDS_DISP_RESET   |
| EX0.7     | IO0_7 LVDS_TOUCH_RESET  |
| EX0.8     | IO1_0 CSI1_PWR_DWN_B  |
| EX0.9     | IO1_1 LEFT_CAM_RESET  |
| EX0.10    | IO1_2 LEFT_ATT_INT    |
| EX0.11    | IO1_3 LEFT_ATT_XSHUT  |
| EX0.12    | IO1_4 CSI2_PWR_DWN_B  |
| EX0.13    | IO1_5 RIGHT_CAM_RESET |
| EX0.14    | IO1_6 RIGHT_ATT_INT   |
| EX0.15    | IO1_7 RIGHT_ATT_XSHUT |

