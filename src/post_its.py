from .display import regular_font, BLACK, WHITE


def handle_post_its(post_it_entity, context, draw):
    if int(post_it_entity.state) > 0:
        post_it_text = context.get("todo.post_it").get("items")[0].get("summary")
        print(post_it_text)
        draw.rectangle([(0, 122 - 32), (250, 122)], BLACK)
        draw.text(
            (1, 122 - 32 + 6),
            post_it_text,
            font=regular_font,
            fill=WHITE,
        )
