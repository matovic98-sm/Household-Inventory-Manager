import pandas as pd #Allows writing to csv file as a DataFrame
import csv #Writes to csv file
from datetime import datetime #Allows expired items to be deleted from the inventory
                              #and be added to grocery list
def welcome_greeting():#Function to greet the user
    name = input("Hello, what is your name? ")
    print("Welcome to your inventory and grocery list manager, " + name + ".\n")
    return name

def load_inventory_from_csv(inventory_file):#Function to load csv file
    try:
        df = pd.read_csv(inventory_file) #Formats csv into a pandas DataFrame
        inventory = {} #Empty dictionary to save input to
        for index, row in df.iterrows():#Iterates through each row
            item = row['item']
            quantity = int(row['quantity'])
            expires = row['expires']
            inventory[item] = {"quantity": quantity, "expires": expires}
        return inventory
    except FileNotFoundError: #If there is no file, starts with an empty dictionary
        return {}

def save_inventory_to_csv(inventory_file, inventory):#Function to save input to csv file
    with open(inventory_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["item", "quantity", "expires"]) #Create headers for DataFrame
        for item, info in inventory.items():#Formats item information into rows
            writer.writerow([item, info["quantity"], info["expires"]])

def view_inventory(inventory):#Fuction to view inventory
    if not inventory:
        print("Your inventory is empty.\n")
        return
    print("\nYour Inventory:")
    for item, info in inventory.items(): 
        print(f"{item}: {info['quantity']} (expires {info['expires']})")
    print()

def add_item(inventory):#Function to add items to inventory
    item = input("What item would you like to add?: ").strip().lower()
    quantity = int(input("How many?: ")) #Ensures that input is processed as an integer type
    expires = input("What is the expiration date (YYYY-MM-DD): ")

    if item in inventory:
        inventory[item]["quantity"] += quantity #Increases quantity of item in inventory 
    else:
        inventory[item] = {"quantity": quantity, "expires": expires} #Adds item to inventory
    
    save_inventory_to_csv("inventory_file.csv", inventory) 
    print(f"{item} added or updated.\n")

def delete_item(inventory, grocery_list):#Function to delete an amount of an item
    item = input("What item would you like to delete? ").strip().lower()

    if item not in inventory:
        print("That item is not in your inventory.\n")
        return

    amount = int(input("How many would you like to remove? "))
    inventory[item]["quantity"] -= amount #Deletes quantity specified
    if inventory[item]["quantity"] <= 0:
        print(f"You are now out of {item}. It has been removed from your inventory and added to your grocery list.\n")
        add_to_grocery_list(item, grocery_list) #Adds item that reaches 0 to grocery list
        save_grocery_list_to_csv("grocery_list.csv", grocery_list)
        del inventory[item]

    else:
        save_inventory_to_csv("inventory_file.csv", inventory) 
        print(f"{item} updated. You now have {inventory[item]['quantity']} left.\n")

def load_grocery_list_from_csv(grocery_list_file):
    try:
        df=pd.read_csv(grocery_list_file)
        grocery_list = list(df["item"])
        return grocery_list
    except FileNotFoundError: #If there's no file, starts with an empty list
        return []
    
def save_grocery_list_to_csv(grocery_list_file, grocery_list):
    with open(grocery_list_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["item"])
        for item in grocery_list:
            writer.writerow([item])

def view_grocery_list(grocery_list): #Function to view items in grocery list
    if not grocery_list:
        print("\nYour grocery list is empty.\n")
        return
    print("\nYour Grocery List")
    for item in grocery_list:
        print("~" + item)
    print()

def add_item_to_grocery_list(grocery_list): #Function to add items to grocery list
    item = input("What item would you like to add to your grocery list? ").strip().lower()
    add_to_grocery_list(item, grocery_list)
    print()

def delete_item_from_grocery_list(grocery_list): #Function to delete item from grocery list
    item = input("Which item would you like to delete? ").strip().lower()
    if item in grocery_list:
        grocery_list.remove(item)
        print(f"{item} was removed successfully.\n")
    else:
        print("I'm sorry, that item couldn't be found.\n")  

def add_to_grocery_list(item, grocery_list):#Function to add item to grocery list
    if item not in grocery_list:            #Works in both the inventory menu and grocery list menu
        grocery_list.append(item)
        print(f"{item} was added to your grocery list.")

def check_expired_items(inventory, grocery_list): #Function to check for expired items and 
    today = datetime.today().date()               #add them to grocery list

    for item, info in list(inventory.items()):
        try:
            expiration_date = datetime.strptime(info["expires"], "%Y-%m-%d").date()
            if expiration_date < today:
                print(f"{item} is expired and was added to your grocery list.")
                add_to_grocery_list(item, grocery_list)
        except ValueError: #Handles expiration dates not entered in correct format
            print(f"Expiration date for {item} was entered incorrectly.The expiration check was skipped. ")


def inventory_menu(name, inventory, inventory_file, grocery_list):#Function to handle inventory management
    print("\nWelcome to your Inventory Manager!\n")

    while True: #Loop to ensure the menu repeats until the user wants to exit
        print("Inventory Menu:")
        print("1. View inventory")
        print("2. Add item")
        print("3. Delete item")
        print("4. Save and exit")

        option = input("Choose 1-4: ")

        if option == "1":
            view_inventory(inventory) #Calls the function associated with the option chosen
        elif option == "2":
            add_item(inventory)
        elif option == "3":
            delete_item(inventory, grocery_list)
        elif option == "4":
            save_inventory_to_csv(inventory_file, inventory)
            print("Inventory saved. Goodbye, " + name + "!")
            break
        else: #Handles unexpected input
            print("Invalid selection.Please enter a number 1-4.\n")

def grocery_list_menu(grocery_list, grocery_list_file): 
    print("\nWelcome to your Grocery List.\n")
    while True: #Loops grocery list menu until user selects 4
        print("Grocery List Menu:")
        print("1. View grocery list")
        print("2. Add item")
        print("3. Delete item")
        print("4. Exit")

        option = input("Choose 1-4: ")

        if option == "1": #Condtional statements, code blocks will only run when true
            view_grocery_list(grocery_list) #Calls function associated with option
        elif option == "2":
            add_item_to_grocery_list(grocery_list)
        elif option == "3":
            delete_item_from_grocery_list(grocery_list)
        elif option == "4":
            save_grocery_list_to_csv(grocery_list_file, grocery_list)
            print("Grocery List saved. Goodbye! ")
            break
        else:
            print("Invalid selection. Please enter a number 1-4.\n")

def main_menu(): #Main function to navigate to either the inventory manager or grocery list
    inventory_file= "inventory_file.csv"
    grocery_list_file = "grocery_list.csv"
    inventory = load_inventory_from_csv(inventory_file) #Calls functions to be run at the start
    grocery_list = load_grocery_list_from_csv(grocery_list_file)
    name = welcome_greeting()

    check_expired_items(inventory, grocery_list)

    while True:
        print("\nMain Menu:")
        print("1. Manage Inventory")
        print("2. Manage Grocery List")
        print("3. Exit")

        option = input("Choose 1-3: ")

        if option == "1":
            inventory_menu(name, inventory, inventory_file, grocery_list)
        elif option == "2":
            grocery_list_menu(grocery_list, grocery_list_file)
        elif option == "3":
            print("Goodbye, " + name + "!")
            break
        else: #Handles unexpected input
            print("Invalid choice.\n")


main_menu() #Calls main function to run the program
              
