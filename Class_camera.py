# 카메라 관련 클래스 정의
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        # 현재 스테이지에 대한 시작과 끝 위치
        self.start_position = 0
        self.end_position = 800

camera = Camera()