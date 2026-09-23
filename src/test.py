# statusCode = int(input('status code: '))

# match statusCode:
#     case 400: desc = 'Bad Req'
#     case _: desc = 'Unknown'
# print (desc)


# items = ['apple', 'strawberry', 'durian', 'peach', 'watermelon']
# print(items[-2:-8:-1])
# print(items[0:6:1])


# languages = ['Python', 'SQL', 'Java', 'C++', 'JavaScript', 'Python']
# if 'Python' in languages:
#     languages.remove('Python')

# print(languages)

# a = [1, 2, 2, 3]
# b = a                    # b 和 a 指向同一个列表
# a = list(dict.fromkeys(a))
# print(a, b)              # [1, 2, 3] [1, 2, 2, 3]

# a[:] = dict.fromkeys(a)
# print(a)


# items = ['Python', 'Java', 'C++', 'c++', 'Kotlin', 'Swift']
# items.sort()
# print(items)  # ['C++', 'Java', 'Kotlin', 'Python', 'Swift', 'c++']
# items.reverse()
# print(items)  # ['c++', 'Swift', 'Python', 'Kotlin', 'Java', 'C++']

# items = []
# for i in range(1, 100):
#     if i % 3 == 0 or i % 5 == 0:
#         items.append(i)
# print(items)

# print(*range(10))
# print(*(i for i in list(range(10))))


# scores = [[95, 83, 92], [80, 75, 82], [92, 97, 90], [80, 78, 69], [65, 66, 89]]
# print(scores[0])
# print(scores[0][1])



import random

red_balls = list(range(1, 34))
selected_balls = []
# 添加6个红色球到选中列表
for _ in range(6):
    # 生成随机整数代表选中的红色球的索引位置
    index = random.randrange(len(red_balls))
    # 将选中的球从红色球列表中移除并添加到选中列表
    selected_balls.append(red_balls.pop(index))
# 对选中的红色球排序
selected_balls.sort()
# 输出选中的红色球
for ball in selected_balls:
    print(f'\033[031m{ball:0>2d}\033[0m', end=' ')
# 随机选择1个蓝色球
blue_ball = random.randrange(1, 17)
# 输出选中的蓝色球
print(f'\033[034m{blue_ball:0>2d}\033[0m')