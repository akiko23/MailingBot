from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import dp, bot, ADMIN_ID, db
from states.states import Message


__all__ = ["set_new_message", "process_hellobtn", "set_hellobtn", "hello_msg_keyb", "join"]

hello_msg_keyb = None
@dp.message_handler(content_types=["text", "photo", "video", "gif"], state=Message.get_new_hello_message)
async def set_new_message(msg: types.Message, state):
    new_hello_msg_id = msg.message_id
    with open("hello_message.txt", "w") as f:
        f.write(str(new_hello_msg_id))
    
    await state.finish()
    await bot.send_message(ADMIN_ID, "Желаете добавить кнопку?", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data="hellobtn-yes"),
                InlineKeyboardButton(text="Нет", callback_data="hellobtn-no"), 
            ]
        ]
    ))

@dp.callback_query_handler(lambda call: call.data.startswith("hellobtn"))
async def process_hellobtn(call: types.CallbackQuery):
    ans = call.data.split("-")[1]
    if ans == "yes":
        await bot.send_message(call.from_user.id, "Введите текст кнопки и юрл через '@' (Пример: Ютуб@https://www.youtube.com/)")
        await Message.get_hellobtn.set()
    else:
        await bot.send_message(call.from_user.id, "Приветственное сообщение успешно изменено!")

@dp.message_handler(content_types=["text"], state=Message.get_hellobtn)
async def set_hellobtn(msg: types.Message, state):
    global hello_msg_keyb
    text, url = msg.text.split("@")
    
    hello_msg_keyb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    [InlineKeyboardButton(text=text, url=url)]
                ]
            ]
        )
    await bot.send_message(ADMIN_ID, "Клавиатура успешно назначена!")
    await state.finish()
        

@dp.chat_join_request_handler()
async def join(update: types.ChatJoinRequest):
    with open("hello_message.txt") as f:
        hello_msg_id = f.read()
    await bot.copy_message(chat_id=update.from_user.id, from_chat_id=ADMIN_ID, message_id=hello_msg_id, reply_markup=hello_msg_keyb)
    await update.approve()

    if not db.user_exists(update.from_user.id):
        db.add_user(update.from_user.id)
