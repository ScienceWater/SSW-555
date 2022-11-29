MONTHS = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}
DAYS_IN_MONTH = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

class Date():
    def __init__(self, str):
        '''Initializes date from GEDCOM input line str.'''
        str = str.split()
        self.day = int(str[0])
        self.month = str[1].upper()
        self.year = int(str[2])
    
    def __str__(self):
        return str(self.day) + " " + self.month + " " + str(self.year)
    
    def __eq__(self, other):
        '''(self == other) iff self and other are the same date.'''
        return self.day == other.day and self.month == other.month and self.year == other.year
    
    def __ne__(self, other):
        '''self != other'''
        return not (self == other)
    
    def __gt__(self, other):
        '''(self > other) iff self occurs after other.'''
        if self.year != other.year:
            return self.year > other.year
        elif self.month != other.month:
            return MONTHS[self.month] > MONTHS[other.month]
        else:
            return self.day > other.day
    
    def __lt__(self, other):
        '''(self < other) iff self occurs before other.'''
        if self.year != other.year:
            return self.year < other.year
        elif self.month != other.month:
            return MONTHS[self.month] < MONTHS[other.month]
        else:
            return self.day < other.day
    
    def __ge__(self, other):
        '''self >= other'''
        if self.year != other.year:
            return self.year > other.year
        elif self.month != other.month:
            return MONTHS[self.month] > MONTHS[other.month]
        else:
            return self.day >= other.day
    
    def __le__(self, other):
        '''self <= other'''
        if self.year != other.year:
            return self.year < other.year
        elif self.month != other.month:
            return MONTHS[self.month] < MONTHS[other.month]
        else:
            return self.day <= other.day
    
    def __isLeapYear(self):
        return (self.year % 4 == 0 and self.year % 100 != 0) or self.year % 400 == 0
    
    def __copy(self):
        return Date(self.__str__())
    
    def __daysInMonth(self):
        if self.month == "FEB" and self.__isLeapYear():
            return 29
        else:
            return DAYS_IN_MONTH[MONTHS[self.month]]
    
    def __addDays(self, days):
        '''Returns a new date 'days' days after self.'''
        self = self.__copy()
        self.day += days
        while self.day > self.__daysInMonth():
            self.day -= self.__daysInMonth()
            if self.month == "DEC":
                self.month = "JAN"
                self.year += 1
            else:
                self.month = list(MONTHS.keys())[list(MONTHS.values()).index(MONTHS[self.month]) + 1]
        while self.day < 1:
            if self.month == "JAN":
                self.month = "DEC"
                self.year -= 1
            else:
                self.month = list(MONTHS.keys())[list(MONTHS.values()).index(MONTHS[self.month]) - 1]
            self.day += self.__daysInMonth()
        return self

    def withinRange(self, other, range):
        '''Returns true iff self <= other <= self + range (if range is positive)
           or self + range <= other <= self (if range is negative).'''
        limit = self.__addDays(range)
        if range > 0:
            return self <= other <= limit
        else:
            return limit <= other <= self
    
    def exists(self):
        '''Returns true iff self represents a valid date. A date can be invalid because
           the month does not exist or because the day does not exist within the given month/year.'''
        return self.month in MONTHS and 1 <= self.day <= self.__daysInMonth