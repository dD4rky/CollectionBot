from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime, timedelta, timezone

import requests
from json import loads
import re

from .filters import *

mailling_router = Router(name="Mailling")

def create_message(i, user):
    username = user["user"]

    tz = timezone(timedelta(hours=3), name="UTC+3")
    time = datetime.fromtimestamp(int(user["time"]), tz).strftime("%d/%m/%Y, %H:%M:%S")

    return f"{i}. {username}\n|\t{time}"

@mailling_router.message(ChatTypeFilter('private'), MessageTypeFilter('text'), Command("get_queue"))
async def get_queue(msg : Message):
    queue = requests.get("http://mailling:8080/get_queue")

    queue_data = loads(queue.json())

    message = "Now queue is empty"

    if queue_data:
        messages = [create_message(i, user) for i, user in enumerate(queue_data, start=1)]
        message = "\n".join(messages)

    await msg.answer(text=message)

@mailling_router.message(ChatTypeFilter('private'), MessageTypeFilter('text'))
async def register_mailling(msg : Message):
    user_pattern = r'@(\w+){0,1000}'
    users = re.findall(user_pattern, msg.text)

    if not users:
        return
        
    request_data = {
        "users" : users
    }
    requests.post("http://mailling:8080/mailling", json=request_data)