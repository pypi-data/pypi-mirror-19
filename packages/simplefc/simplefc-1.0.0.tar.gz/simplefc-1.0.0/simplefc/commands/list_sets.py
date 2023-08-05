"""List all flashcard sets."""

from .base import Base
import sqlite3
import os

class List_sets(Base):

    def run(self):
        path = os.path.dirname(os.path.realpath(__file__))
        conn = sqlite3.connect(path + '/../simplefc.db')
        cur = conn.cursor()
        sets = cur.execute("select name from sqlite_master where "
                           "type = 'table' and name is not "
                           "'sqlite_sequence';")

        for i in sets:
            print(i[0])

        conn.commit()
        conn.close()
