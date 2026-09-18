import os
import logging
from datetime import datetime, time
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')  # Your Telegram user ID
TIMEZONE = pytz.timezone('UTC')  # Change to your timezone

# Store user data (in production, use a database)
user_data = {}

# Active hours configuration (24-hour format)
ACTIVE_START = time(9, 0)  # 9:00 AM
ACTIVE_END = time(22, 0)   # 10:00 PM

def is_active_hours():
    """Check if current time is within active hours"""
    current_time = datetime.now(TIMEZONE).time()
    return ACTIVE_START <= current_time <= ACTIVE_END

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    user_id = user.id
    
    # Store user data
    if user_id not in user_data:
        user_data[user_id] = {
            'first_name': user.first_name,
            'username': user.username,
            'joined': datetime.now(TIMEZONE).isoformat(),
            'messages': 0
        }
    
    welcome_message = f"""
👋 Hello {user.first_name}!

Welcome to our bot! I'm here to help you 24/7.

🎯 **What I can do:**
• Respond to your messages
• Provide information
• Help with queries

📊 **Bot Status:** {'🟢 Active' if is_active_hours() else '🟡 Away Mode'}

Type /help to see all commands!
    """
    
    keyboard = [
        [InlineKeyboardButton("📚 Help", callback_data='help')],
        [InlineKeyboardButton("ℹ️ About", callback_data='about')],
        [InlineKeyboardButton("📞 Contact", callback_data='contact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🤖 **Available Commands:**

/start - Start the bot
/help - Show this help message
/about - About this bot
/status - Check bot status
/contact - Contact information

💬 **Just send me a message and I'll respond!**
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    about_text = """
ℹ️ **About This Bot**

This bot is designed to help you with various tasks.
Built with Python and python-telegram-bot library.

🚀 **Features:**
• 24/7 Availability
• Fast Response Time
• User-Friendly Interface

Version: 1.0.0
    """
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    current_time = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")
    
    status_text = f"""
📊 **Bot Status**

🕐 Current Time: {current_time}
📍 Timezone: {TIMEZONE}
{'🟢 Status: Active' if is_active_hours() else '🟡 Status: Away Mode'}

⏰ Active Hours: {ACTIVE_START.strftime('%H:%M')} - {ACTIVE_END.strftime('%H:%M')}
    """
    
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /contact command"""
    contact_text = """
📞 **Contact Information**

For support or inquiries:
• Email: support@example.com
• Telegram: @your_username

We typically respond within 24 hours.
    """
    await update.message.reply_text(contact_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages"""
    user_id = update.effective_user.id
    message_text = update.message.text.lower()
    
    # Update user message count
    if user_id in user_data:
        user_data[user_id]['messages'] += 1
    
    # Check if within active hours
    if not is_active_hours():
        response = """
🌙 **Away Mode**

Thank you for your message! Our bot is currently in away mode.

We'll be back online during active hours:
⏰ 9:00 AM - 10:00 PM (UTC)

Your message has been recorded and we'll respond as soon as possible!
        """
        await update.message.reply_text(response, parse_mode='Markdown')
        return
    
    # Smart responses based on keywords
    if any(word in message_text for word in ['hello', 'hi', 'hey']):
        response = f"Hello {update.effective_user.first_name}! 👋 How can I help you today?"
    elif any(word in message_text for word in ['price', 'cost', 'pricing']):
        response = "💰 For pricing information, please contact our sales team at @your_username"
    elif any(word in message_text for word in ['help', 'support']):
        response = "🆘 I'm here to help! Please describe your issue and I'll assist you."
    elif any(word in message_text for word in ['thank', 'thanks']):
        response = "You're welcome! 😊 Is there anything else I can help you with?"
    else:
        response = """
I received your message! 📝

Our team will review it and get back to you soon.

In the meantime, you can:
• Type /help for commands
• Type /status to check bot status
• Type /contact for contact info
        """
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'help':
        await query.edit_message_text(
            text="📚 Need help? Type /help to see all available commands!",
            parse_mode='Markdown'
        )
    elif query.data == 'about':
        await query.edit_message_text(
            text="ℹ️ This is a multifunctional Telegram bot designed to assist you 24/7!",
            parse_mode='Markdown'
        )
    elif query.data == 'contact':
        await query.edit_message_text(
            text="📞 Contact us at: support@example.com or @your_username",
            parse_mode='Markdown'
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("contact", contact_command))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
