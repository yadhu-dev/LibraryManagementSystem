import keyboard

scanned_uid = ""

# Function to capture RFID UID
def on_key_event(event):
    global scanned_uid
    if event.name == 'enter':
        # Process the scanned UID
        if scanned_uid:
            print(f"Scanned UID: {scanned_uid}")
        # Reset the scanned UID
        scanned_uid = ""
    else:
        scanned_uid += event.name

# Hook the keyboard
keyboard.on_press(on_key_event)

# Keep the script running
print("Listening for RFID scans...")
keyboard.wait('esc')  # Press 'esc' to stop the script
