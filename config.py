# config.py
import yaml
from bcolors import bcolors


def edit_config(config_path):
    """Edit the config file interactively."""

    print("Don't know what to do? See the README.md file in the project's root directory.")
    edit_yn = input(f"{bcolors.OKCYAN}Do you want to edit config.yaml? (y/n){bcolors.ENDC}: ")
    if edit_yn.lower() != 'y':
        return False

    # Load the existing config file
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    # Iterate through each key in the config
    for key, value in config.items():
        # Determine the type of the existing value
        existing_type = type(value)

        while True:  # Repeat until a valid value is entered or the user chooses to skip
            # Ask the user to enter a new value or press enter to skip
            new_value = input(f"Type new value for {bcolors.OKGREEN}{key}{bcolors.ENDC} (current value: {bcolors.OKBLUE}{value}{bcolors.ENDC}) or press enter to skip: ")

            if not new_value:
                break  # Skip to the next value if the user pressed enter

            try:
                # Convert the new value to the correct type
                converted_value = existing_type(new_value)
                config[key] = converted_value  # Update the value in the config dictionary
                break  # Break out of the while loop once a valid value is entered
            except ValueError:
                print(f"{bcolors.FAIL}Invalid value. Please try again.{bcolors.ENDC}")

    # Write the updated config back to the file
    with open(config_path, 'w', encoding='utf-8') as file:
        yaml.safe_dump(config, file, default_flow_style=False)

    return True


with open('config.yaml', 'r', encoding='utf-8') as file:
    config_data = yaml.safe_load(file)
