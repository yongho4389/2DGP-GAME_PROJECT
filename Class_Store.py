from pico2d import *
from Class_Character_main import *
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
        self.healing_x = self.window_x - 220
        self.healing_y = self.window_y - 30
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

        # skill1 강화
        self.skill1_damage_x = self.window_x + 180
        self.skill1_damage_y = self.window_y + 60
        self.skill1_damage_cost = 100
        self.skill1_damage_level = 1
        self.skill1_range_x = self.window_x + 260
        self.skill1_range_y = self.window_y + 60
        self.skill1_range_cost = 100
        self.skill1_range_level = 1

        # skill2 강화
        self.skill2_damage_x = self.window_x -40
        self.skill2_damage_y = self.window_y - 125
        self.skill2_damage_cost = 100
        self.skill2_damage_level = 1
        self.skill2_range_x = self.window_x + 40
        self.skill2_range_y = self.window_y - 125
        self.skill2_range_cost = 100
        self.skill2_range_level = 1

        # 상점 창 열림 여부
        self.store_onoff = False

        self.basic_damage_upgrade = 5  # 기본 공격 데미지 강화량
        self.basic_range_upgrade = 10  # 기본 공격 범위 강화량

        self.skill1_damage_upgrade = 10  # skill1 데미지 강화량
        self.skill1_range_upgrade = 15  # skill1 범위 강화량

        self.skill2_damage_upgrade = 5  # skill2 데미지 강화량
        self.skill2_range_upgrade = 20  # skill2 범위 강화량

    def draw(self):
        self.image.clip_draw(0, 0, 227, 341, self.x, self.y, 300, 500)
    def store_draw(self, character):
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
            self.font.draw(self.healing_x - 75, self.healing_y + 100, f'회복', (255, 255, 255))

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
            self.font.draw((self.basic_damage_x + self.basic_range_x) // 2 - 130,
                           (self.basic_damage_y + self.basic_range_y) // 2 + 130,
                           f'기본 공격', (255, 255, 255))

            # skill1 강화 버튼
            # skill1 데미지 강화
            self.element_image.clip_draw(420, 170, 210, 170, self.skill1_damage_x, self.skill1_damage_y, 100, 100)
            self.font.draw(self.skill1_damage_x - 15, self.skill1_damage_y + 8, f'{self.skill1_damage_cost}G',
                           (255, 255, 255))
            self.font.draw(self.skill1_damage_x - 40, self.skill1_damage_y + 40, f'LV {self.skill1_damage_level}',
                           (255, 255, 255))
            # skill1 범위 강화
            self.element_image.clip_draw(420, 170, 210, 170, self.skill1_range_x, self.skill1_range_y, 100, 100)
            self.font.draw(self.skill1_range_x - 15, self.skill1_range_y + 8, f'{self.skill1_range_cost}G',
                           (255, 255, 255))
            self.font.draw(self.skill1_range_x + 5, self.skill1_range_y + 40, f'LV {self.skill1_range_level}',
                           (255, 255, 255))
            # skill1 아이콘
            self.element_image.clip_draw(210, 0, 210, 170, (self.skill1_damage_x + self.skill1_range_x) // 2,
                                         (self.skill1_damage_y + self.skill1_range_y) // 2 + 90, 200, 200)
            self.font.draw((self.skill1_damage_x + self.skill1_range_x) // 2 - 100,
                           (self.skill1_damage_y + self.skill1_range_y) // 2 + 130,
                           f'Skill1', (255, 255, 255))

            # skill2 강화 버튼
            # skill2 데미지 강화
            self.element_image.clip_draw(420, 170, 210, 170, self.skill2_damage_x, self.skill2_damage_y, 100, 100)
            self.font.draw(self.skill2_damage_x - 15, self.skill2_damage_y + 8, f'{self.skill2_damage_cost}G',
                           (255, 255, 255))
            self.font.draw(self.skill2_damage_x - 40, self.skill2_damage_y + 40, f'LV {self.skill2_damage_level}',
                           (255, 255, 255))
            # skill2 범위 강화
            self.element_image.clip_draw(420, 170, 210, 170, self.skill2_range_x, self.skill2_range_y, 100, 100)
            self.font.draw(self.skill2_range_x - 15, self.skill2_range_y + 8, f'{self.skill2_range_cost}G',
                           (255, 255, 255))
            self.font.draw(self.skill2_range_x + 5, self.skill2_range_y + 40, f'LV {self.skill2_range_level}',
                           (255, 255, 255))
            # skill2 아이콘
            self.element_image.clip_draw(420, 0, 210, 170, (self.skill2_damage_x + self.skill2_range_x) // 2,
                                         (self.skill2_damage_y + self.skill2_range_y) // 2 + 90, 200, 200)
            self.font.draw((self.skill2_damage_x + self.skill2_range_x) // 2 - 100,
                           (self.skill2_damage_y + self.skill2_range_y) // 2 + 130,
                           f'Skill2', (255, 255, 255))

            # 골드 보유량
            character.UI_image.clip_draw(2720 // 5 * 4, 0, 2720 // 5, 185, self.window_x - 330, self.window_y - 190, 250, 100)  # 골드 보유량
            character.font.draw(self.window_x - 305, self.window_y - 190, f'Gold: {character.Gold}', (255, 255, 0))

    def store_click(self, mx, my, character):
        if self.stage.special_stage and not self.store_onoff and mx >= self.x - 150 and mx <= self.x + 150 and my >= self.y - 250 and my <= self.y + 250:
            self.store_onoff = True
            return
        if self.store_onoff:
            # X 버튼
            if mx >= self.x_button_x - 25 and mx <= self.x_button_x + 25 and my >= self.x_button_y - 25 and my <= self.x_button_y + 25:
                self.store_onoff = False
                return
            # 회복 버튼
            if mx >= self.healing_x - 50 and mx <= self.healing_x + 50 and my >= self.healing_y - 50 and my <= self.healing_y + 50:
                if character.Gold >= self.heal_cost:
                    character.HP = character.Max_HP
                    character.Gold -= self.heal_cost
                return
            # 기본 공격 데미지 강화
            if mx >= self.basic_damage_x - 50 and mx <= self.basic_damage_x + 50 and my >= self.basic_damage_y - 50 and my <= self.basic_damage_y + 50:
                if character.Gold >= self.basic_damage_cost and self.basic_damage_level != 5:
                    character.basic_damage += self.basic_damage_upgrade
                    character.Gold -= self.basic_damage_cost
                    self.basic_damage_level += 1
                    self.basic_damage_cost += 50
                    if self.basic_damage_level >= 5:
                        self.basic_damage_cost = 0 # 최대 레벨 도달 시 비용 0으로 설정
                return
            # 기본 공격 범위 강화
            if mx >= self.basic_range_x - 50 and mx <= self.basic_range_x + 50 and my >= self.basic_range_y - 50 and my <= self.basic_range_y + 50:
                if character.Gold >= self.basic_range_cost and self.basic_range_level != 5:
                    character.basic_range += self.basic_range_upgrade
                    character.Gold -= self.basic_range_cost
                    self.basic_range_level += 1
                    self.basic_range_cost += 50
                    if self.basic_range_level >= 5:
                        self.basic_range_cost = 0 # 최대 레벨 도달 시 비용 0으로 설정
                return