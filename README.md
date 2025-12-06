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
