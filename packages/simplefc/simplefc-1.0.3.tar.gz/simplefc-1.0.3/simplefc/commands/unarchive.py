"""Remove entries from the archive."""

from .base import Base
import sqlite3
import os

class Unarchive(Base):

    def run(self):
        path = os.path.dirname(os.path.realpath(__file__))
        conn = sqlite3.connect(path + '/../simplefc.db')
        cur = conn.cursor()
        name = str(self.options.get('<setname>'))
        IDs = self.options.get('<ID>')
        
        print('\n(ID, term, correct, incorrect, archived)')
        for i in IDs:
            cards = cur.execute("select ID, term, correct, "
                                "incorrect, archived from " +name+
                                " where ID is " +i+ ";")
            [print(j) for j in cards]
 
        choice = input("\nReally unarchive?\n(y/n)\n>")
        
        if choice == 'y':
            for i in IDs:
                cur.execute("update " +name+ " set archived='N' "
                            "where ID=" +i+ ";")

            print('Entries unarchived.')

        elif choice == 'n':
            print('Aborted.')

        else:
            print("required input either 'y' or 'n'.")
            
        conn.commit()
        conn.close()
