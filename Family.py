from Date import Date

class Family():

    def __init__(self, id):
        self.__id = id
        self.__marr = False
        self.__husb = False
        self.__wife = False
        self.__children = []
        self.__div = False
    
    def getID(self):
        return self.__id

    def setMarr(self, marr):
        self.__marr = marr

    def getMarr(self):
        return self.__marr

    def setHusb(self, husb):
        self.__husb = husb
    
    def getHusb(self):
        return self.__husb
    
    def setWife(self, wife):
        self.__wife = wife
    
    def getWife(self):
        return self.__wife

    def addChild(self, child):
        self.__children += [child]
    
    def getChildren(self):
        return self.__children
    
    def setDiv(self, div):
        self.__div = div
    
    def getDiv(self):
        return self.__div