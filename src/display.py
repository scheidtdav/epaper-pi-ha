import asyncio
import digitalio
import busio
import board
import os
import json
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1675 import Adafruit_SSD1675
from homeassistant_api import Client
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

from post_its import handle_post_its
from weather import handle_weather

# ----------------------------------------------------------
# Setup
# ----------------------------------------------------------
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)
srcs = None
up_button = digitalio.DigitalInOut(board.D5)
up_button.switch_to_input()
down_button = digitalio.DigitalInOut(board.D6)
down_button.switch_to_input()
display = Adafruit_SSD1675(
    122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=srcs, rst_pin=rst, busy_pin=busy
)
display.rotation = 1

icon_font = ImageFont.truetype("./meteocons.ttf", 36)
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
regular_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
large_font = ImageFont.truetype("/usr/share/fonts/truetyoe/dejavu/DejaVuSans.ttf", 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DISPLAY_UPDATE_TIMEOUT = 300  # you should not update more often than every 5 mins
DATA_UPDATE_TIMEOUT = 40
BUTTON_UPDATE_TIMEOUT = 0.05

ENTITY_STATES = []
POST_ITS = []


# ----------------------------------------------------------
# Utility functions
# ----------------------------------------------------------
def button_pressed(btn):
    """Checks whether the given button is pressed or not."""
    # Since buttons are pulled low when pressed,
    # their value is False when pressed
    if not btn.value:
        return True


async def update_display():
    while True:
        print(ENTITY_STATES)
        print(POST_ITS)

        image = Image.new("RGB", (display.width, display.height), color=WHITE)
        draw = ImageDraw.Draw(image)
        display.fill(Adafruit_EPD.WHITE)

        if len(ENTITY_STATES) == 0:
            draw.text(
                (1, 1), "Loading states, please wait...", font=small_font, fill=BLACK
            )
        else:
            for entity in ENTITY_STATES:
                # WEATHER
                if entity.entity_id.startswith("weather"):
                    weather_entity = ENTITY_STATES[0]
                    handle_weather(weather_entity, draw)

                # "POST ITs"
                if entity.entity_id.startswith("todo"):
                    post_it_entity = ENTITY_STATES[2]
                    post_it_context = POST_ITS[0]
                    handle_post_its(post_it_entity, post_it_context, draw)

        display.image(image)
        display.display()

        await asyncio.sleep(DISPLAY_UPDATE_TIMEOUT)


async def handle_buttons():
    while True:
        if button_pressed(up_button):
            print("up")

        if button_pressed(down_button):
            print("down")

        await asyncio.sleep(BUTTON_UPDATE_TIMEOUT)


async def fetch_data():
    async with Client(HA_URL, HA_TOKEN, use_async=True) as client:
        while True:
            new_states = []
            new_post_its = []
            for i in ENTITY_IDS:
                new_states.append(await client.async_get_state(entity_id=i))

                # additional data fetching depending on the
                # type of entity
                # if(i.startswith("todo")):
                #     todo = await client.async_get_domain("todo")
                #     changed_states, data = await todo.get_items(entity_id=i)
                #     new_post_its.append(data)

            global ENTITY_STATES, POST_ITS
            ENTITY_STATES = new_states
            POST_ITS = new_post_its
            await asyncio.sleep(DATA_UPDATE_TIMEOUT)


# ----------------------------------------------------------
# Initial setup
# ----------------------------------------------------------
load_dotenv()
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
ENTITY_IDS = json.loads(os.getenv("ENTITY_IDS"))


# ----------------------------------------------------------
# Program
# ----------------------------------------------------------
async def main():
    print("Starting!")
    print("HA_URL: " + HA_URL)
    print("ENTITY_IDS: " + str(ENTITY_IDS))

    await asyncio.gather(update_display(), handle_buttons(), fetch_data())


if __name__ == "__main__":
    asyncio.run(main())
