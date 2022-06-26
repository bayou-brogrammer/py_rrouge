from __future__ import annotations

import logging
import random
import traceback
from enum import Enum, auto

import tcod

import constants
import game.exceptions
import game.handlers
from game import systems
from game.entity import Actor
from game.gamemap import GameMap
from game.node import Node
from game.typing import EventHandlerLike

logger = logging.getLogger(__name__)


class TurnState(Enum):
    PreRun = auto()
    AwaitingInput = auto()
    PlayerTurn = auto()
    MonsterTurn = auto()


class Engine(Node):
    """Game Engine that powers the world"""

    gamemap: GameMap
    rng: random.Random
    mouse_location = (0, 0)

    player: Actor  # Entity ID
    turn_state: TurnState = TurnState.PreRun

    def __init__(self, context: tcod.context.Context) -> None:
        super().__init__()
        self.rng = random.Random()

        self.context = context
        self.event_handler: EventHandlerLike = game.handlers.MainMenuHandler()
        self.root_console = tcod.Console(constants.screen_width, constants.screen_height, order="F")

        self.systems = [systems.FovSystem()]

    def run_game(self) -> None:
        try:
            while True:
                self.tick()
        except game.exceptions.QuitWithoutSaving:
            raise SystemExit()
        except SystemExit:  # Save and quit.
            # game_io.save_game(Path("savegame.sav"))
            raise
        except BaseException:  # Save on any other error.
            # game_io.save_game(Path("savegame.sav"))
            raise

    def __transition_state__(self) -> None:
        match self.turn_state:
            case TurnState.PreRun:
                self.turn_state = TurnState.PlayerTurn
            case TurnState.PlayerTurn:
                self.turn_state = TurnState.MonsterTurn
            case TurnState.MonsterTurn:
                self.turn_state = TurnState.PlayerTurn

    def run_systems(self) -> None:
        for system in self.systems:
            system.process()

        self.__transition_state__()

    def render(self) -> None:
        """Render the game."""
        self.root_console.clear()
        self.event_handler.on_render(console=self.root_console)
        self.context.present(self.root_console)

    def tick(self) -> None:
        self.render()

        try:
            for event in tcod.event.wait():
                self.context.convert_event(event)
                self.event_handler = self.event_handler.handle_events(event)
        except Exception:  # Handle exceptions in game.
            traceback.print_exc()  # Print error to stderr.

            # Then print the error to the message log.
            if isinstance(self.event_handler, game.handlers.EventHandler):
                logger.debug("Stack Error: :)")
            #     g.engine.message_log.add_message(traceback.format_exc(), game.color.error)
