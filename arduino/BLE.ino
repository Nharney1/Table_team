// * Header file for BLE implementation
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define bleServerName "TABLE_TEAM_ESP32" // BLE server name
#define TABLE_SERVER_UUID "df9f28cb-9b6a-4c8f-a3ff-8f087738c90a"
#define TABLE_UUID "7bb6db74-6c47-4722-bb33-bfa652f64713"

int ShouldPlaySpeaker = -1;
int NumberOfRemainingArguments = -1;
int Speaker1 = -1;
int Speaker2 = -1;

bool deviceConnected = false;

// Setup callbacks onConnect and onDisconnect
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* tableServer) {
        Serial.println("Connection established");
        deviceConnected = true;
    }
    void onDisconnect(BLEServer* tableServer) {
        Serial.println("Re-advertising due to disconnect");
        deviceConnected = false;
        tableServer->startAdvertising(); // restart advertising
    }
};

// BLE objects
BLEServer *tableServer;
BLEService *tableService;
BLECharacteristic *tableCharacteristic;

BLEDescriptor tableBleDescriptorcriptor(BLEUUID((uint16_t)0x2903));

// Function prototypes
void createCharacteristics();
void updateCharacteristic(BLECharacteristic cueCharacteristic, int value);

class MyCharacteristicCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic* pCharacteristic) {
        uint8_t *Data = pCharacteristic->getData();
        
        if (Data[0] == (uint8_t)100) {
          ShouldPlaySpeaker = -1;
          NumberOfRemainingArguments = 2;
          Serial.printf("Got a command: %d\n", Data[0]);
        }
        else if (NumberOfRemainingArguments == 2 && Data[0] >= (uint8_t)1 && Data[0] <= (uint8_t)12){
          Speaker1 = Data[0];
          NumberOfRemainingArguments = 1;
          Serial.printf("Got speaker1: %d\n", Data[0]);
        }
        else if (NumberOfRemainingArguments == 1 && Data[0] >= (uint8_t)1 && Data[0] <= (uint8_t)12) {
          Speaker2 = Data[0];
          NumberOfRemainingArguments = 0;
          ShouldPlaySpeaker = 1;
          Serial.printf("Got speaker2: %d\n", Data[0]);
        }
        else {
          Serial.printf("Doing nothing, got: %d\n", Data[0]);
        }

        
        //set the characteristic to that char & start service
        //int num=3;
        //pCharacteristic->setValue(num);
        //pCharacteristic->notify();
     }
 };
 
// Function to set up BLE connection
void setupBLE() {

  // Need to call setup in the main ESP call

    // Create the BLE Device
    BLEDevice::init(bleServerName);

    // Create the BLE Server
    tableServer = BLEDevice::createServer();
    tableServer->setCallbacks(new MyServerCallbacks());

    // Create the BLE Service
    tableService = tableServer->createService(TABLE_SERVER_UUID);
    
    // Create BLE Characteristics and Create a BLE Descriptor
    createCharacteristics();

    // Start the service
    tableService->start();

    // Start advertising
    BLEAdvertising *tableAdvertising = BLEDevice::getAdvertising();
    tableAdvertising->addServiceUUID(TABLE_SERVER_UUID);
    BLEDevice::startAdvertising();
    Serial.println("Waiting a client connection to notify...");
}

// Create all BLE characteristics & descriptors
void createCharacteristics() {
    tableCharacteristic = tableService->createCharacteristic(TABLE_UUID, BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_WRITE_NR);
    tableBleDescriptorcriptor.setValue("table descriptor");
    tableCharacteristic->addDescriptor(&tableBleDescriptorcriptor);
    tableCharacteristic->setCallbacks(new MyCharacteristicCallbacks());
}

// * Set characteristic value and notify client
void updateCharacteristic(BLECharacteristic *cueCharacteristic, int value) {
    // Update and notify
    cueCharacteristic->setValue(value);
    cueCharacteristic->notify();
}

void SendCommandToNano(BLECharacteristic *channel, int command) {
    channel->setValue(command);
    channel->notify();

    // Calling convention is:
    // SendCommandToNano(tableCharacteristic, command);
}

void setup() {
  Serial.begin(115200);
  Serial.println("Beginning");
  setupBLE();
}

void loop() {
  if (ShouldPlaySpeaker == 1) {
    Serial.printf("Playing speaker %d and %d\n", Speaker1, Speaker2);
    delay(1000);
  }

}
