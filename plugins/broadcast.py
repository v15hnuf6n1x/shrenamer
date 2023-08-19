import os
import time
import asyncio 
import logging 
import datetime
from config import ADMIN
from helper_funcs.database import db
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
 
@Client.on_message(filters.command("users") & filters.user(ADMIN))
async def get_stats(bot :Client, message: Message):
    Translation = await message.reply('**📡 ᴀᴄᴄᴇꜱꜱɪɴɢ ᴅᴀᴛᴀʙᴀꜱᴇ...**')
    total_users = await db.total_users_count()
    await Translation.edit( text=f"👾 ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ = `{total_users}`")

@Client.on_message(filters.command("broadcast") & filters.user(ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("🪃 ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜱᴛᴀʀᴛᴇᴅ!!") 
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
           success += 1
        else:
           failed += 1
        if sts == 400:
           await db.delete_user(user['_id'])
        done += 1
        if not done % 20:
           await sts_msg.edit(f"ʙʀᴏᴀᴅᴄᴀꜱᴛ ɪɴ ᴘʀᴏɢʀᴇꜱꜱ:\n➠ ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ {total_users}\n➠ ᴄᴏᴍᴘʟᴇᴛᴇᴅ: {done} / {total_users}\n➠ ꜱᴜᴄᴄᴇꜱꜱ: {success}\n➠ ꜰᴀɪʟᴇᴅ: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ:\n➠ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ: `{completed_in}`.\n\n➠ ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ {total_users}\n➠ ᴄᴏᴍᴘʟᴇᴛᴇᴅ: {done} / {total_users}\n➠ ꜱᴜᴄᴄᴇꜱꜱ: {success}\n➠ ꜰᴀɪʟᴇᴅ: {failed}")
           
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : ᴜꜱᴇʀ ɪᴅ ɪɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500
 
