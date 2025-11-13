from waveshare_transparent_screen_driver.oled_driver import OLED_1in51
from PIL import Image, ImageDraw

disp = OLED_1in51()
disp.Init()

img = Image.new("1", (disp.width, disp.height), "white")
draw = ImageDraw.Draw(img)

draw.rectangle((10, 10, 60, 30), outline=0, fill=0)
draw.ellipse((70, 10, 110, 50), outline=0)

buf = disp.getbuffer(img)
disp.ShowImage(buf)
