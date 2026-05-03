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

        # --- 1. Check for empty content ---
        if not self._has_content:
            draw.text(
                (0, 0),
                f"No content for entity id '{self._entity_id}'",
                font=self.regular_font,
                fill=self.BLACK,
            )
            return img

        # --- 2. Draw Current Weather (Icon & Temp) ---
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

        # Estimate bounding box for temperature text (Starting slightly right of icon)
        # Approximate position: (Width needed + margin, Y_offset)
        # Using a fixed safe offset for initial text placement
        temp_x_start = 50
        temp_y_start = 2

        draw.text(
            (temp_x_start, temp_y_start),
            temp_string,
            font=self.regular_font,
            fill=self.BLACK,
        )

        # --- 3. Draw Forecast (Next 3 days) ---
        if not self.forecast:
            return img

        # Define starting position for the forecast grid
        FORECAST_START_Y = 20
        FORECAST_X_START = 2
        DAY_COL_WIDTH = 122 // 3 - 10  # Approx width for 3 days

        # Title
        draw.text(
            (2, FORECAST_START_Y - 10),
            "🗓️ Forecast",
            font=self.small_font,
            fill=self.BLACK,
        )

        # Iterate through the next 3 days (or fewer if data is limited)
        forecast_days = self.forecast[:3]

        for i, day_data in enumerate(forecast_days):
            # ASSUMPTION: day_data is a dictionary/object with these keys:
            # 'date': Date string (e.g., "Fri")
            # 'icon_map': The icon code (e.g., "H")
            # 'description': A readable description (e.g., "Partly Cloudy")
            # 'temp_high': High temperature
            # 'temp_low': Low temperature

            day_icon = ICON_MAP.get(day_data.get("icon_map"), "?")
            day_name = day_data.get("date", "---")
            description = day_data.get("description", "")
            high_temp = day_data.get("temp_high", "?")
            low_temp = day_data.get("temp_low", "?")

            # Calculate coordinates for this day's column
            day_x = FORECAST_X_START + i * (DAY_COL_WIDTH + 10)

            # Draw Day Name (Top)
            draw.text(
                (day_x, FORECAST_START_Y),
                f"{day_name}",
                font=self.small_font,
                fill=self.BLACK,
            )

            # Draw Day Icon (Middle)
            draw.text(
                (day_x + 10, FORECAST_START_Y + 10),
                day_icon,
                font=icon_font,
                fill=self.BLACK,
            )

            # Draw Description (Middle)
            draw.text(
                (day_x, FORECAST_START_Y + 20),
                description,
                font=self.small_font,
                fill=self.BLACK,
            )

            # Draw Temperature (Bottom)
            temp_line = f"{high_temp} / {low_temp}"
            draw.text(
                (day_x, FORECAST_START_Y + 40),
                temp_line,
                font=self.regular_font,
                fill=self.BLACK,
            )

        return img
