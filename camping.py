#camPing.py - send email to email in prep_email.py containing camera status. credits to DankWaifu & .
              
import subprocess
import os
import csv
import time
from prep_email import send_email
import json

#ping cameras
def pingCam(cameras):
    
    with open(os.devnull, "wb") as limbo:
        statusList = []
        ipList = []
        for n in range(len(cameras)):
        # for n in range(1, 100):
            # ip="192.168.0.{0}".format(n)
            ip = cameras[n]
            result=subprocess.call(["ping", "-c", "1", "-w", "200", ip], stdout=limbo, stderr=limbo)    #ping
            if result:    #if offline add results to list
                online = False
            else:
                online = True    #if online add results to ipList
            statusList.append(online)
            ipList.append(ip)
    return (statusList, ipList)

def run():
    cameras = ["192.168.0.11", "192.168.0.29", "192.168.0.39"]
    statusList, ipList = pingCam(cameras)
    ping1 = {}
    for i in range(len(statusList)):    #add results to dictionary for later comparison
        
        ping1[ipList[i]] = statusList[i]
        print(ping1)

    statusList, ipList = pingCam(cameras)
    ping2 = {}
    for i in range(len(statusList)):    #add results to dictionary for later comparison
        ping2[ipList[i]] = statusList[i]
        print(ping2)
    # return ping2
    if ping1 != ping2:
        result = json.dumps(ping2)
        file = open("camStatus.txt", "w")
        file.write(result)
        file.close() 
        send_email()
    time.sleep(30)
    run()

if __name__ == '__main__':
   
    run()
