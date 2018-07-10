# Library imports
import mysql.connector

# Project imports


class MySqlDatabase:
    MAX_KEY_LENGTH = 32
    CONNECTION_SETTINGS_KEYS = {"user", "password", "host", "port", "database"}
    MANDATORY_SETTINGS_KEYS = {"user", "password", "host", "port", "database"}

    class _Connection:

        def __init__(self, settings: dict):
            self._conn = mysql.connector.connect(**settings)

        def __enter__(self):
            self._cursor = self._conn.cursor(buffered=True)
            return self._cursor

        def __exit__(self, *args, **kwargs):
            self._conn.commit()
            self._cursor.close()
            self._conn.close()

    def __init__(self, user, password, host, port, database):
        self.settings = {"user": user, "password": password, "host": host, "port": port, "database": database}

    def cursor(self):
        return self._Connection(self.settings)

if __name__ == "__main__":
    test_sqlite3_backend()
    print("done")
