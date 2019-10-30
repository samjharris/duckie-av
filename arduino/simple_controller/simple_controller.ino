long encodersLastSent;


void flash(int n){
  for(int i=0;i<n;i++){
    digitalWrite(13,HIGH);
    delay(50);
    digitalWrite(13,LOW);
    delay(20);
  }
}


void setup() {
  Serial.begin(9600);
  // Serial.begin(115200);
  pinMode(13, OUTPUT);

  encodersLastSent = millis();
}


void loop() {
  // send encoder values to pi
  if(millis() > encodersLastSent + 500) {
    encodersLastSent = millis();

    int leftEncoderValue = -1;
    int rightEncoderValue = -1;

    // send encoder values
    Serial.print(leftEncoderValue);
    Serial.print(" ");
    Serial.print(rightEncoderValue);
    Serial.println();
  }

  // receive motor commands
  int leftMotorValue = Serial.parseInt();
  int rightMotorValue = Serial.parseInt();
  flash(leftMotorValue);

  // TODO: remove this in the final program
  delay(100);
}
