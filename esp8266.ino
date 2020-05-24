#include "ESP8266WiFi.h"
#include "Pinger.h"
#include "stdio.h"

extern "C" {
  #include "user_interface.h"
  #include "lwip/icmp.h"
}

Pinger pinger;
String incomingByte = "";
// Test settings
const char* ssid     = "";        
const char* password = "";  

void setup() {
  Serial.begin(9600);
  delay(10);
  Serial.println('\n');
  Serial.println("Welcome to mini-CACTUS discovery");
}

void scanHosts(String ssid){ 
  WiFi.begin(ssid);
  Serial.print("Connecting to ");
  Serial.print(ssid); Serial.println(" ...");

  int i = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000); 
    Serial.print("Connecting:\t");
    Serial.println(++i);
  }

  Serial.println('\n');
  Serial.println("Connection established!");  
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());
  Serial.print("Gateway IP address:\t");
  Serial.println(WiFi.gatewayIP());
  
  pinger.OnEnd([](const PingerResponse& response){
    // Print host data
    Serial.printf("Destination host data:\n");
    Serial.printf(
      "IP address= %s\n",
      response.DestIPAddress.toString().c_str());
      
    if(response.DestMacAddress != nullptr){
      Serial.printf(
        "MAC address= " MACSTR "\n",
        MAC2STR(response.DestMacAddress->addr));
    }
    
    if(response.DestHostname != ""){
      Serial.printf(
        "DNS name= %s\n",
        response.DestHostname.c_str());
    }

    return true;
  });

  // Ping default gateway
  Serial.printf(
    "\n\nPinging default gateway with IP %s\n",
    WiFi.gatewayIP().toString().c_str());
    
  if(pinger.Ping(WiFi.gatewayIP(), 1) == false){
    Serial.println("Error during last ping command.");
  }
  delay(1000);

  // Ping the network
  for(int i=1; i<255; i++){
    IPAddress ip (WiFi.gatewayIP()[0], WiFi.gatewayIP()[1], WiFi.gatewayIP()[2], i);
    Serial.println(ip);
    // The function accept a second integer parameter count that 
    // specify how many pings has to be sent:
    if(pinger.Ping(IPAddress(ip), 1) == false){
      Serial.println("Error during last ping command.");
    }
    delay(1000);
  }
  return;
}

void loop() {
  if(Serial.available()){
      incomingByte = Serial.readString();
      Serial.print("I received: ");
      Serial.println(incomingByte);
      scanHosts(incomingByte);
      //scanHosts("MOYOXXL 2.0");
  }
}
