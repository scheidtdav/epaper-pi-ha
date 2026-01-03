import asyncio
import digitalio
import busio
import board
import gpio
from adafruit_epd.ssd1675 import Adafruit_SSD1675


class Display:
    DISPLAY_UPDATE_TIMEOUT = 300  # you should not update more often than every 5 mins
    _entities = []
    _current_entity_index = 0

    def __init__(self, display_config, entities):
        self._entities = entities

        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        ecs = digitalio.DigitalInOut(gpio.deserialize(display_config["ecs_pin"]))
        dc = digitalio.DigitalInOut(gpio.deserialize(display_config["dc_pin"]))
        rst = digitalio.DigitalInOut(gpio.deserialize(display_config["rst_pin"]))
        busy = digitalio.DigitalInOut(gpio.deserialize(display_config["busy_pin"]))
        srcs = None

        self._display = Adafruit_SSD1675(
            display_config["width_in_pixel"],
            display_config["height_in_pixel"],
            spi,
            cs_pin=ecs,
            dc_pin=dc,
            sramcs_pin=srcs,
            rst_pin=rst,
            busy_pin=busy,
        )

        # only landscape is supported, thus rotation needs to be set to 1
        self._display.rotation = 1

    def cycle(self):
        next = True
        next_index = self._current_entity_index
        while next:
            next_index = self._current_entity_index + 1 % len(self._entities)
            next_entity = self._entities[next_index]
            next = not next_entity.has_content()

        self._current_entity_index = next_index
        image = self.get_current_entity().render()
        self._display.image(image)
        self._display.display()

    def get_current_entity(self):
        return self._entities[self._current_entity_index]

    def __update__(self):
        for i in range(self._current_entity_index):
            entity = self._entities[i]
            if not entity.has_changes():
                print(f"no update for {entity._entity_id}")
                continue

            if not entity.has_content():
                print(f"no content for {entity._entity_id}")
                continue

            print(f"render component {entity._entity_id}")
            image = entity.render()
            self._display.image(image)
            self._display.display()
            return

    async def update(self):
        while True:
            self.__update__()
            await asyncio.sleep(self.DISPLAY_UPDATE_TIMEOUT)
