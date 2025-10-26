from pico2d import *

# 기본 잡몹
class Basic_Monster:
    image = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.width = 64
        self.height = 64
        # 이미지 1번만 로드
        if Basic_Monster.image == None:
            Basic_Monster.image = load_image('basic_monster_sheet.png')

    def update(self):
        self.frame = (self.frame + 1) % 8  # 8 프레임 애니메이션

    def draw(self):
        self.image.clip_draw(self.frame * self.width, 0, self.width, self.height, self.x, self.y)