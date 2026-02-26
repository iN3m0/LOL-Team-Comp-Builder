import csv
from models import Champion

GROUP_COUNT = 11
CLASS_COUNT = 6
PLACE_COUNT = 13
ROLE_COUNT = 5

def load_champions(csv_file):
    all_champions = []
    top_pool = []
    jungle_pool = []
    mid_pool = []
    bot_pool = []
    support_pool = []

    with open(csv_file, newline='', encoding= 'utf-8') as f:
        reader = csv.reader(f)
        next(reader) # Skip header row

        for row in reader:
            name = row[0]

            # Convert yes/no values to boolean lists
            groups  = [row[i].strip().lower() == "yes" for i in range(1, 12)]
            classes = [row[i].strip().lower() == "yes" for i in range(12, 18)]
            roles   = [row[i].strip().lower() == "yes" for i in range(18, 23)]
            places  = [row[i].strip().lower() == "yes" for i in range(23, 36)]

            champ = Champion(name, groups, classes, places, roles)
            all_champions.append(champ)

            # Add to role pools
            if roles[0]: # Top role
                top_pool.append(champ)
            if roles[1]: # Jungle role
                jungle_pool.append(champ)
            if roles[2]: # Mid role
                mid_pool.append(champ)
            if roles[3]: # Bot role
                bot_pool.append(champ)
            if roles[4]: # Support role
                support_pool.append(champ)

    role_pools = [top_pool, jungle_pool, mid_pool, bot_pool, support_pool]

    return all_champions, role_pools