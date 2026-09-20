# 🔴 Pokémon Code Adventure ⚡

An interactive, retro-style educational capstone project designed for beginner Python learners (ages 10-14 and anyone starting their Python journey).

Students write real Python code across 4 progressive missions to build a playable Pokémon battle and safari-catching game with animated sprites, 8-bit sound synthesizer, elemental type matchups, and a retro web interface.

---

## 📋 Prerequisites

Before starting, ensure you have:
- **Python 3.8+** installed (`python3 --version`)
- **Git** (optional, if cloning)
- A modern web browser (Chrome, Firefox, Safari, Edge)

---

## 🚀 Quick Start (One-Click Setup)

The easiest way to install dependencies and run the game is using the one-click startup script:

```bash
# 1. Navigate to the project folder
cd pokemon-capstone

# 2. Run the startup script
./run.sh
```

### What `./run.sh` does automatically:
1. Creates a Python virtual environment (`venv/`).
2. Installs required dependencies (`flask`).
3. Verifies and downloads required Pokémon pixel sprites if missing.
4. Starts the local game server at **`http://localhost:5000`**.

Once started, open your web browser and navigate to:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 🛠️ Manual Installation & Launch

If you prefer to set up manually without using `run.sh`:

### 1. Create and Activate a Virtual Environment

On **Linux / macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

On **Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify / Download Sprites (One-time)
If the animated sprite gifs are missing from `static/images/sprites/`:
```bash
python3 download_sprites.py
```

### 4. Start the Server
```bash
python3 app.py
```
Open your browser at **`http://localhost:5000`**.

---

## 🧪 Running the Tests

You can check code progress anytime without opening the browser.

### Test Student Code
```bash
python3 run_tests.py
```

### Test Teacher Reference Solutions
```bash
python3 run_tests.py --solutions
```

### Test Specific Modules
```bash
python3 tests/test_pokemon.py    # Mission 1: Pokemon Class
python3 tests/test_starters.py   # Mission 2: Starter Selection
python3 tests/test_battle.py     # Mission 3: Combat Math & AI
python3 tests/test_catching.py   # Mission 4: Safari Catching
python3 tests/test_poke_type.py  # Bonus: Elemental Type System
```

---

## 🧭 Project Navigation & Guides

- **Student Guide**: See [`STUDENT_GUIDE.md`](STUDENT_GUIDE.md) for gamified mission instructions, step-by-step checklists, and hints.
- **Teacher & Tutor Guide**: See [`TEACHER_GUIDE.md`](TEACHER_GUIDE.md) for pedagogical tips, Live Share setup, and discussion prompts.
- **AI Coding Directives**: See [`AGENTS.md`](AGENTS.md) for instructions when using AI coding assistants.

---

## 🌐 Remote / VS Code Live Share Classroom

If teaching or learning together over **VS Code Live Share**:
1. Host starts a Live Share session.
2. Under **Shared Servers** in the Live Share tab, click **Share Server** and enter `5000`.
3. The student can now open `http://localhost:5000` on their own laptop and play in real time!
