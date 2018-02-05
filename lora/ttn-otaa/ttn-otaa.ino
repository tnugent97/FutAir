/*******************************************************************************
DeviceEUI
3F46D353552210C9
{ 0x00, 0x3B, 0xDA, 0x17, 0x14, 0xDC, 0x43, 0xFA }


Application key
67DCD999661D569FF209602FA0C10F52
{ 0x0C, 0x10, 0x1E, 0xF1, 0x38, 0x8A, 0x74, 0x45, 0xB2, 0x1E, 0x24, 0x4B, 0x3E, 0x31, 0xBF, 0x0E }

Application EUI (Sandbox)
97feda62e40303ba
{ 0x70, 0xB3, 0xD5, 0x7E, 0xD0, 0x00, 0x9E, 0x3A }
 *******************************************************************************/

#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>

// This EUI must be in little-endian format, so least-significant-byte
// first. When copying an EUI from ttnctl output, this means to reverse
// the bytes. For TTN issued EUIs the last bytes should be 0xD5, 0xB3,
// 0x70.
static const u1_t PROGMEM APPEUI[8]={ 0x70, 0xB3, 0xD5, 0x7E, 0xD0, 0x00, 0x9E, 0x3A };

//static const u1_t PROGMEM APPEUI[8]={ 0x97, 0xFE, 0xDA, 0x62, 0xE4, 0x03, 0x03, 0xBA };
void os_getArtEui (u1_t* buf) { memcpy_P(buf, APPEUI, 8);}

// This should also be in little endian format, see above.
static const u1_t PROGMEM DEVEUI[8]={ 0x00, 0x3B, 0xDA, 0x17, 0x14, 0xDC, 0x43, 0xFA };

//static const u1_t PROGMEM DEVEUI[8]={ 0x3F, 0x46, 0xD3, 0x53, 0x55, 0x22, 0x10, 0xC9 };
void os_getDevEui (u1_t* buf) { memcpy_P(buf, DEVEUI, 8);}

// This key should be in big endian format (or, since it is not really a
// number but a block of memory, endianness does not really apply). In
// practice, a key taken from ttnctl can be copied as-is.
// The key shown here is the semtech default key.
static const u1_t PROGMEM APPKEY[16] = { 0x0C, 0x10, 0x1E, 0xF1, 0x38, 0x8A, 0x74, 0x45, 0xB2, 0x1E, 0x24, 0x4B, 0x3E, 0x31, 0xBF, 0x0E };

//static const u1_t PROGMEM APPKEY[16] = { 0x67, 0xDC, 0xD9, 0x99, 0x66, 0x1D, 0x56, 0x9F, 0xF2, 0x09, 0x60, 0x2F, 0xA0, 0xC1, 0x0F, 0x52 };
void os_getDevKey (u1_t* buf) {  memcpy_P(buf, APPKEY, 16);}

static uint8_t mydata[] = "Hello, world!";
static osjob_t sendjob;

// Schedule TX every this many seconds (might become longer due to duty
// cycle limitations).
const unsigned TX_INTERVAL = 60;

// Pin mapping
//const lmic_pinmap lmic_pins = {
//    .nss = 6,
//    .rxtx = LMIC_UNUSED_PIN,
//    .rst = 5,
//    .dio = {2, 3, 4},
//};

const lmic_pinmap lmic_pins = {
  .nss = 8, // change to match cs / nss
  .rxtx = LMIC_UNUSED_PIN,
  .rst = LMIC_UNUSED_PIN, // possible 4 for the adafruit board
  .dio = {5, 6, 11}, // DIO0, DIO1, DIO2 data pins
};

void onEvent (ev_t ev) {
    Serial.print(os_getTime());
    Serial.print(": ");
    switch(ev) {
        case EV_SCAN_TIMEOUT:
            Serial.println(F("EV_SCAN_TIMEOUT"));
            break;
        case EV_BEACON_FOUND:
            Serial.println(F("EV_BEACON_FOUND"));
            break;
        case EV_BEACON_MISSED:
            Serial.println(F("EV_BEACON_MISSED"));
            break;
        case EV_BEACON_TRACKED:
            Serial.println(F("EV_BEACON_TRACKED"));
            break;
        case EV_JOINING:
            Serial.println(F("EV_JOINING"));
            break;
        case EV_JOINED:
            Serial.println(F("EV_JOINED"));

            // Disable link check validation (automatically enabled
            // during join, but not supported by TTN at this time).
            LMIC_setLinkCheckMode(0);
            break;
        case EV_RFU1:
            Serial.println(F("EV_RFU1"));
            break;
        case EV_JOIN_FAILED:
            Serial.println(F("EV_JOIN_FAILED"));
            break;
        case EV_REJOIN_FAILED:
            Serial.println(F("EV_REJOIN_FAILED"));
            break;
            break;
        case EV_TXCOMPLETE:
            Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
            if (LMIC.txrxFlags & TXRX_ACK)
              Serial.println(F("Received ack"));
            if (LMIC.dataLen) {
              Serial.println(F("Received "));
              Serial.println(LMIC.dataLen);
              Serial.println(F(" bytes of payload"));
            }
            // Schedule next transmission
            os_setTimedCallback(&sendjob, os_getTime()+sec2osticks(TX_INTERVAL), do_send);
            break;
        case EV_LOST_TSYNC:
            Serial.println(F("EV_LOST_TSYNC"));
            break;
        case EV_RESET:
            Serial.println(F("EV_RESET"));
            break;
        case EV_RXCOMPLETE:
            // data received in ping slot
            Serial.println(F("EV_RXCOMPLETE"));
            break;
        case EV_LINK_DEAD:
            Serial.println(F("EV_LINK_DEAD"));
            break;
        case EV_LINK_ALIVE:
            Serial.println(F("EV_LINK_ALIVE"));
            break;
         default:
            Serial.println(F("Unknown event"));
            break;
    }
}

void do_send(osjob_t* j){
    // Check if there is not a current TX/RX job running
    if (LMIC.opmode & OP_TXRXPEND) {
        Serial.println(F("OP_TXRXPEND, not sending"));
    } else {
        // Prepare upstream data transmission at the next possible time.
        LMIC_setTxData2(1, mydata, sizeof(mydata)-1, 0);
        Serial.println(F("Packet queued"));
    }
    // Next TX is scheduled after TX_COMPLETE event.
}

void setup() {
    Serial.begin(9600);
    Serial.println(F("Starting"));

    #ifdef VCC_ENABLE
    // For Pinoccio Scout boards
    pinMode(VCC_ENABLE, OUTPUT);
    digitalWrite(VCC_ENABLE, HIGH);
    delay(1000);
    #endif

    // LMIC init
    os_init();
    // Reset the MAC state. Session and pending data transfers will be discarded.
    LMIC_reset();
    LMIC_setClockError(MAX_CLOCK_ERROR * 1 / 100);

    // Start job (sending automatically starts OTAA too)
    do_send(&sendjob);
}

void loop() {
    os_runloop_once();
}
