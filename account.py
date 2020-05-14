import pickle
import os

class Account:

    current_account = None
    account_to_delete = None

    def __init__(self, name):
        self.name = name
        self.pens = []
        self.money = 0
        self.stats = {}

    @staticmethod
    def save_to_file(acc):
        dir_path = os.path.join(os.environ["APPDATA"], "Python PenFight")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_path = os.path.join(dir_path, f"{acc.name}.dat")
        file_object = open(file_path, 'wb')

        pickle.dump(acc, file_object)
        file_object.close()

    @staticmethod
    def get_account_names():
        dir_path = os.path.join(os.environ["APPDATA"], "Python PenFight")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        names = ['.'.join(x.split('.')[:-1]) for x in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, x))]
        return names

    @staticmethod
    def load_from_file(name):
        dir_path = os.path.join(os.environ["APPDATA"], "Python PenFight")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_path = os.path.join(dir_path, f"{name}.dat")
        file_object = open(file_path, 'rb')

        acc = pickle.load(file_object)
        file_object.close()

        return acc

    @staticmethod
    def delete_account(acc):
        dir_path = os.path.join(os.environ["APPDATA"], "Python PenFight")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_path = os.path.join(dir_path, f"{acc.name}.dat")

        if os.path.exists(file_path):
            os.remove(file_path)