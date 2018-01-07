import pyowm
import time
import datetime
from datetime import datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#rpi pin config
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))


# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

now = datetime.now()
owm = pyowm.OWM(API_key='a2e0525a3ab947074b37ba6c33f11288')
obs = owm.weather_at_coords(44.1, -77.58)
wea = obs.get_weather()
temp = wea.get_temperature(unit='celsius')
wind = wea.get_wind()
status = wea.get_status()
dstatus = wea.get_detailed_status()
#the two following current vars are to initialise the clock vars. First referenced in main loop
currentTimeOld = 0
currentSecond = 0

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
#critical to have a '1' here for 1-bit color (on/off, no dimming)
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
#blanking drawing, full width and height no-fill rectangle
draw.rectangle((0,0,width,height), outline=0, fill=0)
font = ImageFont.load_default()

# args: left position, top start position, width, bottom position
#draw.rectangle((2, 2, 102, height-2), outline=85, fill=0)

# Write two lines of text.
def firstDisplayDraw():
	draw.text((4, 1), '00:00.00   ' + 'Cur:' + str(int(temp['temp'])), font=font, fill=255)
	draw.text((4, 10), 'Hi:' + str(int(temp['temp_max'])) + 'c Lo:' + str(int(temp['temp_min'])) + 'c',  font=font, fill=255)
	draw.text((4, 19), 'Wnd:' + str(int(wind['speed'])) + 'kph ' + str(dstatus), font=font, fill=255)
	disp.image(image)
	disp.display()

def timeupdate():
	draw.rectangle((4,1,60,9), outline=0, fill=0)
	draw.text((4, 1), str(currentTime), font=font, fill=255)
	disp.image(image)
	disp.display()



firstDisplayDraw()


while True:


#START TIME VAR ESTABLISHMENT
	now = datetime.now()
	if int(currentSecond) != now.second:


		currentHour = now.hour - 5
		if currentHour < 1:
			currentHour += 12
		if len(str(currentHour)) == 1:
			currentHour = ' ' + str(currentHour)

		currentMinute = now.minute
		if len(str(currentMinute)) == 1:
			currentMinute = '0' + str(currentMinute)

		currentSecond = now.second
		if len(str(currentSecond)) == 1:
			currentSecond = '0' + str(currentSecond)

		currentTime = str(currentHour) + ':' + str(currentMinute) + '.' + str(currentSecond)

		if currentTime != currentTimeOld:
			currentTimeOld = currentTime
			timeupdate()

#	inputForInterrupt = input('enter some text but plz don\'t hit enter for a few minutes')

