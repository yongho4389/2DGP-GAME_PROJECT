from pico2d import *
from Class_camera import camera
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm. 즉, 1 meter 당 몇 픽셀인지 계산. 10pixel을 0.3(m)으로 나누어 1미터 당 픽셀 수를 구함
RUN_SPEED_KMPH = 5.0 # Km / Hour (여기서 현실적인 속도를 결정) (km/h)
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0) # Meter / Minute
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0) # Meter / Second
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) # 초당 몇 픽셀을 이동할지 결졍 (PPS) (이것이 속도가 됨)

# 기본 잡몹
class Basic_Monster:
    image = None
    UI_image = None
    def __init__(self, x, y, dir, stage, character):
        # 이미지 1번만 로드
        if Basic_Monster.image == None:
            Basic_Monster.image = load_image('./image_sheets/basic_monster_image.png')
        if Basic_Monster.UI_image == None:
            Basic_Monster.UI_image = load_image('./image_sheets/character_UI_sheet.png')
        self.x = x
        self.y = y
        self.stage = stage
        self.character = character
        self.width = 256
        self.height = 256
        self.dir = dir

        self.MAX_HP = self.stage.stage_level * 20 + 50 # 테스트를 위해 50을 더한 것. 실제로는 10만 더하기
        self.HP = self.MAX_HP
        self.damage = self.stage.stage_level * 5 + 10

    def moving(self):
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.x < camera.start_position + 200 or self.x > camera.end_position - 200:
            self.dir *= -1

    def update(self):
        self.moving()
        pass

    def draw(self):
        if self.dir == -1:
            self.image.clip_composite_draw(self.stage.stage_level * self.width, 0,
                                       # 시트상 위치
                                       self.width, self.height,  # 시트상 크기
                                       0, '',
                                       self.x - camera.x, self.y,  # 월드 위치
                                       100, 100)
        else:
            self.image.clip_composite_draw(self.stage.stage_level * self.width, 0,
                                           # 시트상 위치
                                           self.width, self.height,  # 시트상 크기
                                           0, 'h',
                                           self.x - camera.x, self.y,  # 월드 위치
                                           100, 100)
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
            self.dir *= -1 # 피격 시 방향 전환을 수행하여 도망가거나 플레이어에게 달려들도록 함
            # 피격 시 경직 추가 필요 (일반 몹이기 때문)
            if self.HP <= 0:  # 사망 시 삭제
                game_world.remove_object(self)
                self.character.Gold += 10 + (self.stage.stage_level * 10)  # 골드 획득
                self.character.EXP += 5 + (self.stage.stage_level * 5)  # 경험치 획득
