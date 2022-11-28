from Individual import Individual
from Family import Family
from Date import *
import sys
from prettytable import PrettyTable
from datetime import date

# Dictionary with all valid tags within scope of project as keys, and their respective levels as values.
TAGS = {"INDI": 0, "NAME": 1, "SEX": 1, "BIRT": 1, "DEAT": 1, "FAMC": 1, "FAMS": 1, "FAM": 0, "MARR": 1,\
        "HUSB": 1, "WIFE": 1, "CHIL": 1, "DIV": 1, "DATE": 2, "HEAD": 0, "TRLR": 0, "NOTE": 0}

RECENT_LIMIT = 90 # Maximum number of days before today a date can be to be considered "recent."
UPCOMING_LIMIT = 90 # Maximum number of days after today a date can be to be considered "upcoming."

individuals = dict()
families = dict()

def tableFormatter(property):
    if property:
        return property
    else:
        return "N/A"

def print_indi():
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    for indi in individuals.values():
        table.add_row(list(map(tableFormatter, [indi.getID(), indi.getName(), indi.getSex(), indi.getBirth(),\
            indi.getAge(), "No" if indi.getDeath() else "Yes", indi.getDeath(), indi.getFamC(), indi.getFamS()])))
    print(table)

def sort_children(unsorted_children):
    children = []
    for child in unsorted_children:
        children += [individuals[child]]
    children.sort()
    childrenID = []
    for child in children:
        childrenID += [child.getID()]
    return childrenID

def print_fam():
    table = PrettyTable()
    table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
    for fam in families.values():
        table.add_row(list(map(tableFormatter, [fam.getID(), fam.getMarr(), fam.getDiv(), fam.getHusb(),\
            individuals[fam.getHusb()].getName(), fam.getWife(), individuals[fam.getWife()].getName(),\
                sort_children(fam.getChildren())])))
    print(table)

def gedcom_parse(file):
    '''
    Parses through a given .GEDCOM file and prints the following for each line:
    "--> <input line>"
    "<-- <level>|<tag>|<valid?> : Y or N|<arguments>"
    '''
    # Set of all tags which come after the arguments as opposed to before.
    SECOND_TAGS = {"INDI", "FAM"}

    working = False
    current_tag = ""
    current_id = ""
    date_tag = ""
    
    for line in file:
        line = line[:-1]
        # print("--> " + line)
        line = line.split(" ")
        level = int(line[0])
        tag_second = False # After if block is executed, either index of tag >= 2 or False.
        if level == 0:
            for tag in SECOND_TAGS:
                if tag in line:
                    tag_second = line.index(tag)
                    break
        if tag_second:
            tag = line[tag_second]
            args = " ".join(line[1:tag_second])
        else:
            tag = line[1]
            args = " ".join(line[2:])
        # print("<-- " + str(level) + '|' + tag + '|' +\
        #       ('Y' if (tag in TAGS and TAGS[tag] == level) else 'N') + '|' + args)

        if working and level == 0:
            if current_tag == "INDI":
                individuals[current_id] = individual
                individual = ""
            elif current_tag == "FAM":
                families[current_id] = family
                family = ""
            working = False

        if tag == "INDI":
            individual = Individual(args)
            working = True
            current_tag = tag
            current_id = args
        elif tag == "FAM":
            family = Family(args)
            working = True
            current_tag = tag
            current_id = args

        if current_tag == "INDI":
            if tag == "NAME":
                individual.setName(args)
            elif tag == "SEX":
                individual.setSex(args)
            elif tag == "BIRT" or tag == "DEAT":
                date_tag = tag
            elif tag == "FAMC":
                individual.setFamC(args)
            elif tag == "FAMS":
                individual.addFamS(args)
            elif tag == "DATE":
                if date_tag == "BIRT":
                    individual.setBirth(Date(args))
                    date_tag = ""
                if date_tag == "DEAT":
                    individual.setDeath(Date(args))
                    date_tag = ""
        elif current_tag == "FAM":
            if tag == "MARR" or tag == "DIV":
                date_tag = tag
            elif tag == "HUSB":
                family.setHusb(args)
            elif tag == "WIFE":
                family.setWife(args)
            elif tag == "CHIL":
                family.addChild(args)
            elif tag == "DATE":
                if date_tag == "MARR":
                    family.setMarr(Date(args))
                    date_tag = ""
                if date_tag == "DIV":
                    family.setDiv(Date(args))
                    date_tag = ""

def birthBeforeMarriage(indi):
    '''Returns true iff all marriages of indi are not before birth of indi. (User Story 2)'''
    birth = indi.getBirth()
    if birth:
        for fam in indi.getFamS():
            if families[fam].getMarr() < birth:
                return False
    return True

