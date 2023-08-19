from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from pyrogram.errors import FloodWait
import humanize
import random
from helper_funcs.translation import translation
from helper_funcs.database import db
from config import WELCOME_BANNER, FLOOD, ADMIN 


@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)             
    txt=f"Hey! {}\n
I'm Renamer + File To Video Converter Bot With Permanent Thumbnail Support!⚡</b>
<b>Do /help for more Details ...</b>"
    button=InlineKeyboardMarkup([[
        InlineKeyboardButton("❗ Help", callback_data = "help")
        ],[
        InlineKeyboardButton('🏆 Support Channel', url='https://t.me/Cartoon_Seriesz'),
        InlineKeyboardButton('💬 Feedback', url='https://t.me/Dlaize')
        ],[
        InlineKeyboardButton('‼️ About', callback_data = "about"),
        ]])
    if WELCOME_BANNER:
        await message.reply_photo(WELCOME_BANNER, caption=txt, reply_markup=button)       
    else:
        await message.reply_text(text=txt, reply_markup=button, disable_web_page_preview=True)
   

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size) 
    fileid = file.file_id
    try:
        text = f"""**__What do you want me to do with this file.?__**\n\n**➜ ꜰɪʟᴇ ɴᴀᴍᴇ** :- `{filename}`\n\n**➜ ꜰɪʟᴇ ꜱɪᴢᴇ** :- `{filesize}`"""
        buttons = [[ InlineKeyboardButton("📝 Rename", callback_data="rename") ],
                   [ InlineKeyboardButton("❌ Cancel", callback_data="cancel") ]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
        await sleep(FLOOD)
    except FloodWait as e:
        await sleep(e.value)
        text = f"""**__What do you want me to do with this file.?__**\n\n**➜ ꜰɪʟᴇ ɴᴀᴍᴇ** :- `{filename}`\n\n**➜ ꜰɪʟᴇ ꜱɪᴢᴇ** :- `{filesize}`"""
        buttons = [[ InlineKeyboardButton("📝 Rename", callback_data="rename") ],
                   [ InlineKeyboardButton("❌ Cancel", callback_data="cancel") ]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=f"""Hey! {}\n
I'm Renamer + File To Video Converter Bot With Permanent Thumbnail Support!⚡</b>
<b>Do /help for more Details ...</b>""",
            reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("❗ Help", callback_data = "help")
        ],[
        InlineKeyboardButton('🏆 Support Channel', url='https://t.me/Cartoon_Seriesz'),
        InlineKeyboardButton('💬 Feedback', url='https://t.me/Dlaize')
        ],[
        InlineKeyboardButton('‼️ About', callback_data = "about"),
        ]])
            )
    elif data == "help":
        await query.message.edit_text(
            text=translation.HELP_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton('🍬 Anime Channel', url='https://t.me/Cartoon_Seriesz')
               ],[
               InlineKeyboardButton('💬 Feedback', url='https://t.me/Dlaize')
               ],[
               InlineKeyboardButton("🔒 Close", callback_data = "close"),
               InlineKeyboardButton("◀️ Back", callback_data = "start")
               ]]
            )
        )
    elif data == "about":
        await query.message.edit_text(
            text=translation.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup( [[
               #⚠️ don't change source code & source link ⚠️ #
               InlineKeyboardButton('🍬 Anime Channel', url='https://t.me/Cartoon_Seriesz')
               ],[
               InlineKeyboardButton('💬 Feedback', url='https://t.me/Dlaize')
               ],[
               InlineKeyboardButton("🔒 Close", callback_data = "close"),
               InlineKeyboardButton("◀️ Back", callback_data = "start")
               ]]
            )
        )
    elif data == "dev":
        await query.message.edit_text(
            text=translation.DEV_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               #⚠️ don't change source code & source link ⚠️ #
               InlineKeyboardButton('🍬 Anime Channel', url='https://t.me/Cartoon_Seriesz')
               ],[
               InlineKeyboardButton('💬 Feedback', url='https://t.me/Dlaize')
               ],[
               InlineKeyboardButton("🔒 Close", callback_data = "close"),
               InlineKeyboardButton("◀️ Back", callback_data = "start")
               ]]
            )
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()
