import asyncio
import digitalio
import board
import gpio
from display import Display


class Button:
    BUTTON_UPDATE_TIMEOUT = 0.05
    _buttons = {}

    def __init__(
        self,
        config,
        display: Display,
    ):
        self._display = display

        # read config
        for pin, action in config:
            button = digitalio.DigitalInOut(gpio.deserialize(pin))
            board.switch_to_input()
            self._buttons[button] = action

    def button_pressed(button) -> bool:
        return not button.value

    async def handle_buttons(self) -> None:
        while True:
            for button, action in self._buttons:
                if self.button_pressed(button):
                    match action:
                        case "cycle":
                            self.handle_cycle()
                        case "action":
                            self.handle_action()
            await asyncio.sleep(self.BUTTON_UPDATE_TIMEOUT)

    async def handle_cycle(self) -> None:
        self._display.cycle()

    async def handle_action(self) -> None:
        self._display.get_current_entity.handle_action()
