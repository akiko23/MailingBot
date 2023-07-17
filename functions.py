from config import bot, db, ADMIN_ID
from markups.markups import main_menu as mmenu

async def make_mailing(data, keyb=None):
    msg_id = data["msg_id"]
    for uid in filter(lambda x: x != ADMIN_ID, db.get_all_users()):
        try:
            await bot.copy_message(chat_id=uid, from_chat_id=ADMIN_ID, message_id=msg_id, reply_markup=keyb)
        except:
            continue
    await bot.send_message(ADMIN_ID, "Рассылка завершена", reply_markup=mmenu)
