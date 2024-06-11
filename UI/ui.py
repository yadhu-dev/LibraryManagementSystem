from flask import Flask, render_template, jsonify
import serial
import time
import threading

app = Flask(__name__)

# Initialize the serial connection
ser = serial.Serial('COM5', 115200, timeout=1)

# Global variable to store the last read UID
last_uid = None

def read_rfid():
    global last_uid
    flag = {"ets Jul 29 2019 12:21:46", "rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)", 
            "configsip: 0, SPIWP:0xee", "clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00", 
            "mode:DIO, clock div:1", "load:0x3fff0030,len:1184", "load:0x40078000,len:13260", 
            "load:0x40080400,len:3028", "entry 0x400805e4"}

    while True:
        if ser.in_waiting > 0:
            rfid_tag = ser.readline().strip().decode('utf-8')  # Read and decode the RFID tag
            if any(flag_str in rfid_tag for flag_str in flag):
                continue
            else:
                last_uid = rfid_tag.strip()
                print("\nRead Successfully: " + last_uid)

# Start a background thread to read RFID data
thread = threading.Thread(target=read_rfid)
thread.daemon = True
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_uid')
def get_uid():
    global last_uid
    if last_uid:
        return jsonify({'uid': last_uid})
    else:
        return jsonify({'uid': ''})

if __name__ == '__main__':
    app.run(debug=True)
