import serial
import serial.tools.list_ports
import time
import sqlite3
import random
from threading import Thread

conn = sqlite3.connect('test.db')
print("Opened database successfully")
'''
Status:
0: Can't connect
1: OK
2: Time out
'''
try:
    conn.execute('''CREATE TABLE discovery
         (SSID INT PRIMARY KEY     NOT NULL,
         Macs           TEXT    NOT NULL,
         Status            INT     NOT NULL)''')
    print("Table created successfully")
except:
    print("Table was created previusly")

def list_com():
    arduino_coms = []
    COMS = list(serial.tools.list_ports.comports())
    for COM in COMS:
        if "Silicon Labs" in str(COM):
            arduino_coms.append(str(COM).split("-")[0].replace(" ", ""))
    return arduino_coms

def save_db(ssid, macs, status):
    return True

def scan_net(com):
    mac_addreses = []
    ip_addreses = []
    timeout = time.time() + 15
    while True:
        try:
            cc = str(ser.readline())
            if "Connecting:" not in cc:
                print(cc[2:][:-3])
                    
            if "Connecting" in cc and time.time() > timeout:
                print("Imposible conectar")
                break
                
            if "MAC address=" in cc:
                mac_addreses.append(cc.split("=")[1].replace(" ", "").replace("\\n'", ""))
                print("MACCCCS: ", mac_addreses)
                    
            if ".254" in cc:
                break
        except:
            continue

    print("Total: ", mac_addreses)
    return mac_addreses


def use_arduino(com, ssid):
    print("Using: ", com)
    ser.port = com
    ser.open()
    time.sleep(1)
    ssid = bytes(ssid, encoding='utf-8')
    ser.write(ssid)
    scan_net(com)
    ser.close()
    return True

def av_arduino(coms):
    av_coms = []
    while True:
        for com in coms:
            ser.port = com
            if ser.is_open == True:
                continue
            else:
                av_coms.append(com)
        if av_coms:
            break
        else:
            time.sleep(5)
            print("aun no")
            continue

    av_com = random.choice(av_coms)
    return av_com

        
ser = serial.Serial()
ser.baudrate = 9600
coms = list_com()
ssids = ["MOYOXXL 2.0", "_ONOWiFi", "_ONOWiFiXXX"]
print("SSIDS:", list(ssids))
print("Arduino ports:", coms)


for ssid in ssids:
    av_com = av_arduino(coms)
    print("Random:", av_com)
    if av_com:
        thread_with_args = Thread(target=use_arduino, args=(av_com, ssid))
        thread_with_args.start()
        thread_with_args.join()
        time.sleep(5)
        
