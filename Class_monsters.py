from pico2d import *
from Class_camera import camera
import game_world

# 기본 잡몹
class Basic_Monster:
    image = None
    def __init__(self, x, y, stage, character):
        # 이미지 1번만 로드
        if Basic_Monster.image == None:
            Basic_Monster.image = load_image('./image_sheets/basic_monster_image.png')
        self.x = x
        self.y = y
        self.stage = stage
        self.character = character
        self.width = 256
        self.height = 256

        self.HP = self.stage.stage_level * 20 + 100
        self.damage = self.stage.stage_level * 5 + 10


    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.stage.stage_level * self.width, 0, self.width, self.height, self.x - camera.x, self.y, 100, 100)
        draw_rectangle(*self.get_screen_bb())

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
        elif group == 'attack:monster':
            self.HP -= other.damage
            if self.HP <= 0:  # 사망 시 삭제
                game_world.remove_object(self)
                self.character.Gold += 10 + (self.stage.stage_level * 10)  # 골드 획득
                self.character.EXP += 5 + (self.stage.stage_level * 5)  # 경험치 획득
