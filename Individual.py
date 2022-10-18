from Date import *
from datetime import date

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

    def getAge(self):
        today = date.today()
        if self.__birth:
            diff = today.year - self.__birth.year
            if today.month < MONTHS[self.__birth.month]:
                diff -= 1
            elif today.month == MONTHS[self.__birth.month] and today.day < self.__birth.day:
                diff -= 1
            return diff
        else: return False

    def __lt__(self, other):
        return self.getBirth() < other.getBirth()
