/*****************************************
LoRa test written for UK 868 Mhz band
connecting to the BT Tower, London. 
Sending Payload packets to 'thingsconnected'.
******************************************/

// Include necessary libraries
#include <Arduino.h>
#include <elapsedMillis.h>
#include <avr/pgmspace.h>
#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>
#include "dtostrf.h"

/*
 * How often should data be sent?
 */
#define UpdateInterval 1    // Update every n mins

/*
 * Startup message to send
 */
#define STARTUP_MESSAGE "Pollution Sensor!"
#define TRANSMIT_MESSAGE "This is a transmission..."

/**
 * Sensors to enable
 * Add the remaining sensors Douglas...
 */
#define SENSOR_FEATHER_BATTERY  // Battery Voltage
#define SENSOR_FEATHER_MEMORY   // Free memory

// LoRaWAN Config
// Device Address
devaddr_t DevAddr = 0xD4439A1C;

// Network Session Key
unsigned char NwkSkey[16] = { 0x83, 0xEA, 0x1E, 0x35, 0xCC, 0x9A, 0x3B, 0xB7, 0x8C, 0x7A, 0x47, 0x29, 0x39, 0xDC, 0x9F, 0x0E };
// Application Session Key
unsigned char AppSkey[16] = { 0x74, 0xE3, 0xF0, 0xBF, 0x30, 0x62, 0x23, 0x3A, 0x38, 0xC0, 0x7F, 0xBF, 0x8A, 0xDE, 0xA3, 0x70 };

// Feather M0 RFM9x pin mappings
lmic_pinmap pins = {
  .nss = 8,                 // Internal connected
  .rxen = 0,                // Not used for RFM95
  .txen = 0,                // Not used for RFM95
  .rst = 4,                 // Internal connected
  .dio = {3, 5, 6},         // Connect "i01" to "5"
                            // Connect "D2" to "6"
};

// Track if the current message has finished sending
bool dataSent = false;

/**
 * Device Start Up
 */
void setup() {
    // Startup delay for Serial interface to be ready
    Serial.begin(115200);
    delay(3000);

    // Debug message
    Serial.println("Starting...");

    // Some sensors require a delay on startup
    elapsedMillis sinceStart = 0;
    int sensorReady = 0;

    // Setup LoRaWAN state
    initLoRaWAN();

    // Wait for all the sensors to be ready
    if (sensorReady > sinceStart) {
        // A sensor still needs some time
        delay(max(0, (int)(sensorReady - sinceStart)));
    }

    #if defined(STARTUP_MESSAGE)
        // Send Startup Message
        sendStartupMessage();
        delay(1000);
    #endif

    // Shutdown the radio
    os_radio(RADIO_RST);

    // Debug message
    Serial.println("Startup Complete");
}

void initLoRaWAN() {
    // LMIC init
    os_init();

    // Reset the MAC state. Session and pending data transfers will be discarded.
    LMIC_reset();

    // by joining the network, precomputed session parameters are be provided.
    LMIC_setSession(0x1, DevAddr, (uint8_t*)NwkSkey, (uint8_t*)AppSkey);

    // Enabled data rate adaptation
    LMIC_setAdrMode(1);

    // Enable link check validation
    LMIC_setLinkCheckMode(0);

    // Set data rate and transmit power
    LMIC_setDrTxpow(DR_SF12, 21);
}

void loop() {
    // Start timing how long since starting to send data
    elapsedMillis sinceWake = 0;

    // Debug message
    Serial.println("\nBeginning to send data");

    // Send Transmit message
    #if defined(TRANSMIT_MESSAGE)
        sendTransmitMessage();
        delay(1000);
    #endif

    // Send Battery Voltage
    #if defined(SENSOR_FEATHER_BATTERY)
        sendBattery();
        delay(1000);
    #endif

    // Send Free Memory
    #if defined(SENSOR_FEATHER_MEMORY)
        sendFreeMemory();
        delay(1000);
    #endif

    // Shutdown the radio
    os_radio(RADIO_RST);

    // Output sleep time
    int sleepSeconds = 60 * UpdateInterval;
    sleepSeconds -= sinceWake/1000;
    Serial.print("Sleeping for ");
    Serial.print(sleepSeconds);
    Serial.println(" seconds");
    delay(500); // time for Serial send buffer to clear

    // Actually go to sleep
    signed long sleep = 60000 * UpdateInterval;
    sleep -= sinceWake;
    delay(constrain(sleep, 10000, 60000 * UpdateInterval));
}

/**
 * Send a message with the free memory
 */
