from typing import List

import snecs
from snecs import RegisteredComponent
from snecs.typedefs import EntityID

from game.ecs.component import try_entity_component


class Name(RegisteredComponent):
    def __init__(self, name: str) -> None:
        self.name = name


class CombatStats(RegisteredComponent):
    def __init__(self, hp: int, max_hp: int, power: int, defense: int) -> None:
        self.hp = hp
        self.max_hp = max_hp
        self.power = power
        self.defense = defense


class SufferDamage(RegisteredComponent):
    def __init__(self) -> None:
        self.amount: List[int] = []

    @staticmethod
    def new_damage(victim: EntityID, amount: int) -> None:
        if store := try_entity_component(victim, SufferDamage):
            store.amount.append(amount)
        else:
            store = SufferDamage()
            store.amount.append(amount)
            snecs.add_component(victim, store)
