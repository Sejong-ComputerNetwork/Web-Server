import socket
import threading
import logging
import os
import json
import urllib.parse
from DataManager import DataManager
from DataHandler import DataHandler
import boardHandler as boardHandler
from FileHandler import getFileAsString, load_html;

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# [전역 객체 생성]
dataHandler = DataHandler()   
manager = DataManager()      

def parse_http_request(data):
    lines = data.split("\r\n")
    request_line = lines[0]
    if not request_line: return "GET", "/", ""
    
    parts = request_line.split()
    method = parts[0]
    path = parts[1]
    
    body = ""
    if method in ["POST", "PUT", "DELETE"]:
        if "\r\n\r\n" in data:
            body = data.split("\r\n\r\n", 1)[1]
    return method, path, body

def build_response(body, status="200 OK", content_type="text/html"):
    response = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}; charset=utf-8\r\n"
        f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        "\r\n"
        f"{body}"
    )
    return response


# [라우팅 함수] 모든 기능 통합 (GET, POST, PUT, DELETE)

def route_http(method, path, body):
    
    # 1. 화면 보여주기 (메인, 관리자, CSS)
    if method == "GET" and path == "/":
        return load_html("index.html"), "200 OK"
    elif method == "GET" and path == "/admin.html":
        return load_html("admin.html"), "200 OK"
    elif method == "GET" and path.endswith(".css"):
        try:
            filename = path.lstrip("/")
            css_path = os.path.join("./templates", filename)
            with open(css_path, "r", encoding="utf-8") as f:
                return f.read(), "200 OK", "text/css"
        except:
            return "", "404 Not Found", "text/css"

    # 2. 출석 체크 API (POST /api/attendance)
    elif method == "POST" and path == "/api/attendance":
        try:
            if not body: return json.dumps({"message": "No data"}), "400 Bad Request", "application/json"
            data = json.loads(body)
            
            result = manager.mark_attendance(data.get("id"), data.get("name"))
            
            if result == "SUCCESS":
                return json.dumps({"message": "출석 성공"}), "200 OK", "application/json"
            elif result == "ALREADY":
                return json.dumps({"message": "이미 출석했습니다."}), "202 Accepted", "application/json"
            else:
                return json.dumps({"message": "정보 불일치"}), "401 Unauthorized", "application/json"
        except Exception as e:
            return json.dumps({"message": f"Error: {e}"}), "500 Error", "application/json"

    # 3. [관리자용 API] 조회, 추가, 수정(PUT), 삭제(DELETE)
    elif path == "/api/students":
        
        # A. 조회 (GET)
        if method == "GET":
            return json.dumps(manager.get_all_data(), ensure_ascii=False), "200 OK", "application/json"

        # B. 추가 (POST)
        elif method == "POST":
            try:
                data = json.loads(body)
                result = manager.add_student(data.get("id"), data.get("name"))
                if result == "SUCCESS":
                    return json.dumps({"message": "추가 성공"}), "201 Created", "application/json"
                elif result == "DUPLICATE":
                    return json.dumps({"message": "이미 존재하는 학번"}), "409 Conflict", "application/json"
                else:
                    return json.dumps({"message": "실패"}), "400 Bad Request", "application/json"
            except:
                return json.dumps({"message": "Error"}), "500 Error", "application/json"

        # C.  수정 (PUT)
        elif method == "PUT":
            try:
                data = json.loads(body)
                # update_student 함수가 DataManager에 있어야 함!
                result = manager.update_student(data.get("id"), data.get("name"), data.get("attend"))
                
                if result == "SUCCESS":
                    return json.dumps({"message": "수정 성공"}), "200 OK", "application/json"
                else:
                    return json.dumps({"message": "학생 없음"}), "404 Not Found", "application/json"
            except:
                return json.dumps({"message": "Error"}), "500 Error", "application/json"

        # D. 삭제 (DELETE)
        elif method == "DELETE":
            try:
                data = json.loads(body)
                # delete_student 함수가 DataManager에 있어야 함!
                result = manager.delete_student(data.get("id"))
                
                if result == "SUCCESS":
                    return json.dumps({"message": "삭제 성공"}), "200 OK", "application/json"
                else:
                    return json.dumps({"message": "학생 없음"}), "404 Not Found", "application/json"
            except:
                return json.dumps({"message": "Error"}), "500 Error", "application/json"

    elif method == "POST" and path == "/submit":
        params = urllib.parse.parse_qs(body)
        name = params.get("name", [""])[0]
        student_id = params.get("student_id", [""])[0]
        try:
            dataHandler.addNewEntry(student_id, name)
        except:
            dataHandler.editEntry(student_id, name)
        html = load_html("submit.html")
        html = html.replace("{name}", name).replace("{student_id}", student_id)
        return html, "200 OK"
    
    elif path.startswith("/api/user"):
        response_dict = {}
        try:
            if method == "GET":
                response_dict = {"message":"GET: 전체 유저 목록"}
                status = "200 OK"
        except:
            pass
        return json.dumps(response_dict, ensure_ascii=False), "200 OK", "application/json"

    return load_html("404.html"), "404 Not Found"

def handle_client(client_socket, client_address):
    logging.info(f"Client connected: {client_address}")
    try:
        data = client_socket.recv(4096).decode("utf-8", errors="ignore")
        if not data:
            client_socket.close()
            return

        method, path, body = parse_http_request(data)
        logging.info(f"{method} {path}")


        if path == "/boardEvent":
            boardHandler.handleBoard(client_socket)
        elif path == "/board":
            body = load_html(path.lstrip("/") + "/board.html") 
            response = build_response(body, content_type="text/html; charset=utf-8")

            client_socket.sendall(response.encode())
            client_socket.close() 
        elif path == "/board.js":
            body = getFileAsString("./templates/board/board.js") 
            response = build_response(body, content_type="text/javascript; charset=utf-8")
            client_socket.sendall(response.encode())
            client_socket.close() 
        else:
            result = route_http(method, path, body)
            # 3개 반환값 처리 (JSON 대응)
            if len(result) == 2:
                body, status = result
                content_type = "text/html"
            else:
                body, status, content_type = result

            response = build_response(body, status, content_type)
            client_socket.sendall(response.encode("utf-8"))
    except Exception as e:
        logging.error(f"클라이언트 처리 중 오류: {e}")
    finally:
        client_socket.close()


def main():
    HOST = '127.0.0.1' 
    PORT = 1234
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    logging.info(f"HTTP Server running on http://{HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    except KeyboardInterrupt:
        logging.info("서버 종료 중...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()