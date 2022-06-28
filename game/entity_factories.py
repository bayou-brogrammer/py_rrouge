from game.components.ai import HostileEnemy
from game.components.fighter import Fighter
from game.entity import Actor

player: Actor = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
)

orc: Actor = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
)
troll: Actor = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
)
