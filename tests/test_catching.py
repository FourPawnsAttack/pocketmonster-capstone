"""
TEST CASES: Safari Catching Engine (catching.py)
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if os.environ.get("USE_SOLUTIONS") == "1":
    from solutions.catching import attempt_catch
    from solutions.pokemon import Pokemon
else:
    from catching import attempt_catch
    from pokemon import Pokemon

def run_tests():
    print("=" * 60)
    print("  TESTING MODULE 4: Safari Catching (catching.py)")
    print("=" * 60)
    
    passed = 0
    total = 4

    # Test 1: Return Type Format
    try:
        p = Pokemon("Pidgey", "Flying", 50, 30, 30, ["Tackle"])
        p.hp = 25
        result = attempt_catch(p, "poke-ball")
        assert result is not None, "attempt_catch returned None! Did you forget `return caught, shakes`?"
        assert isinstance(result, tuple) and len(result) == 2, f"Expected a tuple of (caught, shakes), got {result}"
        caught, shakes = result
        assert isinstance(caught, bool), f"caught should be a boolean (True/False), got {type(caught)}"
        assert isinstance(shakes, int), f"shakes should be an integer, got {type(shakes)}"
        assert 0 <= shakes <= 3, f"shakes must be between 0 and 3, got {shakes}"
        print("  [PASS] ⭐ 4.1: attempt_catch returns correct tuple format (caught, shakes)")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  4.1 Return Format Error: {e}")
        print("         Hint: Return `(caught_boolean, number_of_shakes)` from attempt_catch!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  4.1 Error in attempt_catch: {e}")

    # Test 2: Successful catch always gives 3 shakes
    try:
        # Run multiple times to find a catch
        saw_catch = False
        p = Pokemon("Pidgey", "Flying", 50, 30, 30, ["Tackle"])
        p.hp = 1  # 1 HP = very easy to catch
        for _ in range(30):
            caught, shakes = attempt_catch(p, "ultra-ball")
            if caught:
                saw_catch = True
                assert shakes == 3, f"A successful catch must have 3 shakes, but got {shakes}!"
                break
        assert saw_catch, "No catches occurred even with 1 HP and Ultra Ball. Check your catch rate formula!"
        print("  [PASS] ⭐ 4.2: Successful catch correctly features 3 full ball shakes")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  4.2 Shake Count Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  4.2 Error: {e}")

    # Test 3: Lower HP yields higher catch rate
    try:
        p_full = Pokemon("Geodude", "Rock", 100, 30, 30, ["Tackle"])
        p_full.hp = 100

        p_low = Pokemon("Geodude", "Rock", 100, 30, 30, ["Tackle"])
        p_low.hp = 5

        catches_full = sum(1 for _ in range(100) if attempt_catch(p_full, "poke-ball")[0])
        catches_low = sum(1 for _ in range(100) if attempt_catch(p_low, "poke-ball")[0])

        assert catches_low > catches_full, f"Low HP Pokemon was caught {catches_low} times vs {catches_full} for full HP. Weakening a Pokemon should make it easier to catch!"
        print(f"  [PASS] ⭐ 4.3: Weakened Pokémon is easier to catch ({catches_low}% vs {catches_full}% at full HP)")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  4.3 HP Scaling Error: {e}")
        print("         Hint: Use missing HP percentage: `missing_hp_pct = (max_hp - hp) / max_hp`")
    except Exception as e:
        print(f"  [FAIL] ⚠️  4.3 Error: {e}")

    # Test 4: Ultra Ball is more effective than Pokéball
    try:
        p = Pokemon("Pidgey", "Flying", 50, 30, 30, ["Tackle"])
        p.hp = 25
        catches_poke = sum(1 for _ in range(100) if attempt_catch(p, "poke-ball")[0])
        catches_ultra = sum(1 for _ in range(100) if attempt_catch(p, "ultra-ball")[0])

        assert catches_ultra >= catches_poke, f"Ultra Ball caught {catches_ultra} times vs Pokéball {catches_poke}. Ultra Ball should be more effective!"
        print(f"  [PASS] ⭐ 4.4: Ultra Ball provides higher catch rate ({catches_ultra}% vs {catches_poke}%)")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  4.4 Ball Multiplier Error: {e}")
        print("         Hint: Multiply base chance by `BALL_MODIFIERS[ball_type]`")
    except Exception as e:
        print(f"  [FAIL] ⚠️  4.4 Error: {e}")

    # --- EDGE CASE TESTS ---

    # Test 5 (Edge Case): Catching at 0 HP (Fainted)
    total += 1
    try:
        p_fainted = Pokemon("Caterpie", "Bug", 30, 10, 10, ["Tackle"])
        p_fainted.hp = 0
        caught, shakes = attempt_catch(p_fainted, "poke-ball")
        assert isinstance(caught, bool) and isinstance(shakes, int)
        assert 0 <= shakes <= 3
        print("  [PASS] ⭐ 4.5 [EDGE CASE]: attempt_catch safely processes 0 HP targets")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] ⚠️  4.5 0 HP Catch Error: {e}")

    # Test 6 (Edge Case): Overhealed / Negative Missing HP (hp > max_hp)
    total += 1
    try:
        p_over = Pokemon("Chansey", "Normal", 100, 10, 10, ["Tackle"])
        p_over.hp = 150 # Bugged/overhealed
        caught, shakes = attempt_catch(p_over, "poke-ball")
        assert isinstance(caught, bool) and 0 <= shakes <= 3
        print("  [PASS] ⭐ 4.6 [EDGE CASE]: attempt_catch handles overhealed HP without negative probabilities")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] ⚠️  4.6 Overhealed HP Error: {e}")

    # Test 7 (Edge Case): Unknown or Custom Ball Name
    total += 1
    try:
        p = Pokemon("Pikachu", "Electric", 50, 40, 40, ["Spark"])
        p.hp = 25
        result_custom = attempt_catch(p, "luxury-ball")
        result_blank = attempt_catch(p, "")
        assert result_custom is not None and result_blank is not None
        print("  [PASS] ⭐ 4.7 [EDGE CASE]: attempt_catch falls back safely on unknown ball types")
        passed += 1
    except KeyError as e:
        print(f"  [FAIL] ⚠️  4.7 KeyError on unknown ball: {e}")
        print("         Hint: Use `BALL_MODIFIERS.get(ball_type, 1.0)` instead of direct dictionary indexing!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  4.7 Error: {e}")

    # Test 8 (Edge Case): Zero Max HP Division by Zero Safeguard
    total += 1
    try:
        p_zero_max = Pokemon("Ghost", "Ghost", 0, 10, 10, ["Tackle"])
        p_zero_max.max_hp = 0
        caught, shakes = attempt_catch(p_zero_max, "poke-ball")
        assert isinstance(caught, bool) and 0 <= shakes <= 3
        print("  [PASS] ⭐ 4.8 [EDGE CASE]: attempt_catch prevents ZeroDivisionError when max_hp is 0")
        passed += 1
    except ZeroDivisionError:
        print("  [FAIL] ⚠️  4.8 ZeroDivisionError when max_hp is 0!")
        print("         Hint: Guard with `max_hp = max(1, getattr(wild_pokemon, 'max_hp', 50))`")
    except Exception as e:
        print(f"  [FAIL] ⚠️  4.8 Error: {e}")

    print(f"\nModule 4 Score: {passed}/{total} tests passed.\n")
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
