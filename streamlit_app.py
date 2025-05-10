# Import python packages
'''import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Title & description
st.title("Customize your Smoothie!! :balloon:")
st.write("This is test!!!")

# Snowflake connection
cnx = st.connection('snowflake')
session = cnx.session()

# Input name
name_on_order = st.text_input('Name on Smoothie:')

# Load fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'), col('SEARCH_ON')
)
pd_df = my_dataframe.to_pandas()

# Multiselect ingredients
ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:', pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

# If ingredients are selected
if ingredient_list:
    # ✅ Use join to avoid extra spaces
    ingredient_string = ' '.join(ingredient_list)
    
    for fruit_chosen in ingredient_list:
        # Get correct search name for API
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write(f'The search value for {fruit_chosen} is {search_on}.')

        st.subheader(f"{fruit_chosen} : Nutrition Information")
        
        # 🆕 Using SmoothieFroot API
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)

        if smoothiefroot_response.status_code == 200:
            sf_data = smoothiefroot_response.json()
            st.dataframe(data=pd.json_normalize(sf_data), use_container_width=True)
        else:
            st.error("Nutrition information not found for " + fruit_chosen)

    # ✅ Insert with trimmed string
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredient_string}', '{name_on_order}')
    """

    if st.button('Submit Order', type="primary"):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")'''

# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
  """Choose the Fruits You want in your Custom Smoothie
  """
)

# option = st.selectbox(
#     "What is your Favourite Fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("You selected:", option)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name in your Smoothie will be: ", name_on_order)


ingredients_list = st.multiselect('Choose upto 5 Ingredients :', my_dataframe, max_selections=5)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

    st.write(ingredients_string)

     
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('"""\
                + ingredients_string + """','""" + name_on_order + """'
                )"""

    st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!',icon="✅")

