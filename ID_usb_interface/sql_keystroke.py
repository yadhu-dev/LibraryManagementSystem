import serial
import sqlite3
import pyautogui
import time

conn = sqlite3.connect('database')
cursor = conn.cursor()

# Open the serial port
ser = serial.Serial('COM5', 115200, timeout=1)
# must change the static 'COM5' to autodetect

def query_database(uid):
    cursor.execute("SELECT rollno FROM StudentData WHERE uid = ?", (uid,))
    return cursor.fetchone()

while True:
    try:
        if ser.in_waiting > 0:
            uid = ser.readline().decode('utf-8').strip()
            print(f"Received UID: {uid}")
            result = query_database(uid)
            if result:
                roll_number = result[0]
                print(f"Roll number: {roll_number}")

                time.sleep(0.5)

                # Typing the rollnumber to the focused textbox
                pyautogui.typewrite(roll_number)
            else:
                print("UID not found in the database.")
    except Exception as e:
        print(f"Error: {e}")
