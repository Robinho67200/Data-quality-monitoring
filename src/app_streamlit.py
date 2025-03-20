import streamlit as st
import pathlib

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

parent_directory = pathlib.Path(__file__).parent
directory_data = f"{parent_directory}/data"

st.title("Data quality monitoring for stores")

st.image(f"{parent_directory}/images/shop.jpg")

st.title("Project objective")

st.markdown(
    """
- Create and query an API
- Manage data quality
- Detect and resolve data quality issues
- Manipulate data (SQL / Pandas / DuckDB)
- Create a Streamlit visualization app
- Orchestrating Python Scripts with Apache Airflow
"""
)