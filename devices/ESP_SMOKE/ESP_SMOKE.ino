// Digital pin 8 will be called 'pin8'
int pin0 = 0;
// Analog pin 0 will be called 'sensor'
int sensor = A0;
// Set the initial sensorValue to 0
int sensorValue = 0;
int digitalValue = 0;

// The setup routine runs once when you press reset
void setup() {
  // Initialize the digital pin 8 as an output
  pinMode(pin0, INPUT);
  // Initialize serial communication at 9600 bits per second
  Serial.begin(115200);
  Serial.println("Start");
}

// The loop routine runs over and over again forever
void loop() {
  // Read the input on analog pin 0 (named 'sensor')
  sensorValue = analogRead(sensor);
  // Print out the value you read
  Serial.println(sensorValue, DEC);
  digitalValue=digitalRead(pin0);
  Serial.println(digitalValue, DEC);
  Serial.flush();
  delay(1000);
  /*
  // If sensorValue is greater than 500
  if (sensorValue > 500) {
    // Activate digital output pin 8 - the LED will light up
    digitalWrite(pin8, HIGH);
  }
  else {
    // Deactivate digital output pin 8 - the LED will not light up
    digitalWrite(pin8, LOW);
  }
  */
}
