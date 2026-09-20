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
from flask import Flask, render_template, request, jsonify, session

from pokemon_data import STARTER_TEMPLATES, WILD_TEMPLATES, MOVES

app = Flask(__name__)
app.secret_key = "pikachu-pika-super-secret-key-123"

# In-memory storage for battle sessions
BATTLE_SESSIONS = {}

def get_modules(use_solution=False):
    """
    Dynamically loads either the student's workspace code
    or the teacher's reference solution.
    """
    if use_solution:
        import solutions.pokemon as mod_pokemon
        import solutions.starters as mod_starters
        import solutions.battle as mod_battle
        import solutions.catching as mod_catching
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
            "use_solution": False,
            "potions": 3,
            "pokedex": [],
            "battle_count": 0,
            "status": "STARTER_SELECT"
        }
    return BATTLE_SESSIONS[sid]

def spawn_wild_pokemon(PokemonClass, battle_count=0):
    """Creates a random wild opponent."""
    if battle_count >= 3:
        # Boss Battle: Mewtwo!
        data = WILD_TEMPLATES[2]
    else:
        # Pidgey or Gengar
        data = random.choice(WILD_TEMPLATES[:2])

    enemy = PokemonClass(
        name=data["name"],
        poke_type=data["type"],
        max_hp=data["max_hp"],
        attack=data["attack"],
        defense=data["defense"],
        moves=list(data["moves"]),
        front_sprite=data["front_sprite"],
        back_sprite=data.get("back_sprite", "")
    )
    # Give full HP
    enemy.hp = enemy.max_hp
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
    return jsonify({"success": True, "starters": starters_info})

@app.route("/api/choose_starter", methods=["POST"])
def choose_starter():
    sid = get_session_id()
    state = get_session_state(sid)
    data = request.json or {}
    choice = data.get("choice", "pikachu")

    mods = get_modules(state["use_solution"])

    try:
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
        if not hasattr(player_mon, "hp") or not hasattr(player_mon, "name"):
            return jsonify({
                "success": False,
                "student_error": True,
                "file": "pokemon.py",
                "function": "__init__",
                "message": "Pokemon object is missing 'name' or 'hp' attributes!",
                "hint": "In pokemon.py, ensure __init__ sets `self.name = name` and `self.hp = max_hp`."
            }), 400

        # Spawn wild enemy
        enemy_mon = spawn_wild_pokemon(mods["Pokemon"], state["battle_count"])

        state["player"] = player_mon
        state["enemy"] = enemy_mon
        state["potions"] = 3
        state["status"] = "BATTLE"

        return jsonify({
            "success": True,
            "player": player_mon.to_dict(),
            "enemy": enemy_mon.to_dict(),
            "potions": state["potions"],
            "dialogue": [
                f"Professor Oak: Excellent choice! Take good care of {player_mon.name}!",
                f"A wild {enemy_mon.name} appeared!"
            ]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "student_error": True,
            "file": "starters.py / pokemon.py",
            "function": "create_starter",
            "message": str(e),
            "hint": "Check the terminal or run `python tests/test_starters.py` to inspect the error!"
        }), 400

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
    mods = get_modules(state["use_solution"])

    dialogue_log = []
    events = []

    # 1. PLAYER'S TURN
    try:
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

        p_dmg, p_crit, p_mult = dmg_result
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
            "enemy_hp": enemy.hp
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "student_error": True,
            "file": "battle.py",
            "function": "calculate_damage",
            "message": str(e),
            "hint": "Check your math formula or types in battle.py!"
        }), 400

    # Check if enemy fainted
    if enemy.is_fainted():
        dialogue_log.append(f"Wild {enemy.name} fainted! You won the battle!")
        state["battle_count"] += 1
        events.append({"type": "enemy_faint"})
        return jsonify({
            "success": True,
            "player": player.to_dict(),
            "enemy": enemy.to_dict(),
            "dialogue": dialogue_log,
            "events": events,
            "battle_over": True,
            "victory": True
        })

    # 2. ENEMY'S TURN
    try:
        e_move = mods["choose_enemy_move"](enemy)
        if not e_move:
            e_move = "Tackle"

        e_result = mods["calculate_damage"](e_move, enemy, player)
        if e_result is None or not isinstance(e_result, (tuple, list)):
            e_dmg, e_crit, e_mult = 10, False, 1.0
        else:
            e_dmg, e_crit, e_mult = e_result

        player.take_damage(e_dmg)

        e_msg = f"Wild {enemy.name} used {e_move}!"
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
            "player_hp": player.hp
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "student_error": True,
            "file": "battle.py",
            "function": "choose_enemy_move / calculate_damage",
            "message": str(e),
            "hint": "Check choose_enemy_move in battle.py!"
        }), 400

    # Check if player fainted
    player_fainted = player.is_fainted()
    if player_fainted:
        dialogue_log.append(f"{player.name} fainted! You rushed back to the Pokémon Center.")
        events.append({"type": "player_faint"})

    return jsonify({
        "success": True,
        "player": player.to_dict(),
        "enemy": enemy.to_dict(),
        "dialogue": dialogue_log,
        "events": events,
        "battle_over": player_fainted,
        "victory": False
    })

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

    # Use potion (+25 HP)
    state["potions"] -= 1
    old_hp = player.hp
    player.heal(25)
    healed_amount = player.hp - old_hp

    dialogue_log = [f"Used a Potion! {player.name} recovered {healed_amount} HP!"]
    events = [{"type": "heal", "healed": healed_amount, "player_hp": player.hp}]

    # Enemy retaliates
    mods = get_modules(state["use_solution"])
    try:
        e_move = mods["choose_enemy_move"](enemy)
        e_result = mods["calculate_damage"](e_move, enemy, player)
        e_dmg = e_result[0] if e_result else 8
        player.take_damage(e_dmg)

        dialogue_log.append(f"Wild {enemy.name} used {e_move} while you healed! Dealt {e_dmg} damage.")
        events.append({
            "type": "enemy_attack",
            "move": e_move,
            "damage": e_dmg,
            "player_hp": player.hp
        })
    except Exception:
        pass

    return jsonify({
        "success": True,
        "player": player.to_dict(),
        "enemy": enemy.to_dict(),
        "potions": state["potions"],
        "dialogue": dialogue_log,
        "events": events,
        "battle_over": player.is_fainted()
    })

