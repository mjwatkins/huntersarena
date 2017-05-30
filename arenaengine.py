from character import Character
from enemy import Enemy
from equipment import Weapon,Armor
from dice import Dice

traits = ("Strength","Speed","Constitution","Skill")


class ArenaEngine():
    """Accepts commands and executes game funtions"""

    def __init__(self,currentcharacter, roundnum):
        self.mainchar = currentcharacter
        self.round = roundnum
        self.gameover = False
        self.nextenemy = 0
        self.victories =0
        self.COMMANDS = ("New Game","Fight","Next Round","Stats",
                         "Inventory")
        self.COMMAND_PROMPT = ("(F)ight", "(N)ext Round","(S)tats","(I)nventory")
        self.STATES = ("Startup","Management","Battle")
        self.currentstate = self.STATES[0]
        self.currentcommand = 0

    def accept_command(self,command):
        """Responds to user commands"""
        if self.currentstate == self.STATES[0]:
                self.execute_new_game()
        elif self.currentstate == self.STATES[1]:
            if command.lower() == self.COMMANDS[3].lower() or command.lower() == self.COMMANDS[3][0].lower() :
               self.execute_stats()
            elif command.lower() == self.COMMANDS[4].lower() or command.lower() == self.COMMANDS[4][0].lower() :
                self.execute_inventory()
            elif command.lower() == self.COMMANDS[2].lower() or command.lower() == self.COMMANDS[2][0].lower() :
                self.execute_next_round()
            elif command.lower() == self.COMMANDS[1].lower() or command.lower() == self.COMMANDS[1][0].lower() :
                self.execute_fight()
            #test for valid command input
        else: #self.currentstate == self.STATES[2]:
            #test for valid command input
            if command.lower() == self.COMMANDS[1].lower() or command.lower() == self.COMMANDS[1][0].lower() :
                self.execute_fight()
            
            
        

    def execute_new_game(self):
        """Sets up new game"""
        self.round = 1
        newname = raw_input("Name your character:")
        self.mainchar = Character(newname)
        self.mainchar.roll_character()
        defaultweapon = Weapon(1,traits[0])
        self.mainchar.equipment["Weapon"] = defaultweapon
        defaultarmor = Armor(1)
        self.mainchar.equipment["Armor"] = defaultarmor
        self.currentstate = self.STATES[1]
        print("Prepare to face 10 rounds of challengers.")
        print("You can face as many challengers in a round as you wish.")
        print("However, you mus defeat at least 5 before you can move on\n")

    def execute_next_round(self):
        """Moves to next round"""
        if self.victories >= 5:
            print("Round " + str(self.round) + " complete!!\n")
            self.round += 1
            if self.round < 11:
                print("Starting round " + str(self.round) + "\n")
                self.victories = 0
                self.mainchar.hp = self.mainchar.maxhp
                self.mainchar.sp = self.mainchar.maxsp
            else:
                print("You WIN!!")
                self.gameover = True
                self.currentState = self.STATES[0]
                #Consider adding output of chracter stats
        else: 
            print("Not enough victories! Keep fighting.\n")
            

    def execute_stats(self):
        """Displays character stats"""
        print("********\n")
        print(self.mainchar.name + " Level " + str(self.mainchar.level) +
              " \n")
        for trait in traits:
            print(trait + ": "+  str(self.mainchar.stats[trait]) + "\n")

        print("Total Experience: " + str(self.mainchar.experience))
        print("Next Level at: " + str((self.mainchar.level+1)**2))
        print("Victories: " + str(self.victories))
        print("********\n")

        while self.mainchar.experience >= (self.mainchar.level+1)**2:
        #if self.mainchar.experience >= (self.mainchar.level+1)**2: #self.mainchar.is_ready_to_level:
            print("You have gained a level\n What stat would you like to" +
                  " increase\n")
            choice = raw_input("Str, Speed, Con, Skill:")
            if choice.lower() == "str":
                self.mainchar.stats["Strength"] += 1
                print("Stat increased by one \n")
                self.mainchar.level += 1
            elif choice.lower() == "speed": 
                self.mainchar.stats["Speed"] += 1
                print("Stat increased by one \n")
                self.mainchar.level += 1
            elif choice.lower() == "con":
                self.mainchar.stats["Constitution"] += 1
                self.mainchar.maxhp += 10
                self.mainchar.hp += 10
                print("Stat increased by one \n")
                self.mainchar.level += 1
            elif choice.lower() == "skill":
                self.mainchar.stats["Skill"] += 1
                self.mainchar.sp += 10
                self.mainchar.maxsp += 10
                print("Stat increased by one \n")
                self.mainchar.level += 1
            else:
                print("Not a valid request")
                break
                
            
    def execute_inventory(self):
        """Allows selection of inventory"""
        #display all items
        print("Equipment: ")
        for key,value in self.mainchar.equipment.items():
            print(value.get_description() + "\n")
        print("Inventory: ")
        for item in self.mainchar.inventory:
            print(item.get_description() + "\n")
        #prompt for action: equip, exit...consider adding drop
        options = ("(1) Equip,(2) Drop,(3) Exit \n")
        choice = raw_input(options)
        if choice == "1":
            whichone = raw_input("Name the Item you would like to wear \n")
            found = False
            for item in self.mainchar.inventory:
                if whichone.lower() == item.get_description().lower():
                    self.mainchar.equip(item)
                    print("You have equipped " + item.get_description())
                    found = True
            if not found:
                print("You don't have that in your inventory")
        elif choice == '2':
            whichone = raw_input("Name the Item you would like to drop \n")
            found = False
            for item in self.mainchar.inventory:
                if whichone.lower() == item.get_description().lower():
                    self.mainchar.inventory.remove(item)
                    print("You have dropped: " + item.get_description())
                    found = True
                    break
            if not found:
                print("You don't have that")           
                
        
                
    def execute_fight(self):
        """Starts Battle state"""
        #create enemy and display
        self.generate_enemy()
        victorious = False
        print("You have encountered a " + self.nextenemy.name + "\n")
        #give choices of action
        options = "(1) Attack, (2) Flee \n"
        #action loop
        while self.nextenemy.hp > 0 and self.mainchar.hp > 0:
            choice = raw_input(options)
            maininit = self.mainchar.roll_initiative()
            foeinit = self.nextenemy.roll_initiative()
            #attack sequence with messages
            if choice == "1":
                #describe round of battle
                if maininit > foeinit:
                    damage = self.attack_attempt(self.mainchar,self.nextenemy)
                    hitdesc = " strikes "
                    if damage == 0:
                        hitdesc = " misses "
                    print(self.mainchar.name + hitdesc + self.nextenemy.name
                          + " for " + str(damage) + " damage")
                    if self.nextenemy.hp <= 0 and self.mainchar.hp > 0:
                        victorious = True
                        break
                    damage = self.attack_attempt(self.nextenemy,self.mainchar)
                    hitdesc = " strikes "
                    if damage == 0:
                        hitdesc = " misses "                    
                    print(self.nextenemy.name + hitdesc + self.mainchar.name
                          + " for " + str(damage) + " damage")
                else: 
                    damage = self.attack_attempt(self.nextenemy,self.mainchar)
                    hitdesc = " strikes "
                    if damage == 0:
                        hitdesc = " misses "
                    print(self.nextenemy.name + hitdesc + self.mainchar.name
                          + " for " + str(damage) + " damage")
                    if self.nextenemy.hp <= 0 and self.mainchar.hp > 0:
                        victorious = True
                        break
                    damage = self.attack_attempt(self.mainchar, self.nextenemy)
                    hitdesc = " strikes "
                    if damage == 0:
                        hitdesc = " misses "
                    print(self.mainchar.name + hitdesc + self.nextenemy.name
                          + " for " + str(damage) + " damage")
            elif choice == "2":  #choice 2 flee
                if maininit >foeinit:
                    #successful flee
                    print("You flee the battle \n")
                    break;
                else: 
                    #failed fleeing
                    print("You failed to flee the battle \n")
            #special attack
            else:
                #invalid choice
                print("Not a valid option...it is time to do battle \n")
            #if battle not over show enemy stats  based on skill check
            if self.mainchar.skill_check() >= self.nextenemy.skill_check():
                print(self.nextenemy.name + " has "+ str(self.nextenemy.hp)+
                      " hit points \n")
            else:
                print(self.nextenemy.name + " is concealing the extent of his injuries... \n")
            #if battle not over show character vital prompt
            print(self.mainchar.get_prompt())
            
        if self.nextenemy.hp <=0 and self.mainchar.hp > 0:
            #catch all to make sure victory conditions are properly met
            victorious = True
        

        if victorious == True:
            #if battle over,(win) - give exp and reward if enemy has something
            self.mainchar.experience += self.nextenemy.experience
            print("Victory. You earn "+str(self.nextenemy.experience) +" exp\n")
            self.victories += 1
            if len(self.nextenemy.inventory) > 0:
                isnew = True
                newitem=self.nextenemy.inventory.pop()
                for item in self.mainchar.inventory:
                    if item.name == newitem.name:
                        isnew = False
                if isnew:
                    self.mainchar.inventory.append(newitem)
                    print("New item added to inventory!! "+newitem.get_description())
                self.state = self.STATES[1]
            print(self.mainchar.get_prompt())
        elif self.mainchar.hp <= 0:
            #if battle over,(loss) - game over, go to start up state
            print("You lose. You will be remembered.. \n")
            self.gameover = True;
            
            self.state = self.STATES[0]
        else: #if fled
            self.state = self.STATES[1]
            print(self.mainchar.get_prompt())
            

        
        

    def generate_enemy(self):
        """Creates Enemy"""
        types = ("Spider","Snake","Wolf","Bear", "Rhino", "Panther", "Lion",
                 "Griffin","Dragon","Legendary Hydra")

        die = Dice(self.round)
        enemynum = die.roll()
        self.nextenemy = Enemy(types[enemynum-1],enemynum)
        for key,value in self.nextenemy.stats.items():
            self.nextenemy.stats[key] = enemynum
        #compensate for default armor
        self.nextenemy.stats[traits[0]] += 1
        self.nextenemy.level = enemynum
        self.nextenemy.experience = enemynum
        die = Dice(10)
        if die.roll() == 10:
            if die.roll() > 5:
                traitdie = Dice(4)
                self.nextenemy.inventory.append(Weapon(enemynum,traits[traitdie.roll()-1]))
            else:
                self.nextenemy.inventory.append(Armor(enemynum))

        hpmod =5
        if enemynum > 4:
            hpmod = 10
        elif enemynum > 9:
            hpmod = 20 #end game bonus to enemy health
            self.nextenemy.stats["Strength"] += 5 #end game damage output increased
        self.nextenemy.hp = hpmod * self.nextenemy.stats["Constitution"]

                                        
    def attack_attempt(self,attacker,defender):
        """Calculates hit success and applies damage if needed"""
        if attacker.to_hit() >= defender.calc_defense():
            armorvalue = 0
            if defender.equipment["Armor"] != 0:
                armorvalue = defender.equipment["Armor"].defense
            damage = attacker.calc_damage() - armorvalue
            if damage > 0:
                defender.hp -= damage
            return damage
        else:
            return 0


        
        
        
        
        
