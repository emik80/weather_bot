import requests

from config import logger, base_config


class OpenWeatherAPI:
    BASE_URL = base_config.OPENWEATHER_API_URL
    api_key = base_config.OPENWEATHER_API_KEY

    def __init__(self, weather_type: str, location_type: str, location_data: dict):
        if not all([weather_type, location_type, location_data]):
            logger.error(f'None parameter: weather_type: {weather_type}, location_type: {location_type}, location_data:{location_data}')
            raise ValueError()

        self.weather_type = weather_type  # 'current_weather' или 'forecast'
        self.location_type = location_type  # 'current' или 'target'
        self.location_data = location_data  # {'lat': xx, 'lon': xx} или {'city': 'Kyiv'}

    def get_weather(self):
        if self.weather_type == 'current_weather':
            return self._get_current_weather()
        elif self.weather_type == 'forecast':
            return self._get_forecast()
        else:
            logger.error('Invalid weather type. Use "current_weather" or "forecast".')
            raise ValueError()

    def _get_current_weather(self):
        endpoint = f'{self.BASE_URL}weather'
        params = self._build_params()
        return self._make_request(endpoint, params)

    def _get_forecast(self):
        endpoint = f'{self.BASE_URL}forecast'
        params = self._build_params()
        return self._make_request(endpoint, params)

    def _build_params(self):
        params = {
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ua, uk'
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

    def _make_request(self, url, params):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            logger.success(response.text)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.exception(f'Error making request: {e}')
            return None
