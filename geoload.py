import urllib, urllib.error, urllib.request, urllib.parse
import json
import ssl
import mysql.connector
from mysql.connector import errorcode


api_key = False # since I do not have api key for google geocoding, I'll use the altenative from professor's code 
''' If I have api_key, the code will look something like:
api_key = <geocoding api key>
api_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
'''

if api_key is False:
    api_key = 42
    api_url = 'http://py4e-data.dr-chuck.net/json?'
else :
    api_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

#Ignore ssl certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Connect to mysql database
conx = mysql.connector.connect(host = "localhost", user = "harry", password = "NUTTERtools1.")
my_cursor = conx.cursor()


def create_db_table():
	my_cursor.execute('''CREATE DATABASE IF NOT EXISTS geodata''')
	my_cursor.execute("USE geodata")
	my_cursor.execute('''CREATE TABLE IF NOT EXISTS Uni(address_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
															uni_address VARCHAR(200),
															geodata VARCHAR(10000) NOT NULL,
															CONSTRAINT unique_address UNIQUE (uni_address))''')

address_handle = open("address.data")
data = address_handle.read()
create_db_table()
count = 0
for values in data.splitlines():
	print(values)
	try:
		my_cursor.execute("SELECT geodata FROM Uni WHERE uni_address = '%s'", (values,))
		data = my_cursor.fetchone()[0]
		print("Found in database ",address)
		continue
	except:
		pass


	url = api_url + urllib.parse.urlencode({"address":values, "key":api_key})
	url_handle =  urllib.request.urlopen(url)
	data = url_handle.read().decode() 

	my_cursor.execute('''INSERT IGNORE INTO Uni (uni_address, geodata) 
						 VALUES(%s, %s)''',(values.encode(),data.encode()))


conx.commit()
print("Data is now in database")	


#print(data.splitlines()[10])