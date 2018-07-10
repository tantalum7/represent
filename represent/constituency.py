
import represent


class Constituency:

    def __init__(self, database: MySqlDatabase, name: str):
        self._db = database
        self._name = name
        self._elected_rep = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def elected_representative(self) -> represent.representative.Representative:
        """ Returns the current elected representative for this constituency """
        if not self._elected_rep:
            self._elected_rep = self._get_elected_rep()
        return self._elected_rep

    def _get_elected_rep(self) -> Representative:
        person_id = None
        with self._db.cursor() as cursor:
            cursor.execute('SELECT person FROM represent.pw_mp WHERE constituency = "%s" AND left_house = "9999-12-31"', (self.name,))
            row = cursor.fetchone()
            if not row:
                raise CannotFindRepresentativeException("Cannot find elected rep for constituency {}".format(self.name))
            person_id = row.get("person")

        return Representative(self._db, person_id)

