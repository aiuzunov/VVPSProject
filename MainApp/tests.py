from django.test import TestCase
from MainApp import FileParser
# Create your tests here.


class UnitTests(TestCase):
    def setUp(self):
        self.parser = FileParser;
