import asyncio
import aiofiles
import json
import pygsheets
import os

gc = pygsheets.authorize(service_account_file='sheets_key.json')
ws = gc.open('База по крипте').worksheet()

async def upload():
    while True:
        os.system('cp to_upload.json to_upload_temp.json')
        async with aiofiles.open('to_upload.json', 'w', encoding='utf-8') as fp:
            await fp.write('[]')
        ids = ws.get_col(1)
        for n,i in enumerate(ids):
            if i == '':
                ids = ids[:n]
                break
        async with aiofiles.open('to_upload_temp.json', 'r', encoding='utf-8') as fp:
            data = json.loads(await fp.read())
            for n, i in enumerate(data):
                j = len(ids)+1
                print('m',n)
                if str(i['telegram_id']) not in ids:
                    ws.update_row(j, [i['telegram_id'], i['first_name'], i['last_name'], i['username'], i['phone'], i['date'], i['chat']])
                    ids.append(str(i['telegram_id']))
        os.remove('to_upload_temp.json')
        await asyncio.sleep(3600)


asyncio.run(upload())