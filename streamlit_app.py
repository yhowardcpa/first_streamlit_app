import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list =my_fruit_list.set_index('Fruit')


streamlit.title('My parents new healthy diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 OKale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

#🥣 

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#Let's put a pick list here so they can pick the fruit they want to include

#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])


#Display the fruit list  on the page
#streamlit.dataframe(my_data_row)

#put the list of selected fruits into a variable called fruits_selected
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the selected fruit in a table on the page
streamlit.dataframe(fruits_to_show)


#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized


#New section to display FruityVice API response
streamlit.header("Fruityvice Fruit Advice")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
         
         # Normalizes the json response from above
            # The normalized data is now placed in a table
        # return streamlit.dataframe(fruityvice_normalized)
except URLError as e:
   streamlit.error()
   
#we caused an issue so let's not run until we troubleshoot
streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruit Load List contains:")
streamlit.dataframe(my_data_rows)

#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load list values ('from streamlit')")
         return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button ('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]
   back_from_function = insert_row_snowflake(add_my_fruit)
streamlit.text(back_from_function)

#this will not work for now but go for it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")



   

