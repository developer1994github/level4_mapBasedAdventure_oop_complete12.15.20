class Player:
    def __init__(self, location, inventory):
        self.location = location
        self.inventory = inventory
    def move(self, new_location):
        self.location = new_location
        self.look()
    def look(self):
        self.location.describe()
    def get_inventory(self):
        if len(self.inventory) > 0:
            for item in self.inventory:
                print('You are carrying a {}.'.format(item))
        else:
            print("You are not carrying anything.")

class Room:
    def __init__(self,name, description):
        self.name = name
        self.directions = {}
        self.description = description
        self.items = {}
    def describe(self):
        print(self.description)
        if len(self.items) > 0:
            for item in self.items:
                print("There is a {} here.".format(item))

class Item:
    def __init__(self,name,use_rooms, message, ends_game):
        self.name = name
        #rooms where the item can be used
        self.use_rooms = use_rooms
        self.message = message
        #boolean to tell whether or not using the item will trigger game over
        self.ends_game = ends_game
    def use_item(self, location):
        if location in self.use_rooms:
            print(self.message)
            return self.ends_game
        else:
            print("You cannot use a {} here".format(self.name))





#set up global variables
game_over = False
#create rooms
cabin = Room('cabin','You are in a quaint cabin, there is a door to the east.')
yard = Room('yard','You find yourself in a beautiful garden. There is a forest to the east, abarn to the south, and a cabin to the west.')
forest = Room("forest",'You are in a spooky forest. The yard is back to the west.')
barn = Room("barn",'You are in a barn. There is a locked treasure chest in the middle of theroom. The yard lies to the north.')
#create map
cabin.directions = {'east': yard}
yard.directions = {'east':forest,'south':barn, "west":cabin}
forest.directions = {'west':yard}
barn.directions = {'north':yard}
#create player
player = Player(cabin, {})
#create the key
key = Item('key',[barn],'You unlocked the treasure chest! You win!',True)
#add the key to the forest
forest.items = {key.name: key}




#update the player's location
def move(direction):
    if direction in player.location.directions:
        player.move(player.location.directions[direction])
    else:
        print("You cannot go {}.".format(direction))

#pick up items and add them to the player's inventory
def get_item(item):
    if item in player.location.items:
        player.inventory[item] = player.location.items[item]
        del player.location.items[item]
        print("You picked up the {}.".format(item))
        return
    print("There is no {} here.".format(item))

#remove items from the players inventory
def drop_item(item):
    if item in player.inventory:
        player.location.items[item] = player.inventory[item]
        del player.inventory[item]
        print("You are no longer carrying the {}.".format(item))
        return
    print("You can't get rid of something you don't have.")

#use items from the player's inventory
def use_item(item):
    global game_over
    if item in player.inventory:
        if(player.inventory[item].use_item(player.location)):
            game_over = True
        return
    print("You are not carrying a {}.".format(item))

#handle player input until the game ends
def main():
    global game_over
    player.look()
    while not game_over:
        choice = input("What would you like to do?\n").split(" ")
        if choice[0] == 'go':
            move(choice[1])
        elif choice[0] == 'get':
            get_item(choice[1])
        elif choice[0] == 'use':
            use_item(choice[1])
        elif choice[0] == 'drop':
            drop_item(choice[1])
        elif choice[0] == 'inventory':
            player.get_inventory()
        elif choice[0] == 'look':
            player.look()
        elif choice[0] == 'quit':
            game_over = True
        elif choice[0] == 'help':
            print("\nInstructions:\n")
            print("Enter 'go <'north', 'east', 'south', or 'west'>' to move.")
            print("Enter 'look' to view the room or 'inventory' to view your inventory.")
            print("Type 'get <item name>' to acquire items.")
            print("Type 'drop <item name>' to get rid of items.")
            print("Type 'use <item name>' to use items.")
            print("Type 'quit' to exit the game.\n")
        else:
            print("I do not understand {}.".format(choice[0]))
    print("Thanks for playing!")



if __name__ == '__main__':
    main()