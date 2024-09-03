#include <PN5180.h>                                                // Basic functions to control the PN5180 NFC module.
#include <PN5180ISO15693.h>                                        // Support for the ISO15693 protocol

//##############################################################################
// Define the pins used for interfacing with the PN5180 module
//##############################################################################


#define PN5180_NSS  10
#define PN5180_BUSY 9
#define PN5180_RST  7


// Create an object "nfc"
PN5180ISO15693 nfc(PN5180_NSS, PN5180_BUSY, PN5180_RST);

// Buffer to store the combined data for reading
String combinedData = "";

// Command mode
String command = "";

//###################################################################################################################################################
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////       Setup starts here.....     //////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//###################################################################################################################################################

void setup() {
  Serial.begin(115200);
  nfc.begin();                                                             // Initialize PN5180ISO15693
  nfc.reset();                                                             // Reset PN5180ISO15693
  nfc.setupRF();                                                           // Enable RF field
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n');
    command.trim();  
  }

  if (command.equalsIgnoreCase("-")) {
    readRFID();
    if (command.equalsIgnoreCase("_")){
      Serial.println(F("Operation stopped. Awaiting new command."));
      command = "";  
    }
  } else if (command.equalsIgnoreCase(";")) {
    writeRFID();
    if (command.equalsIgnoreCase("_")){
      Serial.println(F("Operation stopped. Awaiting new command."));
      command = "";  
    }
  } else if (command.equalsIgnoreCase("_")) {
    Serial.println(F("Operation stopped. Awaiting new command."));
    command = "";  
  }
}

void readRFID() {
  uint8_t uid[8];
  ISO15693ErrorCode rc = nfc.getInventory(uid);
  if (ISO15693_EC_OK != rc) {
    return;
  }

  uint8_t blockSize, numBlocks;
  rc = nfc.getSystemInfo(uid, &blockSize, &numBlocks);
  if (ISO15693_EC_OK != rc) {
    Serial.print(F("Error in getSystemInfo: "));
    Serial.println(nfc.strerror(rc));
    return;
  }

  uint8_t readBuffer[blockSize];
  combinedData = "";  

  for (int no = 0; no < numBlocks; no++) {
    rc = nfc.readSingleBlock(uid, no, readBuffer, blockSize);
    if (ISO15693_EC_OK == rc) {
      for (int i = 0; i < blockSize; i++) {
        if (readBuffer[i] == 0x23) {  // 0x23 is the hexadecimal value for '#'
          no = numBlocks;  // Exit the outer loop
          break;
        } else {
          combinedData += (char)readBuffer[i];
        }
      }
    } else {
      Serial.print(F("Error in readSingleBlock #"));
      Serial.print(no);
      Serial.print(F(": "));
      Serial.println(nfc.strerror(rc));
      break;
    }
  }

  Serial.print(F("Data : "));
  Serial.println(combinedData);
}

void writeRFID() {
  while (true) {
    uint8_t uid[8];
    ISO15693ErrorCode rc = nfc.getInventory(uid);

    Serial.print(F("Inventory successful, UID="));
    for (int i = 0; i < 8; i++) {
      Serial.print(uid[7 - i], HEX);  
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

    Serial.print(F("Enter data to store: "));
    while (Serial.available() == 0) {}

    String inputData = Serial.readStringUntil('\n');
    inputData.trim(); 

    if(inputData != "_"){

      inputData += "#";  // Add delimiter to the end
      int dataLength = inputData.length();
      int numBlocksRequired = (dataLength + blockSize - 1) / blockSize;

      if (numBlocksRequired > numBlocks) {
        Serial.println(F("Error: Not enough blocks available to store data."));
        return;
      }

      for (int blockIndex = 0; blockIndex < numBlocksRequired; ++blockIndex) {
        uint8_t writeBuffer[blockSize];
        int startIndex = blockIndex * blockSize;
        int endIndex = min(startIndex + blockSize, dataLength);
        int length = endIndex - startIndex;

        for (int i = 0; i < blockSize; ++i) {
          writeBuffer[i] = (i < length) ? inputData[startIndex + i] : 0x00;  // Pad with zeros if input is shorter than block size
        }

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

      // Clear the UID after the operation
      memset(uid, 0, sizeof(uid));
      Serial.println(F("UID cleared after successful operation."));
    }
    else{
      Serial.println(F("Operation stopped. Awaiting new command."));
      command = ""; 
      break;
    }

    delay(2000);
  }
}
