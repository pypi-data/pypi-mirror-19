from parse import Parser
from hostapd import ParserHostapd

if __name__ == "__main__":

    print ('\n***********************')
    print ('*     Parse  tShark   *')
    print ('***********************')

    parser = Parser()
    parser.lire()

    print ('\n***********************')
    print ('*    Parse  hostapd   *')
    print ('***********************\n')

    parserhostapd = ParserHostapd()
    parserhostapd.lire()
