from aiogram.dispatcher.filters.state import State, StatesGroup

class Message(StatesGroup):
    get_mailing_msg = State()
    get_new_hello_message = State()
    get_mailingbtn = State()
    get_hellobtn = State()
