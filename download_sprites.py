import os
import urllib.request
import urllib.error

SPRITE_DIR = os.path.join(os.path.dirname(__file__), "static", "images", "sprites")
os.makedirs(SPRITE_DIR, exist_ok=True)

SPRITES_TO_DOWNLOAD = {
    # Front animated GIFs
    "bulbasaur.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/1.gif",
    "charmander.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/4.gif",
    "squirtle.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/7.gif",
    "pikachu.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/25.gif",
    "pidgey.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/16.gif",
    "gengar.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/94.gif",
    "mewtwo.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/150.gif",

    # Back animated GIFs for player
    "bulbasaur_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/1.gif",
    "charmander_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/4.gif",
    "squirtle_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/7.gif",
    "pikachu_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/25.gif",

    # Item icons
    "poke-ball.png": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png",
    "great-ball.png": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/great-ball.png",
    "ultra-ball.png": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/ultra-ball.png",
    "potion.png": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/potion.png",
}

def download_all():
    print("Downloading open-source Pokémon assets from GitHub (PokeAPI/sprites)...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    for filename, url in SPRITES_TO_DOWNLOAD.items():
        filepath = os.path.join(SPRITE_DIR, filename)
        if not os.path.exists(filepath):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response, open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
                print(f"  [OK] Downloaded: {filename}")
            except Exception as e:
                print(f"  [WARNING] Could not download {filename}: {e}")
        else:
            print(f"  [EXISTS] {filename}")
    print("Asset download completed!")

if __name__ == "__main__":
    download_all()