#if defined(SENSOR_FEATHER_MEMORY)
extern "C" char *sbrk(int i);
void sendFreeMemory() {
    // Ensure there is not a current TX/RX job running
    if (LMIC.opmode & (1 << 7)) {
        // Something already in the queque
        return;
    }

    // Get the free memory
    char stack_dummy = 0;
    int freeMem = &stack_dummy - sbrk(0);

    // Convert to a string
    char intStr[10];
    itoa(freeMem, intStr, 10);

    // Put together the data to send
    char packet[25] = "Free Memory: ";
    strcat(packet, intStr);

    // Debug message
    Serial.print("  seqno ");
    Serial.print(LMIC.seqnoUp);
    Serial.print(": ");
    Serial.println(packet);

    // Add to the queque
    dataSent = false;
    uint8_t lmic_packet[25];
    strcpy((char *)lmic_packet, packet);
    LMIC_setTxData2(1, lmic_packet, strlen((char *)lmic_packet), 0);

    // Wait for the data to send or timeout after 15s
    elapsedMillis sinceSend = 0;
    while (!dataSent && sinceSend < 15000) {
        os_runloop_once();
        delay(1);
    }
    os_runloop_once();
}
#endif

/**
 * Send a message with the battery voltage
 */
#if defined(SENSOR_FEATHER_BATTERY)
void sendBattery() {
    // Ensure there is not a current TX/RX job running
    if (LMIC.opmode & (1 << 7)) {
        // Something already in the queque
        return;
    }

    // Get the battery voltage
    float measuredvbat = analogRead(A7); // Hard wired to pin A7 on Adafruit Feather
    measuredvbat *= 2;    // we divided by 2, so multiply back
    measuredvbat *= 3.3;  // Multiply by 3.3V, our reference voltage
    measuredvbat /= 1024; // convert to voltage
    //float val = sensor.readTemperature();
    // Convert to a string
    char floatStr[10];
    dtostrf(measuredvbat, 3, 2, floatStr);
    //dtostrf(val, 3, 2, floatStr);


    // Put together the data to send
    char packet[20] = "Battery: ";
    //char packet[20] = "Temp: ";
    strcat(packet, floatStr);

    // Debug message
    Serial.print("  seqno ");
    Serial.print(LMIC.seqnoUp);
    Serial.print(": ");
    Serial.println(packet);

    // Add to the queque
    dataSent = false;
    uint8_t lmic_packet[20];
    strcpy((char *)lmic_packet, packet);
    LMIC_setTxData2(1, lmic_packet, strlen((char *)lmic_packet), 0);

    // Wait for the data to send or timeout after 15s
    elapsedMillis sinceSend = 0;
    while (!dataSent && sinceSend < 15000) {
        os_runloop_once();
        delay(1);
    }
    os_runloop_once();
}
#endif

/**
 * Send a startup message
 */
#if defined(STARTUP_MESSAGE)
void sendStartupMessage() {
    // Ensure there is not a current TX/RX job running
    if (LMIC.opmode & (1 << 7)) {
        // Something already in the queque
        return;
    }

    // Put together the data to send
    char packet[41] = STARTUP_MESSAGE;

    // Debug message
    Serial.print("  seqno ");
    Serial.print(LMIC.seqnoUp);
    Serial.print(": ");
    Serial.println(packet);

    // Add to the queque
    dataSent = false;
    uint8_t lmic_packet[41];
    strcpy((char *)lmic_packet, packet);
    LMIC_setTxData2(1, lmic_packet, strlen((char *)lmic_packet), 0);

    // Wait for the data to send or timeout after 15s
    elapsedMillis sinceSend = 0;
    while (!dataSent && sinceSend < 15000) {
        os_runloop_once();
        delay(1);
    }
    os_runloop_once();
}
#endif

/**
 * Send a startup message
 */
#if defined(TRANSMIT_MESSAGE)
void sendTransmitMessage() {
    // Ensure there is not a current TX/RX job running
    if (LMIC.opmode & (1 << 7)) {
        // Something already in the queque
        return;
    }

    // Put together the data to send
    char packet[41] = TRANSMIT_MESSAGE;

    // Debug message
    Serial.print("  seqno ");
    Serial.print(LMIC.seqnoUp);
    Serial.print(": ");
    Serial.println(packet);

    // Add to the queque
    dataSent = false;
    uint8_t lmic_packet[41];
    strcpy((char *)lmic_packet, packet);
    LMIC_setTxData2(1, lmic_packet, strlen((char *)lmic_packet), 0);

    // Wait for the data to send or timeout after 15s
    elapsedMillis sinceSend = 0;
    while (!dataSent && sinceSend < 15000) {
        os_runloop_once();
        delay(1);
    }
    os_runloop_once();
}
#endif


// LMIC CALLBACKS
// LoRaWAN Application identifier (AppEUI)
static const u1_t AppEui[8] PROGMEM = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

/**
 * Call back to get the AppEUI
 */
void os_getArtEui (u1_t* buf) {
    memcpy(buf, AppEui, 8);
}

/**
 * Call back to get the Network Session Key
 */
void os_getDevKey (u1_t* buf) {
    memcpy(buf, NwkSkey, 16);
}

/**
 * Callback after a LMIC event
 */
void onEvent (ev_t ev) {
    if (ev == EV_TXCOMPLETE) {
        dataSent = true;
    }
    if (ev == EV_LINK_DEAD) {
        initLoRaWAN();
    }
}
