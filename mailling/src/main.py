from contextlib import asynccontextmanager

import fastapi
from pydantic import BaseModel

from telethon import TelegramClient
import asyncio
import os

from datetime import datetime

import json

import logging

logger = logging.getLogger(__name__)
FORMAT = '[%(asctime)s]\t%(message)s'
logging.basicConfig(filename='log.log', format=FORMAT)

HELLO_MESSAGE_PARTS = [
    "Приветствую, солнце!!",
    "Хочу пригласить тебя в флуд по монологу фармацевта!",
    "",
    "Если согласен(а), прошу дай мне знак, если же нет, то проигнорируй.",
    "Не кидайте в бан пожалуйста, милейшая(ый)",
    "",
    "Инфо — https://t.me/+PMfqpqP0d_VlNTg6"
]

HELLO_MESSAGE = "\n".join(HELLO_MESSAGE_PARTS)

class AbstractStorage:
    data : list
    def __init__(self, filepath):
        data_dir = os.environ["data_dir"]
        self.filepath = os.path.join(data_dir, filepath)
        
        if not os.path.isfile(self.filepath):
            with open(self.filepath, "w+") as f:
                json.dump([], f, indent=4)
        self.load()

    def load(self):
        with open(self.filepath, "r") as f:
            self.data = json.load(f)

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

class MaillingQueue(AbstractStorage):
    def __init__(self, filepath : str = "queue.json"):
        super().__init__(filepath)
        
    def __call__(self, users : list):
        start_time = int(datetime.now().timestamp())
        if self.data:
            start_time = self.data[-1]['time'] + 5 * 60

        for i, user in enumerate(users):
            self.data.append({
                    "user": f"@{user}",
                    "time": start_time + 5 * 60 * i
                })
        self.save()

    def get_user(self):
        if not self.data or self.data[0]['time'] > int(datetime.now().timestamp()):
            return None
            
        user = self.data.pop(0)
        self.save()

        return user
    
    def get_queue(self):
        return self.data

class DoneLsit(AbstractStorage):
    def __init__(self, filepath : str = "done.json"):
        super().__init__(filepath)

    def __call__(self, user : str):
        self.data.append(user.lower())
        self.save()

    def user_in_list(self, user : str) -> bool:
        if user.lower() in self.data:
            return True
        else:
            self.data.append(user)
            self.save()
            return False

class PostMessage(BaseModel):
    users : list

async def mailling_loop():
    api_id = os.environ["api_id"]
    api_hash = os.environ["api_hash"]

    while True:
        try:
            async with TelegramClient(session="dd4rky_dev", 
                api_id=api_id,
                api_hash=api_hash,
                loop=loop) as client:
                user = queue.get_user()

                if user:
                    await client.send_message(user['user'], HELLO_MESSAGE)
                await asyncio.sleep(5)
        except:
            pass
@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(mailling_loop())
    yield
    queue.save()
    done_list.save()

app = fastapi.FastAPI(debug=False, lifespan=lifespan)
queue = MaillingQueue()
done_list = DoneLsit()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@app.post("/mailling")
def mailling(request : PostMessage):
    logging.info(1)
    global queue, done_list

    users = []

    for user in request.users:
        if done_list.user_in_list(user):
            continue
        users.append(user)

    queue(users)

@app.get('/get_queue')
def get_queue():
    global queue

    queue_data = queue.get_queue()

    return json.dumps(queue_data)




