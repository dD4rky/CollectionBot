from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

import os
import logging

import re

import requests
import json

from filters import ChatTypeFilter, MessageTypeFilter

from datetime import datetime

FORMAT = '[%(asctime)s]\t%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

token = os.environ['token']

dp = Dispatcher()
bot = Bot(token)

@dp.message(ChatTypeFilter('private'), MessageTypeFilter('text'), Command("get_queue"))
async def asdfasfsfasfasdf(msg : Message):
    def create_message(i, user):
        username = user["user"]
        time = datetime.fromtimestamp(int(user["time"])).strftime("%d/%m/%Y, %H:%M:%S")
        return f"{i}. {username}\n|\t{time}"

    queue = requests.get("http://mailling:8080/get_queue")

    queue_data = json.loads(queue.json())

    if queue_data:
        messages = [create_message(i, user) for i, user in enumerate(queue_data, start=1)]
        message = "\n".join(messages)

        await bot.send_message(msg.chat.id, message)
    else:
        await bot.send_message(msg.chat.id, "Now queue is empty")

@dp.message(ChatTypeFilter(['group', 'supergroup']),  MessageTypeFilter(['text', 'sticker', 'animation', 'document', 'photo', 'audio', 'voice', 'video', 'video_note', 'story']) )
async def statistic(msg : Message):
    if msg.from_user.is_bot:
        return
    
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

    requests.post("http://statistic:8080/message", json=request_data)

@dp.message(ChatTypeFilter('private'), MessageTypeFilter('text'))
async def mailling(msg : Message):
    user_pattern = r'@(\w+){0,1000}'
    users = re.findall(user_pattern, msg.text)

    if not users:
        return
        
    request_data = {
        "users" : users
    }
    requests.post("http://mailling:8080/mailling", json=request_data)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())