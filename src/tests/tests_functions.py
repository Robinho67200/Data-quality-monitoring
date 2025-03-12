import unittest
from pandas import DataFrame
from datetime import datetime
from src.sensor import Visitors

class TestVisitSensor(unittest.TestCase):
    def test_generate_dataframe(self):
        visitors = Visitors()
        self.assertEqual(type(visitors.generate_data("df")), DataFrame)

    def test_generate_dictionary(self):
        visitors = Visitors()
        self.assertEqual(type(visitors.generate_data("dict")), dict)

    def test_number_of_day(self):
        visitors = Visitors()
        nb_day = (datetime.now() - datetime(2020, 1, 1)).days
        df = visitors.generate_data("df")
        nb_day_dataframe = df.groupby("day").count().shape[0]

        self.assertEqual(nb_day, nb_day_dataframe)

    def test_sunday_closed(self):
        visitors = Visitors()
        visit_count = visitors.get_number_visitors("2025-03-02", 10, "Strasbourg")
        self.assertFalse(visit_count)

    def test_day_open(self):
        visitors = Visitors()
        visit_count = visitors.get_number_visitors("2025-03-03", 10, "Strasbourg")
        self.assertEqual(visit_count, 62)

    def test_breakdown(self):
        visitors = Visitors()
        visit_count = visitors.get_number_visitors("2020-01-13", 12, "Strasbourg")
        self.assertTrue(visit_count)
