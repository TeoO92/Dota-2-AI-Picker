from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from connection import connect
import google.generativeai as genai
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv() # Loads environmental variables from .env file (or Render)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Loads environmental variables from .env file (or Render)
model = genai.GenerativeModel(model_name='gemini-1.5-flash-8b-latest')

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
    with connect() as conn: # Connect to db and execute the query
        cursor = conn.cursor()
        cursor.execute("SELECT localized_name FROM heroes ORDER BY localized_name ASC;")
        results = cursor.fetchall()
        cursor.close()
    heroes = [res[0] for res in results]
    return render_template("nr.html", current_page="Dota 2 AI Picker - Normal/Ranked", heroes=heroes)

@app.route("/suggest34nr", methods=["POST"])
def geminiSuggest34():
    data = request.get_json() # Gather data sent from client
    allied_hero1 = data.get("alliedHero1")
    allied_hero2 = data.get("alliedHero2")
    enemy_hero1 = data.get("enemyHero1")
    enemy_hero2 = data.get("enemyHero2")
    # Prompt for Gemini AI
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
    response34 = model.generate_content(prompt34) # Calls Gemini AI to get a response prompt
    try: # Process the response (assuming that response34.text is a JSON array)
        array34 = json.loads(response34.text.replace("'",'"'))  # Parsing JSON in array
    except json.JSONDecodeError:
        return jsonify({"prompt": "Error: Unable to parse response from Gemini"}), 6660
    prompt_response34 = f"Recommended picks: {', '.join(array34)}" # Generate the final string to send to the frontend in the relative textbox
    return jsonify({"prompt": prompt_response34}) # Return the prompt as a JSON response

@app.route("/suggest5nr", methods=["POST"])
def geminiSuggest5():
    data = request.get_json() # Gather data sent from client
    allied_hero1 = data.get("alliedHero1")
    allied_hero2 = data.get("alliedHero2")
    allied_hero3 = data.get("alliedHero3")
    allied_hero4 = data.get("alliedHero4")
    enemy_hero1 = data.get("enemyHero1")
    enemy_hero2 = data.get("enemyHero2")
    enemy_hero3 = data.get("enemyHero3")
    enemy_hero4 = data.get("enemyHero4")
    # Prompt for Gemini AI
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
    response5 = model.generate_content(prompt5) # Calls Gemini AI to get a response prompt
    try: # Process the response (assuming that response5.text is a JSON array)
        array5 = json.loads(response5.text.replace("'",'"'))  # Parsing JSON in array
    except json.JSONDecodeError:
        return jsonify({"prompt": "Error: Unable to parse response from Gemini"}), 6660
    prompt_response5 = f"Recommended picks: {', '.join(array5)}" # Generate the final string to send to the frontend in the relative textbox
    return jsonify({"prompt": prompt_response5}) # Return the prompt as a JSON response

@app.route("/captains_mode")
def captains_mode_picker():
    with connect() as conn: # Connect to db and execute the query
        cursor = conn.cursor()
        cursor.execute('SELECT localized_name FROM heroes ORDER BY localized_name ASC;')
        results = cursor.fetchall()
        cursor.close()
    heroes = [res[0] for res in results]
    return render_template("cm.html", current_page="Dota 2 AI Picker - Captains Mode", heroes=heroes)

@app.route("/suggestCM", methods=["GET","POST"])
def geminiSuggestCM():
    data = request.get_json() # Gather data sent from client
    sideChosen = data.get("sideChosen")
    radiantBans = data.get("radiantBans")
    radiantPicks = data.get("radiantPicks")
    direBans = data.get("direBans")
    direPicks = data.get("direPicks")
    # Prompt for Gemini AI
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
    responseCM = model.generate_content(promptCM) # Calls Gemini AI to get a response prompt
    try: # Process the response (assuming that responseCM.text is a JSON array)
        arrayCM = json.loads(responseCM.text.replace("'",'"'))  # Parsing JSON in array
    except json.JSONDecodeError:
        return jsonify({"prompt": "Error: Unable to parse response from Gemini"}), 6660
    prompt_responseCM = f"Recommended picks: {', '.join(arrayCM)}" # Generate the final string to send to the frontend in the relative textbox
    return jsonify({"prompt": prompt_responseCM}) # Return the prompt as a JSON response

@app.route("/heroes")
def heroes():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM heroes ORDER BY localized_name ASC;")
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

@app.route("/heroesMELEE")
def heroesMELEE():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM heroes WHERE attack_type = 'Melee' ORDER BY localized_name ASC;")
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
    return render_template("heroes.html", current_page="Dota 2 Melee Heroes", heroes=heroes)

@app.route("/heroesRANGED")
def heroesRANGED():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM heroes WHERE attack_type = 'Ranged' ORDER BY localized_name ASC;")
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
    return render_template("heroes.html", current_page="Dota 2 Ranged Heroes", heroes=heroes)

@app.route("/heroesAGI")
def heroesAGI():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM heroes WHERE primary_attr = 'agi' ORDER BY localized_name ASC;")
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
    return render_template("heroes.html", current_page="Dota 2 Agility Heroes", heroes=heroes)

@app.route("/heroesSTR")
def heroesSTR():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM heroes WHERE primary_attr = 'str' ORDER BY localized_name ASC;")
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
    return render_template("heroes.html", current_page="Dota 2 Strenght Heroes", heroes=heroes)

@app.route("/heroesINT")
def heroesINT():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM heroes WHERE primary_attr = 'int' ORDER BY localized_name ASC;")
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
    return render_template("heroes.html", current_page="Dota 2 Intelligence Heroes", heroes=heroes)

@app.route("/heroesALL")
def heroesALL():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM heroes WHERE primary_attr = 'all' ORDER BY localized_name ASC;")
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
    return render_template("heroes.html", current_page="Dota 2 Universal Heroes", heroes=heroes)

''' @app.route("/heroDetail")      "---  FUTURE UPDATE. WORK IN PROGRESS  ---"
    def heroDetail():
        # Gather data sent from client
        data = request.get_json()
        searchedHero = data.get("searchedHero")
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT localized_name FROM heroes WHERE localized_name = '{searchedHero}';")
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
        return render_template("heroDetail.html", current_page="Dota 2 Searched hero", heroes=heroes) '''

if __name__ == "__main__":
    app.run(port=80)