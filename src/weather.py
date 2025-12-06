from PIL import ImageFont

icon_font = ImageFont.truetype("./meteocons.ttf", 36)

ICON_MAP = {
    "clear-night": "C",
    "cloudy": "N",
    "fog": "M",
    "hail": "X",
    "lightning": "P",
    "lightning-rainy": "Z",
    "partlycloudy": "H",
    "pouring": "R",
    "rainy": "Q",
    "snowy": "V",
    "snowy-rainy": "W",
    "sunny": "B",
    "windy": "F",
    "windy-variant": "S",
    "exceptional": "D",
}


def handle_weather(weather_entity, draw, font, color):
    weather_icon = ICON_MAP[weather_entity.state]
    draw.text(
        (2, 2),
        weather_icon,
        font=icon_font,
        fill=color,
    )

    temperature = weather_entity.attributes.get("temperature", "?")
    temp_unit = weather_entity.attributes.get("temperature_unit", "?")
    temp_string = f"{temperature}{temp_unit}"
    draw.text(
        (36 + 9, 7),
        temp_string,
        font=font,
        fill=color,
    )
