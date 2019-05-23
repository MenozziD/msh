/*
 * ESP01_RELE: Software per nodo ESP01 per MSH.
 * Espone API per comandare RELE e Homa Page con comandi
 * Version 1.0  May, 2019
 * Authors: Davide Menozzi, Simone Sganerzla
*/

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
  server.send(200, "text/html", file_head+file_index_body);
}

void handle_CMD() {

  String jsonOut = "";
  bool ok = false;
  
  for (uint8_t i = 0; i < server.args(); i++) {
    if (server.argName(i) == "n") 
      root["cmd"] = server.arg(i);
      if (root["cmd"] == "on" || root["cmd"] == "off" || root["cmd"] == "stato_rele" || root["cmd"] == "toggle")
        ok=true;
  }
  
  if (ok)
  {
    if (root["cmd"] == "on")          digitalWrite(GPIO0,LOW);
    else if (root["cmd"] == "off")    digitalWrite(GPIO0,HIGH);
    else if (root["cmd"] == "toggle") digitalWrite(GPIO0,not(digitalRead(GPIO0)));
    delay(10);
    root["output"] = (digitalRead(GPIO0)) ? "OFF" : "ON";
  }
  else
    root["output"] = "ERR";    //Comando non valido
  
  root.printTo(jsonOut);
  server.send(200, " application/json", jsonOut);
}

void handleNotFound() {
  server.send(404, "text/html", file_head+file_error_body);
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

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}
