from dice import Dice
from equipment import Weapon,Armor


class Character(object):
    """Stores all character data"""

    def __init__(self,name):
        """Sets up character"""
        self.name = name
        self.stats = {'Strength':1,'Speed':1,'Constitution':1,'Skill':1}
        self.equipment = {'Weapon': 0, 'Armor': 0}
        self.inventory = []
        self.skilllist = []
        self.rolled = False
        self.experience = 0
        self.hp = 0
        self.maxhp =0
        self.sp = 0
        self.maxsp = 0
        self.level = 1
        

    def roll_character(self):
        """Rolls initial stats"""
        die = Dice(4)
        for stat, value in self.stats.items():
            self.stats[stat] = die.roll()
            if stat == 'Constitution':
                self.hp = self.stats[stat] * 10
                self.maxhp = self.stats[stat] * 10
            if stat == 'Skill':
                self.sp = self.stats[stat] * 10
                self.maxsp = self.stats[stat]*10
        self.rolled = True


    def to_hit(self):
        """calculate to hit value for an attempt"""
        die = Dice(6)
        roll = self.stats['Skill'] + die.roll_dice_pool(self.stats['Speed'])
        return roll

    def calc_defense(self):
        """Gives defense rating"""
        defmod = 2
        if self.equipment['Armor'] != 0:
            return self.stats['Speed']*defmod + self.stats['Skill']
            + self.equipment['Armor'].defense
        else:
            return self.stats['Speed']*defmod + self.stats['Skill']
        
        

    
    def calc_damage(self):
        """Calculates damage for successful hit. Strength is effectively doubled on brutal weapon"""
        damage = 0
        if self.equipment['Weapon'] != 0:
             damage = self.equipment['Weapon'].get_damage() + self.stats[self.equipment['Weapon'].trait] + self.stats["Strength"]
        else:
            damage = self.stats["Strength"]
        return damage

    def is_ready_to_level(self): 
        """Determines if level needs to increase"""
        nextlevel = (self.level + 1)**2
        if self.experience >= nextlevel:
            return True
        else:
            return False

    def roll_initiative(self):
        """Roll to see how quickly character acts in battle"""
        die = Dice(self.stats["Speed"])
        return die.roll()

    def skill_check(self):
        """For determining contested skill checks"""
        die = Dice(self.stats["Skill"])
        return die.roll()

    def equip(self,item):
        """Equips an item and puts old one inventory"""
        if isinstance(item,Armor):
            oldarmor = self.equipment["Armor"]
            self.equipment["Armor"] = item
            if item in self.inventory:
                self.inventory.remove(item)
            if oldarmor != 0:
                self.inventory.append(oldarmor)
        elif isinstance(item,Weapon):
            oldweapon = self.equipment["Weapon"]
            self.equipment["Weapon"] = item
            if item in self.inventory:
                self.inventory.remove(item)
            if oldweapon !=0:
                self.inventory.append(oldweapon)
                

    def get_prompt(self):
        """Gives prompt describing character"""
        prompt = self.name + ": Lvl " +str(self.level)+" HP: "+str(self.hp)+" Exp: " +str(self.experience)+" >"
        return prompt


