import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from aries.events import register

@register(pattern="^/sg ?(.*)")
async def _(event):
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_delete(event, "**Mohon Reply Ke Pesan Pengguna.**", 90)
    user, rank = await get_user_from_event(event, secondgroup=True)
    if not user:
        return
    uid = user.id
    chat = "@SangMataInfo_bot"
    manevent = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"/search_id {uid}")
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            await conv.send_message(f"/search_id {uid}")
        responses = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            responses.append(response.text)
        await event.client.send_read_acknowledge(conv.chat_id)
    if not responses:
        await edit_delete(manevent, "**Orang Ini Belum Pernah Mengganti Namanya**", 90)
    if "No records found" in responses:
        await edit_delete(manevent, "**Orang Ini Belum Pernah Mengganti Namanya**", 90)
    names, usernames = await sangamata_seperator(responses)
    cmd = event.pattern_match.group(1)
    risman = None
    check = usernames if cmd == "u" else names
    for i in check:
        if risman:
            await event.reply(i, parse_mode=_format.parse_pre)
        else:
            risman = True
            await manevent.edit(i, parse_mode=_format.parse_pre)
