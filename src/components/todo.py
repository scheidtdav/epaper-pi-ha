from PIL import ImageDraw
from components.base_component import BaseComponent


class Todo(BaseComponent):
    def __init__(self, entity_id, display_dimensions):
        super().__init__(entity_id, display_dimensions)
        self.entity = None
        self.todo_domain = None
        self.todos = []
        self._background_color = self.BLACK

    def fetch_data(self, client):
        if not self.entity:
            self.entity = client.get_state(entity_id=self._entity_id)

        if not self.todo_domain:
            self.todo_domain = client.get_domain("todo")

        data = self.todo_domain.get_items(
            entity_id=self._entity_id,
        )

        last_todos = self.todos
        self.todos = data.get(self._entity_id)

        self._has_changes = self.todos != last_todos
        self._has_content = True if self.todos and int(self.entity.state) > 0 else False

    def render(self):
        img = super().render()
        draw = ImageDraw.Draw(img)

        if not self._has_content:
            draw.text(
                (0, 0),
                f"No content for entity id '{self._entity_id}'",
                font=self.regular_font,
                fill=self.WHITE,
            )
            return img

        draw.text((2, self._dimensions[1] // 2), "!", self.WHITE, self.huge_font, "lm")

        todo_items = self.todos.get("items")
        unchecked_todos = [t for t in todo_items if t.get("status") == "needs_action"]
        if len(unchecked_todos) == 0:
            return img

        # we only support showing the first entry thats not checked
        post_it_text = unchecked_todos[0].get("summary")
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
