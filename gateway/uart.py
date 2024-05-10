import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    # return commPort
    return "COM3"

if getPort() != "None":
    ser = serial.Serial( port=getPort(), baudrate=115200)
    print(ser)

mess = ""
def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")

    print(splitData)
    if splitData[1] == "T":
        client.publish("temperature", splitData[2])
    elif splitData[1] == "H":
        client.publish("humidity", splitData[2])
    elif splitData[1] == "SM":
        soil_moisture = float(splitData[2])
        client.publish("soil-moisture", soil_moisture)
        # Kiểm tra và điều khiển máy bơm
        if soil_moisture > 60:
            client.publish("pump", "0")  # Tắt máy bơm
        elif soil_moisture < 30:
            client.publish("pump", "1")  # Bật máy bơm

mess = ""
def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        print(mess)
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

def writeData(data):
    ser.write(str(data).encode('utf-8'))