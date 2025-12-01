import json
import os

class DataManager:
    def __init__(self, attendance_file="./db/student-info.json"):
        self.attendance_file = attendance_file 
        self.db_folder = "./db/" 
        self.attendance_data = [] 
        
        self._load_attendance() 

    # 파일 읽기
    def _load_attendance(self):
        if not os.path.exists(self.attendance_file):
            self.attendance_data = []
            self._save_attendance()
            print(f"[초기화] {self.attendance_file} 출석부를 새로 만들었습니다.")
        else:
            with open(self.attendance_file, 'r', encoding='utf-8') as f:
                self.attendance_data = json.load(f)
            print(f"[로드] 출석 기록을 불러왔습니다.")

    # 파일 저장
    def _save_attendance(self):
        with open(self.attendance_file, 'w', encoding='utf-8') as f:
            json.dump(self.attendance_data, f, indent=4, ensure_ascii=False)

    # 1. 학생 추가 (관리자용 - 이 함수가 없어서 에러가 났었습니다)
    def add_student(self, student_id, name):
        # 중복 확인
        for student in self.attendance_data:
            if student["id"] == str(student_id):
                return "DUPLICATE"
        
        # 새 학생 데이터 생성 (기본 출석값 False)
        new_entry = {
            "id": str(student_id),
            "name": name,
            "attend": False 
        }
        self.attendance_data.append(new_entry)
        self._save_attendance() # 저장 필수
        return "SUCCESS"

    # 2. 이름 & 학번 확인
    def verify_student(self, student_id, name):
        target_file = os.path.join(self.db_folder, f"{student_id}.json")
        if os.path.exists(target_file):
            try:
                with open(target_file, 'r', encoding='utf-8') as f:
                    user_info = json.load(f)
                    if user_info.get("name") == name:
                        return True 
            except Exception as e:
                print(f"[에러] 파일 읽기 실패: {e}")
                return False
        return False 

    # 3. 출석 체크 (학생용)
    def mark_attendance(self, student_id, name):
        for studentEntry in self.attendance_data:
            if studentEntry["id"] == str(student_id):
                if studentEntry["attend"]:
                    return "ALREADY"
                else:
                    studentEntry["attend"] = True
                    self._save_attendance()
                    return "SUCCESS"
            
        # 명단에 없으면 자동 추가하며 출석 처리
        new_entry = {
            "id": str(student_id),
            "name": name,
            "attend": True 
        }
        self.attendance_data.append(new_entry) 
        self._save_attendance()
        return "SUCCESS"

    # 4. 전체 데이터 조회
    def get_all_data(self):
        return self.attendance_data

    # 5. 학생 정보 수정 (관리자용)
    def update_student(self, student_id, new_name=None, new_attend=None):
        for student in self.attendance_data:
            if student["id"] == str(student_id):
                if new_name is not None:
                    student["name"] = new_name
                if new_attend is not None:
                    student["attend"] = new_attend
                
                self._save_attendance() 
                return "SUCCESS"
        return "NOT_FOUND"

    # 6. 학생 삭제 (관리자용)
    def delete_student(self, student_id):
        for i, student in enumerate(self.attendance_data):
            if student["id"] == str(student_id):
                del self.attendance_data[i] 
                self._save_attendance() 
                return "SUCCESS"
        return "NOT_FOUND"