import serial
import serial.tools.list_ports
import time

def list_com():
    arduino_coms = []
    COMS = list(serial.tools.list_ports.comports())
    for COM in COMS:
        if "Silicon Labs" in str(COM):
            arduino_coms.append(str(COM).split("-")[0])
    print("Arduino ports:", arduino_coms)
    return arduino_coms


ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM4'

ser.open()
time.sleep(2)
#ser.write(b'MOYOXXL 2.0')
ser.write(b'_ONOWiFi')

mac_addreses = []
ip_addreses = []
while True:
     cc=str(ser.readline())
     print(cc[2:][:-3])
     if "MAC address=" in cc:
         mac_addreses.append(cc.split("=")[1].replace(" ", "").replace("\\n'", ""))
         print("MACCCCS: ", mac_addreses)
     if ".255" in cc:
         break
     
ser.close()
