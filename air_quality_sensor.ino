#include <DHT.h>

// -------- DHT11 --------
#define DHTPIN 6
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// -------- MQ Sensor --------
#define MQ_PIN A0

// -------- PM Sensor --------
#define PM_PIN A1

void setup() {
  Serial.begin(9600);
  dht.begin();

  delay(2000);
}

void loop() {

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  int gasValue = analogRead(MQ_PIN);

  int pmValue = analogRead(PM_PIN);

  if (isnan(humidity) || isnan(temperature)) {

    Serial.println("ERROR,ERROR,ERROR,ERROR");

  } else {

    Serial.print(temperature);
    Serial.print(",");

    Serial.print(humidity);
    Serial.print(",");

    Serial.print(gasValue);
    Serial.print(",");

    Serial.println(pmValue);
  }

  delay(30000);
}
