from pico2d import *
from Class_camera import camera
import game_world
import game_framework

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
        self.cur_state = 'Attack2'
        self.current_time = get_time()
        self.frame = 0
        self.motion = 2
        self.start_frame = 0
        self.end_frame = 7
        self.end_motion = False
        self.attacking_onoff = False
        self.TIME_PER_ACTION = 1  # 한 동작을 수행하는데 걸리는 시간 (초)
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION  # 초당 몇 동작을 수행하는지

        self.MAX_HP = 1000
        self.HP = self.MAX_HP
        self.damage = 50 # 몸통 충돌 데미지
        self.attack1_damage = 25 # 에너지볼 데미지
        self.attack2_damage = 50 # 폭발 데미지

    def frame_update(self):
        frame_count = self.end_frame - self.start_frame + 1  # 얼마의 프레임으로 구성되는지 계산
        self.frame = (self.frame + frame_count * self.ACTION_PER_TIME * game_framework.frame_time) % frame_count

    def Attack1(self):
        self.motion = 2
        pass
    def Attack2(self):
        self.motion = 1
        pass
    def Attack3(self):
        self.motion = 0
        pass

    def update(self):
        self.frame_update()
        if (self.cur_state == 'Attack1'):
            self.Attack1()
        elif (self.cur_state == 'Attack2'):
            self.Attack2()
        elif (self.cur_state == 'Attack3'):
            self.Attack3()

    def end_motion_check(self, frame_index):
        # 모션이 끝난 경우 다시 움직이는 동작으로 전환
        if self.end_motion:
            # self.cur_state = 'Attack1'
            self.frame = 0
            self.end_motion = False
            self.attacking_onoff = False
        # 모션이 끝났으면 플래그 활성화
        elif frame_index >= self.end_frame:
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
        draw_rectangle(*self.get_screen_bb2())
        draw_rectangle(*self.get_screen_bb3())

        # 체력바
        hp_length = 1500 * (self.HP / self.MAX_HP)  # HP바 길이가 출력되는 부분 100% 기준으로 계산됨. (최대 1500의 길이)
        self.UI_image.clip_draw(2720 // 5, 0, 2720 // 5, 185, 400, 25, hp_length, 300)  # HP 바

    # 화면용 바운딩 박스
    def get_screen_bb(self):
        # 렌더링용(화면 좌표)
        x1, y1, x2, y2 = self.get_bb()
        return x1 - camera.x, y1, x2 - camera.x, y2

    def get_screen_bb2(self):
        # 렌더링용(화면 좌표)
        x1, y1, x2, y2 = self.body_bb()
        return x1 - camera.x, y1, x2 - camera.x, y2

    def get_screen_bb3(self):
        # 렌더링용(화면 좌표)
        x1, y1, x2, y2 = self.attacking_bb()
        return x1 - camera.x, y1, x2 - camera.x, y2

    def get_bb(self):  # 상호작용 전용 충돌 박스
        xb = self.width / 2
        yb = self.height / 2
        return self.x - xb, self.y - yb, self.x + xb, self.y + yb

    def body_bb(self):  # 몬스터 몸통 충돌 박스
        xb = self.width / 5
        yb = self.height / 2.5
        return self.x - xb, self.y - yb, self.x + xb, self.y + yb

    def body_collision(self, other):
        # 인자로 전달한 객체의 바운딩 박스를 구한다
        left_a, bottom_a, right_a, top_a = self.body_bb()
        left_b, bottom_b, right_b, top_b = other.get_bb()
        # 충돌이 일어나지 않으면 False 리턴, 충돌이 일어나면 맨 마지막에 True를 리턴 (아래 if문들은 충돌이 절대로 일어나지 않을 경우에 대한 처리를 하는 것)
        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True

    def attacking_bb(self):  # 몬스터 공격 충돌 박스
        xr = (self.width / 5 * self.dir)  # x위치 보정
        yr = -self.height / 5  # y위치 보정
        xb = self.width / 5
        yb = self.height / 5
        return self.x - xb + xr, self.y - yb + yr, self.x + xb + xr, self.y + yb + yr

    def attacking_collision(self, other):
        # 인자로 전달한 객체의 바운딩 박스를 구한다
        left_a, bottom_a, right_a, top_a = self.attacking_bb()
        left_b, bottom_b, right_b, top_b = other.get_bb()
        # 충돌이 일어나지 않으면 False 리턴, 충돌이 일어나면 맨 마지막에 True를 리턴 (아래 if문들은 충돌이 절대로 일어나지 않을 경우에 대한 처리를 하는 것)
        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True

    def handle_collision(self, group, other):
        if group == 'character:elite_monster':
            # 플레이어가 공격 범위 안에 들어왔을 경우 (몬스터가 피격 중에는 공격을 하지 않고, 공격 중인 경우 frame을 0으로 초기화하지 않음)
            if self.attacking_collision(
                    other) and not self.cur_state == 'Attacking' and not self.cur_state == 'Attacked':
                self.cur_state = 'Attacking'
                self.frame = 0
        elif group == 'attack:elite_monster' and other.is_attack:
            if self.body_collision(other):
                other.is_attack = False  # 공격 판정은 한 번만 되도록 하며, 몬스터에게 실제 변화가 일어났을 때 공격 판정이 적용되었음을 알림
                self.HP -= other.damage
                # 피격 시 적이 플레이어에게 달려들도록 방향 변경
                if other.adir == self.dir:
                    self.dir *= -1
                # 피격 상태로의 변경
                self.cur_state = 'Attacked'
                self.frame = 0
                self.current_time = get_time()
                if self.HP <= 0:  # 사망 시 삭제
                    game_world.remove_object(self)
                    self.character.Gold += 100 + (self.stage.stage_level * 100)  # 골드 획득
                    self.character.EXP += 50 + (self.stage.stage_level * 50)  # 경험치 획득
