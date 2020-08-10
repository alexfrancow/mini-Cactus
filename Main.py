import serial
import serial.tools.list_ports
import time
import sqlite3
import random
import sys
import json
import hashlib 
from threading import Thread

conn = sqlite3.connect('mini-cactus.db')
cursor = conn.cursor()
print("Opened database successfully")
'''
Status:
0: Can't connect
1: OK
2: Time out
'''
try:
    conn.execute('''CREATE TABLE discovery
        (SSID_md5 TEXT PRIMARY KEY NOT NULL UNIQUE,
        SSID_mac TEXT NOT NULL,
        SSID TEXT  NOT NULL UNIQUE,
        JSON_data           JSON    NOT NULL,
        SSID_Status            INT     NOT NULL,
        Location TEXT NOT NULL)''')
    print("Table created successfully")
except:
    print("Table was created previusly")
conn.commit()

def list_com():
    arduino_coms = []
    COMS = list(serial.tools.list_ports.comports())
    for COM in COMS:
        if "Silicon Labs" in str(COM):
            arduino_coms.append(str(COM).split("-")[0].replace(" ", ""))

    if not arduino_coms:
        print(arduino_coms)
        print("Arduino isn't detected!")
        sys.exit()
    return arduino_coms

def save_db(ssid, json_data, status):
    json_data = str(json_data)
    SSID_md5 = hashlib.md5(ssid.encode('utf-8')).hexdigest()
    try:
        gateway_mac = json_data.split("Gateway:Yes,")[1].split("}")[0]
        gateway_mac = str(gateway_mac).split("MAC_address: ")[1]
       
    except:
        gateway_mac = ""
        
    conn = sqlite3.connect('mini-cactus.db')
    conn.execute("insert into discovery (SSID_md5, SSID_mac, SSID, JSON_data, SSID_Status, Location) values (?, ?, ?, ?, ?, ?)",
            (SSID_md5, gateway_mac, ssid, json_data, status, ""))
    conn.commit()
    return True

def scan_net(com):
    json_data = {}
    json_data[ssid] = {}
    timeout = time.time() + 15
    while True:
        try:
            cc = str(ser.readline())
            if "Connecting:" not in cc:
                print(cc[2:][:-3])
                    
            if "Connecting" in cc and time.time() > timeout:
                print("Imposible conectar")
                break
            
            if "Host:" in cc:
                ip_address = cc.split("IP_address: ")[1].split(",")[0]
                host_information = cc.split("Host:{")[1].split("}")[0]
                json_data[ssid][ip_address] = {host_information}
                    
            if ".254" in cc:
                break
        except:
            continue

    print("JSON: ", json_data)
    return json_data


def use_arduino(com, ssid):
    print("Using: ", com)
    ser.port = com
    ser.open()
    time.sleep(1)
    ssid_bd = ssid
    ssid = bytes(ssid, encoding='utf-8')
    ser.write(ssid)
    json_data = scan_net(com)
    ser.close()
    status = "0"
    if "MAC_address:" in str(json_data):
        status = "1"
    save_db(ssid_bd, json_data, status)
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
        
