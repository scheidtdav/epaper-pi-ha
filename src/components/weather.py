from PIL import ImageFont, ImageDraw
from components.base_component import BaseComponent

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


class Weather(BaseComponent):
    def __init__(self, entity_id, display_dimensions):
        super().__init__(entity_id, display_dimensions)
        self.entity = None
        self.weather_domain = None
        self.forecast = None

    def fetch_data(self, client):
        if not self.entity:
            self.entity = client.get_state(entity_id=self._entity_id)

        if not self.weather_domain:
            self.weather_domain = client.get_domain("weather")

        data = self.weather_domain.get_forecasts(
            entity_id=self._entity_id,
            type="daily",
        )

        last_forecast = self.forecast
        self.forecast = data

        self._has_changes = self.forecast != last_forecast
        self._has_content = True if self.forecast else False

    def render(self):
        img = super().render()
        draw = ImageDraw.Draw(img)

        if not self._has_content:
            draw.text(
                (0, 0),
                f"No content for entity id '{self._entity_id}'",
                font=self.regular_font,
                fill=self.BLACK,
            )
            return img

        weather_icon = ICON_MAP[self.weather_entity.state]
        draw.text(
            (2, 2),
            weather_icon,
            font=icon_font,
            fill=self.BLACK,
        )

        temperature = self.weather_entity.attributes.get("temperature", "?")
        temp_unit = self.weather_entity.attributes.get("temperature_unit", "?")
        temp_string = f"{temperature}{temp_unit}"
        text_bbox = draw.textbbox((36 + 9, 7), temp_string, self.regular_font)
        draw.text(
            (36 + 9, 7),
            temp_string,
            font=self.regular_font,
            fill=self.BLACK,
        )

        if self.forecast:
            print(self.forecast)
            draw.text(
                (text_bbox[2], 0),
                "hello forecast",
                font=self.small_font,
                fill=self.BLACK,
            )

        return img
