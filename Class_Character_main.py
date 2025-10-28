# 주인공 캐릭터 관련 클래스 및 함수 정의
from pico2d import *
from Class_camera import camera
from Class_skills import Skills
import game_world

class Character:
    def __init__(self):
        # 생성 이미지
        self.image = load_image('character_motion_sheets.png')
        self.UI_image = load_image('character_UI_sheet.png')
        self.font = load_font('C:\Windows\Fonts\malgun.ttf', 20)
        # 애니메이션 관련 변수
        self.frame = 0 # 프레임 진행 현황
        self.start_frame = 3 # 프레임 시작 인덱스
        self.end_frame = 3 # 프레임 종료 인덱스
        self.motion = 0  # 기본 서있기
        self.delay = 0.1 # 애니메이션별 프레임 딜레이
        self.time_count = 0.0 # 누적 시간 (이를 통해 각 동작별 프레임 전환 타이밍을 달리 할 수 있음) (동작에 따라 게임의 전체 딜레이가 바뀌는 것을 방지)
        self.end_motion = False # 동작 종료 여부

        # 상태 관련 변수
        self.pre_state = 'None' # 이전 상태
        self.cur_state = 'Standing' # 현재 상태
        self.ignore_stand = False # 서있기 상태 무시 여부 (달리기 중 반대 방향키를 누른 다음 방향키를 떼었을 때 자연스럽게 움직이기 위함)
        self.skill1_Attacking = False
        self.skill2_Attacking = False
        self.attack = None

        # 위치
        self.x = 400
        self.y = 125
        # 크기
        self.width = 200
        self.height = 200
        # 히트 박스
        self.hx1 = self.x - 50
        self.hy1 = self.y + 50
        self.hx2 = self.x + 50
        self.hy2 = self.y - 50
        # animation sheet 크기
        self.sheet_width = 2856
        self.sheet_height = 1910
        # 좌우 방향 (초기값은 오른쪽)
        self.dir = 1

        # 재화
        self.Gold = 1000
        self.Max_EXP = 100 # 최대 경험치
        self.EXP = 30  # 경험치

        # 캐릭터 능력치
        self.Max_HP = 100  # 최대 체력
        self.HP = 25  # 체력
        self.LV = 1     # 레벨
        self.basic_damage = 10  # 기본 공격 데미지
        self.basic_range = 40  # 기본 공격 사거리
        self.skill1_damage = 30  # 스킬1 데미지
        self.skill1_range = 20  # 스킬1 사거리
        self.skill2_damage = 25  # 스킬2 데미지
        self.skill2_range = 200  # 스킬2 사거리

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
    def start_running(self):
        self.frame = 0
        self.start_frame = 0
        self.end_frame = 7
        self.motion = 4
        self.delay = 0.1
        self.end_motion = False
    # 점프 및 착지 모션
    def start_jump_and_down(self):
        self.frame = 0
        self.start_frame = 0
        self.end_frame = 3
        self.motion = 3
        self.delay = 0.2
        self.end_motion = False
    # 피격 모션
    def start_attacked(self):
        self.frame = 0
        self.start_frame = 4
        self.end_frame = 5
        self.motion = 3
        self.delay = 0.5
        self.end_motion = False
    # 기본 공격 모션
    def start_basic_attack(self):
        self.frame = 0
        self.start_frame = 0
        self.end_frame = 5
        self.motion = 2
        self.delay = 0.1
        self.end_motion = False
        self.skill1_Attacking = False
        self.skill2_Attacking = False
        self.attack = Skills(self, 0)
    # 스킬1 공격 모션
    def start_skill1_attack(self):
        self.frame = 0
        self.start_frame = 0
        self.end_frame = 6
        self.motion = 1
        self.delay = 0.1
        self.end_motion = False
        self.skill1_Attacking = False
        self.attack = Skills(self, 1)
    # 대쉬 모션
    def start_dash(self):
        self.frame = 0
        self.start_frame = 0
        self.end_frame = 0
        self.motion = 0
        self.delay = 0.1
        self.end_motion = False
    # 스킬2 공격 모션
    def start_skill2_attack(self):
        self.frame = 0
        self.start_frame = 1
        self.end_frame = 2
        self.motion = 0
        self.delay = 0.5
        self.end_motion = False
        self.skill2_Attacking = False
        self.attack = Skills(self, 2)
    # 서있기 모션
    def start_stand(self):
        self.frame = 0
        self.start_frame = 3
        self.end_frame = 3
        self.motion = 0
        self.delay = 0.0
        self.end_motion = False
    # 방향 전환
    def change_direction_left(self):
        self.dir = -1 # 좌측
    def change_direction_right(self):
        self.dir = 1 # 우측

    # 화면 밖으로 나가는지 체크
    def out_of_position(self):
        if self.x < camera.start_position + 50:
            self.x = camera.start_position + 50
        if self.x > camera.end_position - 50:
            self.x = camera.end_position - 50
    # 이동
    def character_move(self):
        self.x += self.dir * 10
        self.out_of_position()
    # 점프
    def character_jump(self):
        if self.frame < 3:
            self.y += 20
        else:
            self.y -= 60
    # 지상 유지
    def character_land(self):
        if self.y > 125:
            self.y -= 20
        # 맵 벗어남 방지
        if self.y < 125:
            self.y = 125
    # 대쉬
    def character_dash(self):
        self.x += self.dir * 50
        self.out_of_position()

    # 카메라 위치를 캐릭터 위치에 맞게 최신화
    def setting_camera(self):
        if camera.x >= camera.start_position and camera.x <= camera.end_position - 800:
            camera.x = self.x - 400
        # 카메라 맵 벗어나는 경우 보정
        if camera.x < 0:
            camera.x = 0
        if camera.x > camera.end_position - 800:
            camera.x = camera.end_position - 800

    # 하나의 애니메이션이 끝났을 경우 처리
    def end_motion_check(self, frame_index):
        # 동작이 끝났을 때 서있기 모션으로 전환 (단, 달리기 모션은 제외) (동작이 끝나고 즉시 바뀌기 보다는 잠깐의 딜레이 이후 바뀌도록 유도)
        # 처음은 end_motion이 False이므로 그냥 넘어가지만, 그 아래 코드에서 True로 바뀐다.
        # 이후 그 다음 프레임에 end_motion이 True이기에 draw_stand()이 호출되고, 다시 end_motion은 False가 된다.
        if self.end_motion:
            if self.pre_state == 'Running' and (
                    self.cur_state == 'Jumping' or self.cur_state == 'Dashing' or self.cur_state == 'Attacking'):
                self.start_running()
                self.pre_state = self.cur_state
                self.cur_state = 'Running'
            else:
                self.start_stand()
                self.pre_state = self.cur_state
                self.cur_state = 'Standing'
            self.end_motion = False
        if frame_index >= self.end_frame and self.motion != 4:
            self.end_motion = True

    # 캐릭터 상태 업데이트
    def update(self):
        # 히트 박스
        hitbox_size = 50
        self.hx1 = self.x - hitbox_size
        self.hy1 = self.y + hitbox_size
        self.hx2 = self.x + hitbox_size
        self.hy2 = self.y - hitbox_size
        self.frame_change(0.1)  # 프레임 전환 처리
        if self.HP <= 0:
            pass
        if self.EXP >= self.Max_EXP:
            pass
        # 상태에 따른 동작 처리
        # 달리기
        if self.cur_state == 'Running':
            self.character_move()
            self.character_land()
        # 서기
        elif self.cur_state == 'Standing':
            self.character_land()
        # 점프
        elif self.cur_state == 'Jumping':
            self.character_jump()
            if self.pre_state == 'Running':  # 캐릭터가 뛰는 중이었다면 이동도 같이 수행하기
                self.character_move()
        # 대쉬
        if self.cur_state == 'Dashing':
            self.character_dash()
        # 공격
        if self.cur_state == 'Attacking':
            # 기본 공격
            if self.attack.attack_version == 0 and self.frame == 3:  # 프레임 3에 공격 수행
                game_world.add_object(self.attack, 1)
            # 스킬1
            elif self.attack.attack_version == 1 and self.frame == 5 and self.motion == 1:  # 프레임 5에 공격 수행
                game_world.add_object(self.attack, 1)
                self.skill1_Attacking = True
            # 스킬2
            elif self.attack.attack_version == 2 and self.frame == 1 and self.motion == 0:  # 프레임 1에 공격 수행
                game_world.add_object(self.attack, 1)
                self.skill2_Attacking = True
    # UI 그리기
    def draw_UI(self):
        w = 2720 // 5  # 544
        h = 185
        sx = 130
        sy = 550
        hp_length = 400 * (self.HP / self.Max_HP) # HP바 길이가 출력되는 부분 100% 기준으로 계산됨. (최대 400)
        exp_length = 190 * (self.EXP / self.Max_EXP) # 경험치 바 길이 계산 (최대 190)
        hp_pos = 89 * (self.HP / self.Max_HP) # 최대 32, 최소 -57
        exp_pos = 89 * (self.EXP / self.Max_EXP)  # 최대 32, 최소 -57
        self.UI_image.clip_draw(0, 0, w, h, sx, sy, 400, 100) # HP 바 테두리
        self.UI_image.clip_draw(w * 1, 0, w, h, sx + (hp_pos - 57), sy + 21, hp_length, 100) # HP 바
        self.UI_image.clip_draw(w * 2, 0, w, h, sx + (exp_pos - 57), sy + 8, exp_length, 50) # 경험치 바
        self.UI_image.clip_draw(w * 3, 0, w, h, sx - 105, sy + 20, 200, 100)  # 레벨
        self.font.draw(sx - 90, sy + 22, f'{self.LV}', (255, 255, 255))
        self.UI_image.clip_draw(w * 4, 0, w, h, sx - 100, sy - 50, 250, 100)  # 골드 보유량
        self.font.draw(sx - 75, sy - 50, f'Gold: {self.Gold}', (255, 255, 0))
    # 캐릭터 그리기
    def draw(self):
        self.setting_camera()
        frame_index = self.start_frame + self.frame # start_frame과 frame을 활용하여 실제 시트에서 사용될 프레임 인덱스를 계산
        # 우측 방향
        if self.dir == 1:
            self.image.clip_draw(frame_index * (self.sheet_width // 8), (self.motion * self.sheet_height // 5), # 시트상 위치
                                 self.sheet_width // 8, self.sheet_height // 5, # 시트상 크기
                                 self.x - camera.x, self.y, # 월드 위치
                                 self.width, self.height)
        # 좌측 방향
        else:
            self.image.clip_composite_draw(frame_index * (self.sheet_width // 8), (self.motion * self.sheet_height // 5), # 시트상 위치
                                 self.sheet_width // 8, self.sheet_height // 5, # 시트상 크기
                                 0, 'h',
                                 self.x - camera.x, self.y, # 월드 위치
                                 self.width, self.height)
        # 애니메이션 종료 체크
        self.end_motion_check(frame_index)
        self.draw_UI()
