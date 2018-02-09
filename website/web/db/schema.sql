
CREATE TABLE datapoints (
  id            INTEGER PRIMARY KEY,
  nickname      VARCHAR,
  lat           DECIMAL,
  lng           DECIMAL,
  temp          DECIMAL,
  humidity      DECIMAL,
  CO_conc       DECIMAL,
  NO2_conc      DECIMAL,
  pressure      DECIMAL,
  device_time   DATETIME DEFAULT CURRENT_TIMESTAMP,
  created       DATETIME DEFAULT CURRENT_TIMESTAMP
);