@app.route("/api/catch", methods=["POST"])
def catch():
    sid = get_session_id()
    state = get_session_state(sid)
    enemy = state.get("enemy")
    player = state.get("player")

    if not enemy or not player:
        return jsonify({"success": False, "message": "No wild Pokémon to catch!"}), 400

    data = request.json or {}
    ball_type = data.get("ball_type", "poke-ball")
    mods = get_modules(state["use_solution"])

    try:
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

        caught, shakes = catch_result

        dialogue = []
        events = [{"type": "throw_ball", "ball": ball_type, "shakes": shakes, "caught": caught}]

        if caught:
            dialogue.append(f"Gotcha! Wild {enemy.name} was caught!")
            if enemy.name not in state["pokedex"]:
                state["pokedex"].append(enemy.name)
            state["battle_count"] += 1
            return jsonify({
                "success": True,
                "caught": True,
                "shakes": shakes,
                "pokedex": state["pokedex"],
                "dialogue": dialogue,
                "events": events,
                "battle_over": True,
                "victory": True
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
            try:
                e_move = mods["choose_enemy_move"](enemy)
                e_dmg = mods["calculate_damage"](e_move, enemy, player)[0]
                player.take_damage(e_dmg)
                dialogue.append(f"Wild {enemy.name} used {e_move}! Dealt {e_dmg} damage.")
                events.append({
                    "type": "enemy_attack",
                    "move": e_move,
                    "damage": e_dmg,
                    "player_hp": player.hp
                })
            except Exception:
                pass

            return jsonify({
                "success": True,
                "caught": False,
                "shakes": shakes,
                "player": player.to_dict(),
                "enemy": enemy.to_dict(),
                "dialogue": dialogue,
                "events": events,
                "battle_over": player.is_fainted()
            })

    except Exception as e:
        return jsonify({
            "success": False,
            "student_error": True,
            "file": "catching.py",
            "function": "attempt_catch",
            "message": str(e),
            "hint": "Check attempt_catch in catching.py!"
        }), 400

@app.route("/api/next_battle", methods=["POST"])
def next_battle():
    sid = get_session_id()
    state = get_session_state(sid)
    player = state.get("player")

    if not player:
        return jsonify({"success": False, "message": "No player found"}), 400

    mods = get_modules(state["use_solution"])

    # Revive/heal player slightly for next battle
    if player.is_fainted():
        player.hp = player.max_hp
    else:
        player.heal(15)

    enemy_mon = spawn_wild_pokemon(mods["Pokemon"], state["battle_count"])
    state["enemy"] = enemy_mon

    boss_tag = " [BOSS BATTLE!]" if state["battle_count"] >= 3 else ""

    return jsonify({
        "success": True,
        "player": player.to_dict(),
        "enemy": enemy_mon.to_dict(),
        "battle_count": state["battle_count"],
        "pokedex": state["pokedex"],
        "dialogue": [f"A wild {enemy_mon.name}{boss_tag} appeared!"]
    })

@app.route("/api/toggle_mode", methods=["POST"])
def toggle_mode():
    sid = get_session_id()
    state = get_session_state(sid)
    data = request.json or {}
    target_solution = bool(data.get("use_solution", not state["use_solution"]))
    state["use_solution"] = target_solution
    mode_name = "Teacher Reference Solutions" if target_solution else "Student Code Workspace"
    return jsonify({
        "success": True,
        "use_solution": target_solution,
        "mode_name": mode_name
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n=======================================================")
    print(f"  POKÉMON BATTLE SERVER RUNNING ON PORT {port}")
    print(f"  Access locally or via Live Share at: http://localhost:{port}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
