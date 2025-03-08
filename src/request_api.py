import sys
from datetime import datetime, timedelta
import requests
import pandas as pd
import ast
import pathlib

def reset_data_final() -> dict:
    """
    Reset dictionary data_final
    :return: dict
    """
    data_final_reinit = {
        "day": [],
        "hour": [],
        "number_visitors": [],
        "id_sensor": [],
        "store_name": [],
    }
    return data_final_reinit

def add_data(temporary_data: dict, global_data: dict) -> dict:
    """
    Add data to dictionary data_final
    :param temporary_data: dict
    :param global_data: dict
    :return:
    """
    for clef, valeur in temporary_data.items():
        global_data[clef].extend(valeur)

    return global_data

data_final = reset_data_final()

# This condition allows to retrieve data from a specific date by specifying an additional argument when executing the python script.
if len(sys.argv) > 1:
    try:
        date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
        r = requests.get(
            f"http://127.0.0.1:8000/all_data_day_hour?date={date.strftime('%Y-%m-%d')}"
        )
    except ValueError:
        print("Le format de la date n'est pas bon. Voici le format : AAAA-MM-JJ")
# This condition allows to recover all existing data up to today.
else:
    today = datetime.now()
    first_day = datetime(2020, 1, 1)
    nb_days = (today - first_day).days
    for i_day in range(nb_days):
        day = (first_day + timedelta(days=i_day)).strftime("%Y-%m-%d")
        r = requests.get(f"http://127.0.0.1:8000/all_data_day_hour?date={day}")
        data = ast.literal_eval(r.text)
        month_current_day = (first_day + timedelta(days=i_day)).strftime("%Y-%m")

        if len(data_final["day"]) != 0:
            month_dict = data_final["day"][0][:7]
        else:
            month_dict = month_current_day

        if month_dict != month_current_day or i_day == (nb_days - 1):
            df = pd.DataFrame.from_dict(data_final)
            df.to_csv(
                f"{pathlib.Path(__file__).parent.resolve()}/data/raw/{month_dict}.csv"
            )
            data_final = reset_data_final()
            data_final = add_data(data, data_final)

        elif month_dict == month_current_day or len(data_final["day"]) == 0:
            data_final = add_data(data, data_final)
