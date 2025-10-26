from pico2d import *
from Class_stage import *

class Store:
    def __init__(self, stage):
        self.stage = stage
        self.image = load_image('store_sheet.png')
        self.element_image = load_image('store_element_sheet.png')
        # 폰트 불러오기
        self.font = load_font('C:\Windows\Fonts\malgun.ttf', 20)
        self.x = self.stage.width // 2 + 100
        self.y = self.stage.height // 2 - 75

        # 상점 기본창 위치
        self.window_x = self.stage.width // 2
        self.window_y = self.stage.height // 2
        # X버튼 위치
        self.x_button_x = self.window_x + 350
        self.x_button_y = self.window_y + 220
        # 체력 회복
        self.healing_x = self.window_x - 250
        self.healing_y = self.window_y
        self.heal_cost = 100
        # 기본 공격 강화
        self.basic_damage_x = self.window_x - 40
        self.basic_damage_y = self.window_y + 60
        self.basic_damage_cost = 100
        self.basic_damage_level = 1
        self.basic_range_x = self.window_x + 40
        self.basic_range_y = self.window_y + 60
        self.basic_range_cost = 100
        self.basic_range_level = 1

        self.store_onoff = False

    def draw(self):
        self.image.clip_draw(0, 0, 227, 341, self.x, self.y, 300, 500)
    def store_draw(self):
        if self.store_onoff:
            # 기본 창 형성
            self.element_image.clip_draw(0, 170, 210, 170, self.window_x, self.window_y, 1400, 600)
            self.font.draw(self.window_x - 330, self.window_y + 200, f'왼쪽: 데미지 강화', (255, 255, 255))
            self.font.draw(self.window_x - 330, self.window_y + 180, f'오른쪽: 범위 강화', (255, 255, 255))
            # X 버튼
            self.element_image.clip_draw(210, 170, 210, 170, self.x_button_x, self.x_button_y, 100, 100)
            # 회복 버튼
            self.element_image.clip_draw(420, 170, 210, 170, self.healing_x, self.healing_y, 100, 100)
            self.font.draw(self.healing_x - 15, self.healing_y + 8, f'{self.heal_cost}G', (255, 255, 255)) # 회복 비용 출력
            self.element_image.clip_draw(630, 170, 210, 170, self.healing_x, self.healing_y + 75, 200, 200)
            # 기본 공격 강화 버튼
            # 기본 공격 데미지 강화
            self.element_image.clip_draw(420, 170, 210, 170, self.basic_damage_x, self.basic_damage_y, 100, 100)
            self.font.draw(self.basic_damage_x - 15, self.basic_damage_y + 8, f'{self.basic_damage_cost}G', (255, 255, 255))
            self.font.draw(self.basic_damage_x - 40, self.basic_damage_y + 40, f'LV {self.basic_damage_level}', (255, 255, 255))
            # 기본 공격 범위 강화
            self.element_image.clip_draw(420, 170, 210, 170, self.basic_range_x, self.basic_range_y, 100, 100)
            self.font.draw(self.basic_range_x - 15, self.basic_range_y + 8, f'{self.basic_range_cost}G', (255, 255, 255))
            self.font.draw(self.basic_range_x + 5, self.basic_range_y + 40, f'LV {self.basic_range_level}', (255, 255, 255))
            # 기본 공격 아이콘
            self.element_image.clip_draw(0, 0, 210, 170, (self.basic_damage_x + self.basic_range_x) // 2,
                                         (self.basic_damage_y + self.basic_range_y) // 2 + 90, 200, 200)

    def store_click(self, mx, my):
        if self.stage.special_stage and not self.store_onoff and mx >= self.x - 150 and mx <= self.x + 150 and my >= self.y - 250 and my <= self.y + 250:
            self.store_onoff = True
            return
        if self.store_onoff:
            if mx >= self.x_button_x - 25 and mx <= self.x_button_x + 25 and my >= self.x_button_y - 25 and my <= self.x_button_y + 25:
                self.store_onoff = False
                return
