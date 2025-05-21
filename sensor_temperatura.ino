#include <dht11.h>  

#define DHTPIN 2
dht11 DHT11;

#define LEDPIN 10


void setup() {
  Serial.begin(9600);
  pinMode(LEDPIN, OUTPUT);
}

void loop() {
  DHT11.read(DHTPIN);

  Serial.println(DHT11.temperature);

  if (DHT11.temperature > 28) {
    digitalWrite(LEDPIN, HIGH);
  } else {
    digitalWrite(LEDPIN, LOW);
    }
  delay(10000);
}
