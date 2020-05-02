/*
 * ESP01_RELE: Software per nodo ESP01 per MSH.
 * Espone API per comandare RELE + Homa Page con comandi
 * Version 1.0  May, 2019
 * Authors: Davide Menozzi, Simone Sganzerla
*/

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ArduinoJson.h>
#include "index.h"

#ifndef STASSID
#define STASSID ""
#define STAPSK ""
#endif

const int K_TIME = 350;
const char* ssid = STASSID;
const char* password = STAPSK;

bool LOCK_STATUS=false;

ESP8266WebServer server(80);

DynamicJsonDocument jsonBuffer(1024);

void handleRoot() {
  server.send(200, "text/html", file_head+file_index_body);
}

void handle_CMD() 
{
  String jsonOut = "";
  bool ok = false;
  bool param=false;
  jsonBuffer.clear();
  for (uint8_t i = 0; i < server.args(); i++) {
    if (server.argName(i) == "n") 
      jsonBuffer["cmd"] = server.arg(i);
      if (jsonBuffer["cmd"] == "stato" || jsonBuffer["cmd"] == "toggle")
        ok=true;
  }
  if (ok)
  {
    if (jsonBuffer["cmd"] == "toggle") param=true;
    delay(10);
    jsonBuffer["output"] = (LOCK(param)) ? "ON" : "OFF";
  }
  else
    jsonBuffer["output"] = "ERR";    //Comando non valido
  
  serializeJson(jsonBuffer, jsonOut);
  server.send(200, " application/json", jsonOut);
}

void handleNotFound() {
  server.send(404, "text/html", file_head+file_error_body);
}

void setup(void) {
  Serial.begin(9600);
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

//param true significa che la funzione è stata invocata come comando
//param false significa che la funzione è stata invocata per sapere stato aperto/chiuso
bool LOCK(bool param)
{
  byte relON[] = {0xA0, 0x01, 0x01, 0xA2}; //Hex command to send to serial to open relay
  byte relOFF[] = {0xA0, 0x01, 0x00, 0xA1}; //Hex command to send to serial to close relay
  if (param) 
  {
      Serial.write(relON, sizeof(relON)); // turns the relay ON
      delay(K_TIME);
      Serial.write(relOFF, sizeof(relOFF)); // turns the relay OFF      Serial.println("Fatto!!");
      LOCK_STATUS=!LOCK_STATUS;
  }
  return LOCK_STATUS;
}
