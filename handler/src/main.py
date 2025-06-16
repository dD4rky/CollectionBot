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
    MessageTypeFilter(['text', 'sticker', 'animation', 'document', 'photo', 'audio', 'voice', 'video', 'video_note', 'story'])
    )
async def statistic(msg : Message):
    if msg.from_user.is_bot:
        return
    
    logger.info(f'\n\rNew message by user: {msg.from_user.id}\n\tMessage: {msg.text}')
    request_data = {}

    request_data["user_id"] = str(msg.from_user.id)
    request_data["data_type"] = msg.content_type
    request_data["time"] = msg.date.timestamp()
    
    if msg.content_type == 'text':
        request_data["data"] = msg.text
        request_data["length"] = len(msg.text)
 
    if msg.content_type == 'sticker':
        request_data["data"] = msg.sticker.file_id
        request_data["length"] = 1

    if msg.content_type == 'animation':
        request_data["data"] = msg.animation.file_id
        request_data["length"] = msg.animation.duration

    if msg.content_type == 'document':
        request_data["data"] = msg.document.file_id
        request_data["length"] = 1

    elif msg.content_type == 'photo':
        request_data["data"] = [photo.file_id for photo in msg.photo]
        request_data["length"] = len(request_data["data"])
    
    elif msg.content_type == 'audio':
        request_data["data"] = msg.audio.file_id
        request_data["length"] = msg.audio.duration

    elif msg.content_type == 'voice':
        request_data["data"] = msg.voice.file_id
        request_data["length"] = msg.voice.duration

    elif msg.content_type == 'video':
        request_data["data"] = msg.video.file_id
        request_data["length"] = msg.video.duration

    elif msg.content_type == 'video_note':
        request_data["data"] = msg.video_note.file_id
        request_data["length"] = msg.video_note.duration

    elif msg.content_type == 'story':
        request_data["data"] = msg.story.id
        request_data["length"] = 1

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