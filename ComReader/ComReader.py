import hid
import time

# Replace these with your device's VID and PID
VENDOR_ID = 0x1A86  # example VID
PRODUCT_ID = 0xDD01  # example PID

def read_rfid_uid(buffer_size=64, timeout=5):
    try:
        # Open the HID device
        h = hid.Device(vid=VENDOR_ID, pid=PRODUCT_ID)
    except Exception as e:
        print(f"Failed to open device: {e}")
        return None

    print("Listening for RFID scans...")
    start_time = time.time()
    while True:
        try:
            data = h.read(buffer_size, timeout=1000)  # Timeout set to 1000ms for each read
            if data:
                # Process the received data to extract the UID
                print(f"Raw data: {data}")
                uid = ''.join(chr(i) for i in data if i != 0)
                if uid:
                    h.close()
                    return uid.strip()
            # Check if timeout has been reached
            if time.time() - start_time > timeout:
                print("Timeout reached, no data received")
                break
        except KeyboardInterrupt:
            print("Interrupted by user")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
    h.close()
    return None

def main():
    buffer_sizes = [8, 16, 32, 64, 128]  # Common buffer sizes
    for size in buffer_sizes:
        print(f"Trying buffer size: {size}")
        uid = read_rfid_uid(buffer_size=size)
        if uid:
            print(f"Scanned UID: {uid}")
            break
        else:
            print(f"No data received with buffer size {size}")

if __name__ == "__main__":
    main()
