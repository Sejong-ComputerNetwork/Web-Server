자체 제작 HTTP 웹 서버 및 출석 관리 시스템
프로젝트 개요 (Project Overview)
Python의 Raw TCP 소켓을 사용하여 멀티스레드 HTTP 웹 서버를 구현했습니다. HTTP/1.1 프로토콜 표준을 준수하며, 실시간 데이터 스트리밍을 위한 Server-Sent Events(SSE)를 구현했습니다.

사용자 등록, 실시간 상태 모니터링, 관리자 대시보드를 포함한 포괄적인 학생 출석 관리 기능을 구현했습니다.

팀원 정보 (Team Information)
| 이름 | 학번 | 역할 및 기여 |
|:---:|:---:|:---|
| 김하은 | 22012293 | 백엔드 & API 통합: JSON 기반 CRUD 로직 구현, RESTful API 개발(GET/POST/PUT/DELETE), 프론트엔드-백엔드 통신 통합|
| 김윤희 | 21011628 | 기본 HTTP 프로토콜 웹서버 구현, 보여지는 화면 구현, 해당 화면에 API 연결|
| 이태규 | 20011635 | HTTP SSE를 활용한 실시간 출석 현황 웹페이지 구현, 유틸리티 함수/클래스 (DataHandler, FileHandler) 구현, 코드 정리 |
| 이다원 | 22011622 | 백엔드 & API 통합: JSON 기반 CRUD 로직 구현, RESTful API 개발(GET/POST/PUT/DELETE), 프론트엔드-백엔드 통신 통합 |