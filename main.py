import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Render передаст эти переменные сам
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Ссылка на твой сервис на Render (мы получим ее позже)
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 
# Render сам назначает порт, берем его из переменной
PORT = int(os.getenv("PORT", 8080))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я работаю в облаке на Render через Webhook!")

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Облако Render говорит: {message.text}")

# Эта функция скажет Telegram, куда стучаться
async def on_startup(bot: Bot):
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")

def main():
    app = web.Application()
    dp.startup.register(on_startup)
    
    # Регистрируем обработчик вебхука
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    
    # Запускаем сервер на порту, который дал Render
    web.run_app(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
