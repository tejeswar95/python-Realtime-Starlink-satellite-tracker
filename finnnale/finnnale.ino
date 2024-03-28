#include <SoftwareSerial.h>
#include <TinyGPS++.h>


const int gpsTxPin = 4; 
const int gpsRxPin = 3; 
float latitude=12.93385;
float longitude=77.691874; 


SoftwareSerial gpsSerial(gpsTxPin, gpsRxPin);

TinyGPSPlus gps;

void setup() {
  
  Serial.begin(9600);
  gpsSerial.begin(9600);
 
}

void loop() {
  while (gpsSerial.available() > 0) {
    if (gps.encode(gpsSerial.read())) {
      if (!gps.location.isValid()) {
        Serial.print("Latitude: ");
        Serial.println(latitude,6);
        Serial.print("Longitude: ");
        Serial.println(longitude,6);
      } else {
              Serial.println("No data found");
      }
    }
  }
}
