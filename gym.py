"""
====================================================================
           POKÉMON GYM PROGRESSION SYSTEM (gym.py)
====================================================================
Manages Pokémon Gym Leaders, Gym Badges, Battle Progression,
and Trainer League Rules.
====================================================================
"""

from pokemon_data import GYMS

def get_all_gyms():
    """Returns the full list of Kanto Gyms."""
    return GYMS

def get_gym(gym_id):
    """
    Looks up a Gym by its ID (e.g. 'pewter', 'cerulean').
    Returns the gym dictionary or None if not found.
    """
    if not gym_id or not isinstance(gym_id, str):
        return None
    gym_id_clean = gym_id.strip().lower()
    for gym in GYMS:
        if gym["id"].lower() == gym_id_clean:
            return gym
    return None

def is_gym_unlocked(gym_id, player_badges):
    """
    Checks if a Gym is unlocked for the player based on their earned badges.
    The first gym (Pewter Gym / Brock) is unlocked by default.
    Subsequent gyms unlock sequentially once the preceding gym's badge is earned.
    """
    badges = set(player_badges or [])
    for idx, gym in enumerate(GYMS):
        if gym["id"].lower() == str(gym_id).strip().lower():
            if idx == 0:
                return True
            prev_gym = GYMS[idx - 1]
            return prev_gym["badge_id"] in badges
    return False

def can_catch_pokemon(is_gym_battle=False):
    """
    Enforces Pokémon League Rules:
    Wild Pokémon may be caught, but Gym Leader Pokémon cannot be captured!
    """
    return not bool(is_gym_battle)

def create_gym_pokemon(PokemonClass, data):
    """
    Factory function to instantiate a Gym Leader's Pokémon.
    """
    mon = PokemonClass(
        name=data["name"],
        poke_type=data["type"],
        max_hp=data["max_hp"],
        attack=data["attack"],
        defense=data["defense"],
        moves=list(data["moves"]),
        front_sprite=data["front_sprite"],
        back_sprite=data.get("back_sprite", ""),
        level=data.get("level", 5)
    )
    if hasattr(mon, "max_hp"):
        mon.hp = mon.max_hp
    elif hasattr(mon, "hp"):
        mon.max_hp = mon.hp
    else:
        mon.max_hp = data["max_hp"]
        mon.hp = data["max_hp"]
    return mon

def award_gym_rewards(gym_id, state):
    """
    Awards badge, EXP, and items to player upon defeating a Gym Leader.
    Returns a dictionary of rewards earned.
    """
    gym = get_gym(gym_id)
    if not gym:
        return None

    if "badges" not in state:
        state["badges"] = []

    badge_id = gym["badge_id"]
    badge_name = gym["badge_name"]
    is_first_time = badge_id not in state["badges"]
    if is_first_time:
        state["badges"].append(badge_id)

    # Award potions
    potions_awarded = gym.get("reward_potions", 2)
    state["potions"] = state.get("potions", 0) + potions_awarded

    return {
        "badge_id": badge_id,
        "badge_name": badge_name,
        "badge_icon": gym.get("badge_icon", "🏅"),
        "exp": gym.get("reward_exp", 150),
        "potions": potions_awarded,
        "is_first_time": is_first_time,
        "leader": gym["leader"],
        "defeat_dialogue": gym["dialogue_defeat"]
    }
