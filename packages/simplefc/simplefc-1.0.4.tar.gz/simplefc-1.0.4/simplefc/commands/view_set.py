"""View the contents of a flashcard set."""

from .base import Base
import sqlite3
import os

class View_set(Base):

    def run(self):
        path = os.path.dirname(os.path.realpath(__file__))
        conn = sqlite3.connect(path + '/../simplefc.db')
        cur = conn.cursor()
        name = str(self.options.get('<setname>'))
        cards = cur.execute("select ID, term, correct, "
                            "incorrect, archived from " +name)

        print('(ID, term, correct, incorrect, archived)')
        for i in cards:
            print(i)

        conn.commit()
        conn.close()
