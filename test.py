import datetime
import unittest
from unittest.mock import patch
from GEDCOM_parse import *

class TestSprint1(unittest.TestCase):

    gedcom_file = open("error.ged")
    gedcom_parse(gedcom_file)

    def testStory2(self):
        '''Birth before marriage'''
        self.assertFalse(birthBeforeMarriage(individuals["@I10@"])) # married before born (Agnes)
        self.assertTrue(birthBeforeMarriage(individuals["@I6@"])) # married same day as born (Margo)
        self.assertTrue(birthBeforeMarriage(individuals["@I1@"])) # married after born (Bob)
        self.assertTrue(birthBeforeMarriage(individuals["@I9@"])) # never married (Otto)
        self.assertTrue(birthBeforeMarriage(individuals["@I4@"])) # married twice after born (Stuart)

    def testStory3(self):
        '''Birth before death'''
        self.assertFalse(birthBeforeDeath(individuals["@I8@"])) # dies before born (Edith)
        self.assertTrue(birthBeforeDeath(individuals["@I6@"])) # death date same as birth date (Margo)
        self.assertTrue(birthBeforeDeath(individuals["@I10@"])) # dies after born (Agnes)
        self.assertTrue(birthBeforeDeath(individuals["@I2@"])) # still alive, old (Gru)
        self.assertTrue(birthBeforeDeath(individuals["@I1@"])) # still alive, young (Bob)

    def testStory4(self):
        '''Marriage before divorce'''
        self.assertFalse(marriage_before_divorce(families["@F1@"])) # marriage date after divorce date (Gru & Lucy)
        self.assertTrue(marriage_before_divorce(families["@F4@"])) # marriage date same as divorce date (Kevin & Margo)
        self.assertTrue(marriage_before_divorce(families["@F5@"])) # marriage date before divorce date (Bob & Isabelle)
        self.assertTrue(marriage_before_divorce(families["@F2@"])) # no divorce date (Stuart & Agnes)
        self.assertTrue(marriage_before_divorce(families["@F3@"])) # no divorce date for same husband (Stuart & Edith)

    def testStory5(self):
        '''Marriage before death'''
        self.assertFalse(marriage_before_death(individuals["@I8@"])) # marriage date after death date (Edith)
        self.assertTrue(marriage_before_death(individuals["@I6@"])) # marriage date same as death date (Margo)
        self.assertTrue(marriage_before_death(individuals["@I10@"])) # marriage date before death date (Agnes)
        self.assertTrue(marriage_before_death(individuals["@I3@"])) # marriage, no death (Lucy)
        self.assertTrue(marriage_before_death(individuals["@I11@"])) # no marriage, no death (Dave)

    # only functional until next birthday occurs (Jan 5)
    def testStory27(self):
        '''Include individual ages'''
        self.assertEqual(individuals["@I11@"].getAge(), 1) # Dave (young & alive)
        self.assertEqual(individuals["@I6@"].getAge(), 7) # Margo (young & dead)
        self.assertEqual(individuals["@I4@"].getAge(), 33) # Stuart (adult & alive)
        self.assertEqual(individuals["@I8@"].getAge(), 33) # Edith (adult & dead)
        self.assertEqual(individuals["@I2@"].getAge(), 80) # Gru (senior & alive)

    def testStory28(self):
        '''Order siblings by age'''
        self.assertEqual(sort_children(families['@F1@'].getChildren()), ['@I5@', '@I4@', '@I1@']) # family with 3 children
        self.assertEqual(sort_children(families['@F2@'].getChildren()), ['@I11@']) # family with 1 child (husband is spouse in two families)
        self.assertEqual(sort_children(families['@F3@'].getChildren()), ['@I9@']) # family with 1 child (husband is spouse in two families, wife is dead)
        self.assertEqual(sort_children(families['@F4@'].getChildren()), ['@I7@']) # family with 1 child (divorced)
        self.assertEqual(sort_children(families['@F5@'].getChildren()), []) # family with no children

    gedcom_file.close()

if __name__ == '__main__':
    unittest.main()