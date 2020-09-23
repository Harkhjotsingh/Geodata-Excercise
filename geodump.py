import urllib, urllib.error, urllib.request, urllib.parse
import json
import ssl
import mysql.connector
from mysql.connector import errorcode
import codecs


conx = mysql.connector.connect(host = "localhost", user = "harry", password = "NUTTERtools1.")
my_cursor = conx.cursor()
my_cursor.execute("USE geodata")



my_cursor.execute('''SELECT geodata FROM Uni''')
lat_lng_list = []
for rows in my_cursor:
	data = ''.join(rows).encode().decode()
	js_load = json.loads(data)
	try:
		lat = js_load["results"][0]["geometry"]["location"]["lat"]
		lng = js_load["results"][0]["geometry"]["location"]["lng"]
		formatted_address = js_load["results"][0]["formatted_address"]
		formatted_address = formatted_address.replace("'","")
		output = str("["+str(lat)+", "+str(lng)+", "+"'"+str(formatted_address)+"'"+"]")
		print(output)
	except:
		print("+++++++++++++Address retrivel failed+++++++++++++")
		continue
	lat_lng_list.append(output)


file = codecs.open('address_data.js', 'w', encoding="utf-8")
file.write("addData = [\n")
for content in lat_lng_list:
	file.write(content)
	file.write(",\n")

file.write("]; \n")

file.close()
conx.close()