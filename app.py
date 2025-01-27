from flask import Flask, render_template, url_for, request, jsonify
from connection import connect
import google.generativeai as genai
import json
from dotenv import load_dotenv
import os
import requests
import traceback

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
    prompt34 = (  # Prompt for Gemini AI
                f"I am playing Dota 2 and the game mode is normal/ranked matchmaking. Create a list of ten heroes to choose from, considering the following picks: "
                f"Allies: {allied_hero1}, {allied_hero2}; Enemies: {enemy_hero1}, {enemy_hero2}. "
                "DO NOT SUGGEST HEROES WHO HAVE ALREADY BEEN PICKED BY EITHER TEAM!"
                "To give me the most accurate suggestions, you MUST consider ALL of these parameters: "
                "SYNERGY WITH ALLIED HEROES (complementarity and possible combos), COUNTERPICKS to neutralize "
                "the enemy picks and/or to exploit their weaknesses and last but not least, the REMAINING ROLES. "
                "There must be a perfect balance inside the team: generally a Dota 2 team needs a 'primary support', a 'secondary support/roamer', a 'carry', an 'offlaner' and a 'midlaner'). "
                "For example, do not suggest a support if my team has already picked two of them! "
                "By convention, this is the general pick order: primary support, secondary support/roamer, offlaner, carry', and midlaner. "
                "Usually, the third and fourth picks are the offlaner and the carry. Check if they have already been taken. If not, for suggestions, prioritize these two roles; "
                "otherwise choose the best heroes using the same logic I described after the list of allied and enemy heroes."
                "To further improve your choices, use OpenDota API to get updated statistics. Limit your analysis to data derived from games played in the most recent patch."
                "Place greater emphasis on heroes with a higher win rate. Consider not only the overall win rate of a hero, but also its performance against the heroes chosen by the opposing team to identify optimal counterpicks. "
                "Restrict data analysis to matches played at the highest level of ranked matchmaking (Immortal) or in professional tournaments. "
                "YOUR OUTPUT: Provide a JSON array containing the names of recommended heroes. Do not add any other text, explanations, or formatting. The array should be properly formatted with square brackets [ ] and comma-separated hero names in quotes. "
                "Before and after the array, DO NOT INCLUDE ANY SPACES OR EXTRA CHARACTER SUCH AS LINE BREAKS OR SIMILAR! Your response MUST BE LIKE THIS: ['Hero1', 'Hero2', 'Hero3', 'Hero4', 'Hero5', 'Hero6', 'Hero7', 'Hero8', 'Hero9', 'Hero10']."
                )
    prompt34 = prompt34.replace("'",'"')
    try: # Process the response (assuming that response34.text is a JSON array)
        response34 = model.generate_content(prompt34) # Calls Gemini AI to get a response prompt
        array34 = json.loads(response34.text.replace("'",'"'))  # Parsing JSON in array
        prompt_response34 = f"Recommended picks: {', '.join(array34)}" # Generate the final string to send to the frontend in the relative textbox
        return jsonify({"prompt": prompt_response34}) # Return the prompt as a JSON response
    except requests.exceptions.Timeout:
        return jsonify({"prompt": "Error: Request to Gemini timed out"}), 408 # Handle timeout errors
    except requests.exceptions.RequestException as e:
        return jsonify({"prompt": f"Error: A request error occurred: {str(e)}"}), 500 # Handle generic request exceptions
    except json.JSONDecodeError: 
        return jsonify({"prompt": "Error: Unable to parse response from Gemini"}), 500 # Handle errors in parsing the response as JSON
    except Exception as e: # Handle any other unexpected exceptions
        print("Unexpected error:", e)
        print(traceback.format_exc())  
        return jsonify({"prompt": f"Error: An unexpected error occurred: {str(e)}"}), 500
    
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
    prompt5 = (  # Prompt for Gemini AI
                f"I am playing Dota 2 and the game mode is normal/ranked matchmaking. Create a list of TEN heroes to choose from, considering the following picks: "
                f"Allied: {allied_hero1}, {allied_hero2}, {allied_hero3}, {allied_hero4}; Enemies: {enemy_hero1}, {enemy_hero2}, {enemy_hero3}, {enemy_hero4}. "
                "DO NOT SUGGEST HEROES WHO HAVE ALREADY BEEN PICKED BY EITHER TEAM!"
                "To give me the most accurate suggestions, you MUST consider ALL of these parameters: "
                "SYNERGY WITH ALLIED HEROES (complementarity and possible combos), COUNTERPICKS to neutralize "
                "the enemy picks and/or to exploit their weaknesses and last but not least, the REMAINING ROLES. "
                "There must be a perfect balance inside the team: generally a Dota 2 team needs a 'primary support', a 'secondary support/roamer', a 'carry', an 'offlaner' and a 'midlaner'). "
                "For example, do not suggest a support if my team has already picked two of them! "
                "By convention, this is the general pick order: primary support, secondary support/roamer, offlaner, carry', and midlaner. "
                "Usually, the last pick is the midlaner. Check if this role is already been taken. If not, for suggestions, prioritize this role; "
                "otherwise choose the best heroes using the same logic I described after the list of allied and enemy heroes."
                "To further improve your choices, use OpenDota API to get updated statistics. Limit your analysis to data derived from games played in the most recent patch."
                "Place greater emphasis on heroes with a higher win rate. Consider not only the overall win rate of a hero, but also its performance against the heroes chosen by the opposing team to identify optimal counterpicks. "
                "Restrict data analysis to matches played at the highest level of ranked matchmaking (Immortal) or in professional tournaments. "
                "YOUR OUTPUT: Provide a JSON array containing the names of recommended heroes. Do not add any other text, explanations, or formatting. The array should be properly formatted with square brackets [ ] and comma-separated hero names in quotes. "
                "Before and after the array, DO NOT INCLUDE ANY SPACES OR EXTRA CHARACTER SUCH AS LINE BREAKS OR SIMILAR! Your response MUST BE LIKE THIS: ['Hero1', 'Hero2', 'Hero3', 'Hero4', 'Hero5', 'Hero6', 'Hero7', 'Hero8', 'Hero9', 'Hero10']."
                )
    prompt5 = prompt5.replace("'",'"')
    try: # Process the response (assuming that response5.text is a JSON array)
        response5 = model.generate_content(prompt5) # Calls Gemini AI to get a response prompt
        array5 = json.loads(response5.text.replace("'",'"'))  # Parsing JSON in array
        prompt_response5 = f"Recommended picks: {', '.join(array5)}" # Generate the final string to send to the frontend in the relative textbox
        return jsonify({"prompt": prompt_response5}) # Return the prompt as a JSON response
    except requests.exceptions.Timeout:
        return jsonify({"prompt": "Error: Request to Gemini timed out"}), 408 # Handle timeout errors
    except requests.exceptions.RequestException as e:
        return jsonify({"prompt": f"Error: A request error occurred: {str(e)}"}), 500 # Handle generic request exceptions
    except json.JSONDecodeError: 
        return jsonify({"prompt": "Error: Unable to parse response from Gemini"}), 500 # Handle errors in parsing the response as JSON
    except Exception as e: # Handle any other unexpected exceptions
        print("Unexpected error:", e)
        print(traceback.format_exc())  
        return jsonify({"prompt": f"Error: An unexpected error occurred: {str(e)}"}), 500 

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
    promptCM = (  # Prompt for Gemini AI
                f"I am playing Dota 2 and the game mode is Captain's Mode. I am currently playing for the {sideChosen} side. "
                f"Create a list of ten heroes to choose from. Consider the following picks and bans: "
                f"Radiant bans: {radiantBans}; radiant picks: {radiantPicks}; Dire bans: {direBans}; Dire Picks: {direPicks}. "
                "DO NOT SUGGEST HEROES WHO HAVE ALREADY BEEN PICKED OR BANNED BY EITHER TEAM!"
                "To give me the most accurate suggestions, you MUST consider ALL of these parameters: "
                "SYNERGY WITH ALLIED HEROES (complementarity and possible combos), COUNTERPICKS to neutralize "
                "the enemy picks and/or to exploit their weaknesses and last but not least, the REMAINING ROLES. "
                "There must be a perfect balance inside the team: generally a Dota 2 team needs a 'primary support', a 'secondary support/roamer', a 'carry', an 'offlaner' and a 'midlaner'). "
                "For example, do not suggest a support if my team has already picked two of them! "
                "By convention, this is the general pick order: primary support, secondary support/roamer, offlaner, carry', and midlaner. "
                "To further improve your choices, use OpenDota API to get updated statistics. Limit your analysis to data derived from games played in the most recent patch."
                "Place greater emphasis on heroes with a higher win rate. Consider not only the overall win rate of a hero, but also its performance against the heroes chosen by the opposing team to identify optimal counterpicks. "
                "Restrict data analysis to matches played at the highest level of ranked matchmaking (Immortal) or in professional tournaments. "
                "YOUR OUTPUT: Provide a JSON array containing the names of recommended heroes. Do not add any other text, explanations, or formatting. The array should be properly formatted with square brackets [ ] and comma-separated hero names in quotes. "
                "Before and after the array, DO NOT INCLUDE ANY SPACES OR EXTRA CHARACTER SUCH AS LINE BREAKS OR SIMILAR! Your response MUST BE LIKE THIS: ['Hero1', 'Hero2', 'Hero3', 'Hero4', 'Hero5', 'Hero6', 'Hero7', 'Hero8', 'Hero9', 'Hero10']."
            )
    promptCM = promptCM.replace("'",'"')
    try: 
        responseCM = model.generate_content(promptCM) # Calls Gemini AI to get a response prompt
        arrayCM = json.loads(responseCM.text.replace("'",'"'))  # Parsing JSON in array
        prompt_responseCM = f"Recommended picks: {', '.join(arrayCM)}" # Generate the final string to send to the frontend in the relative textbox
        return jsonify({"prompt": prompt_responseCM}) # Return the prompt as a JSON response
    except requests.exceptions.Timeout:
        return jsonify({"prompt": "Error: Request to Gemini timed out"}), 408 # Handle timeout errors
    except requests.exceptions.RequestException as e:
        return jsonify({"prompt": f"Error: A request error occurred: {str(e)}"}), 500 # Handle generic request exceptions
    except json.JSONDecodeError: 
        return jsonify({"prompt": "Error: Unable to parse response from Gemini"}), 500 # Handle errors in parsing the response as JSON
    except Exception as e: # Handle any other unexpected exceptions
        print("Unexpected error:", e)
        print(traceback.format_exc())  
        return jsonify({"prompt": f"Error: An unexpected error occurred: {str(e)}"}), 500

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

''' ---  FUTURE UPDATE. WORK IN PROGRESS  ---" '''
@app.route("/heroDetail")  
def heroDetail():
    return render_template("heroDetail.html", current_page="Dota 2 - Heroes - Details", heroes=heroes)    

'''# Gather data sent from client
data = request.get_json()
searchedHero = data.get("searchedHero")
with connect() as conn:
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM heroes WHERE id = '{searchedHero}';")
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
    heroes.append(cards)'''
    

if __name__ == "__main__":
    app.run(debug=False, port=80)