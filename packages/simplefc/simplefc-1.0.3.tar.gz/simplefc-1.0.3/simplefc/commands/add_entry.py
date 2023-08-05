"""Add entries to flashcard sets, either manually or by
reading a file."""

from .base import Base
import sqlite3
import os
import sys

class Add_entry(Base):

    def run(self):
        path = os.path.dirname(os.path.realpath(__file__))
        conn = sqlite3.connect(path + '/../simplefc.db')
        cur = conn.cursor()
        name = str(self.options.get('<setname>'))

        if self.options.get('-M'):
            entries = self.options.get('<entry>')
            for i in entries:
                if ';;' not in i:
                    conn.commit(); conn.close()
                    sys.exit("All entries must be of the form "
                             "'term;;definition'. Separate each "
                             "entry with a space.")
            for i in entries:
                term, definition = i.split(';;')
                cur.execute("insert into " +name+ " (term, "
                            "definition) values (?,?);", 
                            (term, definition,))

        elif self.options.get('-F'):
            fcfile = open(self.options.get('<file>')[0])
            entries = fcfile.read().split('\n')[:-1]
            for i in entries:
                if ';;' not in i:
                    conn.commit(); conn.close()
                    sys.exit("All entries must be of the form "
                             "'term;;definition'. Separate each "
                             "entry with a newline (\n).")
            for i in entries:
                term, definition = i.split(';;')
                cur.execute("insert into " +name+ " (term, "
                            "definition) values ('" +term+ "','"
                            +definition+ "');")
            
        else:
            conn.commit(); conn.close()
            sys.exit("You must use either the '-i' or '-f' tag, "
                     "followed by one or more individual entries "
                     "or the path to a text file, respectively.")

        num = str(len(entries))
        if num == '1':
            print('Added 1 entry.')
        else:
            print('Added ' +num+ ' entries.')

        conn.commit()
        conn.close()
