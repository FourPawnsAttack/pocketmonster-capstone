"""
TEST CASES: Starters Module (starters.py)
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if os.environ.get("USE_SOLUTIONS") == "1":
    from solutions.starters import create_starter, get_available_starters
else:
    from starters import create_starter, get_available_starters

def run_tests():
    print("=" * 60)
    print("  TESTING MODULE 2: Starter Lab (starters.py)")
    print("=" * 60)
    
    passed = 0
    total = 5

    # Test 1: Charmander
    try:
        char = create_starter("charmander")
        assert char is not None, "create_starter('charmander') returned None!"
        assert char.name == "Charmander", f"Expected name 'Charmander', got {char.name}"
        assert char.poke_type == "Fire", f"Expected type 'Fire', got {char.poke_type}"
        assert len(char.moves) >= 2, "Expected at least 2 moves for Charmander"
        print("  [PASS] ⭐ 2.1: create_starter('charmander') creates Fire-type Charmander")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  2.1 Charmander Error: {e}")
        print("         Hint: Did you instantiate Pokemon using STARTER_TEMPLATES['charmander']?")
    except Exception as e:
        print(f"  [FAIL] ⚠️  2.1 Error in create_starter: {e}")

    # Test 2: Squirtle
    try:
        squirtle = create_starter("squirtle")
        assert squirtle is not None, "create_starter('squirtle') returned None!"
        assert squirtle.name == "Squirtle", f"Expected name 'Squirtle', got {squirtle.name}"
        assert squirtle.poke_type == "Water", f"Expected type 'Water', got {squirtle.poke_type}"
        print("  [PASS] ⭐ 2.2: create_starter('squirtle') creates Water-type Squirtle")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  2.2 Squirtle Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  2.2 Error in create_starter: {e}")

    # Test 3: Bulbasaur
    try:
        bulba = create_starter("bulbasaur")
        assert bulba is not None, "create_starter('bulbasaur') returned None!"
        assert bulba.name == "Bulbasaur", f"Expected name 'Bulbasaur', got {bulba.name}"
        assert bulba.poke_type == "Grass", f"Expected type 'Grass', got {bulba.poke_type}"
        print("  [PASS] ⭐ 2.3: create_starter('bulbasaur') creates Grass-type Bulbasaur")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  2.3 Bulbasaur Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  2.3 Error in create_starter: {e}")

    # Test 4: Pikachu & Case Insensitivity
    try:
        pika = create_starter("PIKACHU")
        assert pika is not None, "create_starter('PIKACHU') returned None!"
        assert pika.name == "Pikachu", f"Expected name 'Pikachu', got {pika.name}"
        assert pika.poke_type == "Electric", f"Expected type 'Electric', got {pika.poke_type}"
        print("  [PASS] ⭐ 2.4: create_starter handles uppercase strings like 'PIKACHU'")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  2.4 Uppercase Error: {e}")
        print("         Hint: Use `choice.lower()` to ignore uppercase letters!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  2.4 Error: {e}")

    # Test 5: Fallback for Unknown Choice
    try:
        unknown = create_starter("missingno")
        assert unknown is not None, "create_starter should return a fallback Pokemon instead of None!"
        print("  [PASS] ⭐ 2.5: create_starter provides a fallback for unknown Pokémon")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  2.5 Fallback Error: {e}")
        print("         Hint: If `choice` is not in STARTER_TEMPLATES, default to 'pikachu'!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  2.5 Error: {e}")

    # --- EDGE CASE TESTS ---

    # Test 6 (Edge Case): Leading and Trailing Whitespace
    total += 1
    try:
        space_mon = create_starter("   charmander   \n\t")
        assert space_mon is not None and space_mon.name == "Charmander", f"Expected Charmander, got {getattr(space_mon, 'name', None)}"
        print("  [PASS] ⭐ 2.6 [EDGE CASE]: create_starter handles leading/trailing whitespace cleanly")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  2.6 Whitespace Error: {e}")
        print("         Hint: Use `choice.strip()` to remove accidental spaces!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  2.6 Error: {e}")

    # Test 7 (Edge Case): Crazy Mixed Casing
    total += 1
    try:
        mixed_mon = create_starter("sQuIrTlE")
        assert mixed_mon is not None and mixed_mon.name == "Squirtle", f"Expected Squirtle, got {getattr(mixed_mon, 'name', None)}"
        print("  [PASS] ⭐ 2.7 [EDGE CASE]: create_starter handles mixed casing like 'sQuIrTlE'")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  2.7 Mixed Casing Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  2.7 Error: {e}")

    # Test 8 (Edge Case): Non-String and Empty Inputs
    total += 1
    try:
        empty_mon = create_starter("")
        none_mon = create_starter(None)
        int_mon = create_starter(999)
        assert empty_mon is not None and empty_mon.name == "Pikachu", "Empty string should fallback to Pikachu safely"
        assert none_mon is not None and none_mon.name == "Pikachu", "None input should fallback to Pikachu safely without crashing"
        assert int_mon is not None and int_mon.name == "Pikachu", "Integer input should fallback to Pikachu safely"
        print("  [PASS] ⭐ 2.8 [EDGE CASE]: create_starter safely handles None, empty strings, and non-strings")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  2.8 Non-string Input Error: {e}")
        print("         Hint: Check `if not choice or not isinstance(choice, str): choice = 'pikachu'`")
    except Exception as e:
        print(f"  [FAIL] ⚠️  2.8 Crash Error on invalid input: {e}")

    # Test 9 (Edge Case): Independent Instances & Mutable List Protection
    total += 1
    try:
        char1 = create_starter("charmander")
        char2 = create_starter("charmander")
        char1.take_damage(20)
        assert char2.hp == char2.max_hp, f"Mutating char1 changed char2 HP! They must be independent objects."

        char1.moves.append("SECRET_SPECIAL_MOVE")
        assert "SECRET_SPECIAL_MOVE" not in char2.moves, "Mutating char1's moves mutated char2's moves! Use list(data['moves']) to make a copy."
        print("  [PASS] ⭐ 2.9 [EDGE CASE]: Each starter is a truly independent object (no shared list bugs)")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  2.9 Shared Object Error: {e}")
        print("         Hint: Use `moves=list(data['moves'])` to prevent sharing the same moves list!")
    except Exception as e:
        print(f"  [FAIL] ⚠️  2.9 Error: {e}")

    print(f"\nModule 2 Score: {passed}/{total} tests passed.\n")
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
