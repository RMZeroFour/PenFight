import pickle
import os

# Used to save settings data
from settings import Settings


class Account:
    # Global variable to hold the currently loaded player
    current_account = None

    # Global variable to hold the player currently selected for deleting
    account_to_delete = None

    TOTAL_WINS = "total_wins"
    TOTAL_LOSSES = "total_losses"
    TOTAL_MONEY = "total_money"
    UNLOCKED_PENS = "unlocked_pens"

    # Create a new account with default settings
    def __init__(self, name):
        self.name = name
        self.pens = []
        self.money = 100
        self.stats = self.create_stats()
        self.settings = Settings()

    def purchase_pen(self, pen):
        self.pens.append(pen.name)
        self.money -= pen.cost
        self.stats[Account.UNLOCKED_PENS] = len(self.pens)

    @staticmethod
    def create_stats():
        return {
            Account.TOTAL_WINS: 0,
            Account.TOTAL_LOSSES: 0,
            Account.TOTAL_MONEY: 0,
            Account.UNLOCKED_PENS: 0
        }

    @staticmethod
    def save_to_file(acc):
        dir_path = os.path.join(os.environ["APPDATA"], "Python PenFight")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_path = os.path.join(dir_path, f"{acc.name}.dat")

        with open(file_path, 'wb') as file_object:
            pickle.dump(acc, file_object)

    @staticmethod
    def get_account_names():
        dir_path = os.path.join(os.environ["APPDATA"], "Python PenFight")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        names = ['.'.join(x.split('.')[:-1]) for x in os.listdir(dir_path)
                 if os.path.isfile(os.path.join(dir_path, x)) and x.endswith(".dat")]
        return names

    @staticmethod
    def load_from_file(name):
        dir_path = os.path.join(os.environ["APPDATA"], "Python PenFight")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_path = os.path.join(dir_path, f"{name}.dat")

        with open(file_path, 'rb') as file_object:
            acc = pickle.load(file_object)
            return acc

    @staticmethod
    def delete_account(acc):
        dir_path = os.path.join(os.environ["APPDATA"], "Python PenFight")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_path = os.path.join(dir_path, f"{acc.name}.dat")

        if os.path.exists(file_path):
            os.remove(file_path)
