import datetime

from PIL import ImageDraw, ImageFont

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

        data = self.weather_domain.get_forecasts.trigger(
            entity_id=self._entity_id,
            type="hourly",
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

        current_icon = ICON_MAP.get(self.entity.state, "?")

        # Draw current weather icon (Top Left)
        draw.text(
            (2, 2),
            current_icon,
            font=icon_font,
            fill=self.BLACK,
        )

        temperature = self.entity.attributes.get("temperature", "?")
        temp_unit = self.entity.attributes.get("temperature_unit", "?")
        temp_string = f"{temperature}{temp_unit}"
        temp_x_start = 50
        temp_y_start = 2

        draw.text(
            (temp_x_start, temp_y_start),
            temp_string,
            font=self.regular_font,
            fill=self.BLACK,
        )

        if not self.forecast:
            return img

        # Define starting position for the forecast grid
        forecast_y_start = 46
        forecast_x_start = 2
        forecast_col_width = 122 // 3

        # Title
        draw.text(
            (2, forecast_y_start),
            "Vorhersage",
            font=self.small_font,
            fill=self.BLACK,
        )

        actual_forecast = self.forecast.get(self._entity_id).get("forecast")[1:4]

        for i, fc_data in enumerate(actual_forecast):
            forecast_icon = ICON_MAP.get(fc_data.get("condition"), "?")
            day_name = f"+{i} Std."
            fc_temp = f"{fc_data.get('temperature', '?')}°C"

            # Calculate coordinates for this day's column
            day_x = forecast_x_start + i * (forecast_col_width + 28)

            # Draw Day Name (Top)
            draw.text(
                (day_x, forecast_y_start + 14),
                f"{day_name}",
                font=self.small_font,
                fill=self.BLACK,
            )

            # Draw Day Icon (Middle)
            draw.text(
                (day_x + 10, forecast_y_start + 28),
                forecast_icon,
                font=icon_font,
                fill=self.BLACK,
            )

            # Draw Temperature (Bottom)
            draw.text(
                (day_x, forecast_y_start + 60),
                fc_temp,
                font=self.small_font,
                fill=self.BLACK,
            )

        return img
