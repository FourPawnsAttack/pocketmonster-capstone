"""
====================================================================
           POKÉMON MISSION 1: THE POKÉMON CLASS (OOP)
====================================================================
Create the Pokemon class to model Pokémon in our game.
====================================================================
"""

from poke_type import PokeType
from pokemon_data import EVOLUTION_DATA, LEARNABLE_MOVES

class Pokemon:
    """
    Represents a Pokémon in the battle arena.
    """

    def __init__(self, name, poke_type, max_hp, attack, defense, moves, front_sprite="", back_sprite="", level=5):
        """
        Initializes a new Pokemon object with its stats, moves, and sprites.
        The Pokemon starts with full HP (current hp equals max_hp), level (default 5), and exp (0).
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

    def gain_exp(self, amount):
        """
        Mission 5: Awards experience points (EXP) to this Pokémon!
        - If amount is 0 or negative, do nothing and return False.
        - Add amount to self.exp.
        - While self.exp >= 100:
            - Subtract 100 from self.exp.
            - Call self.level_up() to grow stronger!
            - Mark that the Pokémon leveled up.
        - Return True if the Pokémon leveled up at least once, otherwise False.
        """
        pass

    def level_up(self):
        """
        Mission 5: Level up stat growth!
        - Increase self.level by 1.
        - Stat boosts:
            - self.max_hp increases by 5.
            - self.attack increases by 3.
            - self.defense increases by 2.
            - Fully restore self.hp back to self.max_hp!
        - Move learning:
            - Check LEARNABLE_MOVES for self.name at self.level.
            - If a new move is found, call self.learn_move(new_move).
        - Evolution:
            - Call self.check_evolution() and save the result.
        - Return a dictionary with:
            {
                "level": self.level,
                "max_hp": self.max_hp,
                "attack": self.attack,
                "defense": self.defense,
                "evolution": evo_result
            }
        """
        pass

    def learn_move(self, new_move):
        """
        Mission 5: Learn a new attack move!
        - If new_move is already in self.moves, return False.
        - If self.moves has fewer than 4 moves:
            - Append new_move to self.moves.
        - Otherwise (already has 4 moves):
            - Remove the oldest move at index 0 (self.moves.pop(0)).
            - Append new_move to self.moves.
        - Return True.
        """
        pass

    def check_evolution(self):
        """
        Mission 5: Evolve into a stronger form!
        - Look up self.name in EVOLUTION_DATA.
        - If found and self.level >= data["evolves_at"]:
            - Save old_name = self.name.
            - Update self.name to data["evolves_into"].
            - Add bonus stats from data["stat_boost"] to max_hp, attack, and defense.
            - Fully restore self.hp to max_hp.
            - Update self.front_sprite and self.back_sprite from data.
            - If data has "new_move", call self.learn_move(data["new_move"]).
            - Return a dictionary with:
                {
                    "old_name": old_name,
                    "new_name": self.name,
                    "level": self.level,
                    "front_sprite": self.front_sprite,
                    "back_sprite": self.back_sprite
                }
        - If not ready to evolve, return None.
        """
        pass

    def to_dict(self):
        """
        Helper method: Turns this Pokémon object into a Python dictionary
        for the web browser. (Leave this method as-is!)
        """
        fainted = False
        try:
            if hasattr(self, "is_fainted"):
                val = self.is_fainted()
                if val is not None:
                    fainted = bool(val)
        except Exception:
            fainted = False

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
            "is_fainted": fainted,
            "level": getattr(self, "level", 5),
            "exp": getattr(self, "exp", 0),
            "max_exp": 100
        }

    def __str__(self):
        name = getattr(self, "name", "Unknown")
        poke_type = getattr(self, "poke_type", "Normal")
        hp = getattr(self, "hp", "?")
        max_hp = getattr(self, "max_hp", "?")
        return f"{name} ({poke_type}) [HP: {hp}/{max_hp}]"

    def __repr__(self):
        name = getattr(self, "name", "Unknown")
        poke_type = getattr(self, "poke_type", "Normal")
        hp = getattr(self, "hp", "?")
        max_hp = getattr(self, "max_hp", "?")
        return f"Pokemon(name='{name}', poke_type='{poke_type}', hp={hp}/{max_hp})"
