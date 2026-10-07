from PIL import ImageDraw
from components.base_component import BaseComponent


class Sensor(BaseComponent):
    def _format_state(self, state):
        """Format the sensor state, rounding numeric values to at most 2 decimal places."""
        if state is None:
            return state
        try:
            # Try to convert to float for rounding
            numeric_value = float(state)
            rounded = round(numeric_value, 2)
            # If it's a whole number, display without decimals
            if rounded == int(rounded):
                return str(int(rounded))
            # Otherwise, display with up to 2 decimal places, stripping trailing zeros
            formatted = f"{rounded:.2f}".rstrip('0').rstrip('.')
            return formatted
        except (ValueError, TypeError):
            # If not numeric, return as-is
            return str(state)
    def __init__(self, entity_id, display_dimensions):
        super().__init__(entity_id, display_dimensions)
        self.entity = None

    def fetch_data(self, client):
        state_before = self.entity.state if self.entity else None

        if not self.entity:
            self.entity = client.get_state(entity_id=self._entity_id)

        self._has_changes = self.entity.state != state_before
        self._has_content = self.entity.state is not None

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

        draw.text(
            (0, 0),
            f"{self.entity.attributes.get('friendly_name', self._entity_id)}",
            font=self.regular_font,
            fill=self.BLACK,
        )
        draw.text(
            (0, 32),
            self._format_state(self.entity.state),
            font=self.large_font,
            fill=self.BLACK,
        )

        return img
