# ePaper Pi for Home Assistant
A HomeAssistant-connected Raspberry Pi showing useful information on an e-paper display.

## Hardware Setup

Parts List:

- [Adafruit 2.13" Monochrome E-Ink Bonnet for Raspberry Pi](https://www.adafruit.com/product/4687)
- Raspberry Pi Zero W
- SD card
- Power supply

## Installation

1. Prepare the Raspberry Pi Zero:
  - Download and flash Raspberry Pi OS Lite onto your SD card
1. TODO 

https://learn.adafruit.com/2-13-in-e-ink-bonnet/usage
pip install python-dotenv
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip
sudo apt install --upgrade python3-setuptools
pip3 install adafruit-circuitpython-epd
wget https://github.com/adafruit/Adafruit_CircuitPython_framebuf/raw/main/examples/font5x8.bin
sudo apt-get install fonts-dejavu
sudo apt-get install python3-pil
pip install HomeAssistant-API
from PIL import Image, ImageDraw, ImageFont
sudo apt install fonts-dejavu-core 
install git clone repo

## Configuration

Copy the `.env.example` file to `.env` and fill in the variables as needed.

## Developing

### Building Components

#### `fetch_data` Method

#### `render` Method

To accelerate local development of views, you can simply render the component to a png and show the result using a mock, e.g. for a sensor:
```python
from unittest.mock import Mock
from components.sensor import Sensor
s = Sensor("test", (250, 122))
s._has_content = True

s.entity = Mock()
s.entity.state = 42
... # set all other required data

# call this every time you change something about the render method
img = s.render()

# this should open a window with the image rendered,
# call this again after calling s.render()
img.show() 
```