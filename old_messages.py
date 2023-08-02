from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, date
import zoneinfo
from settings import *
import os
import sys
import json
import pygsheets


zone = zoneinfo.ZoneInfo("Europe/Moscow")
app = Client("bot", api_id=api_id, api_hash=api_hash)
app.start()
chat_id = sys.argv[1]
gc = pygsheets.authorize(service_account_file='sheets_key.json')
ws = gc.open('База по крипте').worksheet()

try: chat_id = int(chat_id)
except: chat_id = str(chat_id)

history = app.get_chat_history(chat_id=chat_id, limit=10)
data = []
for m in history:
    if m.from_user:
        data.append({
            'chat': str(m.chat.title),
            'first_name': str(m.from_user.first_name),
            'last_name': str(m.from_user.last_name),
            'username': str(m.from_user.username),
            'telegram_id': str(m.from_user.id),
            'phone': str(m.from_user.phone_number),
            'date': str(m.date.date()),
            'link': str(m.link)}),

with open('to_upload_new.json', 'w', encoding='utf-8') as fp:
    json.dump(data, fp)
app.stop()
ids = ws.get_col(1)
for n,i in enumerate(ids):
    if i == '':
        ids = ids[:n]
        break
with open('to_upload_new.json', 'r', encoding='utf-8') as fp:
    data = json.loads(fp.read())
    for n, i in enumerate(data):
        j = len(ids)+1
        print('m',n)
        if str(i['telegram_id']) not in ids:
            ws.update_row(j, [i['telegram_id'], i['first_name'], i['last_name'], i['username'], i['phone'], i['date'], i['chat'], i['link']])
            ids.append(str(i['telegram_id']))
os.remove('to_upload_new.json')