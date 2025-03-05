import unittest

import numpy as np
from pandas import DataFrame
from src.sensor import Visitors
from datetime import datetime


class TestVisitSensor(unittest.TestCase):
    def test_generate_dataframe(self):
        visitors = Visitors()
        self.assertEqual(type(visitors.generate_data()), DataFrame)

    def test_number_of_day(self):
        visitors = Visitors()
        nb_day = (datetime.now() - datetime(2020, 1, 1)).days
        df = visitors.generate_data()
        nb_day_dataframe = df.groupby("day").count().shape[0]

        self.assertEqual(nb_day, nb_day_dataframe)

    def test_sunday_closed(self):
        visitors = Visitors()
        visit_count = visitors.get_number_visitors("2025-03-02", 10)
        self.assertTrue(visit_count)

    def test_day_open(self):
        visitors = Visitors()
        visit_count = visitors.get_number_visitors("2025-03-03", 10)
        self.assertEqual(visit_count, 72)

    def test_breakdown(self):
        visitors = Visitors()
        visit_count = visitors.get_number_visitors("2020-01-13", 12)
        print(f"visit count : {visit_count}")
        self.assertTrue(visit_count)

# git commit -m "Add 4 tests with unitest (test_generate_dataframe, test_number_of_day, test_sunday_closed, test_day_open"
