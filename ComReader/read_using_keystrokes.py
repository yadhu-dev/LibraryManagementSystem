import keyboard
import mysql
import mysql.connector
import pyautogui
import time

scanned_uid = ""

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
            # print(f"Scanned UID: {scanned_uid}")
            print(f"Scanned UID: {comCardDecoder(int(scanned_uid))}")
            search_db(comCardDecoder(int(scanned_uid)))
        # Reset the scanned UID
        scanned_uid = ""
    else:
        scanned_uid += event.name

# Hook the keyboard
keyboard.on_press(on_key_event)

# Keep the script running
print("Listening for RFID scans...")
keyboard.wait('esc')  # Press 'esc' to stop the script
