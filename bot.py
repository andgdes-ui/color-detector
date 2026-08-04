import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiohttp import web  # <-- Новая библиотека для веб-сервера

# --- Ваши данные ---
BOT_TOKEN = "8744042828:AAGea9YUqQbLfKD1M7x2Ah8mNel_U1mdMtQ"
WEB_APP_URL = "https://andgdes-ui.github.io/color-detector/"

# --- Инициализация бота ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Обработчики команд бота ---
@dp.message(Command("start"))
async def start(message: types.Message):
    web_app = WebAppInfo(url=WEB_APP_URL, allow_write_to_camera=True)
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

# --- ЗДЕСЬ НОВЫЙ КОД: Запускаем веб-сервер для Render ---
async def health_check(request):
    return web.Response(text="I'm alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)  # <-- Будет отвечать на запросы по адресу /
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 8080))) # <-- Слушаем порт от Render
    await site.start()
    print(f"✅ Веб-сервер запущен на порту {os.environ.get('PORT', 8080)}")
    # Бесконечно держим сервер включенным
    await asyncio.Event().wait()

# --- Основная функция ---
async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запускаем поллинг бота и веб-сервер параллельно
    await asyncio.gather(
        dp.start_polling(bot),
        start_web_server()
    )

if __name__ == "__main__":
    # Добавляем импорт os для получения переменной PORT
    import os
    asyncio.run(main())
