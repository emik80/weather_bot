# Main Menu commands
MENU_COMMANDS = {
    '/start': '🟢 Start',
    '/help': 'ℹ Help',
    '/cancel': '🔴 Stop',
}

# Bot messages
BOT_MESSAGES = {
    'hello': 'Я твій перший бот Python!',
    'location': '🔽 Введіть місто',
    'location_complete': '✅ Локацію отримано',
    'weather_type': '🔽 Оберіть опцію:',
    'warning': '⚠️ Сталася помилка під час обробки запиту.',
    'current_weather': '🌍 Поточна погода:',
    'forecast': '📅 Прогноз погоди на 5 днів:',
    'help': f'ℹ️ Даний бот може визначити поточну погоду, а також надати прогноз на найближчі 5 днів.\n\n'
            f'Для отримання максимально точного прогнозу можна поділитися своєю геолокацією (працює зі смартфону).\n\n'
            f'Ви можете ввести назву населеного пункту будь-якою мовою або індекс (zip-code). '
            f'Через кому можна вказати код країни (наприклад, UA) для більш точного визначення місця.\n\n'
            f'Для початку роботи з ботом використовуйте команду /start',
    'stop': f'🔴 Скасовано.\n',
    'error': '⚠ Виникла помилка',
    'unknown': f'Невідома команда 🥲\n'
               f'Використовуйте команди /start або /help для роботи з ботом',
}
