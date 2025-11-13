from waveshare_transparent_oled.oled_driver import OLED_1in51
from PIL import Image, ImageDraw, ImageFont
import time

disp = OLED_1in51()
disp.Init()

image = Image.new("1", (disp.width, disp.height), "white")
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()
draw.text((20, 20), "HELLO", font=font, fill=0)

buf = disp.getbuffer(image)
disp.ShowImage(buf)

time.sleep(5)
disp.off()
