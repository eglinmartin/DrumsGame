import sys
import pygame

from canvas import Canvas


def run_game(screen, scale, base_dir, canvas):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock = pygame.time.Clock()
    fps = 60

    canvas.draw()
    pygame.display.flip()
    clock.tick(fps)


def main():
    pygame.init()
    base_dir = r"C:\Storage\Programming\DrumsGame"

    screen_size = {'width':128, 'height': 72}
    screen_scale = 5

    screen = pygame.display.set_mode((screen_size['width']*screen_scale,
                                      screen_size['height']*screen_scale))
    screen.fill((148, 176, 194))

    pygame.display.set_caption("Drum Game")

    canvas = Canvas(screen, base_dir, screen_size, screen_scale)


    while True:
        run_game(screen, screen_scale, base_dir, canvas)


if __name__ == '__main__':
    main()
