void setup() {
  Serial.begin(115200);
  pinMode(13, OUTPUT);
  Serial.println("arduino->pi");
}

void loop() {
  Serial.println("arduino->pi");
  if(Serial.available()){
    flash(Serial.parseInt());
    Serial.flush();
  }
  delay(1000);
}

void flash(int n){
  Serial.print("arduino->pi start");
  Serial.println(n);
  for(int i=0;i<n;i++){
    digitalWrite(13,HIGH);
    delay(500);
    digitalWrite(13,LOW);
    delay(500);
    Serial.println(i+1);
  }
  Serial.println("arduino->pi end");
}
