from Date import Date

class Individual():

    def __init__(self, id):
        self.__id = id
        self.__name = False
        self.__sex = False
        self.__birth = False
        self.__death = False
        self.__famC = False
        self.__famS = []
    
    def getID(self):
        return self.__id

    def setName(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def setSex(self, sex):
        self.__sex = sex
    
    def getSex(self):
        return self.__sex
    
    def setBirth(self, birth):
        self.__birth = birth
    
    def getBirth(self):
        return self.__birth
    
    def setDeath(self, death):
        self.__death = death
    
    def getDeath(self):
        return self.__death
    
    def setFamC(self, famC):
        self.__famC = famC
    
    def getFamC(self):
        return self.__famC
    
    def addFamS(self, famS):
        self.__famS += [famS]
    
    def getFamS(self):
        return self.__famS