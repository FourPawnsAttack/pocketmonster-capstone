"""
====================================================================
           POKÉMON MISSION 4: THE SAFARI CATCHING ENGINE
====================================================================
Implement Pokéball catch rate calculation and shake mechanics.
====================================================================
"""

import random

# Ball power multipliers:
BALL_MODIFIERS = {
    "poke-ball": 1.0,
    "great-ball": 1.5,
    "ultra-ball": 2.0
}

def attempt_catch(wild_pokemon, ball_type="poke-ball"):
    """
    Determines whether a wild Pokémon is caught when a Pokéball is thrown.
    Catch rate scales with how much HP the wild Pokémon is missing and the ball multiplier.
    Returns a tuple of: (caught: bool, shakes: int)
    where shakes is an integer between 0 and 3. A successful catch always has 3 shakes.
    """
    pass
