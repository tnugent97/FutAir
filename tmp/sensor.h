#ifndef _SENSOR_H
#define _SENSOR_H


/**
 * Pin definitions
 */

// CO + NO2 (MiCS-4514 sensor)
#define ANALOG_NO2        3   // Arduino analog pin
#define ANALOG_CO         4   // Arduino analog pin
#define PIN_HEATING_NO2   19  // Arduino digital pin

#define preHeaterON()     digitalWrite(PIN_HEATING_NO2, HIGH);
#define preHeaterOFF()    digitalWrite(PIN_HEATING_NO2, LOW);

#define CALIB_R0_NO2      2200      // R0 calibration value for the NO2 sensor
#define CALIB_R0_CO       750000    // R0 calibration value for the CO sensor

#endif
