#include <PN5180.h>                                                // Basic functions to control the PN5180 NFC module.
#include <PN5180ISO15693.h>                                        // Support for the ISO15693 protocol

//##############################################################################
// Define the pins used for interfacing with the PN5180 module
//##############################################################################

#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_MEGA2560) || defined(ARDUINO_AVR_NANO)  // If using Arduino UNO, Arduino MEGA, Arduino NANO

#define PN5180_NSS  10
#define PN5180_BUSY 9
#define PN5180_RST  7

#elif defined(ARDUINO_ARCH_ESP32)    // Else if using ESP32

#define PN5180_NSS  16
#define PN5180_BUSY 5
#define PN5180_RST  17

#else
#error Please define your pinout here!
#endif

// Create an object "nfc"
PN5180ISO15693 nfc(PN5180_NSS, PN5180_BUSY, PN5180_RST);

//###################################################################################################################################################
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////       Setup starts here.....     //////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//###################################################################################################################################################

void setup() {
  Serial.begin(115200);
  Serial.println(F("=================================="));
  Serial.println(F("PN5180 ISO15693 Write Block Example"));

  nfc.begin();                                                             // Initialize PN5180ISO15693
  nfc.reset();                                                             // Reset PN5180ISO15693
  nfc.setupRF();                                                           // Enable RF field

  Serial.println(F("----------------------------------"));
  Serial.println(F("Initialization complete. Ready to write data to block."));
}


void loop() {
  uint8_t uid[8];
  ISO15693ErrorCode rc = nfc.getInventory(uid);
  if (ISO15693_EC_OK != rc) {
    Serial.print(F("Error in getInventory: "));
    Serial.println(nfc.strerror(rc));
    return;
  }

  Serial.print(F("Inventory successful, UID="));
  for (int i = 0; i < 8; i++) {
    Serial.print(uid[7 - i], HEX); // LSB is first
    if (i < 7) Serial.print(":");
  }
  Serial.println();

  uint8_t blockSize, numBlocks;
  rc = nfc.getSystemInfo(uid, &blockSize, &numBlocks);
  if (ISO15693_EC_OK != rc) {
    Serial.print(F("Error in getSystemInfo: "));
    Serial.println(nfc.strerror(rc));
    return;
  }

  Serial.println(F("----------------------------------"));
  Serial.print(F("Enter data to store: "));

  // Wait for user input
  while (Serial.available() == 0) {}

  // Read the input data
  String inputData = Serial.readStringUntil('\n');
  inputData.trim();  // Remove any trailing newlines or spaces

  // Add delimiter and calculate total length including delimiters
  inputData += "#";  // Add delimiter to the end
  int dataLength = inputData.length();
  int numBlocksRequired = (dataLength + blockSize - 1) / blockSize; // Calculate number of blocks required

  if (numBlocksRequired > numBlocks) {
    Serial.println(F("Error: Not enough blocks available to store data."));
    return;
  }

  // Write data to blocks
  for (int blockIndex = 0; blockIndex < numBlocksRequired; ++blockIndex) {
    uint8_t writeBuffer[blockSize];
    int startIndex = blockIndex * blockSize;
    int endIndex = min(startIndex + blockSize, dataLength);
    int length = endIndex - startIndex;
    
    // Fill buffer with data from inputData
    for (int i = 0; i < blockSize; ++i) {
      if (i < length) {
        writeBuffer[i] = inputData[startIndex + i];
      } else {
        writeBuffer[i] = 0x00;  // Pad with zeros if input is shorter than block size
      }
    }

    // Write the data to the current block
    rc = nfc.writeSingleBlock(uid, blockIndex, writeBuffer, blockSize);
    if (ISO15693_EC_OK != rc) {
      Serial.print(F("Error in writeSingleBlock "));
      Serial.print(blockIndex);
      Serial.print(F(": "));
      Serial.println(nfc.strerror(rc));
      return;
    }
    
    Serial.print(F("Data written to block #"));
    Serial.print(blockIndex);
    Serial.println(F(" successfully."));
  }

  // Read back the data to confirm
  for (int blockIndex = 0; blockIndex < numBlocksRequired; ++blockIndex) {
    uint8_t readBuffer[blockSize];
    rc = nfc.readSingleBlock(uid, blockIndex, readBuffer, blockSize);
    if (ISO15693_EC_OK == rc) {
      Serial.print(F("Data in block #"));
      Serial.print(blockIndex);
      Serial.print(F(": "));
      for (int i = 0; i < blockSize; i++) {
        Serial.print((char)readBuffer[i]);
      }
      Serial.println();
    } else {
      Serial.print(F("Error in readSingleBlock "));
      Serial.print(blockIndex);
      Serial.print(F(": "));
      Serial.println(nfc.strerror(rc));
    }
  }

  delay(5000);  // Delay before next loop iteration
}
