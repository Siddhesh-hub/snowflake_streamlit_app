import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Amoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Let's put a pick list here so het can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table on the page
streamlit.dataframe(fruits_to_show)

#New section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.om/api/fruit/"+ fruit_choice)
    #take the json version of the response and normalize it
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    #output it the screen as table
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()

#font run anthing past here while we trouble shoot 
streamlit.stop()


#Let's put a pick list here so het can pick the fruit they want to include
add_my_fruit = streamlit.multiselect("Which fruit would you like to add?", list(my_data_rows))

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
fruit_advice_to_show = my_fruit_list.loc[add_my_fruit]

#Display the table on the page
streamlit.dataframe(fruit_advice_to_show)

my_cur.execute("Insert into fruit_load_list values ('from streamlit')")

