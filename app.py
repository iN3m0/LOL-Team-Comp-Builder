from data_loader import load_champions

CSV_FILE = "champions.csv"

all_champions, role_pools = load_champions(CSV_FILE)

print(f"Total champions loaded: {len(all_champions)}")
print(f"Top role champions: {[c.name for c in role_pools[0]]}")
print(f"Jungle role champions: {[c.name for c in role_pools[1]]}")
print(f"Mid role champions: {[c.name for c in role_pools[2]]}")
print(f"Bot role champions: {[c.name for c in role_pools[3]]}")
print(f"Support role champions: {[c.name for c in role_pools[4]]}")