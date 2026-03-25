class BMI:
    """BMI 계산 클래스"""
    
    def __init__(self, weight, height):
        """
        BMI 계산을 위한 초기화
        
        Args:
            weight (float): 체중 (kg)
            height (float): 신장 (cm)
        """
        self.weight = weight
        self.height = height / 100  # cm를 m로 변환
    
    def calculate_bmi(self):
        """BMI 계산"""
        if self.height <= 0:
            raise ValueError("신장은 0보다 커야 합니다")
        if self.weight <= 0:
            raise ValueError("체중은 0보다 커야 합니다")
        
        bmi = self.weight / (self.height ** 2)
        return round(bmi, 2)
    
    def get_status(self, bmi):
        """BMI 상태 판정"""
        if bmi < 18.5:
            return "저체중"
        elif bmi < 25:
            return "정상체중"
        elif bmi < 30:
            return "과체중"
        else:
            return "비만"
    
    def get_full_result(self):
        """BMI 계산 및 상태 반환"""
        bmi = self.calculate_bmi()
        status = self.get_status(bmi)
        return {
            'weight': self.weight,
            'height': self.height * 100,
            'bmi': bmi,
            'status': status
        }
