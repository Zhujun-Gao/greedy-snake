"""
游戏说明：

按键：UP DOWN LEFT RIGHT 控制 蛇蛇爬行方向
	 SPACE键 控制游戏暂停与继续
	 按下ESCAPE键 / 鼠标点击退出窗口 => 退出游戏

长度：length = len(snake)*0.5 cm

生命值：初始生命值 = 100
	   若蛇蛇咬到自己，blood -= 5*被咬掉的节数
	   若蛇超出活动范围，则持续减血
	   生命值 = 0  =>  dead
"""

import pygame, sys
from pygame.locals import *
from random import randint


class Point(object):
	"""docstring for Point"""
	def __init__(self, row, col):
		self.col = col
		self.row = row

	def copy(self):
		return Point(self.row, self.col)


def gen_food(head, bodies):
	collision = False
	while True:
		pos = Point(randint(2, ROWS+1), randint(0, COLS-1))

		if pos.row == head.row and pos.col == head.col:
			collision = True

		for body in bodies:
			if pos.row == body.row and pos.col == body.col:
				collision = True
				break

		if not collision:
			return pos



# settings
W  = 800
H = 600
border_top = 40

ROWS = 30
COLS = 40

screen_size = (W, H+border_top)

head_color = (160, 240, 240)
body_color = (230, 230, 230)
food_color = (249, 189, 174)
back_color = (255, 255, 255)


# initialize
pygame.init()
screen = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption("Greedy Snake")
background = pygame.image.load("grasses.png")
pygame.mouse.set_visible(False)


# background music play
pygame.mixer.init()
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0)


# eat effect music
eat_sound = pygame.mixer.Sound("EatSound.ogg")
eat_sound.set_volume(0.8)


# snake
blood = 100
hurt = 2
direction = "left"

head = Point(int(ROWS/2), (int(COLS/2)))
bodies = [
	Point(head.row, head.col+1),
	Point(head.row, head.col+2),
	Point(head.row, head.col+3)
]
food = gen_food(head, bodies)


# state
pause = False


# button
button_size = (120, 45)
button = pygame.Surface(button_size)
button.fill((220, 220, 220), (0, 0, *button_size))
button.fill((180, 240, 240), (5, 5, button_size[0]-10, button_size[1]-10))
myfont = pygame.font.SysFont("arial", 32, bold=True)
rendered = myfont.render("Paused", 0, (100, 100, 100))


# score
myfont = pygame.font.SysFont("arial", 23, bold=True)
board_size = (150, 30)
board = pygame.Surface(board_size)
board.fill((240, 252, 240))

# blood
rendered_blood = myfont.render("blood:", 0, (255, 100, 100))



def draw_rect(point, color):
	cell_width = W / COLS
	cell_height = H / ROWS

	left = point.col * cell_width
	top = point.row * cell_height
	pygame.draw.rect(screen, color, (left, top, cell_width, cell_height))



clock = pygame.time.Clock()

while True:

	# check event
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == K_RIGHT and direction != "left":
				direction = "right"
			elif event.key == K_LEFT and direction != "right":
				direction = "left"
			elif event.key == K_UP and direction != "down":
				direction = "up"
			elif event.key == K_DOWN and direction != "up":
				direction = "down"
			elif event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			elif event.key == K_SPACE:
				pause = not pause


	# move forward
	if not pause:
		bodies.insert(0, head.copy())
		if direction == "left":
			head.col -= 1
		elif direction == "right":
			head.col += 1
		elif direction == "up":
			head.row -= 1
		elif direction == "down":
			head.row += 1
		eat = (head.row == food.row and head.col == food.col)
		if eat:
			eat_sound.play()
			food = gen_food(head, bodies)
		else:
			bodies.pop()

		# collision
		dead = False
		if head.col < 0 or head.col >= COLS or head.row < border_top/20 or head.row >= ROWS:
			blood -= hurt
		count = 0
		for body in bodies:
			count += 1
			if head.col == body.col and head.row == body.row:
				blood -= 5*(len(bodies)-count)
				bodies = bodies[:count-1]
				break

	# dead ?
	if blood <= 0:
		print("Dead")
		sys.exit()

	# draw
	screen.fill(back_color, (0, 0, *screen_size))
	screen.blit(background, (0, border_top))
	screen.fill((235, 250, 236), (0, 0, W, border_top))
	pygame.draw.line(screen, (230,230,230), (0,border_top-1), (W,border_top-1), 1)
	for body in bodies:
		draw_rect(body, body_color)
	draw_rect(head, head_color)
	draw_rect(food, food_color)

	# draw score
	screen.blit(board, (10, 5))
	rendered_length = myfont.render("length: " + str((len(bodies)+1)*0.5)[:4] + " cm", 0, (136,136,136))
	screen.blit(rendered_length, (20, 7))

	# draw blood
	blood_board_size = (102, 22)
	blood_board = pygame.Surface(blood_board_size)
	blood_board.fill((200, 200, 200))
	blood_board.fill((255, 255, 255), (1, 1, 100, 20))
	blood_board.fill((255, 70, 70), (1, 1, blood, 20))
	screen.blit(rendered_blood, (W-190, 8))
	screen.blit(blood_board, (W-120, 10))

	# pause ?
	if pause:
		screen.blit(button, (W/2-60, H-170+border_top))
		screen.blit(rendered, (W/2-45, H-167+border_top))

	clock.tick(10)
	pygame.display.update()