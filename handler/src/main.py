from aiogram import Dispatcher, Bot
from aiogram.types import Message
import asyncio

import os
import logging

import re

import requests

from filters import ChatTypeFilter, MessageTypeFilter

logger = logging.getLogger(__name__)
FORMAT = '[%(asctime)s]\t%(message)s'
logging.basicConfig(filename='log.log', format=FORMAT)

dp = Dispatcher()

@dp.message(
    ChatTypeFilter(['group', 'supergroup']), 
    MessageTypeFilter('text')
    )
async def statistic(msg : Message):
    if msg.from_user.is_bot:
        return
    
    logger.info(f'\n\rNew message by user: {msg.from_user.id}\n\tMessage: {msg.text}')
    
    request_data = {
        "user_id" : str(msg.from_user.id),
        "msg" : msg.text
    }
    await requests.post("http://statistic:8080/message", json=request_data)

@dp.message(
    ChatTypeFilter('private'),
    MessageTypeFilter('text')
    )
async def mailling(msg : Message):
    user_pattern = r'@(\w+){0,1000}'
    users = re.findall(user_pattern, msg.text)

    if not users:
        return
    
    logger.info(f'\n\rInitializating mailling for users: {", ".join(users)}')
    
    request_data = {
        "users" : users
    }
    await requests.post("http://mailling:8080/mailling", json=request_data)

async def main():
    token = os.environ['token']
    bot = Bot(token)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())