import mysql.connector
import openpyxl
import random
mydb = mysql.connector.connect(
                host="10.6.84.20",
                user="tms",
                passwd="d41d8cd98f00b204",
                database="tms",
)
mycursor = mydb.cursor()
carrier='圆通药广'
query="SELECT GROUP_CONCAT(code)list from tms_carrier where `name`=%s;"
mycursor.execute(query,(carrier,))
myresult = mycursor.fetchall()
print(myresult,type(myresult))
b=myresult[0]
a = ','.join(b)
print(a,type(a))
