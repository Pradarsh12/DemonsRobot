import os
from aries import dispatcher
from aries.modules.disable import DisableAbleCommandHandler
from aries.events import register

from telegram.ext import CallbackContext

from aiohttp import ClientSession
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from Python_ARQ import ARQ 
from asyncio import get_running_loop
from wget import download
from aries import ARQ_API_KEY, TOKEN
# Config Check-----------------------------------------------------------------

# ARQ API and Bot Initialize---------------------------------------------------
session = ClientSession()
arq = ARQ("https://thearq.tech", ARQ_API_KEY, session)
pornhub = arq.pornhub

async def download_url(url: str):
    loop = get_running_loop()
    file = await loop.run_in_executor(None, download, url)
    return file

async def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
    )
  # Let's Go----------------------------------------------------------------------
  @register(pattern="^/phub ?(.*)")
  async def sarch(_,message):
    try:
        if "/" in message.text.split(None,1)[0]:
            await message.reply_text(
                "**💡 usage:**\njust type the phub video name you want to download, and this bot will send you the result."
            )
            return
    except:
        pass
    m = await message.reply_text("getting results...")
    search = message.text
    try:
        resp = await pornhub(search,thumbsize="large")
        res = resp.result
    except:
        await m.edit("not found: 404")
        return
    if not resp.ok:
        await m.edit("not found, try again")
        return
    resolt = f"""
**🏷 TITLE:** {res[0].title}
**⏰ DURATION:** {res[0].duration}
**👁‍🗨 VIEWERS:** {res[0].views}
**🌟 RATING:** {res[0].rating}"""
    await m.delete()
    m = await message.reply_photo(
        photo=res[0].thumbnails[0].src,
        caption=resolt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("▶️ NEXT",
                                         callback_data="next"),
                    InlineKeyboardButton("🗑 DELETE",
                                         callback_data="delete"),
                ],
                [
                    InlineKeyboardButton("📥 DOWNLOAD",
                                         callback_data="dload")
                ]
            ]
        ),
        parse_mode="markdown",
    )
    new_db={"result":res,"curr_page":0}
    db[message.chat.id] = new_db
    
 # Next Button--------------------------------------------------------------------------
async def callback_query_next(_, next):
    m = next.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page+1
    db[query.message.chat.id]['curr_page'] = cur_page
    if len(res) <= (cur_page+1):
        cbb = [
                [
                    InlineKeyboardButton("◀️ PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("📥 DOWNLOAD",
                                         callback_data="dload"),
                ],
                [
                    InlineKeyboardButton("🗑 DELETE",
                                         callback_data="delete"),
                ]
              ]
    else:
        cbb = [
                [
                    InlineKeyboardButton("◀️ PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("▶️ NEXT",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🗑 DELETE",
                                         callback_data="delete"),
                    InlineKeyboardButton("📥 DOWNLOAD",
                                         callback_data="dload")
                ]
              ]
    resolt = f"""
**🏷 TITLE:** {res[cur_page].title}
**⏰ DURATION:** {res[curr_page].duration}
**👁‍🗨 VIEWERS:** {res[cur_page].views}
**🌟 RATING:** {res[cur_page].rating}"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )
 
# Previous Button-------------------------------------------------------------------------- 
async def callback_query_next(_, previous):
    m = previous.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1
    db[query.message.chat.id]['curr_page'] = cur_page
    if cur_page != 0:
        cbb=[
                [
                    InlineKeyboardButton("◀️ PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("▶️ NEXT",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🗑 DELETE",
                                         callback_data="delete"),
                    InlineKeyboardButton("📥 DOWNLOAD",
                                         callback_data="dload")
                ]
            ]
    else:
        cbb=[
                [
                    InlineKeyboardButton("▶️ NEXT",
                                         callback_data="next"),
                    InlineKeyboardButton("🗑 DELETE",
                                         callback_data="Delete"),
                ],
                [
                    InlineKeyboardButton("📥DOWNLOAD",
                                         callback_data="dload")
                ]
            ]
    resolt = f"""
**🏷 TITLE:** {res[cur_page].title}
**⏰ DURATION:** {res[curr_page].duration}
**👁‍🗨 VIEWERS:** {res[cur_page].views}
**🌟 RATING:** {res[cur_page].rating}"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )

# Download Button--------------------------------------------------------------------------    
async def callback_query_next(_, dload):
    m = dload.message
    data = db[m.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    dl_links = await phdl(res[curr_page].url)
    db[m.chat.id]['result'] = dl_links.result.video
    db[m.chat.id]['thumb'] = res[curr_page].thumbnails[0].src
    db[m.chat.id]['dur'] = res[curr_page].duration
    resolt = f"""
**🏷 TITLE:** {res[curr_page].title}
**⏰ DURATION:** {res[curr_page].duration}
**👁‍🗨 VIEWERS:** {res[curr_page].views}
**🌟 RATING:** {res[curr_page].rating}"""
    pos = 1
    cbb = []
    for resolts in dl_links.result.video:
        b= [InlineKeyboardButton(f"{resolts.quality} - {resolts.size}", callback_data=f"phubdl {pos}")]
        pos += 1
        cbb.append(b)
    cbb.append([InlineKeyboardButton("Delete", callback_data="delete")])
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )

# Download Button 2--------------------------------------------------------------------------    
async def callback_query_dl(_, phubdl):
    m = phubdl.message
    capsion = m.caption
    entoty = m.caption_entities
    await m.edit(f"**downloading...** :\n\n{capsion}")
    data = db[m.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    thomb = await download_url(data['thumb'])
    durr = await time_to_seconds(data['dur'])
    pos = int(query.data.split()[1])
    pos = pos-1
    try:
        vid = await download_url(res[pos].url)
    except Exception as e:
        print(e)
        await m.edit("download error..., try again")
        return
    await m.edit(f"**Upload Sekarang** :\n\n{capsion}")
    await app.send_chat_action(m.chat.id, "upload_video")
    await m.edit_media(media=InputMediaVideo(vid,thumb=thomb, duration=durr, supports_streaming=True))
    await m.edit_caption(caption=capsion, caption_entities=entoty)
    if os.path.isfile(vid):
        os.remove(vid)
    if os.path.isfile(thomb):
        os.remove(thomb)
    
# Delete Button-------------------------------------------------------------------------- 
async def callback_query_delete(_, delete):
    await delete.message.delete()

PHUB_HANDLER = DisableAbleCommandHandler("phub", phub, run_async=True)
dispatcher.add_handler(PHUB_HANDLER)

__mod_name__ = "PHUB"


__command_list__ = ["odo", "ipe", "diarydodo", "lawak"]
__handlers__ = [PHUB_HANDLER]