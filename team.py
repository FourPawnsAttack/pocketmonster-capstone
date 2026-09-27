"""
====================================================================
           POKÉMON TEAM & PARTY SYSTEM (team.py)
====================================================================
Manages the player's 4-Pokémon battle party, reserves in PC storage,
in-battle Pokémon switching, and Pokémon Center full-team healing!
====================================================================
"""

from pokemon_data import STARTER_TEMPLATES, WILD_TEMPLATES

# Maximum number of Pokémon a trainer can carry in their active battle team
MAX_PARTY_SIZE = 4

def can_add_to_party(party, max_size=MAX_PARTY_SIZE):
    """
    Checks whether there is an open slot in the trainer's battle party.
    Returns True if party has fewer than max_size Pokémon, otherwise False.
    """
    if not isinstance(party, list):
        return False
    return len(party) < max_size

def add_to_party(party, pokemon, max_size=MAX_PARTY_SIZE):
    """
    Adds a Pokémon to the trainer's party if space is available.
    - If pokemon is None, returns False.
    - If party already has max_size Pokémon (default 4), returns False.
    - Otherwise, appends the pokemon to party and returns True.
    """
    if pokemon is None or not isinstance(party, list):
        return False
    if len(party) >= max_size:
        return False
    party.append(pokemon)
    return True

def remove_from_party(party, index):
    """
    Removes a Pokémon from the party at the given index.
    A trainer must always keep at least 1 Pokémon in their party!
    Returns the removed Pokémon if successful, or None if invalid.
    """
    if not isinstance(party, list) or len(party) <= 1:
        return None
    if index < 0 or index >= len(party):
        return None
    return party.pop(index)

def get_active_pokemon(party, active_index=0):
    """
    Safely retrieves the active battle Pokémon from the party.
    Defaults to the first Pokémon (slot 0) if active_index is out of range.
    """
    if not isinstance(party, list) or len(party) == 0:
        return None
    if 0 <= active_index < len(party):
        return party[active_index]
    return party[0]

def is_pokemon_conscious(pokemon):
    """
    Helper function to check if a Pokémon can still battle.
    Returns True if alive (HP > 0 and not fainted), otherwise False.
    """
    if pokemon is None:
        return False
    if hasattr(pokemon, "is_fainted"):
        try:
            val = pokemon.is_fainted()
            if val is not None:
                return not bool(val)
        except Exception:
            pass
    return getattr(pokemon, "hp", 0) > 0

def get_conscious_pokemon(party):
    """
    Returns a list of all Pokémon in the party that have not fainted.
    """
    if not isinstance(party, list):
        return []
    conscious_list = []
    for mon in party:
        if is_pokemon_conscious(mon):
            conscious_list.append(mon)
    return conscious_list

def has_conscious_pokemon(party):
    """
    Checks whether the trainer has at least one conscious Pokémon left to fight.
    Returns True if at least 1 Pokémon has HP > 0, otherwise False.
    """
    if not isinstance(party, list) or len(party) == 0:
        return False
    for mon in party:
        if is_pokemon_conscious(mon):
            return True
    return False

def switch_pokemon(party, current_index, target_index):
    """
    Switches the active Pokémon to a different team member in the party.
    
    Returns a tuple: (success_boolean, new_index_integer, message_string)
    
    Rules:
    - target_index must be a valid slot in the party.
    - Cannot switch to the Pokémon that is already active (current_index).
    - Cannot switch to a fainted Pokémon (HP <= 0).
    """
    if not isinstance(party, list) or len(party) == 0:
        return False, current_index, "Party is empty!"

    if target_index < 0 or target_index >= len(party):
        return False, current_index, "Invalid Pokémon slot!"

    if target_index == current_index:
        mon_name = getattr(party[target_index], "name", "That Pokémon")
        return False, current_index, f"{mon_name} is already in battle!"

    target_mon = party[target_index]
    if not is_pokemon_conscious(target_mon):
        mon_name = getattr(target_mon, "name", "That Pokémon")
        return False, current_index, f"{mon_name} has fainted and cannot battle!"

    mon_name = getattr(target_mon, "name", "Pokémon")
    return True, target_index, f"Go, {mon_name}!"

def swap_party_order(party, idx1, idx2):
    """
    Swaps the positions of two Pokémon within the party (e.g. to set a new lead).
    Returns True if successful, otherwise False.
    """
    if not isinstance(party, list):
        return False
    if idx1 < 0 or idx1 >= len(party) or idx2 < 0 or idx2 >= len(party):
        return False
    party[idx1], party[idx2] = party[idx2], party[idx1]
    return True

def heal_party(party):
    """
    Heals all Pokémon in the party back to full HP!
    Equivalent to visiting Nurse Joy at a Pokémon Center.
    Returns the count of Pokémon healed.
    """
    if not isinstance(party, list):
        return 0
    count = 0
    for mon in party:
        if mon is not None:
            max_hp = getattr(mon, "max_hp", 50)
            if hasattr(mon, "heal"):
                try:
                    mon.heal(max_hp)
                except Exception:
                    mon.hp = max_hp
            else:
                mon.hp = max_hp
            count += 1
    return count

def get_species_template(species_name):
    """
    Searches STARTER_TEMPLATES and WILD_TEMPLATES for matching Pokémon data.
    Safely ignores letter case and whitespace.
    """
    if not species_name or not isinstance(species_name, str):
        return None
    clean_name = species_name.strip().lower()

    # 1. Check starter templates
    for key, data in STARTER_TEMPLATES.items():
        if key.lower() == clean_name or data["name"].lower() == clean_name:
            return data

    # 2. Check wild templates
    for data in WILD_TEMPLATES:
        if data["name"].lower() == clean_name:
            return data

    return None

def create_team_pokemon(PokemonClass, species_name, level=5):
    """
    Factory function to instantiate a Pokémon for the player's team
    from the global Pokémon data registry.
    """
    data = get_species_template(species_name)
    if not data:
        # Safe fallback
        data = STARTER_TEMPLATES["pikachu"]

    scaled_hp = data["max_hp"] + max(0, level - 5) * 5
    scaled_atk = data["attack"] + max(0, level - 5) * 3
    scaled_def = data["defense"] + max(0, level - 5) * 2

    mon = PokemonClass(
        name=data["name"],
        poke_type=data["type"],
        max_hp=scaled_hp,
        attack=scaled_atk,
        defense=scaled_def,
        moves=list(data["moves"]),
        front_sprite=data.get("front_sprite", ""),
        back_sprite=data.get("back_sprite", data.get("front_sprite", "")),
        level=level
    )
    if hasattr(mon, "max_hp"):
        mon.hp = mon.max_hp
    elif hasattr(mon, "hp"):
        mon.max_hp = mon.hp
    return mon
