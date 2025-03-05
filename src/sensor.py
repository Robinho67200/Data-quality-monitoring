import random
from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame


class Visitors:
    """
    Class representing a number of visitors.
    """
    def generate_data(self) -> DataFrame:
        """
        Generate a fictive Dataframe with the number of visitors per day and per hour for
        a store department.
        :return: DataFrame
        """
        today = datetime.now()
        first_day = datetime(2020, 1, 1)
        nb_days = (today - first_day).days

        data = {"day": [], "hour": [], "number_visitors": []}

        for i_day in range(nb_days):
            random.seed(i_day)
            new_day = first_day + timedelta(days=i_day)
            for i_hour in range(8, 20):
                data["day"].append(new_day.strftime("%Y-%m-%d"))
                data["hour"].append(i_hour)
                data["number_visitors"].append(random.randint(20, 100))

        return pd.DataFrame(data)

    def get_number_visitors(self, day: str, hour: int) -> DataFrame:
        """
        Return the number of visitors for an exact day and hour.

        :param day: (str) the day when we want to recover the number of visitors
        :param hour: (int) the hour when we want to recover the number of visitors
        :return: Dataframe
        """
        return self.generate_data().query(f"day == '{day}' and hour == {hour}")

visitors = Visitors()
print(visitors.get_number_visitors("2025-03-04", 17))
