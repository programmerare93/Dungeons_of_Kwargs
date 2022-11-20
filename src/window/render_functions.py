from __future__ import annotations

from typing import TYPE_CHECKING

from window import color

if TYPE_CHECKING:
    from tcod import Console


def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=2, y=66, width=total_width, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=2, y=66, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=2, y=66, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )
