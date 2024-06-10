#include <SPI.h>
#include <MFRC522.h>

// RFID pins on ESP32 Devkit V1
#define SS_PIN 5
#define RST_PIN 22

// Create an MFRC522 instance
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup()
{
    // Create a serial instance
    Serial.begin(115200);
    SPI.begin();
    mfrc522.PCD_Init();
    Serial.println("Tap the ID card on the RFID reader...");
}

void loop()
{
    // Listen for RFID tags/ ID cards
    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial())
    {
        delay(50);
        return;
    }

    String uid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++)
    {
        // Formatting the byte output and storing it in the UID variable
        uid += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
        uid += String(mfrc522.uid.uidByte[i], HEX);
    }
    uid.toUpperCase();

    Serial.println(uid);

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();

    delay(1000);
}
