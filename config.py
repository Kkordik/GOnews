from bcolors import bcolors
from ruamel.yaml import YAML


def edit_config(config_path):
    """Edit the config file interactively in terminal."""
    edit_yn = input(f"{bcolors.OKCYAN}Do you want to edit configuration.yaml interactively? (y/n){bcolors.ENDC}: ")
    if edit_yn.lower() != 'y':
        return False

    yaml = YAML()
    yaml.preserve_quotes = True  # This will preserve any quotes in the file

    # Load the existing config file
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.load(file)

    # Iterate through each section in the config
    for section, values in config.items():
        print(f"\nEditing section: {bcolors.OKCYAN}{section}{bcolors.ENDC}.")
        # Iterate through each key in the section
        for key, value in values.items():
            # Determine the type of the existing value
            existing_type = type(value)

            while True:  # Repeat until a valid value is entered or the user chooses to skip
                # Ask the user to enter a new value or press enter to skip
                new_value = input(f"Type new value for {bcolors.OKGREEN}{key}{bcolors.ENDC} (current value: {bcolors.OKBLUE}{value}{bcolors.ENDC}) to leave empty type {bcolors.OKBLUE}None{bcolors.ENDC}, or press enter to leave current value: ")

                if not new_value:
                    break  # Skip to the next value if the user pressed enter

                try:
                    # Convert the new value to the correct type
                    converted_value = None if new_value.lower() == 'none' else existing_type(new_value)
                    config[section][key] = converted_value  # Update the value in the config dictionary
                    break  # Break out of the while loop once a valid value is entered
                except ValueError:
                    print(f"{bcolors.FAIL}Invalid value. Please try again.{bcolors.ENDC}")

    # Write the updated config back to the file
    with open(config_path, 'w', encoding='utf-8') as file:
        yaml.dump(config, file)

    print(
        f"{bcolors.OKCYAN}Config was edited successfully.{bcolors.ENDC}\n{bcolors.WARNING}The bot hasn't started because the config was edited."
        f" Please restart the program and skip config editing to start the bot.{bcolors.ENDC}")
    return True


with open('configuration.yaml', 'r', encoding='utf-8') as file:
    yaml = YAML()
    config_data = yaml.load(file)
