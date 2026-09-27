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

    # Evolution Front Sprites (Stage 1 & Stage 2)
    "charmeleon.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/5.gif",
    "wartortle.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/8.gif",
    "ivysaur.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/2.gif",
    "raichu.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/26.gif",
    "charizard.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/6.gif",
    "blastoise.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/9.gif",
    "venusaur.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/3.gif",

    # Additional Wild Pokémon Sprites (Front)
    "caterpie.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/10.gif",
    "butterfree.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/12.gif",
    "geodude.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/74.gif",
    "onix.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/95.gif",
    "zubat.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/41.gif",
    "oddish.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/43.gif",
    "machop.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/66.gif",
    "growlithe.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/58.gif",
    "abra.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/63.gif",
    "snorlax.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/143.gif",
    "gyarados.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/130.gif",
    "dragonite.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/149.gif",
    "eevee.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/133.gif",
    "staryu.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/120.gif",

    # Back animated GIFs for player
    "bulbasaur_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/1.gif",
    "charmander_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/4.gif",
    "squirtle_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/7.gif",
    "pikachu_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/25.gif",

    # Evolution Back Sprites
    "charmeleon_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/5.gif",
    "wartortle_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/8.gif",
    "ivysaur_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/2.gif",
    "raichu_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/26.gif",
    "charizard_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/6.gif",
    "blastoise_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/9.gif",
    "venusaur_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/3.gif",

    # Wild Pokémon Back Sprites
    "caterpie_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/10.gif",
    "butterfree_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/12.gif",
    "geodude_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/74.gif",
    "onix_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/95.gif",
    "zubat_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/41.gif",
    "oddish_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/43.gif",
    "machop_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/66.gif",
    "growlithe_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/58.gif",
    "abra_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/63.gif",
    "snorlax_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/143.gif",
    "gyarados_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/130.gif",
    "dragonite_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/149.gif",
    "eevee_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/133.gif",
    "staryu_back.gif": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/120.gif",

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
