import os
import logging
from telethon import TelegramClient, events

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# --- IMPORTANT ---
# Replace these with your actual credentials
API_ID = 1234567  # YOUR_API_ID
API_HASH = 'YOUR_API_HASH'
BOT_TOKEN = 'YOUR_BOT_TOKEN'
# --- IMPORTANT ---

SESSION_NAME = 'telegram-leech-bot'

# Check if the placeholder values have been replaced
if API_ID == 1234567 or API_HASH == 'YOUR_API_HASH' or BOT_TOKEN == 'YOUR_BOT_TOKEN':
    raise ValueError("Please replace the placeholder API_ID, API_HASH, and BOT_TOKEN in bot.py with your actual credentials.")

# Initialize the client
# Using the BOT_TOKEN will connect as a bot
client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    """Handler for the /start command."""
    await event.reply("Hello! I am a Telegram Leech Bot. Send me a link to a public Telegram message and I will leech it for you. \nUsage: `/leech <message_link>`")

@client.on(events.NewMessage(pattern='/leech'))
async def leech_handler(event):
    """
    Handles the /leech command.
    Example: /leech https://t.me/some_channel/123
    """
    try:
        # Get the message link from the command
        parts = event.raw_text.split()
        if len(parts) < 2:
            await event.reply("Please provide a Telegram message link after the command.\nExample: `/leech https://t.me/c/1234567890/123`")
            return

        link = parts[1]

        # Parse the link to get chat_id and message_id
        try:
            link_parts = link.split('/')
            if 't.me' not in link_parts[2]:
                 raise ValueError("Invalid link format.")

            if link_parts[-2] == 'c':
                chat_id = int("-100" + link_parts[-3])
                message_id = int(link_parts[-1])
            else:
                chat_id = link_parts[-2]
                message_id = int(link_parts[-1])

        except (ValueError, IndexError):
            await event.reply("Invalid Telegram message link format. Please use a valid link.")
            return

        status_message = await event.reply("Leeching...")

        # Get the message object
        target_message = await client.get_messages(chat_id, ids=message_id)

        if not target_message:
            await status_message.edit("Could not find the message. Make sure the link is correct and I have access to the channel.")
            return

        # Download and re-upload the media/file
        if target_message.media:
            await status_message.edit("Downloading...")

            file_path = await client.download_media(target_message.media, file="downloads/")

            await status_message.edit(f"Uploading...")

            await client.send_file(
                event.chat_id,
                file_path,
                caption=target_message.text or f"Leeched from {link}",
                reply_to=event.message
            )

            os.remove(file_path)
            await status_message.delete()
        elif target_message.text:
             await event.reply(target_message.text, reply_to=event.message)
             await status_message.delete()
        else:
            await status_message.edit("The linked message does not contain any media or text to leech.")

    except Exception as e:
        LOGGER.error(f"An error occurred: {e}", exc_info=True)
        await event.reply(f"An error occurred: {e}")


async def main():
    """Start the bot."""
    # Ensure the downloads directory exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    # Start the client with the bot token
    await client.start(bot_token=BOT_TOKEN)
    LOGGER.info("Bot is running...")
    # Run the client until disconnected
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())