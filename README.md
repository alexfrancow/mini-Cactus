# mini-Cactus
:cactus: mini-Cactus discovery it's a WiFi Cactus low cost version with ESP8266 devices, at the moment it's just a PoC.

<p align="center"><img src="images/01.jpg" height="215" width="175" /></p>

[![](https://img.shields.io/badge/twitter-@alexfrancow-00aced?style=flat-square&logo=twitter&logoColor=white)](https://twitter.com/alexfrancow) [![](https://img.shields.io/badge/linkedin-@alexfrancow-0084b4?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alexfrancow)

## Requirements

You must install the USB to UART driver:
- https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers

## Multi-Threading

```python

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
            continue
    av_com = random.choice(av_coms)
    return av_com
    
ssids = ["MOYOXXL 2.0", "_ONOWiFi", "_ONOWiFiXXX"]
for ssid in ssids:
    av_com = av_arduino(coms)
    print("Random:", av_com)
    if av_com:
        thread_with_args = Thread(target=use_arduino, args=(av_com, ssid))
        thread_with_args.start()
        thread_with_args.join()
        time.sleep(5)
```

## TODO

- Multithreading ESP8266 devices :white_check_mark:
- Info gathering with port scanning 
- WPS - Pixie Dust Attack
- Web Interface (?)
- BD to Pandas and send it to Kibana
- Evil twin mode
- Improve the code (C++ and Python)
- LCD eyes
- 3D printed case
- Drone PoC (?)
