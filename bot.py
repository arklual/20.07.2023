from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, date
import zoneinfo
from settings import *
import os
import aiofiles
import json

zone = zoneinfo.ZoneInfo("Europe/Moscow")
app = Client("bot", api_id=api_id, api_hash=api_hash)

@app.on_message()
async def on_new_message(client, message:Message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id in CHATS:
        data = []
        async with aiofiles.open('to_upload.json', 'r',encoding='utf-8') as fp:
            data = json.loads(await fp.read())
        for i in data:
            if i['telegram_id'] == user_id:
                return
        data.append({
            'chat': str(message.chat.title),
            'first_name': str(message.from_user.first_name),
            'last_name': str(message.from_user.last_name),
            'username': str(message.from_user.username),
            'telegram_id': str(user_id),
            'phone': str(message.from_user.phone_number),
            'date': str(datetime.now(zone).date)
        })
        async with aiofiles.open('to_upload.json', 'w',encoding='utf-8') as fp:
            await fp.write(json.dumps(data, ensure_ascii=False))


app.run()