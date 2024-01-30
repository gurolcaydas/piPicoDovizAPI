from machine import Pin,SPI,PWM
import framebuf
import time 
import network
from time import sleep
import machine
import urequests as requests 
import ure as re

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10    
CS = 9

ssid = 'wifi'
password = 'şifre'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        #print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    #print(f'Connected on {ip}')
    return ip
class LCD_1inch44(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 128
        self.height = 128
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        

        self.WHITE  =   0xFFFF
        self.BLACK  =  0x0000
        self.GREEN  =  0x07E0
        self.RED    =  0xF800
        self.BLUE   = 0x00FF
        self.GBLUE = 0X0337
        self.YELLOW = 0xFFE0
        self.GUROLCOLOR = 0x1082
        
    def write_cmd(self, cmd):    
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36);
        self.write_data(0x70);
        
        self.write_cmd(0x3A);
        self.write_data(0x05);

         #ST7735R Frame Rate
        self.write_cmd(0xB1);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB2);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB3);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB4); #Column inversion
        self.write_data(0x07);

        #ST7735R Power Sequence
        self.write_cmd(0xC0);
        self.write_data(0xA2);
        self.write_data(0x02);
        self.write_data(0x84);
        self.write_cmd(0xC1);
        self.write_data(0xC5);

        self.write_cmd(0xC2);
        self.write_data(0x0A);
        self.write_data(0x00);

        self.write_cmd(0xC3);
        self.write_data(0x8A);
        self.write_data(0x2A);
        self.write_cmd(0xC4);
        self.write_data(0x8A);
        self.write_data(0xEE);

        self.write_cmd(0xC5); #VCOM
        self.write_data(0x0E);

        #ST7735R Gamma Sequence
        self.write_cmd(0xe0);
        self.write_data(0x0f);
        self.write_data(0x1a);
        self.write_data(0x0f);
        self.write_data(0x18);
        self.write_data(0x2f);
        self.write_data(0x28);
        self.write_data(0x20);
        self.write_data(0x22);
        self.write_data(0x1f);
        self.write_data(0x1b);
        self.write_data(0x23);
        self.write_data(0x37);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x02);
        self.write_data(0x10);

        self.write_cmd(0xe1);
        self.write_data(0x0f);
        self.write_data(0x1b);
        self.write_data(0x0f);
        self.write_data(0x17);
        self.write_data(0x33);
        self.write_data(0x2c);
        self.write_data(0x29);
        self.write_data(0x2e);
        self.write_data(0x30);
        self.write_data(0x30);
        self.write_data(0x39);
        self.write_data(0x3f);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x03);
        self.write_data(0x10);

        self.write_cmd(0xF0); #Enable test command
        self.write_data(0x01);

        self.write_cmd(0xF6); #Disable ram power save mode
        self.write_data(0x00);
            #sleep out
        self.write_cmd(0x11);
        #Turn on the LCD display
        self.write_cmd(0x29);

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0x80)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x02)
        self.write_data(0x00)
        self.write_data(0x82)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
  
if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch44()
    #color BRG
    LCD.fill(LCD.BLACK)
     
    LCD.show()
 
    
    
while True:

    LCD.hline(0,0,127,LCD.GBLUE)
    LCD.hline(0,127,128,LCD.GBLUE)
    LCD.vline(0,0,127,LCD.GBLUE)
    LCD.vline(127,0,127,LCD.GBLUE)
    LCD.text('Connecting',20,20,LCD.WHITE)
    LCD.show()
    ip = connect()
    LCD.fill_rect(1,1,126,126,LCD.BLACK)
    LCD.text('Wifi',20,20,LCD.WHITE)
    LCD.text(ip,10,35,LCD.WHITE)
    
   
   
    key0 = Pin(15,Pin.IN,Pin.PULL_UP) 
    key1 = Pin(17,Pin.IN,Pin.PULL_UP)
    key2 = Pin(2 ,Pin.IN,Pin.PULL_UP)
    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)
   
    while(1):      
        if(key0.value() == 0):
            LCD.fill_rect(1,1,126,126,LCD.GREEN) 
            
        if(key1.value() == 0):
            request = requests.get(url='http://www.tcmb.gov.tr/kurlar/today.xml')
            pattern = re.compile(r'<BanknoteBuying>(.*?)</BanknoteBuying>')
            forex_buying_rate_match = pattern.search(request.text)
            #ilk kur dolar olduğundan onu alıyor XML'den dovizleri çekerseniz bana da haber edin
            tarih_pattern = re.compile(r'Tarih="(.*?)"')
            tarih_match = tarih_pattern.search(request.text)
            tarih=tarih_match.group(1)
            
            
            if forex_buying_rate_match:
                forex_buying_rate = forex_buying_rate_match.group(1)
                tempo_str = '%s' % forex_buying_rate
            else:
                tempo_str = "---" 
            LCD.fill_rect(1,1,126,126,LCD.GUROLCOLOR)
            LCD.text(tarih,17,45,LCD.WHITE) 
            LCD.text('Dolar',17,60,LCD.WHITE)
            LCD.text(tempo_str,17,75,LCD.WHITE) 
            
        if(key2.value() == 0):
            LCD.fill_rect(1,1,126,126,LCD.RED) 
        if(key3.value() == 0):
            LCD.fill_rect(1,1,126,126,LCD.BLUE)
           
                      
        LCD.show()
    time.sleep(1)
    LCD.fill(0xFFFF)







