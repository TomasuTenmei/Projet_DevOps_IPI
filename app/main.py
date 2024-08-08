from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from jinja2 import Environment, FileSystemLoader
import os
import json

app = FastAPI()

# Charger les données des Pokémon depuis le fichier JSON
with open('./data/pokemon.json', 'r', encoding='utf-8') as f:
    pokemons = json.load(f)

# Configure Jinja2
templates_path = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(templates_path))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    template = env.get_template('index.html')
    return template.render()

@app.get("/pokemon/")
def get_all_pokemons():
    return pokemons

@app.get("/pokemon/{number}")
def get_pokemon_by_number(number: int):
    for pokemon in pokemons:
        if pokemon["number"] == str(number):
            return pokemon
    raise HTTPException(status_code=404, detail="Pokémon non trouvé")

@app.get("/pokemon/name/{name}")
def get_pokemon_by_name(name: str):
    for pokemon in pokemons:
        if pokemon["name"].lower() == name.lower():
            return pokemon
    raise HTTPException(status_code=404, detail="Pokémon non trouvé")
