from django.test import TestCase
import pandas
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from MainApp import FileParser

ORIGINAL_FILE_PATH = "G:\\Logs_Course A_StudentsActivities.xlsx";
FIRST_SHORT_TEST_FILE_PATH = "G:\\VVPS DOCS\\Copy of Copy of Logs_Course A_StudentsActivities_short.xlsx"
SECOND_SHORT_TEST_FILE_PATH = "G:\\VVPS DOCS\\Copy of Copy of Logs_Course A_StudentsActivities_short_2.xlsx"
INVALID_SECOND_SHORT_TEST_FILE_PATH = "G:\\VVPS DOCS\\Copy of Copy of Logs_Course " \
                                      "A_StudentsActivities_short_2_invalid.xlsx "


# Create your tests here.

class TestDataAnalyzer(TestCase):
    def setUp(self):
        # f = open("/home/alex/Documents/Logs_Course A_StudentsActivities.xlsx", "rb")
        f = open(SECOND_SHORT_TEST_FILE_PATH, "rb")

        vv = pandas.read_excel(f)
        self.parser = FileParser.FileParser(vv);
        self.parser.findColsIndexes()
        self.parser.getUsersSubmissions()

    def testMaxLenFunc(self):
        test_dict = {'test': 2, 'hehe': 2, 'wow': 1, 'wow': 1, 'wow': 1, 'wow': 2, 'wow': 2, 'wow': 2, 'test': 1,
                     "nn": 1}
        self.assertEqual(self.parser.max_all(test_dict, key=test_dict.get), ['hehe', 'wow'])

    def testColsLen(self):
        self.assertEqual(len(self.parser.cols_dict), 5)

    def testModeCalculation(self):
        self.assertEqual(self.parser.calculateMode(), [2, 3, 1])

    def testStandardDeviationCalculation(self):
        self.assertEqual(self.parser.calculateStandardDeviation(), 0.816496580927726)

    def testAbsoluteAndRelativeFreqCalc(self):
        self.assertEqual(self.parser.calculateFrequencies(), {'8411': [2, 0.3333333333333333],
                                                              '8412': [3, 0.5],
                                                              '8415': [1, 0.16666666666666666]})


class InvalidDataTests(TestCase):
    def setUp(self):
        f = open(INVALID_SECOND_SHORT_TEST_FILE_PATH, "rb")
        vv = pandas.read_excel(f)
        self.parser = FileParser.FileParser(vv);
        self.parser.findColsIndexes()

    def testKeyError(self):
        try:
            self.parser.getUsersSubmissions()
            self.assertEqual(0, 1)
        except KeyError:
            self.assertEqual(1, 1)


class FunctionalTests(LiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.selenium = webdriver.Chrome(options=options,
                                         executable_path="G:\\VVPS DOCS\\chromedriver_win32\\chromedriver.exe")
        self.selenium.get('http://localhost:3000/')

    def testResultModeIsCorrect(self):
        file_button = self.selenium.find_element_by_id('formFile')
        file_button.send_keys("G:\\Logs_Course A_StudentsActivities.xlsx")
        submit_button = self.selenium.find_element_by_id("submitFile")
        submit_button.click()
        nav_link = WebDriverWait(self.selenium, 10).until(lambda d: d.find_element_by_id("mode_tab"))
        nav_link.click()
        first_td = self.selenium.find_element_by_css_selector("td")
        self.assertEqual(first_td.text, "1")

    def testIncorrectFileExtensionSubmission(self):
        file_button = self.selenium.find_element_by_id('formFile')
        file_button.send_keys("G:\\VVPS DOCS\\Example_code_review_checklist\\12wi_code_review_checklist.pdf")
        submit_button = self.selenium.find_element_by_id("submitFile")
        submit_button.click()
        error_label = WebDriverWait(self.selenium, 10).until(
            lambda d: d.find_element_by_xpath("//*[@id=\"root\"]/main/div/div/div/div[2]"))
        self.assertEqual(error_label.text, "Error! Expected .xlsx file but got .pdf 😭")

    def testIncorrectFileDataSubmission(self):
        file_button = self.selenium.find_element_by_id('formFile')
        file_button.send_keys("G:\Functional Test Cases.xlsx")
        submit_button = self.selenium.find_element_by_id("submitFile")
        submit_button.click()
        error_label = WebDriverWait(self.selenium, 10).until(
            lambda d: d.find_element_by_xpath("//*[@id=\"root\"]/main/div/div/div/div[2]"))
        self.assertEqual(error_label.text, "Error! The uploaded file doesn't contain the right fields! 😭")
