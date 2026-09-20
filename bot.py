import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ---------- CONFIG ----------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_URL = os.environ.get("CHANNEL_URL", "https://t.me/yourchannel")
SUPPORT_URL = os.environ.get("SUPPORT_URL", "https://t.me/yoursupport")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------- TEXT ----------
WELCOME = (
    "🎉 សូមស្វាគមន៍មកកាន់ *បក្សីកីឡា-24* 🎉\n\n"
    "✅ ព័ត៌មានកីឡា និងលទ្ធផលផ្ទាល់\n"
    "✅ វិភាគ និងទស្សន៍ទាយ\n"
    "✅ ភ្ជាប់ជាមួយសហគមន៍យើង\n\n"
    "សូមជ្រើសរើសជម្រើសខាងក្រោម 👇"
)

HELP_TEXT = (
    "📖 *របៀបប្រើប្រាស់*\n\n"
    "/start - ចាប់ផ្តើម\n"
    "/help - ជំនួយ\n"
    "/about - អំពីយើង\n"
    "/contact - ទំនាក់ទំនង\n"
    "/channel - ឆានែលផ្លូវការ"
)

ABOUT_TEXT = (
    "🏆 *បក្សីកីឡា-24*\n\n"
    "យើងផ្តល់ព័ត៌មានកីឡាដែលអាចទុកចិត្តបាន 24/7\n"
    "ទាំងកីឡាបាល់ទាត់ បាល់បោះ និងច្រើនទៀត។\n\n"
    "សូមអរគុណសម្រាប់ការគាំទ្រ! 🙏"
)


# ---------- KEYBOARDS ----------
def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📢 ឆានែលផ្លូវការ", url=CHANNEL_URL)],
        [InlineKeyboardButton("💬 ទំនាក់ទំនង", url=SUPPORT_URL)],
        [InlineKeyboardButton("ℹ️ អំពីយើង", callback_data="about")],
        [InlineKeyboardButton("📖 ជំនួយ", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ---------- HANDLERS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    name = user.first_name if user else "អ្នកប្រើ"
    text = f"សូមស្វាគមន៍ *{name}*!\n\n" + WELCOME
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=main_menu()
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        HELP_TEXT, parse_mode="Markdown", reply_markup=main_menu()
    )


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        ABOUT_TEXT, parse_mode="Markdown", reply_markup=main_menu()
    )


async def contact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "💬 សូមទំនាក់ទំនងតាមរយៈ៖ " + SUPPORT_URL,
        disable_web_page_preview=True,
    )


async def channel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📢 ចូលរួមឆានែលផ្លូវការរបស់យើង៖ " + CHANNEL_URL,
        disable_web_page_preview=True,
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "about":
        await query.edit_message_text(
            ABOUT_TEXT, parse_mode="Markdown", reply_markup=main_menu()
        )
    elif query.data == "help":
        await query.edit_message_text(
            HELP_TEXT, parse_mode="Markdown", reply_markup=main_menu()
        )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply friendly to any unknown text."""
    await update.message.reply_text(
        "🙏 សូមអរគុណសម្រាប់សារ!\n"
        "សូមជ្រើសរើសពីម៉ឺនុយ ឬវាយ /start ដើម្បីចាប់ផ្តើម។",
        reply_markup=main_menu(),
    )


# ---------- MAIN ----------
def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit("❌ BOT_TOKEN not set in environment variables.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CommandHandler("contact", contact_cmd))
    app.add_handler(CommandHandler("channel", channel_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("🤖 បក្សីកីឡា-24 bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
