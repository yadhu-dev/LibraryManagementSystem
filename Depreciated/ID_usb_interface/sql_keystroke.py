import mysql.connector
import serial
import pyautogui
import time

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="lms"
)
cursor = mydb.cursor()

# Open the serial port
ser = serial.Serial('COM5', 115200, timeout=1)

# Function for passing the query
def query_database(uid, cursor):
    cursor.execute("SELECT no FROM details WHERE uid = %s", (uid,))
    return cursor.fetchone()

try:
    while True:
        # If data found in serial
        if ser.in_waiting > 0:
            uid = ser.readline().decode('utf-8').strip()
            print(f"Received UID: {uid}")
            # Calling the query function to get roll numbers with the associated UID
            result = query_database(uid, cursor)
            if result:
                roll_number = str(result[0])  # Ensure the roll number is a string
                print(f"Roll number: {roll_number}")

                time.sleep(0.5)

                # Typing the roll number to the focused textbox
                pyautogui.typewrite(roll_number)
                pyautogui.press('enter')
            else:
                print("UID not found in the database.")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close cursor and connection
    cursor.close()
    mydb.close()
    # Close the serial port
    ser.close()
