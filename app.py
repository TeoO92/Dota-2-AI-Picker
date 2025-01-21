from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from connessione import connect
import google.generativeai as genai
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv() # Carica le variabili dal file .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Leggi la chiave API dal file .env
model = genai.GenerativeModel("gemini-1.5-flash")

class listHeroes:
    def __init__(self, heroId, heroName, heroPrimaryAttribute, heroAttackType, heroRoles):
        self.heroId = heroId
        self.heroName = heroName
        self.heroPrimaryAttribute = heroPrimaryAttribute
        self.heroAttackType = heroAttackType
        self.heroRoles = heroRoles

@app.route("/")
def home():
    return render_template("index.html", current_page="index")

@app.route("/normal_ranked")
def normal_ranked_picker():
    # Connessione al database e esecuzione della query
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT localized_name FROM heroes;')
        results = cursor.fetchall()
        cursor.close()
    heroes = [res[0] for res in results]
    return render_template("nr.html", current_page="Normal/Ranked AI Picker", heroes=heroes)

@app.route("/suggest34nr", methods=["POST"])
def geminiSuggest34():
    # Recupera i dati inviati dal client
    data = request.get_json()
    allied_hero1 = data.get("alliedHero1")
    allied_hero2 = data.get("alliedHero2")
    enemy_hero1 = data.get("enemyHero1")
    enemy_hero2 = data.get("enemyHero2")
    # Prompt da inviare a Gemini
    prompt34 = (f"Create a list of eight Dota 2 heroes to choose from, considering the following picks: "
              f"Allied: {allied_hero1}, {allied_hero2}; Enemies: {enemy_hero1}, {enemy_hero2}. "
              "To give me the most accurate suggestions, you MUST consider ALL of these parameters:"
              "SYNERGY WITH ALLIED HEROES (complementarity and possible combos), COUNTERPICKS to neutralize "
              "the enemy picks and/or to exploit their weaknesses and last but not least, the REMAINING ROLES: "
              "there must be a perfect balance inside the team (generally a Dota 2 team need a 'primary support', a 'secondary support/roamer', a 'carry', an 'offlaner' and a 'midlaner'). "
              "To further improve your choices, use OpenDota API to get updated statistics like overall highest winrate heroes and overall highest pickrate heroes "
              "(use 'Public' section or 'Professional' one but not 'Turbo'!)."
              "ABSOLUTELY DO NOT SUGGEST HEROES WHOSE ROLES HAVE ALREADY BEEN TAKEN BY THOSE SELECTED BY MY TEAM! For example, "
              "do not suggest Lion if my team has already picked two supports. Logically, you also don't have to suggest heroes who have already been taken!"
              "Theoretically, the third and fourth picks are the carry and the offlaner. Check if they have already been taken. If not, for suggestions, prioritize these two roles; "
              "otherwise choose the best heroes using the same logic I described after the list of allied and enemy heroes."              
              "YOUR OUTPUT: A text containing an array of hero names with no explanation or anything. "
              "DO NOT FORMAT THE TEXT as code or anything, just provide me with a string of text that contains the array with the suggested heroes.")
    # Chiama Gemini per generare prompt di risposta
    response34 = model.generate_content(prompt34)
    # Elabora la risposta (supponendo che response34.text sia un JSON array)
    try:
        array34 = json.loads(response34.text.replace("'",'"'))  # Parsing JSON in array
    except json.JSONDecodeError:
        return jsonify({"prompt": "Error: Unable to parse response from Gemini"}), 3000
    # Genera la stringa finale da inviare al frontend
    prompt_response34 = f"Recommended picks: {', '.join(array34)}"
    # Restituisci il prompt come risposta JSON
    return jsonify({"prompt": prompt_response34})

@app.route("/suggest5nr", methods=["POST"])
def geminiSuggest5():
    # Recupera i dati inviati dal client
    data = request.get_json()
    allied_hero1 = data.get("alliedHero1")
    allied_hero2 = data.get("alliedHero2")
    allied_hero3 = data.get("alliedHero3")
    allied_hero4 = data.get("alliedHero4")
    enemy_hero1 = data.get("enemyHero1")
    enemy_hero2 = data.get("enemyHero2")
    enemy_hero3 = data.get("enemyHero3")
    enemy_hero4 = data.get("enemyHero4")
    # Prompt da inviare a Gemini
    prompt5 = (f"Create a list of eight Dota 2 heroes to choose from, considering the following picks: "
              f"Allied: {allied_hero1}, {allied_hero2}, {allied_hero3}, {allied_hero4}; Enemies: {enemy_hero1}, {enemy_hero2}, {enemy_hero3}, {enemy_hero4}. "
              "To give me the most accurate suggestions, you MUST consider ALL of these parameters:"
              "SYNERGY WITH ALLIED HEROES (complementarity and possible combos), COUNTERPICKS to neutralize "
              "the enemy picks and/or to exploit their weaknesses and last but not least, the REMAINING ROLES: "
              "there must be a perfect balance inside the team (generally a Dota 2 team need a 'primary support', a 'secondary support/roamer', a 'carry', an 'offlaner' and a 'midlaner'). "
              "To further improve your choices, use OpenDota API to get updated statistics like overall highest winrate heroes and overall highest pickrate heroes "
              "(use 'Public' section or 'Professional' one but not 'Turbo'!)."
              "ABSOLUTELY DO NOT SUGGEST HEROES WHOSE ROLES HAVE ALREADY BEEN TAKEN BY THOSE SELECTED BY MY TEAM! For example, "
              "do not suggest Lion if my team has already picked two supports. Logically, you also don't have to suggest heroes who have already been taken!"
              "To further improve your choices, use OpenDota API to get updated statistics like overall highest winrate heroes and overall highest pickrate heroes "
              "(use 'Public' section or 'Professional' one but not 'Turbo'!). Theoretically, the last pick is the midlaner. Check if it has already been taken. "
              "If not, suggest a midlaner; otherwise choose the best heroes using the same logic i described after the list of allied and enemy heroes."
              "YOUR OUTPUT: A text containing an array of hero names with no explanation or anything. "
              "DO NOT FORMAT THE TEXT as code or anything, just provide me with a string of text that contains the array with the suggested heroes.")
    # Chiama Gemini per generare prompt di risposta
    response5 = model.generate_content(prompt5)
    # Elabora la risposta (supponendo che response34.text sia un JSON array)
    try:
        array5 = json.loads(response5.text.replace("'",'"'))  # Parsing JSON in array
    except json.JSONDecodeError:
        return jsonify({"prompt": "Error: Unable to parse response from Gemini"}), 3000
    # Genera la stringa finale da inviare al frontend
    prompt_response5 = f"Recommended picks: {', '.join(array5)}"
    # Restituisci il prompt come risposta JSON
    return jsonify({"prompt": prompt_response5})

