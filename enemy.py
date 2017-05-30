from character import Character
from equipment import Weapon,Armor
from dice import Dice

class Enemy(Character):
    def __init__(self,name,roundnum):
        """creaes random enemy"""
        super(Enemy,self).__init__(name)
        self.roll_character()
        factor = Dice(roundnum)
        base = roundnum
        for stat,value in self.stats.items():
            if factor.roll() >= 2:
                self.stats[stat] = value + factor.roll()

    
                


        
        
        
        
