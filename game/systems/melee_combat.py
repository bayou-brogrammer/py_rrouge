from typing import Tuple, Type

import snecs

import g
from game import color
from game.components import CombatStats, Name, SufferDamage, WantsToMelee
from game.ecs import System
from game.ecs.component import entity_components

MeleeCTypes = Tuple[Type[WantsToMelee], Type[CombatStats], Type[Name]]
MeleeCs = Tuple[WantsToMelee, CombatStats, Name]


class MeleeCombatSystem(System[MeleeCTypes, MeleeCs]):
    def process(self) -> None:
        for id, (wants_to_melee, stats, name) in self.query():
            if stats.hp > 0:
                (target_stats, target_name) = entity_components(wants_to_melee.target, (CombatStats, Name))
                if target_stats and target_stats.hp > 0:
                    damage = max(0, stats.power - target_stats.defense)

                    attack_desc = f"{name.capitalize()} attacks {target_name}"
                    if id is g.engine.player.id:
                        attack_color = color.player_atk
                    else:
                        attack_color = color.enemy_atk

                    if damage == 0:
                        g.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)
                    else:
                        SufferDamage.new_damage(wants_to_melee.target, damage)
                        g.engine.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_color)

            snecs.remove_component(id, WantsToMelee)


DamageCTypes = Tuple[Type[SufferDamage], Type[CombatStats], Type[Name]]
DamageCs = Tuple[SufferDamage, CombatStats, Name]


class DamageSystem(System[DamageCTypes, DamageCs]):
    def process(self) -> None:
        for id, (suffer_damage, stats, name) in self.query():
            stats.hp -= sum(suffer_damage.amount)
            snecs.remove_component(id, SufferDamage)

            if stats.hp <= 0:
                if g.engine.player.id is id:
                    death_message = "You died!"
                    death_message_color = color.player_die
                else:
                    death_message = f"{name} is dead!"
                    death_message_color = color.enemy_die
                    snecs.schedule_for_deletion(id)

                g.engine.message_log.add_message(death_message, death_message_color)
