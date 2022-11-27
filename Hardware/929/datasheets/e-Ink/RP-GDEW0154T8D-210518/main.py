import machine
import utime
#EPD GPIO
isEPD_W21_BUSY=machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN) #BUSY
EPD_W21_RST= machine.Pin(1, machine.Pin.OUT)#RESE
EPD_W21_DC= machine.Pin(2, machine.Pin.OUT)#DC
EPD_W21_CS= machine.Pin(3, machine.Pin.OUT)#CS
#SPI0
spi_sck=machine.Pin(6) #SCLK
spi_tx=machine.Pin(7)#SDIN
spi_rx=machine.Pin(4)
spi=machine.SPI(0,baudrate=10000000,sck=spi_sck, mosi=spi_tx, miso=spi_rx) #10Mhz

#LED
led_onboard = machine.Pin(25, machine.Pin.OUT)


#PICTURE
gImage_1 =[
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,
0XFF,0XFF,0XFC,0X01,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFC,0XFF,0XFF,0XF0,0X00,0X7F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XC1,0XFE,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFE,0X3F,0XFF,0XE3,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFC,0X7F,0XFF,
0XF1,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,
0XFC,0XFF,0XFF,0XF9,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFC,0XFF,0XF9,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XF3,0XFF,0XFF,0XFC,0X7F,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XE3,0XFF,0XFF,0XFE,0X7F,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XE7,0XFF,0XFF,0XFF,
0X3F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XE6,
0X00,0X07,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,
0XFC,0XFF,0XCE,0X0F,0X87,0XFF,0X9F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,
0X80,0X00,0XFF,0XFC,0XFF,0XCE,0X0F,0X83,0XFF,0X9F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFE,0X01,0X80,0X00,0XFF,0XFC,0XFF,0XCE,0X0F,0X83,0XFF,0X9F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0X80,0X00,0XFF,0XFC,0XFF,0X9E,0X0F,0X83,0XE7,0XCF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0XC0,0X00,0XFF,0XFC,0XFF,0X9E,0X0F,
0XC3,0XE7,0XCF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0XFF,0X80,0XFF,0XFC,
0XFF,0X9E,0X0F,0XC7,0XE7,0XCF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0XFF,
0X80,0XFF,0XFC,0XFF,0X9E,0X0F,0XC7,0XE7,0XCF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0X9E,0X0F,0XFF,0XE7,0XCF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0X9E,0X0F,0XFF,0XE7,0XCF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,0X7E,0X00,0XFF,0XFC,0XFF,0X9E,0X0F,0XFF,
0XE7,0XCF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,0XFF,0X00,0XFF,0XFC,0XFF,
0X9E,0X0F,0XFF,0XE7,0XCF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0XDB,0X80,
0XFF,0XFC,0XFF,0XDE,0X0F,0XFF,0XFF,0X9F,0XFF,0XFF,0XFF,0XDF,0XFF,0XFF,0XFF,0XFE,
0X01,0X99,0X80,0XFF,0XFC,0XFF,0XCE,0X00,0X03,0XFF,0X9F,0XFF,0XFF,0XFF,0XC7,0XFF,
0XFF,0XFF,0XFE,0X01,0X99,0X80,0XFF,0XFC,0XFF,0XCF,0XFF,0XC3,0XFF,0X1F,0XFF,0XFF,
0XFF,0XE1,0XFF,0XFF,0XFF,0XFE,0X01,0XDB,0X80,0XFF,0XFC,0XFF,0XE7,0XFF,0XC3,0XFF,
0X3F,0XFF,0XFF,0XFF,0XF8,0X0F,0XFF,0XFF,0XFE,0X00,0XFF,0X00,0XFF,0XFC,0XFF,0XE3,
0XFF,0XC3,0XFE,0X7F,0XFF,0XFF,0XFF,0XF8,0X0F,0XFF,0XFF,0XFE,0X00,0X7E,0X00,0XFF,
0XFC,0XFF,0XF3,0XFF,0XC3,0XFC,0X7F,0XFF,0XFF,0XFF,0XE1,0XFF,0XFF,0XFF,0XFE,0X00,
0X00,0X00,0XFF,0XFC,0XFF,0XF9,0XFF,0XC3,0XFC,0XFF,0XFF,0XFF,0XFF,0XC7,0XFF,0XFF,
0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XF8,0XFF,0XC3,0XF8,0XFF,0XFF,0XFF,0XFF,
0XDF,0XFF,0XFF,0XFF,0XFE,0X01,0XE0,0X00,0XFF,0XFC,0XFF,0XFE,0X7F,0XE7,0XF1,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0XFC,0X00,0XFF,0XFC,0XFF,0XFE,0X1F,
0XFF,0XC3,0XFF,0XFF,0XFF,0XFF,0XFF,0XCF,0XFF,0XFF,0XFE,0X00,0X3F,0X00,0XFF,0XFC,
0XFF,0XFF,0X8F,0XFF,0X8F,0XFF,0XFF,0XFF,0XFF,0XFF,0X0F,0XFF,0XFF,0XFE,0X00,0X0F,
0XC0,0XFF,0XFC,0XFF,0XFF,0XE0,0X00,0X7F,0XFF,0XFF,0XFF,0XFF,0XFC,0X3F,0XFF,0XFF,
0XFE,0X00,0X07,0XE0,0XFF,0XFC,0XFF,0XFF,0XFC,0X03,0XFF,0XFF,0XFF,0XFF,0XFF,0XE0,
0X7F,0XFF,0XFF,0XFE,0X00,0X3F,0X70,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XC3,0X7F,0XFF,0XFF,0XFE,0X01,0XFC,0X30,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XC3,0X7F,0XFF,0XFF,0XFE,0X01,0XE0,0X30,0XFF,0XFC,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XE0,0X7F,0XFF,0XFF,0XFE,0X00,0X00,0X00,
0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0X3F,0XFF,0XFF,0XFE,
0X00,0XFF,0X80,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0X0F,
0XFF,0XFF,0XFE,0X01,0XFF,0X80,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XCF,0XFF,0XFF,0XFE,0X01,0XB3,0X80,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XEF,0XFF,0XFF,0XFE,0X01,0XB9,0X80,0XFF,0XFC,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XEF,0XFF,0XFF,0XFE,0X01,0X99,0X80,0XFF,
0XFC,0XFF,0XFF,0XFC,0X01,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XEF,0XFF,0XFF,0XFE,0X01,
0XD9,0X80,0XFF,0XFC,0XFF,0XFF,0XF0,0X00,0X3F,0XFF,0XFF,0XFF,0XFF,0XFF,0XEF,0XFF,
0XFF,0XFE,0X00,0XFF,0X80,0XFF,0XFC,0XFF,0XFF,0XC1,0XFE,0X0F,0XFF,0XFF,0XFF,0XFF,
0XC0,0X0F,0XFF,0XFF,0XFE,0X00,0X6F,0X00,0XFF,0XFC,0XFF,0XFF,0X8F,0XFF,0XC7,0XFF,
0XFF,0XFF,0XFF,0XC0,0X0F,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XFF,0X7F,
0XFF,0XF9,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,
0XFF,0XFE,0X7F,0XFF,0XF9,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X0F,0XFF,
0X80,0XFF,0XFC,0XFF,0XFC,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XE1,0XFF,0XFF,0XFF,
0XFE,0X0F,0XFF,0X80,0XFF,0XFC,0XFF,0XF9,0XFF,0XFF,0XFC,0X7F,0XFF,0XFF,0XFF,0XC0,
0XFF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XF3,0XFF,0XFF,0XFE,0X7F,0XFF,
0XFF,0XFF,0XDE,0XFF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XF3,0XFF,0XFF,
0XFF,0X3F,0XFF,0XFF,0XFF,0XDE,0XFF,0XFF,0XFF,0XFE,0X00,0X7E,0X00,0XFF,0XFC,0XFF,
0XF3,0X00,0X03,0XFF,0X3F,0XFF,0XFF,0XFF,0XDE,0XFF,0XFF,0XFF,0XFE,0X00,0XFF,0X00,
0XFF,0XFC,0XFF,0XE7,0X07,0XC3,0XFF,0X9F,0XFF,0XFF,0XFF,0XDE,0XFF,0XFF,0XFF,0XFE,
0X01,0XC3,0X80,0XFF,0XFC,0XFF,0XE7,0X07,0XC1,0XFF,0X9F,0XFF,0XFF,0XFF,0XC0,0X0F,
0XFF,0XFF,0XFE,0X01,0X81,0X80,0XFF,0XFC,0XFF,0XCF,0X07,0XC1,0XF7,0XDF,0XFF,0XFF,
0XFF,0XC0,0X0F,0XFF,0XFF,0XFE,0X01,0X81,0X80,0XFF,0XFC,0XFF,0XCF,0X07,0XC1,0XF7,
0XCF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0XC3,0X80,0XFF,0XFC,0XFF,0XCF,
0X07,0XC1,0XF7,0XCF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0XFF,0XF0,0XFF,
0XFC,0XFF,0XCF,0X07,0XC1,0XF7,0XCF,0XFF,0XFF,0XFF,0XE7,0X1F,0XFF,0XFF,0XFE,0X01,
0XFF,0XF0,0XFF,0XFC,0XFF,0XCF,0X07,0XE3,0X00,0X4F,0XFF,0XFF,0XFF,0XC6,0X0F,0XFF,
0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XCF,0X07,0XFF,0X00,0X4F,0XFF,0XFF,0XFF,
0XDE,0XEF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XCF,0X07,0XFF,0XF7,0XCF,
0XFF,0XFF,0XFF,0XDC,0XEF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XCF,0X07,
0XFF,0XF7,0XCF,0XFF,0XFF,0XFF,0XDD,0XEF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,
0XFF,0XCF,0X07,0XFF,0XF7,0XCF,0XFF,0XFF,0XFF,0XDD,0XEF,0XFF,0XFF,0XFE,0X00,0X00,
0X00,0XFF,0XFC,0XFF,0XEF,0X07,0XFF,0XF7,0X9F,0XFF,0XFF,0XFF,0XC1,0X8F,0XFF,0XFF,
0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XE7,0X07,0XC7,0XFF,0X9F,0XFF,0XFF,0XFF,0XE3,
0X9F,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XE7,0X00,0X03,0XFF,0X9F,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XE7,0XFF,0XC3,
0XFF,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,0X66,0X00,0XFF,0XFC,0XFF,
0XF3,0XFF,0XC1,0XFF,0X3F,0XFF,0XFF,0XFF,0XC0,0X0F,0XFF,0XFF,0XFE,0X00,0XE7,0X00,
0XFF,0XFC,0XFF,0XF9,0XFF,0XC1,0XFE,0X7F,0XFF,0XFF,0XFF,0XC0,0X0F,0XFF,0XFF,0XFE,
0X01,0XC3,0X80,0XFF,0XFC,0XFF,0XF9,0XFF,0XC1,0XFE,0X7F,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFE,0X01,0X81,0X80,0XFF,0XFC,0XFF,0XFC,0XFF,0XC1,0XFC,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0X81,0X80,0XFF,0XFC,0XFF,0XFC,0X7F,0XC3,0XF9,
0XFF,0XFF,0XFF,0XFF,0XF0,0X3F,0XFF,0XFF,0XFE,0X01,0XC3,0X80,0XFF,0XFC,0XFF,0XFF,
0X7F,0XE3,0XF9,0XFF,0XFF,0XFF,0XFF,0XE0,0X1F,0XFF,0XFF,0XFE,0X00,0XFF,0X00,0XFF,
0XFC,0XFF,0XFF,0X8F,0XFF,0XC7,0XFF,0XFF,0XFF,0XFF,0XCF,0XCF,0XFF,0XFF,0XFE,0X00,
0X7E,0X00,0XFF,0XFC,0XFF,0XFF,0XC1,0XFE,0X0F,0XFF,0XFF,0XFF,0XFF,0XDF,0XEF,0XFF,
0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XFF,0XF0,0X00,0X3F,0XFF,0XFF,0XFF,0XFF,
0XDF,0XEF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XFF,0XFC,0X01,0XFF,0XFF,
0XFF,0XFF,0XFF,0XDF,0XEF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XC0,0X0F,0XFF,0XFF,0XFE,0X0D,0XFF,0X80,0XFF,0XFC,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XC0,0X0F,0XFF,0XFF,0XFE,0X0D,0XFF,
0X80,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFE,0X00,0XCF,0X00,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0XDF,0X80,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0X99,0X80,0XFF,0XFC,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X01,0X99,0X80,
0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,
0X01,0X99,0X80,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFE,0X01,0XFB,0X80,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XF0,0X3F,0XFF,0XFF,0XFE,0X00,0XF3,0X00,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XE0,0X1F,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XCF,0XCF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,
0XFC,0XFF,0XFF,0XFF,0XF9,0XFF,0XFF,0XFF,0XFF,0XFF,0XDF,0XEF,0XFF,0XFF,0XFE,0X01,
0XFF,0X80,0XFF,0XFC,0XFF,0XFF,0XFF,0XF8,0XFF,0XFF,0XFF,0XFF,0XFF,0XDF,0XEF,0XFF,
0XFF,0XFE,0X01,0XFF,0X80,0XFF,0XFC,0XFF,0XFF,0XFF,0XF8,0X7F,0XFF,0XFF,0XFF,0XFF,
0XDF,0XEF,0XFF,0XFF,0XFE,0X00,0X03,0X80,0XFF,0XFC,0XFF,0XFF,0XFF,0XF9,0X1F,0XFF,
0XFF,0XFF,0XFF,0XC0,0X0F,0XFF,0XFF,0XFE,0X00,0X01,0X80,0XFF,0XFC,0XFF,0XFF,0XFF,
0XF9,0X87,0XFF,0XFF,0XFF,0XFF,0XC0,0X0F,0XFF,0XFF,0XFE,0X00,0X01,0X80,0XFF,0XFC,
0XFF,0XFF,0XFF,0XF9,0XE1,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,0X01,
0X80,0XFF,0XFC,0XFF,0XFF,0XF0,0X01,0XF0,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFE,0X01,0XFF,0X80,0XFF,0XFC,0XFF,0XFF,0XF0,0X01,0XFC,0X3F,0XFF,0XFF,0XFF,0XF0,
0X3F,0XFF,0XFF,0XFE,0X01,0XFF,0X00,0XFF,0XFC,0XFF,0XFF,0XF3,0XFF,0XFF,0X1F,0XFF,
0XFF,0XFF,0XE0,0X1F,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0XFF,0XF3,0XFF,
0XFF,0XC7,0XFF,0XFF,0XFF,0XCF,0XCF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,
0X00,0X03,0XFF,0XFF,0XC3,0XFF,0XFF,0XFF,0XDF,0XEF,0XFF,0XFF,0XFE,0X0F,0XFF,0X80,
0XFF,0XFC,0XFF,0X00,0X03,0XFF,0XFF,0X0F,0XFF,0XFF,0XFF,0XDF,0XEF,0XFF,0XFF,0XFE,
0X0F,0XFF,0X80,0XFF,0XFC,0XFF,0X3F,0XF3,0XFF,0XFE,0X1F,0XFF,0XFF,0XFF,0XDF,0XEF,
0XFF,0XFF,0XFE,0X07,0XC0,0X00,0XFF,0XFC,0XFF,0X3F,0XF0,0X01,0XF8,0X7F,0XFF,0XFF,
0XFF,0XCF,0XCF,0XFF,0XFF,0XFE,0X01,0XF0,0X00,0XFF,0XFC,0XFF,0X3F,0XF0,0X01,0XF1,
0XFF,0XFF,0XFF,0XFF,0XE0,0X1F,0XFF,0XFF,0XFE,0X00,0X7E,0X00,0XFF,0XFC,0XFF,0X3F,
0XFF,0XF9,0XC3,0XFF,0XFF,0XFF,0XFF,0XF0,0X3F,0XFF,0XFF,0XFE,0X00,0X1F,0X80,0XFF,
0XFC,0XFF,0X00,0X0F,0XF9,0X0F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,
0X0F,0X80,0XFF,0XFC,0XFF,0X00,0X0F,0XF8,0X1F,0XFF,0XFF,0XFF,0XFF,0XF0,0X3F,0XFF,
0XFF,0XFE,0X00,0X7E,0X00,0XFF,0XFC,0XFF,0X3F,0XCF,0XF8,0X3F,0XFF,0XFF,0XFF,0XFF,
0XE0,0X1F,0XFF,0XFF,0XFE,0X01,0XF8,0X00,0XFF,0XFC,0XFF,0X3F,0XCF,0XF9,0X3F,0XFF,
0XFF,0XFF,0XFF,0XCF,0XCF,0XFF,0XFF,0XFE,0X07,0XC0,0X00,0XFF,0XFC,0XFF,0X20,0X0F,
0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,0XDF,0XEF,0XFF,0XFF,0XFE,0X0F,0XFF,0X80,0XFF,0XFC,
0XFF,0X20,0X0F,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,0XDF,0XEF,0XFF,0XFF,0XFE,0X0F,0XFF,
0X80,0XFF,0XFC,0XFF,0X20,0X0F,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,0XDF,0XEF,0XFF,0XFF,
0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0X20,0X0F,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,0XCF,
0XCF,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0X3F,0XCF,0XFF,0X3F,0XFF,0XFF,
0XFF,0XFF,0XE0,0X1F,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,0X3F,0XCF,0XFF,
0X3F,0XFF,0XFF,0XFF,0XFF,0XF0,0X3F,0XFF,0XFF,0XFE,0X00,0X00,0X00,0XFF,0XFC,0XFF,
0X3F,0XCF,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFE,0X00,0X00,0X00,
0XFF,0XFC,0XFF,0X3F,0XCF,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0X3F,0XCF,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,0XF6,0X3F,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0X3F,0XCF,0XFF,0X3F,0XFF,0XFF,0XFF,
0XFF,0XE6,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0X3F,0XCF,0XFF,0X3F,
0XFF,0XFF,0XFF,0XFF,0XCE,0XCF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0X3F,
0XCF,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,0XDE,0XEF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFC,0XFF,0X00,0X0F,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,0XDE,0XEF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFC,0XFF,0X3F,0XFF,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,0XDF,0XEF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0X3F,0XFF,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,
0XCF,0XCF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0X3F,0XFF,0XFF,0X3F,0XFF,
0XFF,0XFF,0XFF,0XE0,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0X00,0X00,
0X00,0X3F,0XFF,0XFF,0XFF,0XFF,0XF0,0X3F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,
0XFF,0X00,0X00,0X00,0X3F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFC,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFC,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,]









