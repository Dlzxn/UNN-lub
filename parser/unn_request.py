import aiohttp, asyncio, time

class UnnRequest:
    def __init__(self, login, password):
        self.login: str = login
        self.psw: str = password
        self.__new_format()
        asyncio.run(self.get_ruz())

    def __new_format(self):
        student_number: int = int(self.login[1:])
        self.format: str = f'https://portal.unn.ru/ruzapi/schedule/student/{student_number-24073692}?start=2024.12.09&finish=2024.12.15&lng=1'

    async def get_ruz(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.format) as response:
                print(await response.json())
                self.json_response = await response.json()