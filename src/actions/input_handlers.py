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

        if key in (tcod.event.K_UP, tcod.event.K_KP_8, tcod.event.K_w):
            action = MovementAction(dx=0, dy=-1)
        elif key in (tcod.event.K_DOWN, tcod.event.K_KP_2, tcod.event.K_s):
            action = MovementAction(dx=0, dy=1)
        elif key in (tcod.event.K_LEFT, tcod.event.K_KP_4, tcod.event.K_a):
            action = MovementAction(dx=-1, dy=0)
        elif key in (tcod.event.K_RIGHT, tcod.event.K_KP_6, tcod.event.K_d):
            action = MovementAction(dx=1, dy=0)
        elif key == tcod.event.K_ESCAPE:
            raise SystemExit()
        elif key == tcod.event.K_LESS:
            action = GoDown()
        elif key == tcod.event.K_i:
            return "inventory"
        elif key == tcod.event.K_h:
            action = HealingAction()
        elif key == tcod.event.K_e:
            action = OpenChest()
        elif key == tcod.event.K_o:
            return "Level Up"
        elif key == tcod.event.K_1:
            action = UseItem()
        return action


class InventoryHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_ESCAPE:
            raise SystemExit()
        elif key == tcod.event.K_i:
            action = "close"
        elif key.name in [f"N{x}" for x in range(1, 10)]:
            action = key.name
        return action


class MainMenuHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_ESCAPE:
            raise SystemExit()
        elif key == tcod.event.K_RETURN:
            action = "New Game"
        return action


class DeathHandler(tcod.event.EventDispatch[None]):
    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        key = event.sym
        if key == tcod.event.K_ESCAPE:
            raise SystemExit()


class LevelUpHandler(tcod.event.EventDispatch[None]):
    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        key = event.sym
        if key == tcod.event.K_ESCAPE:
            raise SystemExit()

        elif key == tcod.event.K_1:
            return "max_hp"
        elif key == tcod.event.K_2:
            return "perception"
        elif key == tcod.event.K_3:
            return "strength"
        elif key == tcod.event.K_4:
            return "intelligence"
        elif key == tcod.event.K_5:
            return "dexterity"
        elif key == tcod.event.K_r:
            return "reset"


class PlayerCannotMove(tcod.event.EventDispatch[None]):
    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        key = event.sym
        if key == tcod.event.K_ESCAPE:
            raise SystemExit()
