from django.test import TestCase
from MainApp import FileParser
import pandas
# Create your tests here.


class CorrectDataTests(TestCase):
    def setUp(self):
        #f = open("/home/alex/Documents/Logs_Course A_StudentsActivities.xlsx", "rb")
        f = open("/home/alex/Documents/Copy of Logs_Course A_StudentsActivities_invalid.xlsx", "rb")

        vv = pandas.read_excel(f)
        self.parser = FileParser.FileParser(vv);
        self.parser.findColsIndexes()
        self.parser.getUsersSubmissions()


    def test_cols_len(self):
        self.assertEqual(len(self.parser.cols_dict), 5)


    def test_calculate_mode(self):
        self.assertEqual(self.parser.calculateMode(), [2])


    def test_standard_deviation(self):
        self.assertEqual(self.parser.calculateStandardDeviation(), 0)

    #def test_frequencies(self):
        #self.assertEqual(self.parser.calculateFrequencies(),{'8441': [2,0.5]})


class InvalidDataTests(TestCase):
    def setUp(self):
        f = open("/home/alex/Documents/Copy of Logs_Course A_StudentsActivities_invalid.xlsx", "rb")
        vv = pandas.read_excel(f)
        self.parser = FileParser.FileParser(vv);
        self.parser.findColsIndexes()
        self.parser.getUsersSubmissions()

    def test_calculate_mode(self):
        print(self.parser.calculateFrequencies()['8411'])
        self.assertEqual(self.parser.calculateMode(), [1])
