"""
====================================================================
           POKÉMON MISSION 2: PROFESSOR OAK'S STARTER LAB
====================================================================
Implement starter selection for new Pokémon trainers visiting the lab.
====================================================================
"""

from pokemon import Pokemon
from pokemon_data import STARTER_TEMPLATES

def create_starter(choice):
    """
    Creates and returns a Pokemon instance based on the player's starter choice.
    Data should be loaded from the STARTER_TEMPLATES dictionary.
    Handles case-insensitivity and unexpected inputs by defaulting to "pikachu".
    """
    pass


def get_available_starters():
    """
    Returns a list of all available starter Pokémon identifiers.
    """
    return list(STARTER_TEMPLATES.keys())
