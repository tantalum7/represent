
from configparser import ConfigParser
from represent.database import MySqlDatabase
from represent.representative import Representative
from represent.division import Division

class Represent:

    def __init__(self, config="settings.ini"):
        self.load_config(config)
        self.db = MySqlDatabase(**self.config["mysql_database"])

    def load_config(self, path):
        """ Loads config file, and stores config items in self.config (dict of sections) """
        # Intialise parser
        config = ConfigParser()

        # using function str instead on lower to make keys case-sensitive
        config.optionxform = str

        # Load config
        config.read(path)

        # Store config sections in class
        self.config = config._sections

    def get_representative(self, person_id):
        return Representative(self.db, person_id)

    def get_division(self, division_id):
        return Division(self.db, division_id)