from typing import Tuple, Type

import snecs

from game.components.intent import WantsToMelee
from game.components.stats import CombatStats, SufferDamage
from game.ecs import System
from game.ecs.component import try_entity_component

MeleeCTypes = Tuple[Type[WantsToMelee], Type[CombatStats]]
MeleeCs = Tuple[WantsToMelee, CombatStats]


class MeleeCombatSystem(System[MeleeCTypes, MeleeCs]):
    def process(self) -> None:
        for id, (wants_to_melee, stats) in self.query():
            if stats.hp > 0:
                target_stats = try_entity_component(wants_to_melee.target, CombatStats)
                if target_stats and target_stats.hp > 0:
                    damage = max(0, stats.power - target_stats.defense)
                    if damage == 0:
                        print("Swing and a miss")
                    else:
                        SufferDamage.new_damage(wants_to_melee.target, damage)

            snecs.remove_component(id, WantsToMelee)


DamageCTypes = Tuple[Type[SufferDamage], Type[CombatStats]]
DamageCs = Tuple[SufferDamage, CombatStats]


class DamageSystem(System[DamageCTypes, DamageCs]):
    def process(self) -> None:
        for id, (suffer_damage, stats) in self.query():
            stats.hp -= sum(suffer_damage.amount)
            snecs.remove_component(id, SufferDamage)

            if stats.hp <= 0:
                snecs.schedule_for_deletion(id)
