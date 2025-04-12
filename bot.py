from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
from bs4 import BeautifulSoup

# Your bot token from @BotFather
BOT_TOKEN = '7597983353:AAF3hR-roVLxWAyk-fui5gE7zcvHWKGuL4k'

# Function to scrape igram.io for download link
def get_reel_download_link(instagram_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'url': instagram_url
        }
        response = requests.post('https://igram.io/i/', headers=headers, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')

        # This gets the first download button
        video_tag = soup.find('a', class_='btn btn-light btn-lg d-block')
        if video_tag:
            return video_tag['href']
        else:
            return None
    except Exception as e:
        print(f"Error while scraping igram.io: {e}")
        return None

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a public Instagram Reel link, and I’ll fetch the download link for you!")

# Handle message with URL
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com/reel/" in url:
        await update.message.reply_text("🔍 Fetching the download link... please wait a moment.")
        video_link = get_reel_download_link(url)
        if video_link:
            await update.message.reply_text(f"✅ Here's your download link:\n{video_link}")
        else:
            await update.message.reply_text("❌ Sorry, I couldn't fetch the video. Make sure it's public.")
    else:
        await update.message.reply_text("⚠️ Please send a valid Instagram Reel URL.")

# Run the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("🚀 Bot is running...")
app.run_polling()
