import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Токен берем из переменных окружения (об этом ниже)
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Ссылка на твой сервер в Railway (ее мы получим позже)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я работаю в облаке через Webhook!")

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Облако говорит: {message.text}")

async def on_startup(bot: Bot):
    # Говорим Telegram, куда отправлять сообщения
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")

def main():
    app = web.Application()
    dp.startup.register(on_startup)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    # Railway сам подставит нужный порт
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

if __name__ == "__main__":
    main()