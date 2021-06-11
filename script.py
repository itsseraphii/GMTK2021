import pygame
import sys

SIZE = WIDTH, HEIGHT = 1280, 720
SPEED = [2, 2]
BLACK = 0, 0, 0

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SIZE)

    i = 0
    ballRect = []
    ballImg = []

    # Attention: code de qualité:
    while 1:
        try:
            ballImg.append(pygame.image.load("res/dvd-logo" + str(i) + ".png"))
            ballImg[i] = pygame.transform.smoothscale(ballImg[i], (256, 142))
            ballRect.append(ballImg[i].get_rect())
        except:
            break
        i+=1

    imgCount = i
    i = 0
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        ballRect[i] = ballRect[i].move(SPEED)

        if ballRect[i].left < 0 or ballRect[i].right > WIDTH:
            SPEED[0] = -SPEED[0]
            x = ballRect[i].x
            y = ballRect[i].y
            i = (i + 1) % imgCount
            ballRect[i].x = x
            ballRect[i].y = y
            

        if ballRect[i].top < 0 or ballRect[i].bottom > HEIGHT:
            SPEED[1] = -SPEED[1]
            x = ballRect[i].x
            y = ballRect[i].y
            i = (i + 1) % imgCount
            ballRect[i].x = x
            ballRect[i].y = y

        screen.fill(BLACK)
        screen.blit(ballImg[i], ballRect[i])
        pygame.display.flip()
        clock.tick(60)
        