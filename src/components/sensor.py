from PIL import ImageDraw
from components.base_component import BaseComponent


class Sensor(BaseComponent):
    def __init__(self, entity_id, display_dimensions):
        super().__init__(entity_id, display_dimensions)
        self.entity = None

    def fetch_data(self, client):
        state_before = self.entity.state if self.entity else None

        if not self.entity:
            self.entity = client.get_state(entity_id=self._entity_id)

        self._has_changes = self.entity.state != state_before
        self._has_content = True if self.entity.state else False

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
            f"{self.entity.state}",
            font=self.large_font,
            fill=self.BLACK,
        )

        return img
