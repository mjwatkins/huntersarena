from random import randint

class Dice():
    """Creates a dice of selected size and also roles it"""

    def __init__(self,maxvalue):
        self.max = maxvalue


    def roll(self):
        """Roll a die and get random result between 1 and te maximum value"""
        return randint(1,self.max)

    def roll_dice_pool(self,numberofdice):
        """roll multiple dice and get total value"""
        sum = 0 
        for i in range(0,numberofdice):
            sum = sum + self.roll()

        return sum

    

        
            

    
    
