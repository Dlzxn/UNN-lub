import aiohttp
import asyncio
import datetime as dt
import os
import sys
from datetime import datetime, timedelta


from bd.json_migration import JsonMigration


def resource_path(relative_path):
    """Получить путь к ресурсу, работает как в упакованном, так и в обычном режиме"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class UnnRequest:
    """
    Class UnnRequest
    using for get information from API UNN
    """
    def __init__(self, login):
        self.login: str = login
        print(f'login: {self.login}')

        try:
            self.get_week_dates()
            self.__new_format()
            self.main()
        except Exception as e:
            print(f"[ERROR] string 16 {e}")

    def init__next(self):
        self.login: str = self.login
        print(f'login: {self.login}')

        try:
            self.get_next_week_date(self.start_date)
            self.__new_format()
            self.main()
        except Exception as e:
            print(f"[ERROR] string 42 {e}")


    def init__previous(self):
        self.login: str = self.login
        print(f'login: {self.login}')

        try:
            self.get_previous_week_date(self.start_date)
            self.__new_format()
            self.main()
        except Exception as e:
            print(f"[ERROR] string 54 {e}")


    def __new_format(self):
        """
        def for generate dynamic URL
        :return: None
        """
        student_number: int = int(self.login[1:])
        self.format: str = f'https://portal.unn.ru/ruzapi/schedule/student/{student_number-24073692}?start={self.start_date}&finish={self.end_date}&lng=1'
        print(f'[INFO] {self.format}')


    @staticmethod
    def proverka_user(self) -> bool:
        """
        idenification user
        :return:
        """
        try:
            asyncio.run(self.main())
            return True
        except Exception as e:
            print(f"[ERROR] str 34 {e}")
            return False


    async def get_ruz(self):
        """
        def for get info from API UNN
        :return:
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.format) as response:
                    print(await response.text(), "fffff")
                    print("RESPONCE")
                    self.json_response = await response.json()
                    self.us = JsonMigration(self.json_response)
        except aiohttp.ClientError as e:
            print(f"[ERROR] Network issue: {e}")
        except Exception as e:
            print(f"[ERROR] JSON Parsing or other issue: {e}")

    def get_week_dates(self):
        """
        def for getting info about start/finish week dates
        :return: None
        """
        # Получаем текущую дату
        today = dt.date.today()

        start_of_week = today - dt.timedelta(days=today.weekday())  # Понедельник текущей недели
        end_of_week = start_of_week + dt.timedelta(days=6)  # Воскресенье текущей недели

        self.start_date = start_of_week.strftime("%Y.%m.%d")
        self.end_date = end_of_week.strftime("%Y.%m.%d")

    async def get_version(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://www.unnapi.ru/version") as response:
                    self.unnapi = await response.json()
                    print(self.unnapi)
                    self.version = self.unnapi['version']
                    print(f'[INFO] Version: {self.version}')
        except aiohttp.ClientError as e:
            print(f'[ERROR] Network issue: {e}')
        except Exception as e:
            print(f"[ERROR] other issue(str96): {e}")

    async def mainloop(self):
        """
        create async tasks
        :return:
        """
        task_one: asyncio.Task = asyncio.create_task(self.get_ruz())
        task_two: asyncio.Task = asyncio.create_task(self.get_version())
        await asyncio.gather(task_one, task_two)

    def main(self):
        """
        start asyncio
        :return:
        """
        asyncio.run(self.mainloop())

    def get_next_week_date(self, start_date):
        """
        Вычисляет начало и конец следующей недели от заданной даты и сохраняет в self.

        :param start_date: Дата в формате 'год.месяц.день' (например, '2025.01.15').
        """
        from datetime import datetime, timedelta

        # Преобразуем строку в объект даты
        date_obj = datetime.strptime(start_date, "%Y.%m.%d")

        # Добавляем 7 дней для начала следующей недели
        start_of_next_week = date_obj + timedelta(weeks=1)

        # Считаем конец следующей недели
        end_of_next_week = start_of_next_week + timedelta(days=6)

        # Сохраняем в self
        self.start_date = start_of_next_week.strftime("%Y.%m.%d")
        self.end_date = end_of_next_week.strftime("%Y.%m.%d")

    def get_previous_week_date(self, start_date):
        """
        Вычисляет начало и конец прошлой недели от заданной даты и сохраняет в self.

        :param start_date: Дата в формате 'год.месяц.день' (например, '2025.01.15').
        """
        from datetime import datetime, timedelta

        # Преобразуем строку в объект даты
        date_obj = datetime.strptime(start_date, "%Y.%m.%d")

        # Вычитаем 7 дней для начала предыдущей недели
        start_of_previous_week = date_obj - timedelta(weeks=1)

        # Считаем конец предыдущей недели
        end_of_previous_week = start_of_previous_week + timedelta(days=6)

        # Сохраняем в self
        self.start_date = start_of_previous_week.strftime("%Y.%m.%d")
        self.end_date = end_of_previous_week.strftime("%Y.%m.%d")



