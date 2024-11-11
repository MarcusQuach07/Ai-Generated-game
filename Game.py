import random

# 1. Character Creation
class Character:
    def __init__(self, name, character_class):
        self.name = name  # Player's name
        self.character_class = character_class  # Player's chosen class (Warrior, Mage, Rogue)
        self.health = 100  # Initial health
        self.max_health = 100  # Max health, which will increase upon leveling up
        self.strength = 10  # Base strength attribute
        self.agility = 10  # Base agility attribute
        self.magic = 10  # Base magic attribute
        self.inventory = []  # List to store the player's items
        self.level = 1  # Starting level
        self.experience = 0  # Starting experience

        # Class-specific attribute adjustments
        if self.character_class == "Warrior":
            self.strength += 5
            self.agility += 2
        elif self.character_class == "Mage":
            self.magic += 5
            self.strength += 2
        elif self.character_class == "Rogue":
            self.agility += 5
            self.strength += 2

    # Method to handle damage taken by the character
    def take_damage(self, damage):
        self.health -= max(damage, 0)  # Prevent negative damage
        print(f"{self.name} takes {damage} damage! Health remaining: {self.health}/{self.max_health}")

    # Method to handle gaining experience and leveling up
    def gain_experience(self, amount):
        self.experience += amount
        print(f"{self.name} gained {amount} experience!")
        # Level up if experience reaches the required threshold
        if self.experience >= 100 * self.level:
            self.level_up()

    # Method to handle leveling up
    def level_up(self):
        self.level += 1  # Increase the level
        self.experience = 0  # Reset experience after leveling up
        self.strength += 2  # Increase attributes
        self.agility += 2
        self.magic += 2
        self.max_health += 10  # Increase max health
        self.health = self.max_health  # Restore health to max
        print(f"{self.name} leveled up to level {self.level}! Stats increased.")

    # Method to handle using an item from the inventory
    def use_item(self, item):
        if item in self.inventory:
            print(f"{self.name} uses {item}")
            self.inventory.remove(item)  # Remove the item from inventory after use
            return True
        else:
            print(f"{item} not found in inventory.")
            return False

# 2. World and Story Progression
class World:
    def __init__(self, player):
        self.player = player  # The player character
        # Locations with possible actions the player can take
        self.locations = {
            "Haunted Forest": ["Explore the haunted woods", "Fight the ghostly apparition", "Leave the forest"],
            "Enchanted Castle": ["Investigate the castle", "Fight the enchanted knight", "Talk to the wizard"],
            "Bandit's Lair": ["Sneak through the lair", "Fight the bandits", "Talk to the bandit leader"]
        }

    # Method to start traveling through the world and encounter locations
    def travel(self):
        while self.player.health > 0:  # Game continues until the player's health reaches zero
            print(f"\nCurrent Location: {self.player.character_class}")
            print("Choose a location to explore:")
            # List all locations and allow the player to choose one
            for index, location in enumerate(self.locations.keys(), 1):
                print(f"{index}. {location}")
            choice = input("Enter the number of the location you wish to visit: ")

            # Handle the player's location choice
            if choice == "1":
                self.location_encounter("Haunted Forest")
            elif choice == "2":
                self.location_encounter("Enchanted Castle")
            elif choice == "3":
                self.location_encounter("Bandit's Lair")
            else:
                print("Invalid location, please try again.")
        print("Game over! You died.")  # End the game if health is zero

    # Method to handle encounters at a given location
    def location_encounter(self, location):
        print(f"\nYou are now in the {location}!")
        actions = self.locations[location]  # Actions available at the location
        # List the possible actions the player can take
        for idx, action in enumerate(actions, 1):
            print(f"{idx}. {action}")
        
        # Prompt for action choice
        action_choice = input("Choose an action (number): ")
        if action_choice == "1":
            self.encounter("combat")  # Trigger combat encounter
        elif action_choice == "2":
            self.encounter("talk")  # Trigger NPC interaction
        else:
            print("Invalid action choice.")

    # Method to trigger an encounter
    def encounter(self, type):
        if type == "combat":
            self.combat()  # Call the combat method
        elif type == "talk":
            print("Talking to NPC...")  # Placeholder for NPC interaction

    # Method to handle combat between the player and an enemy
    def combat(self):
        # Enemy stats are randomly generated for each combat encounter
        enemy_health = random.randint(50, 100)
        enemy_damage = random.randint(10, 20)

        print(f"\nAn enemy appears! It has {enemy_health} health.")
        # Combat loop continues until either the player or the enemy is defeated
        while enemy_health > 0 and self.player.health > 0:
            action = input("Choose action: (Attack/Defend/Use Item): ").lower()
            # Player can attack, defend, or use an item
            if action == "attack":
                damage = random.randint(self.player.strength, self.player.strength + 5)
                enemy_health -= damage
                print(f"You attack the enemy for {damage} damage.")
            elif action == "defend":
                print(f"You defend yourself!")  # Placeholder for defensive actions
            elif action == "use item":
                item = input("Enter item name to use: ")
                self.player.use_item(item)  # Call the player's use_item method
            else:
                print("Invalid action. Please try again.")
            
            # Enemy attacks after the player action
            if enemy_health > 0:
                self.player.take_damage(enemy_damage)

        # Check if the player or the enemy was defeated
        if self.player.health <= 0:
            print("You have been defeated!")
        else:
            print("You defeated the enemy!")
            self.player.gain_experience(50)  # Gain experience for defeating the enemy

# 3. Inventory and Items
class Item:
    def __init__(self, name, use_effect):
        self.name = name  # Item name
        self.use_effect = use_effect  # Effect the item has when used (e.g., health restoration)

    # Method to use the item, affecting the player's health
    def use(self, player):
        print(f"{player.name} uses {self.name}.")
        player.health = min(player.max_health, player.health + self.use_effect)  # Restore health without exceeding max

# 4. Branching Choices and Endings
class Endings:
    def __init__(self):
        # List of possible game endings
        self.endings = [
            "You became the ruler of the kingdom after defeating the dark wizard!",
            "You allied with the dragon and watched as the world fell into chaos.",
            "You died in the haunted forest, never to be seen again."
        ]

    # Method to randomly choose a game ending
    def random_ending(self):
        return random.choice(self.endings)

# 5. Error Handling
def game_loop():
    try:
        # Start of the game
        print("Welcome to the game!")
        name = input("Enter your character's name: ")
        class_choice = input("Choose a class (Warrior/Mage/Rogue): ").capitalize()
        # Ensure the class choice is valid
        while class_choice not in ["Warrior", "Mage", "Rogue"]:
            print("Invalid class. Choose between Warrior, Mage, or Rogue.")
            class_choice = input("Choose a class (Warrior/Mage/Rogue): ").capitalize()

        # Create a new character based on the player's input
        player = Character(name, class_choice)
        world = World(player)  # Create a new world instance for the player

        # Starting the game loop
        world.travel()

    except Exception as e:
        # Catch any exceptions and show an error message
        print(f"An error occurred: {e}")
        print("Exiting the game.")

# Run the game if the script is executed directly
if __name__ == "__main__":
    game_loop()
