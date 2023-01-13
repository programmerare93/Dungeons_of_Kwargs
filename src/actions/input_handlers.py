from typing import Optional

import tcod.event

from actions.actions import (
    Action,
    MovementAction,
    GoDown,
    HealingAction,
    OpenChest,
    UseItem,
)
from actions.actions import *


class EventHandler(tcod.event.EventDispatch[Action]):
    inventory_is_open: bool
    inventory_is_open = False

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        mod = event.mod

        match key:
            case tcod.event.K_w:
                action = MovementAction(dx=0, dy=-1)
            case tcod.event.K_s:
                action = MovementAction(dx=0, dy=1)
            case tcod.event.K_a:
                action = MovementAction(dx=-1, dy=0)
            case tcod.event.K_d:
                action = MovementAction(dx=1, dy=0)
            case tcod.event.K_ESCAPE:
                raise SystemExit()
            case tcod.event.K_LESS:
                action = GoDown()
            case tcod.event.K_i:
                return "inventory"
            case tcod.event.K_h:
                action = HealingAction()
            case tcod.event.K_e:
                action = OpenChest()
            case tcod.event.K_o:
                return "Level Up"
            case tcod.event.K_RIGHT:
                action = "next_page"
            case tcod.event.K_LEFT:
                action = "previous_page"
            case tcod.event.K_RETURN:
                action = "New Game"
            case tcod.event.K_r:
                action = "Reset"

        return action
