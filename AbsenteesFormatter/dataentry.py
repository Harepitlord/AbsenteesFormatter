import sqlite3
from functools import reduce
from operator import add


class ManualEntry:
    name = []
    batch = [[[]]]
    NoBatch = 0
    NoHour = 0

    def Entry(self):

        # Getting the student names from the user
        print("Data Entry Initiated....  Enter a number to stop ", flush=True)
        while True:
            d = input('Enter name: ')
            if d.isdigit():
                break
            self.name.append(d)

        # Getting Total number of day orders and batches, later class of the respective time slots
        torder = int(input('Enter the total no. of day orders: '))
        self.NoBatch = int(input('Enter total number of batches: '))
        self.NoHour = int(input('Enter no. of class per day: '))
        obatch = []
        for i in range(torder):
            bbatch = []
            for j in range(self.NoBatch):
                print('Enter TimeTable of Batch' + str(j + 1) + ' day order ' + str(i + 1) + ' : ')
                cbatch = []
                for K in range(self.NoHour):
                    d = input('Enter class: ')
                    cbatch.append(d)
                bbatch.append(cbatch)
            obatch.append(bbatch)
        self.batch = obatch
        self.intodb()
        return

    def intodb(self):
        con = sqlite3.connect('AbsenteesFormatter\datadb.sqlite')
        cur = con.cursor()
        # Inserting names into the database
        sql = '''CREATE TABLE IF NOT EXISTS STUDENTS(ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME VARCHAR(128) NOT NULL)'''
        cur.execute(sql)
        for n in self.name:
            sql = '''INSERT INTO STUDENTS(NAME) VALUES(?)'''
            cur.execute(sql, (n,))
        con.commit()

        # Inserting class with respect to time slot into the database

        # sql = '''CREATE TABLE IF NOT EXISTS TIMETABLE(ORDERID INTEGER PRIMARY KEY AUTOINCREMENT,B1T1 VARCHAR(10) NOT
        # NULL, B1T2 VARCHAR(10) NOT NULL, B1T3 VARCHAR(10) NOT NULL, B1T4 VARCHAR(10) NOT NULL,B2T1 VARCHAR(10) NOT
        # NULL, B2T2 VARCHAR(10) NOT NULL, B2T3 VARCHAR(10) NOT NULL, B2T4 VARCHAR(10) NOT NULL) '''
        sql = "CREATE TABLE IF NOT EXISTS TIMETABLE(ORDERID INTEGER PRIMARY KEY AUTOINCREMENT,"
        sq = ""
        for b in range(1, self.NoBatch + 1):
            for h in range(1, self.NoHour+1):
                if b == self.NoBatch and h == self.NoHour:
                    break
                sq += "B{0}T{1} VARCHAR(10) NOT NULL,".format(b, h)
        sq += "B{0}T{1} VARCHAR(10) NOT NULL)".format(self.NoBatch, self.NoHour)
        sql += sq

        cur.execute(sql)
        con.commit()

        # for b in self.batch:
        #     sql = '''INSERT INTO TIMETABLE(B1T1,B1T2,B1T3,B1T4,B2T1,B2T2,B2T3,B2T4) VALUES (?,?,?,?,?,?,?,?)'''
        #     cur.execute(sql, (b[0][0], b[0][1], b[0][2], b[0][3], b[1][0], b[1][1], b[1][2], b[1][3],))
        sql = "INSERT INTO TIMETABLE("
        sq = ""
        q = ""
        for b in range(1, self.NoBatch + 1):
            for h in range(1, self.NoHour+1):
                if b == self.NoBatch and h == self.NoHour:
                    break
                sq += "B{0}T{1},".format(b, h)
                q += "?,"
        sq += "B{0}T{1})".format(self.NoBatch, self.NoHour)
        sq += " VALUES (" + q + "?)"
        sql += sq
        c = 0
        for b in self.batch:
            data = tuple(reduce(add, b))
            cur.execute(sql, data)
            c += 1
            if c == 1:
                con.commit()

        con.commit()
        cur.close()
        return
