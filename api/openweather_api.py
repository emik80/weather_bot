from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict

import requests

from config import logger, base_config


class OpenWeatherAPI:
    BASE_URL = base_config.OPENWEATHER_API_URL
    API_KEY = base_config.OPENWEATHER_API_KEY

    def __init__(self, weather_type: str, location_type: str, location_data: dict):
        if not all([weather_type, location_type, location_data]):
            logger.error(f'None parameter: weather_type: {weather_type}, location_type: {location_type},'
                         f' location_data:{location_data}')
            raise ValueError()

        self.weather_type = weather_type
        self.location_type = location_type
        self.location_data = location_data

    def get_weather(self):
        if self.weather_type == 'current_weather':
            return self._get_current_weather()
        elif self.weather_type == 'forecast':
            return self._get_forecast()
        else:
            logger.error('Invalid weather type. Use "current_weather" or "forecast".')
            raise ValueError()

    def _build_params(self) -> Dict[str, str]:
        params = {
            'appid': self.API_KEY,
            'units': 'metric',
            'lang': 'ua'
        }

        if self.location_type == 'current':
            params.update({
                'lat': self.location_data.get('lat'),
                'lon': self.location_data.get('lon')
            })
        elif self.location_type == 'target':
            city = self.location_data
            if city:
                params['q'] = city
            else:
                logger.error('For "target" location_type, "city" key must be provided in location_data.')
                raise ValueError()
        else:
            logger.error('Invalid location_type. Use "current" or "target".')
            raise ValueError()

        return params

    def _get_current_weather(self):
        endpoint = f'{self.BASE_URL}weather'
        params = self._build_params()
        return self._make_request(endpoint, params)

    def _get_forecast(self):
        endpoint = f'{self.BASE_URL}forecast'
        params = self._build_params()
        return self._make_request(endpoint, params)

    def _make_request(self, url, params):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            logger.success(response.text)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.exception(f'Error making request: {e}')
            return None

    @staticmethod
    def parse_weather_data(weather_data):
        main_data = weather_data.get('main')
        wind_data = weather_data.get('wind')
        clouds_data = weather_data.get('clouds')
        weather_description = weather_data.get('weather')[0].get('description')

        weather_message = (f'🌍 <b>Поточна погода:</b> {weather_description}\n\n'
                           f'🌡️ <b>Температура:</b> {int(round(main_data.get('temp'), 0))}°C\n'
                           f'🌬️ <b>Відчувається як:</b> {int(round(main_data.get('feels_like'), 0))}°C\n\n'
                           f'💨 <b>Швидкість вітру:</b> {int(round(wind_data.get('speed'), 0))} м/с\n'
                           f'☁️ <b>Вологість повітря:</b> {main_data.get('humidity')}%\n'
                           f'☁️ <b>Хмарність:</b> {clouds_data.get('all')}%\n'
                           f'🌫️ <b>Атмосферний тиск:</b> {main_data.get('pressure')} гПа\n')
        return weather_message

    @staticmethod
    def parse_forecast_data(forecast_data):
        daily_forecast = defaultdict(
            lambda: {'min_temp': float('inf'), 'max_temp': float('-inf'), 'description': '', 'icon': ''})

        for entry in forecast_data.get('list'):
            if entry:
                date = datetime.fromtimestamp(entry.get('dt'), timezone.utc).strftime('%d-%m-%Y')
                temp_min = entry.get('main').get('temp_min')
                temp_max = entry.get('main').get('temp_max')
                description = entry.get('weather')[0].get('description')

                daily_forecast[date]['min_temp'] = min(daily_forecast[date]['min_temp'], temp_min)
                daily_forecast[date]['max_temp'] = max(daily_forecast[date]['max_temp'], temp_max)
                daily_forecast[date]['description'] = description

        forecast_message = '<b>Прогноз погоди на 5 днів:</b>\n\n'
        for date, data in daily_forecast.items():
            forecast_message += (f'📅 <b>{date}</b>: {data.get('description')}\n'
                                 f'🌡️ <b>Температура:</b> {int(round(data['min_temp'], 0))}...{int(round(data['max_temp'], 0))}°C\n\n')
        return forecast_message
