
import calendar
import datetime
from represent.database import MySqlDatabase
from represent.exceptions import *
import represent.constituency
from represent.division import Division


class Service:

    def __init__(self, id:int, entered:int, exited:int=None):
        self.id = id
        self.entered = entered
        self.exited = exited
        # Magic number is calendar.timegm(datetime.date(9999, 12, 31).timetuple())
        self.exited = None if exited >= 253402214400 else exited

    def in_service(self, timestamp:int):
        if timestamp < self.entered:
            return False
        elif self.exited is None:
            return True
        else:
            return timestamp < self.exited



class Representative:

    def __init__(self, database: MySqlDatabase, person_id: int):

        self._database = database
        self._person_id = person_id
        self.load_mp_data()

    def load_mp_data(self):

        with self._database.cursor() as cursor:
            cursor.execute('SELECT * FROM pw_mp WHERE (Person="%s")', (self._person_id,))

            if cursor.rowcount < 1:
                raise CannotFindRepresentativeException("PersonID: {}".format(self._person_id))

            rows = cursor.fetchall()
            data = dict(zip(cursor.column_names, rows[0]))

            self._first_name = data.get("first_name")
            self._last_name = data.get("last_name")
            self._title = data.get("title")
            self._constituency = data.get("constituency")
            self._party = data.get("party")
            self._house = data.get("house")

            self._mp_history = []

            for row in rows:
                data = dict(zip(cursor.column_names, row))
                entered = calendar.timegm(data["entered_house"].timetuple())
                exit = calendar.timegm(data["left_house"].timetuple())
                mpid = data.get("mp_id")
                self._mp_history.append(Service(mpid, entered, exit))

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
    def constituency(self) -> represent.constituency.Constituency:
        return represent.constituency.Constituency(self._database, self._constituency)

    @property
    def party(self):
        return self._party

    @property
    def house(self):
        return self._house

    def in_service_on(self, date: datetime.date):
        timestamp = calendar.timegm(date.timetuple())
        return any(service.in_service(timestamp) for service in self._mp_history)

    def get_mpid(self, date: datetime.date):
        timestamp = calendar.timegm(date.timetuple())
        for service in self._mp_history:
            if service.in_service(timestamp):
                return service.id
        else:
            return None

    def voted_on(self, division: Division):
        mpid = self.get_mpid(division.date)
        if mpid is None:
            return None
        return division.get_vote(mpid)
