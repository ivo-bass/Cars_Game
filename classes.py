import pygame
from random import randrange


class McQueen(object):
	img = pygame.image.load('images/mcqueen2.png')
	img_left = pygame.image.load('images/mcqueen_left.png')
	img_right = pygame.image.load('images/mcqueen_right.png')
	energy_ = 1000
	score_ = 0

	def __init__(self):
		self.width = 120
		self.height = 200
		self.x = 600 - self.width / 2
		self.y = 600
		self.standing = True
		self.left = False
		self.right = False
		self.vel = 5
		self.crashed = False
		self.crash_count = 0
		self.hit_box = (self.x + 15, self.y + 10, self.width - 30, self.height - 30)

	def draw(self, win):
		if not self.standing:
			if self.left:
				win.blit(self.img_left, (self.x, self.y))
			elif self.right:
				win.blit(self.img_right, (self.x, self.y))
		else:
			win.blit(self.img, (self.x, self.y))
		# pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)
		self.hit_box = (self.x + 15, self.y + 10, self.width - 30, self.height - 30)

	def hit(self):
		if not self.crashed:
			self.crash_count += 1
			self.crashed = True


class Car(object):
	images = [
		pygame.image.load('images/L_red.png'), pygame.image.load('images/L_blue.png'),
		pygame.image.load('images/L_brown.png'), pygame.image.load('images/L_dark_blue.png'),
		pygame.image.load('images/L_gray1.png'), pygame.image.load('images/L_gray2.png'),
		pygame.image.load('images/L_gray3.png'), pygame.image.load('images/L_orange.png'),
		pygame.image.load('images/L_white1.png'), pygame.image.load('images/L_white2.png'),
		pygame.image.load('images/L_white3.png')
	]

	def __init__(self, width, height, speed):
		self.x = randrange(100 + width * 0.5, 1200 - width * 2, 100)
		self.y = 0 - height - 10
		self.width = width
		self.height = height
		self.speed = speed
		self.img = self.images[randrange(0, len(self.images))]
		self.hit_box = (self.x + 10, self.y + 5, 100, 210)
		self.is_hit = False

	def draw(self, win):
		win.blit(self.img, (self.x, self.y))
		# pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)
		self.hit_box = (self.x + 10, self.y + 5, 100, 210)

	def hit(self):
		self.is_hit = True
		McQueen.energy_ -= 50

	def crash_sound(self):
		if self.is_hit:
			crash_sound = pygame.mixer.Sound('sounds/01-crash-consolidated.wav')
			crash_sound.play()


class Police(Car):
	def __init__(self, width, height, speed):
		super().__init__(width, height, speed)
		self.img = pygame.image.load('images/police.png')
		self.hit_box = (self.x + 10, self.y + 5, 100, 230)

	def draw(self, win):
		win.blit(self.img, (self.x, self.y))
		# pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)
		self.hit_box = (self.x + 10, self.y + 5, 100, 230)

	def siren(self):
		siren = pygame.mixer.Sound("sounds/09-police-consolidated.wav")
		siren.play()

	def hit(self):
		self.is_hit = True
		McQueen.energy_ -= 200

	def crash_sound(self):
		if self.is_hit:
			crash_sound = pygame.mixer.Sound('sounds/01-crash2-consolidated.wav')
			crash_sound.play()


class Ambulance(Car):
	def __init__(self, width, height, speed):
		super().__init__(width, height, speed)
		self.img = pygame.image.load('images/ambulance.png')
		self.hit_box = (self.x + 15, self.y + 10, 115, 300)

	def draw(self, win):
		win.blit(self.img, (self.x, self.y))
		# pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)
		self.hit_box = (self.x + 15, self.y + 10, 115, 300)

	def siren(self):
		siren = pygame.mixer.Sound("sounds/01-ambulance-consolidated.wav")
		siren.play()

	def hit(self):
		self.is_hit = True
		McQueen.energy_ += 300

	def crash_sound(self):
		if self.is_hit:
			horns = pygame.mixer.Sound('sounds/health_boost.wav')
			horns.play()


class FireTruck(Car):
	def __init__(self, width, height, speed):
		super().__init__(width, height, speed)
		self.img = pygame.image.load('images/fire_truck.png')
		self.hit_box = (self.x + 5, self.y + 5, 130, 440)

	def draw(self, win):
		win.blit(self.img, (self.x, self.y))
		# pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)
		self.hit_box = (self.x + 5, self.y + 5, 130, 440)

	def siren(self):
		siren = pygame.mixer.Sound("sounds/04-fire_truck-consolidated.wav")
		siren.play()

	def hit(self):
		self.is_hit = True
		McQueen.energy_ -= 300

	def crash_sound(self):
		if self.is_hit:
			crash_sound = pygame.mixer.Sound('sounds/01-crash2-consolidated.wav')
			crash_sound.play()


class Explosion(object):
	def __init__(self, x, y, width, height, speed):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.speed = speed
		self.img = pygame.image.load('images/explosion.png')
		self.hit_box = None

	def draw(self, win):
		win.blit(self.img, (self.x, self.y))

	def hit(self):
		pass

	def crash_sound(self):
		pass


class Hole(object):
	img = pygame.image.load('images/hole.png')

	def __init__(self):
		self.x = randrange(50, 1000)
		self.y = -160
		self.w = 150
		self.h = 75
		self.hit_box = (self.x + 30, self.y + 15, 95, 45)
		self.is_hit = False

	def draw(self, win):
		win.blit(self.img, (self.x, self.y))
		# pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)
		if self.is_hit:
			self.hit_box = None
		else:
			self.hit_box = (self.x + 30, self.y + 15, 95, 45)

	def hit(self):
		self.is_hit = True
		McQueen.energy_ -= 10

	def crash_sound(self):
		if self.is_hit:
			hit_sound = pygame.mixer.Sound('sounds/02-hole-consolidated.wav')
			hit_sound.play()
