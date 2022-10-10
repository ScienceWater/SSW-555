from Individual import Individual
from Family import Family
from Date import Date
import sys
from prettytable import PrettyTable

# Dictionary with all valid tags within scope of project as keys, and their respective levels as values.
TAGS = {"INDI": 0, "NAME": 1, "SEX": 1, "BIRT": 1, "DEAT": 1, "FAMC": 1, "FAMS": 1, "FAM": 0, "MARR": 1,\
        "HUSB": 1, "WIFE": 1, "CHIL": 1, "DIV": 1, "DATE": 2, "HEAD": 0, "TRLR": 0, "NOTE": 0}

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
        table.add_row([tableFormatter(indi.getID()), tableFormatter(indi.getName()), tableFormatter(indi.getSex()), tableFormatter(indi.getBirth()),\
            tableFormatter(indi.getAge()), not indi.getDeath(), tableFormatter(indi.getDeath()), tableFormatter(indi.getFamC()), tableFormatter(indi.getFamS())])
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
        table.add_row([tableFormatter(fam.getID()), tableFormatter(fam.getMarr()), tableFormatter(fam.getDiv()), tableFormatter(fam.getHusb()),\
            tableFormatter(individuals[fam.getHusb()].getName()), tableFormatter(fam.getWife()), tableFormatter(individuals[fam.getWife()].getName()),\
                tableFormatter(sort_children(fam.getChildren()))])
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
    for fam in indi.getFamS():
        if families[fam].getMarr() < birth:
            return False
    return True

def birthBeforeDeath(indi):
    '''Returns true iff death date is not before birth date. (User Story 3)'''
    if indi.getDeath():
        return indi.getBirth() <= indi.getDeath()
    return True

def marriageBeforeDivorce(fam):
    '''Returns true iff marriage date is not after divorce date. (User Story 4)'''
    if fam.getDiv():
        return fam.getMarr() <= fam.getDiv()
    return True

def marriageBeforeDeath(indi):
    '''Returns true iff all marriage dates are not after death date. (User Story 5)'''
    death = indi.getDeath()
    if death:
        for fam in indi.getFamS():
            if death < families[fam].getMarr():
                return False
    return True

def anomalyCheck():
    for indi in individuals.values():
        if indi.getAge() >= 150:
            print("Anomaly: Individual " + str(indi.getID()) + " is " + str(indi.getAge()) + " years old. Are you sure that's correct?")

def errorCheck():
    for indi in individuals.values():
        if not birthBeforeMarriage(indi):
            print("Error: Marriage date of Individual " + str(indi.getID()) + " is before their birth date.")
        if not birthBeforeDeath(indi):
            print("Error: Death date of Individual " + str(indi.getID()) + " is before their birth date.")
        if not marriageBeforeDeath(indi):
            print("Error: Death date of Individual " + str(indi.getID()) + " is before their marriage date.")
    for fam in families.values():
        if not marriageBeforeDivorce(fam):
            print("Error: Divorce date of Family " + str(fam.getID()) + " is before marriage date.")

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
    errorCheck()
    anomalyCheck()
    gedcom_file.close()

if __name__ == "__main__":
    main(sys.argv)