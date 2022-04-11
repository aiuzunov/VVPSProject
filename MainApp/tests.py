from django.test import TestCase
from MainApp import FileParser
import pandas
# Create your tests here.


class UnitTests(TestCase):
    def setUp(self):
        f = open("/home/alex/Documents/Logs_Course A_StudentsActivities.xlsx", "rb")
        vv = pandas.read_excel(f)
        self.parser = FileParser.FileParser(vv);
        self.parser.findColsIndexes()
        self.parser.getUsersSubmissions()


    def test_cols_len(self):
        self.assertEqual(len(self.parser.cols_dict), 5)


    def test_calculate_mode(self):
        self.assertEqual(self.parser.calculateMode(), [1])


    def test_standard_deviation(self):
        self.assertEqual(self.parser.calculateStandardDeviation(), 0)
