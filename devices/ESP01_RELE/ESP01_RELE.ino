#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ArduinoJson.h>
#include "index.h"

#ifndef STASSID
#define STASSID ""
#define STAPSK  ""
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

ESP8266WebServer server(80);

StaticJsonBuffer<200> jsonBuffer;
JsonObject& root = jsonBuffer.createObject();

const int GPIO0 = 0;

void handleRoot() {
  server.send(200, "text/html", file1);
}


void handle_CMD() {

  String cmd="";
  String result="";
  String output="";
  String jsonOut="";
    
  int check=0;
  for (uint8_t i = 0; i < server.args(); i++) {
    if (server.argName(i)=="n")
      cmd=server.arg(i);
  }

  if (cmd=="on" || cmd=="off" || cmd=="stato_rele" || cmd=="toggle")
  {
    if (cmd=="on")
      digitalWrite(GPIO0,LOW);
    else if (cmd=="off")
      digitalWrite(GPIO0,HIGH);
    else if (cmd=="toggle")
      digitalWrite(GPIO0,not(digitalRead(GPIO0)));

    delay(100);
    result = String(!digitalRead(GPIO0));  
    output = (digitalRead(GPIO0)) ? "OFF" : "ON";
  }    
  else
  {
    //Comando non valido
    result = "-1";
    output="ERR";
  }  
  root["cmd"] = cmd;
  root["result"] = result;
  root["output"] = output;
  
  root.printTo(jsonOut);
  server.send(200, " application/json", jsonOut);
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
