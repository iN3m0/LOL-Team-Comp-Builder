
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

    # Return the champion in the specified role index (0-4)
    def champ_at(self, index):
        return self.champions[index]

    def __repr__(self):
        return ", ".join(f"{role}: {champ.name}" for role, champ in zip(self.ROLE_NAMES, self.champions))