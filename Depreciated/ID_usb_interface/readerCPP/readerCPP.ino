#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 5
#define RST_PIN 22
#define INDICATOR 13
#define BUZZER 12
#define STATUS 2

char card[22];

MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {

    Serial.begin(115200);

    pinMode(INDICATOR, OUTPUT);
    pinMode(STATUS, OUTPUT);
    pinMode(BUZZER, OUTPUT);

    SPI.begin();
    rfid.PCD_Init();
    digitalWrite(STATUS, HIGH);

    // Initialize LEDC peripheral for the buzzer
    ledcSetup(0, 5000, 8); // Channel 0, 5 kHz frequency, 8-bit resolution
    ledcAttachPin(BUZZER, 0); // Attach channel 0 to the buzzer pin
}

void loop()
{
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial())
  {

    // Clear the card array
    memset(card, 0, sizeof(card));

    // Process the UID
    for (byte i = 0; i < rfid.uid.size; i++)
    {
      // Convert each byte to hex and store in the card array
      sprintf(&card[i * 3], "%02X ", rfid.uid.uidByte[i]);
    }

    card[rfid.uid.size * 3 - 1] = '\0';

    // Print the card array for verification
    Serial.println(card);

    // Buzzer and LED indicators
    digitalWrite(INDICATOR, HIGH);
    // Start the tone using LEDC
    ledcWriteTone(0, 698); // Channel 0, frequency 698 Hz
    delay(50);
    digitalWrite(INDICATOR, LOW);
    // Stop the tone
    ledcWriteTone(0, 0);

    // Halt PICC and stop encryption on PCD
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }
}
