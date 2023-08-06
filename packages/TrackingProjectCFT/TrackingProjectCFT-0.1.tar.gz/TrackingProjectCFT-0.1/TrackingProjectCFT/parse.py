class Parser:
    """Classe pour paser les ficher"""
    def __init__(self):
        self.nom = ""

    def lire(self):
        with open("data", "r") as f:
            print ('\n')
            for line in f.readlines():
                if(len(line) == 101):

                    while (line[:1] < '0' or line[:1] > '9'):
                        line = line[1:]
        #            print(line)

                    numData = 0
                    for data in line.split(" "):
        #                print(data, numData)
                        if(numData == 1):
                            print ('DATE         : ', data)
                        if(numData == 2):
                            print ('HEURE        : ', data)
                        if(numData == 3):
                            print ('MAC SOURCE   : ', data)
                        if(numData == 5):
                            print ('MAC DEST     : ', data)

                        numData = numData + 1
                    print ('\n------\n')
