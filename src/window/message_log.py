from typing import List, Reversible, Tuple
import textwrap

import tcod

from window.color import *


class Message:
    """Klass för att representera ett meddelande"""

    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        self.count = 1  # Antalet gånger som meddelandet har skickats i rad

    @property
    def full_text(self) -> str:
        """Hela texten, inklusive antalet gånger den har stackats"""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"  # x2, x3, x4... om meddelandet stackas
        return self.plain_text


class MessageLog:
    """Klass som tar hand om alla meddelanden som skrivs ut"""

    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(
        self,
        text: str,
        fg: Tuple[int, int, int] = white,
        *,
        stack: bool = True,
    ) -> None:
        """Används för att lägga till ett meddelande till loggen."""
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(
                Message(text, fg)
            )  # Gör om meddelandet till en Message-objekt och lägger till det i listan

    def render_messages(
        self,
        console: tcod.Console,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        """Visa meddelanden i en lista, från äldsta till nyaste."""
        y_offset = height - 1

        for message in reversed(
            self.messages
        ):  # Reversed gör så att äldsta meddelandet visas först
            for line in reversed(
                textwrap.wrap(message.full_text, width)
            ):  # Wrap ger tillbaka en lista med texten som är wrapped till bredden
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return  # Inga fler meddelanden får plats på skärmen
