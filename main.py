import os, json, random, openai, logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# 🌟 Load environment
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "7985313998:AAGwmmTLYfzBDgdOfm96yWFMQGrFqPMi3fo")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
SUPERADMIN_ID = int(os.getenv("SUPERADMIN_ID", "6659102577"))
BACKUP_ADMINS = [6333465234, 6994450514]
openai.api_key = OPENAI_API_KEY

# 📁 Load or create config
config_path = "config.json"
if not os.path.exists(config_path):
    default_config = {
        "project_name": "$GALAXYX",
        "emoji": "🌌",
        "threshold": 75,
        "roadmap": ["Token Launch", "Bot Deployment", "AI Meme Engine"],
        "links": {
            "website": "https://galaxyx.io",
            "chart": "https://dexscreener.com",
            "twitter": "https://x.com/galaxyxtoken"
        }
    }
    with open(config_path, "w") as f:
        json.dump(default_config, f, indent=2)

with open(config_path, "r") as f:
    config = json.load(f)

# 🧠 AI Prompt
def get_ai_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], temperature=0.7
    )
    return response.choices[0].message.content

# 🎉 Welcome Pool
welcome_msgs = [f"🚀 Welcome {{username}} to {config['emoji']} {config['project_name']}!", f"🌌 {{username}}, get ready to meme and raid!"]

# ❌ Foul Words
bad_words = ["scam", "rug", "hack", "dump", "trash", "larp", "shitcoin"]

# 👑 Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    if uid == SUPERADMIN_ID or uid in BACKUP_ADMINS:
        buttons = [
            [InlineKeyboardButton("🔧 Edit Project Name", callback_data="edit_name")],
            [InlineKeyboardButton("🌌 Edit Emoji", callback_data="edit_emoji")],
            [InlineKeyboardButton("💸 Buy Threshold", callback_data="edit_thresh")],
            [InlineKeyboardButton("📄 Show Roadmap", callback_data="roadmap")],
            [InlineKeyboardButton("📣 Show Links", callback_data="show_links")],
        ]
        await update.message.reply_text(f"👑 Hello @{username}! Admin Panel:", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        msg = random.choice(welcome_msgs).replace("{username}", f"@{username}")
        await update.message.reply_text(msg)

# 🤖 Help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠 Use /start to view menu.\nEdit project settings as Superadmin.")

# 🧠 AI Timed Posts
async def ai_posts(context: ContextTypes.DEFAULT_TYPE):
    joke = get_ai_text("Tell me a short crypto joke.")
    hype = get_ai_text(f"Give a motivational message for {config['project_name']}")
    await context.bot.send_message(chat_id=context.job.chat_id, text=f"🤣 {joke}")
    await context.bot.send_message(chat_id=context.job.chat_id, text=f"🚀 {hype}")

# 🚫 Foul Word Filter
async def word_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    for word in bad_words:
        if word in text:
            await update.message.delete()
            await update.message.reply_text("⚠️ Please keep it clean.")
            break

# ❓ Unknown
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Command not recognized. Try /start or /help.")

# 🔘 Button Handling
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == "edit_name":
        config["project_name"] = "GalaxyX (edited)"
        await query.edit_message_text(f"✅ Project name updated: {config['project_name']}")
    elif action == "edit_emoji":
        config["emoji"] = "🚀"
        await query.edit_message_text(f"✅ Emoji updated to: {config['emoji']}")
    elif action == "edit_thresh":
        config["threshold"] = 100
        await query.edit_message_text(f"✅ Buy threshold set to ${config['threshold']}")
    elif action == "roadmap":
        roadmap = "\n• " + "\n• ".join(config["roadmap"])
        await query.edit_message_text(f"📄 Roadmap:\n{roadmap}")
    elif action == "show_links":
        links = config["links"]
        text = f"🌐 Links:\nWebsite: {links['website']}\nChart: {links['chart']}\nTwitter: {links['twitter']}"
        await query.edit_message_text(text)

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

# ✅ Command Registration
async def set_commands(app):
    cmds = [
        BotCommand("start", "Launch admin panel"),
        BotCommand("help", "Show usage guide")
    ]
    await app.bot.set_my_commands(cmds)

# 🚀 Launch Bot
logging.basicConfig(level=logging.INFO)
app = ApplicationBuilder().token(BOT_TOKEN).post_init(set_commands).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), word_filter))
app.add_handler(MessageHandler(filters.COMMAND, unknown))
app.add_handler(CallbackQueryHandler(button_handler))
app.job_queue.run_repeating(ai_posts, interval=1800, first=15, chat_id=SUPERADMIN_ID)
app.run_polling()
