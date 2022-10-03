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