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

    # Other types & Powerful evolution moves
    "Gust": {"name": "Gust", "type": "Flying", "power": 40},
    "Shadow Ball": {"name": "Shadow Ball", "type": "Ghost", "power": 60},
    "Psychic": {"name": "Psychic", "type": "Psychic", "power": 75},
    "Fire Blast": {"name": "Fire Blast", "type": "Fire", "power": 90},
    "Surf": {"name": "Surf", "type": "Water", "power": 70},
    "Petal Dance": {"name": "Petal Dance", "type": "Grass", "power": 80},
    "Thunder": {"name": "Thunder", "type": "Electric", "power": 85},
    "Dragon Breath": {"name": "Dragon Breath", "type": "Dragon", "power": 65},
    "Hyper Beam": {"name": "Hyper Beam", "type": "Normal", "power": 95},

    # Additional Type Moves
    "Bug Bite": {"name": "Bug Bite", "type": "Bug", "power": 45},
    "Rock Throw": {"name": "Rock Throw", "type": "Rock", "power": 45},
    "Rock Slide": {"name": "Rock Slide", "type": "Rock", "power": 65},
    "Absorb": {"name": "Absorb", "type": "Grass", "power": 35},
    "Bite": {"name": "Bite", "type": "Normal", "power": 50},
    "Karate Chop": {"name": "Karate Chop", "type": "Fighting", "power": 50},
    "Low Kick": {"name": "Low Kick", "type": "Fighting", "power": 45},
    "Flame Wheel": {"name": "Flame Wheel", "type": "Fire", "power": 55},
    "Psybeam": {"name": "Psybeam", "type": "Psychic", "power": 55},
    "Body Slam": {"name": "Body Slam", "type": "Normal", "power": 70},
    "Headbutt": {"name": "Headbutt", "type": "Normal", "power": 55},
    "Wing Attack": {"name": "Wing Attack", "type": "Flying", "power": 55},
    "Bubble Beam": {"name": "Bubble Beam", "type": "Water", "power": 55},
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
        "name": "Caterpie",
        "type": "Bug",
        "max_hp": 30,
        "attack": 30,
        "defense": 35,
        "moves": ["Tackle", "Bug Bite"],
        "front_sprite": "/static/images/sprites/caterpie.gif",
        "back_sprite": "/static/images/sprites/caterpie_back.gif",
        "rarity": "Common"
    },
    {
        "name": "Geodude",
        "type": "Rock",
        "max_hp": 40,
        "attack": 48,
        "defense": 58,
        "moves": ["Tackle", "Rock Throw"],
        "front_sprite": "/static/images/sprites/geodude.gif",
        "back_sprite": "/static/images/sprites/geodude_back.gif",
        "rarity": "Common"
    },
    {
        "name": "Zubat",
        "type": "Poison",
        "max_hp": 35,
        "attack": 40,
        "defense": 35,
        "moves": ["Bite", "Gust", "Quick Attack"],
        "front_sprite": "/static/images/sprites/zubat.gif",
        "back_sprite": "/static/images/sprites/zubat_back.gif",
        "rarity": "Common"
    },
    {
        "name": "Oddish",
        "type": "Grass",
        "max_hp": 42,
        "attack": 45,
        "defense": 45,
        "moves": ["Absorb", "Vine Whip", "Tackle"],
        "front_sprite": "/static/images/sprites/oddish.gif",
        "back_sprite": "/static/images/sprites/oddish_back.gif",
        "rarity": "Common"
    },
    {
        "name": "Eevee",
        "type": "Normal",
        "max_hp": 46,
        "attack": 48,
        "defense": 45,
        "moves": ["Tackle", "Quick Attack", "Bite"],
        "front_sprite": "/static/images/sprites/eevee.gif",
        "back_sprite": "/static/images/sprites/eevee_back.gif",
        "rarity": "Common"
    },
    {
        "name": "Machop",
        "type": "Fighting",
        "max_hp": 48,
        "attack": 56,
        "defense": 42,
        "moves": ["Karate Chop", "Low Kick", "Tackle"],
        "front_sprite": "/static/images/sprites/machop.gif",
        "back_sprite": "/static/images/sprites/machop_back.gif",
        "rarity": "Uncommon"
    },
    {
        "name": "Growlithe",
        "type": "Fire",
        "max_hp": 46,
        "attack": 55,
        "defense": 45,
        "moves": ["Ember", "Flame Wheel", "Bite"],
        "front_sprite": "/static/images/sprites/growlithe.gif",
        "back_sprite": "/static/images/sprites/growlithe_back.gif",
        "rarity": "Uncommon"
    },
    {
        "name": "Butterfree",
        "type": "Bug",
        "max_hp": 52,
        "attack": 46,
        "defense": 44,
        "moves": ["Gust", "Bug Bite", "Psybeam"],
        "front_sprite": "/static/images/sprites/butterfree.gif",
        "back_sprite": "/static/images/sprites/butterfree_back.gif",
        "rarity": "Uncommon"
    },
    {
        "name": "Abra",
        "type": "Psychic",
        "max_hp": 38,
        "attack": 62,
        "defense": 28,
        "moves": ["Psybeam", "Swift", "Quick Attack"],
        "front_sprite": "/static/images/sprites/abra.gif",
        "back_sprite": "/static/images/sprites/abra_back.gif",
        "rarity": "Uncommon"
    },
    {
        "name": "Gengar",
        "type": "Ghost",
        "max_hp": 54,
        "attack": 58,
        "defense": 48,
        "moves": ["Scratch", "Shadow Ball", "Quick Attack"],
        "front_sprite": "/static/images/sprites/gengar.gif",
        "back_sprite": "",
        "rarity": "Uncommon"
    },
    {
        "name": "Snorlax",
        "type": "Normal",
        "max_hp": 82,
        "attack": 68,
        "defense": 58,
        "moves": ["Body Slam", "Headbutt", "Bite"],
        "front_sprite": "/static/images/sprites/snorlax.gif",
        "back_sprite": "/static/images/sprites/snorlax_back.gif",
        "rarity": "Rare"
    },
    {
        "name": "Gyarados",
        "type": "Water",
        "max_hp": 76,
        "attack": 72,
        "defense": 62,
        "moves": ["Hydro Pump", "Bite", "Dragon Breath"],
        "front_sprite": "/static/images/sprites/gyarados.gif",
        "back_sprite": "/static/images/sprites/gyarados_back.gif",
        "rarity": "Rare"
    },
    {
        "name": "Dragonite",
        "type": "Dragon",
        "max_hp": 86,
        "attack": 82,
        "defense": 68,
        "moves": ["Dragon Breath", "Wing Attack", "Hyper Beam"],
        "front_sprite": "/static/images/sprites/dragonite.gif",
        "back_sprite": "/static/images/sprites/dragonite_back.gif",
        "rarity": "Epic"
    },
    {
        "name": "Mewtwo",
        "type": "Psychic",
        "max_hp": 90,
        "attack": 82,
        "defense": 70,
        "moves": ["Swift", "Psychic", "Shadow Ball", "Hyper Beam"],
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

# ====================================================================
# PROGRESSION & EVOLUTION CONFIGURATION
# ====================================================================

EVOLUTION_DATA = {
    "Charmander": {
        "evolves_at": 7,
        "evolves_into": "Charmeleon",
        "stat_boost": {"max_hp": 15, "attack": 12, "defense": 10},
        "new_move": "Fire Blast",
        "front_sprite": "/static/images/sprites/charmeleon.gif",
        "back_sprite": "/static/images/sprites/charmeleon_back.gif"
    },
    "Charmeleon": {
        "evolves_at": 10,
        "evolves_into": "Charizard",
        "stat_boost": {"max_hp": 25, "attack": 20, "defense": 15},
        "new_move": "Dragon Breath",
        "front_sprite": "/static/images/sprites/charizard.gif",
        "back_sprite": "/static/images/sprites/charizard_back.gif"
    },
    "Squirtle": {
        "evolves_at": 7,
        "evolves_into": "Wartortle",
        "stat_boost": {"max_hp": 15, "attack": 10, "defense": 14},
        "new_move": "Surf",
        "front_sprite": "/static/images/sprites/wartortle.gif",
        "back_sprite": "/static/images/sprites/wartortle_back.gif"
    },
    "Wartortle": {
        "evolves_at": 10,
        "evolves_into": "Blastoise",
        "stat_boost": {"max_hp": 25, "attack": 16, "defense": 22},
        "new_move": "Hyper Beam",
        "front_sprite": "/static/images/sprites/blastoise.gif",
        "back_sprite": "/static/images/sprites/blastoise_back.gif"
    },
    "Bulbasaur": {
        "evolves_at": 7,
        "evolves_into": "Ivysaur",
        "stat_boost": {"max_hp": 18, "attack": 10, "defense": 12},
        "new_move": "Petal Dance",
        "front_sprite": "/static/images/sprites/ivysaur.gif",
        "back_sprite": "/static/images/sprites/ivysaur_back.gif"
    },
    "Ivysaur": {
        "evolves_at": 10,
        "evolves_into": "Venusaur",
        "stat_boost": {"max_hp": 28, "attack": 18, "defense": 18},
        "new_move": "Hyper Beam",
        "front_sprite": "/static/images/sprites/venusaur.gif",
        "back_sprite": "/static/images/sprites/venusaur_back.gif"
    },
    "Pikachu": {
        "evolves_at": 8,
        "evolves_into": "Raichu",
        "stat_boost": {"max_hp": 22, "attack": 22, "defense": 14},
        "new_move": "Thunder",
        "front_sprite": "/static/images/sprites/raichu.gif",
        "back_sprite": "/static/images/sprites/raichu_back.gif"
    }
}

# Moves learned automatically upon hitting specific level milestones:
LEARNABLE_MOVES = {
    "Charmander": [(6, "Flamethrower"), (7, "Fire Blast"), (10, "Dragon Breath")],
    "Charmeleon": [(8, "Fire Blast"), (10, "Dragon Breath")],
    "Squirtle": [(6, "Hydro Pump"), (7, "Surf"), (10, "Hyper Beam")],
    "Wartortle": [(8, "Surf"), (10, "Hyper Beam")],
    "Bulbasaur": [(6, "Solar Beam"), (7, "Petal Dance"), (10, "Hyper Beam")],
    "Ivysaur": [(8, "Petal Dance"), (10, "Hyper Beam")],
    "Pikachu": [(6, "Thunderbolt"), (8, "Thunder"), (10, "Hyper Beam")],
    "Raichu": [(9, "Thunder"), (10, "Hyper Beam")],
}

# ====================================================================
# GYM PROGRESSION SYSTEM
# ====================================================================

GYMS = [
    {
        "id": "pewter",
        "name": "Pewter Gym",
        "city": "Pewter City",
        "leader": "Brock",
        "title": "The Rock-Solid Pokémon Trainer",
        "badge_id": "boulder",
        "badge_name": "Boulder Badge",
        "badge_icon": "🪨",
        "type": "Rock",
        "recommended_level": 6,
        "dialogue_intro": "I'm Brock, the Pewter Gym Leader! My rock-hard willpower is unbreakable!",
        "dialogue_defeat": "I took you for granted. As proof of your victory, here is the Boulder Badge!",
        "reward_exp": 150,
        "reward_potions": 2,
        "team": [
            {
                "name": "Geodude",
                "type": "Rock",
                "level": 6,
                "max_hp": 45,
                "attack": 48,
                "defense": 55,
                "moves": ["Tackle", "Rock Throw"],
                "front_sprite": "/static/images/sprites/geodude.gif",
                "back_sprite": "/static/images/sprites/geodude_back.gif"
            },
            {
                "name": "Onix",
                "type": "Rock",
                "level": 8,
                "max_hp": 58,
                "attack": 52,
                "defense": 65,
                "moves": ["Tackle", "Rock Slide", "Bite"],
                "front_sprite": "/static/images/sprites/onix.gif",
                "back_sprite": "/static/images/sprites/onix_back.gif"
            }
        ]
    },
    {
        "id": "cerulean",
        "name": "Cerulean Gym",
        "city": "Cerulean City",
        "leader": "Misty",
        "title": "The Tomboyish Mermaid",
        "badge_id": "cascade",
        "badge_name": "Cascade Badge",
        "badge_icon": "💧",
        "type": "Water",
        "recommended_level": 10,
        "dialogue_intro": "My policy is an all-out offensive with Water-type Pokémon! Can you swim with the best?",
        "dialogue_defeat": "You're much tougher than you look! You've earned the Cascade Badge!",
        "reward_exp": 200,
        "reward_potions": 3,
        "team": [
            {
                "name": "Staryu",
                "type": "Water",
                "level": 9,
                "max_hp": 50,
                "attack": 50,
                "defense": 52,
                "moves": ["Water Gun", "Swift", "Tackle"],
                "front_sprite": "/static/images/sprites/staryu.gif",
                "back_sprite": "/static/images/sprites/staryu_back.gif"
            },
            {
                "name": "Gyarados",
                "type": "Water",
                "level": 11,
                "max_hp": 70,
                "attack": 66,
                "defense": 60,
                "moves": ["Hydro Pump", "Bite", "Dragon Breath"],
                "front_sprite": "/static/images/sprites/gyarados.gif",
                "back_sprite": "/static/images/sprites/gyarados_back.gif"
            }
        ]
    },
    {
        "id": "vermilion",
        "name": "Vermilion Gym",
        "city": "Vermilion City",
        "leader": "Lt. Surge",
        "title": "The Lightning American",
        "badge_id": "thunder",
        "badge_name": "Thunder Badge",
        "badge_icon": "⚡",
        "type": "Electric",
        "recommended_level": 13,
        "dialogue_intro": "Ten-hut! Electric Pokémon saved my life in the army! They'll zap ya to ashes!",
        "dialogue_defeat": "Whoa! You're the real deal kid! Take the Thunder Badge and wear it proudly!",
        "reward_exp": 250,
        "reward_potions": 3,
        "team": [
            {
                "name": "Pikachu",
                "type": "Electric",
                "level": 12,
                "max_hp": 55,
                "attack": 60,
                "defense": 45,
                "moves": ["Quick Attack", "Thundershock", "Thunderbolt"],
                "front_sprite": "/static/images/sprites/pikachu.gif",
                "back_sprite": "/static/images/sprites/pikachu_back.gif"
            },
            {
                "name": "Raichu",
                "type": "Electric",
                "level": 14,
                "max_hp": 72,
                "attack": 70,
                "defense": 55,
                "moves": ["Thunderbolt", "Thunder", "Quick Attack", "Hyper Beam"],
                "front_sprite": "/static/images/sprites/raichu.gif",
                "back_sprite": "/static/images/sprites/raichu_back.gif"
            }
        ]
    },
    {
        "id": "celadon",
        "name": "Celadon Gym",
        "city": "Celadon City",
        "leader": "Erika",
        "title": "The Nature-Loving Princess",
        "badge_id": "rainbow",
        "badge_name": "Rainbow Badge",
        "badge_icon": "🌈",
        "type": "Grass",
        "recommended_level": 16,
        "dialogue_intro": "Hello... Lovely weather isn't it? My gentle Grass Pokémon are stronger than they appear.",
        "dialogue_defeat": "Oh, my! You are remarkably skilled. Please take this lovely Rainbow Badge.",
        "reward_exp": 300,
        "reward_potions": 4,
        "team": [
            {
                "name": "Oddish",
                "type": "Grass",
                "level": 14,
                "max_hp": 60,
                "attack": 55,
                "defense": 55,
                "moves": ["Absorb", "Vine Whip", "Petal Dance"],
                "front_sprite": "/static/images/sprites/oddish.gif",
                "back_sprite": "/static/images/sprites/oddish_back.gif"
            },
            {
                "name": "Venusaur",
                "type": "Grass",
                "level": 17,
                "max_hp": 88,
                "attack": 74,
                "defense": 72,
                "moves": ["Solar Beam", "Petal Dance", "Hyper Beam", "Vine Whip"],
                "front_sprite": "/static/images/sprites/venusaur.gif",
                "back_sprite": "/static/images/sprites/venusaur_back.gif"
            }
        ]
    },
    {
        "id": "viridian",
        "name": "Viridian Gym",
        "city": "Viridian City",
        "leader": "Giovanni",
        "title": "The Boss of Team Rocket",
        "badge_id": "earth",
        "badge_name": "Earth Badge",
        "badge_icon": "🌍",
        "type": "Ground",
        "recommended_level": 20,
        "dialogue_intro": "Welcome to my hideout! You have proven a nuisance to Team Rocket. Now face true power!",
        "dialogue_defeat": "Ha! A fabulous battle! I concede defeat! Take the Earth Badge—you are a true Pokémon Master!",
        "reward_exp": 450,
        "reward_potions": 5,
        "team": [
            {
                "name": "Dragonite",
                "type": "Dragon",
                "level": 19,
                "max_hp": 90,
                "attack": 85,
                "defense": 75,
                "moves": ["Dragon Breath", "Wing Attack", "Hyper Beam"],
                "front_sprite": "/static/images/sprites/dragonite.gif",
                "back_sprite": "/static/images/sprites/dragonite_back.gif"
            },
            {
                "name": "Mewtwo",
                "type": "Psychic",
                "level": 22,
                "max_hp": 110,
                "attack": 92,
                "defense": 82,
                "moves": ["Psychic", "Shadow Ball", "Hyper Beam", "Swift"],
                "front_sprite": "/static/images/sprites/mewtwo.gif",
                "back_sprite": "",
            }
        ]
    }
]
