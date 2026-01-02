import asyncio
import digitalio
import board


BUTTON_UPDATE_TIMEOUT = 0.05

up_button = digitalio.DigitalInOut(board.D5)
up_button.switch_to_input()
down_button = digitalio.DigitalInOut(board.D6)
down_button.switch_to_input()

def button_pressed(button):
    return not button.value

async def handle_buttons():
    while True:
        if button_pressed(up_button):
            print("up")

        if button_pressed(down_button):
            print("down")

        await asyncio.sleep(BUTTON_UPDATE_TIMEOUT)