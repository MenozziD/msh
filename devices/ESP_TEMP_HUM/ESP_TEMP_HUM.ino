/*
 * ESP01_RELE: Software per nodo ESP01 per MSH.
 * Espone API per leggere Temperatura e Umidita + Home Page con comandi
 * Version 1.0  May, 2019
 * Authors: Davide Menozzi, Simone Sganzerla
*/

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ArduinoJson.h>
#include "index.h"
#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include <SimpleDHT.h>

#ifndef STASSID
#define STASSID ""
#define STAPSK ""
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

ESP8266WebServer server(80);

DynamicJsonDocument jsonBuffer(1024);


#define GPIO_DHT11 2
#define DHTLIB_ERROR_CHECKSUM 6
#define DHTLIB_ERROR_CONNECT -3
#define DHTLIB_ERROR_TIMEOUT -2
#define DHTLIB_OK 0
// per DHT11
SimpleDHT11 DHT; // Oggetto dht11
byte temperature = 0;
byte humidity = 0;


void handleRoot() {
  server.send(200, "text/html", file_head+file_index_body);
}

void handle_CMD() {

  String jsonOut = "";
  bool ok = false;
  int chk;
  float temp, humi;
  jsonBuffer.clear();
  for (uint8_t i = 0; i < server.args(); i++) {
    if (server.argName(i) == "n") 
      jsonBuffer["cmd"] = server.arg(i);
      if (jsonBuffer["cmd"] == "stato")
        ok=true;
  }
  
  if (ok)
  {
    chk = DHT.read(GPIO_DHT11, &temperature, &humidity, NULL);  // Legge il sensore dht11
    temp =float(temperature);
    humi =float(humidity);
    switch (chk){
      case DHTLIB_OK:  
                jsonBuffer["output"] = String(temp)+"°C;"+String(humi)+"%";
                break;
      case DHTLIB_ERROR_CHECKSUM:
                jsonBuffer["output"] ="ERR Checksum error";  
                break;
      case DHTLIB_ERROR_TIMEOUT: 
                jsonBuffer["output"] ="ERR Time out error"; 
                break;
      case DHTLIB_ERROR_CONNECT: 
                jsonBuffer["output"] ="ERR Connection error"; 
                break;                
      default: 
                jsonBuffer["output"] ="ERR " + String(chk) + " error"; 
                break;
    }
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
