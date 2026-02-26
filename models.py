# models.py
class Champion:
    def __init__(self, name, groups, classes, places, roles):
        self.name = name
        self.groups = groups
        self.classes = classes
        self.places = places
        self.roles = roles

    # Groups are in order of Large AOE Ult, Defy Death, Poke, Displacements, 2 or more CC, Global, Traps, Heals/Shields, Stealth, Summon, Terrain
    def is_in_group(self, index):
        return self.groups[index]
    
    # Classes are in order of Assassin, Fighter, Mage, Marksman, Support, Tank
    def is_in_class(self, index):
        return self.classes[index]

    # Places are in order of Bandle City, Bilgewater, Demacia, Freljord, Ionia, Ixtal, Noxus, Piltover, Shadow Isles, Shurima, Targon, Void, Zaun
    def is_in_place(self, index):
        return self.places[index]

    # Roles are in order of Top, Jungle, Mid, Bot, Support
    def is_in_role(self, index):
        return self.roles[index]
    
    def __repr__(self):
        return self.name


class Team:
    ROLE_NAMES = ["Top", "Jungle", "Mid", "Bot", "Support"]

    # champions: list of 5 Champion objects in order [Top, Jungle, Mid, Bot, Support]
    def __init__(self, champions):
        if len(champions) != 5:
            raise ValueError("A team must consist of exactly 5 champions.")
        self.champions = champions

    # --- Trait Helpers ---
    def champ_at(self, index):
        return self.champions[index]

    def count_group(self, index):
        return sum(champ.is_in_group(index) for champ in self.champions)

    def count_class(self, index):
        return sum(champ.is_in_class(index) for champ in self.champions)

    def count_place(self, index):
        return sum(champ.is_in_place(index) for champ in self.champions)

    # --- Scoring Method ---
    def calculate_score(self, group_names, group_required,
                        class_name="Variety's Overrated",
                        place_names=None,
                        required_challenges=None):

        self.score = 0
        self.completed_challenges = []

        # Group challenges
        for i, name in enumerate(group_names):
            if self.count_group(i) >= group_required[i]:
                self.score += 1
                self.completed_challenges.append(name)

        # Class challenge (5 champions in same class)
        for i in range(6):
            if self.count_class(i) >= 5:
                self.score += 1
                self.completed_challenges.append(class_name)

        # Place challenges
        if place_names:
            for i, name in enumerate(place_names):
                if self.count_place(i) >= 5:
                    self.score += 1
                    self.completed_challenges.append(name)

        # Check required challenges
        if required_challenges:
            self.valid = all(ch in self.completed_challenges for ch in required_challenges)
        else:
            self.valid = True

        return self.score

    def __repr__(self):
        return ", ".join(f"{role}: {champ.name}" for role, champ in zip(self.ROLE_NAMES, self.champions))