"""
====================================================================
           POKÉMON CAPSTONE SERVER (Flask API)
====================================================================
Serves the web battle interface and orchestrates game state between
the browser UI and the student's Python code modules.
====================================================================
"""

import os
import sys
import random
import traceback
import re
import subprocess
from flask import Flask, render_template, request, jsonify, session

from pokemon_data import STARTER_TEMPLATES, WILD_TEMPLATES, MOVES, GYMS
from gym import get_all_gyms, get_gym, is_gym_unlocked, create_gym_pokemon, award_gym_rewards, can_catch_pokemon
from team import (
    MAX_PARTY_SIZE,
    can_add_to_party,
    add_to_party,
    remove_from_party,
    get_active_pokemon,
    is_pokemon_conscious,
    get_conscious_pokemon,
    has_conscious_pokemon,
    switch_pokemon,
    swap_party_order,
    heal_party,
    create_team_pokemon,
)

app = Flask(__name__)
app.secret_key = "pikachu-pika-super-secret-key-123"
app.config["TEMPLATES_AUTO_RELOAD"] = True

# In-memory storage for battle sessions
BATTLE_SESSIONS = {}

# Check whether teacher reference solutions are present in the workspace
SOLUTIONS_DIR = os.path.join(os.path.dirname(__file__), "solutions")
HAS_SOLUTIONS = os.path.isfile(os.path.join(SOLUTIONS_DIR, "pokemon.py"))

def extract_student_error(exc, default_file="app.py", default_func="action"):
    """
    Extracts the offending file, function, line number and a student-friendly hint
    from an exception or SyntaxError.
    """
    if isinstance(exc, SyntaxError):
        filename = os.path.basename(exc.filename or default_file)
        lineno = exc.lineno or "?"
        msg = f"Syntax Error on line {lineno}: {exc.msg}"
        hint = f"Check line {lineno} in {filename} for missing colons (:), unclosed parentheses, or quotes!"
        return filename, f"Line {lineno}", msg, hint

    student_files = ("pokemon.py", "starters.py", "battle.py", "catching.py", "poke_type.py")
    tb = exc.__traceback__
    target_file = default_file
    target_func = default_func

    if tb:
        frames = traceback.extract_tb(tb)
        for frame in reversed(frames):
            base = os.path.basename(frame.filename)
            if base in student_files:
                target_file = base
                target_func = frame.name
                break

    msg = str(exc)
    hint = f"Review your code logic in {target_file} around {target_func}!"
    if isinstance(exc, AttributeError):
        hint = "Make sure attributes like 'hp', 'max_hp', or 'name' are set on `self` in __init__!"
    elif isinstance(exc, ZeroDivisionError):
        hint = "Guard against 0 using max(1, ...) to prevent division by zero!"
    elif isinstance(exc, KeyError):
        hint = f"KeyError: check dictionary keys or use .get('{msg}', default) safely!"
    elif isinstance(exc, TypeError) and "NoneType" in msg:
        hint = "Did you forget a `return` statement in one of your functions?"

    return target_file, target_func, msg, hint

def update_session_instances(state, PokemonClass):
    """
    Ensures existing session instances in memory pick up new method definitions
    when student reloads or modifies code.
    """
    targets = [state.get("player"), state.get("enemy")]
    targets.extend(state.get("party", []))
    targets.extend(state.get("storage", []))

    for obj in targets:
        if obj is not None and type(obj) is not PokemonClass:
            try:
                obj.__class__ = PokemonClass
            except Exception:
                pass

def get_modules(use_solution=False):
    """
    Dynamically loads either the student's workspace code
    or the teacher's reference solution.
    """
    if use_solution and HAS_SOLUTIONS:
        import solutions.pokemon as mod_pokemon
        import solutions.starters as mod_starters
        import solutions.battle as mod_battle
        import solutions.catching as mod_catching
        import importlib
        importlib.reload(mod_pokemon)
        importlib.reload(mod_starters)
        importlib.reload(mod_battle)
        importlib.reload(mod_catching)
    else:
        # Reload student modules if they were edited during live share
        import pokemon as mod_pokemon
        import starters as mod_starters
        import battle as mod_battle
        import catching as mod_catching
        import importlib
        importlib.reload(mod_pokemon)
        importlib.reload(mod_starters)
        importlib.reload(mod_battle)
        importlib.reload(mod_catching)

    return {
        "Pokemon": mod_pokemon.Pokemon,
        "create_starter": mod_starters.create_starter,
        "get_type_multiplier": mod_battle.get_type_multiplier,
        "calculate_damage": mod_battle.calculate_damage,
        "choose_enemy_move": mod_battle.choose_enemy_move,
        "attempt_catch": mod_catching.attempt_catch,
    }

def get_session_id():
    if "session_id" not in session:
        session["session_id"] = os.urandom(8).hex()
    return session["session_id"]

def get_session_state(sid):
    if sid not in BATTLE_SESSIONS:
        BATTLE_SESSIONS[sid] = {
            "player": None,
            "enemy": None,
            "party": [],
            "active_index": 0,
            "storage": [],
            "use_solution": False,
            "potions": 3,
            "pokedex": [],
            "badges": [],
            "gym_battle": None,
            "battle_count": 0,
            "status": "STARTER_SELECT"
        }
    state = BATTLE_SESSIONS[sid]
    if "party" not in state:
        state["party"] = [state["player"]] if state.get("player") else []
    if "active_index" not in state:
        state["active_index"] = 0
    if "storage" not in state:
        state["storage"] = []
    if "badges" not in state:
        state["badges"] = []
    if "gym_battle" not in state:
        state["gym_battle"] = None
    return state

