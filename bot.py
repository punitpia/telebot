from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import subprocess
import os

TOKEN = "7831083294:AAHZYHhgMESyiMKz03FCdtq33rmQcTtK6O8"

async def start(update: Update, context):
    await update.message.reply_text("Send me an Instagram Reel link, and I'll download it for you!")

async def download_reel(update: Update, context):
    url = update.message.text
    await update.message.reply_text("Downloading the Reel...")

    try:
        # Using yt-dlp to download the video
        output_file = "reel.mp4"
        command = f'yt-dlp -o {output_file} {url}'
        subprocess.run(command, shell=True, check=True)

        # Send the video back to user
        with open(output_file, "rb") as video:
            await update.message.reply_video(video)

        os.remove(output_file)

    except Exception as e:
        await update.message.reply_text("Failed to download the video. Make sure it's a public link.")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_reel))

    application.run_polling()

if __name__ == "__main__":
    main()
