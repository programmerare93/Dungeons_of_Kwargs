from __future__ import annotations

from typing import TYPE_CHECKING

from window.color import *

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
    color1=bar_empty,
    color2=bar_filled,
) -> None:
    """En funktion för att rita en statusbar"""
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=x, y=y, width=total_width, height=1, ch=1, bg=color1)

    if bar_width > 0:
        console.draw_rect(x=x, y=y, width=bar_width, height=1, ch=1, bg=color2)

    console.print(
        x=x,
        y=y - 1,
        string=f"{stat}: {current_value}/{maximum_value}",
        fg=white,
    )
