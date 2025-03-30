from aiogram import Bot
from aiogram.types import BotCommand, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.text import MENU_COMMANDS


async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
                                command=command,
                                description=description
                          ) for command, description in MENU_COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)


def create_inline_kb(width: int = 2, **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()


def reply_kb_builder(buttons, width=2):
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


start_kb = create_inline_kb(
        current='📍 Моя локація',
        target='💬 Ввести вручну',
    )

forecast_type_kb = create_inline_kb(
    current_weather='🌡️ Поточна погода',
    forecast='📅 На 5 днів',
)

# Buttons
share_button = KeyboardButton(text='📍 Поділитися локацією', request_location=True)
cancel_button = KeyboardButton(text='🔴 Скасувати')

share_geo_kb = reply_kb_builder(buttons=[share_button, cancel_button])