@app.route("/captains_mode")
def captains_mode_picker():
    # Connessione al database e esecuzione della query
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT localized_name FROM heroes;')
        results = cursor.fetchall()
        cursor.close()
    heroes = [res[0] for res in results]
    return render_template("cm.html", current_page="Captains Mode AI Picker", heroes=heroes)

@app.route("/suggestCM", methods=["GET","POST"]) #ROUTE PER suggestCM
def geminiSuggestCM():
    # Recupera i dati inviati dal client
    data = request.get_json()
    sideChosen = data.get("sideChosen")
    radiantBans = data.get("radiantBans")
    radiantPicks = data.get("radiantPicks")
    direBans = data.get("direBans")
    direPicks = data.get("direPicks")
    # Prompt da inviare a Gemini
    promptCM = (f"I am playing at Dota 2 in Captains Mode and actually playing as {sideChosen}. "
              f"Create a list of eight Dota 2 heroes to choose from, considering the following picks and bans: "
              f"Radiant bans: {radiantBans}; radiant picks: {radiantPicks}; Dire bans: {direBans}; Dire Picks: {direPicks}. "
              "To give me the most accurate suggestions, you MUST consider ALL of these parameters:"
              "SYNERGY WITH ALLIED HEROES (complementarity and possible combos), COUNTERPICKS to neutralize "
              "the enemy picks and/or to exploit their weaknesses and last but not least, the REMAINING ROLES: "
              "there must be a perfect balance inside the team (generally a Dota 2 team need a 'primary support', a 'secondary support/roamer', a 'carry', an 'offlaner' and a 'midlaner'). "
              "To further improve your choices, use OpenDota API to get updated statistics like overall highest winrate heroes and overall highest pickrate heroes "
              "(use 'Public' section or 'Professional' one but not 'Turbo'!)."
              "ABSOLUTELY DO NOT SUGGEST HEROES WHOSE ROLES HAVE ALREADY BEEN TAKEN BY THOSE SELECTED BY MY TEAM! For example, "
              "do not suggest Lion if my team has already picked two supports. Logically, you also don't have to suggest heroes who have already been taken or banned!"
              "To further improve your choices, use OpenDota API to get updated statistics like overall highest winrate heroes and overall highest pickrate heroes "
              f"(use 'Public' section or 'Professional' one but not 'Turbo'!). Always keep in mind that i am currently playing as {sideChosen}. DON'T SUGGEST THE ALREADY BANNED HEROES!"
              "YOUR OUTPUT: A text containing an array of hero names with no explanation or anything. "
              "DO NOT FORMAT THE TEXT as code or anything, just provide me with a string of text that contains the array with the suggested heroes.")
    # Chiama Gemini per generare prompt di risposta
    responseCM = model.generate_content(promptCM)
    # Elabora la risposta (supponendo che response34.text sia un JSON array)
    try:
        arrayCM = json.loads(responseCM.text.replace("'",'"'))  # Parsing JSON in array
    except json.JSONDecodeError:
        return jsonify({"prompt": "Error: Unable to parse response from Gemini"}), 3000
    # Genera la stringa finale da inviare al frontend
    prompt_responseCM = f"Recommended picks: {', '.join(arrayCM)}"
    # Restituisci il prompt come risposta JSON
    return jsonify({"prompt": prompt_responseCM})

@app.route("/heroes")
def heroes():
    # Connessione al database e esecuzione della query + chiusura connessione
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM heroes ORDER BY id ASC;')
        results = cursor.fetchall()
        cursor.close()
    heroes = []
    for res in results:
        heroId = res[0]
        heroName = res[1]
        heroPrimaryAttribute = res[2]
        heroAttackType = res[3]
        heroRoles = res[4]
        cards = listHeroes(heroId, heroName, heroPrimaryAttribute, heroAttackType, heroRoles)
        heroes.append(cards)
    return render_template("heroes.html", current_page="Dota 2 Heroes", heroes=heroes)

if __name__ == "__main__":
    app.run(port=80)