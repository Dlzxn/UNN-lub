import aiohttp, asyncio, datetime

class UnnRequest:
    def __init__(self, login, password):
        self.login: str = login
        self.psw: str = password
        self.get_week_dates()
        self.__new_format()
        asyncio.run(self.get_ruz())

    def __new_format(self):
        student_number: int = int(self.login[1:])
        # self.format: str = f'https://portal.unn.ru/ruzapi/schedule/student/{student_number-24073692}?start={self.start_date}&finish={self.end_date}&lng=1'
        self.format: str = f'https://portal.unn.ru/ruzapi/schedule/student/{student_number - 24073692}?start=2024.12.09&finish=2024.12.15&lng=1'
        print(self.format)


    async def get_ruz(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.format) as response:
                print(await response.text(), "fffff")
                print("RESPONCE")
                self.json_response = await response.json()


    def get_week_dates(self):
        # Получаем текущую дату
        today = datetime.date.today()

        start_of_week = today - datetime.timedelta(days=today.weekday())  # Понедельник текущей недели
        end_of_week = start_of_week + datetime.timedelta(days=6)  # Воскресенье текущей недели

        self.start_date = start_of_week.strftime("%Y.%m.%d")
        self.end_date = end_of_week.strftime("%Y.%m.%d")



