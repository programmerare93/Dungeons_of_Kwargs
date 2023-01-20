from typing import Set, Iterable, Any
import time
import winsound

import tcod.constants
from tcod import Console
from tcod.context import Context
from tcod.map import compute_fov

import stage.tile_types as tile_types

from actions.input_handlers import *
from creature.entity import Entity, Player, Monster
from stage.game_map import GameMap
from stage.procgen import Generator
from stage.floor import Floor
from window.render_functions import render_bar
from window.message_log import MessageLog
from window import color, window
from window.window import Window


class Engine:
    """Klassen för spel motorn, håller koll på i princip alla delar av spelat och fungerar som en central hub för allt som händer i spelet."""

    def __init__(
        self,
        game_map: GameMap,
        player: Entity,
        floor: Floor,
        generator: Generator,
        player_can_attack: bool = True,
        player_can_move: bool = False,
        player_attack_cool_down: int = 0,
        window: Window = None,
    ):
        self.window = window
        self.event_handler = EventHandler()
        self.game_map = game_map
        self.message_log = MessageLog()
        self.player = player
        self.floor = floor
        self.generator = generator
        self.tick = 0
        self.monster_tick = 0
        self.game_has_started = False
        self.inventory_open = False
        self.player_can_move = player_can_move
        self.player_can_attack = player_can_attack
        self.player_attack_cool_down = player_attack_cool_down
        self.update_game_map()
        self.update_fov()
        self.window = window
        self.creatures = [x for x in self.game_map.entities if x.char != "C"]

    def update_game_map(self) -> None:
        """Uppdaterar spel kartan när spelaren hamnar på en ny våning."""
        if self.game_map:
            self.game_map.entities = [self.player]
        self.generator.generate_dungeon()
        self.game_map = self.generator.get_dungeon()
        self.update_fov()
        self.tick = 0
        self.monster_tick = 0
        self.generator.difficulty += 1
        self.game_map.difficulty += 1
        self.generator.max_monsters_per_room = self.generator.difficulty * 2
        self.floor.floor += 1
        self.creatures = [x for x in self.game_map.entities if x.char != "C"]

    def entity_activated_trap(self, x: int, y: int) -> bool:
        """Kollar om spelaren har aktiverat en fälla."""
        return isinstance(self.game_map.tiles[x, y], tile_types.Trap)

    def handle_events(self) -> None:
        """Tar hand om alla event som sker i spelet."""
        events = tcod.event.wait()  # Samlar alla event som sker i spelet
        for event in events:
            if isinstance(event, tcod.event.MouseButtonDown) and event.button == 1:
                # Mus knapp tryck är specialfall och måste konverteras till en tile
                self.window.context.convert_event(event)
                return tuple(event.tile)
            elif isinstance(event, tcod.event.MouseButtonDown) and event.button == 3:
                self.window.context.convert_event(event)
                return list(event.tile)
            action = self.event_handler.dispatch(
                event
            )  # Dispatch metoden ärvs av EventHandler klassen från tcod.event klassen, så vi vet inte hur den fungerar, fast den kommer att kalla på andra funktioner i event_handler
            if action in [str(x) for x in range(6)]:
                return action
            elif action == "exit" and not self.inventory_open:
                raise SystemExit()

            elif action == "exit" and self.inventory_open:
                return None

            match action:  # Tittar på vad som händer i action variabeln och gör något beroende på vad det är
                case None:  # Ifall det inte är något så gör vi inget
                    continue
                case "inventory":
                    if (
                        self.game_has_started
                    ):  # Om spelet har startat så öppnas inventoryt
                        self.inventory_open = not self.inventory_open
                        return "inventory"
                    else:
                        continue
                case "close":  # Fortsätter bara efter det event_handler gav oss och ger det sedan till de game_loops som vill ha det
                    return "close"
                case "next_page":
                    return "next_page"
                case "previous_page":
                    return "previous_page"
                case "New Game":
                    return "new_game"
                case "Reset":
                    return "reset"

            if (
                action.perform(self, self.player) is not None
            ):  # Ifall spelaren gjorde något som att röra sig eller attackera så ökas antalet ticks
                self.tick += 1
                self.update_fov()  # Uppdaterar spelarens fält av syn

    def handle_enemy_AI(self) -> None:
        """Tar hand om hur fiender beter sig."""
        if self.monster_tick != self.tick:  # Om spelaren har gjort något
            self.game_map.generate_pathfinding_map()  # Tittar på spelplanen och skapar en pathfinding karta
            for monster in self.game_map.entities:
                if (
                    monster.char not in ("@", "C")
                    and random.randint(0, 100) < monster.move_chance
                    and monster.hp > 0
                    and self.game_map.calculate_distance(
                        monster.x, monster.y, self.player.x, self.player.y
                    )
                    <= monster.perception  # Ifall spelaren är inom fiendens syn
                ):
                    if (
                        monster.hp
                        < monster.max_hp
                        // 2  # Ifall monstret är skadat så kan den använda en brygd
                        and monster.items
                        and not monster.used_items
                        and random.randint(0, 100) > 50
                    ):
                        item = monster.choose_item()
                        item.use(engine=self, entity=monster)
                    else:
                        monster.monster_pathfinding(
                            self.player, self.game_map, self
                        )  # Fienden försöker hitta en väg till spelaren
            self.monster_tick = (
                self.tick
            )  # Efter att ha kollat på varenda fiende så ökas antalet monster ticks till det nuvarande tick antalet

    def can_player_attack(self) -> None:
        """Sätter bara en cooldown på spelarens attack så att spelaren inte kan attackera för ofta."""
        if not self.player_can_attack:
            self.player_attack_cool_down = time.time()
            self.player_can_attack = "None"

        if time.time() - self.player_attack_cool_down >= 1:
            self.player_can_attack = True

    def handle_used_items(self) -> None:
        """Behandlar alla items som spelaren eller alla monster använt."""
        for entity in self.creatures:
            if entity.used_items != []:
                for item in entity.used_items:
                    if (
                        self.tick - item.activated_tick >= item.duration
                    ):  # Kontrollerar om items duration har gått ut
                        item.remove_effect(entity)
                        self.message_log.add_message(
                            f"The {entity.name}'s {item.type} has worn off!",
                            yellow,
                        )

    def update_fov(self) -> None:
        """Ändrar fältet av syn baserat på spelarens position och vad som är transparent eller inte"""
        for (x, row) in enumerate(self.game_map.tiles):
            for (y, value) in enumerate(row):
                if self.game_map.get_tile(x, y).transparent:
                    self.game_map.transparent_tiles[x, y] = True

        self.game_map.visible[:] = compute_fov(
            transparency=self.game_map.transparent_tiles,
            pov=(self.player.x, self.player.y),
            radius=self.player.perception // 2,
            algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST,
        )

    def check_inventory(self) -> str:
        if self.inventory_open:
            return "open"

    def check_entities(self) -> str:
        """Tittar på alla entities och kollar om de har 0 eller mindre hp, om de har det så dör de och xp läggs till spelaren"""
        for entity in self.game_map.entities:
            if entity.hp <= 0:
                if entity.char == "@":
                    return "player_kill"
                self.message_log.add_message(f"{entity.name} died!", color.death_text)
                self.game_map.entities.remove(entity)
                self.creatures.remove(entity)
                self.player.xp += entity.xp_value
                self.render(console=self.window.console, context=self.window.context)
                self.player_can_attack = True
                if entity.name == "Ancient Titan":
                    return "boss_kill"
                # self.sound_handler.monster_death()
                break

        self.game_map.explored |= self.game_map.visible

    def check_xp(self) -> str:
        """Kollar om spelaren har tillräckligt med xp för att levla upp"""
        if self.player.xp >= self.player.xp_to_next_level:
            self.player.level += 1
            self.message_log.add_message(
                f"You are now level {self.player.level}!", blue
            )
            self.player.xp_to_next_level *= 2
            return "Level Up"

    def render(self, console: Console, context: Context) -> None:
        """Renderar allt som ska visas på skärmen"""
        self.game_map.render(console)
        render_bar(  # Visar HP
            x=2,
            y=65,
            console=console,
            current_value=self.player.hp,
            maximum_value=self.player.max_hp,
            total_width=20,
        )
        render_bar(  # Visar XP
            x=2,
            y=68,
            console=console,
            current_value=self.player.xp,
            maximum_value=self.player.xp_to_next_level,
            total_width=20,
            color1=white,
            color2=blue,
            stat="XP",
        )
        self.message_log.render_messages(
            console=console, x=23, y=62, width=38, height=6
        )  # Visar meddelanden
        self.window.render_log(  # Visar loggen
            player=self.player,
        )
        context.present(console)  # Presenterar allt som ska visas på skärmen

        console.clear()  # Tömmer konsolen
