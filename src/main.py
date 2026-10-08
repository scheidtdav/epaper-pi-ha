import asyncio
from typing import Any, Dict, List, Tuple
import tomllib
from homeassistant_api import WebsocketClient

from button import Button
from components.base_component import BaseComponent
from components.weather import Weather
from components.todo import Todo
from components.sensor import Sensor
from display import Display


async def fetch_data(ha_config: Dict[str, Any], entities: List[BaseComponent]) -> None:
    with WebsocketClient(ha_config["url"], ha_config["token"]) as client:
        while True:
            for entity in entities:
                entity.fetch_data(client)
            await asyncio.sleep(ha_config["update_timeout"])


def init_entities(ha_config: Dict[str, Any], display_dimensions: Tuple[int, int]) -> List[BaseComponent]:
    entities: List[BaseComponent] = []
    for id in ha_config["entities"]:
        match id:
            case i if i.startswith("weather."):
                entities.append(Weather(i, display_dimensions))
            case i if i.startswith("todo."):
                entities.append(Todo(i, display_dimensions))
            case i if i.startswith("sensor."):
                entities.append(Sensor(i, display_dimensions))
            case _:
                print(f"No idea what to do with entity id '{i}', skipping.")
    return entities


async def main() -> int:
    try:
        with open("config.toml", "rb") as f:
            config: Dict[str, Any] = tomllib.load(f)
    except Exception as e:
        print("Could not work out the configuration, exiting.", e)
        return 1

    ha_url: str = config["home_assistant"]["url"]
    entities_list: List[str] = config["home_assistant"]["entities"]

    print("Starting!")
    print("HA_URL: " + ha_url)
    print("ENTITY_IDS: " + str(entities_list))

    display_dimensions: Tuple[int, int] = (
        config["display"]["height_in_pixel"],
        config["display"]["width_in_pixel"],
    )

    entities: List[BaseComponent] = init_entities(
        config["home_assistant"],
        display_dimensions,
    )
    display: Display = Display(config["display"], entities)
    buttons: Button = Button(config["buttons"], display)

    await asyncio.gather(
        display.update(),
        buttons.handle_buttons(),
        fetch_data(config["home_assistant"], entities),
    )
    return 0


if __name__ == "__main__":
    asyncio.run(main())
