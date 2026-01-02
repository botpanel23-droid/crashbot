import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from datetime import datetime, timedelta

API_TOKEN = "8550954767:AAFD-u5tdLHFshIPK6aQQzAJCn6-Ax1azCA"
OWNER_ID = 8452357204  # owner telegram id

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

bot_stopped = False
premium_users = set()
waiting_time = set()

# Keyboard
main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="/signal")]],
    resize_keyboard=True
)

# /start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    uid = message.from_user.id
    await message.answer(
        f"👋 Welcome to Signal Bot\n\n🆔 Your User ID: {uid}",
        reply_markup=main_kb
    )

# /signal
@dp.message(Command("signal"))
async def signal_cmd(message: types.Message):
    uid = message.from_user.id

    if bot_stopped and uid not in premium_users and uid != OWNER_ID:
        await message.answer(
            "❌ Bot restricted.\n"
            "Please activate Premium for your User ID."
        )
        return

    waiting_time.add(uid)
    await message.answer(
        "Please send the current time in English format.\n"
        "Example: 10:16"
    )

# Time input
@dp.message()
async def time_handler(message: types.Message):
    uid = message.from_user.id

    if uid not in waiting_time:
        return

    try:
        user_time = datetime.strptime(message.text, "%H:%M")
        signal_time = user_time + timedelta(minutes=5)

        waiting_time.remove(uid)

        await message.answer(
            f"⏰ Your Time: {user_time.strftime('%H:%M')}\n"
            f"⏰ Signal Time: {signal_time.strftime('%H:%M')}\n\n"
            f"⚠️ When placing a bet, bet on the round AFTER this time."
        )
    except:
        await message.answer("❌ Invalid format! Use HH:MM (Example: 10:16)")

# /stop (Owner)
@dp.message(Command("stop"))
async def stop_cmd(message: types.Message):
    global bot_stopped
    if message.from_user.id != OWNER_ID:
        return

    bot_stopped = True
    await message.answer("🚫 Bot stopped for FREE users.")

# /premium <id>
@dp.message(Command("premium"))
async def premium_cmd(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return

    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Usage: /premium <userid>")
        return

    uid = int(args[1])
    premium_users.add(uid)

    await message.answer(f"✅ Premium activated for {uid}")
    try:
        await bot.send_message(uid, "✅ Premium Activated!\nYou can now use the bot.")
    except:
        pass

# Start bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
