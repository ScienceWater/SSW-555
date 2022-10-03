from Individual import Individual
from Family import Family
from Date import Date
import sys

# Dictionary with all valid tags within scope of project as keys, and their respective levels as values.
TAGS = {"INDI": 0, "NAME": 1, "SEX": 1, "BIRT": 1, "DEAT": 1, "FAMC": 1, "FAMS": 1, "FAM": 0, "MARR": 1,\
        "HUSB": 1, "WIFE": 1, "CHIL": 1, "DIV": 1, "DATE": 2, "HEAD": 0, "TRLR": 0, "NOTE": 0}

individuals = dict()
families = dict()

def print_indi(dict):
    longest_id = len("Individual ID")
    longest_name = len("Individual Name")

    for key in dict:
        if len(key) > longest_id:
            longest_id = len(key)
        if len(dict[key].getName()) > longest_name:
            longest_name = len(dict[key].getName())

    print(("{:<" + str(longest_id + 2) + "} {:<" + str(longest_name + 2) + "}").format("Individual ID", "Individual Name"))
    
    for key in dict:
        print(("{:<" + str(longest_id + 2) + "} {:<" + str(longest_name + 2) + "}").format(key, dict[key].getName()))

def print_fam(dict):
    longest_fam_id = len("Family ID")
    longest_husb_id = len("Husband ID")
    longest_husb_name = len("Husband Name")
    longest_wife_id = len("Wife ID")
    longest_wife_name = len("Wife Name")

    for key in dict:
        husb = dict[key].getHusb()
        wife = dict[key].getWife()

        if len(key) > longest_fam_id:
            longest_fam_id = len(key)
        if len(husb) > longest_husb_id:
            longest_husb_id = len(husb)
        if len(individuals[husb].getName()) > longest_husb_name:
            longest_husb_name = len(individuals[husb].getName())
        if len(wife) > longest_wife_id:
            longest_wife_id = len(wife)
        if len(individuals[wife].getName()) > longest_wife_name:
            longest_wife_name = len(individuals[wife].getName())

    print(("{:<" + str(longest_fam_id + 2) + "} {:<" + str(longest_husb_id + 2) + "} {:<" + str(longest_husb_name + 2) + "} {:<" + str(longest_wife_id + 2) + "} {:<" + str(longest_wife_name + 2) +\
         "}").format("Family ID", "Husband ID", "Husband Name", "Wife ID", "Wife Name"))
    
    for key in dict:
        husb = dict[key].getHusb()
        wife = dict[key].getWife()

        print(("{:<" + str(longest_fam_id + 2) + "} {:<" + str(longest_husb_id + 2) + "} {:<" + str(longest_husb_name + 2) + "} {:<" + str(longest_wife_id + 2) + "} {:<" + str(longest_wife_name + 2) +\
         "}").format(key, husb, individuals[husb].getName(), wife, individuals[wife].getName()))

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
    '''Returns true iff all marriages of indi are not before birth of indi.'''
    birth = indi.getBirth()
    for fam in indi.getFamS():
        if families[fam].getMarr() < birth:
            return False
    return True

def birthBeforeDeath(indi):
    '''Returns true iff death date is not before birth date.'''
    if indi.getDeath():
        return indi.getBirth() <= indi.getDeath()
    return True

def marriageBeforeDivorce(fam):
    '''Returns true iff marriage date is not after divorce date'''
    if fam.getDiv():
        return fam.getMarr() <= fam.getDiv()
    return True

def marriageBeforeDeath(indi):
    '''Returns true iff all marriage dates are not after death date'''
    death = indi.getDeath()
    if death:
        for fam in indi.getFamS():
            if death < families[fam].getMarr():
                return False
    return True

def errorCheck():
    for indi in individuals.values():
        if not birthBeforeMarriage(indi):
            print("Error: Marriage date of Individual " + indi + " is before their birth date.")
        if not birthBeforeDeath(indi):
            print("Error: Death date of Individual " + indi + " is before their birth date.")
        if not marriageBeforeDeath(indi):
            print("Error: Death date of Individual " + indi + " is before their marriage date.")
    for fam in families.values():
        if not marriageBeforeDivorce(fam):
            print("Error: Divorce date of Family " + fam + " is before marriage date.")

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
    print_indi(individuals)
    print()
    print_fam(families)
    print()
    errorCheck()
    gedcom_file.close()

if __name__ == "__main__":
    main(sys.argv)