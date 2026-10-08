import datetime
from typing import Any, Dict, Optional

from PIL import Image, ImageDraw, ImageFont

from components.base_component import BaseComponent

icon_font: ImageFont.ImageFont = ImageFont.truetype("./meteocons.ttf", 36)

ICON_MAP: Dict[str, str] = {
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
    def __init__(self, entity_id: str, display_dimensions: tuple[int, int]) -> None:
        super().__init__(entity_id, display_dimensions)
        self.entity: Optional[Any] = None
        self.weather_domain: Optional[Any] = None
        self.forecast: Optional[Dict[str, Any]] = None

    def fetch_data(self, client: Any) -> None:
        if not self.entity:
            self.entity = client.get_state(entity_id=self._entity_id)

        if not self.weather_domain:
            self.weather_domain = client.get_domain("weather")

        data: Dict[str, Any] = self.weather_domain.get_forecasts.trigger(
            entity_id=self._entity_id,
            type="hourly",
        )

        last_forecast: Optional[Dict[str, Any]] = self.forecast
        self.forecast = data

        self._has_changes = self.forecast != last_forecast if self._has_changes is False else False
        self._has_content = True if self.forecast else False

    def render(self) -> Image.Image:
        self._has_changes = False
        img: Image.Image = super().render()
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

        if not self._has_content:
            draw.text(
                (0, 0),
                f"No content for entity id '{self._entity_id}'",
                font=self.regular_font,
                fill=self.BLACK,
            )
            return img

        current_icon: str = ICON_MAP.get(self.entity.state, "?")

        # Draw current weather icon (Top Left)
        draw.text(
            (2, 2),
            current_icon,
            font=icon_font,
            fill=self.BLACK,
        )

        temperature: Any = self.entity.attributes.get("temperature", "?")
        temp_unit: str = self.entity.attributes.get("temperature_unit", "?")
        temp_string: str = f"{temperature}{temp_unit}"
        temp_x_start: int = 50
        temp_y_start: int = 16

        draw.text(
            (temp_x_start, 2),
            "Aktuell",
            font=self.small_font,
            fill=self.BLACK,
        )
        draw.text(
            (temp_x_start, temp_y_start),
            temp_string,
            font=self.regular_font,
            fill=self.BLACK,
        )

        if not self.forecast:
            return img

        # Define starting position for the forecast grid
        forecast_y_start: int = 42
        forecast_x_start: int = 2
        forecast_col_width: int = 122 // 3

        actual_forecast: list = self.forecast.get(self._entity_id, {}).get("forecast", [])[1:5]

        for i, fc_data in enumerate(actual_forecast):
            forecast_icon: str = ICON_MAP.get(fc_data.get("condition"), "?")
            day_name: str = f"+{i + 1} Std."
            fc_temp: str = f"{fc_data.get('temperature', '?')}°C"

            # Calculate coordinates for this day's column
            day_x: int = forecast_x_start + i * (forecast_col_width + 24)

            # Draw Day Name (Top)
            draw.text(
                (day_x, forecast_y_start + 14),
                f"{day_name}",
                font=self.small_font,
                fill=self.BLACK,
            )

            # Draw Day Icon (Middle)
            draw.text(
                (day_x + 10, forecast_y_start + 30),
                forecast_icon,
                font=icon_font,
                fill=self.BLACK,
            )

            # Draw Temperature (Bottom)
            draw.text(
                (day_x, forecast_y_start + 63),
                fc_temp,
                font=self.small_font,
                fill=self.BLACK,
            )

        return img
