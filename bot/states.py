from aiogram.fsm.state import StatesGroup, State


class FSMCommon(StatesGroup):
    get_location_type = State('get_location_type')
    get_location_data = State('get_location_data')
    get_location_geo = State('get_location_geo')
    get_weather_type = State('get_weather')
    processing = State('processing')
