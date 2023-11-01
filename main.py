import app.parse_chats.parse_chats_handler
import app.parse_admin_chat.parse_admin_chat_handler
from app.define_app import app
from bcolors import bcolors
from config import edit_config
import os


if __name__ == '__main__':
    print(f'{bcolors.WARNING}***RESELLING THIS CODE IS FORBIDDEN***\nThank you for using this bot! You can find my github here: https://github.com/Kkordik{bcolors.ENDC}\n')

    if not edit_config("config.yaml"):
        print(f'{bcolors.OKGREEN}Starting app..{bcolors.ENDC}')
        if not os.path.exists('my_account.session'):
            print(f"{bcolors.WARNING}Since you are running this for the first time, you will be asked to log in. Remember to restart the program after a successful login.{bcolors.ENDC}")
        app.run()

    else:
        print(f"{bcolors.OKGREEN}Config edited successfully.{bcolors.ENDC}\n{bcolors.WARNING}The bot hasn't started because the config was edited."
              f" Please restart the program and skip config editing to start the bot.{bcolors.ENDC}")
        if not os.path.exists('my_account.session'):
            print(f"{bcolors.WARNING}Since you are running this for the first time, you will be asked to log in. Remember to restart the program after a successful login.{bcolors.ENDC}")
            app.run()
