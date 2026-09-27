# 🏷️ Move Types & Badge System: Curriculum & Pedagogical Guide

> **Reference:** [PokémonDB All Moves Database](https://pokemondb.net/move/all)  
> **Target Audience:** 12-year-old student learning Python for the first time  
> **Pedagogical Goal:** Teach data structures (dictionaries, lists, lookups) and combat math through elemental move typing and instant visual UI feedback.

---

## 📖 1. Overview & Motivation

In Pokémon battle mechanics, every move has an **elemental type** (e.g. *Ember* is **Fire**, *Water Gun* is **Water**, *Vine Whip* is **Grass**, *Thunderbolt* is **Electric**, and *Tackle* is **Normal**). 

### The Problem
Previously, moves in the battle UI were displayed as generic monochrome buttons showing only `MOVE NAME` and `POW: 40+`. In battle calculations, move typing was pre-configured behind the scenes, depriving the student of the fun and insight of discovering **how move types interact with defending Pokémon**.

### The Proposal
1. **Visual Move Badges in Retro Web UI**: Add a small, high-contrast elemental badge to every move button in the Battle Arena (e.g. `EMBER` `[FIRE]`, `WATER GUN` `[WATER]`, `TACKLE` `[NORMAL]`), along with its exact base power.
2. **The "Move Typing" Mission**: Start all moves as default `"Normal"` type. The student must assign or resolve moves to their authentic elemental types according to PokémonDB.
3. **Instant "Aha!" Payoff**: 
   - When *Ember* is `"Normal"`, using it against Bulbasaur deals neutral `1.0x` damage with a gray `[NORMAL]` badge.
   - Once the student re-types *Ember* to `"Fire"`, the badge turns radiant red `[FIRE]` in the UI, and the battle engine announces:  
     `🔥 It's super effective! Dealt 2.0x damage!`

---

## 🧠 2. Pedagogical Difficulty Assessment for a 12-Year-Old

How difficult is this for a beginner 12-year-old student?

| Approach | Python Concepts Used | Difficulty (1 to 5) | Cognitive Load | Recommended For |
| :--- | :--- | :--- | :--- | :--- |
| **Option A: Dictionary Data Mapping** | Dict keys/values, strings | ⭐ 1.5 / 5 | Low (Fun & Visual) | **First-time Python learners** |
| **Option B: Classifier Function (`get_move_type`)** | `if`/`elif`/`else`, `in` list, `.lower()` | ⭐⭐ 2.5 / 5 | Medium (Logic practice) | **Students learning conditionals** |
| **Option C: Object-Oriented `Move` Class** | Classes, `__init__`, composition | ⭐⭐⭐ 3.5 / 5 | High (Multi-file refactor) | **Bonus / Advanced challenge** |

### Why This Is Beginner-Friendly (Low Friction, High Reward)
- **Gamified Intuition**: 12-year-olds already know from playing Pokémon that Charizard breathes fire and Pikachu shoots electricity. They do not need to memorize abstract formulas; their gaming knowledge guides their coding!
- **Instant Visual Validation**: The retro browser UI immediately reflects their changes without needing to decipher complex terminal tracebacks.
- **Natural Stepping Stone to Mission 3**: Mission 3 currently asks students to write `get_type_multiplier(move_type, defender_type)`. If all moves are `"Normal"`, that function cannot shine until moves have real types!

---

## 🛠️ 3. Implementation Architectures

### Option A: The Dictionary Data Mission (Beginner - Recommended)
In `pokemon_data.py`, all moves are initially provided with `"type": "Normal"`:

```python
# INITIAL STUDENT STATE:
MOVES = {
    "Tackle":        {"name": "Tackle",        "type": "Normal", "power": 40},
    "Quick Attack":  {"name": "Quick Attack",  "type": "Normal", "power": 40},
    "Ember":         {"name": "Ember",         "type": "Normal", "power": 40}, # 👈 Student fixes this to "Fire"!
    "Water Gun":     {"name": "Water Gun",     "type": "Normal", "power": 40}, # 👈 Student fixes this to "Water"!
    "Vine Whip":     {"name": "Vine Whip",     "type": "Normal", "power": 45}, # 👈 Student fixes this to "Grass"!
    "Thundershock":  {"name": "Thundershock",  "type": "Normal", "power": 40}, # 👈 Student fixes this to "Electric"!
}
```

#### What the Student Learns:
- How Python dictionaries work (`key: value` pairs).
- Accurate syntax (commas, quotes, colons).
- Researching specifications: Looking up moves on [pokemondb.net/move/all](https://pokemondb.net/move/all).

#### Mitigating "Data Entry" Fatigue:
> [!TIP]
> Do **not** make the student re-type all 35 moves in the game! Only have them fix the **8 core starter moves** for Charmander, Squirtle, Bulbasaur, and Pikachu. The rest can remain pre-filled or bonus.

---

### Option B: The Classifier Function (`get_move_type`) in `battle.py`
Instead of editing raw dictionary data, the student writes a Python function in `battle.py`:

```python
def get_move_type(move_name):
    """
    Returns the elemental type string for a given move name.
    Defaults to 'Normal' if the move is unknown or physical.
    """
    clean_name = str(move_name).strip().lower()
    
    if clean_name in ["ember", "flamethrower", "fire blast", "flame wheel"]:
        return "Fire"
    elif clean_name in ["water gun", "hydro pump", "surf", "bubble beam"]:
        return "Water"
    elif clean_name in ["vine whip", "solar beam", "petal dance", "absorb"]:
        return "Grass"
    elif clean_name in ["thundershock", "thunderbolt", "thunder"]:
        return "Electric"
    elif clean_name in ["gust", "wing attack"]:
        return "Flying"
    elif clean_name in ["psybeam", "psychic"]:
        return "Psychic"
    else:
        return "Normal"
```

#### What the Student Learns:
- String sanitization (`.strip().lower()`).
- Checking list membership with `in`.
- Writing multi-branch `if` / `elif` / `else` control flow.
- Providing defensive fallback (`else: return "Normal"`).

---

### Option C: The OOP `Move` Class (Advanced / Bonus)
Introduce a new class in `pokemon.py` or `move.py`:

```python
class Move:
    def __init__(self, name, poke_type, power):
        self.name = str(name).strip()
        self.poke_type = str(poke_type).strip().capitalize()
        self.power = int(power)

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.poke_type,
            "power": self.power
        }
```

Then in `Pokemon`, `self.moves` contains instances of `Move`:
```python
ember = Move("Ember", "Fire", 40)
print(ember.poke_type) # "Fire"
```

#### Why Option C is Too Heavy for Day 1:
- Requiring a `Move` object changes `Pokemon.__init__` parameters and breaks existing starter factory dictionaries.
- It is best kept as an **optional stretch challenge** after Mission 5.

---

## 🎨 4. Retro UI Move Badge Implementation

The Web UI now features dedicated pixel-art badges for each move!

### CSS Type Badge Palette (`static/css/style.css`)
Matches authentic Pokémon elemental colors:
- 🔥 **Fire**: `#e74c3c` (Crimson Red)
- 💧 **Water**: `#3498db` (Cerulean Blue)
- 🌿 **Grass**: `#2ecc71` (Emerald Green)
- ⚡ **Electric**: `#f1c40f` (Electric Yellow, black text)
- ⚪ **Normal**: `#95a5a6` (Silver Gray)
- 🌪️ **Flying**: `#1abc9c` (Turquoise)
- 👻 **Ghost**: `#8e44ad` (Deep Purple)
- 🔮 **Psychic**: `#e84393` (Psychic Pink)
- 🐛 **Bug**: `#879b1d` (Olive Green)
- 🪨 **Rock**: `#a59132` (Ochre Brown)
- 🥋 **Fighting**: `#c0392b` (Fighting Red)
- 🐉 **Dragon**: `#6c5ce7` (Indigo Dragon)

### Battle Menu Button Layout
```html
<button class="btn-retro btn-move">
    <div class="move-top-row">
        <span class="move-name">FLAMETHROWER</span>
        <span class="move-type-badge type-Fire">FIRE</span>
    </div>
    <div class="move-bottom-row">
        <span class="move-power">POW: 70</span>
    </div>
</button>
```

### Server Endpoint (`app.py`)
- Exposes `@app.route("/api/moves")` returning all moves and their configured types/powers.
- Includes `moves_database` in `/api/starters` so the browser loads move data instantly on startup.

---

## 🧪 5. Automated Testing Blueprint

To verify the student's move implementation, add the following test assertions to `tests/test_battle.py`:

```python
def test_move_types():
    """Verify that elemental starter moves have their proper types assigned."""
    expected_starter_moves = {
        "Ember": "Fire",
        "Flamethrower": "Fire",
        "Water Gun": "Water",
        "Hydro Pump": "Water",
        "Vine Whip": "Grass",
        "Solar Beam": "Grass",
        "Thundershock": "Electric",
        "Thunderbolt": "Electric",
        "Tackle": "Normal",
        "Quick Attack": "Normal",
    }
    for move_name, expected_type in expected_starter_moves.items():
        move_info = MOVES.get(move_name, {})
        actual_type = move_info.get("type", "Normal")
        assert actual_type.lower() == expected_type.lower(), (
            f"Move '{move_name}' should be '{expected_type}' type, but got '{actual_type}'! "
            f"Check https://pokemondb.net/move/all for reference."
        )
```

---

## 👩‍🏫 6. Teacher Coaching Tips & Socratic Questions

When walking a 12-year-old through this mission:

1. **Start with the In-Game Mystery**:
   - *"When you choose Charmander and use Ember on Bulbasaur, why does it only do normal damage? What color is the badge on the button?"*
   - Let the student notice that the badge is gray and says `[NORMAL]`.
2. **Open PokémonDB Together**:
   - Guide them to [pokemondb.net/move/all](https://pokemondb.net/move/all).
   - *"Search for Ember. What type does the website say it is? What color is its badge?"*
3. **Bridge to Python Dictionaries**:
   - *"Look at line 14 of `pokemon_data.py`. Can you find `\"Ember\"`? What key controls its type?"*
   - *"Change `\"type\": \"Normal\"` to `\"type\": \"Fire\"` and refresh your browser!"*
4. **Celebrate the Victory**:
   - When the student clicks *Ember* and sees a bright red `[FIRE]` badge and `2.0x Super Effective!` text, celebrate! That direct link between modifying code and seeing the game transform is the core magic of programming.
