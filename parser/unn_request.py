import aiohttp
import asyncio


async def login(session, url, username, password):
    login_data = {
        'AUTH_FORM': 'Y',
        'TYPE': 'AUTH',
        'backurl': '/ruz/main?_url=%2Fmain',
        'USER_LOGIN': username,
        'USER_PASSWORD': password,
        'USER_REMEMBER': 'Y'  # Опционально, если нужно запомнить пользователя
    }

    # Отправляем POST-запрос для входа
    async with session.post(url, data=login_data) as response:
        response.raise_for_status()  # Проверка на ошибки
        return response.url  # Возвращаем URL для подтверждения входа


async def access_protected_page(session, protected_url):
    async with session.get(protected_url) as response:
        response.raise_for_status()  # Проверка на ошибки
        return await response.text()  # Получаем содержимое страницы


async def main(login, password):
    # Создаем сессию
    async with aiohttp.ClientSession() as session:
        login_url = 'https://portal.unn.ru/'  # Замените на реальный URL авторизации
        protected_url = 'https://portal.unn.ru/ruz/main'  # Замените на реальный защищенный URL
        username = login  # Ваше имя пользователя
        password = password  # Ваш пароль

        try:
            await login(session, login_url, username, password)  # Сохраняем сессию
            page_content = await access_protected_page(session,
                                                       protected_url)  # Используем сессию для доступа к защищенной странице
            return page_content  # Выводим содержимое защищенной страницы
        except Exception as e:
            return f"Произошла ошибка: {e}"


