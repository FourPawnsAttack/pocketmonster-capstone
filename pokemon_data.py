"""
POKÉMON DATA CONFIGURATION
Contains moves, base stats, types, and sprite assets for the game.
"""

MOVES = {
    # Normal moves
    "Tackle": {"name": "Tackle", "type": "Normal", "power": 40},
    "Scratch": {"name": "Scratch", "type": "Normal", "power": 40},
    "Quick Attack": {"name": "Quick Attack", "type": "Normal", "power": 40},
    "Swift": {"name": "Swift", "type": "Normal", "power": 50},

    # Fire moves
    "Ember": {"name": "Ember", "type": "Fire", "power": 40},
    "Flamethrower": {"name": "Flamethrower", "type": "Fire", "power": 70},

    # Water moves
    "Water Gun": {"name": "Water Gun", "type": "Water", "power": 40},
    "Hydro Pump": {"name": "Hydro Pump", "type": "Water", "power": 75},

    # Grass moves
    "Vine Whip": {"name": "Vine Whip", "type": "Grass", "power": 45},
    "Solar Beam": {"name": "Solar Beam", "type": "Grass", "power": 75},

    # Electric moves
    "Thundershock": {"name": "Thundershock", "type": "Electric", "power": 40},
    "Thunderbolt": {"name": "Thunderbolt", "type": "Electric", "power": 70},

    # Other types
    "Gust": {"name": "Gust", "type": "Flying", "power": 40},
    "Shadow Ball": {"name": "Shadow Ball", "type": "Ghost", "power": 60},
    "Psychic": {"name": "Psychic", "type": "Psychic", "power": 75},
}

STARTER_TEMPLATES = {
    "charmander": {
        "name": "Charmander",
        "type": "Fire",
        "max_hp": 45,
        "attack": 52,
        "defense": 43,
        "moves": ["Scratch", "Ember", "Flamethrower", "Quick Attack"],
        "front_sprite": "/static/images/sprites/charmander.gif",
        "back_sprite": "/static/images/sprites/charmander_back.gif",
        "description": "A Fire-type lizard with high Attack and fiery determination!"
    },
    "squirtle": {
        "name": "Squirtle",
        "type": "Water",
        "max_hp": 48,
        "attack": 48,
        "defense": 58,
        "moves": ["Tackle", "Water Gun", "Hydro Pump", "Quick Attack"],
        "front_sprite": "/static/images/sprites/squirtle.gif",
        "back_sprite": "/static/images/sprites/squirtle_back.gif",
        "description": "A Water-type turtle with sturdy Defense and powerful water blasts!"
    },
    "bulbasaur": {
        "name": "Bulbasaur",
        "type": "Grass",
        "max_hp": 52,
        "attack": 49,
        "defense": 49,
        "moves": ["Tackle", "Vine Whip", "Solar Beam", "Quick Attack"],
        "front_sprite": "/static/images/sprites/bulbasaur.gif",
        "back_sprite": "/static/images/sprites/bulbasaur_back.gif",
        "description": "A Grass-type companion with high endurance and leafy attacks!"
    },
    "pikachu": {
        "name": "Pikachu",
        "type": "Electric",
        "max_hp": 42,
        "attack": 55,
        "defense": 40,
        "moves": ["Quick Attack", "Thundershock", "Thunderbolt", "Tackle"],
        "front_sprite": "/static/images/sprites/pikachu.gif",
        "back_sprite": "/static/images/sprites/pikachu_back.gif",
        "description": "An Electric-type mouse with shocking speed and electric sparks!"
    }
}

WILD_TEMPLATES = [
    {
        "name": "Pidgey",
        "type": "Flying",
        "max_hp": 35,
        "attack": 38,
        "defense": 35,
        "moves": ["Tackle", "Gust", "Quick Attack"],
        "front_sprite": "/static/images/sprites/pidgey.gif",
        "back_sprite": "",
        "rarity": "Common"
    },
    {
        "name": "Gengar",
        "type": "Ghost",
        "max_hp": 50,
        "attack": 55,
        "defense": 45,
        "moves": ["Scratch", "Shadow Ball", "Quick Attack"],
        "front_sprite": "/static/images/sprites/gengar.gif",
        "back_sprite": "",
        "rarity": "Uncommon"
    },
    {
        "name": "Mewtwo",
        "type": "Psychic",
        "max_hp": 85,
        "attack": 75,
        "defense": 65,
        "moves": ["Swift", "Psychic", "Shadow Ball"],
        "front_sprite": "/static/images/sprites/mewtwo.gif",
        "back_sprite": "",
        "rarity": "Legendary Boss"
    }
]

# Simple, intuitive type advantage chart for beginners:
TYPE_CHART = {
    ("Fire", "Grass"): 2.0,
    ("Fire", "Water"): 0.5,
    ("Fire", "Fire"): 0.5,

    ("Water", "Fire"): 2.0,
    ("Water", "Grass"): 0.5,
    ("Water", "Water"): 0.5,

    ("Grass", "Water"): 2.0,
    ("Grass", "Fire"): 0.5,
    ("Grass", "Grass"): 0.5,

    ("Electric", "Water"): 2.0,
    ("Electric", "Flying"): 2.0,
    ("Electric", "Grass"): 0.5,
    ("Electric", "Electric"): 0.5,

    ("Flying", "Grass"): 2.0,
    ("Flying", "Electric"): 0.5,

    ("Ghost", "Normal"): 0.5,
    ("Normal", "Ghost"): 0.5,
}
