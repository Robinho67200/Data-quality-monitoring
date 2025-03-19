# Create an application for data quality monitoring. 

## Project objective

- Create and query an API
- Manage data quality
- Detect and resolve data quality issues
- Manipulate data (SQL / Pandas / DuckDB)
- Create a Streamlit visualization app
- Orchestrating Python Scripts with Apache Airflow
  
## Flow diagram

![image](https://github.com/user-attachments/assets/0561514c-a47f-482e-bbce-c5f98911d1b8)


## Explanation of the steps

### sensor.py file

This file generates fictitious data for stores.
The data is created using the random library and several conditions that, for example, increase the number of visitors on Saturdays or during lunch breaks and evenings on weekdays.

The Visitors class contains three methods:
  - generate_data: Generates the data, allowing the choice between a DataFrame or Dictionary output.
  - get_number_visitors: Returns the number of visitors for a given date and time in a store.
  - get_all_data_day: Retrieves all data for a specific day.

### test_functions.py

This file is used to test the code in given scenarios to ensure that modifications do not affect the expected behavior.

Currently, there are six tests:

  - test_generate_dataframe: Ensures that the export is of type DataFrame for the generate_data("df") method.
  - test_generate_dictionary: Ensures that the export is of type Dictionary for the generate_data("dict") method.
  - test_number_of_day: Verifies that the export contains all days from 01/01/2020 up to today.
  - test_sunday_closed: Ensures that there are no visitors on Sundays.
  - test_day_open: Ensures that there are visitors on the opening day.
  - test_breakdown: Checks that the code generates random errors (intentional sensor failures).

### app.py

This file creates the API to make the data accessible to anyone who needs it.

Two routes are defined:

  - /: Sends the number of visitors for a given day.
  - /all_data_day_hour: Sends all data for a specific day and hour.

### request_api.py

This file is used to query the previously created API.

It has two functionalities:
  - It allows querying the API by passing an argument when executing the Python script :
    ```bash
    python3 request_api.py 2025-03-10
    ```
  - If no argument is provided, it collects the data and saves it into a separate file for each month inside the data/raw folder.

### reading_data_csv.py

This file is used to:
  - Collect all files and generate a global file.
  - Analyze the file.
  - Clean the file (removing null and NaN values).
  - Export new tables in .parquet format using SQL queries.

### app_streamlit.py

This file generates the front-end of the Streamlit application to visualize DataFrames and various charts based on the user’s choices (store selection and sensor data).

### dag.py (Airflow)

This file orchestrates data collection and processing using Apache Airflow.
Bash operators are used to execute the request_api.py and reading_data_csv.py Python scripts.

⚠️ Airflow should not execute these tasks locally. In a production environment, Airflow should connect to external servers that handle API calls and store data (e.g., on S3).

## Link
  - Streamlit link : https://data-quality-monitoring.streamlit.app/
  - API link : https://data-quality-monitoring.onrender.com/docs

## Running the Code Locally

### Clone the Repository (SSH)
```bash
git@github.com:Robinho67200/Data-quality-monitoring.git
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the API
  - Step 1: Modify the app.py file and remove src. from `from src.sensor import Visitors` (the src. prefix prevents an error when deploying the API on Render but causes one locally).
  - Step 2 :
```bash
fastapi dev src/app.py
```

### Run the Streamlit App
```bash
streamlit run src/app_streamlit.py
```


## Next Step
  - Cloud data storage
  - Additional dashboards/graphs
  - Run the code on a machine in the cloud rather than locally (e.g., an Amazon EC2)
  - Send an email when there's an alert (a daily value for a sensor that falls below the alert threshold)
  - Add a comparison/alert when a sensor's percentage change is too different from other sensors in the same location for the same date