#SPI#####################
def SPI_Write(data):
    spi.write(chr(data))			

def EPD_W21_WriteCMD(command):
    EPD_W21_CS.value(0) #CS                
    EPD_W21_DC.value(0) #DC		
    SPI_Write(command)# command write
    EPD_W21_CS.value(1) #CS  

def EPD_W21_WriteDATA(data):
    EPD_W21_CS.value(0) #CS                       
    EPD_W21_DC.value(1) #DC			
    SPI_Write(data)  # data write
    EPD_W21_CS.value(1) #CS  

#EPD IC RESET
def EPD_W21_Init():
    EPD_W21_RST.value(0) # Module reset
    utime.sleep(0.01)   #At least 10ms delay 
    EPD_W21_RST.value(1)
    utime.sleep(0.01)   #At least 10ms delay 

    EPD_W21_RST.value(0) # Module reset
    utime.sleep(0.01)   #At least 10ms delay 
    EPD_W21_RST.value(1)
    utime.sleep(0.01)   #At least 10ms delay 

    EPD_W21_RST.value(0) # Module reset
    utime.sleep(0.01)   #At least 10ms delay 
    EPD_W21_RST.value(1)
    utime.sleep(0.01)   #At least 10ms delay 
#BUSY
def lcd_chkstatus():
    while isEPD_W21_BUSY.value()==0: #0 is busy
        utime.sleep(0.01) 
