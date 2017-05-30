#!/usr/bin/python
from arenaengine import ArenaEngine
from character import Character


print("**********\n")
print("Huner's Arena")
print("Version 0.2")
print("Developer: Maurice J. Watkins")
print("**********\n")

#initial key components

command = "New Game"
engine = ArenaEngine(Character("Sam"), 1)

#primary game loop
while True:
    engine.accept_command(command)
    if (engine.gameover == True):
        break;
    try:
        print("Valid Commands:" + str(engine.COMMAND_PROMPT))
        command = raw_input(engine.mainchar.get_prompt())
    except SyntaxError:
        print("Please enter a command. Current status")
        command = "Stats"
        
    
