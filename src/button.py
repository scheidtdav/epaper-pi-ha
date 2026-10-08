import asyncio
from typing import Any, Dict
import digitalio
import gpio
from display import Display


class Button:
    BUTTON_UPDATE_TIMEOUT: float = 0.05
    _buttons: Dict[Any, Dict[str, str]] = {}

    def __init__(
        self,
        config: Dict[str, Dict[str, str]],
        display: Display,
    ) -> None:
        self._display: Display = display

        # read config
        for pin, action in config.items():
            button: Any = digitalio.DigitalInOut(gpio.deserialize(pin))
            button.switch_to_input()
            self._buttons[button] = action["action"]

    def button_pressed(self, button: Any) -> bool:
        return not button.value

    async def handle_buttons(self) -> None:
        while True:
            for button, action in self._buttons.items():
                if self.button_pressed(button):
                    match action:
                        case "cycle":
                            self.handle_cycle()
                        case "action":
                            self.handle_action()
                    print(f"Button pressed: {action}")
            await asyncio.sleep(self.BUTTON_UPDATE_TIMEOUT)

    def handle_cycle(self) -> None:
        self._display.cycle()

    def handle_action(self) -> None:
        self._display.get_current_entity().handle_action()
