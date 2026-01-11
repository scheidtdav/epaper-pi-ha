from PIL import Image, ImageFont, ImageDraw


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
    huge_font = ImageFont.truetype(
        "/usr/share/fonts/truetyoe/dejavu/DejaVuSans.ttf", 84
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

    def text_width(
        self, s: str, draw: ImageDraw.ImageDraw, font: ImageFont.ImageFont
    ) -> int:
        bbox = draw.textbbox((0, 0), s, font=font)
        return bbox[2] - bbox[0]

    def multiline_text(
        self,
        draw: ImageDraw.ImageDraw,
        font: ImageFont.ImageFont,
        text: str,
        max_width: int,
    ):
        words = text.split()
        if not words:
            return ""

        paragraphs = text.splitlines() or [""]
        lines = []

        for para in paragraphs:
            words = para.split()
            if not words:
                lines.append("")  # blank line
                continue

            current = []
            for word in words:
                test = " ".join(current + [word]) if current else word
                if self.text_width(test, draw, font) <= max_width:
                    current.append(word)
                else:
                    if not current:
                        # single long word: break by characters
                        part = ""
                        for ch in word:
                            test_part = part + ch
                            if self.text_width(test, draw, font) <= max_width:
                                part = test_part
                            else:
                                if part:
                                    lines.append(part)
                                part = ch
                        if part:
                            current = [part]
                        else:
                            current = []
                    else:
                        lines.append(" ".join(current))
                        current = [word]
            if current:
                lines.append(" ".join(current))

        return "\n".join(lines)
