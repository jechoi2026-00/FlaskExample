# BMI 계산기 웹 애플리케이션

체중과 신장을 입력하면 BMI를 계산하고, 결과를 데이터베이스에 저장한 후 결과 페이지를 보여주는 Flask 웹 애플리케이션입니다.

## 프로젝트 구조

```
bmi_calculator/
├── app.py                    # Flask 웹 애플리케이션 메인 파일
├── bmi.py                    # BMI 계산 클래스
├── db.py                     # 데이터베이스 연결 및 관리 클래스
├── requirements.txt          # 필수 패키지
├── templates/
│   ├── index.html           # 체중, 신장 입력 폼 페이지
│   ├── result.html          # BMI 계산 결과 페이지
│   └── history.html         # 과거 계산 기록 페이지
└── static/
    └── style.css            # 웹사이트 스타일
```

## 주요 기능

1. **app.py**: Flask 웹 애플리케이션의 주요 파일로, 라우트와 요청 처리를 담당합니다.
2. **bmi.py**: BMI 계산과 관련된 로직을 포함하는 클래스를 정의합니다.
3. **db.py**: 데이터베이스 연결 및 종료 클래스를 정의합니다.
4. **templates/index.html**: 사용자가 체중과 신장을 입력할 수 있는 폼을 제공합니다.
5. **templates/result.html**: 계산된 BMI 결과를 표시합니다.
6. **templates/history.html**: 입력된 값을 저장하여 표시합니다.
7. **static/style.css**: 웹 페이지의 스타일을 정의합니다.

## 설치 및 실행

### 1. MySQL 데이터베이스 설정

먼저 MySQL에서 데이터베이스를 생성합니다:

```sql
CREATE DATABASE bmi_db;
CREATE USER 'root'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON bmi_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 정보 설정

`db.py`와 `app.py` 파일에서 다음 정보를 본인의 MySQL 설정에 맞게 수정하세요:

```python
db = Database(
    host='localhost',      # MySQL 호스트
    user='root',           # MySQL 사용자명
    password='',           # MySQL 비밀번호 (있는 경우)
    database='bmi_db'      # 데이터베이스명
)
```

### 4. 애플리케이션 실행

```bash
python app.py
```

### 5. 웹 브라우저에서 접속

```
http://localhost:5000
```

## 사용 방법

1. **계산하기 페이지**: 체중(kg)과 신장(cm)을 입력하고 "BMI 계산" 버튼을 클릭합니다.
2. **결과 페이지**: 계산된 BMI와 건강 상태(저체중, 정상체중, 과체중, 비만)가 표시됩니다.
3. **히스토리 페이지**: 과거에 계산한 모든 기록을 확인하고 삭제할 수 있습니다.

## BMI 분류 기준

| 분류 | BMI 범위 |
|------|---------|
| 저체중 | BMI < 18.5 |
| 정상체중 | 18.5 ≤ BMI < 25 |
| 과체중 | 25 ≤ BMI < 30 |
| 비만 | BMI ≥ 30 |

## 필수 패키지

- Flask==2.3.3
- Werkzeug==2.3.7
- pymysql==1.1.0

## 주의사항

- MySQL 서버가 실행 중이어야 합니다.
- 데이터베이스 접속 정보가 올바르게 설정되어야 합니다.
- 브라우저에서 JavaScript가 활성화되어 있어야 합니다.

## 라이선스

이 프로젝트는 자유롭게 사용할 수 있습니다.
