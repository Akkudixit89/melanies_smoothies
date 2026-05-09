# Import python packages
import streamlit as st
import requests

from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

# App title
st.title(f"Customize Your Smoothie! :cup_with_straw: {st.__version__}")

st.write("Choose the fruits you want in your custom smoothie!")

# Get Snowflake session
session = get_active_session()

# Query table
my_dataframe = session.table(
    "SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
).select(col("FRUIT_NAME"))

# Display dataframe
st.dataframe(my_dataframe, use_container_width=True)

# Input for customer name
name_on_order = st.text_input("Name on Smoothie:")

st.write("The name on your Smoothie will be:", name_on_order)

# Convert dataframe column to list
fruit_list = my_dataframe.to_pandas()["FRUIT_NAME"].tolist()

# Multiselect ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Submit order
if ingredients_list:

    ingredients_string = ", ".join(ingredients_list)

    st.write("Ingredients selected:", ingredients_string)

    # Insert query
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders
    (ingredients, name_on_order)
    VALUES
    ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")

# API request
smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

# Show API response
st.write(smoothiefroot_response.json())
