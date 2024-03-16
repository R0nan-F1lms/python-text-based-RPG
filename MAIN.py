import random
import time
import uuid
import os
from collections import Counter


# Function for smoother typing effect



# Function for player sign-up
def player_signup():
    print("Welcome to the Futuristic Adventure Game!")
    name = input("Enter your name: ").lower()

    user_id = str(uuid.uuid4())[:8]  # Generate a unique user ID
    print(f"Welcome, {name}! Your user ID is: {user_id}")
    return (name, user_id)


# Function to load player data or create new player data
def load_player_data(user_id):
    data_file = f"{user_id}_data.txt"
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            data = eval(file.read())
        return data
    else:
        return {"inventory": [], "highscore": 0, "health": 100}



# Function to save player data
def save_player_data(user_id, inventory, highscore, health):
    player_data_file = f"{user_id}.txt"
    with open(player_data_file, "w") as file:
        file.write(",".join(inventory) + "\n")
        file.write(str(highscore) + "\n")
        file.write(str(health) + "\n")

def handle_death():
    print("You have died.")
    # Reset score to 0
    player_data['score'] = 0
    # Clear inventory
    player_data['inventory'] = []
    print("Your inventory has been cleared.")


# Function to display the menu and get user choice
def display_menu():
    print("1. Go left")
    print("2. Go right")
    print("3. Go straight")
    print("0. Quit")
    choice = input("Enter your choice: ")
    return choice


# Function to generate outcome file if it doesn't exist and load outcomes from the file
def load_outcomes():
    outcome_file = "outcomes.txt"

    if not os.path.exists(outcome_file):
        # Create a sample set of outcomes
        outcomes = [
            #Hostile things to battle
            {"id": 1, "name": "Hostile drone", "category": "enemy", "rarity": 2},
            {"id": 2, "name": "Alien", "category": "enemy", "rarity": 1},
            {"id": 3, "name": "Space Monkey", "category": "enemy", "rarity": 3},
            {"id": 4, "name": "Space Whale", "category": "enemy", "rarity": 2},
            {"id": 5, "name": "Queen Elizabeth II", "category": "enemy", "rarity": 2},
            # Discovery
            {"id": 6, "name": "Hidden passage", "category": "discovery", "rarity": 1},
            # Weapons
            {"id": 7, "name": "Plasma Gun", "category": "weapon", "rarity": 4},
            {"id": 8, "name": "Blaster", "category": "weapon", "rarity": 3},
            {"id": 9, "name": "Laser Sword", "category": "weapon", "rarity": 2},
            {"id": 10, "name": "Ion Blaster", "category": "weapon", "rarity": 1},
            {"id": 11, "name": "Photon Rifle", "category": "weapon", "rarity": 1},
            # Items
            {"id": 12, "name": "Health pack", "category": "item", "rarity": 3},
            {"id": 13, "name": "Large Health pack", "category": "item", "rarity": 4},
            {"id": 14, "name": "Gold Bar", "category": "item", "rarity": 6},
            # Friendly creatures (allies/encounter)
            {"id": 15, "name": "Science robot", "category": "ally", "rarity": 2},
            {"id": 16, "name": "Doctor Who", "category": "ally", "rarity": 4},
            {"id": 17, "name": "Rose Tyler", "category": "ally", "rarity": 3},
            # Hazards could kill you be careful
            {"id": 18, "name": "Trap", "category": "hazard", "rarity": 4},
            {"id": 19, "name": "Toxic gas trap", "category": "hazard", "rarity": 4},
            #Special
            {"id": 20, "name": "Mysterious portal", "category": "special", "rarity": 4},
            {"id": 21, "name": "Black Hole", "category": "special", "rarity": 4},
            {"id": 22, "name": "Ancient artifact", "category": "special", "rarity": 5},
            {"id": 23, "name": "Treasure chest", "category": "Special", "rarity": 3},
            {"id": 24, "name": "Rare Artifact", "category": "special", "rarity": 5},

        ]

        # Write outcomes to the file
        with open(outcome_file, "w") as f:
            for outcome in outcomes:
                f.write(f"{outcome['id']:03d}, {outcome['name']}, {outcome['category']}, {outcome['rarity']}\n")
    else:
        # Load outcomes from the file
        outcomes = []
        with open(outcome_file, "r") as f:
            for line in f:
                outcome_data = line.strip().split(", ")
                outcome = {"id": int(outcome_data[0]), "name": outcome_data[1], "category": outcome_data[2], "rarity": int(outcome_data[3])}
                outcomes.append(outcome)

    return outcomes



