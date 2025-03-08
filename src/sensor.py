import random
from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame


def add_data(
    data: dict,
    sensor: str,
    new_day: datetime,
    store: str,
    hour: int,
    coef_improbable_data: float,
    coef_sensor_a: float,
) -> dict:
    """
    Add data to dictionary.
    :param data:
    :param sensor:
    :param new_day:
    :param store:
    :param hour:
    :param coef_improbable_data:
    :param coef_sensor_a:
    :return:
    """
    data["store_name"].append(store)
    data["day"].append(new_day.strftime("%Y-%m-%d"))
    data["hour"].append(hour)

    if random.random() <= 0.05:  # 5% error
        data["id_sensor"].append("null")
    else:
        data["id_sensor"].append(sensor)

    if int(new_day.strftime("%w")) == 0:  # Store close the Sunday
        nb_visitors = "null"
    elif random.random() <= 0.02:  # 2% failure
        nb_visitors = "null"
    elif random.random() >= 0.95:  # 5% of improbable data
        nb_visitors = random.randint(20, 100) * coef_improbable_data
    else:
        nb_visitors = random.randint(20, 100)

    if nb_visitors != "null":
        if sensor == "A":
            nb_visitors = round(nb_visitors * coef_sensor_a, 0)
        else:
            nb_visitors = round(nb_visitors * (1 - coef_sensor_a), 0)

    data["number_visitors"].append(nb_visitors)

    return data


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

        data = {
            "day": [],
            "hour": [],
            "number_visitors": [],
            "id_sensor": [],
            "store_name": [],
        }
        stores = ["Strasbourg", "Metz", "Colmar", "Haguenau"]
        sensors = ["A", "B"]
        for store in stores:
            for i_day in range(nb_days):
                random.seed(i_day)
                new_day = first_day + timedelta(days=i_day)
                for i_hour in range(8, 20):
                    for sensor in sensors:
                        data = add_data(data, sensor, new_day, store, i_hour, 0.6, 0.7)
                        random.random()

        return pd.DataFrame(data)

    def get_number_visitors(self, day: str, hour: int, store: str) -> int:
        """
        Return the number of visitors for an exact day and hour.

        :param day: (str) the day when we want to recover the number of visitors
        :param hour: (int) the hour when we want to recover the number of visitors
        :param store: (str) the store
        :return: Dataframe
        """
        return (
            self.generate_data()
            .query(
                f"day == '{day}' and hour == {hour} and store_name == '{store}' and number_visitors != 'null'"
            )["number_visitors"]
            .sum()
        )

    def get_all_data_day(self, day: str) -> dict:
        """
        Return all the data per day

        :param day: (str) the day when we want to recover the number of visitors
        :return: dict
        """
        data = self.generate_data().query(f"day == '{day}'").to_dict('list')

        return data
