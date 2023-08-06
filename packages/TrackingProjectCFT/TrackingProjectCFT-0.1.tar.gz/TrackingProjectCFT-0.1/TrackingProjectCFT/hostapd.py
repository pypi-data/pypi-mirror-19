class ParserHostapd:
    def __init__(self):
        self.nom = ""

    def lire(self):
        with open("hostapd", "r") as f:
            for line in f.readlines():
                if(len(line) == 53):
                    numData = 0
                    for data in line.split(" "):
                        if(numData == 2):
                            print ('APPAREIL CONNECTE : ', data)
                        if(numData == 5):
                            print ('ASSOCIATION : ', data)
                        numData = numData + 1
                    print ("-------")
