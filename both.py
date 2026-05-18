import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# توکن رباتت رو اینجا بذار
BOT_TOKEN = "8682112702:AAF2_4G6LeVXjXxToMZ7Abs-ch6hT8zJvs0"

# آدرس کیف پول
WALLET_ADDRESS = "0x7519E3041Dd2Fb75dA5FdA4b77eB0dbD24844B59"

# قیمت‌ها (دلار)
PRICES = {
    "ps10": 9.5,
    "ps20": 19,
    "ps50": 47.5,
    "ps100": 95,
    "apple10": 9.5,
    "apple20": 19,
    "apple50": 47.5,
    "apple100": 95,
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 PS Gift Card", callback_data="menu_ps")],
        [InlineKeyboardButton("🍎 Apple Gift Card", callback_data="menu_apple")],
    ]
    await update.message.reply_text(
        "🎮 *فروشگاه گیفت کارت*\n\nلطفاً یکی رو انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def menu_ps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("$10 - 9.5 USDT", callback_data="ps10")],
        [InlineKeyboardButton("$20 - 19 USDT", callback_data="ps20")],
        [InlineKeyboardButton("$50 - 47.5 USDT", callback_data="ps50")],
        [InlineKeyboardButton("$100 - 95 USDT", callback_data="ps100")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back")],
    ]
    await update.callback_query.message.reply_text(
        "🎮 *PS Gift Card*\nانتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def menu_apple(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("$10 - 9.5 USDT", callback_data="apple10")],
        [InlineKeyboardButton("$20 - 19 USDT", callback_data="apple20")],
        [InlineKeyboardButton("$50 - 47.5 USDT", callback_data="apple50")],
        [InlineKeyboardButton("$100 - 95 USDT", callback_data="apple100")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back")],
    ]
    await update.callback_query.message.reply_text(
        "🍎 *Apple Gift Card*\nانتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    product = query.data
    if product == "back":
        await start(update, context)
        return
    
    price = PRICES.get(product, 0)
    
    await query.message.reply_text(
        f"💰 قیمت: ${price}\n\n"
        f"🧱 آدرس کیف پول (USDT/TRC20):\n"
        f"`{WALLET_ADDRESS}`\n\n"
        "پس از پرداخت اسکرین‌شات بفرستید.",
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_ps, pattern="^menu_ps$"))
    app.add_handler(CallbackQueryHandler(menu_apple, pattern="^menu_apple$"))
    app.add_handler(CallbackQueryHandler(handle_payment))
    
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
