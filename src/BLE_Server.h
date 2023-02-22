// * Header file for BLE implementation
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define bleServerName "NOAH_ESP32" // BLE server name
#define SERVICE_UUID "91bad492-b950-4226-aa2b-4ede9fa42f59" // https://www.uuidgenerator.net/
#define ACCELERATION_UUID "ca73b3ba-39f6-4ab3-91ae-186dc9577d99"
#define ROLL_UUID "1d710a64-929a-11ed-a1eb-0242ac120002"
#define PITCH_UUID "1d710d8e-929a-11ed-a1eb-0242ac120002"
#define YAW_UUID "1d710f6e-929a-11ed-a1eb-0242ac120002"
#define BUTTON_UUID "1d7110c2-929a-11ed-a1eb-0242ac120002"
#define FSM_UUID "1d7111da-929a-11ed-a1eb-0242ac120002"
#define NOAH_SERVER_UUID "df9f28cb-9b6a-4c8f-a3ff-8f087738c90a"
#define NOAH_UUID = "7bb6db74-6c47-4722-bb33-bfa652f64713"

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

// BLE objects
BLEServer *cueServer;
BLEService *cueService;
BLECharacteristic *accCharacteristic;
BLECharacteristic *rollCharacteristic;
BLECharacteristic *pitchCharacteristic;
BLECharacteristic *yawCharacteristic;
BLECharacteristic *buttonCharacteristic;
BLECharacteristic *fsmCharacteristic;

BLECharacteristic *noahServer;
BLEService *noahService;
BLECharacteristic *noahCharacterisitc;

BLEDescriptor accelerationDescriptor(BLEUUID((uint16_t)0x2903));
BLEDescriptor rollDescriptor(BLEUUID((uint16_t)0x2903));
BLEDescriptor pitchDescriptor(BLEUUID((uint16_t)0x2903));
BLEDescriptor yawDescriptor(BLEUUID((uint16_t)0x2903));
BLEDescriptor buttonDescriptor(BLEUUID((uint16_t)0x2903));
BLEDescriptor fsmDescriptor(BLEUUID((uint16_t)0x2903));

BLEDescriptor(noahDescriptor(BLEUUID((uint16_t)0x2903));

// Function prototypes
void createCharacteristics();
void updateCharacteristic(BLECharacteristic cueCharacteristic, int value);

class MyCharacteristicCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic* pCharacteristic) {
        uint8_t * Data = pCharacteristic->getData();
        Serial.printf("State was set to: %d\n", Data[0]);
  
        //set the characteristic to that char & start service
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
    // FSM State
    //fsmCharacteristic = cueService->createCharacteristic(FSM_UUID,
             //                                        BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_WRITE_NR);
    //fsmDescriptor.setValue("FSM State");
    //fsmCharacteristic->addDescriptor(&fsmDescriptor);

    noahCharacterisitc = noahService->createCharacteristics(NOAH_UUID, BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_WRITE_NR)
    noahDescriptor.setValue("noah descriptor")
    noahCharacterisitc->addDescriptor(&noahDescriptor)
}

// * Set characteristic value and notify client
void updateCharacteristic(BLECharacteristic *cueCharacteristic, int value) {
    // Update and notify
    cueCharacteristic->setValue(value);
    cueCharacteristic->notify();
}