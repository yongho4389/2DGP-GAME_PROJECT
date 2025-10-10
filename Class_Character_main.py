# 주인공 캐릭터 관련 클래스 및 함수 정의
from pico2d import *

class Character:
    def __init__(self):
        self.image = load_image('character_motion_sheets.png')
        self.frame = 0 # 프레임 진행 현황
        self.start_frame = 3 # 프레임 시작 인덱스
        self.end_frame = 3 # 프레임 종료 인덱스
        self.motion = 0  # 기본 서있기
        self.delay = 0.1 # 애니메이션별 프레임 딜레이
        self.time_count = 0.0 # 누적 시간 (이를 통해 각 동작별 프레임 전환 타이밍을 달리 할 수 있음) (동작에 따라 게임의 전체 딜레이가 바뀌는 것을 방지)
        self.end_motion = False # 동작 종료 여부

        self.Running = False # 달리기 상태 여부
        self.ignore_stand = False # 서있기 상태 무시 여부 (달리기 중 반대 방향키를 누른 다음 방향키를 떼었을 때 자연스럽게 움직이기 위함)
        self.Jumping = False # 점프 상태 여부
        self.Attacking = False # 공격 상태 여부
        self.Dashing = False # 대쉬 상태 여부

        # 위치
        self.x = 400
        self.y = 300
        # 크기
        self.width = 100
        self.height = 100
        # animation sheet 크기
        self.sheet_width = 2856
        self.sheet_height = 1910
        # 좌우 방향 (초기값은 오른쪽)
        self.dir = 1

    # 프레임 증가 함수
    def frame_update(self):
        frame_count = self.end_frame - self.start_frame + 1 # 얼마의 프레임으로 구성되는지 계산
        self.frame = (self.frame + 1) % frame_count # 해당 프레임 개수를 기반으로 프레임 업데이트
    # 프레임 전환 타이밍 계산
    def frame_change(self, delta_time):
        self.time_count += delta_time # 인자로 전달된 delta_time을 time_count에 누적
        if self.time_count >= self.delay: # time_count가 각 동작에게 부여된 delay와 같거나 더 크면 frame_update를 호출하여 frame을 전환. 이후 다시 time_count를 0으로 초기화하여 다음 프레임 전환까지 대기
            self.frame_update()
            self.time_count = 0.0
    # 달리기 모션
    def draw_running(self):
        self.frame = 0
        self.start_frame = 0
        self.end_frame = 7
        self.motion = 4
        self.delay = 0.1
        self.end_motion = False
        self.Running = True
    # 점프 및 착지 모션
    def draw_jump_and_down(self):
        self.frame = 0
        self.start_frame = 0
        self.end_frame = 3
        self.motion = 3
        self.delay = 0.2
        self.end_motion = False
        self.Jumping = True
    # 피격 모션
    def draw_attacked(self):
        self.frame = 0
        self.start_frame = 4
        self.end_frame = 5
        self.motion = 3
        self.delay = 0.5
        self.end_motion = False
    # 기본 공격 모션
    def draw_basic_attack(self):
        self.frame = 0
        self.start_frame = 0
        self.end_frame = 5
        self.motion = 2
        self.delay = 0.1
        self.end_motion = False
        self.Attacking = True
    # 스킬1 공격 모션
    def draw_skill1_attack(self):
        self.frame = 0
        self.start_frame = 0
        self.end_frame = 6
        self.motion = 1
        self.delay = 0.1
        self.end_motion = False
        self.Attacking = True
    # 대쉬 모션
    def draw_dash(self):
        self.frame = 0
        self.start_frame = 0
        self.end_frame = 0
        self.motion = 0
        self.delay = 0.1
        self.end_motion = False
        self.Dashing = True
    # 스킬2 공격 모션
    def draw_skill2_attack(self):
        self.frame = 0
        self.start_frame = 1
        self.end_frame = 2
        self.motion = 0
        self.delay = 0.5
        self.end_motion = False
        self.Attacking = True
    # 서있기 모션
    def draw_stand(self):
        self.frame = 0
        self.start_frame = 3
        self.end_frame = 3
        self.motion = 0
        self.delay = 0.0
        self.end_motion = False
        self.Running = False
        self.Jumping = False
        self.Attacking = False
        self.Dashing = False
    # 방향 전환
    def change_direction_left(self):
        self.dir = -1 # 좌측
    def change_direction_right(self):
        self.dir = 1 # 우측

    # 이동
    def character_move(self):
        self.x += self.dir * 10
    # 점프
    def character_jump(self):
        if self.frame < 3:
            self.y += 10
        else:
            self.y -= 60
            self.ignore_stand = False # 착지 후에 달리기가 멈추지 않는 버그 방지
    # 대쉬
    def character_dash(self):
        self.x += self.dir * 50

    # 캐릭터 그리기
    def draw_character(self):
        frame_index = self.start_frame + self.frame # start_frame과 frame을 활용하여 실제 시트에서 사용될 프레임 인덱스를 계산
        # 우측 방향
        if self.dir == 1:
            self.image.clip_draw(frame_index * (self.sheet_width // 8), (self.motion * self.sheet_height // 5), # 시트상 위치
                                 self.sheet_width // 8, self.sheet_height // 5, # 시트상 크기
                                 self.x, self.y, # 월드 위치
                                 self.width, self.height)
        # 좌측 방향
        else:
            self.image.clip_composite_draw(frame_index * (self.sheet_width // 8), (self.motion * self.sheet_height // 5), # 시트상 위치
                                 self.sheet_width // 8, self.sheet_height // 5, # 시트상 크기
                                 0, 'h',
                                 self.x, self.y, # 월드 위치
                                 self.width, self.height)
        # 동작이 끝났을 때 서있기 모션으로 전환 (단, 달리기 모션은 제외) (동작이 끝나고 즉시 바뀌기 보다는 잠깐의 딜레이 이후 바뀌도록 유도)
        # 처음은 end_motion이 False이므로 그냥 넘어가지만, 그 아래 코드에서 True로 바뀐다.
        # 이후 그 다음 프레임에 end_motion이 True이기에 draw_stand()이 호출되고, 다시 end_motion은 False가 된다.
        if self.end_motion:
            if self.Running and (self.Jumping or self.Dashing):
                self.Jumping = False
                self.Dashing = False
                self.draw_running()
            else:
                self.draw_stand()
            self.end_motion = False
        if frame_index >= self.end_frame and self.motion != 4:
            self.end_motion = True

# 캐릭터 객체 생성
character = Character()
character.draw_stand()