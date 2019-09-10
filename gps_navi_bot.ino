#include <TinyGPS++.h>
#include <SoftwareSerial.h>

static const int RXPin = 3, TXPin = 4;
static const uint32_t GPSBaud = 9600;

TinyGPSPlus gps;
SoftwareSerial ss(RXPin, TXPin);

float destinationLat = 12.0;
float destinationLong = 80.0;

void setup()
{
  Serial.begin(115200);
  ss.begin(GPSBaud);

  pinMode(5, OUTPUT); //1 left
  pinMode(6, OUTPUT); //1 left
  pinMode(7, OUTPUT); //2
  pinMode(8, OUTPUT); //2
}

float dist_angle(float destinationLat, float destinationLong)
{
  Serial.print("Location : ");
  Serial.print(gps.location.lat());
  Serial.print(" , ");
  Serial.print(gps.location.lng());

  float lati = gps.location.lat();
  float longi = gps.location.lng();

  if (millis() > 10000 && gps.charsProcessed() < 10)
  {
    Serial.println("No GPS detected: check wiring");
    while (true);
  }

  float dlong = destinationLong - longi;
  float dlat = destinationLat - lati;
  float y = sin(dlong) * cos(destinationLat);
  float x = (cos(lati) * sin(destinationLat)) - sin(lati) * cos(destinationLat) * cos(dlong);
  int angle = atan2(y, x);
  angle = angle * 57.29;
  angle = (angle + 360) % 360;
  angle = 360 - angle;

  float a = sq(sin(dlat / 2)) + cos(lati) * cos(destinationLat) * sq(sin(dlong / 2));
  float c = 2 * atan2(sqrt(a), sqrt(1 - a));
  float dist = 6371 * c;

  Serial.print("Distance : ");
  Serial.println(dist);
  Serial.print("Angle : ");
  Serial.println(angle);
  return (dist, angle);
  delay(1000);
}
void loop()
{
  float lati1 = gps.location.lat();
  float longi1 = gps.location.lng();

  digitalWrite(5, HIGH);
  digitalWrite(6, LOW);
  digitalWrite(7, HIGH);
  digitalWrite(8, LOW);
  delay(5000);

  float lati2 = gps.location.lat();
  float longi2 = gps.location.lng();

  float dlong = longi2 - longi1;
  float dlat = lati2 - lati1;
  float y = sin(dlong) * cos(lati2);
  float x = (cos(lati1) * sin(lati2)) - sin(lati1) * cos(lati2) * cos(dlong);
  int hangle = atan2(y, x);
  hangle = hangle * 57.29;
  hangle = (hangle + 360) % 360;
  hangle = 360 - hangle;

  float newlat = gps.location.lat();
  float newlong = gps.location.lng();

  float trdist, trangle = dist_angle(destinationLat, destinationLong);
  int rotangle = hangle - trangle;

  int rotime = trangle / 6;
  digitalWrite(5, HIGH);
  digitalWrite(6, LOW);
  delay(rotime);

  int mvtime = trdist / 2.25;
  digitalWrite(5, HIGH);
  digitalWrite(6, LOW);
  digitalWrite(7, HIGH);
  digitalWrite(8, LOW);
  delay(mvtime);


}
