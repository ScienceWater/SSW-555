import datetime
import unittest
from unittest.mock import patch
from GEDCOM_parse import *
from Date import *

class TestSprint1(unittest.TestCase):

    gedcom_file = open("error.ged")
    gedcom_parse(gedcom_file)

    def testStory1(self):
        '''Dates before current date (note these test cases will only all work properly before 2099)'''
        self.assertFalse(birthBeforeCurrent(individuals["@I7@"])) # born after today (Tim)
        self.assertFalse(marriageBeforeCurrent(families["@F1@"])) # married after today (Gru and Lucy)
        self.assertFalse(divorceBeforeCurrent(families["@F5@"])) # divorced after today (Bob and Isabelle)
        self.assertFalse(deathBeforeCurrent(individuals["@I9@"])) # died after today (Otto))
        self.assertTrue(birthBeforeCurrent(individuals["@I2@"])) # not born before today (Gru)
            
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
    
    def testStory7(self):
        '''Less than 150 years old (note these test cases will only work properly for the rest of the semester)'''
        self.assertFalse(under150Years(individuals["@I2@"])) # older than 150 years old (Gru)
        self.assertFalse(under150Years(individuals["@I3@"])) # 150 years old (Lucy)
        self.assertTrue(under150Years(individuals["@I1@"])) # less than 150 years old (Bob)
        self.assertTrue(under150Years(individuals["@I11@"])) # 1 year old (Dave)
        self.assertTrue(under150Years(individuals["@I7@"])) # not born yet/negative age (Tim)

    def testStory27(self):
        '''Include individual ages (note these test cases will only work properly for the rest of the semester)'''
        self.assertEqual(individuals["@I11@"].getAge(), 1) # Dave (young & alive)
        self.assertEqual(individuals["@I6@"].getAge(), 7) # Margo (young & dead)
        self.assertEqual(individuals["@I4@"].getAge(), 33) # Stuart (adult & alive)
        self.assertEqual(individuals["@I8@"].getAge(), 33) # Edith (adult & dead)
        self.assertEqual(individuals["@I2@"].getAge(), 180) # Gru (senior & alive)

    def testStory28(self):
        '''Order siblings by age'''
        self.assertEqual(sort_children(families['@F1@'].getChildren()), ['@I5@', '@I4@', '@I1@']) # family with 3 children
        self.assertEqual(sort_children(families['@F2@'].getChildren()), ['@I11@']) # family with 1 child (husband is spouse in two families)
        self.assertEqual(sort_children(families['@F3@'].getChildren()), ['@I9@']) # family with 1 child (husband is spouse in two families, wife is dead)
        self.assertEqual(sort_children(families['@F4@'].getChildren()), ['@I7@']) # family with 1 child (divorced)
        self.assertEqual(sort_children(families['@F5@'].getChildren()), []) # family with no children
    
    def testStory35(self):
        '''List recent births (test cases directly access withinRange function for consistent results regardless of current date)'''
        self.assertTrue(individuals["@I1@"].getBirth().withinRange(Date("12 NOV 1991"), 0)) # same day, should be true if range is 0
        self.assertTrue(individuals["@I1@"].getBirth().withinRange(Date("12 NOV 1991"), 1)) # same day, should be true if range is positive
        self.assertTrue(individuals["@I1@"].getBirth().withinRange(Date("12 NOV 1991"), -5000)) # same day, should be true if range is negative
        self.assertTrue(individuals["@I1@"].getBirth().withinRange(Date("21 NOV 1991"), 10)) # 9 days after, should be true if range is 10
        self.assertTrue(individuals["@I1@"].getBirth().withinRange(Date("21 NOV 1991"), 10)) # 9 days after, should be false if range is -10
    
    def testStory36(self):
        '''List recent deaths (test cases directly access withinRange function for consistent results regardless of current date)'''
        self.assertTrue(individuals["@I6@"].getDeath().withinRange(Date("17 JAN 2015"), 0)) # same day, should be true if range is 0
        self.assertTrue(individuals["@I6@"].getDeath().withinRange(Date("17 JAN 2015"), 1)) # same day, should be true if range is positive
        self.assertTrue(individuals["@I6@"].getDeath().withinRange(Date("17 JAN 2015"), -5000)) # same day, should be true if range is negative
        self.assertTrue(individuals["@I6@"].getDeath().withinRange(Date("26 JAN 2015"), 10)) # 9 days after, should be true if range is 10
        self.assertTrue(individuals["@I6@"].getDeath().withinRange(Date("26 JAN 2015"), 10)) # 9 days after, should be false if range is -10

    def testStory38(self):
        '''List upcoming birthdays (note these test cases will only work properly for the rest of the semester, and for an UPCOMING_LIMIT of 90)'''
        self.assertTrue(upcomingBirthday(individuals["@I7@"])) # upcoming birthday, this year (Tim: Dec)
        self.assertTrue(upcomingBirthday(individuals["@I2@"])) # upcoming birthday, next year (Gru: Jan)
        self.assertFalse(upcomingBirthday(individuals["@I5@"])) # not upcoming birthday (Kevin: Aug)
        self.assertFalse(upcomingBirthday(individuals["@I6@"])) # upcoming birthday but individual is deceased (Margo: Jan)
        self.assertFalse(upcomingBirthday(individuals["@I10@"])) # not upcoming birthday and individual is deceased (Agnes: Apr)

    def testStory39(self):
        '''List upcoming anniversaries'''

    gedcom_file.close()

if __name__ == '__main__':
    unittest.main()