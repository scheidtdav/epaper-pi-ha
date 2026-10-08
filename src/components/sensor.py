from typing import Any, Optional
from PIL import Image, ImageDraw
from components.base_component import BaseComponent


class Sensor(BaseComponent):
    def __init__(self, entity_id: str, display_dimensions: tuple[int, int]) -> None:
        super().__init__(entity_id, display_dimensions)
        self.entity: Optional[Any] = None

    def _format_state(self, state: Any) -> str:
        """Format the sensor state, rounding numeric values to at most 2 decimal places."""
        if state is None:
            return state
        try:
            # Try to convert to float for rounding
            numeric_value: float = float(state)
            rounded: float = round(numeric_value, 2)
            # If it's a whole number, display without decimals
            if rounded == int(rounded):
                return str(int(rounded))
            # Otherwise, display with up to 2 decimal places, stripping trailing zeros
            formatted: str = f"{rounded:.2f}".rstrip('0').rstrip('.')
            return formatted
        except (ValueError, TypeError):
            # If not numeric, return as-is
            return str(state)

    def fetch_data(self, client: Any) -> None:
        state_before: Any = self.entity.state if self.entity else None

        if not self.entity:
            self.entity = client.get_state(entity_id=self._entity_id)

        self._has_changes = self.entity.state != state_before
        self._has_content = self.entity.state is not None

    def render(self) -> Image.Image:
        img: Image.Image = super().render()
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

        if not self._has_content:
            text: str = f"No content for entity id '{self._entity_id}'"
            text_width: int = self.text_width(text, draw, self.regular_font)
            x: int = (self._dimensions[0] - text_width) // 2
            y: int = (self._dimensions[1] - self.regular_font.size) // 2
            draw.text(
                (x, y),
                text,
                font=self.regular_font,
                fill=self.BLACK,
            )
            return img

        title: str = f"{self.entity.attributes.get('friendly_name', self._entity_id)}"
        value: str = self._format_state(self.entity.state)
        
        title_width: int = self.text_width(title, draw, self.regular_font)
        value_width: int = self.text_width(value, draw, self.large_font)
        
        title_x: int = (self._dimensions[0] - title_width) // 2
        value_x: int = (self._dimensions[0] - value_width) // 2
        
        title_y: int = (self._dimensions[1] - self.regular_font.size - self.large_font.size) // 2
        value_y: int = title_y + self.regular_font.size

        draw.text(
            (title_x, title_y),
            title,
            font=self.regular_font,
            fill=self.BLACK,
        )
        draw.text(
            (value_x, value_y),
            value,
            font=self.large_font,
            fill=self.BLACK,
        )

        return img
