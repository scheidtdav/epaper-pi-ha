from PIL import Image, ImageFont


class BaseComponent:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    small_font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14
    )
    regular_font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18
    )
    large_font = ImageFont.truetype(
        "/usr/share/fonts/truetyoe/dejavu/DejaVuSans.ttf", 24
    )

    def __init__(self, entity_id, display_dimensions):
        self._entity_id = entity_id
        self._dimensions = display_dimensions
        self._has_content = False
        self._has_changes = False
        self._background_color = self.WHITE

    def handle_action(self):
        pass

    def render(self):
        self._has_changes = False
        image = Image.new("RGB", self._dimensions, color=self._background_color)
        return image

    def has_content(self):
        return self._has_content

    def has_changes(self):
        return self._has_changes