def birthBeforeDeath(indi):
    '''Returns true iff death date is not before birth date. (User Story 3)'''
    if indi.getBirth() and indi.getDeath():
        return indi.getBirth() <= indi.getDeath()
    return True

def marriage_before_divorce(fam):
    '''Returns true iff marriage date is not after divorce date. (User Story 4)'''
    if fam.getMarr() and fam.getDiv():
        return fam.getMarr() <= fam.getDiv()
    return True

def marriage_before_death(indi):
    '''Returns true iff all marriage dates are not after death date. (User Story 5)'''
    death = indi.getDeath()
    if death:
        for fam in indi.getFamS():
            if death < families[fam].getMarr():
                return False
    return True

def dateBeforeCurrent(d):
    '''Returns true iff d is not after current date.'''
    if not d: return True
    current = date.today()
    if d.year < current.year:
        return True
    elif d.year == current.year:
        if MONTHS[d.month] < current.month:
            return True
        elif MONTHS[d.month] == current.month:
            return d.day <= current.day
        else:
            return False
    else:
        return False

def birthBeforeCurrent(indi):
    '''Returns true iff birth date is not after current date.'''
    return dateBeforeCurrent(indi.getBirth())

def marriageBeforeCurrent(fam):
    '''Returns true iff marriage date is not after current date.'''
    return dateBeforeCurrent(fam.getMarr())

def divorceBeforeCurrent(fam):
    '''Returns true iff divorce date is not after current date.'''
    return dateBeforeCurrent(fam.getDiv())

def deathBeforeCurrent(indi):
    '''Returns true iff death date is not after current date.'''
    return dateBeforeCurrent(indi.getDeath())

def under150Years(indi):
    '''Returns true iff indi is less than 150 years old (individuals with no birth date are assumed to be under 150).'''
    age = indi.getAge()
    return (not age) or age < 150

def fewerThan15Siblings(fam):
    '''Returns true iff fam has fewer than 15 siblings'''
    num_siblings = len(fam.getChildren())
    return num_siblings < 15

def marriedToSibling(indi):
    '''Returns true iff indi is married to a sibling'''
    # Checks if indi and their spouse are children of the same family, for each family in which indi is a spouse
    if indi.getSex() == "M":
        for fam in indi.getFamS():
            if indi.getFamC() == individuals[families[fam].getWife()].getFamC():
                return families[fam].getWife()
    if indi.getSex() == "F":
        for fam in indi.getFamS():
            if indi.getFamC() == individuals[families[fam].getHusb()].getFamC():
                return families[fam].getHusb()
    return False

def birthIsRecent(indi):
    '''Returns true iff indi was born within the past RECENT_LIMIT days.'''
    if indi.getBirth():
        today = date.today()
        today = Date(str(today.day) + " " + list(MONTHS.keys())[today.month - 1] + " " + str(today.year))
        return indi.getBirth().withinRange(today, RECENT_LIMIT)
    else:
        return False

def deathIsRecent(indi):
    '''Returns true iff indi has died within the past RECENT_LIMIT days.'''
    if indi.getDeath():
        today = date.today()
        today = Date(str(today.day) + " " + list(MONTHS.keys())[today.month - 1] + " " + str(today.year))
        return indi.getDeath().withinRange(today, -RECENT_LIMIT)
    else:
        return False

def recentDateCheck():
    recentBirths = []
    recentDeaths = []
    for indi in individuals.values():
        if birthIsRecent(indi):
            recentBirths += [indi]
        if deathIsRecent(indi):
            recentDeaths += [indi]
    if recentBirths:
        print("\nThe following people were born recently (within the last " + str(RECENT_LIMIT) + " days):")
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Birthday"]
        for indi in recentBirths:
            table.add_row([indi.getID(), indi.getName(), indi.getBirth()])
        print(table)
    if recentDeaths:
        print("\nThe following people have died recently (within the last " + str(RECENT_LIMIT) + " days):")
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Death Date"]
        for indi in recentDeaths:
            table.add_row([indi.getID(), indi.getName(), indi.getDeath()])
        print(table)
    if recentBirths or recentDeaths:
        print()

def upcomingBirthday(indi):
    '''Returns true iff indi's birthday is within the next UPCOMING_LIMIT days.'''
    if indi.getBirth() and not indi.getDeath():
        today = date.today()
        today = Date(str(today.day) + " " + list(MONTHS.keys())[today.month - 1] + " " + str(today.year))
        birthday = indi.getBirth()
        birthday_this_year = Date(str(birthday.day) + " " + birthday.month + " " + str(today.year))
        birthday_next_year = Date(str(birthday.day) + " " + birthday.month + " " + str(today.year + 1))
        return today.withinRange(birthday_this_year, UPCOMING_LIMIT) or today.withinRange(birthday_next_year, UPCOMING_LIMIT)
    else:
        return False

