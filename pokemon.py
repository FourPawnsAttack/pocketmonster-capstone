"""
====================================================================
           POKÉMON MISSION 1: THE POKÉMON CLASS (OOP)
====================================================================
Create the Pokemon class to model Pokémon in our game.
====================================================================
"""

from poke_type import PokeType

class Pokemon:
    """
    Represents a Pokémon in the battle arena.
    """

    def __init__(self, name, poke_type, max_hp, attack, defense, moves, front_sprite="", back_sprite=""):
        """
        Initializes a new Pokemon object with its stats, moves, and sprites.
        The Pokemon starts with full HP (current hp equals max_hp).
        """
        pass

    def take_damage(self, amount):
        """
        Reduces the Pokemon's current HP by the given damage amount.
        Current HP should not drop below 0.
        Returns the updated current HP.
        """
        pass

    def heal(self, amount):
        """
        Restores HP to the Pokemon by the given amount.
        Current HP cannot exceed max_hp.
        Returns the updated current HP.
        """
        pass

    def is_fainted(self):
        """
        Checks whether the Pokemon has fainted.
        Returns True if current HP is 0 or less, otherwise returns False.
        """
        pass

    def to_dict(self):
        """
        Helper method: Turns this Pokémon object into a Python dictionary
        for the web browser. (Leave this method as-is!)
        """
        return {
            "name": getattr(self, "name", "Unknown"),
            "poke_type": str(getattr(self, "poke_type", "Normal")),
            "max_hp": getattr(self, "max_hp", 50),
            "hp": getattr(self, "hp", 50),
            "attack": getattr(self, "attack", 40),
            "defense": getattr(self, "defense", 40),
            "moves": getattr(self, "moves", ["Tackle"]),
            "front_sprite": getattr(self, "front_sprite", ""),
            "back_sprite": getattr(self, "back_sprite", ""),
            "is_fainted": self.is_fainted() if hasattr(self, "is_fainted") and self.is_fainted() is not None else False
        }
