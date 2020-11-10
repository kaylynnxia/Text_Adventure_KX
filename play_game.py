import json
import time
import random

def main():
    # TODO: allow them to choose from multiple JSON files?
    #with open('spooky_mansion.json') as fp:
    with open(files_to_play()) as fp:
        game = json.load(fp)
    print_instructions()
    start = start_time()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)
    time_elapsed(start)

def find_non_win_rooms(game):
    keep = []
    for room_name in game.keys():
        # skip if it is the "fake" metadata room that has title & start
        if room_name == '__metadata__':
            continue
        # skip if it ends the game
        if game[room_name].get('ends_game', False):
            continue
        # keep everything else:
        keep.append(room_name)
    return keep

def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    #current_place = "balcony"
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    #cat_place = "kitchen"
    visited = {}

    while True:
        print("")
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])
        
        cat_rooms = find_non_win_rooms(rooms)
        current_cat_room = random.choice(cat_rooms)
        
        if current_cat_room == current_place:
            print("--------There is a cat in here!--------")
        #print(current_cat_room)
        
        if current_place in visited:
            print("...You've been in this room before.")
        visited[current_place] = True
            
        
        # TODO: print any available items in the room...
        if here["items"] == []:
            print(" ")
        else:
            print("The item available is", here["items"])
        # e.g., There is a Mansion Key.

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        
        if action == "help":
            print_instructions()
            continue

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        if action == "stuff":
            if len(stuff) > 0:
                for item in stuff:
                    print(item)
            else:
                print("You have no items.")
            continue
        
        # TODO: if they type "take", grab any items in the room.
        if action == "take":
            for item in here["items"]:
                stuff.append(item)
            here["items"] = []
            continue
            
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        if action == "search" or action == "find":
            for item in here["exits"]:
                if "hidden" in item:
                    if item["hidden"] == True:
                        item["hidden"] = False
            continue
        
        #Drop an item
        if action == "drop":
            stuff_dict = dict()
            counter = 1
            for item in stuff:
                stuff_dict[counter] = item
                counter += 1
            print(stuff_dict)
            item_drop = int(input("What item number do you want to drop? Your items are above:"))
            if item_drop in stuff_dict:
                dropping = stuff.pop(item_drop-1)
                here["items"].append(dropping)
            else:
                print("Whoops, item not found!")
            continue
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")

import os, sys
def files_to_play():
    dirs = os.listdir()
    file_list = []
        
    for file in dirs:
        if file.endswith(".json"):
            file_list.append(file)
    count = 1
    new_file_list = dict()
    for item in file_list:
        new_file_list[count] = item
        count += 1
    print("Here are your options:")
    print(new_file_list)
    user = int(input("Which number would you like? "))
    if user in new_file_list:
        return new_file_list[user]
    else:
        print("Whoops! Game not found!")
        files_to_play()
        
def start_time():
    start = time.time()
    return start

def time_elapsed(start):
    elapsed = time.time()-start
    minutes = elapsed//60
    seconds = elapsed - (60 * minutes)
    print("The game took you", minutes, "minutes, and", seconds, "seconds")
    
def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.
    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        if "required_key" in exit:
            if exit["required_key"] in stuff:
                usable.append(exit)
            continue
        usable.append(exit)
    return usable

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'drop' to drop an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' or 'find' to take a deeper look at a room.")
    print(" - Type 'help' to see the instructions again.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()
