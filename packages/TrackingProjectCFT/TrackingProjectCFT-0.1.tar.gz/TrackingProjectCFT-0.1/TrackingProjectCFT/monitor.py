import sys
import time
k = 0
try:
    buff = ''
    while True:
        buff += sys.stdin.read(1)
        if buff.endswith('\n'):

            while (buff[:1] < '0' or buff[:1] > '9'):
                buff = buff[1:]

            numData = 0
            liste = ["", "", "", "", ""]
            for data in buff.split(" "):
                # print numData, '--', data
                if(numData == 1):
                # print data
                    liste[0] = data
                if(numData == 2):
                    liste[1] = data
                if(numData == 3):
                    liste[2] = data
                if(numData == 5):
                    liste[3] = data
                if(numData == 11):
                    liste[4] = data

                numData = numData + 1

            if(liste[4] == "Probe"):
                print (liste[0])
                print (liste[1])
                print (liste[2])
                print (liste[4])
                print ('\n------\n')

            buff = ''

except KeyboardInterrupt:
    sys.stdout.flush()
    pass
print (k)
