from typing import Optional

import tcod.event

from actions.actions import (
    Action,
    MovementAction,
    GoDown,
    OpenChest,
)
from actions.actions import *



class EventHandler(tcod.event.EventDispatch[Action]):
    """En klass som hanterar alla inputs som sker i spelet, ärver från en av tcods event klasser"""
    inventory_is_open: bool
    inventory_is_open = False

    def ev_quit(
        self, event: tcod.event.Quit
    ) -> Optional[
        Action
    ]:  # Den här metoden kallas på när användaren trycker på X i fönstret
        raise SystemExit()

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[
        Action
    ]:  # Den här metoden kallas på när användaren trycker på en tangent
        action: Optional[Action] = None

        key = event.sym  # Gör om eventet till en tcod.event variabel
        mod = event.mod

        match key:
            case tcod.event.K_w:  # Rörelser
                action = MovementAction(dx=0, dy=-1)
            case tcod.event.K_s:
                action = MovementAction(dx=0, dy=1)
            case tcod.event.K_a:
                action = MovementAction(dx=-1, dy=0)
            case tcod.event.K_d:
                action = MovementAction(dx=1, dy=0)
            case tcod.event.K_ESCAPE:  # För att stänga av spelet
                raise SystemExit()
            case tcod.event.K_LESS:  # För att gå ner en trappa
                action = GoDown()
            case tcod.event.K_i:  # För att öppna inventory
                return "inventory"
            case tcod.event.K_e:  # För att öppna en kista
                action = OpenChest()
            case tcod.event.K_RIGHT:  # För att bläddra i inventory
                action = "next_page"
            case tcod.event.K_LEFT:
                action = "previous_page"
            case tcod.event.K_RETURN:  # För att starta spelet
                action = "New Game"
            case tcod.event.K_r:  # För att göra om sin level up
                action = "Reset"

        return action
