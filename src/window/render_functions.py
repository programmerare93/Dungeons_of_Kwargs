from __future__ import annotations

from typing import TYPE_CHECKING

from window import color

if TYPE_CHECKING:
    from tcod import Console


def render_bar(
    x,
    y,
    console: Console,
    current_value: int,
    maximum_value: int,
    total_width: int,
    stat="HP",
    color1=color.bar_empty,
    color2=color.bar_filled,
) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=x, y=y, width=total_width, height=1, ch=1, bg=color1)

    if bar_width > 0:
        console.draw_rect(
            x=x, y=y, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=x,
        y=y - 1,
        string=f"{stat}: {current_value}/{maximum_value}",
        fg=(255, 255, 255),
    )
