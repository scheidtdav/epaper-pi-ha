from typing import Any, Dict, List, Optional
from PIL import Image, ImageDraw

from components.base_component import BaseComponent


class Todo(BaseComponent):
    def __init__(self, entity_id: str, display_dimensions: tuple[int, int]) -> None:
        super().__init__(entity_id, display_dimensions)
        self.entity: Optional[Any] = None
        self.todo_domain: Optional[Any] = None
        self.todos: Dict[str, Any] = {}
        self._background_color: tuple[int, int, int] = self.BLACK

    def fetch_data(self, client: Any) -> None:
        if not self.entity:
            self.entity = client.get_state(entity_id=self._entity_id)

        if not self.todo_domain:
            self.todo_domain = client.get_domain("todo")

        data: Dict[str, Any] = self.todo_domain.get_items.trigger(
            entity_id=self._entity_id,
        )

        last_todos: Dict[str, Any] = self.todos
        self.todos = data.get(self._entity_id)

        self._has_content = True if self.todos and int(self.entity.state) > 0 else False

    def handle_action(self) -> bool:
        if not self.todo_domain or not self._has_content:
            return False

        todo_items: List[Dict[str, Any]] = self.todos.get("items", [])
        unchecked_todos: List[Dict[str, Any]] = [t for t in todo_items if t.get("status") == "needs_action"]

        if unchecked_todos:
            first_todo: Dict[str, Any] = unchecked_todos[0]
            item_identifier: Optional[str] = first_todo.get("uid") or first_todo.get("summary")
            if item_identifier:
                self.todo_domain.update_item.trigger(
                    entity_id=self._entity_id,
                    item=item_identifier,
                    status="completed"
                )
                return True
        return False

    def render(self) -> Image.Image:
        img: Image.Image = super().render()
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

        if not self._has_content:
            draw.text(
                (0, 0),
                f"No content for entity id '{self._entity_id}'",
                font=self.regular_font,
                fill=self.WHITE,
            )
            return img

        draw.text((2, self._dimensions[1] // 2), "!", self.WHITE, self.huge_font, "lm")

        todo_items: Optional[List[Dict[str, Any]]] = self.todos.get("items")
        unchecked_todos: List[Dict[str, Any]] = [t for t in todo_items if t.get("status") == "needs_action"]
        if len(unchecked_todos) == 0:
            return img

        # we only support showing the first entry thats not checked
        post_it_text: str = unchecked_todos[0].get("summary", "")
        draw.text(
            (32, self._dimensions[1] // 2),
            self.multiline_text(
                draw,
                self.regular_font,
                post_it_text,
                self._dimensions[0] - 32,
            ),
            self.WHITE,
            self.regular_font,
            "lm",
        )

        return img
