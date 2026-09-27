"""
====================================================================
           TEST SUITE: POKÉMON TEAM & PARTY SYSTEM
====================================================================
Validates 4-Pokémon party capacity, conscious tracking, switching,
and full-team Pokémon Center healing.
====================================================================
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from solutions.pokemon import Pokemon
from team import (
    MAX_PARTY_SIZE,
    can_add_to_party,
    add_to_party,
    remove_from_party,
    get_active_pokemon,
    is_pokemon_conscious,
    get_conscious_pokemon,
    has_conscious_pokemon,
    switch_pokemon,
    swap_party_order,
    heal_party,
    create_team_pokemon,
)

def make_mon(name="Pikachu", hp=40, max_hp=40):
    mon = Pokemon(name, "Electric", max_hp, 50, 40, ["Quick Attack", "Thunderbolt"], "", "")
    mon.hp = hp
    return mon

def test_party_max_size_enforced():
    party = []
    for i in range(MAX_PARTY_SIZE):
        assert can_add_to_party(party) is True
        assert add_to_party(party, make_mon(f"Mon{i}")) is True

    assert len(party) == 4
    assert can_add_to_party(party) is False
    # 5th Pokémon cannot be added to active party
    assert add_to_party(party, make_mon("ExtraMon")) is False
    assert len(party) == 4
    print("  [PASS] ⭐ 7.1: Party enforces strict 4-Pokémon maximum capacity")

def test_add_to_party_rejects_none():
    party = []
    assert add_to_party(party, None) is False
    assert len(party) == 0
    print("  [PASS] ⭐ 7.2: add_to_party gracefully rejects None and non-lists")

def test_conscious_pokemon_tracking():
    p1 = make_mon("Pikachu", hp=40)
    p2 = make_mon("Charmander", hp=0)   # Fainted
    p3 = make_mon("Squirtle", hp=1)     # Barely alive (1 HP boundary)
    p4 = make_mon("Bulbasaur", hp=-5)   # Fainted clamp

    party = [p1, p2, p3, p4]

    assert has_conscious_pokemon(party) is True
    conscious = get_conscious_pokemon(party)
    assert len(conscious) == 2
    assert conscious[0].name == "Pikachu"
    assert conscious[1].name == "Squirtle"

    # Now faint all
    p1.hp = 0
    p3.hp = 0
    assert has_conscious_pokemon(party) is False
    assert len(get_conscious_pokemon(party)) == 0
    print("  [PASS] ⭐ 7.3: has_conscious_pokemon and get_conscious_pokemon track alive members")

def test_switch_pokemon_valid():
    p1 = make_mon("Pikachu", hp=40)
    p2 = make_mon("Charmander", hp=45)
    party = [p1, p2]

    success, new_idx, msg = switch_pokemon(party, current_index=0, target_index=1)
    assert success is True
    assert new_idx == 1
    assert "Charmander" in msg
    print("  [PASS] ⭐ 7.4: switch_pokemon successfully switches to conscious teammate")

def test_switch_pokemon_cannot_switch_to_active():
    p1 = make_mon("Pikachu", hp=40)
    p2 = make_mon("Charmander", hp=45)
    party = [p1, p2]

    success, new_idx, msg = switch_pokemon(party, current_index=0, target_index=0)
    assert success is False
    assert new_idx == 0
    assert "already in battle" in msg.lower()
    print("  [PASS] ⭐ 7.5: switch_pokemon prevents switching to already-active Pokémon")

def test_switch_pokemon_cannot_switch_to_fainted():
    p1 = make_mon("Pikachu", hp=40)
    p2 = make_mon("Charmander", hp=0) # Fainted
    party = [p1, p2]

    success, new_idx, msg = switch_pokemon(party, current_index=0, target_index=1)
    assert success is False
    assert new_idx == 0
    assert "fainted" in msg.lower()
    print("  [PASS] ⭐ 7.6: switch_pokemon blocks switching to fainted Pokémon")

def test_heal_party_restores_all():
    p1 = make_mon("Pikachu", hp=5, max_hp=40)
    p2 = make_mon("Charmander", hp=0, max_hp=45)
    p3 = make_mon("Bulbasaur", hp=20, max_hp=50)
    party = [p1, p2, p3]

    healed_count = heal_party(party)
    assert healed_count == 3
    assert p1.hp == 40
    assert p2.hp == 45
    assert p3.hp == 50
    assert has_conscious_pokemon(party) is True
    print("  [PASS] ⭐ 7.7: heal_party restores all Pokémon in party back to full HP")

def test_create_team_pokemon_factory():
    mon = create_team_pokemon(Pokemon, "Pidgey", level=6)
    assert mon.name == "Pidgey"
    assert mon.level == 6
    assert mon.hp == mon.max_hp
    assert len(mon.moves) > 0
    print("  [PASS] ⭐ 7.8: create_team_pokemon instantiates registered species from templates")

def test_remove_from_party_preserves_at_least_one():
    p1 = make_mon("Pikachu")
    p2 = make_mon("Eevee")
    party = [p1, p2]

    removed = remove_from_party(party, 1)
    assert removed.name == "Eevee"
    assert len(party) == 1

    # Cannot remove last Pokémon
    last_removed = remove_from_party(party, 0)
    assert last_removed is None
    assert len(party) == 1
    print("  [PASS] ⭐ 7.9: remove_from_party guarantees trainer always has at least 1 Pokémon")

def run_tests():
    print("\n" + "=" * 60)
    print("  TESTING MODULE 7: 4-POKÉMON PARTY & TEAM SYSTEM (team.py)")
    print("=" * 60)
    tests = [
        test_party_max_size_enforced,
        test_add_to_party_rejects_none,
        test_conscious_pokemon_tracking,
        test_switch_pokemon_valid,
        test_switch_pokemon_cannot_switch_to_active,
        test_switch_pokemon_cannot_switch_to_fainted,
        test_heal_party_restores_all,
        test_create_team_pokemon_factory,
        test_remove_from_party_preserves_at_least_one,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {t.__name__}: {e}")
        except Exception as e:
            print(f"  [ERROR] {t.__name__}: {e}")

    print(f"\nTeam Score: {passed}/{len(tests)} tests passed.")
    return passed == len(tests)

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
