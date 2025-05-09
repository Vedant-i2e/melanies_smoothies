import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# App title
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for name
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multiselect for fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Process selected fruits
if ingredients_list:
    ingredients_string = ''
    nutrition_data = []

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # Call API for each fruit
        response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
        fruit_info = response.json()
        nutrition_data.append(fruit_info)

    # Display selected fruit string
    st.write(ingredients_string)

    # Insert order to Snowflake
    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """
    st.write(my_insert_stmt)

    time_to_convert = st.button('Submit Order')

    if time_to_convert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    # Show nutrition data
    sf_df = pd.DataFrame(nutrition_data)
    st.dataframe(sf_df, use_container_width=True)
