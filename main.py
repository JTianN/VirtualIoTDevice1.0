from fastapi import FastAPI
import uvicorn
import time
import threading
from azure.iot.device import IoTHubModuleClient
import requests
import json



idData = []
statusDevice = []
listA = []

def initPro():
    url = "https://iotdevice-7175.restdb.io/rest/iotdevice"

    headers = {
        'content-type': "application/json",
        'x-apikey': "db915e399a7eca3fb34591582dca5bb24e8cd",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    for i in data:
        idData.append(i['_id'])
initPro()


def intdata():
    for i in idData:
        url = "https://iotdevice-7175.restdb.io/rest/iotdevice/"+i
        payload = "{\"status\":\"clear\"}"                                  ## ตั้งค่า status device = 0  แรกเริ่ม
        headers = {
            'content-type': "application/json",
            'x-apikey': "db915e399a7eca3fb34591582dca5bb24e8cd",
            'cache-control': "no-cache"
                }
        response = requests.request("PUT", url, data=payload, headers=headers)
intdata()

def intdata2():
    for i in idData:
        url = "https://iotdevice-7175.restdb.io/rest/iotdevice/"+i
        payload = "{\"status\":\"ON\"}"                                  ## ตั้งค่า status device = 0  แรกเริ่ม
        headers = {
            'content-type': "application/json",
            'x-apikey': "db915e399a7eca3fb34591582dca5bb24e8cd",
            'cache-control': "no-cache"
                }
        response = requests.request("PUT", url, data=payload, headers=headers)


def updatestatus(statusB,no):
    inputB = statusB
    idDevice = no
    url = "https://iotdevice-7175.restdb.io/rest/iotdevice/" + idData[idDevice]
    print(url)
    payload = '{\"status\":\"' + 'str(inputB)' + '\"}'  #str(inputB)
    print(payload)
    headers = {
    'content-type': "application/json",
    'x-apikey': "db915e399a7eca3fb34591582dca5bb24e8cd",
    'cache-control': "no-cache"
    }
    response = requests.request("PUT", url, data=payload, headers=headers)


# List of connection strings for multiple devices
CONNECTION_STRINGS = [
    "HostName=D7A4IHSI02.azure-devices.net;DeviceId=665427f514e2fe0ce5c8247b;SharedAccessKey=ZHPWEd21iGmjMXpDQ+8s/wuGJoXngPn2Sp8tRMJwv1Q=", # Device 1 GH A
    "HostName=D7A4IHSI02.azure-devices.net;DeviceId=6654283414e2fe48c5c824a5;SharedAccessKey=laQS5um49Ea8jgJgu1LTjgKJfB/e8Eg+ZTE4SMYIntw=", # Device 2 GH B
    "HostName=D7A4IHSI02.azure-devices.net;DeviceId=665428e114e2fe4612c8250e;SharedAccessKey=UCjFDthiXe3pCd4+79E1L8yDADcCkjHWCzpT1pxr2Mk=", # Device 3 GH C
    "HostName=D7A4IHSI02.azure-devices.net;DeviceId=660b874f3418af65fedd60c0;SharedAccessKey=Pu554PVhvT0t5ESO8mjjQa17qVLS3k/LQR2xDbSjLqU=", # Device 4 FZ A
    "HostName=D7A4IHSI02.azure-devices.net;DeviceId=6654295b14e2fe6447c82554;SharedAccessKey=MPQOwEyflg9kQrMwJBmk37RH1AQ8YdJD0hNdb7UTjKo=", # Device 5 FZ B
    "HostName=D7A4IHSI02.azure-devices.net;DeviceId=665429d914e2fe2e04c825a1;SharedAccessKey=byTTIL3RaH7pnVaAgkHloY8aGuxVRxegK75vSPt0QRU="  # Device 6 FZ C
    # Add more connection strings as needed
]


def twin_update_listener(client, device_id):
    while True:
        patch = client.receive_twin_desired_properties_patch()  # blocking call
        print(f"Twin patch received for device {device_id}")
        patch.pop('$version', None)
        print(f"Sending Twin as reported property for device {device_id}...")
        print(patch)
        client.patch_twin_reported_properties(patch)
        print(f"Reported properties updated for device {device_id}")

roundT = 0
status = 0 
# เพิ่มการ check status ว่าเชื่อมต่อสำเร็จหรือไม่ ?
def iothub_client_init(connection_string):
        global statusDevice  # ประกาศให้ statusDevice เป็น global
        global listA  # ประกาศให้ listA เป็น global
        global roundT
        global status 
        try:
            # สร้าง client จาก connection string
            client = IoTHubModuleClient.create_from_connection_string(connection_string)

            # เชื่อมต่อกับ Azure IoT Hub
            client.connect()

            # ตรวจสอบว่าการเชื่อมต่อสำเร็จ
            a = client.connected
            print(a)
            if client.connected:
                status = status+1
                intdata2()
                roundT = roundT+1
                print("เชื่อมต่อกับ Azure IoT Hub สำเร็จ")
            else:
                print("ไม่สามารถเชื่อมต่อกับ Azure IoT Hub ได้")

            return client
        except Exception as e:
            print("เกิดข้อผิดพลาดในการเชื่อมต่อกับ Azure IoT Hub:", e)
            return None



def iothub_client_sample_run():
    try:
        clients = []

        for connection_string in CONNECTION_STRINGS:
            client = iothub_client_init(connection_string)
            device_id = connection_string.split(";")[1].split("=")[1]  # Extract device ID
            clients.append((client, device_id))

            twin_update_listener_thread = threading.Thread(target=twin_update_listener, args=(client, device_id))
            twin_update_listener_thread.daemon = True
            twin_update_listener_thread.start()



        while True:
            time.sleep(1000)

    except KeyboardInterrupt:
        print("IoT Hub Device Twin device sample stopped")





###########################################################
# RestAPI Initial
# Clear data to status initial








##########################################################
# setting Server
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"} 

@app.get("/AllDevice")
def GetListDevice():

        return CONNECTION_STRINGS





##########################################################

# Setup main function
def run_iothub_client():
    iothub_client_sample_run()

def run_uvicorn():
    uvicorn.run("main:app", host="0.0.0.0", port=8082)

##########################################################

if __name__ == "__main__":
    iothub_thread = threading.Thread(target=run_iothub_client)
    uvicorn_thread = threading.Thread(target=run_uvicorn)

    # เริ่มต้นทั้งสองเธรด
    iothub_thread.start()

    uvicorn_thread.start()

    # ถ้าต้องการ รอให้ทั้งสองเธรดทำงานเสร็จ
    iothub_thread.join()

    uvicorn_thread.join()