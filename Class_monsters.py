from pico2d import *
from Class_camera import camera
import game_world

# 기본 잡몹
class Basic_Monster:
    image = None
    UI_image = None
    def __init__(self, x, y, stage, character):
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

        self.MAX_HP = self.stage.stage_level * 20 + 100 # 테스트를 위해 100을 더한 것. 실제로는 10만 더하기
        self.HP = self.MAX_HP
        self.damage = self.stage.stage_level * 5 + 10


    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.stage.stage_level * self.width, 0, self.width, self.height, self.x - camera.x, self.y, 100, 100)
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
            if self.HP <= 0:  # 사망 시 삭제
                game_world.remove_object(self)
                self.character.Gold += 10 + (self.stage.stage_level * 10)  # 골드 획득
                self.character.EXP += 5 + (self.stage.stage_level * 5)  # 경험치 획득
