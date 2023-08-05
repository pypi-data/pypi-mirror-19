"""delete a flashcard set"""

from .base import Base
import sqlite3
import os

class Delete_set(Base):

    def run(self):
        name = str(self.options.get('<setname>'))
        yn = input("Are you sure you want to delete flashcard set '"
                 + name + "'?\n(y/n)\n> ")
        if yn == 'y':
            path = os.path.dirname(os.path.realpath(__file__))
            conn = sqlite3.connect(path + '/../simplefc.db')
            cur = conn.cursor()
            cur.execute('drop table ' + name + ';')
            conn.commit()
            conn.close()
            print("deleted set '" + name + "'")

        elif yn == 'n':
            print("took no action")

        else:
            print("required input either 'y' or 'n'.")
