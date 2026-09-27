"""
TEST CASES: Progression System - Leveling Up, Move Learning & Evolution (pokemon.py)
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
    print("  TESTING MODULE 5: Level Up & Evolution System (pokemon.py)")
    print("=" * 60)

    passed = 0
    total = 8

    # Test 1: EXP Gain & Thresholds
    try:
        p = Pokemon("Pikachu", "Electric", 40, 50, 40, ["Quick Attack"], level=5)
        assert getattr(p, "level", 5) == 5, f"Expected start level 5, got {getattr(p, 'level', None)}"
        assert getattr(p, "exp", 0) == 0, f"Expected start exp 0, got {getattr(p, 'exp', None)}"
        
        leveled = p.gain_exp(50)
        assert leveled is False, "gain_exp(50) should NOT trigger a level up yet (threshold 100)"
        assert p.exp == 50, f"Expected 50 exp, got {p.exp}"

        leveled = p.gain_exp(60) # total 110 exp -> level up to 6, 10 exp remaining
        assert leveled is True, "gain_exp(60) should trigger a level up when reaching >= 100 EXP"
        assert p.level == 6, f"Expected level 6, got {p.level}"
        assert p.exp == 10, f"Expected 10 exp remaining, got {p.exp}"
        print("  [PASS] ⭐ 5.1: gain_exp() accumulates exp and triggers level_up() at 100 EXP")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  5.1 EXP Gain Error: {e}")
        print("         Hint: Did you subtract 100 from self.exp and call self.level_up()?")
    except Exception as e:
        print(f"  [FAIL] ⚠️  5.1 Error in gain_exp: {e}")

    # Test 2: Stat Growth on Level Up
    try:
        p = Pokemon("Squirtle", "Water", 44, 48, 65, ["Tackle"], level=5)
        p.hp = 10  # Damaged before level up
        gains = p.level_up()

        assert p.level == 6, f"Expected level 6, got {p.level}"
        assert p.max_hp == 49, f"Expected max_hp 49 (+5), got {p.max_hp}"
        assert p.attack == 51, f"Expected attack 51 (+3), got {p.attack}"
        assert p.defense == 67, f"Expected defense 67 (+2), got {p.defense}"
        assert p.hp == 49, f"Expected HP to be fully restored to max_hp (49), got {p.hp}"
        assert isinstance(gains, dict), "level_up() should return a dictionary of gains"
        assert gains.get("level") == 6, f"Gains dict should report level 6, got {gains.get('level')}"
        print("  [PASS] ⭐ 5.2: level_up() boosts max_hp (+5), attack (+3), defense (+2), and restores HP")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  5.2 Stat Growth Error: {e}")
        print("         Hint: Increase level by 1, max_hp by 5, attack by 3, defense by 2, and set hp = max_hp.")
    except Exception as e:
        print(f"  [FAIL] ⚠️  5.2 Error in level_up: {e}")

    # Test 3: Learn Move (Capacity & FIFO Replacement)
    try:
        p = Pokemon("Bulbasaur", "Grass", 45, 49, 49, ["Tackle", "Growl"], level=5)
        res = p.learn_move("Vine Whip")
        assert res is True, "learn_move should return True when learning a new move"
        assert "Vine Whip" in p.moves, "moves should contain 'Vine Whip'"
        assert len(p.moves) == 3, f"Expected 3 moves, got {len(p.moves)}"

        # Attempt duplicate
        dup = p.learn_move("Tackle")
        assert dup is False, "learn_move should return False if move is already known"
        assert len(p.moves) == 3, "Moveset should not duplicate existing moves"

        # Add 4th move
        p.learn_move("Leech Seed")
        assert len(p.moves) == 4, f"Expected 4 moves, got {len(p.moves)}"
        assert p.moves == ["Tackle", "Growl", "Vine Whip", "Leech Seed"]

        # Add 5th move: Should drop oldest move ("Tackle") and append "Solar Beam"
        p.learn_move("Solar Beam")
        assert len(p.moves) == 4, f"Moveset must stay capped at 4 moves, got {len(p.moves)}"
        assert p.moves[0] == "Growl", f"Expected 'Growl' at index 0 after dropping oldest, got {p.moves[0]}"
        assert p.moves[-1] == "Solar Beam", f"Expected 'Solar Beam' at end of moveset, got {p.moves[-1]}"
        assert "Tackle" not in p.moves, "'Tackle' should have been replaced!"
        print("  [PASS] ⭐ 5.3: learn_move() enforces 4-move maximum with oldest-move replacement")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  5.3 Move Learning Error: {e}")
        print("         Hint: If len(self.moves) == 4, use self.moves.pop(0) before appending the new move.")
    except Exception as e:
        print(f"  [FAIL] ⚠️  5.3 Error in learn_move: {e}")

    # Test 4: Milestone Move Learning upon Level Up
    try:
        p = Pokemon("Pikachu", "Electric", 35, 55, 40, ["Quick Attack", "Thunder Shock"], level=7)
        p.level_up()  # Level 8 milestone for Pikachu -> learns "Thunder"
        assert p.level == 8, f"Expected level 8, got {p.level}"
        assert "Thunder" in p.moves, f"Pikachu should learn 'Thunder' at level 8! Moves: {p.moves}"
        print("  [PASS] ⭐ 5.4: Milestone moves automatically learned upon reaching target level")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  5.4 Milestone Move Error: {e}")
        print("         Hint: In level_up(), check LEARNABLE_MOVES for moves unlocking at self.level.")
    except Exception as e:
        print(f"  [FAIL] ⚠️  5.4 Error in milestone moves: {e}")

    # Test 5: Evolution Trigger & Transformations
    try:
        p = Pokemon("Charmander", "Fire", 39, 52, 43, ["Scratch", "Ember"], level=6)
        evo_before = p.check_evolution()
        assert evo_before is None, "Charmander should NOT evolve at level 6 (threshold is 7)"

        # Level up to 7
        p.level_up()
        assert p.level == 7, f"Expected level 7, got {p.level}"
        assert p.name == "Charmeleon", f"Expected name 'Charmeleon', got '{p.name}'"
        assert "charmeleon" in p.front_sprite.lower(), f"Expected Charmeleon front sprite, got {p.front_sprite}"
        assert "charmeleon" in p.back_sprite.lower(), f"Expected Charmeleon back sprite, got {p.back_sprite}"
        # Stat boost verification: 39 base + 5 (lvl up) + 15 (evo boost) = 59 max_hp
        assert p.max_hp == 59, f"Expected 59 max_hp after evolution boost, got {p.max_hp}"
        print("  [PASS] ⭐ 5.5: check_evolution() evolves Pokémon at threshold with stat boosts & sprites")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  5.5 Evolution Error: {e}")
        print("         Hint: In check_evolution(), update name, sprites, and add stat_boost bonuses.")
    except Exception as e:
        print(f"  [FAIL] ⚠️  5.5 Error in check_evolution: {e}")

    # Test 6: Multi-Stage Evolution (Charmander -> Charmeleon -> Charizard)
    try:
        p = Pokemon("Charmander", "Fire", 39, 52, 43, ["Scratch", "Ember"], level=5)
        # Advance to level 7
        p.gain_exp(200)
        assert p.name == "Charmeleon", f"Should be Charmeleon at level 7, got {p.name}"

        # Advance to level 10 (stage 2 evolution)
        p.gain_exp(300)
        assert p.level == 10, f"Expected level 10, got {p.level}"
        assert p.name == "Charizard", f"Should be Charizard at level 10, got {p.name}"
        assert "Fire Blast" in p.moves, f"Charizard should have learned 'Fire Blast'! Moves: {p.moves}"
        print("  [PASS] ⭐ 5.6: Multi-stage evolution works smoothly across progressive levels")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  5.6 Multi-stage Evolution Error: {e}")
    except Exception as e:
        print(f"  [FAIL] ⚠️  5.6 Error in multi-stage evolution: {e}")

    # --- EDGE CASES ---

    # Test 7 (Edge Case): Zero, Negative, or Multi-Level EXP Drops
    try:
        p = Pokemon("Bulbasaur", "Grass", 45, 49, 49, ["Tackle"], level=5)
        res = p.gain_exp(0)
        assert res is False and p.exp == 0, "gain_exp(0) should be ignored"
        res = p.gain_exp(-50)
        assert res is False and p.exp == 0, "gain_exp(-50) should be ignored"

        # Massive EXP drop: +250 EXP = +2 levels (to lvl 7), with 50 EXP leftover
        leveled = p.gain_exp(250)
        assert leveled is True, "gain_exp(250) should level up multiple times"
        assert p.level == 7, f"Expected level 7 after +250 EXP, got {p.level}"
        assert p.exp == 50, f"Expected 50 exp leftover, got {p.exp}"
        print("  [PASS] ⭐ 5.7 [EDGE CASE]: gain_exp safely handles non-positive amounts and multi-level gains")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  5.7 EXP Edge Case Error: {e}")
        print("         Hint: Guard `if amount <= 0: return False` and use `while self.exp >= 100:`")
    except Exception as e:
        print(f"  [FAIL] ⚠️  5.7 Error: {e}")

    # Test 8 (Edge Case): Evolution Immunity for Fully Evolved or Unknown Pokémon
    try:
        p = Pokemon("Mewtwo", "Psychic", 106, 110, 90, ["Psychic", "Swift"], level=50)
        evo = p.check_evolution()
        assert evo is None, "Mewtwo does not evolve; check_evolution should return None"

        charizard = Pokemon("Charizard", "Fire", 100, 100, 100, ["Flamethrower"], level=100)
        evo2 = charizard.check_evolution()
        assert evo2 is None, "Fully evolved Charizard should return None from check_evolution"
        print("  [PASS] ⭐ 5.8 [EDGE CASE]: check_evolution returns None safely for fully evolved Pokémon")
        passed += 1
    except AssertionError as e:
        print(f"  [FAIL] ⚠️  5.8 Evolution Guard Error: {e}")
        print("         Hint: Return None if self.name is not found in EVOLUTION_DATA.")
    except Exception as e:
        print(f"  [FAIL] ⚠️  5.8 Error: {e}")

    print(f"\nModule 5 Score: {passed}/{total} tests passed.\n")
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
