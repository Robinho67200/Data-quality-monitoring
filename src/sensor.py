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

                if random.random() <= 0.02:  # 2% failure
                    data["number_visitors"].append(None)
                elif random.random() >= 0.95:  # 5% of improbable data
                    data["number_visitors"].append(random.randint(20, 100) * 0.6)
                else:
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
