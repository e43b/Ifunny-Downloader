import json
import os

# Function to check and install necessary dependencies
def check_install_dependencies():
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Required libraries not found.")
        choice = input("Do you want to install the necessary libraries? (y/n): ").strip().lower()
        if choice == 'y':
            os.system('pip install -r requirements.txt')
        else:
            print("Installation canceled. The program may not function properly.")
            input("\nPress Enter to continue...")
            return False
    return True

def modify_config(option):
    # Open the config.json file and modify the "crop_logo" option
    try:
        with open('code/config.json', 'r+') as f:
            config = json.load(f)
            if option == 1:
                # Toggle the value between True and False
                config['crop_logo'] = not config.get('crop_logo', False)
                f.seek(0)  # Move the cursor to the beginning of the file
                json.dump(config, f, indent=4)
                f.truncate()  # Truncate any content that may be beyond this point
            elif option == 2:
                pass  # No modification for option 2 in this example
            else:
                print("Invalid option.")
                return False
    except FileNotFoundError:
        print("File config.json not found.")
        return False
    return True

def clear_console():
    # Clear the console (works on Unix and Windows systems)
    os.system('cls' if os.name == 'nt' else 'clear')

def load_script():
    # Execute the script code/main.py
    try:
        os.system('python code/main.py')
    except FileNotFoundError:
        print("Script code/main.py not found.")

def main():
    # Check and install necessary dependencies
    if not check_install_dependencies():
        return

    # Load the current state of 'crop_logo' from config.json
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            crop_logo = config.get('crop_logo', False)
    except FileNotFoundError:
        print("File config.json not found.")
        return

    while True:
        # Determine the text to display based on the current state of 'crop_logo'
        if crop_logo:
            logo_state = "enabled"
        else:
            logo_state = "disabled"

        print("Ifunny Downloader\n")
        print("This script allows you to download posts from the site iFunny.co, downloading either individual posts or multiple posts sequentially.\n")
        print(f"1. Remove Ifunny logo: {logo_state}")
        print("2. I want to download posts from Ifunny\n")
        option = input("Enter your choice: ")

        if option == '1':
            if modify_config(1):
                crop_logo = not crop_logo  # Update the state after modification
                clear_console()
                continue
        elif option == '2':
            clear_console()
            load_script()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
