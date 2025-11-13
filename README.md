# Note From the Developer

Waveshare didn’t ship any working Raspberry Pi code for this transparent OLED, and the few repos I found online were all Arduino-based or used custom microcontroller drivers. So I decided to build my own driver for Raspberry Pi fully in Python.

Why Python instead of C for a “firmware”-type project?
Honestly… because I know Python best, and I wanted something fast to prototype, easy to extend, and beginner-friendly for anyone else trying to get this display working.

Also:
The manufacturer’s wiring guide for Raspberry Pi was wrong, so getting this working required manually mapping pins, figuring out the correct SPI config, and reverse-engineering a stable init sequence. Hopefully this saves the next person a few hours (or days).

Everything else in this repo is handwritten, the only thing AI touched was sprucing up the README formatting.

Enjoy the driver. Hope it helps someone.

— Asray 

# 🟦 Waveshare 1.51" Transparent OLED Driver (Raspberry Pi)

A lightweight, Python-based driver for the **Waveshare 1.51-inch Transparent OLED (128×64, Light Blue)**, designed specifically for the **Raspberry Pi** using **SPI** and **CircuitPython GPIO**.

This library provides:

✔ Simple `.on()`, `.off()`, `.sleep()`, `.wake()` controls
✔ Easy image rendering with Pillow
✔ Full-frame buffer support
✔ Clean hardware reset
✔ Example scripts (hello, clear, shapes, on/off)
✔ Raspberry Pi–compatible SPI initialization

---

# 📦 Supported Hardware

### **Screen**

**Waveshare 1.51" Transparent OLED**

* Resolution: **128 × 64**
* Color: **Light Blue (monochrome)**
* Interfaces: **SPI / I²C (SPI used here)**
* SKU example:

  * *Waveshare 1.51inch Transparent OLED 128×64 Module*

### **Tested On**

* Raspberry Pi 3B / 3B+
* Raspberry Pi 4B
* Raspberry Pi Zero 2W

Uses standard GPIO pin numbering via Adafruit Blinka.

---

# 🔌 Wiring (Raspberry Pi → OLED)

| OLED Pin  | Raspberry Pi Pin | GPIO    |
| --------- | ---------------- | ------- |
| VCC       | 3.3V             | —       |
| GND       | GND              | —       |
| D0 (SCLK) | Physical Pin 23  | GPIO 11 |
| D1 (MOSI) | Physical Pin 19  | GPIO 10 |
| DC        | Physical Pin 18  | GPIO 24 |
| RST       | Physical Pin 22  | GPIO 25 |
| CS        | Physical Pin 24  | GPIO 8  |

SPI must be enabled:

```
sudo raspi-config
Interfacing Options → SPI → Yes
```

---

# 📥 Installation

### **Install from PyPI**

You can install the Waveshare Transparent OLED driver directly from PyPI:

```bash
pip install waveshare-transparent-oled
```

If you’re on Raspberry Pi OS (which uses PEP 668 “externally managed environments”), you may need:

```bash
pip install waveshare-transparent-oled --break-system-packages
```

---

## 📦 PyPI Link

You can view the package on PyPI here:

🔗 **[https://pypi.org/project/waveshare-transparent-oled/](https://pypi.org/project/waveshare-transparent-oled/)**

---

## Installing Locally
### 1. Install system dependencies

```
sudo apt update
sudo apt install python3-pip python3-pil python3-spidev
```

### 2. Enable Python GPIO abstraction (Blinka)

```
pip install adafruit-blinka
```

### 3. Install this library

If installing locally:

```
pip install .
```

Or after publishing:

```
pip install waveshare-transparent-oled
```

---

# 🚀 Usage Example

### **Display “Hello OLED” in white on transparent background**

```python
from waveshare_transparent_oled import OLED_1in51
from PIL import Image, ImageDraw, ImageFont

disp = OLED_1in51()
disp.Init()

img = Image.new("1", (128, 64), "white")
draw = ImageDraw.Draw(img)

font = ImageFont.load_default()
draw.text((10, 25), "Hello OLED!", fill=0)

buf = disp.getbuffer(img)
disp.ShowImage(buf)
```

---

# 🟦 Turn Display On / Off

```python
disp.on()     # Full power on
disp.off()    # Panel off
```

---

# 🌙 Sleep / Wake

```python
disp.sleep()  # Low-power mode
disp.wake()   # Restore + turn on
```

---

# 🧽 Clear the display

```python
disp.clear()
```

---

# 📁 Example Scripts

Inside the `examples/` folder:

| File             | Description                |
| ---------------- | -------------------------- |
| `hello.py`       | Static "Hello OLED" text   |
| `demo_shapes.py` | Draw rectangle/circle test |
| `on.py`          | Turn the screen ON         |
| `off.py`         | Turn the screen OFF        |
| `clear.py`       | Clear the panel            |

Run an example:

```
python3 examples/hello.py
```

---

# 🧠 How the Driver Works

* Uses **SPI** for fast frame updates
* Uses **Pillow** to generate a monochrome image
* Converts image → SSD1309-compatible buffer
* Sends 8 pages (128 bytes each) to the OLED
* Uses hardware reset for reliable startup

This driver is fully optimized for Raspberry Pi and avoids heavy overhead.

---

# 🛠 Contributing

Pull requests are welcome!
To modify the source:

```
waveshare_transparent_oled/oled_driver.py
```

---

# 📄 License

MIT License
© 2025 Asray Gopa

