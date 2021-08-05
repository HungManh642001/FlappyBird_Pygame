import pygame
from random import randint

pygame.init()

screen = pygame.display.set_mode((500, 600))

pygame.display.set_caption('Flappy bird')

GREY = (120, 120, 120)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0 , 255)

clock = pygame.time.Clock()

background_img = pygame.image.load('images/background.png')
background_img = pygame.transform.scale(background_img, (500, 600))

bird_img = pygame.image.load('images/bird.png')
bird_img = pygame.transform.scale(bird_img, (35, 35))
tube_img = pygame.image.load('images/tube.png')
tube_op_img = pygame.image.load('images/tube_op.png')
sound = pygame.mixer.Sound('music/no6.wav')
sand_img = pygame.image.load('images/sand.png')
sand_img = pygame.transform.scale(sand_img, (500, 30))


bird_x = 50
bird_y = 350
tube1_x = 600
tube2_x = 800
tube3_x = 1000
tube_width = 50
tube1_height = randint(100, 400)
tube2_height = randint(100, 400)
tube3_height = randint(100, 400)
d_2tube = 150

bird_drop_velocity = 0
gravity = 0.5
tube_velocity = 2
score = 0
font = pygame.font.SysFont('san', 20)
fontOver = pygame.font.SysFont('san', 50)

tube1_pass = False
tube2_pass = False
tube3_pass = False

pausing = False
running = True
start = False

while running:
	# giup man hinh hien 60 lan tren s
	clock.tick(60)

	pygame.mixer.Sound.play(sound)

	screen.blit(background_img, (0, 0))

	# Ép ảnh ống và vẽ ống
	tube1_img = pygame.transform.scale(tube_img, (tube_width, tube1_height))
	tube1 = screen.blit(tube1_img, (tube1_x, 0))

	tube2_img = pygame.transform.scale(tube_img, (tube_width, tube2_height))
	tube2 = screen.blit(tube2_img, (tube2_x, 0))
	
	tube3_img = pygame.transform.scale(tube_img, (tube_width, tube3_height))
	tube3 = screen.blit(tube3_img, (tube3_x, 0))

	# Ép ảnh ống và vẽ ống đối diện
	tube1_op_img = pygame.transform.scale(tube_op_img, (tube_width, 600 - d_2tube - tube1_height))
	tube1_op = screen.blit(tube1_op_img, (tube1_x, tube1_height + d_2tube))

	tube2_op_img = pygame.transform.scale(tube_op_img, (tube_width, 600 - d_2tube - tube2_height))
	tube2_op = screen.blit(tube2_op_img, (tube2_x, tube2_height + d_2tube))

	tube3_op_img = pygame.transform.scale(tube_op_img, (tube_width, 600 - d_2tube - tube3_height))
	tube3_op = screen.blit(tube3_op_img, (tube3_x, tube3_height + d_2tube))

	# Ống di chuyển sang trái
	if start:
		tube1_x -= tube_velocity
		tube2_x -= tube_velocity
		tube3_x -= tube_velocity

	# Tạo ống mới
	if tube1_x <= -tube_width:
		tube1_x = 550
		tube1_height = randint(100, 400)
		tube1_pass = False
	if tube2_x <= -tube_width:
		tube2_x = 550
		tube2_height = randint(100, 400)
		tube2_pass = False
	if tube3_x <= -tube_width:
		tube3_x = 550
		tube3_height = randint(100, 400)
		tube3_pass = False

	# Vẽ chim 
	bird = screen.blit(bird_img,(bird_x, bird_y))

	# Vẽ nền cát ở dưới và nền trên
	head = pygame.draw.rect(screen, WHITE, (0,0,500, 1))
	sand = screen.blit(sand_img,(0, 570))

	# Vẽ chim rơi
	if start:
		bird_y += bird_drop_velocity
		bird_drop_velocity += gravity

	# Ghi điểm
	score_txt = font.render("Score: " + str(score), True, RED)
	screen.blit(score_txt, (5, 5))

	# Cộng điểm
	if tube1_x + tube_width <= bird_x and tube1_pass == False:
		score += 1
		tube1_pass = True
	if tube2_x + tube_width <= bird_x and tube2_pass == False:
		score += 1
		tube2_pass = True
	if tube3_x + tube_width <= bird_x and tube3_pass == False:
		score += 1
		tube3_pass = True

	if score < 25:
		tube_velocity =  score / 10 + 2
	else:
		tube_velocity = score / 20 + 4.5

	# Xử lý va chạm
	tubes = [tube1, tube2, tube3, tube1_op, tube2_op, tube3_op, sand, head]
	for tube in tubes:
		if bird.colliderect(tube):
			pygame.mixer.pause()
			tube_velocity = 0
			bird_drop_velocity = 0
			game_over_txt = fontOver.render("Game Over!", True, RED)
			screen.blit(game_over_txt, (160, 200))
			game_over_txt = fontOver.render("Score: " + str(score), True, RED)
			screen.blit(game_over_txt, (190, 260))
			space_txt = font.render("Press Space to continue!", True, BLUE)
			screen.blit(space_txt, (180, 330))
			pausing = True
			start = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				bird_drop_velocity = 0
				bird_drop_velocity -=7
				start = True
				if pausing == True:
					pygame.mixer.unpause()
					tube1_x = 600
					tube2_x = 800
					tube3_x = 1000
					bird_y = 350
					tube_velocity = 2
					score = 0
					pausing = False	
					start = False	

	# giup ve len man hinh co hieu luc
	pygame.display.flip() 

# Khi chay xong chuong trinh xoa toan bo du lieu cua game
pygame.quit()

