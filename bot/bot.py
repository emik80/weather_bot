import asyncio

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError

import bot.handlers as user_handlers
from bot.keyboards import set_main_menu
from config import logger, base_config


@logger.catch
async def main():
    logger.info('Starting bot')
    bot = Bot(token=base_config.BOT_TOKEN)
    dp = Dispatcher()

    await set_main_menu(bot)
    dp.include_router(user_handlers.router)
    logger.info('READY')

    while True:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
        except TelegramNetworkError as e:
            logger.exception(f'[BOT EXCEPTION]: Error occurred: {e}. Restarting the bot...')
            await asyncio.sleep(5)
        except Exception as e:
            logger.exception(f'[BOT EXCEPTION]: Unexpected error occurred: {e}. Exiting...')
            break


if __name__ == '__main__':
    asyncio.run(main())
