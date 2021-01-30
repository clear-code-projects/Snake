import pygame, sys, random
from vec import Vector2


left = Vector2(-1, 0)
up = Vector2(0, -1)
right = Vector2(1, 0)
down = Vector2(0, 1)


class SNAKE:
    def __init__(self):
        self.reset()

        def load_image(name):
            return pygame.image.load(f"Graphics/{name}.png").convert_alpha()

        self.graphics = {"head": {}, "tail": {}, "body": {}}
        self.graphics["head"][up] = load_image("head_up")
        self.graphics["head"][down] = load_image("head_down")
        self.graphics["head"][right] = load_image("head_right")
        self.graphics["head"][left] = load_image("head_left")

        self.graphics["tail"][up] = load_image("tail_up")
        self.graphics["tail"][down] = load_image("tail_down")
        self.graphics["tail"][right] = load_image("tail_right")
        self.graphics["tail"][left] = load_image("tail_left")

        self.graphics["body"][down] = load_image("body_vertical")
        self.graphics["body"][right] = load_image("body_horizontal")
        self.graphics["body"][up + right] = load_image("body_tr")
        self.graphics["body"][up + left] = load_image("body_tl")
        self.graphics["body"][down + right] = load_image("body_br")
        self.graphics["body"][down + left] = load_image("body_bl")

        self.crunch_sound = pygame.mixer.Sound("Sound/crunch.wav")

    def draw_snake(self):
        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(
                int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size
            )

            if index == 0:
                body_part = "head"
                direction = self.body[0] - self.body[1]
            elif index == len(self.body) - 1:
                body_part = "tail"
                direction = self.body[-1] - self.body[-2]
            else:
                body_part = "body"

                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    direction = down
                elif previous_block.y == next_block.y:
                    direction = right
                else:
                    direction = previous_block + next_block

            screen.blit(self.graphics[body_part][direction], block_rect)

    def move_snake(self):
        self.body = [self.body[0] + self.direction] + (
            self.body[:] if self.new_block else self.body[:-1]
        )
        self.new_block = False
   
    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False


class FRUIT:
	def __init__(self):
		self.randomize()

	def draw_fruit(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
		screen.blit(apple,fruit_rect)
		#pygame.draw.rect(screen,(126,166,114),fruit_rect)

	def randomize(self):
		self.x = random.randint(0,cell_number - 1)
		self.y = random.randint(0,cell_number - 1)
		self.pos = Vector2(self.x,self.y)

class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()

	def update(self):
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()

	def draw_elements(self):
		self.draw_grass()
		self.fruit.draw_fruit()
		self.snake.draw_snake()
		self.draw_score()

	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.fruit.randomize()
			self.snake.add_block()
			self.snake.play_crunch_sound()

		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize()

	def check_fail(self):
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			self.game_over()

		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()
		
	def game_over(self):
		self.snake.reset()

	def draw_grass(self):
		grass_color = (167,209,61)
		for row in range(cell_number):
			if row % 2 == 0: 
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)			

	def draw_score(self):
		score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(score_text,True,(56,74,12))
		score_x = int(cell_size * cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

		pygame.draw.rect(screen,(167,209,61),bg_rect)
		screen.blit(score_surface,score_rect)
		screen.blit(apple,apple_rect)
		pygame.draw.rect(screen,(56,74,12),bg_rect,2)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == SCREEN_UPDATE:
			main_game.update()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if main_game.snake.direction.y != 1:
					main_game.snake.direction = Vector2(0,-1)
			if event.key == pygame.K_RIGHT:
				if main_game.snake.direction.x != -1:
					main_game.snake.direction = Vector2(1,0)
			if event.key == pygame.K_DOWN:
				if main_game.snake.direction.y != -1:
					main_game.snake.direction = Vector2(0,1)
			if event.key == pygame.K_LEFT:
				if main_game.snake.direction.x != 1:
					main_game.snake.direction = Vector2(-1,0)

	screen.fill((175,215,70))
	main_game.draw_elements()
	pygame.display.update()
	clock.tick(60)