def upcomingAnniversary(fam):
    '''Returns true iff fam's anniversary is within the next UPCOMING_LIMIT days.'''
    if fam.getMarr() and not fam.getDiv():
        today = date.today()
        today = Date(str(today.day) + " " + list(MONTHS.keys())[today.month - 1] + " " + str(today.year))
        anniversary = fam.getMarr()
        anniversary_this_year = Date(str(anniversary.day) + " " + anniversary.month + " " + str(today.year))
        anniversary_next_year = Date(str(anniversary.day) + " " + anniversary.month + " " + str(today.year + 1))
        return today.withinRange(anniversary_this_year, UPCOMING_LIMIT) or today.withinRange(anniversary_next_year, UPCOMING_LIMIT)
    else:
        return False

def upcomingDateCheck():
    '''Checks for and prints (if applicable) events (birthdays & anniversaries) within the next UPCOMING_LIMIT days.'''
    upcomingBirthdays = []
    upcomingAnniversaries = []

    for indi in individuals.values():
        if upcomingBirthday(indi):
            upcomingBirthdays += [indi]
    for fam in families.values():
        if upcomingAnniversary(fam):
            upcomingAnniversaries += [fam]

    if upcomingBirthdays:
        print("\nThe following people have upcoming birthdays (within the next " + str(UPCOMING_LIMIT) + " days):")
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Birthday"]
        for indi in upcomingBirthdays:
            table.add_row([indi.getID(), indi.getName(), indi.getBirth()])
        print(table)
    if upcomingAnniversaries:
        print("\nThe following families have upcoming anniversaries (within the next " + str(UPCOMING_LIMIT) + " days):")
        table = PrettyTable()
        table.field_names = ["ID", "Husband Name", "Wife Name", "Marriage Date"]
        for fam in upcomingAnniversaries:
            table.add_row([fam.getID(), individuals[fam.getHusb()].getName(), individuals[fam.getWife()].getName(), fam.getMarr()])
        print(table)
    if upcomingBirthdays or upcomingAnniversaries:
        print()    

def anomalyCheck():
    for indi in individuals.values():
        if not under150Years(indi):
            print("Anomaly: Individual " + str(indi.getID()) + " is " + str(indi.getAge()) + " years old. Are you sure that's correct?")
        if marriedToSibling(indi):
            print("Anomoly: Individual " + str(indi.getID()) + " is married to a sibling (individual " + marriedToSibling(indi) + "). Are you sure that's correct?")
    for fam in families.values():
        if not fewerThan15Siblings(fam):
            print("Anomoly: Family " + str(fam.getID()) + " has " + str(len(fam.getChildren())) + " siblings. Are you sure that's correct?")

def errorCheck():
    for indi in individuals.values():
        if not birthBeforeMarriage(indi):
            print("Error: Marriage date of Individual " + str(indi.getID()) + " is before their birth date.")
        if not birthBeforeDeath(indi):
            print("Error: Death date of Individual " + str(indi.getID()) + " is before their birth date.")
        if not marriage_before_death(indi):
            print("Error: Death date of Individual " + str(indi.getID()) + " is before their marriage date.")
        if not birthBeforeCurrent(indi):
            print("Error: Birth date of Individual " + str(indi.getID()) + " is in the future.")
        if not deathBeforeCurrent(indi):
            print("Error: Death date of Individual " + str(indi.getID()) + " is in the future.")
    for fam in families.values():
        if not marriage_before_divorce(fam):
            print("Error: Divorce date of Family " + str(fam.getID()) + " is before marriage date.")
        if not marriageBeforeCurrent(fam):
            print("Error: Marriage date of Family " + str(fam.getID()) + " is in the future.")
        if not divorceBeforeCurrent(fam):
            print("Error: Divorce date of Family " + str(fam.getID()) + " is in the future.")

def main(argv):
    if len(argv) != 2:
        print("Usage: " + str(argv[0]) + " <GEDCOM file>")
        return

    gedcom_file_name = str(argv[1])

    try:
        gedcom_file = open(gedcom_file_name)
    except:
        print("Invalid file name: File must be a GEDCOM file")
        return

    gedcom_parse(gedcom_file)
    print_indi()
    print()
    print_fam()
    print()
    recentDateCheck()
    upcomingDateCheck()
    errorCheck()
    anomalyCheck()
    gedcom_file.close()

if __name__ == "__main__":
    main(sys.argv)