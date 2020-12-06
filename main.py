import pygame
from random import randrange
from classes import McQueen, Car, Police, Ambulance, FireTruck, Explosion, Hole
from welcome import welcome

pygame.init()
run = False
run = welcome(run)

pygame.mixer.music.load("sounds/song.mp3")
pygame.mixer.music.play(-1)
engine_sound = pygame.mixer.Sound('sounds/02-engine_short-consolidated.wav')
engine_sound.play(-1)
horn = pygame.mixer.Sound('sounds/03-horns-consolidated.wav')

font = pygame.font.SysFont('comicsans', size=40, bold=False, italic=True)

W, H = 1200, 800
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("MCQUEEN RUSH")

bg = pygame.image.load('images/road.png').convert()
bg_y = 0
bg_y2 = -1200
clock = pygame.time.Clock()


def redraw_game_window():
	win.blit(bg, (0, bg_y))
	win.blit(bg, (0, bg_y2))
	for ho in holes:
		ho.draw(win)
	for c in cars:
		c.draw(win)
	energy = font.render('Energy: ' + str(mcqueen.energy_), True, (0, 200, 0))
	win.blit(energy, (90, 15))
	score = font.render('Score: ' + str(int(mcqueen.score_)), True, (0, 0, 200))
	win.blit(score, (950, 15))
	mcqueen.draw(win)
	pygame.display.update()


def check_if_crash(obj):
	if obj.hit_box:
		if mcqueen.hit_box[1] < obj.hit_box[1] + obj.hit_box[3] and \
				mcqueen.hit_box[0] < obj.hit_box[0] + obj.hit_box[2] and \
				mcqueen.hit_box[0] + mcqueen.hit_box[2] > obj.hit_box[0] and \
				mcqueen.hit_box[1] + mcqueen.hit_box[3] > obj.hit_box[1]:
			obj.hit()
			mcqueen.hit()
			obj.crash_sound()
			return True


def game_over():
	# TODO game over func
	print(f"Crashes: {mcqueen.crash_count}, Energy: {mcqueen.energy_}, Score: {mcqueen.score_}")


fps = 60

scroll_speed = 1
car_speed = scroll_speed * (randrange(2, 3) / 6) + 3

speed_up = pygame.USEREVENT + 1
pygame.time.set_timer(speed_up, 1000)

run_new_car = pygame.USEREVENT + 2
start_range, stop_range = 1500, 3000
pygame.time.set_timer(run_new_car, randrange(start_range, stop_range))

special_car = pygame.USEREVENT + 3
pygame.time.set_timer(special_car, 20000)

hole_on_track = pygame.USEREVENT + 4
pygame.time.set_timer(hole_on_track, randrange(4000, 6000))

mcqueen = McQueen()
cars = []
holes = []

while run:
	if mcqueen.energy_ <= 0:
		game_over()
		break
	redraw_game_window()
	time_counter = clock.tick(fps)

	bg_y += scroll_speed
	bg_y2 += scroll_speed

	if bg_y > bg.get_height():
		bg_y = bg.get_height() * -1

	if bg_y2 > bg.get_height():
		bg_y2 = bg.get_height() * -1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

		if event.type == speed_up:
			fps += 1
			mcqueen.score_ += 1
			start_range -= 10
			stop_range -= 20

		if event.type == run_new_car:
			cars.append(Car(120, 220, car_speed))

		if event.type == special_car:
			police = Police(120, 200, car_speed)
			ambulance = Ambulance(150, 318, car_speed)
			fire_truck = FireTruck(150, 450, car_speed)
			special_cars = [police, ambulance, fire_truck]
			index = randrange(0, len(special_cars))
			cars.append(special_cars[index])
			special_cars[index].siren()
			time_counter = 0

		if event.type == hole_on_track:
			holes.append(Hole())

	# ____CARS____
	for car in cars:
		car.y += car.speed
		index_l = cars.index(car)
		if check_if_crash(car):
			mcqueen.score_ -= 50
			x, y, w, h, sp, hb = car.x, car.y, car.width, car.height, scroll_speed, car.hit_box
			cars.pop(index_l)
			cars.append(Explosion(x, y, W, h, sp))
		if car.y > win.get_height() + 10:
			cars.pop(index_l)
		if not mcqueen.crashed:
			mcqueen.score_ += 0.05
		mcqueen.crashed = False
	# _______________________________

	# ____HOLES____
	for hole in holes:
		hole.y += scroll_speed
		index = holes.index(hole)
		if check_if_crash(hole):
			mcqueen.score_ -= 10
		if hole.y > win.get_height() + 10:
			holes.pop(index)

	keys = pygame.key.get_pressed()
	if (keys[pygame.K_LEFT] or keys[pygame.K_LCTRL]) and mcqueen.x > mcqueen.vel + 70:
		mcqueen.x -= mcqueen.vel
		mcqueen.left = True
		mcqueen.right = False
		mcqueen.standing = False
	elif (keys[pygame.K_RIGHT] or keys[pygame.K_RCTRL]) and mcqueen.x < W - (mcqueen.width + mcqueen.vel + 70):
		mcqueen.x += mcqueen.vel
		mcqueen.left = False
		mcqueen.right = True
		mcqueen.standing = False
	else:
		mcqueen.standing = True

	if keys[pygame.K_SPACE]:
		horn.play(maxtime=300)

	if keys[pygame.K_ESCAPE]:
		game_over()
		pygame.quit()
		quit()
