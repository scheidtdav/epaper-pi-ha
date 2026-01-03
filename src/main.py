import asyncio
import tomllib
from homeassistant_api import WebsocketClient
from PIL import ImageFont

from src.button import Button
from src.components.weather import Weather
from src.display import Display

icon_font = ImageFont.truetype("./meteocons.ttf", 36)
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
regular_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
large_font = ImageFont.truetype("/usr/share/fonts/truetyoe/dejavu/DejaVuSans.ttf", 24)


async def fetch_data(ha_config, entities):
    with WebsocketClient(ha_config["url"], ha_config["token"]) as client:
        while True:
            for entity in entities:
                entity.fetch_data(client)
            await asyncio.sleep(ha_config["update_timeout"])


def init_entities(ha_config):
    entities = []
    for id in ha_config["entities"]:
        match id:
            case i if i.startswith("weather."):
                entities.append(Weather(i))
            case i if i.startswith("todo."):
                entities.append(Todo(i))
            case _:
                print(f"No idea what to do with entity id '{i}', skipping.")
    return entities


async def main():
    try:
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)
    except Exception as e:
        print("Could not work out the configuration, exiting.", e)
        return 1

    ha_url = config["home_assistant"]["url"]
    entities = config["home_assistant"]["entities"]

    print("Starting!")
    print("HA_URL: " + ha_url)
    print("ENTITY_IDS: " + str(entities))

    entities = init_entities(config["home_assistant"])
    display = Display(config["display"], entities)
    buttons = Button(config["buttons"], display)

    await asyncio.gather(
        display.update(),
        buttons.handle_buttons(),
        fetch_data(config["home_assistant"], entities),
    )


if __name__ == "__main__":
    asyncio.run(main())
