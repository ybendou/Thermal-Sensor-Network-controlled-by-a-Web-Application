/*
  Web client

 This sketch connects to a website (http://www.google.com)
 using an Arduino Wiznet Ethernet shield.

 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13

 created 18 Dec 2009
 by David A. Mellis
 modified 9 Apr 2012
 by Tom Igoe, based on work by Adrian McEwen

 */

#include <SPI.h>
#include <Ethernet.h>
#include <dht.h>
dht DHT;

#define DHT22_PIN 6
String Temperature;
String key="projetdev09";
int identifiant=4;
// Enter a MAC address for your controller below.
// Newer Ethernet shields have a MAC address printed on a sticker on the shield
byte mac[] = { 0x90, 0xA2, 0xDA, 0x0F, 0x1C, 0xEA };
// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
//IPAddress server(74,125,232,128);  
char server[] = "163.172.163.119";    
//char server[] = "192.168.0.100";
// Set the static IP address to use if the DHCP fails to assign
IPAddress ip(172, 22, 220, 174);

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
EthernetClient client;

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  Serial.println("DHT TEST PROGRAM ");
  Serial.print("LIBRARY VERSION: ");
  Serial.println(DHT_LIB_VERSION);
  Serial.println();
  Serial.println("Type,\tstatus,\tHumidity (%),\tTemperature (C)");
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // try to congifure using IP address instead of DHCP:
    Ethernet.begin(mac, ip);
  }
  // give the Ethernet shield a second to initialize:
  delay(1000);
  
}
String cryptData(String message){
    int k_len = key.length();
    int k_ints[k_len];
    int txt_ints[message.length()];
    String ret_txt = "";
    for (int i=0 ; i<k_len;i++){
      char character=key[i];
      k_ints [i]= character;
    };
    for (int i=0; i<message.length();i++){
      char character=message[i];
        txt_ints[i] = character;
      };
    for (int i=0 ; i<message.length();i++){
      int adder=k_ints[i%k_len];
      int v = (txt_ints[i]-32+adder)%95;
      char character = v+32;
      ret_txt+=character;
    }
      
  Serial.println("text : "+ret_txt);
  return(ret_txt);
}
void sendData(double Temperature){
  String crypted_message=cryptData("send_temp/"+String(identifiant)+"/"+String(Temperature));
  String request="GET /collecte/send/"+crypted_message+" HTTP/1.1";  
  Serial.println("connecting...");
  // if you get a connection, report back via serial:

  
  if (client.connect(server, 8965)) {
    Serial.println("connected");
    // Make a HTTP request:
    client.println(request);
    client.println();
    client.stop();
  } else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
  Serial.println(request);
}

void loop() {

  Serial.print("DHT22, \t");
  int chk = DHT.read22(DHT22_PIN);
  switch (chk)
  {
    case DHTLIB_OK:  
    Serial.print("OK,\t"); 
    break;
    case DHTLIB_ERROR_CHECKSUM: 
    Serial.print("Checksum error,\t"); 
    break;
    case DHTLIB_ERROR_TIMEOUT: 
    Serial.print("Time out error,\t"); 
    break;
    default: 
    Serial.print("Unknown error,\t"); 
    break; 
    }
    // DISPLAY DATA
  Serial.print(DHT.humidity, 1);
  Serial.print(",\t");
  Serial.println(DHT.temperature, 1);
  
  sendData(DHT.temperature);
  delay(300000);
  // if there are incoming bytes available
  // from the server, read them and print them:
  if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }

  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    Serial.println("disconnecting.");

  }
}
