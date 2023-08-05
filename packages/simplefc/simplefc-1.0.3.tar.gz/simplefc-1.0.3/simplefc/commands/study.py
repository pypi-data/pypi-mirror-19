"""Present entries individually, either by term (-t), 
definition (-d), or both (-b). Include all (-a), many (exclude 
easy ones; -m), or few (only the hard ones; -f)."""

from .base import Base
import sqlite3
import os
import sys
import random
from numpy import repeat

class _Getch:
    """Gets a single character from standard input. Does not 
echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

class Study(Base):

    def flash(self):
        print("\n ~" +str(self.counter)+ "~ Press [space] for"
              " answer.")
        ch1 = _Getch()
        ch = ch1()
        if ch == ' ':
            answer = self.cur.execute("select " +self.td[1]+
            " from " +self.name+ " where ID is " +str(self.i)+ ";")
            [print('\n' + j[0]) for j in answer]
            print("\n ~*~ 'c' = correct, "
                  "'i' = incorrect, 'e' = exit, 'a' = archive")
            ch2 = _Getch()
            ch = ch2()
            if ch == 'c':
                self.cur.execute("update " +self.name+ " set correct"
                "=correct+1 where ID is " +str(self.i)+ ";")
            elif ch == 'i':
                self.cur.execute("update " +self.name+ " set "
                "incorrect=incorrect+1 where ID is " +str(self.i)+ 
                ";")
            elif ch == 'a':
                print('\n-------------------------------------')
                print('\n ~*~ Entry staged for archive:')
                print('\n(ID, term, definition, correct, '
                      'incorrect, archived)')
                ent = self.cur.execute("select ID, term, definition"
                    ", correct, incorrect, archived from "
                    +self.name+ " where ID is " +str(self.i)+ ";")
                [print(j) for j in ent]
                arch = input('\n ~*~ This entry will be removed '
                             'from play until\n     you unarchive it'
                             '. Confirm archive? (y/n)\n > ')
                if arch == 'y':
                    self.cur.execute("update " +self.name+ " set "
                    "archived='Y' where ID is " +str(self.i)+ ";")
                    print(' ~*~ Entry archived. Press any key'
                          ' to continue.')
                    ch1 = _Getch()
                    ch = ch1()
                    try:
                        ch
                    except NameError:
                        pass
                elif arch == 'n':
                    print(' ~*~ Archiving aborted. Press any key'
                          ' to continue.')
                    ch1 = _Getch()
                    ch = ch1()
                    try:
                        ch
                    except NameError:
                        pass
                else:
                    print('\n ~*~ Invalid.')
                    self.flash()
            elif ch == 'e':
                self.conn.commit(); self.conn.close()
                sys.exit('Changes saved.')
            else:
                print('\n ~*~ invalid')
                self.flash()
        else:
            print('\n ~*~ invalid')
            self.flash()

    def mode_parser(self):
        if self.options.get('-r'):
            random.shuffle(self.pool)

        if self.options.get('-b'):
            for i in range(len(self.pool)):
                self.td = ['term','definition']
                random.shuffle(self.td)
                term = self.cur.execute("select " +self.td[0]+
                " from " +self.name+ " where ID is " 
                +str(self.pool[i])+ " and archived='N';")
                [print('\n' + j[0]) for j in term]
                self.i = i
                self.counter = len(self.pool) - self.i
                self.flash()
        else:
            for i in self.pool:
                term = self.cur.execute("select " +self.td[0]+
                " from " +self.name+ " where ID is " +str(i)+
                " and archived='N';")
                [print('\n' + j[0]) for j in term]
                self.i = i
                self.counter = len(self.pool) - self.i + 1
                self.flash()
    
    def combined_sets(self):
        self.tables = self.cur.execute("""select name from 
                     sqlite_master where type = 'table' and name 
                     is not 'sqlite_sequence';""")
        self.tables =[j[0] for j in self.tables]
        self.comb_pool = list(range(len(self.tables)))
        if self.which == 'many':
            for i in range(len(self.tables)):
                id_list = self.cur.execute("select ID from"
                            " " +self.tables[i]+ " where archived="
                            "'N' and correct/incorrect <= 2;")
                self.comb_pool[i] = [j[0] for j in id_list]
        elif self.which == 'few':
            for i in range(len(self.tables)):
                id_list = self.cur.execute("select ID from"
                            " " +self.tables[i]+ " where archived="
                            "'N' and correct/incorrect <= 0.75;")
                self.comb_pool[i] = [j[0] for j in id_list]
        else:
            for i in range(len(self.tables)):
                id_list = self.cur.execute("select ID from"
                            " " +self.tables[i]+ " where archived="
                            "'N';")
                self.comb_pool[i] = [j[0] for j in id_list]
        for tab in range(len(self.comb_pool)):
            random.shuffle(self.comb_pool[tab])
            self.comb_pool[tab].append(self.tables[tab])
        random.shuffle(self.comb_pool)
        tab_ind = list(range(len(self.comb_pool)))
        for tab in tab_ind:
            tab_ind[tab] = list(repeat(tab, 
                                len(self.comb_pool[tab])-1))
        self.flat = [i for sublist in tab_ind for i in sublist]
        random.shuffle(self.flat)
        self.flat_count = 0
        self.entry_count = repeat(0, len(self.comb_pool))
        self.comb_tdb()

    def comb_tdb(self):
        if self.flat_count >= len(self.flat):
            self.conn.commit(); self.conn.close()
            sys.exit('\nEnd of all sets.')
        if self.options.get('-t'):
            self.td = ['term', 'definition']
        elif self.options.get('-d'):
            self.td = ['definition', 'term']
        else:
            self.td = ['term', 'definition']
            random.shuffle(self.td)
        fcset = self.flat[self.flat_count]
        entry = self.entry_count[fcset]
        self.i = self.comb_pool[fcset][entry]
        self.name = self.comb_pool[fcset][len(self.comb_pool[fcset])-1]
        term = self.cur.execute("select " +self.td[0]+ " from " 
               +self.name+ " where ID is " +str(self.i)+ ";")
        [print('\n' + j[0]) for j in term]
        self.flat_count += 1
        self.entry_count[fcset] += 1
        self.counter = len(self.flat) - self.flat_count + 1
        self.flash()
        self.comb_tdb()
 
    def allfc(self):
        self.pool = self.cur.execute("select ID from " 
                    +self.name+ " where archived='N';")
        self.termdef()

    def manyfc(self):
        self.pool = self.cur.execute("select ID from " 
                    +self.name+ " where archived='N' "
                    "and correct/incorrect <=2;")
        self.termdef()

    def fewfc(self):
        self.pool = self.cur.execute("select ID from " 
                    +self.name+ " where archived='N' and "
                    "correct/incorrect <=0.75;")
        self.termdef()

    def termdef(self):
        self.pool = [i[0] for i in self.pool]
        if self.options.get('-t'):
            self.td = ['term','definition']
        elif self.options.get('-d'):
            self.td = ['definition','term']
        else:
            pass
        self.mode_parser()
    
    def run(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.conn = sqlite3.connect(path + '/../simplefc.db')
        self.cur = self.conn.cursor()
        self.name = str(self.options.get('<setname>'))
        flags = ['-t','-d','-b','-a','-m','-f','-s','-r']
        TF = [self.options.get(i) for i in flags]
        used = [i[0] for i in list(zip(flags, TF)) if i[1]]
        key = ''.join(sorted(''.join(used).replace('-','')))
        
        if str(self.name) == '.':
            if key in ['at','ab','ad']:
                self.which = 'all'
                self.combined_sets()
            elif key in ['mt','bm','dm']:
                self.which = 'many'
                self.combined_sets()
            elif key in ['ft','bf','df']:
                self.which = 'few'
                self.combined_sets()
            elif key == '':
                self.which = 'all'
                self.td = ['term','definition']
                self.combined_sets()
            else:
                sys.exit("The -r flag is chosen by default when "
                         "<setname> is set to '*' (combined sets)."
                         " Specify one flag each from -tdb and -amf,"
                         " but exclude -rs. You may also omit all"
                         " flags to accept defaults (-atr).")
        else:
            if key in ['ast','art','abs','abr','ads','adr']:
                self.allfc()
            elif key in ['mst','mrt','bms','bmr','dms','dmr']:
                self.manyfc()
            elif key in ['fst','ftr','bfs','bfr','dfs','dfr']:
                self.fewfc()
            elif key == '':
                self.td = ['term','definition']
                self.allfc()
            else:
                self.conn.commit(); self.conn.close()
                sys.exit("Need one flag each from -tdb -amf and "
                         "-sr,\n or no flags for the default (-tas)."
                         "\n Enter 'simplefc -h' for details.")
        
        print('\nEnd of set.')
        self.conn.commit()
        self.conn.close()
