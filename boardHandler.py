import json
import time 
import socket
import FileHandler

def compareDict(a,b):
    # 두 dict의 key 집합이 다르면 변경된 것으로 간주
    if set(a.keys()) ^ set(b.keys()) != set():
        return False 

    # 모든 key의 value가 동일해야 동일한 구조로 판단
    for key in a.keys():
        if a[key] != b[key]:
            return False

    return True

def buildBoard(fullChart):
    # student-info.json 구조를 서버 전송용 구조로 재가공
    result = {}

    # 학생 ID를 key 로 하고 필요한 정보만 추출
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

    # 초기에 파일 내용을 읽고 캐시 생성
    studentInfo = json.loads(FileHandler.getFileAsString("./db/student-info.json"))
    cache = None

    # 클라이언트 연결이 끊길 때까지 반복
    while True:
        studentInfo = json.loads(FileHandler.getFileAsString("./db/student-info.json"))
        updated = buildBoard(studentInfo)

        # 캐시와 동일하면 이벤트 전송 생략 (폴링 주기는 1초)
        if cache != None and compareDict(cache, updated):
            time.sleep(1)
            continue
        
        # SSE 메시지 형식:
        #   event: 이벤트이름
        #   data: 전송할데이터
        frame = (
            f"event: update\n"
            f"data: {json.dumps(updated)}\n\n"
        )
        print(frame)

        # 클라이언트로 전송. 실패 시 연결 종료로 판단
        try:
            client_socket.sendall(frame.encode())
        except:
            print("no client found")
            break
        
        # 최신 상태를 캐시에 저장
        cache = updated


# 설명
# 연결을 '닫지 않고 계속 유지'하는 방식으로 동작한다.
# 이것을 SSE(Server-Sent Events)라고 한다.
#
# SSE는 웹브라우저가 서버에 한 번 요청을 보내면,
# 서버가 그 연결을 계속 붙들고 있다가 필요한 순간마다
# "event: ..." 형식의 메시지를 다시 보내는 구조다.
#
# 서버 -> 브라우저 단방향으로 "변경 사항을 밀어주는" 기능이라 생각하면 편함
#
# 이 방식의 핵심은 다음 두 가지다:
#   1) HTTP 연결을 끊지 않는다.
#   2) 서버는 데이터가 바뀌었을 때마다 새로운 메시지를 push한다.
#         2-1) 이 코드는 1초마다 변경이 있는지 확인하는 구조
#
# 덕분에 프런트엔드는 계속 요청을 보내지 않아도 되고,
# 서버도 불필요한 polling(주기적 반복 요청)을 처리할 필요가 없다.
#
# 아래 헤더는 SSE에서 필수 요소다.
# - Content-Type: text/event-stream  → 브라우저에 "이 연결은 SSE다"라고 알림
# - Connection: keep-alive          → 연결을 닫지 않겠다는 의미
# 브라우저는 이를 기반으로 EventSource 객체를 통해 지속적으로 메시지를 수신한다.