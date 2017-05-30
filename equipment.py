from random import randint
from dice import Dice

armors = {1:"Silk Armor", 2:"Leather Armor", 3:"Studded Leather Armor",
         4:"Bone Armor", 5:"Chain Mail", 6:"Ebony Armor",
         7:"King's Armor",8:"Plate Armor", 9:"Dragonscale Plate Armor",
         10:"Aegis Armor"}
weapons = {1:"Dagger",2:"Shortsword",3:"Longsword", 9:"WarHammer",8:"Great Axe",
                  4:"Broadsword",7:"Katana",10:"Claymore",5:"Axe",6:"Mace"}
traittypes = {"Strength":"Brutal","Speed":"Sleek","Constitution":"Heavy",
              "Skill":"Tactical"}

class Weapon ():

    def __init__(self,damage,trait):
        """Creates weapon of specific rarity"""
        self.damage = damage
        self.trait = trait
        self.name = weapons[damage]

    def get_damage(self):
        """Randomly calculates damage for weapon on attack"""
        die = Dice(self.damage)
        return die.roll()

    def get_description(self):
        """Gives colorful description of weapon"""
        return traittypes[self.trait] + " " + self.name

class Armor():
    """Armor provides defense to character"""
    def __init__(self,name, defense):
        self.defense = defense
        self.name = name

    def __init__(self,defense):
        self.defense = defense
        self.name = armors[defense]

    def get_description(self):
        """Give colorful description of armor"""
        return self.name
    

        


    