def get_outcome():
    outcomes = load_outcomes()
    total_rarity = sum(outcome['rarity'] for outcome in outcomes)
    rand_num = random.randint(1, total_rarity)

    cumulative_rarity = 0
    for outcome in outcomes:
        cumulative_rarity += outcome['rarity']
        if rand_num <= cumulative_rarity:
            return outcome

    # This should not happen, but in case of any issues, return None
    return None


# Function to simulate a battle
def battle(outcome):
    player_health = player_data["health"]

    # Check if the outcome is an enemy encounter
    if outcome["id"] in [1, 2, 3, 4, 5]:
        monster = {
            "name": outcome["name"],
            "health": random.randint(50, 100),
            "damage": random.randint(5, 20)
        }

        print(f"A {monster['name']} appears!")

        while player_health > 0 and monster['health'] > 0:
            print("1. Attack")
            print("2. Use Weapon")
            print("3. Run away")
            action = input("Enter your choice: ")

            if action == '1':
                player_damage = random.randint(10, 30)
                monster_damage = monster['damage']

                print(f"You attack the {monster['name']} and deal {player_damage} damage!")
                monster['health'] -= player_damage

                if monster['health'] <= 0:
                    print(f"You defeated the {monster['name']}!")
                    return True
                else:
                    print(f"The {monster['name']} attacks you and deals {monster_damage} damage!")
                    player_health -= monster_damage
                    print(f"Your health: {player_health}")
                    print(f"{monster['name']}'s health: {monster['health']}")
            elif action == '2':
                weapon_choice = input("Select a weapon:\n1. Plasma Gun\n2. Blaster\n3. Laser Sword\n4. Ion Blaster\n5. Photon Rifle\nEnter weapon choice: ")
                if weapon_choice == '1':
                    if "Plasma Gun" in player_data['inventory']:
                        player_damage = random.randint(30, 50)  # Damage boosted for Plasma Gun
                        print("You use the Plasma Gun and deal massive damage!")
                        player_data['inventory'].remove("Plasma Gun")  # Remove weapon from inventory after use
                    else:
                        print("You don't have the Plasma Gun!")
                        continue
                elif weapon_choice == '2':
                    if "Blaster" in player_data['inventory']:
                        player_damage = random.randint(20, 40)
                        print("You use the Blaster and deal significant damage!")
                        player_data['inventory'].remove("Blaster")
                    else:
                        print("You don't have the Blaster!")
                        continue
                elif weapon_choice == '3':
                    if "Laser Sword" in player_data['inventory']:
                        player_damage = random.randint(15, 35)
                        print("You use the Laser Sword and deal moderate damage!")
                        player_data['inventory'].remove("Laser Sword")
                    else:
                        print("You don't have the Laser Sword!")
                        continue
                elif weapon_choice == '4':
                    if "Ion Blaster" in player_data['inventory']:
                        player_damage = random.randint(10, 30)
                        print("You use the Ion Blaster and deal minor damage!")
                        player_data['inventory'].remove("Ion Blaster")
                    else:
                        print("You don't have the Ion Blaster!")
                        continue
                elif weapon_choice == '5':
                    if "Photon Rifle" in player_data['inventory']:
                        player_damage = random.randint(5, 25)
                        print("You use the Photon Rifle and deal minimal damage!")
                        player_data['inventory'].remove("Photon Rifle")
                    else:
                        print("You don't have the Photon Rifle!")
                        continue

                monster['health'] -= player_damage

                if monster['health'] <= 0:
                    print(f"You defeated the {monster['name']}!")
                    return True
                else:
                    print(f"The {monster['name']} attacks you and deals {monster_damage} damage!")
                    player_health -= monster_damage
                    print(f"Your health: {player_health}")
                    print(f"{monster['name']}'s health: {monster['health']}")
            elif action == '3':
                print(f"You ran away from the {monster['name']}!")
                score_penalty = random.randint(10, 20)
                player_data['score'] = max(player_data['score'] - score_penalty, 0)  # Ensure score doesn't go below zero
                return False
            else:
                print("Invalid choice. Please enter a valid option.")

        if player_health <= 0:
            print("You were defeated in battle.")
            handle_death()  # Call the function to handle player death
            return False
    else:
        # Handle non-enemy outcomes here
        # Add your logic for non-enemy outcomes
        pass




