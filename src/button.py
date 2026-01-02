import asyncio
import digitalio
import board

class Button:

    BUTTON_UPDATE_TIMEOUT = 0.05
    _buttons = {}

    def __init__(self, display, config):
        # read config
        for pin, action in config:
            button = digitalio.DigitalInOut(pin)
            board.switch_to_input()
            self._buttons[button] = action

        self._display = display

    up_button = digitalio.DigitalInOut(board.D5)
    up_button.switch_to_input()
    down_button = digitalio.DigitalInOut(board.D6)
    down_button.switch_to_input()

    def button_pressed(button) ->bool:
        return not button.value

    async def handle_buttons(self) -> None:
        while True:
            for button, action in self._buttons:
                if self.button_pressed(button):
                    match action:
                        case "next":
                            self.handle_next()
                        case "action":
                            self.handle_action()
            await asyncio.sleep(self.BUTTON_UPDATE_TIMEOUT)

    async def handle_next(self) -> None:
        self._display.itterate_view()
        

    async def handle_action(self) -> None:
        self._display.get_current_view.handle_action()