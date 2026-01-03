import digitalio
import busio
import digitalio
import busio
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1675 import Adafruit_SSD1675

class Display:

    _views = []
    _current_view_id = 0

    def __init__(self, config):
        # init display
        displayConfig = config["display"]
        spi = busio.SPI(displayConfig.SCK, MOSI=displayConfig.MOSI, MISO=displayConfig.MISO)
        ecs = digitalio.DigitalInOut(displayConfig.CE0)
        dc = digitalio.DigitalInOut(displayConfig.D22)
        rst = digitalio.DigitalInOut(displayConfig.D27)
        busy = digitalio.DigitalInOut(displayConfig.D17)
        srcs = None

        self._display = Adafruit_SSD1675(122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=srcs, rst_pin=rst, busy_pin=busy)
        self._display.rotation = 1

        for view in config["views"]:
            #ToDo init/deserialize view
            self._views.append(view) 


    def itterate_view(self):
        self._current_view_id = self._current_view_id + 1 % len(self._views)
        self.update()


    def get_current_view(self):
        return self._views[self.get_current_view]
    
    

    def update(self):
        self._display.fill(Adafruit_EPD.WHITE)
        image = self._views(self._current_view_id).reder()
        self._display.image(image)
        self._display.display()
