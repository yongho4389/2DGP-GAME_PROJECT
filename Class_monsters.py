from pico2d import *
from Class_camera import camera

# 기본 잡몹
class Basic_Monster:
    image = None
    def __init__(self, x, y, stage):
        self.x = x
        self.y = y
        self.stage = stage
        self.width = 256
        self.height = 256
        self.damage = self.stage.stage_level * 5 + 10
        # 이미지 1번만 로드
        if Basic_Monster.image == None:
            Basic_Monster.image = load_image('./image_sheets/basic_monster_image.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.stage.stage_level * self.width, 0, self.width, self.height, self.x - camera.x, self.y, 100, 100)