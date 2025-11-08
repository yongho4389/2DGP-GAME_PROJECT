from pico2d import *
from Class_camera import camera
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm. 즉, 1 meter 당 몇 픽셀인지 계산. 10pixel을 0.3(m)으로 나누어 1미터 당 픽셀 수를 구함
SKILL1_SPEED_KMPH = 2.0 # Km / Hour (여기서 현실적인 속도를 결정) (km/h)
SKILL1_SPEED_MPM = (SKILL1_SPEED_KMPH * 1000.0 / 60.0) # Meter / Minute
SKILL1_SPEED_MPS = (SKILL1_SPEED_MPM / 60.0) # Meter / Second
SKILL1_SPEED_PPS = (SKILL1_SPEED_MPS * PIXEL_PER_METER) # 초당 몇 픽셀을 이동할지 결졍 (PPS) (이것이 속도가 됨)

class Skills:
    image = None
    def __init__(self, character, attack_version):
        self.character = character
        self.attack_version = attack_version
        if Skills.image == None:
            Skills.image = load_image('./image_sheets/attack_effect_sheets.png')

        self.turning = 0.0
        self.skill_Activate_time = get_time()
        self.adir = self.character.dir

        if attack_version == 0:
            self.damage = self.character.basic_damage
            self.range = self.character.basic_range
            self.ax = self.character.x + (self.character.dir * (20 + self.range // 2))
            self.ay = self.character.y

        elif attack_version == 1:
            self.damage = self.character.skill1_damage
            self.range = self.character.skill1_range
            self.ax = self.character.x + (self.character.dir * (20 + self.range // 2))
            self.ay = self.character.y

        elif attack_version == 2:
            self.damage = self.character.skill2_damage
            self.range = self.character.skill2_range
            self.ax = self.character.x
            self.ay = self.character.y

        self.hitbox = (self.ax - (self.range // 2), self.ay - (self.range // 2),
                       self.ax + (self.range // 2), self.ay + (self.range // 2))

    # 공격 이펙트 그리기
    def draw(self):
        # 카메라 위치 최신화
        self.character.setting_camera()
        skill1_scale = 0
        if self.attack_version == 1:
            skill1_scale = 200
        else:
            skill1_scale = 0
        if self.adir == 1:
            self.image.clip_composite_draw(self.attack_version * (564 // 3), 0,
                                                  564 // 3, 188,
                                                  self.turning, '',
                                                  self.ax - camera.x, self.ay,
                                                  100 + self.range, 100 + self.range + skill1_scale)
        else:
            self.image.clip_composite_draw(self.attack_version * (564 // 3), 0,
                                                  564 // 3, 188,
                                                  self.turning, 'h',
                                                  self.ax - camera.x, self.ay,
                                                  100 + self.range, 100 + self.range + skill1_scale)

    # 스킬 지속 시간 처리
    def update(self):
        # 히트박스 최신화
        self.hitbox = (self.ax - (self.range // 2), self.ay - (self.range // 2),
                       self.ax + (self.range // 2), self.ay + (self.range // 2))
        if self.attack_version == 0:
            if get_time() - self.skill_Activate_time >= 0.5:
                self.character.basic_Attacking = False
                if self in game_world.world[1]:
                    game_world.remove_object(self)
        if self.attack_version == 1:
            if get_time() - self.skill_Activate_time >= 2.0:
                self.character.skill1_Attacking = False
                if self in game_world.world[1]:
                    game_world.remove_object(self)
            else:
                self.ax += self.adir * SKILL1_SPEED_PPS * game_framework.frame_time # 스킬1은 지속 시간 동안 천천히 앞으로 이동
        elif self.attack_version == 2:
            if get_time() - self.skill_Activate_time >= 2.0:
                self.character.skill2_Attacking = False
                if self in game_world.world[1]:
                    game_world.remove_object(self)
            else:
                self.ax = self.character.x
                self.ay = self.character.y
                self.turning += self.adir * game_framework.frame_time