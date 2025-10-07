# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

#st.text(smoothiefroot_response.json())
# Write directly to the app
st.title(f"Example Streamlit App :balloon: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

name_on_order = st.text_input('Name on Smoothie : ')
st.write(' the name on your moothie will be : ', name_on_order)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients?",
    my_dataframe
    ,max_selections=5
)
if ingredients_list:
    st.write("You selected:", ingredients_list)
    st.text(ingredients_list)

    ingredients_string=''

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit +' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME']==each_fruit,'SEARCH_ON'].iloc[0]
        st.write('the search value for',each_fruit,' is ',search_on,'.')
        st.subheader(each_fruit+' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        session.sql
        ''




