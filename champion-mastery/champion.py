import os
import json
import re
import html
import math
from tabulate import tabulate  # Install using: pip install tabulate

# ANSI escape codes for background colors and reset
RESET = "\033[0m"
BG_RED = "\033[41m"      # for stun
BG_GREEN = "\033[42m"    # for root
BG_MAGENTA = "\033[45m"  # for knockup/knockback
BG_CYAN = "\033[46m"     # for fear, taunt, charm, sleep
BG_BLUE = "\033[44m"     # for slow
BG_YELLOW = "\033[43m"   # for silence

# Define CC-related keywords (all lower-case)
CC_KEYWORDS = [
    "stun", "slow", "knockup", "knockback", "root", "silence",
    "suppress", "disarm", "fear", "taunt", "charm", "sleep",
    "blind", "cripple", "polymorph", "bind", "air", "knock"
]

# Path to the folder containing champion JSON files
CHAMPION_FOLDER = "champion_data"

def load_champion_data():
    """Loads all champion data into a dictionary for quick searching."""
    champions = {}
    for filename in os.listdir(CHAMPION_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(CHAMPION_FOLDER, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                champion_name = list(data["data"].keys())[0]
                champions[champion_name.lower()] = data["data"][champion_name]
    return champions

def round_cooldown(value):
    try:
        num = float(value)
        return int(num + 0.5)
    except ValueError:
        return value

def extract_first_sentence(text):
    text = html.unescape(text)
    match = re.match(r"^(.*?[.!?])\s", text)
    if match:
        return match.group(1)
    else:
        # Fallback: split at first period.
        parts = text.split(".")
        return parts[0] + "." if parts[0] else text

def get_row_bg_color(cc_type_string):
    ct = cc_type_string.lower()
    if any(x in ct for x in ["stun", "charm", "cripple", "polymorph", "suppress", "disarm", "air", "bind", "knock", "root", "knockup", "knockback", "sleep"]):
        return BG_RED
    elif any(x in ct for x in ["slow", "silence", "fear", "taunt", "blind"]):
        return BG_GREEN
    else:
        return ""

def extract_cc_info(champion):
    """Extracts CC information from a champion's abilities."""
    spells = champion.get("spells", [])
    ability_info = []
    for spell in spells:
        spell_name = html.unescape(spell.get("name", "Unknown"))
        spell_description = html.unescape(spell.get("description", "No description available."))
        first_sentence = extract_first_sentence(spell_description)
        
        cooldowns = spell.get("cooldown", [])
        if cooldowns:
            min_cd = min(cooldowns, key=float)
            cooldown_final = round_cooldown(min_cd)
        else:
            cooldown_final = "N/A"
        
        spell_description_lower = spell_description.lower()
        has_cc = any(cc in spell_description_lower for cc in CC_KEYWORDS)
        # Get all CC types found; if none, then "None"
        found_cc = [cc for cc in CC_KEYWORDS if cc in spell_description_lower]
        cc_type = ", ".join(found_cc) if found_cc else "None"
        cc_indicator = "✔" if has_cc else "✘"

        # Original list: [Ability, Spell Name, Has CC?, CC Type, Cooldown, Description]
        ability_info.append([
            "",  # Placeholder for Ability (removed)
            spell_name,
            cc_indicator,
            cc_type,
            cooldown_final,
            first_sentence
        ])
    return ability_info

def main():
    """Runs the interactive terminal game."""
    champions = load_champion_data()
    print("\n🔥 Welcome to the League of Legends Champion CC Explorer! 🔥")
    print('Type a champion\'s name to view their abilities and CC effects.')
    print('Type "exit" to quit.\n')
    
    while True:
        user_input = input("Enter a champion's name: ").strip().lower()
        if user_input == "exit":
            print("\n👋 Thanks for playing! Goodbye.")
            break
        if user_input in champions:
            champion = champions[user_input]
            ability_info = extract_cc_info(champion)
            # Prepare rows; if the ability has CC (cc_indicator == "✔"), color entire row.
            # Remove the Ability (index 0) and Has CC? (index 2) columns.
            colored_info = []
            for row in ability_info:
                new_row = [row[1], row[3], row[4], row[5]]  # Spell Name, CC Type, Cooldown, Description
                if row[2] == "✔":
                    row_color = get_row_bg_color(row[3])
                    colored_row = [f"{row_color}{cell}{RESET}" for cell in new_row]
                    colored_info.append(colored_row)
                else:
                    colored_info.append(new_row)
            
            print(f"\n📜 {champion['name']} - {champion['title']}\n")
            table = tabulate(
                colored_info,
                tablefmt="grid",
                colalign=("left", "left", "center", "left")
            )
            print(table, "\n")
        else:
            print("\n⚠️ Champion not found! Make sure you typed it correctly.\n")

if __name__ == "__main__":
    main()
