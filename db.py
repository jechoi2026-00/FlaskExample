import pymysql
from datetime import datetime

class Database:
    """데이터베이스 연결 및 관리 클래스"""

    def __init__(self, host='localhost', user='root', password='', database='bmi_db', charset='utf8mb4'):
        """
        데이터베이스 초기화

        Args:
            host (str): 데이터베이스 호스트
            user (str): 데이터베이스 사용자
            password (str): 데이터베이스 비밀번호
            database (str): 데이터베이스 이름
            charset (str): 문자 인코딩
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.connection = None

    def connect(self):
        """데이터베이스 연결"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("MariaDB 데이터베이스 연결 성공")
        except pymysql.Error as e:
            print(f"MariaDB 데이터베이스 연결 실패: {e}")
            raise

    def disconnect(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            print("MariaDB 데이터베이스 연결 종료")

    def create_table(self):
        """테이블 생성"""
        sql = """
        CREATE TABLE IF NOT EXISTS bmi_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            weight FLOAT NOT NULL,
            height FLOAT NOT NULL,
            bmi FLOAT NOT NULL,
            status VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
                print("테이블 생성 완료")
        except pymysql.Error as e:
            print(f"테이블 생성 실패: {e}")

    def insert_bmi_result(self, weight, height, bmi, status):
        """BMI 결과 저장"""
        sql = """
        INSERT INTO bmi_results (weight, height, bmi, status)
        VALUES (%s, %s, %s, %s)
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (weight, height, bmi, status))
                self.connection.commit()
                return cursor.lastrowid
        except pymysql.Error as e:
            print(f"데이터 삽입 실패: {e}")
            return None

    def get_all_results(self):
        """모든 BMI 결과 조회"""
        sql = """
        SELECT * FROM bmi_results ORDER BY created_at DESC
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except pymysql.Error as e:
            print(f"데이터 조회 실패: {e}")
            return []

    def get_result_by_id(self, result_id):
        """특정 ID의 BMI 결과 조회"""
        sql = """
        SELECT * FROM bmi_results WHERE id = %s
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (result_id,))
                result = cursor.fetchone()
                return result
        except pymysql.Error as e:
            print(f"데이터 조회 실패: {e}")
            return None

    def delete_result(self, result_id):
        """BMI 결과 삭제"""
        sql = """
        DELETE FROM bmi_results WHERE id = %s
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (result_id,))
                self.connection.commit()
                return True
        except pymysql.Error as e:
            print(f"데이터 삭제 실패: {e}")
            return False
