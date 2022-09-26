# Dictionary with all valid tags within scope of project as keys, and their respective levels as values.
TAGS = {"INDI": 0, "NAME": 1, "SEX": 1, "BIRT": 1, "DEAT": 1, "FAMC": 1, "FAMS": 1, "FAM": 0, "MARR": 1,\
        "HUSB": 1, "WIFE": 1, "CHIL": 1, "DIV": 1, "DATE": 2, "HEAD": 0, "TRLR": 0, "NOTE": 0}

def gedcom_parse(file):
    '''
    Parses through a given .GEDCOM file and prints the following for each line:
    "--> <input line>"
    "<-- <level>|<tag>|<valid?> : Y or N|<arguments>"
    '''
    # Set of all tags which come after the arguments as opposed to before.
    SECOND_TAGS = {"INDI", "FAM"}

    individuals = dict()
    families = dict()
    working = False
    current_tag = ""
    current_id = ""
    date_tag = ""
    
    for line in file:
        line = line[:-1]
        print("--> " + line)
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
        print("<-- " + str(level) + '|' + tag + '|' +\
              ('Y' if (tag in TAGS and TAGS[tag] == level) else 'N') + '|' + args)

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
                    individual.setBirth(args)
                    date_tag = ""
                if date_tag == "DEAT":
                    individual.setDeath(args)
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
                    family.setMarr(args)
                    date_tag = ""
                if date_tag == "DIV":
                    family.setDiv(args)
                    date_tag = ""