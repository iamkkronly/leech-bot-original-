# Telegram Leech Bot

This is a simple Telegram bot that can "leech" files from both **direct download links** and **Telegram channel messages**.

## How it Works
*   **Direct Links:** You provide a direct URL to a file (e.g., `http://example.com/file.zip`), and the bot downloads it to the server and then uploads it to your Telegram chat.
*   **Telegram Links:** You provide a link to a message in a Telegram channel. The bot will fetch the media or text from that message and send it to you. **Important:** For this to work, the bot must be a member of the source channel.

## How to Set Up and Run the Bot

### 1. Prerequisites
*   A VPS or any machine that can run Python scripts 24/7.
*   Python 3.8+ installed.
*   A Telegram account.

### 2. Getting your Bot Token
To run this bot, you only need one credential from Telegram: your `BOT_TOKEN`.

1.  Open your Telegram app and search for **@BotFather**.
2.  Start a chat with BotFather and send the `/newbot` command.
3.  Follow the instructions to create a new bot. You will need to give it a name and a username.
4.  Once your bot is created, BotFather will give you a **token**. This is your `BOT_TOKEN`. Keep it safe.

### 3. Setting up the Bot on Your Server

1.  **Download the bot files** to your VPS:
    *   `bot.py`
    *   `requirements.txt`

2.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your credentials:**
    *   Open the `bot.py` file with a text editor.
    *   Find this line near the top of the file:
        ```python
        # --- IMPORTANT ---
        # Replace this with your actual Bot Token
        BOT_TOKEN = 'YOUR_BOT_TOKEN'
        # --- IMPORTANT ---
        ```
    *   Replace the placeholder value (`'YOUR_BOT_TOKEN'`) with the actual token you got from BotFather.

### 4. Running the Bot

1.  **Start the bot:**
    ```bash
    python bot.py
    ```
2.  If everything is set up correctly, you will see a message in your console saying "Bot is running...".
3.  Your bot is now live on Telegram!

### 5. How to Use the Bot

1.  Find your bot on Telegram (the one you created with BotFather).
2.  Send the `/start` command to see the welcome message and usage instructions.
3.  To leech a file or message, use the `/leech` command followed by the link.

    **Example 1: Direct Download Link**
    ```
    /leech http://speed.hetzner.de/100MB.bin
    ```

    **Example 2: Telegram Message Link**
    (Remember to add your bot to the channel `some_public_channel` first)
    ```
    /leech https://t.me/some_public_channel/12345
    ```

The bot will show a progress status and then send you the file.