"""
TEST CASES: Battle Engine (battle.py)
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if os.environ.get("USE_SOLUTIONS") == "1":
    from solutions.battle import get_type_multiplier, calculate_damage, choose_enemy_move
    from solutions.pokemon import Pokemon
else:
    from battle import get_type_multiplier, calculate_damage, choose_enemy_move
    from pokemon import Pokemon

def run_tests():
    print("=" * 60)
    print("  TESTING MODULE 3: Battle Engine (battle.py)")
    print("=" * 60)
    
    passed = 0
    total = 5

    # Test 1: Type Multipliers
    try:
        assert get_type_multiplier("Water", "Fire") == 2.0, "Water vs Fire should be 2.0x (Super Effective!)"
        assert get_type_multiplier("Fire", "Water") == 0.5, "Fire vs Water should be 0.5x (Not Very Effective)"
        assert get_type_multiplier("Normal", "Normal") == 1.0, "Normal vs Normal should be 1.0x (Neutral)"
        print("  [PASS] ⭐ 3.1: get_type_multiplier calculates type matchups correctly")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  3.1 Type Multiplier Error: {e}")
        print("         Hint: Check TYPE_CHART dictionary in pokemon_data.py")
    except Exception as e:
        print(f"  [FAIL] ⚠️  3.1 Error in get_type_multiplier: {e}")

    # Test 2: Damage Calculation format
    try:
        p1 = Pokemon("Charmander", "Fire", 50, 50, 40, ["Ember"])
        p2 = Pokemon("Bulbasaur", "Grass", 50, 40, 40, ["Tackle"])
        result = calculate_damage("Ember", p1, p2)
        assert result is not None, "calculate_damage returned None! Did you forget `return damage, is_critical, type_mult`?"
        assert isinstance(result, tuple) and len(result) == 3, f"Expected a tuple of 3 items (damage, is_critical, type_multiplier), got {result}"
        dmg, crit, mult = result
        assert isinstance(dmg, int), f"Damage should be an integer, got {type(dmg)}"
        assert dmg > 0, f"Damage should be greater than 0, got {dmg}"
        assert isinstance(crit, bool), f"is_critical should be a boolean (True/False), got {crit}"
        print("  [PASS] ⭐ 3.2: calculate_damage returns correct tuple (damage, crit, multiplier)")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  3.2 Return Format Error: {e}")
        print("         Hint: Return `final_damage, is_critical, type_mult` from calculate_damage!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  3.2 Error in calculate_damage: {e}")

    # Test 3: Damage Formula Math
    try:
        # Attacker atk: 100, Defender def: 50. Move power: 40. Type: Normal (1.0x).
        # Base: (40 * 100) / 50 = 80. With normal/crit, damage should be around 80 or 120.
        p_strong = Pokemon("Mewtwo", "Psychic", 100, 100, 50, ["Swift"])
        p_target = Pokemon("Pidgey", "Flying", 100, 50, 50, ["Tackle"])
        dmg, crit, mult = calculate_damage("Swift", p_strong, p_target)
        assert dmg >= 50, f"Damage with strong stats was unexpectedly low ({dmg}). Check the damage formula!"
        print("  [PASS] ⭐ 3.3: calculate_damage scales correctly with Attack and Defense stats")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  3.3 Damage Formula Error: {e}")
        print("         Hint: Formula is `base_damage = (power * attacker.attack) / defender.defense`")
    except Exception as e:
        print(f"  [FAIL] ⚠️  3.3 Error in calculate_damage: {e}")

    # Test 4: Minimum 1 Damage Guarantee
    try:
        p_weak = Pokemon("Caterpie", "Bug", 10, 1, 10, ["Tackle"])
        p_tank = Pokemon("Steelix", "Steel", 100, 50, 999, ["Tackle"])
        dmg, crit, mult = calculate_damage("Tackle", p_weak, p_tank)
        assert dmg >= 1, f"Damage must always be at least 1, but got {dmg}"
        print("  [PASS] ⭐ 3.4: calculate_damage guarantees at least 1 damage even against high defense")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  3.4 Min Damage Error: {e}")
        print("         Hint: Use `final_damage = max(1, int(round(total_damage)))`")
    except Exception as e:
        print(f"  [FAIL] ⚠️  3.4 Error in calculate_damage: {e}")

    # Test 5: Enemy AI Move Choice
    try:
        enemy = Pokemon("Gengar", "Ghost", 50, 50, 50, ["Shadow Ball", "Scratch", "Quick Attack"])
        choices = set()
        for _ in range(25):
            chosen = choose_enemy_move(enemy)
            assert chosen in enemy.moves, f"choose_enemy_move returned '{chosen}' which is not in {enemy.moves}"
            choices.add(chosen)
        assert len(choices) > 1, "choose_enemy_move returned the exact same move every time! Use random.choice()."
        print("  [PASS] ⭐ 3.5: choose_enemy_move randomly selects valid moves from enemy moveset")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  3.5 Enemy Move Error: {e}")
        print("         Hint: Use `random.choice(enemy_pokemon.moves)` inside choose_enemy_move!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  3.5 Error in choose_enemy_move: {e}")

    # --- EDGE CASE TESTS ---

    # Test 6 (Edge Case): Division by Zero in Defense
    total += 1
    try:
        attacker = Pokemon("Pikachu", "Electric", 50, 50, 40, ["Thunderbolt"])
        zero_def_enemy = Pokemon("Glass", "Normal", 50, 10, 0, ["Tackle"]) # 0 defense!
        dmg, crit, mult = calculate_damage("Thunderbolt", attacker, zero_def_enemy)
        assert dmg > 0, "Damage should be a valid positive integer"
        print("  [PASS] ⭐ 3.6 [EDGE CASE]: calculate_damage survives 0 defense without ZeroDivisionError")
        passed += 1
    except ZeroDivisionError:
        print("  [FAIL] ⚠️  3.6 ZeroDivisionError! Defender defense was 0.")
        print("         Hint: Use `defense = max(1, defender.defense)` before dividing!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  3.6 Error: {e}")

    # Test 7 (Edge Case): Unknown Move Name or Lowercase Move
    total += 1
    try:
        p1 = Pokemon("Mewtwo", "Psychic", 80, 70, 60, ["Swift"])
        p2 = Pokemon("Pidgey", "Flying", 40, 30, 30, ["Tackle"])
        res_case = calculate_damage("swift", p1, p2) # lowercase
        res_unknown = calculate_damage("NonExistentMove999", p1, p2) # unknown move
        assert res_case is not None, "calculate_damage('swift', ...) returned None!"
        assert res_unknown is not None, "calculate_damage('NonExistentMove999', ...) returned None!"
        assert isinstance(res_case, tuple) and len(res_case) == 3, f"Expected 3-item tuple for 'swift', got {res_case}"
        assert isinstance(res_unknown, tuple) and len(res_unknown) == 3, f"Expected 3-item tuple for unknown move, got {res_unknown}"
        print("  [PASS] ⭐ 3.7 [EDGE CASE]: calculate_damage gracefully handles unknown and lowercase moves")
        passed += 1
    except KeyError as e:
        print(f"  [FAIL] ⚠️  3.7 KeyError on move name: {e}")
        print("         Hint: Use `MOVES.get(move_name, default_dict)` instead of `MOVES[move_name]`!")
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  3.7 Return Format Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  3.7 Error: {e}")

    # Test 8 (Edge Case): Unknown Types & Type Casing
    total += 1
    try:
        mult_unknown = get_type_multiplier("Dragon", "Steel")
        assert mult_unknown == 1.0, f"Unknown type matchup should default to 1.0, got {mult_unknown}"
        mult_case = get_type_multiplier("water", "FIRE")
        assert mult_case == 2.0, f"Type matching should handle lowercase/uppercase (water vs FIRE = 2.0), got {mult_case}"
        print("  [PASS] ⭐ 3.8 [EDGE CASE]: get_type_multiplier handles unknown types and case variations")
        passed += 1
    except KeyError as e:
        print(f"  [FAIL] ⚠️  3.8 KeyError on unknown type: {e}")
        print("         Hint: Check `if matchup in TYPE_CHART: return TYPE_CHART[matchup] else: return 1.0`")
    except Exception as e:
        print(f"  [FAIL] ⚠️  3.8 Error: {e}")

    # Test 9 (Edge Case): Enemy with Single Move or Empty Moves
    total += 1
    try:
        solo_enemy = Pokemon("Ditto", "Normal", 40, 40, 40, ["Transform"])
        move_solo = choose_enemy_move(solo_enemy)
        assert move_solo == "Transform", f"Expected 'Transform' for single move set, got '{move_solo}'"

        empty_enemy = Pokemon("Baby", "Normal", 10, 10, 10, [])
        fallback_move = choose_enemy_move(empty_enemy)
        assert fallback_move is not None, "choose_enemy_move on empty moveset returned None!"
        assert isinstance(fallback_move, str) and len(fallback_move) > 0, f"Expected non-empty string fallback move (e.g. 'Tackle'), got {fallback_move}"
        print("  [PASS] ⭐ 3.9 [EDGE CASE]: choose_enemy_move handles 1-move and empty move sets safely")
        passed += 1
    except IndexError as e:
        print(f"  [FAIL] ⚠️  3.9 IndexError choosing from empty moves list: {e}")
        print("         Hint: Check `if not enemy_pokemon.moves: return 'Tackle'` before random.choice!")
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  3.9 Enemy Move Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  3.9 Error: {e}")

    print(f"\nModule 3 Score: {passed}/{total} tests passed.\n")
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
