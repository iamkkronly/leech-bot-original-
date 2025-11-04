import os
import logging
import time
import math
import aiohttp
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeFilename

# --- IMPORTANT ---
# Replace this with your actual Bot Token
BOT_TOKEN = 'YOUR_BOT_TOKEN'
# --- IMPORTANT ---

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Session name for the bot
SESSION_NAME = 'telegram-leech-bot'

# Check if the placeholder value has been replaced
if BOT_TOKEN == 'YOUR_BOT_TOKEN':
    raise ValueError("Please replace the placeholder BOT_TOKEN in bot.py with your actual credential.")

# Initialize the client. We only need the session name and bot token.
# API_ID and API_HASH are not required for bot accounts.
client = TelegramClient(SESSION_NAME, api_id=None, api_hash=None).start(bot_token=BOT_TOKEN)

# --- Helper Functions ---

def get_human_readable_size(size_bytes):
    """Converts bytes to a human-readable format."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

async def download_from_url(url, status_message, reply_to_message):
    """Downloads a file from a direct URL and uploads it to Telegram."""
    try:
        start_time = time.time()
        file_path = os.path.join("downloads", os.path.basename(url))

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=None) as response:
                if response.status != 200:
                    await status_message.edit(f"Error: Received status {response.status} from the server.")
                    return

                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                last_update_time = 0

                with open(file_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024 * 1024): # 1MB chunks
                        f.write(chunk)
                        downloaded_size += len(chunk)

                        # Update status every 2 seconds to avoid flooding
                        current_time = time.time()
                        if current_time - last_update_time > 2:
                            last_update_time = current_time
                            percentage = (downloaded_size / total_size) * 100 if total_size > 0 else 0
                            elapsed_time = current_time - start_time
                            speed = downloaded_size / elapsed_time if elapsed_time > 0 else 0

                            progress_text = (
                                f"**Downloading...**\n"
                                f"**URL:** `{url}`\n"
                                f"**Progress:** {percentage:.1f}%\n"
                                f"**Downloaded:** {get_human_readable_size(downloaded_size)} / {get_human_readable_size(total_size)}\n"
                                f"**Speed:** {get_human_readable_size(speed)}/s"
                            )
                            await status_message.edit(progress_text)

        await status_message.edit("Download complete. Now uploading to Telegram...")

        # Upload to Telegram
        await client.send_file(
            reply_to_message.chat_id,
            file_path,
            caption=f"Leeched from: `{url}`",
            reply_to=reply_to_message,
            attributes=[DocumentAttributeFilename(file=os.path.basename(file_path))]
        )

        os.remove(file_path)
        await status_message.delete()

    except aiohttp.ClientError as e:
        await status_message.edit(f"An error occurred during download: {e}")
        LOGGER.error(f"AIOHTTP Error: {e}", exc_info=True)
    except Exception as e:
        await status_message.edit(f"An unexpected error occurred: {e}")
        LOGGER.error(f"Unexpected Error: {e}", exc_info=True)
        if os.path.exists(file_path):
            os.remove(file_path)

# --- Bot Event Handlers ---

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    """Handler for the /start command."""
    await event.reply("Hello! I am a Telegram Leech Bot.\n\n"
                      "**Usage:**\n"
                      "1. **Telegram Link:** `/leech <telegram_message_link>`\n"
                      "   (I must be a member of the channel for this to work).\n\n"
                      "2. **Direct Link:** `/leech <direct_download_link>`")

@client.on(events.NewMessage(pattern='/leech'))
async def leech_handler(event):
    """Handles the /leech command for both Telegram and direct links."""
    try:
        parts = event.raw_text.split()
        if len(parts) < 2:
            await event.reply("Please provide a link after the command.\n"
                              "**Example:** `/leech https://t.me/some_channel/123` or `/leech http://example.com/file.zip`")
            return

        link = parts[1]
        status_message = await event.reply("Processing link...")

        # Check if it's a Telegram link
        if "t.me/" in link:
            try:
                link_parts = link.split('/')
                if 't.me' not in link_parts[2]:
                    raise ValueError("Invalid Telegram link format.")

                if link_parts[-2] == 'c':
                    chat_id = int("-100" + link_parts[-3])
                    message_id = int(link_parts[-1])
                else:
                    chat_id = link_parts[-2]
                    message_id = int(link_parts[-1])

                await status_message.edit("Leeching from Telegram link...")
                target_message = await client.get_messages(chat_id, ids=message_id)

                if not target_message:
                    await status_message.edit("Could not find the message. Make sure the link is correct and I am a member of the channel.")
                    return

                if target_message.media:
                    await status_message.edit("Downloading from Telegram...")
                    file_path = await client.download_media(target_message.media, file="downloads/")
                    await status_message.edit("Uploading to chat...")
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
                    await status_message.edit("The linked message has no content to leech.")

            except (ValueError, IndexError):
                await status_message.edit("Invalid Telegram message link format.")
            except Exception as e:
                await status_message.edit(f"Failed to leech from Telegram: {e}\n\nNote: I must be a member of the source channel.")
                LOGGER.error(f"Telegram Leech Error: {e}", exc_info=True)

        # Check if it's a direct download link
        elif link.startswith("http://") or link.startswith("https://"):
            await download_from_url(link, status_message, event.message)

        else:
            await status_message.edit("Invalid link format. Please provide a valid Telegram message link or a direct download link (http/https).")

    except Exception as e:
        LOGGER.error(f"An error occurred in leech_handler: {e}", exc_info=True)
        await event.reply(f"An error occurred: {e}")

# --- Main Execution ---

async def main():
    """Start the bot."""
    # Ensure the downloads directory exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    LOGGER.info("Bot is running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())