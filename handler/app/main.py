from aiogram import Dispatcher, Bot
import asyncio

import os
import logging

from routing import statistic_router, mailling_router, message_router, inline_router

FORMAT = '[%(asctime)s]\t%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# load token from env variable
if os.environ["DEBUG"] == "true":
    token = os.environ["debug_token"]
else:
    token = os.environ["token"]


# define dispatcher and bot
dp = Dispatcher()
bot = Bot(token)

# main function
async def main():
    dp.include_routers(statistic_router, mailling_router, message_router, inline_router)
    await dp.start_polling(bot)

# start
if __name__ == '__main__':
    asyncio.run(main())