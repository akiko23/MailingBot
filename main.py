from aiogram import executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.states import Message
from config import bot, dp, db, ADMIN_ID
from markups.markups import main_menu as mmenu


from handlers.hello_msg import *
from handlers.mailing import *

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    user_id = msg.from_user.id
    if not db.user_exists(user_id):
        db.add_user(user_id)
    await bot.send_message(user_id, "Выберите действие", reply_markup=mmenu)

@dp.callback_query_handler(lambda call: call.data.startswith("mmenu"))
async def main_menu_handler(call: types.CallbackQuery):
    await bot.delete_message(ADMIN_ID, call.message.message_id)
    action = call.data.split("_")[1]
    
    if call.from_user.id == ADMIN_ID:
        if action == "makemailing":
            await bot.send_message(ADMIN_ID, "Отправьте сообщение, которое разошлется всем пользователям", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Отмена", callback_data="cancel_action")]
                ]
            ))
            await Message.get_mailing_msg.set()
        else:
            await bot.send_message(ADMIN_ID, "Отправьте новое сообщение", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Отмена", callback_data="cancel_action")]
                ]
            ))
            await Message.get_new_hello_message.set()

@dp.callback_query_handler(lambda call: call.data == "cancel_action", state=Message.all_states)
async def cancel_action(call, state):
    await bot.delete_message(ADMIN_ID, call.message.message_id)
    
    await bot.send_message(ADMIN_ID, "Вы отменили действие", reply_markup=mmenu)
    await state.finish()

def main():
    executor.start_polling(dp, allowed_updates=["update_id", "callback_query", "message", "channel_post", "chat_member", "chat_join_request"])

if __name__ == "__main__":
    main()
