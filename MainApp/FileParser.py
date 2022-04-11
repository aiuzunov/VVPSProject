import re
import math


class FileParser:
    def __init__(self, excel_table):
        self.cols_dict = {}
        self.excel_table = excel_table
        self.users_submissions_dict = {}
        self.result = {}

    def findColsIndexes(self):
        for index, col_name in enumerate(self.excel_table.columns):
            self.cols_dict[col_name] = index

    def getUsersSubmissions(self):
        for index, row in self.excel_table.iterrows():
            if row[self.cols_dict['Event context']] == 'Assignment: Качване на курсови задачи и проекти' \
                    and row[self.cols_dict['Component']] == 'File submissions' \
                    and row[self.cols_dict['Event name']] == 'Submission created.':
                event_descr = row[self.cols_dict['Description']]
                user_id = re.findall('\'([^\']*)\'', event_descr)[0]
                if user_id in self.users_submissions_dict:
                    self.users_submissions_dict[user_id] += 1
                else:
                    self.users_submissions_dict[user_id] = 1
        return self.users_submissions_dict

    def calculateFrequencies(self):
        frequencies_dict = {}
        total_submissions = sum(self.users_submissions_dict.values())
        for user in self.users_submissions_dict:
            frequencies_dict[user] = []
            frequencies_dict[user].append(self.users_submissions_dict[user])
            frequencies_dict[user].append(self.users_submissions_dict[user] / total_submissions)
        self.result['frequencies'] = frequencies_dict

        return frequencies_dict

    def calculateMode(self):
        dictionary = {}

        for item in self.users_submissions_dict:
            if self.users_submissions_dict[item] in dictionary:
                dictionary[self.users_submissions_dict[item]] += 1
            else:
                dictionary[self.users_submissions_dict[item]] = 1

        max_times = max(dictionary, key=dictionary.get)

        modes = []
        for item in dictionary:
            if item == max_times:
                modes.append(item)

        self.result['modes'] = modes

        return modes

    def calculateStandardDeviation(self):
        values = self.users_submissions_dict.values()
        mean = sum(values) / len(values)
        variance = sum(pow(x - mean, 2) for x in values) / len(values)
        standard_deviation = math.sqrt(variance)

        self.result['standard_deviation'] = standard_deviation

        return standard_deviation

    def getResult(self):
        self.findColsIndexes()
        self.getUsersSubmissions()
        self.calculateFrequencies()
        self.calculateMode()
        self.calculateStandardDeviation()

        return self.result
