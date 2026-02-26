# app.py
import tkinter as tk
from tkinter import ttk
from itertools import product
import threading
import time

from models import Team
from data_loader import load_champions

# --- Load Data ---
all_champions, role_pools = load_champions("champions.csv")
role_names = ["Top", "Jungle", "Mid", "Bot", "Support"]

# --- Challenges ---
group_names = ["Large AOE Ult", "Defy Death", "Poke", "Displacements",
               "2 or more CC", "Global", "Traps", "Heals/Shields",
               "Stealth", "Summon", "Terrain"]
group_required = [3]*11
class_name = "Variety's Overrated"
place_names = ["Bandle City","Bilgewater","Demacia","Freljord","Ionia","Ixtal","Noxus",
               "Piltover","Shadow Isles","Shurima","Targon","Void","Zaun"]

# --- GUI Setup ---
root = tk.Tk()
root.title("LOL Team Comp Builder")

selected_vars = [tk.StringVar(value="Select") for _ in role_names]
progress_var = tk.DoubleVar(value=0)
eta_var = tk.StringVar(value="ETA: 0s")

for i, role in enumerate(role_names):
    tk.Label(root, text=role).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    options = ["Select"] + [champ.name for champ in role_pools[i]]
    dropdown = ttk.Combobox(root, textvariable=selected_vars[i], values=options, state="readonly", width=22)
    dropdown.grid(row=i, column=1, padx=5, pady=5)

tk.Label(root, text="Required Challenges").grid(row=0, column=2, padx=5, pady=5)
req_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=15, width=25)
for challenge in group_names + [class_name] + place_names:
    req_listbox.insert(tk.END, challenge)
req_listbox.grid(row=1, column=2, rowspan=5, padx=5, pady=5)

output_text = tk.Text(root, width=80, height=15)
output_text.grid(row=8, column=0, columnspan=3, padx=5, pady=10)

progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.grid(row=6, column=0, columnspan=3, pady=5)
eta_label = tk.Label(root, textvariable=eta_var)
eta_label.grid(row=7, column=0, columnspan=3, pady=5)

cancel_flag = False

# -------------------------
# Auto Generator
# -------------------------
def auto_generate_with_locks(selected_champs, required_challenges):
    global cancel_flag
    best_team = None
    best_score = -1

    open_role_indexes = [i for i, champ in enumerate(selected_champs) if champ is None]
    if not open_role_indexes:
        team = Team(selected_champs)
        score = team.calculate_score(group_names, group_required, class_name, place_names, required_challenges)
        return team, score

    open_pools = [role_pools[i] for i in open_role_indexes]
    total_combos = 1
    for pool in open_pools: total_combos *= len(pool)
    checked = 0
    start_time = time.time()
    update_every = max(1, total_combos // 100)

    for combo in product(*open_pools):
        if cancel_flag: return None, None
        checked += 1

        if checked % update_every == 0:
            elapsed = time.time() - start_time
            progress = checked / total_combos * 100
            eta_seconds = int((elapsed / checked) * (total_combos - checked))
            root.after(0, lambda p=progress, e=eta_seconds: update_progress(p, e))

        team_champs = selected_champs.copy()
        for idx, role_index in enumerate(open_role_indexes):
            team_champs[role_index] = combo[idx]

        if len(set(team_champs)) < 5: continue

        team = Team(team_champs)
        score = team.calculate_score(group_names, group_required, class_name, place_names, required_challenges)

        if required_challenges and not team.valid: continue

        if score > best_score:
            best_score = score
            best_team = team

    return best_team, best_score

# -------------------------
# GUI Functions
# -------------------------
def update_progress(progress, eta_seconds):
    progress_var.set(progress)
    eta_var.set(f"ETA: {eta_seconds}s")

def auto_generate_button():
    global cancel_flag
    cancel_flag = False
    generate_button.config(state="disabled")
    cancel_button.config(state="normal")
    progress_var.set(0)
    eta_var.set("ETA: 0s")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Generating best team...\n")

    selected_champs = []
    for i in range(5):
        name = selected_vars[i].get()
        if name == "Select":
            selected_champs.append(None)
        else:
            champ = next((c for c in role_pools[i] if c.name == name), None)
            selected_champs.append(champ)

    required_challenges = [req_listbox.get(i) for i in req_listbox.curselection()]
    thread = threading.Thread(target=run_generation, args=(selected_champs, required_challenges), daemon=True)
    thread.start()

def run_generation(selected_champs, required_challenges):
    best_team, best_score = auto_generate_with_locks(selected_champs, required_challenges)
    root.after(0, lambda: finish_generation(best_team, best_score))

def finish_generation(best_team, best_score):
    cancel_button.config(state="disabled")
    generate_button.config(state="normal")
    progress_var.set(0)
    eta_var.set("ETA: 0s")
    output_text.delete("1.0", tk.END)

    if best_team is None:
        output_text.insert(tk.END, "Generation cancelled or no valid team found.\n")
        return

    for i, champ in enumerate(best_team.champions):
        selected_vars[i].set(champ.name)

    output_text.insert(tk.END, "Best Team:\n")
    output_text.insert(tk.END, f"{best_team}\n\n")
    output_text.insert(tk.END, f"Score: {best_score}\n")
    output_text.insert(tk.END, "Completed Challenges:\n")
    for challenge in best_team.completed_challenges:
        output_text.insert(tk.END, f"- {challenge}\n")

def cancel_generation():
    global cancel_flag
    cancel_flag = True
    output_text.insert(tk.END, "\nCancelling...\n")

# -------------------------
# Buttons
# -------------------------
generate_button = tk.Button(root, text="Auto Generate Best Team", command=auto_generate_button, width=28)
generate_button.grid(row=5, column=0, pady=10)
cancel_button = tk.Button(root, text="Cancel", command=cancel_generation, width=12, state="disabled")
cancel_button.grid(row=5, column=1, pady=10)

root.mainloop()