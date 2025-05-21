const int relePin = 3;

void setup() {
  pinMode(relePin, OUTPUT);
  digitalWrite(relePin, HIGH); // Desliga no início
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');

    if (comando == "ON") {
      digitalWrite(relePin, LOW);
    } else if (comando == "OFF") {
      digitalWrite(relePin, HIGH);
    }
  }
  delay(1000);
}