def spawn_wild_pokemon(PokemonClass, battle_count=0):
    """
    Creates a random wild Pokémon opponent based on rarity and battle progression.
    Early battles encounter Common & Uncommon Pokémon.
    Milestone battles and higher counts feature Rare, Epic, and Legendary Boss Pokémon!
    """
    common = [p for p in WILD_TEMPLATES if p.get("rarity") == "Common"]
    uncommon = [p for p in WILD_TEMPLATES if p.get("rarity") == "Uncommon"]
    rare = [p for p in WILD_TEMPLATES if p.get("rarity") == "Rare"]
    epic = [p for p in WILD_TEMPLATES if p.get("rarity") == "Epic"]
    boss = [p for p in WILD_TEMPLATES if "Boss" in p.get("rarity", "")]

    # Check for milestone encounters
    if battle_count > 0 and battle_count % 5 == 0:
        candidates = epic + boss
    elif battle_count < 2:
        candidates = common
    elif battle_count < 5:
        candidates = common * 2 + uncommon
    else:
        candidates = common + uncommon * 2 + rare + (epic if battle_count >= 8 else [])

    data = random.choice(candidates if candidates else WILD_TEMPLATES)
    wild_level = min(15, max(3, 3 + (battle_count // 2)))

    enemy = PokemonClass(
        name=data["name"],
        poke_type=data["type"],
        max_hp=data["max_hp"],
        attack=data["attack"],
        defense=data["defense"],
        moves=list(data["moves"]),
        front_sprite=data["front_sprite"],
        back_sprite=data.get("back_sprite", ""),
        level=wild_level
    )
    # Give full HP safely
    if hasattr(enemy, "max_hp"):
        enemy.hp = enemy.max_hp
    elif hasattr(enemy, "hp"):
        enemy.max_hp = enemy.hp
    else:
        enemy.max_hp = data["max_hp"]
        enemy.hp = data["max_hp"]
    return enemy

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/starters", methods=["GET"])
def get_starters():
    """Returns the starter templates for Professor Oak's lab."""
    starters_info = []
    for key, data in STARTER_TEMPLATES.items():
        starters_info.append({
            "id": key,
            "name": data["name"],
            "type": data["type"],
            "hp": data["max_hp"],
            "attack": data["attack"],
            "defense": data["defense"],
            "moves": data["moves"],
            "sprite": data["front_sprite"],
            "description": data["description"]
        })
    return jsonify({
        "success": True,
        "starters": starters_info,
        "moves_database": MOVES,
        "has_solutions": HAS_SOLUTIONS
    })

@app.route("/api/moves", methods=["GET"])
def get_moves():
    """Returns the move catalog containing base power and elemental types."""
    return jsonify({
        "success": True,
        "moves": MOVES
    })

@app.route("/api/choose_starter", methods=["POST"])
def choose_starter():
    sid = get_session_id()
    state = get_session_state(sid)
    data = request.json or {}
    choice = data.get("choice", "pikachu")

    try:
        mods = get_modules(state["use_solution"])
        player_mon = mods["create_starter"](choice)
        if player_mon is None:
            return jsonify({
                "success": False,
                "student_error": True,
                "file": "starters.py",
                "function": "create_starter",
                "message": "create_starter returned None!",
                "hint": "Make sure you instantiate and return a Pokemon object using STARTER_TEMPLATES."
            }), 400

        # Validate that essential attributes exist
        if not hasattr(player_mon, "hp") or not hasattr(player_mon, "name") or not hasattr(player_mon, "max_hp"):
            return jsonify({
                "success": False,
                "student_error": True,
                "file": "pokemon.py",
                "function": "__init__",
                "message": "Pokemon object is missing 'name', 'hp', or 'max_hp' attributes!",
                "hint": "In pokemon.py, ensure __init__ sets `self.name = name`, `self.max_hp = max_hp`, and `self.hp = max_hp`."
            }), 400

        # Reset battle count for fresh adventure
        state["battle_count"] = 0
        enemy_mon = spawn_wild_pokemon(mods["Pokemon"], state["battle_count"])

        state["party"] = [player_mon]
        state["active_index"] = 0
        state["storage"] = []
        state["player"] = player_mon
        state["enemy"] = enemy_mon
        state["potions"] = 3
        state["badges"] = []
        state["gym_battle"] = None
        state["status"] = "BATTLE"
        update_session_instances(state, mods["Pokemon"])

        # Register starter partner in Pokédex
        if player_mon.name not in state["pokedex"]:
            state["pokedex"].append(player_mon.name)

        return jsonify({
            "success": True,
            "player": player_mon.to_dict(),
            "enemy": enemy_mon.to_dict(),
            "party": [m.to_dict() for m in state["party"]],
            "active_index": state["active_index"],
            "storage": [m.to_dict() for m in state["storage"]],
            "potions": state["potions"],
            "badges": state["badges"],
            "pokedex": state["pokedex"],
            "dialogue": [
                f"Professor Oak: Excellent choice! Take good care of {player_mon.name}!",
                f"A wild {enemy_mon.name} appeared!"
            ]
        })

    except Exception as e:
        target_file, target_func, msg, hint = extract_student_error(
            e, default_file="starters.py", default_func="create_starter"
        )
        return jsonify({
            "success": False,
            "student_error": True,
            "file": target_file,
            "function": target_func,
            "message": msg,
            "hint": hint
        }), 400

def award_player_exp(player, exp_amount, state, dialogue_log, events):
    """
    Awards EXP to the player's Pokémon, handling level-ups, stat boosts,
    milestone moves, and evolution.
    """
    old_name = getattr(player, "name", "Pokemon")
    old_level = getattr(player, "level", 5)
    leveled_up = False

    if hasattr(player, "gain_exp"):
        try:
            leveled_up = bool(player.gain_exp(exp_amount))
        except Exception:
            leveled_up = False

    dialogue_log.append(f"{old_name} gained {exp_amount} EXP!")

    new_name = getattr(player, "name", old_name)
    new_level = getattr(player, "level", old_level)
    evolution_occurred = (new_name != old_name)

    evo_info = None
    if evolution_occurred:
        evo_info = {
            "old_name": old_name,
            "new_name": new_name,
            "level": new_level,
            "front_sprite": getattr(player, "front_sprite", ""),
            "back_sprite": getattr(player, "back_sprite", "")
        }
        # Add new evolved form to pokedex
        if "pokedex" in state and new_name not in state["pokedex"]:
            state["pokedex"].append(new_name)

    if leveled_up:
        dialogue_log.append(f"🎉 {new_name} grew to Level {new_level}!")
        events.append({
            "type": "level_up",
            "level": new_level,
            "max_hp": getattr(player, "max_hp", 50),
            "attack": getattr(player, "attack", 40),
            "defense": getattr(player, "defense", 40)
        })

    if evolution_occurred:
        dialogue_log.append(f"✨ What? {old_name} is evolving! ... Congratulations! Your {old_name} evolved into {new_name}!")
        events.append({
            "type": "evolution",
            "old_name": old_name,
            "new_name": new_name,
            "front_sprite": getattr(player, "front_sprite", ""),
            "back_sprite": getattr(player, "back_sprite", "")
        })

    return {
        "exp_gained": exp_amount,
        "leveled_up": leveled_up,
        "evolution": evo_info
    }

@app.route("/api/attack", methods=["POST"])
def attack():
    sid = get_session_id()
    state = get_session_state(sid)
    player = state.get("player")
    enemy = state.get("enemy")

    if not player or not enemy:
        return jsonify({"success": False, "message": "No active battle. Pick a starter first!"}), 400

    data = request.json or {}
    move_name = data.get("move", "Tackle")

    try:
        mods = get_modules(state["use_solution"])
        update_session_instances(state, mods["Pokemon"])

        dialogue_log = []
        events = []

        # 1. PLAYER'S TURN
        dmg_result = mods["calculate_damage"](move_name, player, enemy)
        if dmg_result is None:
            return jsonify({
                "success": False,
                "student_error": True,
                "file": "battle.py",
                "function": "calculate_damage",
                "message": "calculate_damage returned None!",
                "hint": "Did you forget `return final_damage, is_critical, type_multiplier` at the end of calculate_damage()?"
            }), 400

        if not isinstance(dmg_result, (tuple, list)) or len(dmg_result) < 3:
            return jsonify({
                "success": False,
                "student_error": True,
                "file": "battle.py",
                "function": "calculate_damage",
                "message": f"calculate_damage returned {dmg_result} instead of a 3-item tuple!",
                "hint": "Return a tuple: `return damage, is_critical, type_multiplier`."
            }), 400

        p_dmg, p_crit, p_mult = dmg_result[0], dmg_result[1], dmg_result[2]
        enemy.take_damage(p_dmg)

        msg = f"{player.name} used {move_name}!"
        if p_crit:
            msg += " Critical hit!"
        if p_mult > 1.0:
            msg += " It's super effective!"
        elif p_mult < 1.0:
            msg += " It's not very effective..."
        msg += f" Dealt {p_dmg} damage!"
        dialogue_log.append(msg)

        events.append({
            "type": "player_attack",
            "move": move_name,
            "damage": p_dmg,
            "is_critical": p_crit,
            "multiplier": p_mult,
            "enemy_hp": getattr(enemy, "hp", 0)
        })

        # Check if enemy fainted
        enemy_fainted = bool(enemy.is_fainted()) if (hasattr(enemy, "is_fainted") and enemy.is_fainted() is not None) else (getattr(enemy, "hp", 1) <= 0)
        if enemy_fainted:
            gym_battle = state.get("gym_battle")
            if gym_battle:
                idx = gym_battle.get("pokemon_index", 0)
                team = gym_battle.get("team", [])
                leader = gym_battle.get("leader", "Gym Leader")

                # If leader has another Pokémon in their team:
                if idx + 1 < len(team):
                    gym_battle["pokemon_index"] = idx + 1
                    next_mon_data = team[idx + 1]
                    next_enemy = create_gym_pokemon(mods["Pokemon"], next_mon_data)
                    state["enemy"] = next_enemy

                    dialogue_log.append(f"Leader {leader}'s {enemy.name} fainted!")
                    dialogue_log.append(f"Gym Leader {leader}: \"Go, {next_enemy.name}!\"")
                    events.append({"type": "enemy_faint"})
                    events.append({
                        "type": "gym_next_mon",
                        "leader": leader,
                        "enemy": next_enemy.to_dict()
                    })

                    exp_data = award_player_exp(player, 60, state, dialogue_log, events)

                    return jsonify({
                        "success": True,
                        "player": player.to_dict(),
                        "enemy": next_enemy.to_dict(),
                        "pokedex": state.get("pokedex", []),
                        "dialogue": dialogue_log,
                        "events": events,
                        "battle_over": False,
                        "is_gym_battle": True,
                        "gym_pokemon_index": idx + 1,
                        "gym_pokemon_total": len(team),
                        "exp_gained": exp_data["exp_gained"],
                        "leveled_up": exp_data["leveled_up"],
                        "evolution": exp_data["evolution"]
                    })
                else:
                    # Final gym leader Pokémon defeated!
                    rewards = award_gym_rewards(gym_battle["gym_id"], state)
                    dialogue_log.append(f"Leader {leader}'s {enemy.name} fainted!")
                    dialogue_log.append(f"Leader {leader}: \"{rewards['defeat_dialogue']}\"")
                    if rewards["is_first_time"]:
                        dialogue_log.append(f"🏆 You earned the {rewards['badge_name']} {rewards['badge_icon']}!")
                    dialogue_log.append(f"Received +{rewards['potions']} Potions as a reward!")

                    events.append({"type": "enemy_faint"})
                    events.append({
                        "type": "badge_earned",
                        "badge_id": rewards["badge_id"],
                        "badge_name": rewards["badge_name"],
                        "badge_icon": rewards["badge_icon"],
                        "leader": leader
                    })

                    state["gym_battle"] = None
                    state["status"] = "BATTLE_VICTORY"
                    state["battle_count"] += 1

                    exp_data = award_player_exp(player, rewards["exp"], state, dialogue_log, events)

                    return jsonify({
                        "success": True,
                        "player": player.to_dict(),
                        "enemy": enemy.to_dict(),
                        "pokedex": state.get("pokedex", []),
                        "badges": state.get("badges", []),
                        "potions": state.get("potions", 3),
                        "dialogue": dialogue_log,
                        "events": events,
                        "battle_over": True,
                        "victory": True,
                        "is_gym_victory": True,
                        "badge_earned": rewards["badge_name"],
                        "badge_icon": rewards["badge_icon"],
                        "leader": leader,
                        "exp_gained": exp_data["exp_gained"],
                        "leveled_up": exp_data["leveled_up"],
                        "evolution": exp_data["evolution"]
                    })

            # Normal wild battle victory
            dialogue_log.append(f"Wild {enemy.name} fainted! You won the battle!")
            events.append({"type": "enemy_faint"})
            state["battle_count"] += 1

            exp_amount = 120 if getattr(enemy, "name", "") in ["Mewtwo", "Dragonite"] else 60
            exp_data = award_player_exp(player, exp_amount, state, dialogue_log, events)

            return jsonify({
                "success": True,
                "player": player.to_dict(),
                "enemy": enemy.to_dict(),
                "pokedex": state.get("pokedex", []),
                "dialogue": dialogue_log,
                "events": events,
                "battle_over": True,
                "victory": True,
                "exp_gained": exp_data["exp_gained"],
                "leveled_up": exp_data["leveled_up"],
                "evolution": exp_data["evolution"]
            })

        # 2. ENEMY'S TURN
        e_move = mods["choose_enemy_move"](enemy)
        if not e_move:
            e_move = "Tackle"

        e_result = mods["calculate_damage"](e_move, enemy, player)
        if e_result is None or not isinstance(e_result, (tuple, list)) or len(e_result) < 3:
            e_dmg, e_crit, e_mult = 10, False, 1.0
        else:
            e_dmg, e_crit, e_mult = e_result[0], e_result[1], e_result[2]

        player.take_damage(e_dmg)

        gym_battle = state.get("gym_battle")
        if gym_battle:
            e_prefix = f"Leader {gym_battle['leader']}'s {enemy.name}"
        else:
            e_prefix = f"Wild {enemy.name}"

        e_msg = f"{e_prefix} used {e_move}!"
        if e_crit:
            e_msg += " Critical hit!"
        if e_mult > 1.0:
            e_msg += " It's super effective!"
        elif e_mult < 1.0:
            e_msg += " It's not very effective..."
        e_msg += f" Dealt {e_dmg} damage to {player.name}!"
        dialogue_log.append(e_msg)

        events.append({
            "type": "enemy_attack",
            "move": e_move,
            "damage": e_dmg,
            "is_critical": e_crit,
            "multiplier": e_mult,
            "player_hp": getattr(player, "hp", 0)
        })

        # Check if active player fainted
        player_fainted = bool(player.is_fainted()) if (hasattr(player, "is_fainted") and player.is_fainted() is not None) else (getattr(player, "hp", 1) <= 0)
        switch_required = False
        all_fainted = False

        if player_fainted:
            events.append({"type": "player_faint"})
            party = state.get("party", [player])
            if has_conscious_pokemon(party):
                switch_required = True
                dialogue_log.append(f"{player.name} fainted! Choose your next Pokémon!")
            else:
                all_fainted = True
                if gym_battle:
                    dialogue_log.append(f"{player.name} fainted! All your Pokémon fainted! Leader {gym_battle['leader']} won the match!")
                    state["gym_battle"] = None
                else:
                    dialogue_log.append(f"{player.name} fainted! All your Pokémon fainted! You rushed back to the Pokémon Center.")
                heal_party(party)

        return jsonify({
            "success": True,
            "player": player.to_dict(),
            "enemy": enemy.to_dict(),
            "party": [m.to_dict() for m in state.get("party", [])],
            "active_index": state.get("active_index", 0),
            "dialogue": dialogue_log,
            "events": events,
            "battle_over": all_fainted,
            "switch_required": switch_required,
            "victory": False
        })

    except Exception as e:
        target_file, target_func, msg, hint = extract_student_error(
            e, default_file="battle.py", default_func="calculate_damage"
        )
        return jsonify({
            "success": False,
            "student_error": True,
            "file": target_file,
            "function": target_func,
            "message": msg,
            "hint": hint
        }), 400

@app.route("/api/item", methods=["POST"])
def use_item():
    sid = get_session_id()
    state = get_session_state(sid)
    player = state.get("player")
    enemy = state.get("enemy")

    if not player or not enemy:
        return jsonify({"success": False, "message": "No active battle!"}), 400

    if state.get("potions", 0) <= 0:
        return jsonify({"success": False, "message": "You have no Potions left!"}), 400

    try:
        mods = get_modules(state["use_solution"])
        update_session_instances(state, mods["Pokemon"])

        # Check if already full HP
        cur_hp = getattr(player, "hp", 50)
        max_hp = getattr(player, "max_hp", 50)
        if cur_hp >= max_hp:
            return jsonify({
                "success": True,
                "player": player.to_dict(),
                "enemy": enemy.to_dict(),
                "potions": state["potions"],
                "dialogue": [f"{player.name} is already at full health!"],
                "events": [],
                "battle_over": False
            })

        # Use potion (+25 HP)
        state["potions"] -= 1
        old_hp = cur_hp
        player.heal(25)
        healed_amount = max(0, getattr(player, "hp", old_hp) - old_hp)

        dialogue_log = [f"Used a Potion! {player.name} recovered {healed_amount} HP!"]
        events = [{"type": "heal", "healed": healed_amount, "player_hp": player.hp}]

        # Enemy retaliates
        e_move = mods["choose_enemy_move"](enemy)
        if not e_move:
            e_move = "Tackle"

        e_result = mods["calculate_damage"](e_move, enemy, player)
        if e_result and isinstance(e_result, (tuple, list)) and len(e_result) >= 3:
            e_dmg, e_crit, e_mult = e_result[0], e_result[1], e_result[2]
        else:
            e_dmg, e_crit, e_mult = 8, False, 1.0

        player.take_damage(e_dmg)
        dialogue_log.append(f"Wild {enemy.name} used {e_move} while you healed! Dealt {e_dmg} damage.")
        events.append({
            "type": "enemy_attack",
            "move": e_move,
            "damage": e_dmg,
            "is_critical": e_crit,
            "multiplier": e_mult,
            "player_hp": getattr(player, "hp", 0)
        })

        player_fainted = bool(player.is_fainted()) if (hasattr(player, "is_fainted") and player.is_fainted() is not None) else (getattr(player, "hp", 1) <= 0)
        switch_required = False
        all_fainted = False

        if player_fainted:
            events.append({"type": "player_faint"})
            party = state.get("party", [player])
            if has_conscious_pokemon(party):
                switch_required = True
                dialogue_log.append(f"{player.name} fainted! Choose your next Pokémon!")
            else:
                all_fainted = True
                state["gym_battle"] = None
                dialogue_log.append(f"{player.name} fainted! All your Pokémon fainted! You rushed back to the Pokémon Center.")
                heal_party(party)

        return jsonify({
            "success": True,
            "player": player.to_dict(),
            "enemy": enemy.to_dict(),
            "party": [m.to_dict() for m in state.get("party", [])],
            "active_index": state.get("active_index", 0),
            "potions": state["potions"],
            "dialogue": dialogue_log,
            "events": events,
            "battle_over": all_fainted,
            "switch_required": switch_required
        })

    except Exception as e:
        target_file, target_func, msg, hint = extract_student_error(
            e, default_file="pokemon.py", default_func="heal"
        )
        return jsonify({
            "success": False,
            "student_error": True,
            "file": target_file,
            "function": target_func,
            "message": msg,
            "hint": hint
        }), 400

@app.route("/api/catch", methods=["POST"])
def catch():
    sid = get_session_id()
    state = get_session_state(sid)
    enemy = state.get("enemy")
    player = state.get("player")

    if not enemy or not player:
        return jsonify({"success": False, "message": "No wild Pokémon to catch!"}), 400

    gym_battle = state.get("gym_battle")
    if gym_battle:
        return jsonify({
            "success": False,
            "gym_catch_blocked": True,
            "message": "You can't catch a Gym Leader's Pokémon! That's against Pokémon League rules!"
        }), 400

    data = request.json or {}
    ball_type = data.get("ball_type", "poke-ball")

    try:
        mods = get_modules(state["use_solution"])
        update_session_instances(state, mods["Pokemon"])

        catch_result = mods["attempt_catch"](enemy, ball_type)
        if catch_result is None:
            return jsonify({
                "success": False,
                "student_error": True,
                "file": "catching.py",
                "function": "attempt_catch",
                "message": "attempt_catch returned None!",
                "hint": "Did you forget `return caught, shakes` inside attempt_catch()?"
            }), 400

        if not isinstance(catch_result, (tuple, list)) or len(catch_result) < 2:
            return jsonify({
                "success": False,
                "student_error": True,
                "file": "catching.py",
                "function": "attempt_catch",
                "message": f"attempt_catch returned {catch_result} instead of (caught, shakes)!",
                "hint": "Make sure you return `(caught_boolean, shakes_integer)`."
            }), 400

        caught, shakes = catch_result[0], catch_result[1]

        dialogue = []
        events = [{"type": "throw_ball", "ball": ball_type, "shakes": shakes, "caught": caught}]

        if caught:
            dialogue.append(f"Gotcha! Wild {enemy.name} was caught!")
            if can_add_to_party(state.get("party", [])):
                add_to_party(state["party"], enemy)
                dialogue.append(f"{enemy.name} joined your battle party! ({len(state['party'])}/4 Pokémon)")
            else:
                state["storage"].append(enemy)
                dialogue.append(f"{enemy.name} was sent to your PC Storage box!")

            if enemy.name not in state["pokedex"]:
                state["pokedex"].append(enemy.name)
            state["battle_count"] += 1

            exp_amount = 120 if getattr(enemy, "name", "") == "Mewtwo" else 60
            exp_data = award_player_exp(player, exp_amount, state, dialogue, events)

            return jsonify({
                "success": True,
                "caught": True,
                "shakes": shakes,
                "player": player.to_dict(),
                "party": [m.to_dict() for m in state.get("party", [])],
                "active_index": state.get("active_index", 0),
                "storage": [m.to_dict() for m in state.get("storage", [])],
                "pokedex": state["pokedex"],
                "dialogue": dialogue,
                "events": events,
                "battle_over": True,
                "victory": True,
                "exp_gained": exp_data["exp_gained"],
                "leveled_up": exp_data["leveled_up"],
                "evolution": exp_data["evolution"]
            })
        else:
            if shakes == 0:
                dialogue.append(f"Oh no! The Pokémon broke free right away!")
            elif shakes == 1:
                dialogue.append(f"Aww! It appeared to be caught!")
            elif shakes == 2:
                dialogue.append(f"Aargh! Almost had it!")
            else:
                dialogue.append(f"Shoot! It was so close, too!")

            # Enemy attacks back if escape
            e_move = mods["choose_enemy_move"](enemy)
            if not e_move:
                e_move = "Tackle"

            e_result = mods["calculate_damage"](e_move, enemy, player)
            if e_result and isinstance(e_result, (tuple, list)) and len(e_result) >= 3:
                e_dmg, e_crit, e_mult = e_result[0], e_result[1], e_result[2]
            else:
                e_dmg, e_crit, e_mult = 8, False, 1.0

            player.take_damage(e_dmg)
            dialogue.append(f"Wild {enemy.name} used {e_move}! Dealt {e_dmg} damage.")
            events.append({
                "type": "enemy_attack",
                "move": e_move,
                "damage": e_dmg,
                "is_critical": e_crit,
                "multiplier": e_mult,
                "player_hp": getattr(player, "hp", 0)
            })

            player_fainted = bool(player.is_fainted()) if (hasattr(player, "is_fainted") and player.is_fainted() is not None) else (getattr(player, "hp", 1) <= 0)
            switch_required = False
            all_fainted = False

            if player_fainted:
                events.append({"type": "player_faint"})
                party = state.get("party", [player])
                if has_conscious_pokemon(party):
                    switch_required = True
                    dialogue.append(f"{player.name} fainted! Choose your next Pokémon!")
                else:
                    all_fainted = True
                    dialogue.append(f"{player.name} fainted! All your Pokémon fainted! You rushed back to the Pokémon Center.")
                    heal_party(party)

            return jsonify({
                "success": True,
                "caught": False,
                "shakes": shakes,
                "player": player.to_dict(),
                "enemy": enemy.to_dict(),
                "party": [m.to_dict() for m in state.get("party", [])],
                "active_index": state.get("active_index", 0),
                "dialogue": dialogue,
                "events": events,
                "battle_over": all_fainted,
                "switch_required": switch_required
            })

    except Exception as e:
        target_file, target_func, msg, hint = extract_student_error(
            e, default_file="catching.py", default_func="attempt_catch"
        )
        return jsonify({
            "success": False,
            "student_error": True,
            "file": target_file,
            "function": target_func,
            "message": msg,
            "hint": hint
        }), 400

@app.route("/api/next_battle", methods=["POST"])
def next_battle():
    sid = get_session_id()
    state = get_session_state(sid)
    player = state.get("player")

    if not player:
        return jsonify({"success": False, "message": "No player found"}), 400

    try:
        mods = get_modules(state["use_solution"])
        update_session_instances(state, mods["Pokemon"])

        party = state.get("party", [])
        if not has_conscious_pokemon(party):
            heal_party(party)
            state["active_index"] = 0
            state["player"] = party[0] if party else None
        else:
            cur_active = party[state.get("active_index", 0)] if party else None
            if not is_pokemon_conscious(cur_active):
                for idx, mon in enumerate(party):
                    if is_pokemon_conscious(mon):
                        state["active_index"] = idx
                        state["player"] = mon
                        break
            if state.get("player"):
                state["player"].heal(15)

        player = state.get("player")
        enemy_mon = spawn_wild_pokemon(mods["Pokemon"], state["battle_count"])
        state["enemy"] = enemy_mon
        state["gym_battle"] = None
        state["status"] = "BATTLE"

        boss_tag = " [BOSS BATTLE!]" if getattr(enemy_mon, "name", "") in ["Mewtwo", "Dragonite"] or (state["battle_count"] > 0 and state["battle_count"] % 5 == 0) else ""

        return jsonify({
            "success": True,
            "player": player.to_dict(),
            "enemy": enemy_mon.to_dict(),
            "party": [m.to_dict() for m in state.get("party", [])],
            "active_index": state.get("active_index", 0),
            "battle_count": state["battle_count"],
            "pokedex": state["pokedex"],
            "badges": state.get("badges", []),
            "dialogue": [f"A wild {enemy_mon.name}{boss_tag} appeared!"]
        })

    except Exception as e:
        target_file, target_func, msg, hint = extract_student_error(
            e, default_file="battle.py", default_func="next_battle"
        )
        return jsonify({
            "success": False,
            "student_error": True,
            "file": target_file,
            "function": target_func,
            "message": msg,
            "hint": hint
        }), 400

@app.route("/api/party", methods=["GET"])
def get_party():
    """Returns the trainer's 4-Pokémon active party and PC storage."""
    sid = get_session_id()
    state = get_session_state(sid)
    mods = get_modules(state["use_solution"])
    update_session_instances(state, mods["Pokemon"])

    party_data = [m.to_dict() for m in state.get("party", []) if m is not None]
    storage_data = [m.to_dict() for m in state.get("storage", []) if m is not None]

    return jsonify({
        "success": True,
        "party": party_data,
        "active_index": state.get("active_index", 0),
        "storage": storage_data,
        "pokedex": state.get("pokedex", [])
    })

@app.route("/api/switch_pokemon", methods=["POST"])
def switch_pokemon_route():
    """
    Handles switching Pokémon in battle.
    - Voluntary switch (during move turn): uses player's turn, opponent attacks incoming Pokémon!
    - Forced switch (after faint): cleanly sends out replacement Pokémon.
    """
    sid = get_session_id()
    state = get_session_state(sid)
    party = state.get("party", [])
    active_idx = state.get("active_index", 0)
    enemy = state.get("enemy")

    if not party:
        return jsonify({"success": False, "message": "No Pokémon in party!"}), 400

    data = request.json or {}
    target_idx = data.get("target_index")
    is_voluntary = bool(data.get("is_voluntary", True))

    if target_idx is None:
        return jsonify({"success": False, "message": "Missing target_index"}), 400

    try:
        mods = get_modules(state["use_solution"])
        update_session_instances(state, mods["Pokemon"])

        success, new_idx, msg = switch_pokemon(party, active_idx, target_idx)
        if not success:
            return jsonify({"success": False, "message": msg}), 400

        old_mon = party[active_idx]
        state["active_index"] = new_idx
        state["player"] = party[new_idx]
        new_mon = state["player"]

        dialogue_log = []
        events = []

        if is_voluntary:
            dialogue_log.append(f"Trainer withdrew {old_mon.name}! Go, {new_mon.name}!")
            events.append({
                "type": "player_switch",
                "old_pokemon": old_mon.to_dict(),
                "new_pokemon": new_mon.to_dict()
            })

            # Voluntary switch costs the player's turn! Opponent attacks incoming Pokémon.
            if enemy and not (enemy.is_fainted() if hasattr(enemy, "is_fainted") else getattr(enemy, "hp", 1) <= 0):
                e_move = mods["choose_enemy_move"](enemy)
                if not e_move:
                    e_move = "Tackle"

                e_result = mods["calculate_damage"](e_move, enemy, new_mon)
                if e_result and isinstance(e_result, (tuple, list)) and len(e_result) >= 3:
                    e_dmg, e_crit, e_mult = e_result[0], e_result[1], e_result[2]
                else:
                    e_dmg, e_crit, e_mult = 10, False, 1.0

                new_mon.take_damage(e_dmg)

                gym_battle = state.get("gym_battle")
                e_prefix = f"Leader {gym_battle['leader']}'s {enemy.name}" if gym_battle else f"Wild {enemy.name}"
                e_msg = f"{e_prefix} used {e_move}!"
                if e_crit:
                    e_msg += " Critical hit!"
                if e_mult > 1.0:
                    e_msg += " It's super effective!"
                elif e_mult < 1.0:
                    e_msg += " It's not very effective..."
                e_msg += f" Dealt {e_dmg} damage to incoming {new_mon.name}!"
                dialogue_log.append(e_msg)

                events.append({
                    "type": "enemy_attack",
                    "move": e_move,
                    "damage": e_dmg,
                    "is_critical": e_crit,
                    "multiplier": e_mult,
                    "player_hp": getattr(new_mon, "hp", 0)
                })

                incoming_fainted = bool(new_mon.is_fainted()) if (hasattr(new_mon, "is_fainted") and new_mon.is_fainted() is not None) else (getattr(new_mon, "hp", 1) <= 0)
                if incoming_fainted:
                    events.append({"type": "player_faint"})
                    if has_conscious_pokemon(party):
                        dialogue_log.append(f"{new_mon.name} fainted! Choose your next Pokémon!")
                        return jsonify({
                            "success": True,
                            "player": new_mon.to_dict(),
                            "enemy": enemy.to_dict(),
                            "party": [m.to_dict() for m in party],
                            "active_index": state["active_index"],
                            "dialogue": dialogue_log,
                            "events": events,
                            "battle_over": False,
                            "switch_required": True
                        })
                    else:
                        dialogue_log.append(f"{new_mon.name} fainted! All your Pokémon fainted! You rushed back to the Pokémon Center.")
                        heal_party(party)
                        return jsonify({
                            "success": True,
                            "player": new_mon.to_dict(),
                            "enemy": enemy.to_dict(),
                            "party": [m.to_dict() for m in party],
                            "active_index": state["active_index"],
                            "dialogue": dialogue_log,
                            "events": events,
                            "battle_over": True,
                            "switch_required": False
                        })
        else:
            # Forced switch after faint - clean entrance without free enemy hit
            dialogue_log.append(f"Go, {new_mon.name}!")
            events.append({
                "type": "player_send_out",
                "pokemon": new_mon.to_dict()
            })

        return jsonify({
            "success": True,
            "player": new_mon.to_dict(),
            "enemy": enemy.to_dict() if enemy else None,
            "party": [m.to_dict() for m in party],
            "active_index": state["active_index"],
            "dialogue": dialogue_log,
            "events": events,
            "battle_over": False,
            "switch_required": False
        })

    except Exception as e:
        target_file, target_func, msg, hint = extract_student_error(e, default_file="team.py", default_func="switch_pokemon")
        return jsonify({
            "success": False,
            "student_error": True,
            "file": target_file,
            "function": target_func,
            "message": msg,
            "hint": hint
        }), 400

@app.route("/api/team/manage", methods=["POST"])
def manage_team():
    """Allows trainers to manage their 4-Pokémon party, withdraw, deposit, or heal."""
    sid = get_session_id()
    state = get_session_state(sid)
    data = request.json or {}
    action = data.get("action", "")

    mods = get_modules(state["use_solution"])
    update_session_instances(state, mods["Pokemon"])
    party = state.get("party", [])
    storage = state.get("storage", [])

    if action == "add_from_pokedex":
        species = data.get("species", "")
        if not can_add_to_party(party):
            return jsonify({"success": False, "message": "Your battle party is already full (4/4)! Deposit or swap a Pokémon first."}), 400

        lead_level = getattr(state.get("player"), "level", 5)
        new_mon = create_team_pokemon(mods["Pokemon"], species, level=lead_level)
        add_to_party(party, new_mon)
        if species not in state.get("pokedex", []):
            state["pokedex"].append(species)

        return jsonify({
            "success": True,
            "party": [m.to_dict() for m in party],
            "active_index": state.get("active_index", 0),
            "storage": [m.to_dict() for m in storage],
            "pokedex": state.get("pokedex", []),
            "message": f"{new_mon.name} joined your battle party!"
        })

    elif action == "swap_slots":
        idx1 = data.get("index1", 0)
        idx2 = data.get("index2", 1)
        if swap_party_order(party, idx1, idx2):
            if state["active_index"] == idx1:
                state["active_index"] = idx2
            elif state["active_index"] == idx2:
                state["active_index"] = idx1
            state["player"] = party[state["active_index"]]
            return jsonify({
                "success": True,
                "party": [m.to_dict() for m in party],
                "active_index": state["active_index"],
                "player": state["player"].to_dict()
            })
        return jsonify({"success": False, "message": "Failed to swap slots"}), 400

    elif action == "deposit":
        idx = data.get("index", -1)
        removed = remove_from_party(party, idx)
        if removed:
            storage.append(removed)
            if state["active_index"] >= len(party):
                state["active_index"] = 0
            state["player"] = party[state["active_index"]]
            return jsonify({
                "success": True,
                "party": [m.to_dict() for m in party],
                "active_index": state["active_index"],
                "storage": [m.to_dict() for m in storage],
                "player": state["player"].to_dict(),
                "message": f"{removed.name} moved to PC Storage."
            })
        return jsonify({"success": False, "message": "Cannot deposit your only Pokémon!"}), 400

    elif action == "withdraw":
        s_idx = data.get("storage_index", -1)
        if not can_add_to_party(party):
            return jsonify({"success": False, "message": "Battle party is full (4/4)!"}), 400
        if 0 <= s_idx < len(storage):
            mon = storage.pop(s_idx)
            add_to_party(party, mon)
            return jsonify({
                "success": True,
                "party": [m.to_dict() for m in party],
                "active_index": state["active_index"],
                "storage": [m.to_dict() for m in storage],
                "message": f"{mon.name} joined your active party!"
            })
        return jsonify({"success": False, "message": "Invalid storage index"}), 400

    elif action == "heal_all":
        heal_party(party)
        heal_party(storage)
        return jsonify({
            "success": True,
            "party": [m.to_dict() for m in party],
            "active_index": state["active_index"],
            "player": state["player"].to_dict() if state.get("player") else None,
            "message": "Nurse Joy fully healed your entire team!"
        })

    return jsonify({"success": False, "message": f"Unknown action: {action}"}), 400

@app.route("/api/toggle_mode", methods=["POST"])
def toggle_mode():
    sid = get_session_id()
    state = get_session_state(sid)
    data = request.json or {}
    target_solution = bool(data.get("use_solution", not state["use_solution"]))

    if target_solution and not HAS_SOLUTIONS:
        return jsonify({
            "success": False,
            "use_solution": False,
            "message": "Teacher reference solutions are not included in this student repository."
        }), 400

    state["use_solution"] = target_solution
    mode_name = "Teacher Reference Solutions" if target_solution else "Student Code Workspace"
    return jsonify({
        "success": True,
        "use_solution": target_solution,
        "mode_name": mode_name
    })

# ====================================================================
# GYM PROGRESSION ROUTES
# ====================================================================

@app.route("/api/gyms", methods=["GET"])
def get_gyms():
    sid = get_session_id()
    state = get_session_state(sid)
    badges = set(state.get("badges", []))

    gyms_list = []
    for g in get_all_gyms():
        unlocked = is_gym_unlocked(g["id"], badges)
        defeated = g["badge_id"] in badges
        gyms_list.append({
            "id": g["id"],
            "name": g["name"],
            "city": g["city"],
            "leader": g["leader"],
            "title": g["title"],
            "badge_id": g["badge_id"],
            "badge_name": g["badge_name"],
            "badge_icon": g["badge_icon"],
            "type": g["type"],
            "recommended_level": g["recommended_level"],
            "is_unlocked": unlocked,
            "is_defeated": defeated,
            "team_count": len(g["team"]),
            "dialogue_intro": g["dialogue_intro"],
            "reward_exp": g["reward_exp"],
            "reward_potions": g.get("reward_potions", 2),
            "team_preview": [{"name": m["name"], "level": m["level"], "type": m["type"]} for m in g["team"]]
        })

    return jsonify({
        "success": True,
        "gyms": gyms_list,
        "badges": list(badges)
    })

@app.route("/api/gym/challenge", methods=["POST"])
def gym_challenge():
    sid = get_session_id()
    state = get_session_state(sid)
    player = state.get("player")
    if not player:
        return jsonify({"success": False, "message": "Please choose a starter Pokémon first!"}), 400

    data = request.json or {}
    gym_id = data.get("gym_id")

    gym = get_gym(gym_id)
    if not gym:
        return jsonify({"success": False, "message": f"Gym '{gym_id}' not found!"}), 404

    badges = set(state.get("badges", []))
    if not is_gym_unlocked(gym_id, badges):
        return jsonify({"success": False, "message": "This Gym is locked! Defeat previous Gym Leaders first."}), 400

    try:
        mods = get_modules(state["use_solution"])
        update_session_instances(state, mods["Pokemon"])

        # Revive/heal party if all fainted, or ensure active is conscious
        party = state.get("party", [player])
        if not has_conscious_pokemon(party):
            heal_party(party)
            state["active_index"] = 0
            state["player"] = party[0]
        else:
            cur_active = party[state.get("active_index", 0)] if party else None
            if not is_pokemon_conscious(cur_active):
                for idx, mon in enumerate(party):
                    if is_pokemon_conscious(mon):
                        state["active_index"] = idx
                        state["player"] = mon
                        break
        player = state.get("player")

        # First gym pokemon
        first_mon_data = gym["team"][0]
        enemy_mon = create_gym_pokemon(mods["Pokemon"], first_mon_data)

        state["enemy"] = enemy_mon
        state["gym_battle"] = {
            "gym_id": gym["id"],
            "leader": gym["leader"],
            "badge_id": gym["badge_id"],
            "badge_name": gym["badge_name"],
            "badge_icon": gym["badge_icon"],
            "pokemon_index": 0,
            "team": gym["team"],
            "reward_exp": gym["reward_exp"],
            "reward_potions": gym.get("reward_potions", 2),
            "dialogue_defeat": gym["dialogue_defeat"]
        }
        state["status"] = "GYM_BATTLE"

        dialogue = [
            f"You entered {gym['name']} in {gym['city']}!",
            f"Gym Leader {gym['leader']}: \"{gym['dialogue_intro']}\"",
            f"Leader {gym['leader']} sent out {enemy_mon.name} (Lv. {getattr(enemy_mon, 'level', first_mon_data['level'])})!"
        ]

        return jsonify({
            "success": True,
            "player": player.to_dict(),
            "enemy": enemy_mon.to_dict(),
            "party": [m.to_dict() for m in state.get("party", [])],
            "active_index": state.get("active_index", 0),
            "gym": {
                "id": gym["id"],
                "leader": gym["leader"],
                "badge_name": gym["badge_name"],
                "badge_icon": gym["badge_icon"],
                "team_count": len(gym["team"]),
                "current_index": 0
            },
            "dialogue": dialogue,
            "is_gym_battle": True
        })

    except Exception as e:
        target_file, target_func, msg, hint = extract_student_error(
            e, default_file="gym.py", default_func="gym_challenge"
        )
        return jsonify({
            "success": False,
            "student_error": True,
            "file": target_file,
            "function": target_func,
            "message": msg,
            "hint": hint
        }), 400

# ====================================================================
# PROGRESSION & MISSION CODE TEST RUNNER
# ====================================================================

def get_code_progress(use_solutions=False):
    """
    Executes all mission test suites in isolated subprocesses and parses
    test pass/fail counts, descriptions, and hints.
    """
    test_specs = [
        {"id": "m1", "name": "Mission 1: Pokemon Class", "file": "pokemon.py", "script": "tests/test_pokemon.py", "concept": "Classes, __init__, and self"},
        {"id": "m2", "name": "Mission 2: Starter Lab", "file": "starters.py", "script": "tests/test_starters.py", "concept": "Dictionaries, Strings, and Factories"},
        {"id": "m3", "name": "Mission 3: Battle Engine", "file": "battle.py", "script": "tests/test_battle.py", "concept": "Damage Formula, Tuples, and AI"},
        {"id": "m4", "name": "Mission 4: Safari Catching", "file": "catching.py", "script": "tests/test_catching.py", "concept": "Probabilities, Clamping, and Ball Shakes"},
        {"id": "m5", "name": "Mission 5: Level Up & Evolution", "file": "pokemon.py", "script": "tests/test_progression.py", "concept": "EXP Gain, Stat Growth, and Evolution"},
        {"id": "bonus", "name": "Bonus: Elemental Type System", "file": "poke_type.py", "script": "tests/test_poke_type.py", "concept": "Type Object Pattern and Matchups"}
    ]

    env = dict(os.environ)
    env["USE_SOLUTIONS"] = "1" if use_solutions else "0"

    missions_result = []
    total_tests_passed = 0
    total_tests_count = 0
    missions_completed_count = 0

    for spec in test_specs:
        script_path = os.path.join(os.path.dirname(__file__), spec["script"])
        try:
            res = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                env=env,
                timeout=6
            )
            stdout = res.stdout
            lines = stdout.splitlines()

            pass_items = [l.strip() for l in lines if "[PASS]" in l]
            fail_items = [l.strip() for l in lines if "[FAIL]" in l]
            hint_items = [l.strip() for l in lines if "Hint:" in l]

            score_match = re.search(r"Score:\s*(\d+)/(\d+)\s+tests passed", stdout, re.IGNORECASE)
            if score_match:
                passed_num = int(score_match.group(1))
                total_num = int(score_match.group(2))
            else:
                passed_num = len(pass_items)
                total_num = len(pass_items) + len(fail_items)

            is_completed = (res.returncode == 0) and (passed_num == total_num) and (total_num > 0)
            if is_completed:
                missions_completed_count += 1

            total_tests_passed += passed_num
            total_tests_count += total_num

            missions_result.append({
                "id": spec["id"],
                "name": spec["name"],
                "file": spec["file"],
                "concept": spec["concept"],
                "completed": is_completed,
                "passed": passed_num,
                "total": total_num,
                "pass_items": pass_items,
                "fail_items": fail_items,
                "hint_items": hint_items,
            })
        except Exception as exc:
            missions_result.append({
                "id": spec["id"],
                "name": spec["name"],
                "file": spec["file"],
                "concept": spec["concept"],
                "completed": False,
                "passed": 0,
                "total": 1,
                "pass_items": [],
                "fail_items": [f"[FAIL] Error running tests: {str(exc)}"],
                "hint_items": []
            })

    return {
        "missions": missions_result,
        "missions_completed": missions_completed_count,
        "total_missions": len(test_specs),
        "total_tests_passed": total_tests_passed,
        "total_tests_count": total_tests_count,
        "percent_completed": round((missions_completed_count / len(test_specs)) * 100, 1),
        "use_solutions": use_solutions
    }

@app.route("/progress")
def progress_page():
    """Serves the Progress dashboard webpage."""
    return render_template("progress.html")

@app.route("/api/progress", methods=["GET"])
def get_progress():
    """
    Returns both Code Progress (automated test suite results) and
    Game Progress (player partner, gym badges, Pokédex, battles).
    """
    sid = get_session_id()
    state = get_session_state(sid)

    use_sol_param = request.args.get("use_solution")
    if use_sol_param is not None:
        use_solutions = use_sol_param in ("1", "true", "True")
    else:
        use_solutions = state.get("use_solution", False)

    code_data = get_code_progress(use_solutions)

    player = state.get("player")
    badges = state.get("badges", [])

    all_gyms = []
    for g in get_all_gyms():
        all_gyms.append({
            "id": g["id"],
            "name": g["name"],
            "city": g["city"],
            "leader": g["leader"],
            "badge_id": g["badge_id"],
            "badge_name": g["badge_name"],
            "badge_icon": g["badge_icon"],
            "type": g["type"],
            "recommended_level": g["recommended_level"],
            "is_unlocked": is_gym_unlocked(g["id"], badges),
            "is_defeated": g["badge_id"] in badges
        })

    all_species = set()
    for s in STARTER_TEMPLATES.values():
        all_species.add(s["name"])
    for w in WILD_TEMPLATES:
        all_species.add(w["name"])

    game_data = {
        "has_player": player is not None,
        "player": player.to_dict() if player else None,
        "badges": badges,
        "total_badges": len(all_gyms),
        "gyms": all_gyms,
        "pokedex": state.get("pokedex", []),
        "pokedex_total": len(all_species),
        "battle_count": state.get("battle_count", 0),
        "potions": state.get("potions", 3),
        "use_solution": state.get("use_solution", False),
        "status": state.get("status", "STARTER_SELECT")
    }

    return jsonify({
        "success": True,
        "code_progress": code_data,
        "game_progress": game_data
    })

@app.route("/api/run_tests", methods=["POST"])
def run_tests_endpoint():
    """Allows client to re-run test suites on demand."""
    sid = get_session_id()
    state = get_session_state(sid)

    data = request.json or {}
    use_sol = data.get("use_solution", state.get("use_solution", False))
    code_data = get_code_progress(use_sol)
    return jsonify({
        "success": True,
        "code_progress": code_data
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n=======================================================")
    print(f"  POKÉMON BATTLE SERVER RUNNING ON PORT {port}")
    print(f"  Access locally or via Live Share at: http://localhost:{port}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
