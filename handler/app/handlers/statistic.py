from aiogram import Router
from aiogram.types import Message
import requests

from .filters import *

statistic_router = Router(name="Statistic")

@statistic_router.message(ChatTypeFilter(['group', 'supergroup']),  MessageTypeFilter(['text', 'sticker', 'animation', 'document', 'photo', 'audio', 'voice', 'video', 'video_note', 'story']) )
async def register_message(msg : Message):
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