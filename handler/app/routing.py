from aiogram import Router

from handlers.statistic import statistic_router
from handlers.mailling import mailling_router

message_router = Router(name="Message")
inline_router = Router(name="Inline")
