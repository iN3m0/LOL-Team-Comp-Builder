
class Champion:
    def __init__(self, name, groups, classes, places, roles):
        self.name = name
        self.groups = groups
        self.classes = classes
        self.places = places
        self.roles = roles

    # Helper methods

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

    # champions is a list of 5 Champion objects in the order of [Top, Jungle, Mid, Bot, Support]
    def __init__(self, champions):
        if len(champions) != 5:
            raise ValueError("A team must consist of exactly 5 champions.")
        self.champions = champions

    # --- Trait Helpers ---

    # Return the champion in the specified role index (0-4)
    def champ_at(self, index):
        return self.champions[index]

    # Check if any champion in the team belongs to the specified group index
    def has_group(self, index):
        return any(champ.groups[index] for champ in self.champions)

    # Check how many champions in the team belong to the specified group index
    def count_group(self, index):
        return sum(champ.is_in_group(index) for champ in self.champions)

    # Check if any champion in the team belongs to the specified class index
    def has_class(self, index):
        return any(champ.classes[index] for champ in self.champions)

    # Check how many champions in the team belong to the specified class index
    def count_class(self, index):
        return sum(champ.is_in_class(index) for champ in self.champions)

    # Check if any champion in the team belongs to the specified place index
    def has_place(self, index):
        return any(champ.places[index] for champ in self.champions)
    
    # Check how many champions in the team belong to the specified place index
    def count_place(self, index):
        return sum(champ.is_in_place(index) for champ in self.champions)

    # --- Scoring Method ---

    def calculate_score(self, group_names, group_required,
                        class_name="Variety's Overrated", place_names=None):
        
        # Calculates the total score of the team and stores completed challenges.
        # - group_names: list of group challenge names
        # - group_required: list of required counts per group
        # - class_name: name of class challenge
        # - place_names: list of place challenge names

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

        return self.score

    def __repr__(self):
        return ", ".join(f"{role}: {champ.name}" for role, champ in zip(self.ROLE_NAMES, self.champions))
