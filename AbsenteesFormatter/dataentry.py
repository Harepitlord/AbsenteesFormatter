import sqlite3


class ManualEntry:
    name = []
    batch = [[[]]]

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
        tbatch = int(input('Enter total number of batches: '))
        tclass = int(input('Enter no. of class per day: '))
        obatch = []
        for i in range(torder):
            bbatch = []
            for j in range(tbatch):
                print('Enter TimeTable of Batch' + str(j + 1) + ' day order ' + str(i + 1) + ' : ')
                cbatch = []
                for K in range(tclass):
                    d = input('Enter class: ')
                    cbatch.append(d)
                bbatch.append(cbatch)
            obatch.append(bbatch)
        self.batch = obatch
        self.intodb()
        return

    def intodb(self):
        con = sqlite3.connect('datadb.sqlite')
        cur = con.cursor()
        # Inserting names into the database
        sql = '''CREATE TABLE IF NOT EXISTS STUDENTS(ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME VARCHAR(128) NOT NULL)'''
        cur.execute(sql)
        for n in self.name:
            sql = '''INSERT INTO STUDENTS(NAME) VALUES(?)'''
            cur.execute(sql, (n,))
        con.commit()

        # Inserting class with respect to time slot into the database
        sql = '''CREATE TABLE IF NOT EXISTS TIMETABLE(ORDERID INTEGER PRIMARY KEY AUTOINCREMENT,B1T1 VARCHAR(10) NOT 
        NULL, B1T2 VARCHAR(10) NOT NULL, B1T3 VARCHAR(10) NOT NULL, B1T4 VARCHAR(10) NOT NULL,B2T1 VARCHAR(10) NOT 
        NULL, B2T2 VARCHAR(10) NOT NULL, B2T3 VARCHAR(10) NOT NULL, B2T4 VARCHAR(10) NOT NULL) '''
        cur.execute(sql)
        for b in self.batch:
            sql = '''INSERT INTO TIMETABLE(B1T1,B1T2,B1T3,B1T4,B2T1,B2T2,B2T3,B2T4) VALUES (?,?,?,?,?,?,?,?)'''
            cur.execute(sql, (b[0][0], b[0][1], b[0][2], b[0][3], b[1][0], b[1][1], b[1][2], b[1][3],))
        con.commit()
        cur.close()
        return
