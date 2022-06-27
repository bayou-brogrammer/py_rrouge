from __future__ import annotations

import random
import traceback
from enum import Enum, auto
from pathlib import Path
from typing import List

import snecs
import tcod

import constants
import g
import game.exceptions
import game.handlers
from g_io import save_game
from game import color, ecs, systems
from game.entity import Actor
from game.gamemap import GameMap
from game.handlers.game_handler import GameOverEventHandler
from game.message_log import MessageLog
from game.node import Node
from game.typing import EventHandlerLike


class TurnState(Enum):
    PreRun = auto()
    AwaitingInput = auto()
    PlayerTurn = auto()
    MonsterTurn = auto()
    MainMenu = auto()
    GameOver = auto()


class Engine(Node):
    """Game Engine that powers the world"""

    gamemap: GameMap
    rng: random.Random
    mouse_location = (0, 0)

    player: Actor  # Entity ID
    turn_state: TurnState = TurnState.MainMenu
    systems: List[ecs.System]  # type: ignore

    def __init__(self) -> None:
        super().__init__()
        self.rng = random.Random()

        self.event_handler: EventHandlerLike = game.handlers.MainMenuHandler()
        self.root_console = tcod.Console(constants.screen_width, constants.screen_height, order="F")

        self.message_log = MessageLog()

        self.systems = [
            systems.FovSystem(),
            systems.AISystem(),
            systems.IndexingSystem(),
            systems.MeleeCombatSystem(),
            systems.DamageSystem(),
            systems.EndTurnSystem(),
        ]

    def run_game(self) -> None:
        try:
            while True:
                self.tick()
        except game.exceptions.QuitWithoutSaving:
            raise SystemExit()
        except SystemExit:  # Save and quit.
            save_game(Path("savegame.sav"))
            raise
        except BaseException:  # Save on any other error.
            save_game(Path("savegame.sav"))
            raise

    def run_systems(self) -> None:
        for system in self.systems:
            system.process()

        snecs.process_pending_deletions()

    def render(self) -> None:
        """Render the game."""
        self.root_console.clear()
        self.event_handler.on_render(console=self.root_console)
        g.context.present(self.root_console)

    def tick(self) -> None:
        self.render()

        if self.turn_state == TurnState.GameOver:
            self.event_handler = GameOverEventHandler()

        try:
            for event in tcod.event.get():
                g.context.convert_event(event)
                self.event_handler = self.event_handler.handle_events(event)
        except Exception:  # Handle exceptions in game.
            traceback.print_exc()  # Print error to stderr.
            # Then print the error to the message log.
            if isinstance(self.event_handler, game.handlers.EventHandler):
                g.engine.message_log.add_message(traceback.format_exc(), color.error)
