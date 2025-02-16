import json
import os
import sys

def resource_path(relative_path):
    """Получить путь к ресурсу, работает как в упакованном, так и в обычном режиме"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class JsonMigration():

    def __init__(self, info=None):
        self.info = info
        self.json_dump()

    def __get__(self, instance, owner):
        """
        Magic function for getting attribute
        :param instance:
        :param owner:
        :return: attribute of the class
        """
        print(f"[INFO] You get {instance}")

    def json_dump(self):
        """
        Dump info about the user to a JSON file
        :return: None
        """
        try:
            file_path = resource_path("bd/rasp.json")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Создать папки, если их нет
            with open(file_path, "w") as file:
                print("rasp.json opened")
                json.dump(self.info, file)
                print('[INFO] - DUMP is ready!')
        except Exception as err:
            print(f"[ERROR] {err}")

    def json_load(self):
        """
        Load info from a JSON file
        :return: None
        """
        try:
            file_path = resource_path("rasp.json")
            with open(file_path, "r") as file:
                self.info = json.load(file)
        except Exception as err:
            print(f"[ERROR] {err}")
