from typing import Tuple
from PIL import Image, ImageDraw, ImageFont


class BaseComponent:
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)

    small_font: ImageFont.ImageFont = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14
    )
    regular_font: ImageFont.ImageFont = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18
    )
    large_font: ImageFont.ImageFont = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24
    )
    huge_font: ImageFont.ImageFont = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 84
    )

    def __init__(self, entity_id: str, display_dimensions: Tuple[int, int]) -> None:
        self._entity_id: str = entity_id
        self._dimensions: Tuple[int, int] = display_dimensions
        self._has_content: bool = False
        self._has_changes: bool = False
        self._background_color: Tuple[int, int, int] = self.WHITE

    def handle_action(self) -> None:
        pass

    def render(self) -> Image.Image:
        self._has_changes = False
        image: Image.Image = Image.new("RGB", self._dimensions, color=self._background_color)
        return image

    def has_content(self) -> bool:
        return self._has_content

    def has_changes(self) -> bool:
        return self._has_changes

    def text_width(
        self, s: str, draw: ImageDraw.ImageDraw, font: ImageFont.ImageFont
    ) -> int:
        bbox = draw.textbbox((0, 0), s, font=font)
        return int(bbox[2] - bbox[0])

    def multiline_text(
        self,
        draw: ImageDraw.ImageDraw,
        font: ImageFont.ImageFont,
        text: str,
        max_width: int,
    ) -> str:
        words: list[str] = text.split()
        if not words:
            return ""

        paragraphs: list[str] = text.splitlines() or [""]
        lines: list[str] = []

        for para in paragraphs:
            words = para.split()
            if not words:
                lines.append("")  # blank line
                continue

            current: list[str] = []
            for word in words:
                test: str = " ".join(current + [word]) if current else word
                if self.text_width(test, draw, font) <= max_width:
                    current.append(word)
                else:
                    if not current:
                        # single long word: break by characters
                        part: str = ""
                        for ch in word:
                            test_part: str = part + ch
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
