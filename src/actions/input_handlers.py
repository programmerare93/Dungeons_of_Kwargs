from typing import Optional

import tcod.event

from src.actions.actions import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        mod = event.mod

        if key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        elif key in (tcod.event.K_UP, tcod.event.K_KP_8):
            action = MovementAction(dx=0, dy=-1)
        elif key in (tcod.event.K_DOWN, tcod.event.K_KP_2):
            action = MovementAction(dx=0, dy=1)
        elif key in (tcod.event.K_LEFT, tcod.event.K_KP_4):
            action = MovementAction(dx=-1, dy=0)
        elif key in (tcod.event.K_RIGHT, tcod.event.K_KP_6):
            action = MovementAction(dx=1, dy=0)

        # No valid key was pressed
        return action
