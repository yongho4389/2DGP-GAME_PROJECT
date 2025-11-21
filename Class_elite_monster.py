from pico2d import *
from Class_camera import camera
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm. 즉, 1 meter 당 몇 픽셀인지 계산. 10pixel을 0.3(m)으로 나누어 1미터 당 픽셀 수를 구함
RUN_SPEED_KMPH = 5.0  # Km / Hour (여기서 현실적인 속도를 결정) (km/h)
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # Meter / Minute
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)  # Meter / Second
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  # 초당 몇 픽셀을 이동할지 결졍 (PPS) (이것이 속도가 됨)


# 기본 잡몹
class Elite_Monster:
    image = None
    UI_image = None

    def __init__(self, x, y, dir, stage, character):
        # 이미지 1번만 로드
        if Elite_Monster.image == None:
            Elite_Monster.image = load_image('./image_sheets/elite_monster_sheet.png')
        if Elite_Monster.UI_image == None:
            Elite_Monster.UI_image = load_image('./image_sheets/character_UI_sheet.png')
        self.x = x
        self.y = y
        self.stage = stage
        self.character = character
        self.width = 2184 // 7
        self.height = 849 // 3
        self.dir = dir
        self.rotate = 0.0
        self.cur_state = 'Moving'
        self.current_time = get_time()
        self.frame = 0
        self.motion = 2
        self.start_frame = 0
        self.end_frame = 6
        self.end_motion = False
        self.TIME_PER_ACTION = 1  # 한 동작을 수행하는데 걸리는 시간 (초)
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION  # 초당 몇 동작을 수행하는지

        self.MAX_HP = self.stage.stage_level * 100 + 100
        self.HP = self.MAX_HP
        self.damage = self.stage.stage_level * 20 + 20
    
    def frame_update(self):
        frame_count = self.end_frame - self.start_frame + 1 # 얼마의 프레임으로 구성되는지 계산
        self.frame = (self.frame + frame_count * self.ACTION_PER_TIME * game_framework.frame_time) % frame_count

    def moving(self):
        self.motion = 2
        self.end_frame = 6
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.x < camera.start_position + 200 or self.x > camera.end_position - 200:
            self.dir *= -1

    def Attacked(self):
        self.motion = 0
        self.end_frame = 1
        self.rotate = 45.0 * self.dir
        if get_time() - self.current_time > 0.5: # 동작 종료 타이밍 별도 설정
            self.cur_state = 'Moving'
            self.frame = 0
            self.rotate = 0.0
            self.end_motion = False

    def Attacking(self):
        self.motion = 1
        self.end_frame = 6
        pass

    def update(self):
        self.frame_update()
        if (self.cur_state == 'Moving'):
            self.motion = 2
            self.end_frame = 7
            self.moving()
        elif (self.cur_state == 'Attacked'):
            self.motion = 0
            self.end_frame = 2
            self.Attacked()
        elif (self.cur_state == 'Attacking'):
            self.motion = 1
            self.end_frame = 7
            self.Attacking()

    def end_motion_check(self, frame_index):
        # 모션이 끝난 경우 다시 움직이는 동작으로 전환
        if self.end_motion:
            self.cur_state = 'Moving'
            self.frame = 0
            self.end_motion = False
        # 모션이 끝났으면 플래그 활성화 (피격 시는 별도 처리)
        elif frame_index >= self.end_frame and not self.motion == 0:
            self.end_motion = True

    def draw(self):
        frame_index = self.start_frame + int(self.frame)
        if self.dir == 1:
            direction = ''
        else:
            direction = 'h'
        self.image.clip_composite_draw(frame_index * self.width, (self.motion * self.height),
                                       # 시트상 위치
                                       self.width, self.height,  # 시트상 크기
                                       self.rotate, direction,
                                       self.x - camera.x, self.y,  # 월드 위치
                                       100, 100)
        self.end_motion_check(frame_index)
        draw_rectangle(*self.get_screen_bb())

        # 체력바
        hp_length = 400 * (self.HP / self.MAX_HP)  # HP바 길이가 출력되는 부분 100% 기준으로 계산됨. (최대 400)
        self.UI_image.clip_draw(2720 // 5, 0, 2720 // 5, 185, self.x - camera.x, self.y + 50, hp_length, 100)  # HP 바

    # 화면용 바운딩 박스
    def get_screen_bb(self):
        # 렌더링용(화면 좌표)
        x1, y1, x2, y2 = self.get_bb()
        return x1 - camera.x, y1, x2 - camera.x, y2

    def get_bb(self):
        xb = self.width / 8
        yb = self.height / 8
        return self.x - xb, self.y - yb, self.x + xb, self.y + yb

    def handle_collision(self, group, other):
        if group == 'character:monster':
            pass
        elif group == 'attack:monster' and other.is_attack:
            other.is_attack = False  # 공격 판정은 한 번만 되도록 하며, 몬스터에게 실제 변화가 일어났을 때 공격 판정이 적용되었음을 알림
            self.HP -= other.damage
            # 피격 시 적이 플레이어에게 달려들도록 방향 변경
            if other.adir == self.dir:
                self.dir *= -1
            # 피격 상태로의 변경
            self.cur_state = 'Attacked'
            self.current_time = get_time()
            # 피격 시 경직 추가 필요 (일반 몹이기 때문)
            if self.HP <= 0:  # 사망 시 삭제
                game_world.remove_object(self)
                self.character.Gold += 10 + (self.stage.stage_level * 10)  # 골드 획득
                self.character.EXP += 5 + (self.stage.stage_level * 5)  # 경험치 획득