# Main function to run the game
def main():
    name, user_id = player_signup()

    global player_data
    player_data = load_player_data(user_id)

    print(f"Welcome, {name}! Your current high score is {player_data['highscore']}.")

    score = 0  # Initialize score
    inventory = player_data['inventory']  # Initialize inventory

    while True:
        choice = display_menu()

        if choice == '1' or choice == '2' or choice == '3':
            # Get a random outcome
            outcome = get_outcome()
            print(f"You have found \"{outcome["name"]}\"")

            # Check if the outcome is an enemy encounter
            if outcome["category"] == "enemy":
                battle(outcome)
            elif outcome["category"] == "discovery":
                print(f"You have discovered {outcome["name"]} collect 5 credits to your score")
                score += 5
            elif outcome["category"] == "ally":
                credits = random.randint(20, 70)
                print(f"You have found {outcome["name"]} as an ally, this will be crucial through out your space travel, collect {credits} credits to your score")
                score += credits
            elif outcome["category"] == "weapon":
                print(f"You have stumbled upon a {outcome["name"]}!\nThis is added to your inventory, you can use this to fight against any one that may try and attack you to deal more damage")
                inventory.append(outcome["name"])
            elif outcome["category"] == "item":
                if outcome["id"] == 13:
                    print(f"You have found a {outcome["name"]} collect 50+ health")
                    player_data['health'] += 50
                elif outcome["id"] == 12:
                    print(f"You have found a {outcome["name"]} collect 20+ health")
                    player_data['health'] += 20
                elif outcome["id"] == 14:
                    print(f"You have uncovered {outcome["name"]} collect 100 credits to your score")
                    score += 100
            elif outcome["category"] == "special":
                        #{"id": 20, "name": "Mysterious portal", "category": "special", "rarity": 4},
                        #{"id": 21, "name": "Black Hole", "category": "special", "rarity": 4},
                        #{"id": 22, "name": "Ancient artifact", "category": "special", "rarity": 5},
                        #{"id": 23, "name": "Treasure chest", "category": "Special", "rarity": 3},
                        # {"id": 24, "name": "Rare Artifact", "category": "special", "rarity": 5},
                if outcome["id"] == 20:
                    credits = random.randint(35, 45)
                    score += credits
                    print(f"You have unearthed {outcome["name"]} collect {credits} credits to your score")
                elif outcome["id"] == 21:
                    credits = random.randint(45, 60)
                    score += credits
                    print(f"You have unearthed {outcome["name"]} collect {credits} credits to your score")
                elif outcome["id"] == 22:
                    credits = random.randint(30, 40)
                    score += credits
                    print(f"You have unearthed {outcome["name"]} collect {credits} credits to your score")
                elif outcome["id"] == 23:
                    credits = random.randint(10, 25)
                    score += credits
                    print(f"You have unearthed {outcome["name"]} collect {credits} credits to your score")
                elif outcome["id"] == 24:
                    credits = random.randint(65, 80)
                    score += credits
                    print(f"You have unearthed {outcome["name"]} collect {credits} credits to your score")

            elif outcome["category"] == "hazard":
                survival_chance = random.randint(1, 10)  # Random survival chance
                if survival_chance <= 6:  # 60% chance of survival
                    print(f"You encountered a {outcome["name"]} but managed to survive!")
                else:
                    print(f"You encountered a {outcome["name"]} but sadly you died!")
                    handle_death()  # Call the function to handle player death

            print(f"Your current score is: {score}")
            print("Inventory: ")
            inventory_counts = Counter(inventory)
            for item, count in inventory_counts.items():
                print(f"{item} x {count}")
            player_data['inventory'] = inventory

            # Update high score if current score is higher
            if score > player_data['highscore']:
                player_data['highscore'] = score
                save_player_data(user_id, inventory, score, player_data.get('health', 100))
                print("Congratulations! You've achieved a new high score!")
        elif choice == '4':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
