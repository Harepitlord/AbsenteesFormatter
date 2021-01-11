from dataentry import ManualEntry
from formatter import Format
import sys
import time


def main():
    NoBatch = 2
    NoHour = 4
    while True:
        print('Enter the choice : \n1.Data formatting\n2.Data entry\n3.Exit')
        choice = int(input())
        if choice == 1:
            f = Format(NoBatch,NoHour)
            f.formatter()
        if choice == 2:
            d = ManualEntry()
            d.Entry()
        else:
            print(flush=True)
            print('Exiting the Program...........')
            time.sleep(3)
            sys.exit()


if __name__ == '__main__':
    main()
