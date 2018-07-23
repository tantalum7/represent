
from configparser import ConfigParser
from represent.database import MySqlDatabase
from represent.representative import Representative
from represent.division import Division
from represent.exceptions import *


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

    def search_representative(self, first_name, last_name):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT person from pw_mp WHERE (first_name LIKE %s AND last_name LIKE %s)", (first_name+"%", last_name+"%"))
            if cursor.rowcount < 1:
                raise CannotFindRepresentativeException()

            person_ids = set([p[0] for p in cursor])
            return [Representative(self.db, person_id) for person_id in person_ids]

    def get_division(self, division_id=None, division_number=None):
        if division_id:
            return Division(self.db, division_id)
        elif division_number:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT division_id from pw_division WHERE (division_number=%s)", (division_number,))
                if cursor.rowcount < 1:
                    raise CannotFindDivisionException()
                return Division(self.db, cursor.fetchone()[0])


    def search_divisions(self, search_term):
        division_list = []
        with self.db.cursor() as cursor:
            cursor.execute("SELECT division_id FROM pw_division WHERE (division_name LIKE %s)", ("%"+search_term+"%",))

            for row, in cursor:
                division_list.append(Division(self.db, row))

        return division_list
