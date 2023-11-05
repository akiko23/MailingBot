from config import bot, db, ADMIN_ID
from markups.markups import main_menu as mmenu

TG_RPS_LIMIT = 30

async def make_mailing(data, keyb=None):
    msg_id = data["msg_id"]
    for r_num, uid in enumerate(filter(lambda x: x != ADMIN_ID, db.get_all_users())):
        if r_num % TG_RPS_LIMIT == 0:
            await asyncio.sleep(1)
        await bot.copy_message(chat_id=uid, from_chat_id=ADMIN_ID, message_id=msg_id, reply_markup=keyb)
    await bot.send_message(ADMIN_ID, "Рассылка завершена", reply_markup=mmenu)
