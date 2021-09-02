import re
import os
from asyncio import gather, get_event_loop, sleep

from aiohttp import ClientSession
from pyrogram import Client, filters, idle
from Python_ARQ import ARQ

from pyrogram import Client,filters 
from pyrogram.types import (InlineKeyboardButton,  InlineKeyboardMarkup)


is_config = os.path.exists("config.py")

if is_config:
    from config import *
else:
    from sample_config import *

luna = Client(
    ":memory:",
    bot_token=bot_token,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)

bot_id = int(bot_token.split(":")[0])
arq = None


async def lunaQuery(query: str, user_id: int):
    query = (
        query
        if LANGUAGE == "en"
        else (await arq.translate(query, "en")).result.translatedText
    )
    resp = (await arq.luna(query, user_id)).result
    return (
        resp
        if LANGUAGE == "en"
        else (
            await arq.translate(resp, LANGUAGE)
        ).result.translatedText
    )


async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(2))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, "cancel")


@luna.on_message(filters.command("repo") & ~filters.edited)
async def repo(_, message):
    await message.reply_text(
        "[Creator](https://t.me/KhiladiKing45)"
        + " | [Chatting Group](t.me/Tamil_Chat_Empire)",
        disable_web_page_preview=False,
    )

@luna.on_message(filters.command("chatbot") & ~filters.edited)
async def repo(_, message):
    await message.reply_text("Hey I am Anjel")    

@luna.on_message(filters.command("help") & ~filters.edited)
async def start(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text("/repo - Get Repo Link")
    
    
    
@luna.on_message(filters.command(['start']))
def start(client, message):
    AnjelBots = f'🍁 𝗛𝗲𝗹𝗹𝗼 @{message.from_user.username}\n\n I AM 🎸 ★ANJEL CHAT★᭄ꦿ [🎶](https://telegra.ph/file/dcaf78e7cbd527013194c.jpg)'
    message.reply_text(
        text=AnjelBots, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('♻️𝐒𝐔𝐏𝐏𝐎𝐑𝐓❄️', url='https://t.me/GodofAnjelsupport'),
                    InlineKeyboardButton('⚜️𝐀𝐃𝐃 𝐌𝐄⚜️ ', url='https://t.me/AnjelChatBot?startgroup=true')
                ],
                [
                    InlineKeyboardButton('🍂𝐂𝐇𝐀𝐓𝐓𝐈𝐍𝐆🍃', url='https://t.me/TamilChat07'),
                    InlineKeyboardButton('🔆𝐂𝐑𝐄𝐀𝐓𝐎𝐑🍒', url='https://t.me/KhiladiKing45')
                ]
            ]
        )
    )
    
@luna.on_message(
    & filters.text
    & ~filters.command("help")
    & ~filters.edited,
    group=69,
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        from_user_id = message.reply_to_message.from_user.id
        if from_user_id != bot_id:
            return
    else:
        match = re.search(
            "[.|\n]{0,}luna[.|\n]{0,}",
            message.text.strip(),
            flags=re.IGNORECASE,
        )
        if not match:
            return
    await type_and_send(message)


@luna.on_message(
    filters.private & ~filters.command("help") & ~filters.edited
)
async def chatpm(_, message):
    if not message.text:
        return
    await type_and_send(message)


async def main():
    global arq
    session = ClientSession()
    arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

    await luna.start()
    print(
        """
-----------------
| Luna Started! |
-----------------
"""
    )
    await idle()


loop = get_event_loop()
loop.run_until_complete(main())
