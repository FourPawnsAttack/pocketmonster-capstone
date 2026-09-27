"""
TEST CASES: Gym Progression System (gym.py)
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pokemon_data import GYMS
from gym import get_all_gyms, get_gym, is_gym_unlocked, can_catch_pokemon, award_gym_rewards, create_gym_pokemon

try:
    if os.environ.get("USE_SOLUTIONS") == "1":
        from solutions.pokemon import Pokemon
    else:
        from pokemon import Pokemon
        test_p = Pokemon("Test", "Normal", 10, 10, 10, ["Tackle"])
        if not hasattr(test_p, "name") or not hasattr(test_p, "max_hp"):
            from solutions.pokemon import Pokemon
except Exception:
    from solutions.pokemon import Pokemon

def run_tests():
    print("=" * 60)
    print("  TESTING MODULE: Gym Progression System (gym.py)")
    print("=" * 60)

    passed = 0
    total = 7

    # Test 1: Gym Registry contains all 5 Kanto Gyms
    try:
        all_gyms = get_all_gyms()
        assert len(all_gyms) >= 5, f"Expected at least 5 gyms, got {len(all_gyms)}"
        gym_ids = [g["id"] for g in all_gyms]
        assert "pewter" in gym_ids, "Pewter Gym missing!"
        assert "cerulean" in gym_ids, "Cerulean Gym missing!"
        assert "vermilion" in gym_ids, "Vermilion Gym missing!"
        assert "celadon" in gym_ids, "Celadon Gym missing!"
        assert "viridian" in gym_ids, "Viridian Gym missing!"
        print("  [PASS] ⭐ 6.1: Gym registry includes all 5 major Kanto Gyms")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  6.1 Registry Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  6.1 Error: {e}")

    # Test 2: get_gym lookups (case-insensitive and whitespace-safe)
    try:
        g1 = get_gym("pewter")
        assert g1 is not None and g1["leader"] == "Brock", f"Expected Brock, got {g1}"
        assert g1["badge_name"] == "Boulder Badge"

        # Case and whitespace tolerance
        g2 = get_gym("  CeRuLeAn  ")
        assert g2 is not None and g2["leader"] == "Misty", f"Expected Misty, got {g2}"

        # Unknown gym fallback
        assert get_gym("pallet_town_gym") is None
        assert get_gym("") is None
        print("  [PASS] ⭐ 6.2: get_gym() accurately looks up Gyms with case and whitespace tolerance")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  6.2 Lookup Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  6.2 Error: {e}")

    # Test 3: Sequential Gym Unlock Progression
    try:
        # Player has 0 badges
        assert is_gym_unlocked("pewter", []) is True, "First gym (Pewter) should be unlocked by default"
        assert is_gym_unlocked("cerulean", []) is False, "Cerulean Gym should be locked with 0 badges"
        assert is_gym_unlocked("viridian", []) is False, "Viridian Gym should be locked with 0 badges"

        # Player earns Boulder Badge
        badges = ["boulder"]
        assert is_gym_unlocked("cerulean", badges) is True, "Cerulean Gym should unlock with Boulder Badge"
        assert is_gym_unlocked("vermilion", badges) is False, "Vermilion Gym should still be locked"

        # Player earns Cascade Badge
        badges.append("cascade")
        assert is_gym_unlocked("vermilion", badges) is True, "Vermilion Gym should unlock with Cascade Badge"
        assert is_gym_unlocked("viridian", badges) is False, "Viridian Gym should still be locked"
        print("  [PASS] ⭐ 6.3: Gyms unlock sequentially as preceding badges are earned")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  6.3 Unlock Progression Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  6.3 Error: {e}")

    # Test 4: League Rules - Catch Restriction
    try:
        assert can_catch_pokemon(is_gym_battle=False) is True, "Wild Pokémon should be catchable"
        assert can_catch_pokemon(is_gym_battle=True) is False, "Gym Leader Pokémon must NOT be catchable!"
        print("  [PASS] ⭐ 6.4: League rules enforce no-catching in Gym battles")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  6.4 Catch Restriction Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  6.4 Error: {e}")

    # Test 5: create_gym_pokemon Factory
    try:
        brock = get_gym("pewter")
        onix_data = brock["team"][1]
        onix = create_gym_pokemon(Pokemon, onix_data)
        assert onix.name == "Onix", f"Expected Onix, got {onix.name}"
        assert getattr(onix, "max_hp", 0) == onix_data["max_hp"]
        assert getattr(onix, "hp", 0) == onix_data["max_hp"]
        assert getattr(onix, "level", 1) == onix_data["level"]
        assert "Rock Slide" in onix.moves
        print("  [PASS] ⭐ 6.5: create_gym_pokemon instantiates Gym Leader Pokémon with correct stats & moves")
        passed += 1
    except AttributeError as e:
        print(f"  [FAIL] ⚠️  6.5 Pokemon Attribute Error: {e}")
        print("         Hint: Finish Mission 1 in pokemon.py (__init__) so Pokemon attributes are set!")
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  6.5 Factory Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  6.5 Error: {e}")

    # Test 6: award_gym_rewards
    try:
        state = {"badges": [], "potions": 3}
        rewards = award_gym_rewards("pewter", state)
        assert rewards is not None, "award_gym_rewards returned None!"
        assert "boulder" in state["badges"], "Boulder badge not added to badges!"
        assert state["potions"] == 5, f"Expected 5 potions (3+2), got {state['potions']}"
        assert rewards["exp"] == 150, f"Expected 150 EXP, got {rewards['exp']}"
        assert rewards["is_first_time"] is True

        # Rematch should not duplicate badge
        rematch_rewards = award_gym_rewards("pewter", state)
        assert state["badges"].count("boulder") == 1, "Duplicate badge was awarded on rematch!"
        assert rematch_rewards["is_first_time"] is False
        print("  [PASS] ⭐ 6.6: award_gym_rewards awards badges, items, exp without duplicate badges")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  6.6 Reward Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  6.6 Error: {e}")

    # Test 7: Gym Leader Teams & Type Theming
    try:
        pewter = get_gym("pewter")
        assert pewter["type"] == "Rock"
        assert len(pewter["team"]) == 2

        cerulean = get_gym("cerulean")
        assert cerulean["type"] == "Water"
        assert cerulean["leader"] == "Misty"

        viridian = get_gym("viridian")
        assert viridian["leader"] == "Giovanni"
        assert any(m["name"] == "Mewtwo" for m in viridian["team"]), "Viridian Gym should feature Mewtwo!"
        print("  [PASS] ⭐ 6.7: All Gyms have themed leader teams, dialog, and battle parameters")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  6.7 Leader Team Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  6.7 Error: {e}")

    print(f"\nGym Module Score: {passed}/{total} tests passed.\n")
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
