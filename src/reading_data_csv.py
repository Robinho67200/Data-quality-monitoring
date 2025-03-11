import re
import pandas as pd
import pathlib
import glob
import duckdb

parent_directory = pathlib.Path(__file__).parent
directory_csv_files = f"{parent_directory}/data/raw/*.csv"
list_files_csv = glob.glob(directory_csv_files)

content = []
for directory in list_files_csv:
    df = pd.read_csv(directory)
    content.append(df)

df = pd.concat(content).reset_index()
df = df.drop(columns=["index", "Unnamed: 0"], axis=1)
df.to_csv((f"{parent_directory}/data/all.csv"))

# Step 1 : Data analysis
"""
Verification of columns types :
day : Check if we have only date formats by converting to date format
hour : Check that we only have store opening hours (8am to 7pm) and the format (int)
number_visitors : float
id_sensor : Check the number of sensors
store_name : Check the number of stores
"""
# 1.1 : Display the types of the columns
print(df.dtypes)
print("-" * 100)
columns = df.columns
for column in columns:
    number_nan = df[column].isna().sum()
    print(f"We have {number_nan} lines with a NaN value in a column {column}")

print("If we remove all the Nan lines, we rest ")
print("-" * 100)

# 1.2 : Checking the date column format
try:
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    df["day"].apply(lambda x: re.match(pattern, x))
    print("The format of date is correct")
except TypeError:
    print("date format error")
print("-" * 100)

# 1.3 : Check that we only have store opening hours (8am to 7pm) and the format (int)
verification_hour = df.query("hour <8 | hour > 19")["hour"].count()

if verification_hour == 0:
    print("There are no values with hour < 8 or hour > 19.")
else:
    print(
        f"There are {verification_hour} values corresponding to hour < 8 or hour > 19."
    )
print("-" * 100)

# 1.5 : id_sensor : Check the number of sensors
print(df["id_sensor"].value_counts().to_dict().keys())
print("-" * 100)

# 1.6 : store_name : Check the number of stores
print(df["store_name"].value_counts().to_dict().keys())
print("-" * 100)

# Step 2 : Data Cleaning

# 2.1 : Remove all the line with a Nan Value
for column in columns:
    df = df[df[column].isna() == False]

# 2.2 : Check that NaNs are removed
for column in columns:
    number_nan = df[column].isna().sum()
    print(f"We have {number_nan} lines with a NaN value in a column {column}")

print("-" * 100)

# Step 3 : Data processing

# 3.1 : Get daily traffic by day, store and sensor
q = """
SELECT CAST(day AS DATETIME) AS day,
store_name,
id_sensor,
SUM(number_visitors) AS number_visitors
FROM df
GROUP BY (day, store_name, id_sensor)
"""

duckdb.sql(q).show()
df2 = duckdb.sql(q).df()
df2.to_parquet(f"{parent_directory}/data/daily_traffic.parquet")

# 3.2 : Average number of visitors over the last 4 same days of the week per store and sensor
q = """
WITH four_last_day_of_week AS (
SELECT
day,
number_visitors,
store_name,
id_sensor,
DAYOFWEEK(CAST(day AS DATETIME)) AS day_of_week,
DENSE_RANK() OVER(PARTITION BY day_of_week, store_name, id_sensor ORDER BY day DESC) AS number_of_day
FROM df2
QUALIFY number_of_day <= 4
)

SELECT
day,
number_visitors,
store_name, id_sensor,
DAYOFWEEK(CAST(day AS DATETIME)) AS day_of_week,
AVG(number_visitors) OVER(PARTITION BY day_of_week, store_name, id_sensor ORDER BY day) AS moving_average
FROM four_last_day_of_week
"""

duckdb.sql(q).show(max_width=250, max_rows=10)

df3 = duckdb.sql(q)

# 3.3 : Measure the percentage change of the moving average per day of week
q = """
SELECT *,
LAG(moving_average) OVER(PARTITION BY day_of_week, store_name, id_sensor) AS average_last_day,
(moving_average - average_last_day) // average_last_day AS pct_change
FROM df3
"""

duckdb.sql(q).show(max_width=250, max_rows=50)

# Step 4 : Export results in .parquet format
filtered = duckdb.sql(q)
filtered.to_parquet(f"{parent_directory}/data/filtered.parquet")
