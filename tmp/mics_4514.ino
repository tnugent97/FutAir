#include "Arduino.h"
#include "sensor.h"

void setup()
{
  // MiCS-4514 sensor
  pinMode(PIN_HEATING_NO2, OUTPUT);   // Configure pre-heating pin as output
  preHeaterON();
  delay(30000);
  preHeaterOFF();
  Serial.begin(9600);
}

/**
 * sensor_ReadMics4514
 *
 * Read CO and NO2 levels from MiCS-4514 sensor
 *
 * Return -1 in case of error. Return 0 otherwise
 */
int sensor_ReadMics4514(void)
{
  unsigned int reading;
  unsigned long calib;
  float fVolt, fRes, fConc;

  /**
   * Read CO sensor
   */
  reading = analogRead(ANALOG_CO);
  // Convert reading to voltage (Volts)
  fVolt = (reading * 3.3) / 1024.0;
  // Get Rs/R0 value
  calib = CALIB_R0_CO;
  fRes = (5000.0/fVolt - 1000) / calib;

  // Convert to ppm
  if (fRes > 0.7)
    fRes = 0.7;
  if (fRes > 0.6)
    fConc = (0.711 - fRes) / 0.011;
  else if (fRes > 0.3)
    fConc = (0.7 - fRes) / 0.01;
  else
    fConc = (0.3233 - fRes) / 0.00058;

  reading = fConc;
  Serial.println(reading);

  /**
   * Read NO2 sensor
   */

  reading = analogRead(ANALOG_NO2);
  // Convert reading to voltage (Volts)
  fVolt = 3.3;
  fVolt *= reading;
  fVolt /= 1024.0;

  // Get Rs/R0 value
  calib = CALIB_R0_NO2;

  fRes = (5000.0/fVolt - 1000) / calib;

  // Convert to ppm
  if (fRes < 3.0)
    fRes = 3.0;
  if (fRes >= 3.0 && fRes < 8.0)
    fConc = (fRes - 0.5) / 0.25;
  else
    fConc = (fRes + 129.655) / 4.589;

  reading = fConc;
Serial.println(reading);
}

/**
 * initSensor
 *
 * Initialize sensor pins
 */

void loop()
{
  sensor_ReadMics4514();
  delay(5000);
}
