import pygame


def welcome(run):
    def redraw_welcome_window(st):
        win.blit(bg, (0, bg_y))
        start_msg = start_font.render('Press SPACE to start', True, (0, 200, 0))
        win.blit(start_msg, (310, 550))
        quit_msg = start_font.render('Press ESC to quit', True, (250, 0, 0))
        win.blit(quit_msg, (350, 15))
        pygame.display.update()

    pygame.mixer.music.load("sounds/Blind.mp3")
    pygame.mixer.music.play(-1)
    horn = pygame.mixer.Sound('sounds/03-horns-consolidated.wav')
    start_font = pygame.font.SysFont('comicsans', size=80, bold=False, italic=True)
    w, h = 1200, 800
    win = pygame.display.set_mode((w, h))
    pygame.display.set_caption("MCQUEEN RUSH")
    bg = pygame.image.load('images/road.png').convert()
    bg_y = 0
    start = False
    while True:
        redraw_welcome_window(start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()
        if keys[pygame.K_SPACE]:
            countdown = pygame.mixer.Sound('sounds/01-countdown-consolidated.wav')
            countdown.play().set_volume(3.0)
            pygame.time.wait(4500)
            pygame.mixer.music.stop()
            horn.play()
            run = True
            return run
