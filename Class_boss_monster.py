from pico2d import *
from Class_camera import camera
import game_world
import game_framework
from Class_boss_skills import Boss_skills
from game_world import PIXEL_PER_METER
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from random import randint

# 기본 잡몹
class Boss_Monster:
    image = None
    UI_image = None

    def __init__(self, x, y, dir, stage, character):
        # 이미지 1번만 로드
        if Boss_Monster.image == None:
            Boss_Monster.image = load_image('./image_sheets/boss_monster_sheets.png')
        if Boss_Monster.UI_image == None:
            Boss_Monster.UI_image = load_image('./image_sheets/character_UI_sheet.png')
        self.x = x
        self.y = y
        self.stage = stage
        self.character = character
        self.width = 3288 // 8
        self.height = 1416 // 3
        self.dir = dir
        self.rotate = 0.0
        self.cur_state = 'Attack1'
        self.current_time = get_time()
        self.frame = 0
        self.motion = 2
        self.start_frame = 0
        self.end_frame = 7
        self.end_motion = False
        self.attacking_onoff = False
        self.TIME_PER_ACTION = 1  # 한 동작을 수행하는데 걸리는 시간 (초)
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION  # 초당 몇 동작을 수행하는지

        self.build_behavior_tree()

        self.MAX_HP = 1000
        self.HP = self.MAX_HP
        self.damage = 50 # 몸통 충돌 데미지
        self.energy_damage = 25 # 에너지볼 데미지
        self.bomb_damage = 50 # 폭발 데미지
        self.attack1_count = 0 # 에너지볼 공격 횟수 카운트

    def frame_update(self):
        frame_count = self.end_frame - self.start_frame + 1  # 얼마의 프레임으로 구성되는지 계산
        self.frame = (self.frame + frame_count * self.ACTION_PER_TIME * game_framework.frame_time) % frame_count

    def Attack1(self):
        if self.cur_state != 'Attack1': # 다른 동작 수행 중이었을 경우
            self.frame = 0
            self.attacking_onoff = False
        self.cur_state = 'Attack1'
        self.motion = 2
    def Attack2(self):
        if self.cur_state != 'Attack2':  # 다른 동작 수행 중이었을 경우
            self.frame = 0
            self.attacking_onoff = False
        self.cur_state = 'Attack2'
        self.motion = 1
    def Attack3(self):
        if self.cur_state != 'Attack3':  # 다른 동작 수행 중이었을 경우
            self.frame = 0
            self.attacking_onoff = False
        self.cur_state = 'Attack3'
        self.motion = 0

    def Attacking(self):
        if self.frame >= 4 and not self.attacking_onoff:
            # 에너지볼 발사
            if self.cur_state == 'Attack1':
                type, x, y = 0, self.x, randint(100, 200)
                skill = Boss_skills(x, y, type, self)
                game_world.add_object(skill, 1)
                game_world.add_collision_pair('character:boss_attack', None, skill)
                game_world.add_collision_pair('player_attack:boss_attack', None, skill)
            elif self.cur_state == 'Attack2':
                type, x, y = 1, self.character.x, self.character.y
                skill = Boss_skills(x, y, type, self)
                game_world.add_object(skill, 1)
                game_world.add_collision_pair('character:boss_attack', None, skill)
            elif self.cur_state == 'Attack3':
                for _ in range(3):
                    skill = Boss_skills(randint(200, 600), 600, 2, self)
                    game_world.add_object(skill, 1)
                    game_world.add_collision_pair('character:boss_attack', None, skill)
                    game_world.add_collision_pair('player_attack:boss_attack', None, skill)
            self.attacking_onoff = True


    # 거리 비교 함수 (x1, y1)와 (x2, y2) 사이의 거리가 r 미터보다 작은지
    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2  # 게임 내에서 사용하는 미터 단위로 맞춤

    def nearby(self, distance):
        if self.distance_less_than(self.character.x, self.character.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def attack1_count_compare(self):
        if self.attack1_count >= 5:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def update(self):
        self.frame_update()
        self.bt.run()
        self.Attacking()
        if get_time() - self.current_time >= 0.25:
            self.rotate = 0.0  # 피격 모션 초기화

    def end_motion_check(self, frame_index):
        # 모션이 끝난 경우 다시 움직이는 동작으로 전환
        if self.end_motion:
            self.cur_state = 'Attack1'
            self.frame = 0
            self.end_motion = False
            self.attacking_onoff = False
        # 모션이 끝났으면 플래그 활성화
        elif frame_index >= self.end_frame:
            if self.cur_state == 'Attack1' or self.cur_state == 'Attack2': # 공격 후 다시 0으로 바뀌려면 공격2에서도 count를 늘려줘야 함
                self.attack1_count = (self.attack1_count + 1) % 6  # 에너지볼 공격 횟수 카운트 (5회 후 초기화)
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
                                       300, 300)
        self.end_motion_check(frame_index)
        draw_rectangle(*self.get_screen_bb())

        # 체력바
        hp_length = 1500 * (self.HP / self.MAX_HP)  # HP바 길이가 출력되는 부분 100% 기준으로 계산됨. (최대 1500의 길이)
        self.UI_image.clip_draw(2720 // 5, 0, 2720 // 5, 185, 400, 25, hp_length, 300)  # HP 바

    # 화면용 바운딩 박스
    def get_screen_bb(self):
        # 렌더링용(화면 좌표)
        x1, y1, x2, y2 = self.get_bb()
        return x1 - camera.x, y1, x2 - camera.x, y2

    def get_bb(self):  # 상호작용 전용 충돌 박스
        xb = self.width / 5
        yb = self.height / 4
        return self.x - xb, self.y - yb, self.x + xb, self.y + yb

    def build_behavior_tree(self):
        action_attack1 = Action('a1', self.Attack1)
        # 공격 2
        action_attack2 = Action('a2', self.Attack2)
        c_attack2 = Condition('a2_check', self.attack1_count_compare)
        Attack2 = Sequence('Attack2', c_attack2, action_attack2)
        # 공격 3
        action_attack3 = Action('a3', self.Attack3)
        c_attack3 = Condition('a3_check', self.nearby, 7)
        root = Attack3 = Sequence('Attack3', c_attack3, action_attack3)
        root = Boss_behavior = Selector('Boss_behavior', Attack3, Attack2, action_attack1)
        self.bt = BehaviorTree(root)
        pass

    def handle_collision(self, group, other):
        if group == 'character:boss_monster':
            pass
        elif group == 'attack:monster' and other.is_attack:
            other.is_attack = False  # 공격 판정은 한 번만 되도록 하며, 몬스터에게 실제 변화가 일어났을 때 공격 판정이 적용되었음을 알림
            self.HP -= other.damage
            self.rotate = math.radians(-30)  # 피격 모션
            self.current_time = get_time()
