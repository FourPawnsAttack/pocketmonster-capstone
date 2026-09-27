#!/usr/bin/env python3
"""
====================================================================
           POKÉMON CODE MASTER TEST RUNNER
====================================================================
Runs tests across all 4 student missions:
  1. pokemon.py   (Pokemon Class & OOP)
  2. starters.py  (Starter Lab & Conditionals)
  3. battle.py    (Damage Formula & Enemy AI)
  4. catching.py  (Pokéball Catching Probability)

Usage:
  python run_tests.py             # Test student code
  python run_tests.py --solutions # Test teacher reference solutions
====================================================================
"""

import sys
import os

def main():
    if "--solutions" in sys.argv:
        solutions_file = os.path.join(os.path.dirname(__file__), "solutions", "pokemon.py")
        if not os.path.isfile(solutions_file):
            print("\n" + "=" * 65)
            print("  ⚠️  TEACHER REFERENCE SOLUTIONS NOT FOUND")
            print("=" * 65)
            print("  The 'solutions/' directory is not included in this repository.")
            print("  Run tests against the student code workspace instead:\n")
            print("    python3 run_tests.py\n")
            print("=" * 65 + "\n")
            sys.exit(1)

        os.environ["USE_SOLUTIONS"] = "1"
        target_name = "TEACHER REFERENCE SOLUTIONS"
    else:
        os.environ["USE_SOLUTIONS"] = "0"
        target_name = "STUDENT CODE WORKSPACE"

    print("\n" + "=" * 65)
    print(f"       POKÉMON CODE TEST SUITE: {target_name}")
    print("=" * 65 + "\n")

    # Import test runners
    from tests.test_pokemon import run_tests as test_m1
    from tests.test_starters import run_tests as test_m2
    from tests.test_battle import run_tests as test_m3
    from tests.test_catching import run_tests as test_m4

    results = {
        "Mission 1: Pokemon Class": test_m1(),
        "Mission 2: Starter Lab": test_m2(),
        "Mission 3: Battle Engine": test_m3(),
        "Mission 4: Safari Catching": test_m4(),
    }

    run_bonus = "--bonus" in sys.argv or "--all" in sys.argv
    if run_bonus:
        from tests.test_poke_type import run_tests as test_bonus
        results["Bonus: Elemental Type System"] = test_bonus()

    run_progression = "--progression" in sys.argv or "--all" in sys.argv
    if run_progression:
        from tests.test_progression import run_tests as test_m5
        results["Mission 5: Level Up & Evolution"] = test_m5()

    if "--gym" in sys.argv:
        from tests.test_gym import run_tests as test_gym
        test_gym()

    run_team = "--team" in sys.argv or "--all" in sys.argv
    if run_team:
        from tests.test_team import run_tests as test_m7
        results["Mission 7: 4-Pokémon Party & Team System"] = test_m7()

    print("=" * 65)
    print("                    MISSION SUMMARY REPORT")
    print("=" * 65)
    
    all_passed = True
    passed_count = sum(1 for res in results.values() if res)
    total_missions = len(results)

    for mission, passed in results.items():
        if passed:
            print(f"  [COMPLETED] ⭐ {mission}")
        else:
            print(f"  [IN PROGRESS] ⏳ {mission}")
            all_passed = False

    print("-" * 65)
    if all_passed:
        print(f"  🏆 CONGRATULATIONS! ALL {passed_count}/{total_missions} MISSIONS COMPLETED!")
        print("  Your Pokémon Battle Game is fully powered and ready to play!")
        if not run_bonus:
            print("  💡 Tip: Try the bonus elemental type challenge: python3 run_tests.py --bonus")
        if not run_progression:
            print("  💡 Tip: Test the evolution & level up system: python3 run_tests.py --progression")
    else:
        print(f"  Keep going! {passed_count}/{total_missions} missions completed.")
        print("  Check the hints above to solve the remaining missions!")
    print("=" * 65 + "\n")

    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
