import streamlit as st
import duckdb
import pandas as pd
import pathlib
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Data visualization & Data", page_icon="📈")

parent_directory = pathlib.Path(__file__).parent.parent
directory_data = f"{parent_directory}/data"

df = duckdb.read_parquet(f"{directory_data}/filtered.parquet").df()
daily_traffic = duckdb.read_parquet(f"{directory_data}/daily_traffic.parquet").df()

# Mapping des valeurs numériques vers les jours de la semaine
day_mapping = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
}
# Remplacement des valeurs dans le DataFrame
df["day_of_week"] = df["day_of_week"].map(day_mapping)

with st.sidebar:
    store = st.selectbox("Stores ?", df["store_name"].unique())
    sensor = st.selectbox("Sensors ?", df["id_sensor"].unique())
    if sensor and store:
        st.write(f"You selected the sensor {sensor} of the store {store}")



tab1, tab2 = st.tabs(["Data visualization", "Data"])

with tab1:
    st.title("Data visualization")
    # Définir les dates de début et de fin
    start_date = daily_traffic["day"].min().date()
    end_date = daily_traffic["day"].max().date()
    start_date_cursor = end_date - timedelta(90)
    # Ajouter un slider pour la plage de dates
    date_range = st.slider(
        "Select a date range",
        min_value=start_date,
        max_value=end_date,
        value=(start_date_cursor, end_date),
        format="YYYY-MM-DD",
    )

    df = df[(df["id_sensor"] == sensor) & (df["store_name"] == store)]
    df.sort_values("day", ascending=True, inplace=True)

    daily_traffic = daily_traffic[
        (daily_traffic["id_sensor"] == sensor)
        & (daily_traffic["store_name"] == store)
        & (daily_traffic["day"] >= pd.Timestamp(date_range[0]))
        & (daily_traffic["day"] <= pd.Timestamp(date_range[1]))
    ]
    daily_traffic.sort_values("day", ascending=True, inplace=True)

    # Convertir la colonne "day" en string sans les heures
    daily_traffic["day_str"] = daily_traffic["day"].dt.strftime("%Y-%m-%d")

    fig = px.line(
        daily_traffic,
        x="day_str",
        y="number_visitors",
        title=f"Evolution of the number of visits for sensor {sensor} of the {store} store between {date_range[0]} and {date_range[1]}",
        labels={"day_str": "day", "number_visitors": "number of visitors"},
    )
    fig.update_xaxes(type="category")
    st.plotly_chart(fig)

    fig = px.line(
        df,
        x="day",
        y="number_visitors",
        color="day_of_week",
        title=f"Moving average of the last 4 similar days for sensor {sensor} of the {store} store",
        labels={
            "day_str": "day",
            "number_visitors": "number of visitors",
            "day_of_week": "day of week",
        },
    )
    st.plotly_chart(fig)

    now = datetime.now()
    current_month_daily_traffic = daily_traffic.copy()
    current_month_daily_traffic["month"] = current_month_daily_traffic["day"].apply(
        lambda x: x.strftime("%Y-%m")
    )
    current_month_daily_traffic = current_month_daily_traffic[
        current_month_daily_traffic["month"] == now.strftime("%Y-%m")
    ]

    fig = px.line(
        current_month_daily_traffic,
        x="day",
        y="number_visitors",
        title=f"Evolution of the number of visits for sensor {sensor} of the {store} for the current month",
        labels={"day_str": "day", "number_visitors": "number of visitors"},
    )
    st.plotly_chart(fig)

    current_week_daily_traffic = daily_traffic.copy()
    current_week_daily_traffic["week"] = current_week_daily_traffic["day"].apply(
        lambda x: x.strftime("%Y-%U")
    )
    current_week_daily_traffic = current_week_daily_traffic[
        current_week_daily_traffic["week"] == now.strftime("%Y-%U")
    ]

    fig = px.line(
        current_week_daily_traffic,
        x="day",
        y="number_visitors",
        title=f"Evolution of the number of visits for sensor {sensor} of the {store} for the current week",
        labels={"day_str": "day", "number_visitors": "number of visitors"},
    )
    st.plotly_chart(fig)

with tab2:
    st.title("Data")

    st.write(
        f"Moving average of the last 4 similar days for sensor {sensor} of the {store} store"
    )
    st.write(df)
    st.write(
        f"Evolution of the number of visits for sensor {sensor} of the {store} store between {date_range[0]} and {date_range[1]}"
    )
    st.write(daily_traffic)
