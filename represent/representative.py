
from represent.database import MySqlDatabase
from represent.exceptions import *
from represent import Constituency


class Representative:

    def __init__(self, database: MySqlDatabase, person_id: int):

        self._database = database
        self._person_id = person_id
        self.load_mp_data()

    def load_mp_data(self):

        with self._database.cursor() as cursor:
            cursor.execute('SELECT * FROM pw_mp WHERE (Person="%s")', (self._person_id,))
            row = cursor.fetchone()

            if not row:
                raise CannotFindRepresentativeException("PersonID: {}".format(self._person_id))

            data = dict(zip(cursor.column_names, row))

            self._first_name = data.get("first_name")
            self._last_name = data.get("last_name")
            self._title = data.get("title")
            self._constituency = data.get("constituency")
            self._party = data.get("party")
            self._house = data.get("house")

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def title(self) -> str:
        return self._title

    @property
    def full_name(self) -> str:
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def constituency(self) -> Constituency:
        return Constituency(self._database, self._constituency)

    @property
    def party(self):
        return self._party

    @property
    def house(self):
        return self._house
