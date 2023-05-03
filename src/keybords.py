from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_client = InlineKeyboardMarkup(row_width=3)
kb_client.add(
    InlineKeyboardButton("Stop", callback_data="stop"),
    InlineKeyboardButton("Help", callback_data="help")
)