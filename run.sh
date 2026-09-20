#!/bin/bash
# ====================================================================
# ONE-CLICK START SCRIPT FOR POKÉMON CODE ADVENTURE
# ====================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "======================================================="
echo "   POKÉMON CODE ADVENTURE - SERVER LAUNCHER"
echo "======================================================="

# 1. Check or create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo "Installing required dependencies..."
    ./venv/bin/pip install -r requirements.txt
else
    echo "Virtual environment found."
fi

# 2. Check and download sprites if missing
if [ ! -f "static/images/sprites/charmander.gif" ]; then
    echo "Downloading animated Pokémon assets from GitHub..."
    ./venv/bin/python3 download_sprites.py
fi

# 3. Start the game server
PORT="${PORT:-5000}"
echo ""
echo "🚀 Starting server at: http://localhost:$PORT"
echo "💡 For VS Code Live Share: Share port $PORT so your student can open it!"
echo "======================================================="
echo ""

exec ./venv/bin/python3 app.py
