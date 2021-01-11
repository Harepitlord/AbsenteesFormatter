import sqlite3


class Format:
    NoBatch = 0
    NoHour = 0
    data = {}
    odname = []
    od = False
    fstr = open("AbsenteesFormatter/output.txt", "w")

    def __int__(self,b,h):
        self.LoadData()
        self.NoBatch = b
        self.NoHour = h
        # self.fstr = open("output.txt", "w")

    def LoadData(self):

        dat = input('Enter the date (dd/mm/yyyy) : ')
        self.data['dat'] = dat
        order = int(input('Enter day order : '))
        self.data['Order'] = order
        con = sqlite3.connect('datadb.sqlite')
        cur = con.cursor()
        print('Loading Students Info.....')
        sqls = "SELECT * FROM Students"
        cur.execute(sqls)
        rows = cur.fetchall()
        if rows is None:
            print('Student table is empty')
            return

        student = {}
        for row in rows:
            student[row[0]] = row[1]
        self.data['student'] = student

        print('Loading Day Order Info.....')
        sqld = "SELECT * FROM TIMETABLE WHERE ORDERID = ?"
        cur.execute(sqld, (self.data['Order'],))
        rows = cur.fetchall()
        if rows is None:
            print('Day Order Table is empty')
            return
        for b in range(self.NoBatch):
            dat = []
            for r in rows[0][b*self.NoHour+1:(b+1)*self.NoHour +1]:
                dat.append(r)
            self.data['batch' + str(b + 1)] = dat
        return

    def NameFinder(self, noa, informed):
        i = 0
        while i < noa:
            try:
                reg = int(input('Enter roll number: '))
                if reg < 10:
                    self.fstr.write('19EUCB00' + str(reg))
                elif reg < 100:
                    self.fstr.write('19EUCB0' + str(reg))
                else:
                    self.fstr.write('20EUCB' + str(reg))
                if informed:
                    self.fstr.write('    ' + self.data["student"][reg] + '  (informed)\n')
                    if reg not in self.odname:
                        self.odname.append(reg)
                else:
                    self.fstr.write('    ' + self.data["student"][reg] + '  (uninformed)\n')
                i += 1
            except ValueError:
                print('Enter a valid register number only number')
                continue
        return

    def AbsenteesFinder(self, a, bno, hr):
        noa = int(input('Enter no. of absentees in ' + str(a) + '(batch ' + str(bno) + ', ' + str(hr) + ') : '))
        if noa == 0:
            self.fstr.write(' \nBatch ' + str(bno) + ': ( ' + a + ' ) : ' + 'nil' + ' absentees\n')
        else:
            self.fstr.write(' \nBatch ' + str(bno) + ': ( ' + a + ' ) : ' + str(noa) + ' absentees\n')
            self.NameFinder(noa, False)
        if self.od:
            oda = int(input('Enter no. of OD in ' + a + ': '))
            if oda == 0:
                self.fstr.write('\n  OD ' + ' : nil\n')
            else:
                self.fstr.write(' \n   OD : ' + '  ' + a + ' : ' + str(oda) + '\n')
                self.NameFinder(oda, True)
        return

    def formatter(self):
        self.LoadData()
        # print(self.data)
        if input('Anyone on OD: (y-True) ').lower() == 'y':
            self.od = True
        self.fstr.write('Date: ' + self.data['dat'] + '\nDay Order: ' + str(self.data['Order']))
        for c in range(1, self.NoHour+1):
            self.fstr.write('\nHour ' + str(c) + ' : ')
            for b in range(1,self.NoBatch+1):
                self.AbsenteesFinder(self.data['batch'+str(b)][c-1],b,c)

        if len(self.odname) > 0:
            self.fstr.write("\nOD: " + str(len(self.odname)) + "\n\n")
            for reg in self.odname:
                if reg < 10:
                    self.fstr.write('19EUCB00' + str(reg))
                else:
                    self.fstr.write('19EUCB0' + str(reg))
                self.fstr.write('    ' + self.data["student"][reg] + '  (informed)\n')

        self.fstr.close()
        return
