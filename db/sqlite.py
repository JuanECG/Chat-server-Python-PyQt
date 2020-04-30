import sqlite3
import pandas as pd

connection = sqlite3.connect('names.db')
cursor = connection.cursor()

#cursor.execute('CREATE TABLE names (id INTEGER PRIMARY KEY, fname TEXT, lname TEXT) ') 

read_names = pd.read_csv (r"C:\Users\Juan Esteban\Downloads\names - Sheet1.csv")
read_names.to_sql('names', connection, if_exists='append', index = False)

cursor.execute('SELECT DISTINCT * FROM names ')
   
print(cursor.fetchall())
connection.commit()

