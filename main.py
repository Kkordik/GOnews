import app.parse_chats.parse_chats_handler
import app.parse_admin_chat.parse_admin_chat_handler
from app.define_app import app
from bcolors import bcolors
from config import edit_config
import os


if __name__ == '__main__':
    print(f'***RESELLING THIS CODE IS FORBIDDEN***\nThank you for using this bot! You can find my github here: https://github.com/Kkordik\n')
    print(f"{bcolors.WARNING}Remember to edit the configuration.yaml file before starting the bot. You can find it in the project's root directory.{bcolors.ENDC}")
    print("Don't know what to do? See the README.md file in the project's root directory.\n")

    if edit_config("configuration.yaml"):
        if not os.path.exists('my_account.session'):
            print(f"{bcolors.WARNING}Since you are running this for the first time, you will be asked to log in. Remember to restart the program after a successful login.{bcolors.ENDC}")
            app.run()
    else:
        print(f'{bcolors.OKGREEN}Starting app..{bcolors.ENDC}')
        if not os.path.exists('my_account.session'):
            print(f"{bcolors.WARNING}Since you are running this for the first time, you will be asked to log in. Remember to restart the program after a successful login.{bcolors.ENDC}")
        app.run()
