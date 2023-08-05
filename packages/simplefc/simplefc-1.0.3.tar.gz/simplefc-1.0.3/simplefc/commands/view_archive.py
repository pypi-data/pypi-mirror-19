"""View archived entries within a flashcard set."""

from .base import Base
import sqlite3
import os

class View_archive(Base):

    def run(self):
        path = os.path.dirname(os.path.realpath(__file__))
        conn = sqlite3.connect(path + '/../simplefc.db')
        cur = conn.cursor()
        name = str(self.options.get('<setname>'))
        cards = cur.execute("select ID, term, correct, "
                            "incorrect from " +name+ " where archived "
                            "is 'Y';")

        print('(ID, term, correct, incorrect)')
        for i in cards:
            print(i)

        conn.commit()
        conn.close()
