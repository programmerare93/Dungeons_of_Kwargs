from typing import Optional

import tcod.event

from actions.actions import Action, MovementAction, GoDown, HealingAction, UseItem


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        mod = event.mod

        if key in (tcod.event.K_UP, tcod.event.K_KP_8):
            action = MovementAction(dx=0, dy=-1)
        elif key in (tcod.event.K_DOWN, tcod.event.K_KP_2):
            action = MovementAction(dx=0, dy=1)
        elif key in (tcod.event.K_LEFT, tcod.event.K_KP_4):
            action = MovementAction(dx=-1, dy=0)
        elif key in (tcod.event.K_RIGHT, tcod.event.K_KP_6):
            action = MovementAction(dx=1, dy=0)
        elif key == tcod.event.K_ESCAPE:
            raise SystemExit()
        elif key == tcod.event.K_LESS:
            action = GoDown()
        elif key == tcod.event.K_h:
            action = HealingAction()
        elif key == tcod.event.K_o:
            return "Level Up"
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
