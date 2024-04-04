import dataclasses
from typing import Optional

@dataclasses.dataclass
class Unit:
    toughness: int
    wounds: int
    armour_save: int
    invulnerable_save: Optional[int]

@dataclasses.dataclass
class Weapon:
    attacks: int
    weapon_skill: int
    strength: int
    armour_penetration: int
    damage: int

def wound_roll(strength: int, toughness: int) -> int:
    if strength >= 2 * toughness:
        return 2

    if strength > toughness:
        return 3

    if strength == toughness:
        return 4

    if 2 * strength > toughness:
        return 5

    return 6

def n_up_to_fraction(n: Optional[int]) -> float:
    return (7-n)/6 if n else 0

def get_save(unit: Unit, ap: int) -> Optional[int]:
    save = unit.armour_save + ap
    if unit.invulnerable_save:
        save = min(save, unit.invulnerable_save)

    return save if save <= 6 else None

def average_damage(unit: Unit, weapon: Weapon) -> float:
    attack_success_fraction = n_up_to_fraction(weapon.weapon_skill)
    wound_success_fraction = n_up_to_fraction(wound_roll(weapon.strength, unit.toughness))
    save_success_fraction = 1 - n_up_to_fraction(get_save(unit, weapon.armour_penetration))

    return weapon.attacks * attack_success_fraction * wound_success_fraction * save_success_fraction * weapon.damage
