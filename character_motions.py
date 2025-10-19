# 달리기 모션
def start_running(self):
    self.frame = 0
    self.start_frame = 0
    self.end_frame = 7
    self.motion = 4
    self.delay = 0.1
    self.end_motion = False
    self.Running = True
    self.Attacking = False # 공격 중 이동 시 공격이 계속되는 버그 방지
# 점프 및 착지 모션
def start_jump_and_down(self):
    self.frame = 0
    self.start_frame = 0
    self.end_frame = 3
    self.motion = 3
    self.delay = 0.2
    self.end_motion = False
    self.Jumping = True
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
    self.Attacking = True
    self.skill1_Attacking = False
    self.skill2_Attacking = False
    self.attack_version = 0
    # 기본 공격 데미지 및 사거리로 초기화
    self.damage = self.basic_damage
    self.range = self.basic_range
    self.ax = self.x + (self.dir * (20 + self.range // 2))
    self.ay = self.y
    self.adir = self.dir
# 스킬1 공격 모션
def start_skill1_attack(self):
    self.frame = 0
    self.start_frame = 0
    self.end_frame = 6
    self.motion = 1
    self.delay = 0.1
    self.end_motion = False
    self.Attacking = True
    self.skill1_Attacking = False
    self.attack_version = 1
    # skill1 데미지 및 사거리로 초기화
    self.damage = self.skill1_damage
    self.range = self.skill1_range
    self.ax = self.x + (self.dir * (20 + self.range // 2))
    self.ay = self.y
    self.adir = self.dir
    self.skill_Activate_time = 0.0
# 대쉬 모션
def start_dash(self):
    self.frame = 0
    self.start_frame = 0
    self.end_frame = 0
    self.motion = 0
    self.delay = 0.1
    self.end_motion = False
    self.Dashing = True
# 스킬2 공격 모션
def start_skill2_attack(self):
    self.frame = 0
    self.start_frame = 1
    self.end_frame = 2
    self.motion = 0
    self.delay = 0.5
    self.end_motion = False
    self.Attacking = True
    self.skill2_Attacking = False
    self.attack_version = 2
    # skill2 데미지 및 사거리로 초기화
    self.damage = self.skill2_damage
    self.range = self.skill2_range
    self.ax = self.x
    self.ay = self.y
    self.adir = self.dir
    self.skill_Activate_time = 0.0
# 서있기 모션
def start_stand(self):
    self.frame = 0
    self.start_frame = 3
    self.end_frame = 3
    self.motion = 0
    self.delay = 0.0
    self.end_motion = False
    self.Running = False
    self.Jumping = False
    self.Dashing = False
    self.Attacking = False