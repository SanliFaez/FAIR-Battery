String Comm;

int output = DAC0;
int input;
int val;
String inData;
String tempValue;
String channel;
int sensorPin = A0;    // select the input pin for the potentiometer
int sensorValue;
bool isData = false;
int i = 0;


void setup() {
  Serial.begin(9600);
  while (!Serial);
  analogWriteResolution(12);
  analogWrite(DAC0, 0);
  analogWrite(DAC1, 0);
  for (i = 2; i <= 13; i++) {
    pinMode(i, OUTPUT);
  }
  for (i = 22; i <= 53; i++) {
    pinMode(i, OUTPUT);
  }
  Serial.flush();
}

void loop() {
  while (Serial.available() > 0 ) {
    char value = Serial.read();
    Comm += value;
    if (value == '\n') {
      isData = true;
    }
  }
  if (isData) {
    isData = false;
    if (Comm.startsWith("IDN")) {
      Serial.print("General DAQ Device built by Uetke. v.1.2019");
      Serial.print("\n");
    }
    else if (Comm.startsWith("OUT")) {
      channel = Comm[6];
      if (channel.toInt() == 1) {
        output = DAC1;
      }
      else if (channel.toInt() == 0) {
        output = DAC0;
      }
      tempValue = "";
      for (i = 8; i < Comm.length(); i++) {
        tempValue += Comm[i];
      }
      val = tempValue.toInt();
      analogWrite(output, val);
      Serial.println(val);
    }
    else if (Comm.startsWith("IN")) {
      channel = Comm[5];
      input = channel.toInt();
      val = analogRead(input);
      Serial.print(val);
      Serial.print("\n");
    }
    else if (Comm.startsWith("DI")) {
      channel = Comm.substring(5, 7);
      input = channel.toInt();
      tempValue = Comm[8];
      val = tempValue.toInt();
      if (val == 0) {
        digitalWrite(input, LOW);
        Serial.println("Setting to LOW");
      }
      else if (val == 1) {
        digitalWrite(input, HIGH);
        Serial.println("Setting to HIGH");
      }
    }
    else {
      Serial.print("Command not known\n");
    }
    Comm = "";
  }
  delay(20);
}
