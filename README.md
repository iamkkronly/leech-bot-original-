# Telegram Leech Bot

This is a simple Telegram bot that can "leech" messages from public channels and send them to the chat where the command is used.

## How to set up and run the bot

### 1. Prerequisites

*   A VPS or any machine that can run Python scripts 24/7.
*   Python 3.6+ installed.
*   A Telegram account.

### 2. Getting your Telegram API Credentials

To run this bot, you need three credentials from Telegram: `API_ID`, `API_HASH`, and `BOT_TOKEN`.

#### a. Get `API_ID` and `API_HASH`

1.  Go to [my.telegram.org](https://my.telegram.org) and log in with your Telegram account.
2.  Click on **API development tools**.
3.  Fill in the "App title" and "Short name" fields. You can enter anything you like.
4.  Click on **Create application**.
5.  You will now see your `api_id` and `api_hash`. Keep them safe.

#### b. Get `BOT_TOKEN`

1.  Open your Telegram app and search for **@BotFather**.
2.  Start a chat with BotFather and send the `/newbot` command.
3.  Follow the instructions to create a new bot. You will need to give it a name and a username.
4.  Once your bot is created, BotFather will give you a **token**. This is your `BOT_TOKEN`.

### 3. Setting up the Bot on Your Server

1.  **Download the bot files** to your VPS.
    *   `bot.py`
    *   `requirements.txt`

2.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your credentials:**
    *   Open the `bot.py` file with a text editor.
    *   Find these lines near the top of the file:
        ```python
        # --- IMPORTANT ---
        # Replace these with your actual credentials
        API_ID = 1234567  # YOUR_API_ID
        API_HASH = 'YOUR_API_HASH'
        BOT_TOKEN = 'YOUR_BOT_TOKEN'
        # --- IMPORTANT ---
        ```
    *   Replace the placeholder values (`1234567`, `'YOUR_API_HASH'`, and `'YOUR_BOT_TOKEN'`) with the actual credentials you obtained in **Step 2**.

### 4. Running the Bot

1.  **Start the bot:**
    ```bash
    python bot.py
    ```
2.  If everything is set up correctly, you will see a message in your console saying "Bot is running...".
3.  Your bot is now live on Telegram!

### 5. How to Use the Bot

1.  Find your bot on Telegram (the one you created with BotFather).
2.  Send the `/start` command to see the welcome message.
3.  To leech a message, use the `/leech` command followed by the link to the message.

    **Example:** `/leech https://t.me/some_public_channel/12345`

The bot will then download the media or copy the text from that message and send it to you.

**Note:** This bot can only leech from public channels or chats where your bot has been added. For private channels, the account associated with your `API_ID` and `API_HASH` must be a member of that channel.