import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Read token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Function to scrape igram.io for the Reel download link
def get_reel_download_link(instagram_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'url': instagram_url
        }

        response = requests.post('https://igram.io/i/', headers=headers, data=data, timeout=10)
        if response.status_code != 200:
            print(f"igram.io returned status code {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            if link['href'].endswith('.mp4'):
                return link['href']

        print("No .mp4 link found in the response.")
        return None

    except Exception as e:
        print(f"Error in get_reel_download_link: {e}")
        return None

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! Send me a public Instagram Reel link and I’ll fetch the video for you!")

# Message handler for receiving URLs
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com/reel/" in url:
        await update.message.reply_text("⏳ Fetching download link…")
        video_link = get_reel_download_link(url)
        if video_link:
            await update.message.reply_text(f"✅ Here's your download link:\n{video_link}")
        else:
            await update.message.reply_text("❌ Sorry, I couldn’t fetch the video. Please check the link and try again.")
    else:
        await update.message.reply_text("⚠️ Please send a valid Instagram Reel link.")

# Main app
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("🚀 Bot is running...")
app.run_polling()
