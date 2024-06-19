import keyboard
import mysql
import mysql.connector
import pyautogui
import time
from flask import Flask, render_template, jsonify, request

scanned_uid = ""

app = Flask(__name__)

# DB creds and initialization
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="tiger",
  database ="lms"
)
mycursor = mydb.cursor()



# Function for passing the query
def query_database(uid, cursor):
    cursor.execute("SELECT no FROM details WHERE uid = %s", (uid,))
    return cursor.fetchone()


# Function to insert data into the database
def insertdata(uid, rollno):
    try:
        while True:
            # Read RFID
            if uid:
                # Taking parameters for the query
                para = (uid, rollno)

                # SQL query for inserting data into table
                sqlinput = "INSERT INTO details (uid, no) VALUES (%s, %s)"
                try:
                    # Inserting data
                    mycursor.execute(sqlinput, para)
                    mydb.commit()
                    print(f"{mycursor.rowcount} record(s) inserted.")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                # Adding a small delay to avoid rapid continuous polling
                time.sleep(1)
    finally:
        # Close cursor and connection
        mycursor.close()
        mydb.close()



# Function to search for a rollno corresponding to the uid
def search_db(uid):
    try:
        print(f"UID received : {uid}")
        result = query_database(uid, mycursor)
        if result:
                roll_number = str(result[0])
                print(f"Roll number: {roll_number}")

                time.sleep(0.5)

                # Typing the roll number to the focused textbox
                # pyautogui.typewrite(roll_number)
                # pyautogui.press('enter')
        else:
            print("UID not found in the database.")

    except Exception as e:
        print(f"Exception raised : {e}")



# Decimal to endian to standard conversion
def comCardDecoder(decimal_number):
    hex_string = format(decimal_number, '08x')

    endian = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    endian.reverse()
    endian = ''.join(endian)

    standard = [endian[i:i+2] for i in range(0, len(endian), 2)]
    standard_format = ' '.join(standard).upper()

    # print(f"\nTo Standard Format: {standard_format}\n")
    return standard_format



# Function to capture RFID UID
def on_key_event(event):
    global scanned_uid
    if event.name == 'enter':
        # Process the scanned UID
        if scanned_uid:
            # Filter out non-digit characters
            UID = "".join(filter(str.isdigit, scanned_uid))

            # Decode UID to standard format and search in database
            decoded_uid = comCardDecoder(int(UID))
            print(f"Scanned UID: {decoded_uid}")

            search_db(decoded_uid)
        # Reset the scanned UID
        scanned_uid = ""

    else:
        scanned_uid += event.name

############################################################
##################### FLASK ENDPOINTS ######################
############################################################



############################################################
#################### FLASK ENDPOINTS END ###################
############################################################

# Hook the keyboard
keyboard.on_press(on_key_event)

# Keep the script running
print("Listening for RFID scans...")
keyboard.wait('esc')  # Press 'esc' to stop the script
