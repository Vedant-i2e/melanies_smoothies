import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Title and instructions
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Text input
name_on_order = st.text_input("Name on Smothee")
st.write("The name on your smothee will be", name_on_order)

# Connect to Snowflake and get fruit options
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert to Pandas
pd_df = my_dataframe.to_pandas()

# Multiselect - GUI-friendly names
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],
    max_selections=5
)

# Submit logic
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ','  # 👈 comma separator
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # Remove trailing comma
    cleaned_ingredients = ingredients_string.rstrip(',')
    st.write(cleaned_ingredients)

    # Final insert SQL
    my_insert_stmt = f"""
    insert into smoothies.public.orders(ingredients, name_on_order)
    values ('{cleaned_ingredients}','{name_on_order}')
    """
    st.write(my_insert_stmt)

    # Button
    time_to_convert = st.button('submit order')
    if time_to_convert:
        session.sql(my_insert_stmt).collect()
        st.success('✅ Your Smoothie is ordered!', icon="✅")

