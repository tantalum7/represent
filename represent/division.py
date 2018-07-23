
from datetime import datetime
from represent.database import MySqlDatabase
from represent.exceptions import *


class Division:

    def __init__(self, database: MySqlDatabase, division_id: int):

        self._db = database
        self._division_id = division_id
        self._load_data()
        self._votes = {}

    @property
    def division_id(self) -> int:
        return self._division_id

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def motion(self) -> str:
        return self._motion

    @property
    def votes(self):
        if self._votes == {}:
            self._load_votes()
        return self._votes.copy()

    @property
    def is_successful(self):
        if self._votes == {}:
            self._load_votes()
        return (self._votes["aye"] + self._votes["tellaye"]) > (self._votes["no"] + self._votes["tellno"])

    def get_vote(self, mp_id: str):
        with self._db.cursor() as cursor:
            cursor.execute("SELECT * FROM pm_vote WHERE (division_id='%s' AND mp_id='%s", (self._division_id, mp_id))

            if cursor.rowcount == -1:
                return None
            else:
                vote = cursor.fetchone().get("vote")
                vote = vote[0] if isinstance(vote, tuple) else vote
                return vote

    def _load_data(self):
        with self._db.cursor() as cursor:
            cursor.execute("SELECT * FROM pw_division WHERE (division_id=%s)", (self._division_id,))
            row = cursor.fetchone()
            if not row:
                raise CannotFindDivisionException("Can't find division id {}".format(self._division_id))
            data = dict(zip(cursor.column_names, row))
            self._date = data.get("division_date")
            self._name = data.get("division_name")
            self._url = data.get("source_url")
            self._motion = data.get("motion")

    def _load_votes(self):
        with self._db.cursor() as cursor:
            cursor.execute("SELECT vote FROM pw_vote WHERE (division_id='%s')", (self._division_id,))
            if cursor.rowcount == -1:
                raise CannotFindVotesException("Can't find votes for division id {}".format(self._division_id))

            self._votes = {"aye": 0, 'no': 0, 'tellaye': 0, 'tellno': 0}

            for vote in cursor:
                vote = vote[0] if isinstance(vote, tuple) else vote
                if vote not in self._votes:
                    self._votes[vote] = 0
                self._votes[vote] += 1

