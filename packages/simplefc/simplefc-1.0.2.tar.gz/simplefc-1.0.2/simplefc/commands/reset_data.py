"""Set all 'correct' and 'incorrect' records back to 0."""

from .base import Base
import sqlite3
import os

class Reset_data(Base):

    def run(self):
        path = os.path.dirname(os.path.realpath(__file__))
        conn = sqlite3.connect(path + '/../simplefc.db')
        cur = conn.cursor()
        name = str(self.options.get('<setname>'))
        cur.execute("update " +name+ " set correct=0, "
                    "incorrect=0;")
        
        print("Correct/incorrect count has been reset "
              "for flashcard set '" +name+ "'.")

        conn.commit()
        conn.close()
