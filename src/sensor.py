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

    random_coefficient = random.uniform(0.7, 1.0)
    saturday_coefficient = random.uniform(1.5, 2.0)
    lunchtime_or_evening_coefficient = random.uniform(1.2, 1.4)
    day_of_week = new_day.strftime("%w")

    if random.random() <= 0.05:  # 5% error
        data["id_sensor"].append("null")
    else:
        data["id_sensor"].append(sensor)

    if int(day_of_week) == 6 :  # More customers on Saturday
        nb_visitors = random.randint(20, 100) * saturday_coefficient
    elif hour == 12 or hour >= 18 :  # More customers at lunchtime and evening for the rest of the week
        nb_visitors = (
            random.randint(20, 100)
            * saturday_coefficient
            * lunchtime_or_evening_coefficient
        )
    else:
        nb_visitors = random.randint(20, 100) * random_coefficient

    if int(day_of_week) == 0:  # Store close the Sunday
        nb_visitors = "null"
    elif random.random() <= 0.02:  # 2% failure
        nb_visitors = "null"
    elif random.random() >= 0.95:  # 5% of improbable data
        nb_visitors = (
            random.randint(20, 100) * coef_improbable_data * random_coefficient
        )

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

    def generate_data(self, df_or_dict: str) -> DataFrame | dict:
        """
        Generate a fictive Dataframe with the number of visitors per day and per hour for
        a store department.

        :param df_or_dict: (str) the export type (dataframe or dictionary)
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
        start_random_seed = {"Strasbourg":1, "Metz": 20000, "Colmar":40000, "Haguenau":60000}
        for store in stores:
            for i_day in range(nb_days):
                random.seed(i_day + start_random_seed[store])
                new_day = first_day + timedelta(days=i_day)
                for i_hour in range(8, 20):
                    for sensor in sensors:
                        data = add_data(data, sensor, new_day, store, i_hour, 0.6, 0.7)
                        random.random()
        if df_or_dict == "df":
            return pd.DataFrame(data)
        elif df_or_dict == "dict":
            return data

    def get_number_visitors(self, day: str, hour: int, store: str) -> int:
        """
        Return the number of visitors for an exact day and hour.

        :param day: (str) the day when we want to recover the number of visitors
        :param hour: (int) the hour when we want to recover the number of visitors
        :param store: (str) the store
        :return: Dataframe
        """
        return (
            self.generate_data("df")
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
        data = self.generate_data("dict")
        index = [i for i, d in enumerate(data["day"]) if d == day]
        filtered_data = {
            key: [values[i] for i in index] for key, values in data.items()
        }

        return filtered_data