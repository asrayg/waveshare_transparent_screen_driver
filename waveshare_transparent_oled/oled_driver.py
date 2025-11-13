python3 - << 'EOF'
import time
import board
import digitalio
import busio
from PIL import Image, ImageDraw, ImageFont


OLED_WIDTH  = 128
OLED_HEIGHT = 64


class OLED_1in51:
    def __init__(self):
        # SPI
        self.spi = busio.SPI(board.SCLK, MOSI=board.MOSI)

        # Pins
        self.dc = digitalio.DigitalInOut(board.D24)
        self.rst = digitalio.DigitalInOut(board.D25)
        self.cs = digitalio.DigitalInOut(board.D8)
        for pin in [self.dc, self.rst, self.cs]:
            pin.direction = digitalio.Direction.OUTPUT

        # Configure SPI
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=8000000, phase=0, polarity=0)
        self.spi.unlock()

        self.width = OLED_WIDTH
        self.height = OLED_HEIGHT

    def command(self, cmd):
        self.dc.value = 0
        self.cs.value = 0
        self.spi.write(bytes([cmd]))
        self.cs.value = 1

    def data(self, data):
        self.dc.value = 1
        self.cs.value = 0
        self.spi.write(data)
        self.cs.value = 1


    def reset(self):
        print("Testing RST pin (should cause one clean flash)...")
        self.rst.value = 0
        time.sleep(0.2)
        self.rst.value = 1
        time.sleep(0.2)

    def off(self):
        """Turn OLED panel OFF (no pixels lit, still powered)"""
        self.command(0xAE)

    def on(self):
        """Turn OLED panel ON"""
        self.command(0xAF)

    def sleep(self):
        """Enter low-power mode"""
        self.command(0xAE)
        self.command(0x8D)
        self.data([0x10])

    def wake(self):
        """Wake from low-power mode"""
        self.command(0xAE)
        self.command(0x8D)
        self.data([0x14])
        self.command(0xAF)

    def Init(self):
        print("Sending OLED init sequence...")
        self.reset()
        cmds = [
            0xAE, 0xD5, 0xA0, 0xA8, 0x3F, 0xD3, 0x00,
            0x40, 0xA1, 0xC8, 0xDA, 0x12, 0x81, 0x7F,
            0xA4, 0xA6, 0xD9, 0xF1, 0xDB, 0x40, 0xAF
        ]
        for c in cmds:
            self.command(c)
        print("Init complete.\n")

    def getbuffer(self, image):
        buf = [0x00] * (self.width * self.height // 8)
        img = image.convert("1")
        pixels = img.load()
        for y in range(self.height):
            for x in range(self.width):
                if pixels[x, y] == 0:
                    buf[x + (y // 8) * self.width] |= (1 << (y % 8))
        return buf

    def ShowImage(self, buf):
        """Send a full frame buffer to the display"""
        for page in range(8):
            self.command(0xB0 + page)  
            self.command(0x00)
            self.command(0x10)

            start = page * 128
            end   = start + 128
            self.data(buf[start:end])

    def clear(self):
        """Clear the display"""
        blank = [0x00] * (self.width * self.height // 8)
        self.ShowImage(blank)


disp = OLED_1in51()
disp.Init()


# TEST 1: FULL BLUE
print("TEST 1: Filling screen with BLUE...")
img1 = Image.new("1", (128, 64), "black")  # black → blue
buf1 = disp.getbuffer(img1)
disp.ShowImage(buf1)
time.sleep(2)

print(">>> Does the screen become FULL BLUE without flickering? (yes/no)")
time.sleep(0.5)


# TEST 2: CHECKERBOARD
print("\nTEST 2: Checkerboard pattern...")
img2 = Image.new("1", (128, 64), "white")
draw2 = ImageDraw.Draw(img2)
for y in range(0, 64, 8):
    for x in range(0, 128, 8):
        if (x//8 + y//8) % 2 == 0:
            draw2.rectangle((x, y, x+7, y+7), fill="black")
buf2 = disp.getbuffer(img2)
disp.ShowImage(buf2)
time.sleep(2)

print(">>> Does the checkerboard look stable? Any vertical/horizontal missing lines?")


# TEST 3: Static HELLO
print("\nTEST 3: Static HELLO text...")
img3 = Image.new("1", (128, 64), "white")
draw3 = ImageDraw.Draw(img3)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
draw3.text((20, 18), "HELLO", fill="black")
buf3 = disp.getbuffer(img3)
disp.ShowImage(buf3)

print(">>> Does it show stable HELLO letters with no flicker?")


print("\n=== TEST COMPLETE ===")
print("Tell me the result of:")
print("1. Full blue test")
print("2. Checkerboard test")
print("3. HELLO test\n")
EOF