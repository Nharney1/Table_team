// * Header file for BLE implementation
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define bleServerName "NOAH_ESP32" // BLE server name
#define NOAH_SERVER_UUID "df9f28cb-9b6a-4c8f-a3ff-8f087738c90a"
#define NOAH_UUID "7bb6db74-6c47-4722-bb33-bfa652f64713"

bool deviceConnected = false;

// Setup callbacks onConnect and onDisconnect
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* cueServer) {
        Serial.println("Connection established");
        deviceConnected = true;
    }
    void onDisconnect(BLEServer* cueServer) {
        Serial.println("Re-advertising due to disconnect");
        deviceConnected = false;
        cueServer->startAdvertising(); // restart advertising
    }
};

BLEServer *noahServer;
BLEService *noahService;
BLECharacteristic *noahCharacteristic;

BLEDescriptor noahDescriptor(BLEUUID((uint16_t)0x2903));

// Function prototypes
void createCharacteristics();
void updateCharacteristic(BLECharacteristic cueCharacteristic, int value);

class MyCharacteristicCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic* pCharacteristic) {
        uint8_t * Data = pCharacteristic->getData();
        Serial.printf("Got value: %d\n", Data[0]);
  
        //set the characteristic to that char & start service
        int num=3;
        pCharacteristic->setValue(num);
        pCharacteristic->notify();
     }
 };
 
// Function to set up BLE connection
void setupBLE() {

    // Need to call setup in the main ESP call

    // Create the BLE Device
    BLEDevice::init(bleServerName);

    // Create the BLE Server
    noahServer = BLEDevice::createServer();
    noahServer->setCallbacks(new MyServerCallbacks());

    // Create the BLE Service
    noahService = noahServer->createService(NOAH_SERVER_UUID);
    
    // Create BLE Characteristics and Create a BLE Descriptor
    createCharacteristics();

    // Start the service
    noahService->start();

    // Start advertising
    BLEAdvertising *tableAdvertising = BLEDevice::getAdvertising();
    tableAdvertising->addServiceUUID(NOAH_SERVER_UUID);
    BLEDevice::startAdvertising();
    Serial.println("Waiting a client connection to notify...");
}

// Create all BLE characteristics & descriptors
void createCharacteristics() {
    noahCharacteristic = noahService->createCharacteristic(NOAH_UUID, BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_WRITE_NR);
    noahDescriptor.setValue("noah descriptor");
    noahCharacteristic->addDescriptor(&noahDescriptor);
    noahCharacteristic->setCallbacks(new MyCharacteristicCallbacks());
}

// * Set characteristic value and notify client
void updateCharacteristic(BLECharacteristic *cueCharacteristic, int value) {
    // Update and notify
    cueCharacteristic->setValue(value);
    cueCharacteristic->notify();
}