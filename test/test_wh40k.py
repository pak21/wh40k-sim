import pytest

import wh40k

@pytest.mark.parametrize('strength, toughness, expected', [
    (10,  5, 2),
    ( 9,  5, 3),
    ( 6,  5, 3),
    ( 5,  5, 4),
    ( 5,  6, 5),
    ( 5,  9, 5),
    ( 5, 10, 6),
])
def test_wound_roll(strength, toughness, expected):
    wound_roll = wh40k.wound_roll(strength, toughness)

    assert wound_roll == expected

@pytest.mark.parametrize('n, expected', [
    (2, 5/6),
    (3, 4/6),
    (4, 3/6),
    (5, 2/6),
    (6, 1/6),
    (None, 0),
])
def test_n_up_to_fraction(n, expected):
    fraction = wh40k.n_up_to_fraction(n)

    assert fraction == expected

@pytest.mark.parametrize('ap, expected', [(0, 3), (1, 4), (2, 5), (3, 6), (4, None)])
def test_save_without_invulnerable(ap, expected):
    unit = wh40k.Unit(4, 2, 3, None)

    save = wh40k.get_save(unit, ap)

@pytest.mark.parametrize('ap, expected', [(0, 3), (1, 4), (2, 5), (3, 5), (4, 5)])
def test_save_with_invulnerable(ap, expected):
    unit = wh40k.Unit(4, 2, 3, 5)

    save = wh40k.get_save(unit, ap)

    assert save == expected

@pytest.mark.parametrize('attacks, weapon_skill, strength, ap, damage, expected', [
    # 'Base' case: 1 attack, WS 4+, AP 0, S4 (vs T4), 1 damage
    (1, 4, 4, 0, 1, 1/8),
    
    # Each of these cases changes one parameter from the base case
    (2, 4, 4, 0, 1, 1/4), # 2 attacks
    (1, 3, 4, 0, 1, 1/6), # WS 3+
    (1, 4, 3, 0, 1, 1/12), # S3
    (1, 4, 4, 1, 1, 1/6), # AP -1
    (1, 4, 4, 0, 3, 3/8), # 3 damage
])
def test_average_damage(attacks, weapon_skill, strength, ap, damage, expected):
    unit = wh40k.Unit(4, 4, 4, None)
    weapon = wh40k.Weapon(attacks, weapon_skill, strength, ap, damage)

    average_damage = wh40k.average_damage(unit, weapon)

    assert average_damage == pytest.approx(expected)
