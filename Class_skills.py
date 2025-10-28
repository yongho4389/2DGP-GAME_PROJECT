from pico2d import *
from Class_camera import camera

class Skills:
    image = None
    def __init__(self, character, attack_version):
        self.character = character
        self.attack_version = attack_version
        if Skills.image == None:
            Skills.image = load_image('attack_effect_sheets.png')

        self.turning = 0.0
        self.skill_Activate_time = 0.0
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

    # 공격 이펙트 그리기
    def draw_attack(self):
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
    def skill_update(self, delta_time):
        self.draw_attack()
        self.skill_Activate_time += delta_time
        if self.skill_Activate_time >= 1.0:
            self.character.skill1_Attacking = False
            self.character.skill2_Attacking = False
        elif self.attack_version == 1:
            self.ax += self.adir * (self.range // 2)  # 스킬1은 지속 시간 동안 천천히 앞으로 이동
        else:
            self.ax = self.character.x
            self.ay = self.character.y
            self.turning += 100.0 * delta_time * self.adir