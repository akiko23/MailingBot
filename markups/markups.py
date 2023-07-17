from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Сделать рассылку", callback_data="mmenu_makemailing"),
                    InlineKeyboardButton(text="Поменять приветственное сообщение", callback_data="mmenu_changemsg"),
                ]
            ]
        )

