from pico2d import *
from Class_camera import camera
import game_world
import game_framework
from game_world import PIXEL_PER_METER
import math

ENERGY_SPEED_KMPH = 30.0 # Km / Hour (여기서 현실적인 속도를 결정) (km/h)
ENERGY_SPEED_MPM = (ENERGY_SPEED_KMPH * 1000.0 / 60.0) # Meter / Minute
ENERGY_SPEED_MPS = (ENERGY_SPEED_MPM / 60.0) # Meter / Second
ENERGY_SPEED_PPS = (ENERGY_SPEED_MPS * PIXEL_PER_METER) # 초당 몇 픽셀을 이동할지 결졍 (PPS) (이것이 속도가 됨)


# 기본 잡몹
class Boss_skills:
    image = None
    UI_image = None

    def __init__(self, x, y, type, boss):
        # 이미지 1번만 로드
        if Boss_skills.image == None:
            Boss_skills.image = load_image('./image_sheets/boss_effect_sheet.png')
        self.skill_Activate_time = get_time()
        self.is_attack = True  # 공격 여부 결정 (필드에 남아있어도 몬스터 당 한 번만 공격하도록)
        self.ax = x
        self.ay = y
        self.boss = boss
        self.type = type
        self.width = 516 // 3
        self.height = 118
        self.turning = 0
        self.size = 100

        if type == 0:
            self.damage = self.boss.energy_damage
        elif type == 1:
            self.damage = self.boss.bomb_damage
            self.size = 25
        elif type == 2:
            self.damage = self.boss.energy_damage
            self.turning = math.radians(90)

        # 공격 이펙트 그리기

    def draw(self):
        self.image.clip_composite_draw(self.type * self.width, 0,
                                       self.width, self.height,
                                       self.turning, '',
                                       self.ax - camera.x, self.ay,
                                       self.size, self.size)
        draw_rectangle(*self.get_screen_bb())
        # 스킬 지속 시간 처리

    def update(self):
        if self.type == 0:
            if get_time() - self.skill_Activate_time >= 5.0: # 5초 후 삭제
                game_world.remove_object(self)
            else:
                self.ax -= ENERGY_SPEED_PPS * game_framework.frame_time # 좌측으로 이동
        if self.type == 1:
            if get_time() - self.skill_Activate_time >= 2.0: # 3초 후 삭제
                game_world.remove_object(self)
            else:
                self.size += 75 * game_framework.frame_time  # 크기 증가
        elif self.type == 2:
            if get_time() - self.skill_Activate_time >= 5.0: # 5초 후 삭제
                game_world.remove_object(self)
            else:
                self.ay -= ENERGY_SPEED_PPS * game_framework.frame_time # 아래로 하강

    def get_screen_bb(self):
        # 렌더링용(화면 좌표)
        x1, y1, x2, y2 = self.get_bb()
        return x1 - camera.x, y1, x2 - camera.x, y2

    def get_bb(self):
        if self.type == 0 or self.type == 2:
            xb = 10
            yb = 10
        elif self.type == 1:
            xb = self.size / 4
            yb = self.size / 4
        return self.ax - xb, self.ay - yb, self.ax + xb, self.ay + yb

    def handle_collision(self, group, other):
        if group == 'attack:monster' and self.is_attack:
            self.skill_Activate_time = 0  # 충돌 후 바로 삭제되도록 시간 초기화 (update에서 처리)

