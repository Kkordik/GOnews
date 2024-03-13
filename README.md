# GOnews
**GOnews** is a Telegram bot, that parses multiple telegram channels and on new post deletes from it tails (e.g. "Subscribe on @orig_channel") then rephrases it with GPT and adds new tail (e.g. "Subscribe on @my_channel") and sends it to the group of admins, where they can edit the message and forward it to their channel in one click.
## Installation and Setup

### Step 1: Check for Git

Open a terminal or command prompt and run the following command:

```bash
git --version
```

If you don't see git version, install it:

```bash
sudo apt update
sudo apt-get install git
```

### Step 2: Clone the Repository

First, you'll need to clone the repository from GitHub. Open a terminal or command prompt and run the following command:

```bash
git clone https://github.com/KKordik/GOnews.git
```

### Step 3: Setup python environment 
Navigate to the directory of the cloned repository:

```bash
cd GOnews
```

Create a new python environment:
```bash
python -m venv venvbot
```

Activate it:
```bash
source venvbot/bin/activate
```

Install required libraries:
```bash
pip install -r requirements.txt
```

### Step 4: Run main.py and fill credentials

Firstly, make sure you've activated `venvbot`:
```bash
source venvbot/bin/activate
```

Then run `main.py`:
```bash
python main.py
```
Now, you will be asked:

```
Do you want to edit configuration.yaml interactively? (y/n):
```

- Type `y` and press enter, if you haven't edited `configuration.yaml` file manually before
- Otherwise you can skip this step with `n` and continue with **Step 5**

If you've chosen to edit `configuration.yaml`, you will be asked to type a new value for each parameter or press enter to skip. 
![Interactive config editing](https://i.imgur.com/dtA7U0n.png)
At least `essential` section must be filled. Where:
- `API_HASH` and `API_ID` you can get [here](https://my.telegram.org/auth). I recommend not to use your main telegram account, but to create a new one (we will call it '*bot account*').

- `ADMIN_CHAT_ID` is chat_id of the chat, for administrating your channel, create a new group and add there your *bot account*, you can use [myidbot](https://t.me/myidbot?startgroup=1) to get the chat_it.

- `CHANNEL_ID` is chat_id of your channel, you can use [myidbot](https://t.me/myidbot), simply forward a post from your channel to the bot. Remember that *bot account* must be an administrator in the channel to be able send posts.

See about other parameters at `CONFIG_GUIDE.md`

### Step 5: Log in to the *bot account* via the terminal

After editing `configuration.yaml` or having edited it previously, you will be asked to log in

![Logging in](https://i.imgur.com/vWQCAs5.png)

After succesful login <kbd>Ctrl</kbd> + <kbd>C</kbd> to stop the program


### Step 6: Run in background

Leave from  `venvbot`:
```bash
deactivate
```

Install screen
```bash
sudo apt install screen
```

Run new screen
```bash
screen
```
Run `venvbot`:
```bash
source venvbot/bin/activate
```

Run `main.py`:
```bash
python main.py
```
You will be asked, type `n`:

```
Do you want to edit configuration.yaml interactively? (y/n): n
```
Thats it! Now <kbd>Ctrl</kbd> + <kbd>a</kbd> + <kbd>d</kbd> to detatch the screen.

Now the bot will be running in the background

## Available bot commands:
```
!send <to_chat_id> <from_chat_id> <message_id>
```
```
!channel <username> '<tails divided by comma without space>'
```
