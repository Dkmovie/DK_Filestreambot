#(c) Adarsh-Goel
import os
import asyncio
from asyncio import TimeoutError
from Adarsh.bot import StreamBot
from Adarsh.utils.database import Database
from Adarsh.utils.human_readable import humanbytes
from Adarsh.vars import Var
from urllib.parse import quote_plus
from pyrogram import filters, Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.name)


MY_PASS = os.environ.get("MY_PASS",None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")


@StreamBot.on_message((filters.regex("loginπ") | filters.command("login")) , group=4)
async def login_handler(c: Client, m: Message):
    try:
        try:
            ag = await m.reply_text("Now send me password.\n\n for πΏπ°ππππΎππ³ send  π΅ππ΄π΄ π³πΌ @R_KOHLI  \n\n (for running bot need contributions..unwanted message = ban + report)")
            _text = await c.listen(m.chat.id, filters=filters.text, timeout=90)
            if _text.text:
                textp = _text.text
                if textp=="/cancel":
                   await ag.edit("Process Cancelled Successfully")
                   return
            else:
                return
        except TimeoutError:
            await ag.edit("I can't wait more for password, try again")
            return
        if textp == MY_PASS:
            await pass_db.add_user_pass(m.chat.id, textp)
            ag_text = "yeah! you entered the password correctly"
        else:
            ag_text = "Wrong password, try again"
        await ag.edit(ag_text)
    except Exception as e:
        print(e)

@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio | filters.photo) , group=4)
async def private_receive_handler(c: Client, m: Message):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(m.chat.id)
        if check_pass== None:
            await m.reply_text("Κα΄Ι’ΙͺΙ΄ ?ΙͺΚsα΄ α΄sΙͺΙ΄Ι’ /login α΄α΄α΄(α΄Κα΄α΄ /login)  \n\n for πΏπ°ππππΎππ³ send  π΅ππ΄π΄ π³πΌ @R_KOHLI \n\n (for running bot need contributions..unwanted message = ban + report)")
            return
        if check_pass != MY_PASS:
            await pass_db.delete_user(m.chat.id)
            return
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"Nα΄α΄‘ Usα΄Κ Jα΄ΙͺΙ΄α΄α΄ : \n\n Nα΄α΄α΄ : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Sα΄α΄Κα΄α΄α΄ Yα΄α΄Κ Bα΄α΄ !!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == enums.ChatMemberStatus.BANNED:
                await c.send_message(
                    chat_id=m.chat.id,
                    text="Κα΄α΄ α΄Κα΄ π±π°π½π½α΄α΄ Κα΄α΄α΄α΄sα΄ α΄? α΄ Ιͺα΄Κα΄α΄ΙͺΙ΄Ι’ Κα΄Κα΄sπ../**",
                    disable_web_page_preview=True
                )
                return 
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<i>α΄α΄ΙͺΙ΄ α΄Κ α΄α΄α΄α΄α΄α΄s α΄Κα΄Ι΄Ι΄α΄Κ α΄α΄ α΄sα΄ α΄α΄..**</i>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("α΄α΄ΙͺΙ΄ Ι΄α΄α΄‘", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                )
            )
            return
        except Exception as e:
            await m.reply_text(e)
            await c.send_message(
                chat_id=m.chat.id,
                text="**π°π³π³ π΅πΎππ²π΄ πππ± ππΎ π°π½π π²π·π°π½π½π΄π»**",
                disable_web_page_preview=True)
            return
    try:

        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        
        online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
       
        
        

        msg_text ="""
<b>Κα΄α΄Κ ΚΙͺΙ΄α΄ Ιͺs Ι’α΄Ι΄α΄Κα΄α΄α΄α΄...β‘

<b>π§ ?ΙͺΚα΄ Ι΄α΄α΄α΄ :- </b> <i><b>{}</b></i>

<b>π¦ ?ΙͺΚα΄ sΙͺα΄’α΄ :- </b> <i><b>{}</b></i>

<b>π α΄α΄α΄‘Ι΄Κα΄α΄α΄ ΚΙͺΙ΄α΄ :- </b> <i><b>{}</b></i>

<b>π₯ α΄‘α΄Κα΄Κ α΄Ι΄ΚΙͺΙ΄α΄ :- </b> <i><b>{}</b></i>

<b>β»οΈ α΄ΚΙͺs ΚΙͺΙ΄α΄ Ιͺs α΄α΄Κα΄α΄Ι΄α΄Ι΄α΄ α΄Ι΄α΄ α΄‘α΄Ι΄'α΄ Ι’α΄α΄s α΄xα΄ΙͺΚα΄α΄ β»οΈ\n\n@movie_a1</b>"""

        await log_msg.reply_text(text=f"**Rα΄Qα΄α΄κ±α΄α΄α΄ ΚΚ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uκ±α΄Κ Ιͺα΄ :** `{m.from_user.id}`\n**Stream ΚΙͺΙ΄α΄ :** {stream_link}", disable_web_page_preview=True, quote=True)
        await m.reply_text(
            text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link, stream_link),
            
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("β‘ α΄‘α΄α΄α΄Κ β‘", url=stream_link), #Stream Link
                                                InlineKeyboardButton('β‘ α΄α΄α΄‘Ι΄Κα΄α΄α΄ β‘', url=online_link)]]) #Download Link
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gα΄α΄ FΚα΄α΄α΄Wα΄Ιͺα΄ α΄? {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**ππππ πΈπ³ :** `{str(m.from_user.id)}`", disable_web_page_preview=True)


@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.photo) & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(broadcast.chat.id)
        if check_pass == None:
            await broadcast.reply_text("Login first using /login cmd \n don\'t know the pass? request it from @R_KOHLI")
            return
        if check_pass != MY_PASS:
            await broadcast.reply_text("Wrong password, login again")
            await pass_db.delete_user(broadcast.chat.id)
            return
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"       
        online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        await log_msg.reply_text(
            text=f"**CΚα΄Ι΄Ι΄α΄Κ Nα΄α΄α΄:** `{broadcast.chat.title}`\n**CΚα΄Ι΄Ι΄α΄Κ ID:** `{broadcast.chat.id}`\n**Rα΄Η«α΄α΄sα΄ α΄ΚΚ:** {stream_link}",
            quote=True
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            id=broadcast.id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("β‘ α΄‘α΄α΄α΄Κ β‘", url=stream_link),
                     InlineKeyboardButton('β‘ α΄α΄α΄‘Ι΄Κα΄α΄α΄ β‘', url=online_link)] 
                ]
            )
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"Gα΄α΄ FΚα΄α΄α΄Wα΄Ιͺα΄ α΄? {str(w.x)}s from {broadcast.chat.title}\n\n**CΚα΄Ι΄Ι΄α΄Κ ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#α΄ΚΚα΄Κ_α΄Κα΄α΄α΄Κα΄α΄α΄:** `{e}`", disable_web_page_preview=True)
        print(f"Cα΄Ι΄'α΄ Eα΄Ιͺα΄ BΚα΄α΄α΄α΄α΄sα΄ Mα΄ssα΄Ι’α΄!\nEΚΚα΄Κ:  **Give me edit permission in updates and bin Chanell{e}**")