#UC8151D init
def EPD_init():
    EPD_W21_Init()  #Electronic paper IC reset

    EPD_W21_WriteCMD(0x04)  
    lcd_chkstatus()#waiting for the electronic paper IC to release the idle signal

    EPD_W21_WriteCMD(0x00)	    #panel setting
    EPD_W21_WriteDATA(0x1f)		#LUT from OTP£¬KW-BF   KWR-AF	BWROTP 0f	BWOTP 1f

    EPD_W21_WriteCMD(0x61)	  #resolution setting
    EPD_W21_WriteDATA (0x98)   #152     	 
    EPD_W21_WriteDATA (0x00)   #152
    EPD_W21_WriteDATA (0x98)	

    EPD_W21_WriteCMD(0X50)			#VCOM AND DATA INTERVAL SETTING			
    EPD_W21_WriteDATA(0x97)		#WBmode:VBDF 17|D7 VBDW 97 VBDB 57		WBRmode:VBDF F7 VBDW 77 VBDB 37  VBDR B7
#display 
def PIC_display(picData):
    #Write Data
    EPD_W21_WriteCMD(0x10)       #Transfer old data
    for i in range(2888):
        EPD_W21_WriteDATA(0xff)

    EPD_W21_WriteCMD(0x13);		     #Transfer new data
    for i in range(2888):     
        EPD_W21_WriteDATA(picData[i]) #Transfer the actual displayed data

    #Refresh
    EPD_W21_WriteCMD(0x12)		#DISPLAY REFRESH 	
    utime.sleep(0.01)	        #!!!The delay here is necessary, 200uS at least!!! 
    lcd_chkstatus()          #waiting for the electronic paper IC to release the idle signal
