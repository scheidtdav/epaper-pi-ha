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

def render(json):
    return


def handle_weather(weather_entity, forecast, draw, font, small_font, color):
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
    text_bbox = draw.textbbox((36 + 9, 7), temp_string, font)
    draw.text(
        (36 + 9, 7),
        temp_string,
        font=font,
        fill=color,
    )

    if forecast:
        print(forecast)
        draw.text((text_bbox[2], 0), "hello", font=small_font, fill=color)
