# Class to store settings data
class Settings:

    # Key for volume setting
    VOLUME = "volume"

    def __init__(self):
        self.data = {
            Settings.VOLUME: 100
        }

    # Add or update a setting
    def add(self, key, value):
        self.data[key] = value

    # Retrieve a setting
    def get(self, key):
        return self.data[key]