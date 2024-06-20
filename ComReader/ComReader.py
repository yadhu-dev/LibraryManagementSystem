import mysql.connector
import pyautogui
import time
from flask import Flask, render_template, jsonify, request
from pynput import keyboard
import threading

scanned_uid = ""
hexUID = ""
write_active = False
record_keystrokes = True
listener = None
last_key_time = time.time()
timeout = 0.2

app = Flask(__name__)

# DB creds and initialization
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="tiger",
  database="lms"
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

            time.sleep(0.3)

            return roll_number

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
def on_press(key):
    global scanned_uid
    global hexUID
    global write_active
    global record_keystrokes
    global last_key_time

    current_time = time.time()
    if current_time - last_key_time > timeout:
        scanned_uid = ""
    last_key_time = current_time

    try:
        if key.char and record_keystrokes:
            scanned_uid += key.char
    except AttributeError:
        if key == keyboard.Key.enter:
            if scanned_uid and 8 <= len(scanned_uid) <= 10:  # Assuming UID is 8-10 digits long
                # Filter out non-digit characters
                UID = "".join(filter(str.isdigit, scanned_uid))

                if UID:
                    # Decode UID to standard format and search in database
                    decoded_uid = comCardDecoder(int(UID))
                    hexUID = decoded_uid
                    print(f"Scanned UID: {decoded_uid}")

                    if write_active:
                        # Typing the roll number to the focused textbox
                        pyautogui.press('up')
                        for _ in range(10):
                            pyautogui.press('backspace')
                        roll_number = search_db(hexUID)
                        if roll_number:
                            record_keystrokes = False
                            pyautogui.typewrite(roll_number)
                            pyautogui.press('down')
                            record_keystrokes = True
                # Reset the scanned UID after processing
                scanned_uid = ""

############################################################
##################### FLASK ENDPOINTS ######################
############################################################

# Homepage
@app.route('/')
def index():
    global listener
    if listener is None:
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
    return render_template('index.html')

# UID fetch endpoint
@app.route('/get_uid')
def get_uid():
    global hexUID
    if hexUID:
        return jsonify({'uid': hexUID})
    else:
        return jsonify({'uid': ''})

# Send UID and rollno for database storage
@app.route('/postdata', methods=['POST'])
def postdata():
    data = request.get_json()
    rollno = data.get('rollno', '')
    uid = data.get('uid', '')
    print(f"Received rollno: {rollno}\nReceived UID: {uid}")

    try:
        para = (uid, rollno)
        query = "INSERT INTO details (uid, no) VALUES (%s, %s)"

        mycursor.execute(query, para)
        mydb.commit()
        print(f"{mycursor.rowcount} record(s) inserted.")
        return jsonify({'status': 'success', 'received_rollno': rollno, 'received_uid': uid})

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'status': 'failed', 'received_rollno': rollno, 'received_uid': uid})

# Start and stop keystroke function
@app.route('/keystrokeData', methods=['POST'])
def keystrokeData():
    global write_active

    data = request.get_json()
    counter = data.get('ctr', '')

    if counter == 0:
        write_active = False

        print("Write Stopped")
        print(f"write_active: {write_active}")

        return jsonify({'status': 'stopped'})

    else:
        write_active = True

    print(f"Counter : {counter}")

    return jsonify({'status': 'ended'})

############################################################
#################### FLASK ENDPOINTS END ###################
############################################################

if __name__ == '__main__':
    app.run()
