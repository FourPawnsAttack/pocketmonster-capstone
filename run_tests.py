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

    print("=" * 65)
    print("                    MISSION SUMMARY REPORT")
    print("=" * 65)
    
    all_passed = True
    passed_count = sum(1 for res in results.values() if res)

    for mission, passed in results.items():
        if passed:
            print(f"  [COMPLETED] ⭐ {mission}")
        else:
            print(f"  [IN PROGRESS] ⏳ {mission}")
            all_passed = False

    print("-" * 65)
    if all_passed:
        print(f"  🏆 CONGRATULATIONS! ALL {passed_count}/4 MISSIONS COMPLETED!")
        print("  Your Pokémon Battle Game is fully powered and ready to play!")
    else:
        print(f"  Keep going! {passed_count}/4 missions completed.")
        print("  Check the hints above to solve the remaining missions!")
    print("=" * 65 + "\n")

    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
