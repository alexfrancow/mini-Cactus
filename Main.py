import serial
import serial.tools.list_ports
import time
import sqlite3
import random
import sys
import json
import hashlib 
from threading import Thread
import multiprocessing


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

def scan_net(ser, ssid, com):
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

            if ".22" in cc:
                time.sleep(2)
                break
        except:
            continue

    print("JSON: ", json_data)
    return json_data


def use_arduino(ser, com, ssid):
    print("[?] Using: ", com)
    print("[?] SSID: ", ssid)
    ser.port = com
    ser.open()
    time.sleep(1)
    ssid_bd = ssid
    ssid = bytes(ssid, encoding='utf-8')
    ser.write(ssid)
    json_data = scan_net(ser, ssid, com)
    ser.close()
    status = "0"
    if "MAC_address:" in str(json_data):
        status = "1"
    save_db(ssid_bd, json_data, status)
    return True

def av_arduino(ser, coms):
    while True:
        av_coms = []
        for com in coms:
            ser.port = com
            try:
                ser.open()
                ser.close()
            except:
                continue
            else:
                av_coms.append(com)
      
        if av_coms:
            break
        else:
            time.sleep(5)
            continue

    return av_coms


if __name__ == '__main__':
    conn = sqlite3.connect('mini-cactus.db')
    cursor = conn.cursor()
    print("Opened database successfully")
    try:
        conn.execute('''CREATE TABLE discovery
            (SSID_md5 TEXT NOT NULL,
            SSID_mac TEXT NOT NULL,
            SSID TEXT  NOT NULL,
            JSON_data           JSON    NOT NULL,
            SSID_Status            INT     NOT NULL,
            Location TEXT)''')
        print("Table created successfully")
    except:
        print("Table was created previusly")
    conn.commit()
    
    ser = serial.Serial()
    ser.baudrate = 9600
    coms = list_com()
    ssids = ["alexfrancow", "MOYOXXL 2.0", "FaryLink_C5BDD4", "alexfrancow", "_ONOWiFi", "FaryLink_C5BDD4", "_ONOWiFiXXX"]
    #ssids = ["FaryLink_C5BDD4"]
    print("SSIDS:", list(ssids))
    print("Arduino ports:", coms)

    n_ssids = len(ssids)
    num = 0
    while True:
        av_coms = av_arduino(ser, coms)
        if len(av_coms) > 0:
            print("[?] Availables: ", av_coms)
            threads = []
            for av_com in av_coms:
                threads.append(av_com+"_thread")
                com_tread = av_com+"_thread"
                print("[!] Starting: ",com_tread)
                com_tread = multiprocessing.Process(target=use_arduino, args=(ser, av_com, ssids[num],)).start()
                num += 1

        time.sleep(2)
  
