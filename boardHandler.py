import json
import time 
import socket
import FileHandler

def compareDict(a,b):
    if set(a.keys()) ^ set(b.keys()) != set():
        return False 

    for key in a.keys():
        if a[key] != b[key]:
            return False

    return True

def buildBoard(fullChart):
    result = {}

    for student in fullChart:
        studentId = student["id"] 
        didAttend = student["attend"]
        result[studentId] = {
            "name": student["name"],
            "status": didAttend
        } 

    return result

def handleBoard(client_socket):
    header =  (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/event-stream\r\n"
        "Cache-Control: no-cache\r\n" 
        "Connection: keep-alive\r\n"
        "\r\n"
    )

    client_socket.sendall(header.encode())
    
    studentInfo = json.loads(FileHandler.getFileAsString("./db/student-info.json"))
    cache = None

    while True:
        studentInfo = json.loads(FileHandler.getFileAsString("./db/student-info.json"))
        updated = buildBoard(studentInfo)
        
        if cache != None and compareDict(cache, updated):
            time.sleep(1)
            continue

        frame = (
            f"event: update\n"
            f"data: {json.dumps(updated)}\n\n"
        )
        print(frame)

        try:
            client_socket.sendall(frame.encode())
        except:
            print("no client found")
            break

        cache = updated
