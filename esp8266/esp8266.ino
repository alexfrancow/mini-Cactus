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

void scanHosts(String ssid){ Serial.println('\n');
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

  pinger.OnReceive([](const PingerResponse& response)
  {
    if (response.ReceivedResponse)
    {
      Serial.printf(
        "Reply from %s: bytes=%d time=%lums TTL=%d\n",
        response.DestIPAddress.toString().c_str(),
        response.EchoMessageSize - sizeof(struct icmp_echo_hdr),
        response.ResponseTime,
        response.TimeToLive);
    }
    else
    {
      Serial.printf("Request timed out.\n");
    }

    // Return true to continue the ping sequence.
    // If current event returns false, the ping sequence is interrupted.
    return true;
  });
  
  pinger.OnEnd([](const PingerResponse& response){
    if(response.TotalReceivedResponses > 0)
    {
    // Print host data
    Serial.printf("{Host:{");

    if (response.DestIPAddress.toString() == WiFi.gatewayIP().toString()){
      Serial.printf(
        "Gateway:Yes, ");
    }
    
    Serial.printf(
      "IP_address: %s,",
      response.DestIPAddress.toString().c_str());
      
    if(response.DestMacAddress != nullptr){
      Serial.printf(
        "MAC_address: " MACSTR "}}\n",
        MAC2STR(response.DestMacAddress->addr));
    }
    return true;
    }
    return false;
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

void scanAPs(){
  //Serial.print("Scan start ... ");
  int n = WiFi.scanNetworks();
  //Serial.print(n);
  //Serial.println(" network(s) found:");
  Serial.print("{Networks:[");
  for (int i = 0; i < n; i++)
  {
    if(i>0){
      Serial.print(", ");
    }
    Serial.print(WiFi.SSID(i));
  }
  Serial.println("]}");
  delay(1000);
}

void loop() {
  if(Serial.available()){
      incomingByte = Serial.readString();
      incomingByte.trim();
      if(incomingByte.substring(0) == "scanAPs()"){
        Serial.print("[");
        Serial.print(WiFi.macAddress());
        Serial.print("] ");
        Serial.print("received: ");
        Serial.print(incomingByte);
        Serial.println(" function");
        scanAPs();
      }
      else {
        Serial.print("[");
        Serial.print(WiFi.macAddress());
        Serial.print("] ");
        Serial.print("received: ");
        Serial.print(incomingByte);
        Serial.println(" SSID");
        scanHosts(incomingByte);
      }
  }
}
