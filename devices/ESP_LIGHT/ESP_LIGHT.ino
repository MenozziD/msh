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

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN        2 // On Trinket or Gemma, suggest changing this to 1
// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 7 // Popular NeoPixel ring size
#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. Note that for older NeoPixel
// strips you might need to change the third parameter -- see the
// strandtest example for more information on possible values.
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

const char* ssid = STASSID;
const char* password = STAPSK;

ESP8266WebServer server(80);

DynamicJsonDocument jsonBuffer(1024);

bool STATO_LED;

void handleRoot() {
  server.send(200, "text/html", file_head+file_index_body);
}

void handle_CMD() {

  String jsonOut = "";
  bool ok = false;
  bool param=false;
  jsonBuffer.clear();
  for (uint8_t i = 0; i < server.args(); i++) {
    if (server.argName(i) == "n") 
      jsonBuffer["cmd"] = server.arg(i);
      jsonOut=server.arg(i);
      Serial.println(jsonOut);
      if (jsonBuffer["cmd"] == "toggle" || jsonBuffer["cmd"] == "stato")
        ok=true;
  }
  
  if (ok)
  {
    if (jsonBuffer["cmd"] == "toggle") param=true;
    //jsonBuffer["output"] = (STATO_LED == true) ? "ON" : "OFF";
    jsonOut = (light(param)) ? "ON" : "OFF";
    Serial.println(jsonOut);
    jsonBuffer["output"]=jsonOut;
  }
  else
    jsonBuffer["output"] = "ERR";    //Comando non valido
  
  jsonOut="";
  serializeJson(jsonBuffer, jsonOut);
  server.send(200, " application/json", jsonOut);
}

void handleNotFound() {
  server.send(404, "text/html", file_head+file_error_body);
}


void setup() {
  // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
  // Any other board, you can remove this part (but no harm leaving it):
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.
  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)

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
  STATO_LED=true;  
}

void loop() {

  server.handleClient();
  MDNS.update();
  }

bool light (bool cmd)
{
  bool result;
  result=false;
  uint32_t black = pixels.Color(0, 0, 0);
  uint32_t white = pixels.Color(255,255,25);
  uint32_t color = pixels.getPixelColor(0);
  

    if (cmd == true)
    { 
      pixels.clear(); // Set all pixel colors to 'off'
      for(int i=0; i<NUMPIXELS; i++) { // For each pixel...
        // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
        // Here we're using a moderately bright green color:
        if (color == black)
          pixels.setPixelColor(i, white);
        else
          pixels.setPixelColor(i, black);
        pixels.show();   // Send the updated pixel colors to the hardware.
      }
    }
    delay(10);
    color = pixels.getPixelColor(0);
    if (color == black)
      result=false;
    else      
      result=true;
      
  return result;
}
