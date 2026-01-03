from PIL import ImageDraw
from base_component import BaseComponent


class Todo(BaseComponent):
    def __init__(self, entity_id):
        super().__init__(entity_id)
        self.entity = None
        self.todo_domain = None
        self.todos = []

    def fetch_data(self, client):
        if not self.entity:
            self.entity = client.get_state(entity_id=self.entity_id)

        if not self.todo_domain:
            self.todo_domain = client.get_domain("todo")

        _, data = self.todo_domain.get_items(
            entity_id=self.entity_id,
        )

        last_todos = self.todos
        self.todos = data

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
                fill=self.BLACK,
            )
            return img

        post_it_text = self.entity.get("items")[0].get("summary")
        print(post_it_text)
        draw.rectangle([(0, 122 - 32), (250, 122)], self.BLACK)
        draw.text(
            (1, 122 - 32 + 6),
            post_it_text,
            font=self.large_font,
            fill=self.WHITE,
        )

        return img
