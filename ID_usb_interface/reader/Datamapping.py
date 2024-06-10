import mysql.connector
import serial

ser = serial.Serial('COM5', 115200, timeout=1)

# Function to read RFID tag
def read_rfid():
    print("Place your RFID tag near the reader...")
    rfid_tag = ser.readline().strip().decode('utf-8')  # Read and decode the RFID tag
    return rfid_tag.strip()

#Connecting to database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="tiger",
  database ="lms"
)
mycursor = mydb.cursor()

#Show all Tables
mycursor.execute("SHOW TABLES")
print("\nTable name in database lms")
for x in mycursor:
    print(x)

# Show column names in table details
print("\nColumn names in table details are")
mycursor.execute("SHOW COLUMNS FROM details")
print(mycursor.fetchall())

#taking values 
uid = read_rfid
no = int(input("Enter no (integer): "))
para = (uid, no)

#sql query for inserting data in table
sqlinput = "INSERT INTO details (uid, no) VALUES (%s, %s)"
#inserting data
mycursor.execute(sqlinput, para)
mydb.commit()

#sql query for selecting data from table
mycursor.execute("SELECT * FROM details")
print("\nRows in 'details' table:")
for row in mycursor.fetchall():
    print(row)


mycursor.close()
mydb.close()