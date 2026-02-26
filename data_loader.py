# data_loader.py
import csv
import sys
import os
from models import Champion

def get_csv_path(filename):
    """Return path to CSV inside PyInstaller bundle or normal script"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return filename

def load_champions(csv_file):
    csv_file = get_csv_path(csv_file)

    all_champions = []
    top_pool, jungle_pool, mid_pool, bot_pool, support_pool = [], [], [], [], []

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            name = row[0]
            groups  = [row[i].strip().lower() == "yes" for i in range(1, 12)]
            classes = [row[i].strip().lower() == "yes" for i in range(12, 18)]
            roles   = [row[i].strip().lower() == "yes" for i in range(18, 23)]
            places  = [row[i].strip().lower() == "yes" for i in range(23, 36)]

            champ = Champion(name, groups, classes, places, roles)
            all_champions.append(champ)

            if roles[0]: top_pool.append(champ)
            if roles[1]: jungle_pool.append(champ)
            if roles[2]: mid_pool.append(champ)
            if roles[3]: bot_pool.append(champ)
            if roles[4]: support_pool.append(champ)

    role_pools = [top_pool, jungle_pool, mid_pool, bot_pool, support_pool]
    return all_champions, role_pools