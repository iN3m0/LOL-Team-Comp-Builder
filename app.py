# main.py
from models import Champion, Team
from data_loader import load_champions

all_champions, role_pools = load_champions("champions.csv")
print(f"Loaded {len(all_champions)} champions.\n")

# --- 2. Challenge data ---
group_names = ["Large AOE Ult", "Defy Death", "Poke", "Displacements", "2 or more CC",
               "Global", "Traps", "Heals/Shields", "Stealth", "Summon", "Terrain"]
group_required = [3]*11
class_name = "Variety's Overrated"
place_names = ["Bandle City","Bilgewater","Demacia","Freljord","Ionia","Ixtal","Noxus",
               "Piltover","Shadow Isles","Shurima","Targon","Void","Zaun"]

# --- 3. Map role names to pools ---
role_names = ["Top", "Jungle", "Mid", "Bot", "Support"]
selected_champions = []

# --- 4. User selects one champion per role ---
for i, role in enumerate(role_names):
    available = role_pools[i]
    print(f"\nAvailable champions for {role}: {[c.name for c in available]}")
    
    choice = None
    while choice is None:
        name_input = input(f"Select champion for {role}: ").strip()
        for champ in available:
            if champ.name.lower() == name_input.lower():
                choice = champ
                break
        if choice is None:
            print("Invalid choice. Try again.")
    
    selected_champions.append(choice)

# --- 5. Create team ---
team = Team(selected_champions)

# --- 6. Calculate score ---
score = team.calculate_score(group_names, group_required, class_name, place_names)

# --- 7. Display results ---
print("\nTeam Composition:")
print(team)
print(f"\nTeam Score: {score}")
print(f"Completed Challenges: {team.completed_challenges}")