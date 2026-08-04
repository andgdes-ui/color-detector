import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command

BOT_TOKEN = "8744042828:AAGea9YUqQbLfKD1M7x2Ah8mNel_U1mdMtQ"
WEB_APP_URL = "https://andgdes-ui.github.io/color-detector/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    web_app = WebAppInfo(url=WEB_APP_URL, allow_write_to_camera=True)  # <-- ВКЛЮЧАЕТ КАМЕРУ
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📸 Открыть камеру", web_app=web_app)]
        ]
    )
    await message.answer("Нажмите кнопку, чтобы открыть приложение", reply_markup=keyboard)

@dp.message(lambda message: message.web_app_data is not None)
async def handle_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        await message.answer(f"🎨 Цвет: {data.get('color_name', 'N/A')} ({data.get('hex', 'N/A')})")
    except:
        await message.answer("Ошибка обработки")

async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
