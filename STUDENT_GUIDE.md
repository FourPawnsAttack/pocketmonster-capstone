# ⚡ Pokémon Code Adventure: Student Trainer Guide

Welcome, Pokémon Trainer & Coder! 🎮

In this adventure, you are going to program your very own **Pokémon Battle & Catching Game** using Python!

Every file you work on gives your game superpowers. Once you finish your missions, you will have a working retro web game where you can pick your starter, battle wild Pokémon, cast elemental moves, and catch wild Pokémon in Pokéballs!

---

## 🚀 Quick Start: How to Run and Test Your Game

### 1. Launch the Game in Your Browser
Open your terminal and run:
```bash
./run.sh
```
Then open your browser to:
👉 **`http://localhost:5000`**

*(If you are pairing with your teacher on VS Code Live Share, your teacher can share port 5000 so you can play on your laptop!)*

### 2. Check Your Code with the Master Test Runner
Whenever you write or change code, check your progress by running:
```bash
python3 run_tests.py
```
You will see friendly star badges ⭐ as you pass each test!

---

## 🗺️ The 4 Pokémon Missions

```
Mission 1: pokemon.py   --> Build the Pokémon Blueprint (Classes & Objects)
Mission 2: starters.py  --> Professor Oak's Starter Lab (Dictionaries & Strings)
Mission 3: battle.py    --> The Battle Engine (Damage Math & Enemy AI)
Mission 4: catching.py  --> Safari Catching (Probabilities & Pokéballs)
```

---

## 🛡️ Mission 1: The Pokémon Class (`pokemon.py`)
**Test with:** `python3 tests/test_pokemon.py`

### 🎯 Your Goal
Teach Python what a Pokémon is! A **Class** is like a blueprint (or a Pokémon trading card template). Every individual Pokémon created from this blueprint is called an **Object**.

### 📝 What to Code in `pokemon.py`

1. **`__init__(self, name, poke_type, max_hp, attack, defense, moves, front_sprite="", back_sprite="")`**:
   - Save all the stats onto `self`.
   - Set current HP: `self.hp = max_hp` (Pokémon start battle with full health!).
   - *Example:* `self.name = name`, `self.attack = attack`.

2. **`take_damage(self, amount)`**:
   - If `amount` is 0 or negative, do nothing and return `self.hp`.
   - Subtract `amount` from `self.hp`.
   - **Clamp to 0**: A Pokémon cannot have negative health! If `self.hp < 0`, set `self.hp = 0`.
   - Return the updated `self.hp`.

3. **`heal(self, amount)`**:
   - If `amount` is 0 or negative, return `self.hp`.
   - Add `amount` to `self.hp`.
   - **Clamp to max_hp**: A Pokémon's health cannot exceed `self.max_hp`!
   - Return the updated `self.hp`.

4. **`is_fainted(self)`**:
   - Return `True` if `self.hp <= 0`, otherwise return `False`.

### 💡 Trainer Hints
- **What is `self`?** Think of `self` as a Pokémon's personal backpack or name tag. It ensures that when Pikachu takes damage, Charmander doesn't lose health!
- **Edge Case Alert:** What happens if a move accidentally deals `-10` damage? Without an `if amount <= 0:` check, subtracting a negative number would accidentally *heal* the Pokémon!

---

## 🌿 Mission 2: Professor Oak's Starter Lab (`starters.py`)
**Test with:** `python3 tests/test_starters.py`

### 🎯 Your Goal
Help Professor Oak give new trainers their starter Pokémon (Charmander, Squirtle, Bulbasaur, or Pikachu)!

### 📝 What to Code in `starters.py`

1. **`create_starter(choice)`**:
   - **Clean up the choice string**:
     - Players might type spaces or weird casing like `" Charmander "` or `"sQuIrTlE"`.
     - Use `.strip().lower()` to clean it up!
   - **Safeguard inputs**:
     - If `choice` is empty or not a string, default to `"pikachu"`.
   - **Check STARTER_TEMPLATES**:
     - If the cleaned choice is in `STARTER_TEMPLATES`, grab its data dictionary.
     - Otherwise, default to `STARTER_TEMPLATES["pikachu"]`.
   - **Create and Return the Pokémon**:
     - Instantiate and return a `Pokemon` object using the values from the dictionary!

### 💡 Trainer Hints
- In `pokemon_data.py`, look at `STARTER_TEMPLATES`. Each starter has keys like `data["name"]`, `data["type"]`, `data["max_hp"]`, `data["attack"]`, `data["defense"]`, and `data["moves"]`.
- Make sure to pass a copy of the moves list: `moves=list(data["moves"])` so two players picking the same starter don't share the same moves list!

---

## ⚔️ Mission 3: The Battle Arena Engine (`battle.py`)
**Test with:** `python3 tests/test_battle.py`

### 🎯 Your Goal
Program the combat math that decides how much damage attacks deal and how the enemy chooses its moves!

### 📝 What to Code in `battle.py`

