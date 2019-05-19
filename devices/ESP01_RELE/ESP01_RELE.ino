#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#ifndef STASSID
#define STASSID "Room WiFi"
#define STAPSK  "roomwifi3553!"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

ESP8266WebServer server(80);

const int GPIO0 = 0;

void handleRoot() {
  server.send(200, "text/plain", "Hello from ESP-01 RELE!");
}


void handle_CMD() {

  String cmd="";
  String mex="Stato RELE:";
  int check=0;
  for (uint8_t i = 0; i < server.args(); i++) {
    if (server.argName(i)=="n")
      cmd=server.arg(i);
  }
  
  if (cmd=="on")
  {
    digitalWrite(GPIO0,LOW);
    check=1;
  }  
  else if (cmd=="off")
  {
    digitalWrite(GPIO0,HIGH);
    check=1;
  }  
  else if (cmd=="toggle")
  {
    digitalWrite(GPIO0,not(digitalRead(GPIO0)));
    check=1;
  } 
  else if (cmd=="stato_rele" or check==1)
  {
    delay(50);
    if (digitalRead(GPIO0)== 0)
      mex=mex+"ON";
    else
      mex=mex+"OFF";
  }
  else
    mex=mex+"CMD SCONOSCIUTO";    
  server.send(200, "text/plain", mex);
}

void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  digitalWrite(GPIO0, 0);
}

void setup(void) {
  pinMode(GPIO0, OUTPUT);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);
  server.on("/on", handle_ON);
  server.on("/off", handle_OFF);
  server.on("/toggle", handle_TOGGLE);
  server.on("/stato", handle_STATUS);
  server.on("/cmd", handle_CMD);

  server.on("/inline", []() {
    server.send(200, "text/plain", "this works as well");
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}
