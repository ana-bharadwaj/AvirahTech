


#include <WiFi.h>
#include <WebServer.h>

int req = D8;  // mic REQ line goes to pin 5 through q1 (arduino high pulls request line low)
int dat = D1; //2;  // mic Data line goes to pin 2
int clk = D10;  // mic Clock line goes to pin 3
int led = D3;
int ledstate=LOW;
int i = 0;
int j = 0;
int k = 0;
int signCh = 8;
int sign = 0;
int decimal;
float dpp;
int units;
String s = "not on";
String vb;
byte mydata[14];
String value_str;
long value_int;  // was an int, could not measure over 32mm
float valu;
float Vbattf;
unsigned long prevMil=0;
unsigned long prevMil2=0;

const char* ssid = "Kingsman";  // your_wifi_ssid
const char* password = "12345678";

//const char* ssid = "Excitel_Wifi - 2.4G";  // your_wifi_ssid
//const char* password = "7380590909";
uint8_t retries = 0;
WebServer server(80);

void setup() {
  // Start the serial communication with the computer
  Serial.begin(115200);
  delay(100);
  pinMode(A0, INPUT); 
  Serial.println();

  pinMode(led, OUTPUT);
  pinMode(req, OUTPUT);
  pinMode(clk, INPUT_PULLUP);
  pinMode(dat, INPUT_PULLUP);
  // Try and Connect to the Network
  WiFi.begin(ssid, password);
  Serial.print("Connecting to ");
  Serial.print(ssid);
  Serial.println("...");

  // Wait for WiFi to connect for a maximum timeout of 20 seconds
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.print("Successfully connected to ");
  Serial.println(ssid);
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  server.on("/", mi);
  server.begin();
  updateWebpage(s);
  digitalWrite(req,LOW); 
  
}

void loop() {
  // Maintain your WiFi connection by checking its status before performing any internet-related task
  Serial.println(s);
  server.handleClient();
  Serial.println("here");
  mi();
  unsigned long currMil = millis();
  if(currMil-prevMil>= 1000){//1000 ms delay
  bat();
  prevMil=currMil;
  }
 if (Vbattf <= 3.7){
  unsigned long currMil2 = millis();
  if(currMil2-prevMil2>= 1000){//1000 ms delay
    if (ledstate == LOW){ledstate = HIGH;}
    else{ledstate=LOW;}
    digitalWrite(led,ledstate);
  prevMil2=currMil2;
  }}
}

void bat() {
  uint32_t Vbatt = 0;
  for(int i = 0; i < 16; i++) {
    Vbatt = Vbatt + analogReadMilliVolts(A0); // ADC with correction   
  }
  Vbattf = 2 * Vbatt / 16 / 1000.0;     // attenuation ratio 1/2, mV --> V
  Serial.println(Vbattf, 3);
  vb=String(Vbattf);
  server.send(200, "text/html", updateWebpage(String(Vbattf)));
//  delay(1000);
}
void mi() {
  digitalWrite(req, HIGH);  // generate set request
  for (i = 0; i < 13; i++) {
    k = 0;
    for (j = 0; j < 4; j++) {
      while (digitalRead(clk) == LOW) {} // hold until clock is high
      while (digitalRead(clk) == HIGH) {} // hold until clock is low
      bitWrite(k, j, (digitalRead(dat) & 0x1));
    }
    mydata[i] = k;
  }
  sign = mydata[4];
  value_str = String(mydata[6]) + String(mydata[7]) + String(mydata[8]) + String(mydata[9]) + String(mydata[10]);
  decimal = mydata[11];
  units = mydata[12];

  value_int = value_str.toInt();
  if (decimal == 0) dpp = 1.0;
  if (decimal == 1) dpp = 10.0;
  if (decimal == 2) dpp = 100.0;
  if (decimal == 3) dpp = 1000.0;
  if (decimal == 4) dpp = 10000.0;
  if (decimal == 5) dpp = 100000.0;

  valu = value_int / dpp;

  if (sign == 0) {
    s = String(valu, decimal);
  }
  if (sign == 8) {
    s = "-" + String(valu, decimal);
  }
  if (units == 0) {
    s = s + "mm";
  }
  if (units > 0) {
    s = s + "inch";
  }
  digitalWrite(req, LOW);
  Serial.println(s);
  server.send(200, "text/html", updateWebpage(s));
  delay(100);
  
}

String updateWebpage(String s) {
  Serial.print("=");
  String ptr = "<!DOCTYPE html> <html>\n";
  ptr += "<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=no\">\n";
  ptr += "<title>LED Control</title>\n ";
  ptr += "<meta http-equiv=\"refresh\" content=\"0.0001\">\n";
  ptr += "<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}\n";
  ptr += "body{margin-top: 50px;} h1 {color: #444444;margin: 50px auto 30px;} h3 {color: #444444;margin-bottom: 50px;}\n";
  ptr += ".button {display: block;width: 80px;background-color: #1abc9c;border: none;color: white;padding: 13px 30px;text-decoration: none;font-size: 25px;margin: 0px auto 35px;cursor: pointer;border-radius: 4px;}\n";
  ptr += ".button-on {background-color: #3498db;}\n";
  ptr += ".button-on:active {background-color: #3498db;}\n";
  ptr += ".button-off {background-color: #34495e;}\n";
  ptr += ".button-off:active {background-color: #2c3e50;}\n";
  ptr += "p {font-size: 14px;color: #888;margin-bottom: 10px;}\n";
  ptr += "</style>\n";
  ptr += "</head>\n";
  ptr += "<body>\n";
  ptr += "<h1>Digital Gauge Web Server</h1>\n";
  ptr += "<h2>Using STP Mode </h2>\n";
  ptr += "<h3>Digital Gauge Value " + s + "</h3>\n";
  ptr += "<h3>Battery"+ vb + "</h3>\n";
  ptr += "</body>\n";
  ptr += "</html>\n";
  return ptr;
}