1. **`get_type_multiplier(move_type, defender_type)`**:
   - Look up the matchup in `TYPE_CHART` (or use `PokeType.get(move_type).effectiveness_against(defender_type)`).
   - Super effective deals **`2.0`** (e.g. Water vs Fire).
   - Not very effective deals **`0.5`** (e.g. Fire vs Water).
   - Neutral deals **`1.0`** (e.g. Normal vs Normal).

2. **`calculate_damage(move_name, attacker, defender)`**:
   - **Step 1: Move Power**: Look up `move_name` in `MOVES`. If unknown, default power to 40 and type to `"Normal"`.
   - **Step 2: Base Damage**:
     $$\text{base\_damage} = \frac{\text{power} \times \text{attacker.attack}}{\text{defender.defense}}$$
     *(Guard against zero defense: if defender.defense <= 0, use 1!)*
   - **Step 3: Critical Hit**:
     - Roll a random float: `is_critical = random.random() < 0.10` (10% chance!).
     - If critical, multiplier is `1.5`, otherwise `1.0`.
   - **Step 4: Type Multiplier**:
     - Call `get_type_multiplier(move_type, defender.poke_type)`.
   - **Step 5: Final Damage**:
     - Multiply: `total = base_damage * crit_mult * type_mult`.
     - Round to a whole number and guarantee at least 1 damage: `final_damage = max(1, int(round(total)))`.
   - **Return**: A 3-item tuple: `return final_damage, is_critical, type_mult`.

3. **`choose_enemy_move(enemy_pokemon)`**:
   - If `enemy_pokemon.moves` is empty, return `"Tackle"`.
   - Otherwise, pick a random move: `return random.choice(enemy_pokemon.moves)`.

### 💡 Trainer Hints
- Remember that Python functions can return multiple items as a tuple:
  `return final_damage, is_critical, type_multiplier`
- When you run your damage formula in the game, you'll see glowing red damage numbers and retro sound effects!

---

## 🔴 Mission 4: The Safari Catching Engine (`catching.py`)
**Test with:** `python3 tests/test_catching.py`

### 🎯 Your Goal
Throw Pokéballs and calculate whether a wild Pokémon is caught or breaks free!

### 📝 What to Code in `catching.py`

1. **`attempt_catch(wild_pokemon, ball_type="poke-ball")`**:
   - **Ball Multipliers**:
     - Poké Ball = `1.0x`
     - Great Ball = `1.5x`
     - Ultra Ball = `2.0x`
   - **Missing HP Percentage**:
     - Weaker Pokémon are easier to catch!
     - $\text{missing\_hp\_pct} = \frac{\text{max\_hp} - \text{current\_hp}}{\text{max\_hp}}$
   - **Catch Chance Formula**:
     - $\text{base\_chance} = 0.30 + (0.60 \times \text{missing\_hp\_pct})$
     - $\text{total\_chance} = \min(0.95, \text{base\_chance} \times \text{ball\_mult})$
   - **Roll to Catch**:
     - Roll `roll = random.random()`.
     - If `roll < total_chance`: Caught! Return `True, 3` (3 shakes and a click!).
     - Else: Escaped! Determine suspense shakes:
       - If `roll < total_chance + 0.15`: Return `False, 2` (broke out on 2nd shake!).
       - Else if `roll < total_chance + 0.35`: Return `False, 1`.
       - Else: Return `False, 0` (broke out immediately!).

---

## 🌟 Bonus: Elemental Types & `PokeType` (`poke_type.py`)

Did you know types are real objects in this game?
- You can inspect a type:
  ```python
  from poke_type import PokeType
  fire = PokeType.get("Fire")
  print(fire.effectiveness_against("Grass")) # 2.0x!
  ```
- **Dual Types**: Some Pokémon have two types (e.g. Water + Flying). You can calculate compound effectiveness by multiplying both defensive multipliers!

---

## 🐛 Bug Catcher's Survival Guide (Common Errors)

| Error Message | What It Usually Means | How to Fix It |
| :--- | :--- | :--- |
| **`IndentationError`** | Python lines aren't lined up. | Ensure every indented block uses 4 spaces. |
| **`AttributeError: 'Pokemon' object has no attribute 'hp'`** | The Pokémon doesn't have an `hp` variable. | In `__init__`, write `self.hp = max_hp`. |
| **`TypeError: cannot unpack non-iterable NoneType object`** | Your function returned `None` instead of a tuple. | Did you forget a `return` statement? E.g., `return damage, is_critical, mult`. |
| **`ZeroDivisionError: division by zero`** | Dividing by 0 defense or 0 max HP. | Use `defense = max(1, defender.defense)` before dividing! |
| **`KeyError: 'swift'`** | Dictionary couldn't find a move name. | Use `.get()` or check casing (`move_name.capitalize()`). |

---

## 🏆 Becoming a Pokémon Code Master!

Once all 4 missions pass (`python3 run_tests.py` shows 4/4 completed):
1. **Choose your Starter** in Professor Oak's lab.
2. **Battle wild Pidgey and Gengar** in the arena.
3. **Use Potions** from your bag when health is low.
4. **Throw Pokéballs** to fill up your Pokédex.
5. **Defeat the Legendary Boss (Mewtwo)** at battle streak 3!

Good luck, Trainer! You've got this! 🚀✨
