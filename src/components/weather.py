from PIL import ImageFont
from jinja2 import Environment, FileSystemLoader

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

class WeatherComponent:
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.entity = None
        self.weather_domain = None
        self.forecast = None

    def fetch_data(self, client):
        self.entity = client.get_state(entity_id=self.entity_id)
        self.weather_domain = client.get_domain("weather")
        _, data = self.weather_domain.get_forecasts(
            entity_id=self.entity_id,
            type="daily",
        )
        self.forecast = data
    
    async def render(self):

        pass

def render(weather_entity, forecast, draw, font, small_font, color):
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
