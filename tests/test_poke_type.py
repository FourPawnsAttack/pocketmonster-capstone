"""
TEST CASES: PokeType System (poke_type.py)
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from poke_type import PokeType

def run_tests():
    print("=" * 60)
    print("  TESTING MODULE: PokeType Class (poke_type.py)")
    print("=" * 60)

    passed = 0
    total = 7

    # Test 1: PokeType creation and registry
    try:
        fire = PokeType.get("Fire")
        assert isinstance(fire, PokeType), "PokeType.get('Fire') should return a PokeType instance"
        assert fire.name == "Fire", f"Expected name 'Fire', got '{fire.name}'"
        print("  [PASS] ⭐ T.1: PokeType retrieved from registry correctly")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  T.1 Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  T.1 Unexpected Error: {e}")

    # Test 2: Offensive effectiveness
    try:
        fire = PokeType.get("Fire")
        water = PokeType.get("Water")
        grass = PokeType.get("Grass")

        assert fire.effectiveness_against(grass) == 2.0, "Fire against Grass should be 2.0x (Super effective)"
        assert fire.effectiveness_against(water) == 0.5, "Fire against Water should be 0.5x (Not very effective)"
        assert fire.effectiveness_against("Electric") == 1.0, "Fire against Electric should be 1.0x (Neutral)"
        print("  [PASS] ⭐ T.2: Offensive effectiveness_against works correctly")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  T.2 Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  T.2 Unexpected Error: {e}")

    # Test 3: Defensive multipliers
    try:
        grass = PokeType.get("Grass")
        water = PokeType.get("Water")

        assert grass.defensive_multiplier_against("Fire") == 2.0, "Grass defending against Fire should take 2.0x damage"
        assert water.defensive_multiplier_against("Fire") == 0.5, "Water defending against Fire should take 0.5x damage"
        assert water.defensive_multiplier_against("Normal") == 1.0, "Water defending against Normal should take 1.0x damage"
        print("  [PASS] ⭐ T.3: Defensive defensive_multiplier_against works correctly")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  T.3 Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  T.3 Unexpected Error: {e}")

    # Test 4: String equality and representation
    try:
        electric = PokeType.get("Electric")
        assert electric == "Electric", "PokeType('Electric') should equal string 'Electric'"
        assert electric == "electric", "Equality should be case-insensitive"
        assert str(electric) == "Electric", "str(PokeType('Electric')) should return 'Electric'"
        assert repr(electric) == "PokeType('Electric')"
        print("  [PASS] ⭐ T.4: String interoperability (__str__, __eq__, __repr__) works seamlessly")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  T.4 Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  T.4 Unexpected Error: {e}")

    # Test 5: Dynamic type creation and custom interactions
    try:
        custom = PokeType("Cosmic")
        custom.add_advantage("Ghost")
        custom.add_disadvantage("Psychic")
        assert custom.effectiveness_against("Ghost") == 2.0
        assert custom.effectiveness_against("Psychic") == 0.5
        assert custom.effectiveness_against("Normal") == 1.0
        print("  [PASS] ⭐ T.5: Custom types and dynamic matchup modifications work")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  T.5 Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  T.5 Unexpected Error: {e}")

    # Test 6: Dual typing simulation (Architecture capability)
    try:
        # Gyarados or Mantine: Water / Flying dual-type attacked by Electric
        water = PokeType.get("Water")
        flying = PokeType.get("Flying")
        electric = PokeType.get("Electric")

        dual_mult = water.defensive_multiplier_against(electric) * flying.defensive_multiplier_against(electric)
        assert dual_mult == 4.0, f"Electric vs Water/Flying should deal 4.0x damage, got {dual_mult}"
        print("  [PASS] ⭐ T.6: Dual-type composite effectiveness (4.0x) calculated cleanly")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  T.6 Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  T.6 Unexpected Error: {e}")

    # Test 7: Unknown types fallback safely to neutral (1.0x)
    try:
        unknown_atk = PokeType.get("Alien")
        unknown_def = PokeType.get("Mystic")
        assert unknown_atk.effectiveness_against(unknown_def) == 1.0
        assert unknown_def.defensive_multiplier_against(unknown_atk) == 1.0
        print("  [PASS] ⭐ T.7: Unknown types safely default to 1.0x neutral multiplier")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  T.7 Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  T.7 Unexpected Error: {e}")

    print(f"\nPokeType Score: {passed}/{total} tests passed.\n")
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
