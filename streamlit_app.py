# Import python packages
import streamlit as st

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw: {st.__version__}")

st.write(
    """Choose the fruits you want in your custom smoothie!"""
)


from snowflake.snowpark.functions import col

# Get Snowflake session
session = get_active_session()

# Query table
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))

# Display table
st.dataframe(my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name in your Smoothie will be: ", name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()

# list data type
ingredients_list = st.multiselect(
 'Choose up to 5 ingredients: ',  my_dataframe, max_selections = 5
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ''
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
                    values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    st.write(my_insert_stmt)
    st.stop()
    # time_to_insert=st.button('Submit Order')
    # if time_to_insert:
    #     session.sql(my_insert_stmt).collect()
    #     st.success('Your Smoothie is ordered!', icon="✅")
import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)