#Clear screen
def PIC_display_Clear():
    #Write Data
    EPD_W21_WriteCMD(0x10)	       #Transfer old data
    for i in range(2888):  	
        EPD_W21_WriteDATA(0xFF) 
        EPD_W21_WriteCMD(0x13)		     #Transfer new data
    for i in range(2888):       
        EPD_W21_WriteDATA(0xFF)  #Transfer the actual displayed data
    #Refresh
    EPD_W21_WriteCMD(0x12)		#DISPLAY REFRESH 	
    utime.sleep(0.01)	             #!!!The delay here is necessary, 200uS at least!!!     
    lcd_chkstatus()         #waiting for the electronic paper IC to release the idle signal
#Enter deep sleep mode 
def EPD_sleep(): 
    EPD_W21_WriteCMD(0X50)  #VCOM AND DATA INTERVAL SETTING			
    EPD_W21_WriteDATA(0xf7) #WBmode:VBDF 17|D7 VBDW 97 VBDB 57		WBRmode:VBDF F7 VBDW 77 VBDB 37  VBDR B7	

    EPD_W21_WriteCMD(0X02)  	#power off
    lcd_chkstatus()          #waiting for the electronic paper IC to release the idle signal
    EPD_W21_WriteCMD(0X07)  	#deep sleep
    EPD_W21_WriteDATA(0xA5)
 
 
#Main function part
while True:    
    #Picture
    EPD_init() #EPD init
    PIC_display(gImage_1)#EPD Clear
    EPD_sleep()#EPD_sleep,Sleep instruction is necessary, please do not delete!!!
    utime.sleep(3) #delay 3s

    #Clear
    EPD_init() #EPD init
    PIC_display_Clear()#EPD Clear
    EPD_sleep()#EPD_sleep,Sleep instruction is necessary, please do not delete!!!
    utime.sleep(1) #delay 1s
    
    while 1: 
        led_onboard.toggle()
        utime.sleep(1) #delay 1s



 
    
    
    

   
    
    
    
