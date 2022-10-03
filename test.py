import unittest
from GEDCOM_parse import *

class TestSprint1(unittest.TestCase):

    gedcom_file = open("error.ged")
    gedcom_parse(gedcom_file)

    def story2(self):
        '''Birth before marriage'''
        pass

    def story3(self):
        '''Birth before death'''
        pass

    def story4(self):
        '''Marriage before divorce'''
        self.assertFalse(marriageBeforeDivorce(families["@F1@"])) # marriage date after divorce date (Gru & Lucy)
        self.assertTrue(marriageBeforeDivorce(families["@F4@"])) # marriage date same as divorce date (Kevin & Margo)
        self.assertTrue(marriageBeforeDivorce(families["@F5@"])) # marriage date before divorce date (Bob & Isabelle)
        self.assertTrue(marriageBeforeDivorce(families["@F2@"])) # no divorce date (Stuart & Agnes)
        self.assertTrue(marriageBeforeDivorce(families["@F3@"])) # no divorce date for same husband (Stuart & Edith)

    def story5(self):
        '''Marriage before death'''
        self.assertFalse(marriageBeforeDeath(individuals["@I8@"])) # marriage date after death date (Edith)
        self.assertTrue(marriageBeforeDeath(individuals["@I6@"])) # marriage date same as death date (Margo)
        self.assertTrue(marriageBeforeDeath(individuals["@I10@"])) # marriage date before death date (Agnes)
        self.assertTrue(marriageBeforeDeath(individuals["@I3@"])) # marriage, no death (Lucy)
        self.assertTrue(marriageBeforeDeath(individuals["@I11@"])) # no marriage, no death (Dave)

    gedcom_file.close()

if __name__ == '__main__':
    unittest.main()