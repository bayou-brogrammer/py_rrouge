import game.color
from game.components import Fighter, HealingConsumable, Inventory
from game.components.ai import HostileEnemy
from game.entity import Actor, Item

player: Actor = Actor(
    char="@",
    color=game.color.yellow,
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=26),
)
orc: Actor = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
)
troll: Actor = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
)
health_potion: Item = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=HealingConsumable(amount=4),
)
