from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command, StateFilter

from api import OpenWeatherAPI
from bot.keyboards import start_kb, forecast_type_kb, share_geo_kb
from bot.text import BOT_MESSAGES
from bot.states import FSMCommon
from config import logger

router = Router()
router.message.filter(F.chat.type.in_({"private"}))
router.callback_query.filter(F.message.chat.type.in_({"private"}))


# Help
@router.message(Command(commands='help'))
async def process_command_help(message: Message):
    await message.answer(text=BOT_MESSAGES.get('help'))


# Start
@router.message(CommandStart())
async def process_command_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FSMCommon.get_location_type)
    await state.update_data(user_id=message.from_user.id,
                            location_type=None,
                            location_data=None,
                            weather_type=None)
    await message.answer(text=BOT_MESSAGES.get('start'),
                         reply_markup=start_kb)


# Cancel
@router.message(F.text.in_({'/cancel', '🔴 Скасувати'}))
@router.callback_query(F.data == 'cancel')
async def process_command_cancel(callback: Union[Message, CallbackQuery], state: FSMContext):
    await state.clear()
    await state.set_state(FSMCommon.get_location_type)
    await state.update_data(user_id=callback.from_user.id,
                            location_type=None,
                            location_data=None,
                            weather_type=None)
    text = BOT_MESSAGES.get('stop')
    if isinstance(callback, Message):  # Message
        message = callback
        await message.answer(text=text,
                             reply_markup=start_kb)
    else:  # CallbackQuery
        await callback.message.edit_text(text=text, reply_markup=start_kb)
        await callback.answer()


# Get location type
@router.callback_query(StateFilter(FSMCommon.get_location_type))
async def get_location(callback: CallbackQuery, state: FSMContext):
    location_type = callback.data
    await state.update_data(location_type=location_type)
    match location_type:
        case 'current':
            await state.set_state(FSMCommon.get_location_geo)
            await callback.message.answer(text='Відправка локації:',
                                          reply_markup=share_geo_kb)
            await callback.answer()

        case 'target':
            await state.set_state(FSMCommon.get_location_data)
            await callback.message.answer(text=BOT_MESSAGES.get('location'),
                                          reply_markup=None)
            await callback.answer()


# Enter location text
@router.message(StateFilter(FSMCommon.get_location_data))
async def process_url(message: Message, state: FSMContext):
    location_data = message.text
    await state.update_data(location_data=location_data)
    await state.set_state(FSMCommon.get_weather_type)
    await message.answer(text=BOT_MESSAGES.get('weather_type'),
                         reply_markup=forecast_type_kb)


# Share location geo
@router.message(StateFilter(FSMCommon.get_location_geo))
async def process_url(message: Message, state: FSMContext):
    location_data = {
        'lat': message.location.latitude,
        'lon': message.location.longitude
    }
    await state.update_data(location_data=location_data)
    await state.set_state(FSMCommon.get_weather_type)
    await message.answer(text=BOT_MESSAGES.get('location_complete'),
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text=BOT_MESSAGES.get('weather_type'),
                         reply_markup=forecast_type_kb)


# Enter weather type
@router.callback_query(StateFilter(FSMCommon.get_weather_type))
async def get_weather_type(callback: CallbackQuery, state: FSMContext):
    weather_type = callback.data
    await state.update_data(weather_type=weather_type)
    await state.set_state(FSMCommon.processing)
    await callback.answer()
    await callback.message.answer(text=BOT_MESSAGES.get('wait'))

    user_data = await state.get_data()
    weather_type = user_data.get('weather_type')
    location_type = user_data.get('location_type')
    location_data = user_data.get('location_data')

    try:
        weather_api = OpenWeatherAPI(
            weather_type=weather_type,
            location_type=location_type,
            location_data=location_data
        )
        weather_data = weather_api.get_weather()

        if weather_data:
            message_text = f'{BOT_MESSAGES.get(weather_type)}\n\n{weather_data}'
            await callback.message.answer(text=message_text,
                                          reply_markup=start_kb)
        else:
            await callback.message.answer(text=BOT_MESSAGES.get('warning'),
                                          reply_markup=start_kb)
            logger.error(f'[ERROR]: {location_type}: {location_data} - {weather_type}')

    except Exception as e:
        logger.exception(e)

    await state.clear()
    await state.set_state(FSMCommon.get_location_type)
    await state.update_data(user_id=callback.message.from_user.id,
                            location_type=None,
                            location_data=None,
                            weather_type=None)


# Other messages
@router.message(~StateFilter(FSMCommon.get_location_data))
async def send_error(message: Message):
    try:
        await message.answer(text=BOT_MESSAGES.get('unknown'))
        await message.delete()
    except TypeError as ex:
        await message.reply(text=BOT_MESSAGES.get('error'))
        logger.warning(ex)


@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    try:
        await message.reply(text='echo' + BOT_MESSAGES.get('error'))
    except TypeError as ex:
        await message.reply(text='echo' + BOT_MESSAGES.get('error'))
        logger.warning(ex)
