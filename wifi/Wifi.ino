&&//Leonardo
//Serial_ & dbgTerminal = Serial;
//HardwareSerial & espSerial = Serial1;

////UNO & M328P
#include <SoftwareSerial.h>
SoftwareSerial dbgTerminal(3, 2); // RX, TX
HardwareSerial & espSerial = Serial;

//
////MEGA2560 & Due
//HardwareSerial & dbgTerminal = Serial;
//HardwareSerial & espSerial = Serial1;
void setup()
{
  dbgTerminal.begin(9600);
  espSerial.begin(9600);
  GetResponse("AT");
  GetResponse("AT+RST");
}

void loop()
{
  if (espSerial.available())
    dbgTerminal.write(espSerial.read());
  if (dbgTerminal.available())
    espSerial.write(dbgTerminal.read());
  delayMicroseconds(1000);
}
String GetResponse(String AT_Command) {
  String tmpData;
  espSerial.println(AT_Command);
  delay(100);
  while (espSerial.available() > 0 )  {
    char c = espSerial.read();
    tmpData += c;

    if ( tmpData.indexOf(AT_Command) > -1 )
      tmpData = "";
    else
      tmpData.trim();
  }
  dbgTerminal.println(AT_Command + " --> " + tmpData);
  return tmpData;
}
