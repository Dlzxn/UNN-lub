import json


class JsonMigration():

    def __init__(self, info = None):
        self.info = info


    def __get__(self, instance, owner):
        """
        Magic function For get attribute___LOG [INFO]
        :param instance:
        :param owner:
        :return: attribute Class
        """
        print(f"[INFO] You get {instance}")


    def json_dump(self):
        """
        Dump info about useer
        :return: None
        """
        try:
            with open("../rasp.json", "w") as file:
                json.dump(self.info, file)
                file.close()
                print('[INFO] - DUMP is ready!')

        except Exception as err:
            print(f"[ERROR] {err}")


    def json_load(self):
        try:
            with open("../rasp.json", "r") as file:
                self.info = json.load(file)