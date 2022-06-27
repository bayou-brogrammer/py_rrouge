"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import lzma
import pickle
from pathlib import Path

import g
import game.color
import game.engine


def save_game(path: Path) -> None:
    """If an engine is active then save it."""
    if not hasattr(g, "engine"):
        return  # If called before a new game is started then g.engine is not assigned.
    path.write_bytes(lzma.compress(pickle.dumps(g.engine)))
    print("Game saved.")


def load_game(path: Path) -> game.engine.Engine:
    """Load an Engine instance from a file."""
    engine = pickle.loads(lzma.decompress(path.read_bytes()))
    assert isinstance(engine, game.engine.Engine)
    g.engine = engine
    return engine
