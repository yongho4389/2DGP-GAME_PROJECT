world = [[], [], []] # layers for game objects

def add_object(o, depth):
    world[depth].append(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return
    raise Exception("World 에 존재하지 않는 오브젝트를 지우려고 시도함")

# collision_pairs에 들어있는 모든 o를 제거
def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
    pass

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def clear():
    for layer in world:
        layer.clear()

def collide(a, b):
    # 인자로 전달한 객체의 바운딩 박스를 구한다
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    # 충돌이 일어나지 않으면 False 리턴, 충돌이 일어나면 맨 마지막에 True를 리턴 (아래 if문들은 충돌이 절대로 일어나지 않을 경우에 대한 처리를 하는 것)
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

collision_pairs = {}
def add_collision_pair(group, a, b):
    if group not in collision_pairs: # 처음 추가되는 그룹인 경우
        collision_pairs[group] = ([], []) # 해당 그룹을 위한 빈 리스트를 작성 (a가 왼쪽, b가 오른쪽에 들어감) (None을 인자로 받은 것은 해당 부분의 리스트를 채우지 않겠다는 뜻
    if a: # a가 None이 아닌 경우에만 추가
        collision_pairs[group][0].append(a)
    if b: # b가 None이 아닌 경우에만 추가
        collision_pairs[group][1].append(b)
    return None


def handle_collision():
    for group, pairs in collision_pairs.items(): # collision_pairs 딕셔너리의 (키, 값) 쌍을 하나씩 꺼내서 처리 (pairs는 (a 리스트, b 리스트) 튜플)
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b) # a에게는 누구와 충돌했는지를 알려주고, 그 group도 알려주어 a가 스스로 b에 대한 처리를 하도록 만든다.
                    b.handle_collision(group, a) # b에게도 동일하게 처리

    return None