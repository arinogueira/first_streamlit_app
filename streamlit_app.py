import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
#streamlit.dataframe(my_fruit_list) / old exercise
streamlit.dataframe(fruits_to_show)
#Let's Call the Fruityvice API from Our Streamlit App!

#create the repeatable code block (called function)
def get_fruityvice_data(this_fruit_choice):
  # streamlit.text(fruityvice_response.json()) # just writes the data to screen - "deleted" as per exercice line 32 below
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  # take the json version of the response and normalize it
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  # output it the screen as a table
  return fruityvice_normalized
#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  # removed -> streamlit.write('The user entered', fruit_choice)   
  if not fruit_choice:
      streamlit.error("Please select a fruit go get information.")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      # output it the screen as a table
      streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()
       
# Let's removed the line of raw JSON, and separate the base URL from the fruit name (which will make it easier to use a variable there).
#Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call

streamlit.header ("View Our Fruit List - Add your Favorites!")
#Snowflake-related fucntions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
       my_cur. execute("SELECT * from fruit_load_list")
       return my_cur.fetchall()
 #add a button to laod the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list() 
  my_cns.close()
  streamlit.dataframe (my_data_rows)

#Allow user to add a fruit to the list. 
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
       my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")    
       return 'Thanks for adding ' + new_fruit
    
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.write(back_from_function)


#don't run anything past here while we troubleshoot
streamlit.stop()
