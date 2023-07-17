from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import dp, bot, ADMIN_ID 
from states.states import Message
from functions import make_mailing


__all__ = ["get_mailing_message", "process_mailing_msg_btn", "set_hellobtn"]

@dp.message_handler(content_types=["text", "photo", "video", "gif"], state=Message.get_mailing_msg)
async def get_mailing_message(msg: types.Message, state):
    await bot.send_message(ADMIN_ID, "Сообщение назначено, желаете добавить кнопку?", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data="addbtn-yes"),
                InlineKeyboardButton(text="Нет", callback_data="addbtn-no"), 
            ]
        ]
    ))
    data = await state.get_data()
    data["msg_id"] = msg.message_id
    await state.set_data(data)

@dp.callback_query_handler(lambda call: call.data.startswith("addbtn"), state=Message.get_mailing_msg)
async def process_mailing_msg_btn(call: types.CallbackQuery, state):
    await bot.delete_message(ADMIN_ID, call.message.message_id)
    ans, data = call.data.split("-")[1], await state.get_data()
    if ans == "yes":
        await bot.send_message(call.from_user.id, "Введите текст кнопки и юрл через '@' (Пример: Ютуб@https://www.youtube.com/)")
        await Message.get_mailingbtn.set()
    else:
        await make_mailing(data=data)
        await state.finish()

@dp.message_handler(content_types=["text"], state=Message.get_mailingbtn)
async def set_hellobtn(msg: types.Message, state):
    text, url = msg.text.split("@")
    data = await state.get_data()

    mailing_keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, url=url)]
        ]
    )
    await bot.send_message(ADMIN_ID, "Кнопка назначена!")
    await make_mailing(data=data, keyb=mailing_keyb)
    await state.finish()
