from bs4 import BeautifulSoup
import json, datetime

class AnalyticHtml:
    def __init__(self):
        self.load()
        # self.__inizial_soup()
        self.analyse()
        self.get_week_dates()
        self.set_slovar()


    def load(self):
        with open('../bd/rasp.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
            print(self.data)

    def analyse(self):
        self.rasp = {}
        print(len(self.data))
        self.rasp = []
        for item in self.data:
            # print(item["date"])
            # if item["date"] not in self.rasp:
            #     sp = [item["dayOfWeekString"], item["auditorium"], item["building"], item["discipline"],
            #           item["kindOfWork"], item["lecturer"], item["beginLesson"], item["endLesson"]]
            #     self.rasp[item["date"]] = sp
            # else:
            #     sp += [item["dayOfWeekString"], item["auditorium"], item["building"], item["discipline"],
            #           item["kindOfWork"], item["lecturer"], item["beginLesson"], item["endLesson"]]
            #     self.rasp[item["date"]] += sp
            self.rasp.append([item["dayOfWeekString"], item["auditorium"], item["building"], item["discipline"],
                      item["kindOfWork"], item["lecturer"], item["beginLesson"], item["endLesson"]])
        print(self.rasp)

    def get_week_dates(self):
        # Получаем текущую дату
        today = datetime.date.today()

        start_of_week = today - datetime.timedelta(days=today.weekday())  # Понедельник текущей недели
        end_of_week = start_of_week + datetime.timedelta(days=6)  # Воскресенье текущей недели

        self.start_date = start_of_week.strftime("%Y.%m.%d")
        self.end_date = end_of_week.strftime("%Y.%m.%d")


    def set_slovar(self):
        self.slovar = {}

        for item in range(len(self.rasp)):
            if self.rasp[item][0] not in self.slovar:
                self.slovar[self.rasp[item][0]] = [{"День:": f"{self.rasp[item][0]}", "Название": f"{self.rasp[item][3]}",
                                                "Преподаватель": f"{self.rasp[item][5]}", "Аудитория": f'{self.rasp[item][1]} {self.rasp[item][2]}',
                                                "Время": f"{self.rasp[item][6]} - {self.rasp[item][7]}",
                                                }]

            else:
                self.slovar[self.rasp[item][0]] += [{"День:": f"{self.rasp[item][0]}", "Название": f"{self.rasp[item][3]}",
                                                "Преподаватель": f"{self.rasp[item][5]}", "Аудитория": f'{self.rasp[item][1]} {self.rasp[item][2]}',
                                                "Время": f"{self.rasp[item][6]} - {self.rasp[item][7]}",
                                                }]
        print(self.slovar)
        return self.slovar


