from flask import Flask, render_template, request, redirect, url_for, flash 
import os
from bmi import BMI
from db import Database

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

def get_db_connection():
    """환경변수 기반 DB 연결 생성"""
    return Database(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '123'),
        database=os.getenv('DB_NAME', 'bmi_db'),
        port=int(os.getenv('DB_PORT', '3306'))
    )

# 데이터베이스 초기화
db = get_db_connection()

def init_db():
    """데이터베이스 초기화"""
    try:
        db.connect()
        db.create_table()
    except Exception as e:
        print(f"데이터베이스 초기화 실패: {e}")

@app.route('/')
def index():
    """홈 페이지"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """BMI 계산 및 결과 저장"""
    try:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        
        # 입력값 검증
        if weight <= 0 or height <= 0:
            flash('체중과 신장은 0보다 커야 합니다.', 'error')
            return redirect(url_for('index'))
        
        # BMI 계산
        bmi_calculator = BMI(weight, height)
        result = bmi_calculator.get_full_result()
        
        # 데이터베이스에 저장
        db_connection = get_db_connection()
        db_connection.connect()
        result_id = db_connection.insert_bmi_result(
            result['weight'],
            result['height'],
            result['bmi'],
            result['status']
        )
        db_connection.disconnect()
        
        if result_id:
            return render_template('result.html', 
                                 weight=result['weight'],
                                 height=result['height'],
                                 bmi=result['bmi'],
                                 status=result['status'],
                                 result_id=result_id)
        else:
            flash('데이터 저장에 실패했습니다.', 'error')
            return redirect(url_for('index'))
    
    except ValueError:
        flash('체중과 신장을 올바르게 입력해주세요.', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'오류가 발생했습니다: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/history')
def history():
    """히스토리 페이지"""
    try:
        db_connection = get_db_connection()
        db_connection.connect()
        results = db_connection.get_all_results()
        db_connection.disconnect()
        return render_template('history.html', results=results)
    except Exception as e:
        flash(f'히스토리 조회 실패: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/delete/<int:result_id>', methods=['POST'])
def delete_record(result_id):
    """기록 삭제"""
    try:
        db_connection = get_db_connection()
        db_connection.connect()
        if db_connection.delete_result(result_id):
            flash('기록이 삭제되었습니다.', 'success')
        else:
            flash('기록 삭제에 실패했습니다.', 'error')
        db_connection.disconnect()
    except Exception as e:
        flash(f'오류가 발생했습니다: {str(e)}', 'error')
    
    return redirect(url_for('history'))

@app.errorhandler(404)
def not_found(error):
    """404 에러 처리"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 에러 처리"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='localhost', port=5000)
