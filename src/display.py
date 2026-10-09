import asyncio
from typing import Any, List, Optional
import digitalio
import busio
import board
import gpio
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.ssd1675 import Adafruit_SSD1675
from components.base_component import BaseComponent


class Display:
    DISPLAY_UPDATE_TIMEOUT: int = 300  # you should not update more often than every 5 mins
    _entities: List[BaseComponent]
    _current_entity_index: int = 0

    def __init__(self, display_config: dict, entities: List[BaseComponent]) -> None:
        self._entities: List[BaseComponent] = entities
        self._initialized: bool = False
        self._dimensions: tuple[int, int] = (
            display_config["height_in_pixel"],
            display_config["width_in_pixel"],
        )

        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        ecs = digitalio.DigitalInOut(gpio.deserialize(display_config["ecs_pin"]))
        dc = digitalio.DigitalInOut(gpio.deserialize(display_config["dc_pin"]))
        rst = digitalio.DigitalInOut(gpio.deserialize(display_config["rst_pin"]))
        busy = digitalio.DigitalInOut(gpio.deserialize(display_config["busy_pin"]))
        srcs: Any = None

        self._display: Any = Adafruit_SSD1675(
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
        
        # Show initialization screen immediately
        self._show_init_screen()

    def mark_initialized(self) -> None:
        """Mark that initial data has been fetched."""
        self._initialized = True

    def _show_init_screen(self) -> None:
        """Show initialization screen."""
        img: Image.Image = Image.new("RGB", self._dimensions, color=(255, 255, 255))
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)
        
        # Use a simple font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Center the text
        text: str = "Initializing..."
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width: int = bbox[2] - bbox[0]
        text_height: int = bbox[3] - bbox[1]
        
        x: int = (self._dimensions[0] - text_width) // 2
        y: int = (self._dimensions[1] - text_height) // 2
        
        draw.text((x, y), text, font=font, fill=(0, 0, 0))
        
        self._display.image(img)
        self._display.display()

    def cycle(self) -> None:
        print("called cycle")
        # If not initialized yet, don't cycle
        if not self._initialized:
            return
            
        # Find the next entity with content, starting from current + 1
        for i in range(len(self._entities)):
            next_index: int = (self._current_entity_index + 1 + i) % len(self._entities)
            if self._entities[next_index].has_content():
                self._current_entity_index = next_index
                image: Any = self.get_current_entity().render()
                self._display.image(image)
                self._display.display()
                return

        # If no entity has content, do nothing (stay on current)

    def get_current_entity(self) -> BaseComponent:
        return self._entities[self._current_entity_index]

    def __update__(self) -> None:
        print("__update__")
        
        # If not initialized, check if any entity has content now
        if not self._initialized:
            for i, entity in enumerate(self._entities):
                if entity.has_content():
                    print(f"Initial data fetched for {entity._entity_id}, switching to normal display")
                    self._initialized = True
                    self._current_entity_index = i
                    image: Any = entity.render()
                    self._display.image(image)
                    self._display.display()
                    return
            # No content yet, keep showing init screen
            print("Still waiting for initial data...")
            return
        
        # Normal update logic
        for i in range(self._current_entity_index + 1):
            entity: BaseComponent = self._entities[i]
            if not entity.has_changes():
                print(f"no update for {entity._entity_id}")
                continue

            if not entity.has_content():
                print(f"no content for {entity._entity_id}")
                continue

            print(f"render component {entity._entity_id}")
            self._current_entity_index = i
            image: Any = entity.render()
            self._display.image(image)
            self._display.display()
            return

    async def update(self) -> None:
        while True:
            self.__update__()
            # Use a shorter timeout while waiting for initial data
            timeout = 5 if not self._initialized else self.DISPLAY_UPDATE_TIMEOUT
            await asyncio.sleep(timeout)
