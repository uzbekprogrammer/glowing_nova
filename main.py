import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import submission
from database.core import init_db

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logging.error("BOT_TOKEN variable is not set in .env file.")
        return

    bot = Bot(token=bot_token)
    dp = Dispatcher()

    # Register routers
    dp.include_router(submission.router)

    # Initialize database
    logging.info("Initializing database...")
    await init_db()
    logging.info("Database initialized.")

    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
             asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
