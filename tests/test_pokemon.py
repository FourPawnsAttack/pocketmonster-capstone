"""
TEST CASES: Pokemon Class (pokemon.py)
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if os.environ.get("USE_SOLUTIONS") == "1":
    from solutions.pokemon import Pokemon
else:
    from pokemon import Pokemon

def run_tests():
    print("=" * 60)
    print("  TESTING MODULE 1: Pokemon Class (pokemon.py)")
    print("=" * 60)
    
    passed = 0
    total = 5

    # Test 1: Initialization
    try:
        p = Pokemon(
            name="Pikachu",
            poke_type="Electric",
            max_hp=40,
            attack=55,
            defense=40,
            moves=["Thunderbolt", "Quick Attack"],
            front_sprite="front.gif",
            back_sprite="back.gif"
        )
        assert getattr(p, "name", None) == "Pikachu", "p.name should be 'Pikachu'"
        assert getattr(p, "poke_type", None) == "Electric", "p.poke_type should be 'Electric'"
        assert getattr(p, "max_hp", None) == 40, "p.max_hp should be 40"
        assert getattr(p, "hp", None) == 40, "p.hp should start at full max_hp (40)"
        assert getattr(p, "attack", None) == 55, "p.attack should be 55"
        assert getattr(p, "defense", None) == 40, "p.defense should be 40"
        assert "Thunderbolt" in getattr(p, "moves", []), "p.moves should contain 'Thunderbolt'"
        print("  [PASS] ⭐ 1.1: Pokemon initializes all attributes correctly")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  1.1 Initialization Error: {e}")
        print("         Hint: Make sure __init__ sets `self.name = name`, `self.hp = max_hp`, etc.")
    except Exception as e:
        print(f"  [FAIL] ⚠️  1.1 Unexpected Error in __init__: {e}")

    # Test 2: take_damage lowers HP
    try:
        p = Pokemon("Charmander", "Fire", 50, 50, 50, ["Ember"])
        res = p.take_damage(15)
        assert p.hp == 35, f"Expected HP to be 35 after taking 15 damage from 50, got {p.hp}"
        print("  [PASS] ⭐ 1.2: take_damage() correctly lowers current HP")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  1.2 take_damage Error: {e}")
        print("         Hint: Did you subtract `amount` from `self.hp`?")
    except Exception as e:
        print(f"  [FAIL] ⚠️  1.2 Error in take_damage: {e}")

    # Test 3: take_damage clamping to 0
    try:
        p = Pokemon("Squirtle", "Water", 30, 40, 50, ["Water Gun"])
        p.take_damage(999)
        assert p.hp == 0, f"Expected HP to clamp at 0 when taking overkill damage, got {p.hp}"
        print("  [PASS] ⭐ 1.3: take_damage() clamps to 0 (no negative HP)")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  1.3 Clamp Error: {e}")
        print("         Hint: Add `if self.hp < 0: self.hp = 0` inside take_damage!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  1.3 Error in take_damage: {e}")

    # Test 4: heal increases HP and clamps to max_hp
    try:
        p = Pokemon("Bulbasaur", "Grass", 50, 45, 45, ["Tackle"])
        p.hp = 20
        p.heal(15)
        assert p.hp == 35, f"Expected HP to be 35 after healing 15 from 20, got {p.hp}"
        p.heal(100)
        assert p.hp == 50, f"Expected HP to not exceed max_hp (50), got {p.hp}"
        print("  [PASS] ⭐ 1.4: heal() restores HP and clamps to max_hp")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  1.4 heal Error: {e}")
        print("         Hint: Make sure `if self.hp > self.max_hp: self.hp = self.max_hp`")
    except Exception as e:
        print(f"  [FAIL] ⚠️  1.4 Error in heal: {e}")

    # Test 5: is_fainted check
    try:
        p = Pokemon("Pikachu", "Electric", 40, 50, 40, ["Spark"])
        p.hp = 10
        assert p.is_fainted() is False, "is_fainted() should return False when HP is 10"
        p.hp = 0
        assert p.is_fainted() is True, "is_fainted() should return True when HP is 0"
        p.hp = -5
        assert p.is_fainted() is True, "is_fainted() should return True when HP is <= 0"
        print("  [PASS] ⭐ 1.5: is_fainted() returns True when HP <= 0")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  1.5 is_fainted Error: {e}")
        print("         Hint: Return `self.hp <= 0` in is_fainted()")
    except Exception as e:
        print(f"  [FAIL] ⚠️  1.5 Error in is_fainted: {e}")

    # --- EDGE CASE TESTS ---

    # Test 6 (Edge Case): Zero or Negative Damage
    total += 1
    try:
        p = Pokemon("Charmander", "Fire", 50, 50, 50, ["Ember"])
        p.hp = 40
        p.take_damage(0)
        assert p.hp == 40, f"take_damage(0) should leave HP unchanged, but got {p.hp}"
        p.take_damage(-15)
        assert p.hp == 40, f"take_damage(-15) should NOT increase HP! Expected 40, got {p.hp}"
        print("  [PASS] ⭐ 1.6 [EDGE CASE]: take_damage handles 0 and negative damage safely")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  1.6 Zero/Negative Damage Error: {e}")
        print("         Hint: Add `if amount <= 0: return self.hp` at the start of take_damage!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  1.6 Error: {e}")

    # Test 7 (Edge Case): Zero or Negative Healing
    total += 1
    try:
        p = Pokemon("Squirtle", "Water", 50, 40, 50, ["Water Gun"])
        p.hp = 30
        p.heal(0)
        assert p.hp == 30, f"heal(0) should leave HP unchanged, got {p.hp}"
        p.heal(-10)
        assert p.hp == 30, f"heal(-10) should NOT decrease HP! Expected 30, got {p.hp}"
        print("  [PASS] ⭐ 1.7 [EDGE CASE]: heal handles 0 and negative healing safely")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  1.7 Zero/Negative Heal Error: {e}")
        print("         Hint: Add `if amount <= 0: return self.hp` at the start of heal!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  1.7 Error: {e}")

    # Test 8 (Edge Case): Healing already full Pokémon
    total += 1
    try:
        p = Pokemon("Bulbasaur", "Grass", 50, 45, 45, ["Tackle"])
        p.hp = 50
        p.heal(30)
        assert p.hp == 50, f"heal() when already at max HP should stay at max HP (50), got {p.hp}"
        print("  [PASS] ⭐ 1.8 [EDGE CASE]: heal() when already full HP remains at max HP")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  1.8 Full HP Heal Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  1.8 Error: {e}")

    # Test 9 (Edge Case): Boundary at exactly 1 HP vs 0 HP
    total += 1
    try:
        p = Pokemon("Pikachu", "Electric", 40, 50, 40, ["Spark"])
        p.hp = 1
        assert p.is_fainted() is False, "Pokémon with exactly 1 HP is NOT fainted!"
        p.take_damage(1)
        assert p.hp == 0, f"Expected 0 HP, got {p.hp}"
        assert p.is_fainted() is True, "Pokémon with exactly 0 HP IS fainted!"
        assert isinstance(p.is_fainted(), bool), "is_fainted() must return a boolean True/False!"
        print("  [PASS] ⭐ 1.9 [EDGE CASE]: is_fainted() precisely detects the 1 HP vs 0 HP boundary")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  1.9 Boundary Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  1.9 Error: {e}")

    print(f"\nModule 1 Score: {passed}/{total} tests passed.\n")
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
