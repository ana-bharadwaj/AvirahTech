#include <WiFi.h>
#include <HTTPClient.h>
#include <WebServer.h>

int req = 5;  // REQ line connected to pin 5
int dat = 2;  // Data line connected to pin 2
int clk = 3;  // Clock line connected to pin 3
int led = 4;  // LED connected to pin 4

float Vbattf;
String s = "not on";
String vb;
WebServer server(80);

const char* ssid = "Kingsman";  // your WiFi SSID
const char* password = "12345678";
const char* streamlit_url = "http://your-streamlit-app-url/endpoint";  // Replace with your Streamlit app's URL and endpoint

void setup() {
  Serial.begin(115200);
  pinMode(req, OUTPUT);
  pinMode(clk, INPUT_PULLUP);
  pinMode(dat, INPUT_PULLUP);
  pinMode(led, OUTPUT);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to ");
  Serial.print(ssid);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.begin();
}

void loop() {
  server.handleClient();
  sendDataToStreamlit(s);
  delay(1000);
}

void handleRoot() {
  String page = updateWebpage(s);
  server.send(200, "text/html", page);
}

String updateWebpage(String s) {
  String ptr = "<!DOCTYPE html><html>\n";
  ptr += "<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=no\">\n";
  ptr += "<title>ESP32 Web Server</title>\n";
  ptr += "<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}\n";
  ptr += "body {margin-top: 50px;} h1 {color: #444444;margin: 50px auto 30px;} h3 {color: #444444;margin-bottom: 50px;}\n";
  ptr += ".button {display: block;width: 80px;background-color: #1abc9c;border: none;color: white;padding: 13px 30px;text-decoration: none;font-size: 25px;margin: 0px auto 35px;cursor: pointer;border-radius: 4px;}\n";
  ptr += ".button-on {background-color: #3498db;}\n";
  ptr += ".button-on:active {background-color: #3498db;}\n";
  ptr += ".button-off {background-color: #34495e;}\n";
  ptr += ".button-off:active {background-color: #2c3e50;}\n";
  ptr += "p {font-size: 14px;color: #888;margin-bottom: 10px;}\n";
  ptr += "</style>\n";
  ptr += "</head>\n";
  ptr += "<body>\n";
  ptr += "<h1>ESP32 Web Server</h1>\n";
  ptr += "<h3>Current Value: " + s + "</h3>\n";
  ptr += "<h3>Battery: " + vb + "</h3>\n";
  ptr += "</body>\n";
  ptr += "</html>\n";
  return ptr;
}

void sendDataToStreamlit(String value) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(streamlit_url);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    String httpRequestData = "value=" + value;
    int httpResponseCode = http.POST(httpRequestData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("Error in WiFi connection");
  }
}
