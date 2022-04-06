# Third-party imports
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


class DBEngine:
    _DB_ENGINE = None

    def __init__(self):
        # TODO: Make user with less privileges and password protected.
        self._DB_ENGINE = create_engine('postgresql+psycopg2://postgres@localhost/blue_prism')
        self.create_database()

    def get_engine(self):
        if self._DB_ENGINE:
            return self._DB_ENGINE
        else:
            self.__init__()

    def create_database(self):
        if not database_exists(self._DB_ENGINE.url):
            create_database(self._DB_ENGINE.url)
