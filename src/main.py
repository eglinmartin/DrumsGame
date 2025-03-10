import sys
import pygame

from utils import Input, create_sine_wave
from canvas import Canvas


class Drumstick:
    def __init__(self, base_x, base_y):
        self.x = base_x
        self.y = base_y
        self.rot = 0


class Player:
    def __init__(self):
        self.base_y = 48
        self.y = self.base_y

        self.left_stick = Drumstick(base_x=37, base_y=49)
        self.right_stick = Drumstick(base_x=27, base_y=49)

    def trigger(self):
        self.y += 0.5

    def update(self):
        if self.y > self.base_y:
            self.y -= 0.05
        else:
            self.y = self.base_y


class Cymbal:
    def __init__(self, base_angle, vel_amount, direction):
        self.velocity = 0
        self.rotation_animation = create_sine_wave(20, 5, 8, 800)
        self.rotation_frame = 0
        self.vel_amount = vel_amount
        self.base_angle = base_angle
        self.rotation = base_angle
        self.direction = direction

    def trigger(self):
        self.rotation_frame = 5
        self.velocity = self.vel_amount

    def update(self):
        if self.velocity > 0:
            self.velocity -= 0.05
        else:
            self.velocity = 0

        # Rotate orders
        self.rotation_frame += 1
        if self.rotation_frame >= len(self.rotation_animation) - 1:
            self.rotation_frame = 0

        if self.velocity > 0:
            if self.direction == 1:
                self.rotation = self.base_angle+self.rotation_animation[self.rotation_frame] * self.velocity
            else:
                self.rotation = self.base_angle-self.rotation_animation[self.rotation_frame] * self.velocity
        else:
            self.rotation = self.base_angle


class Drum:
    def __init__(self, base_angle, vel_amount):
        self.vel_amount = vel_amount
        self.scale = 0
        self.rotation = base_angle

    def trigger(self):
        self.scale = self.vel_amount

    def update(self):
        if self.scale > 0:
            self.scale -= 0.1
        else:
            self.scale = 0


class DrumKit:
    def __init__(self):
        self.kick = Drum(base_angle=0, vel_amount=1)
        self.snare = Drum(base_angle=0, vel_amount=1)
        self.racktom = Drum(base_angle=355, vel_amount=1)
        self.floortom = Drum(base_angle=0, vel_amount=1)

        self.cymbal_crash1 = Cymbal(base_angle=340, vel_amount=4, direction=0)
        self.cymbal_crash2 = Cymbal(base_angle=20, vel_amount=4, direction=1)
        self.cymbal_ride = Cymbal(base_angle=355, vel_amount=1, direction=0)

    def update(self):
        self.kick.update()
        self.snare.update()
        self.racktom.update()
        self.floortom.update()

        self.cymbal_crash1.update()
        self.cymbal_crash2.update()
        self.cymbal_ride.update()


def parse_user_input(player, drum_kit):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()

            # Kick drum
            if event.key == pygame.K_SPACE:
                drum_kit.kick.trigger()
                player.trigger()

            # Snare drum
            if event.key == pygame.K_a:
                drum_kit.snare.trigger()

            # Rack tom
            if event.key == pygame.K_s:
                drum_kit.racktom.trigger()

            # Floor tom
            if event.key == pygame.K_d:
                drum_kit.floortom.trigger()

            # Hi-hat cymbal
            if event.key == pygame.K_PERIOD:
                if key[pygame.K_LSHIFT]:
                    print(Input.HIHAT_OPEN)
                else:
                    print(Input.HIHAT)

            # Ride cymbal
            if event.key == pygame.K_COMMA:
                drum_kit.cymbal_ride.trigger()

            # Crash cymbal 1
            if event.key == pygame.K_m:
                drum_kit.cymbal_crash1.trigger()

            # Crash cymbal 2
            if event.key == pygame.K_SLASH:
                drum_kit.cymbal_crash2.trigger()

    # Snare roll
    key = pygame.key.get_pressed()
    if key[pygame.K_LCTRL] and key[pygame.K_a]:
        print(Input.SNAREROLL)


def run_game(screen, scale, base_dir, canvas, player, drum_kit):
    player.update()
    drum_kit.update()

    clock = pygame.time.Clock()
    fps = 60

    parse_user_input(player, drum_kit)

    screen.fill((148, 176, 194))
    canvas.draw()
    pygame.display.flip()
    clock.tick(fps)


def main():
    pygame.init()
    base_dir = r"C:\Storage\Programming\DrumsGame"

    screen_size = {'width':128, 'height': 72}
    screen_scale = 8

    screen = pygame.display.set_mode((screen_size['width']*screen_scale,
                                      screen_size['height']*screen_scale))

    pygame.display.set_caption("Drum Game")

    player = Player()
    drum_kit = DrumKit()
    canvas = Canvas(screen, base_dir, screen_size, screen_scale, player, drum_kit)

    while True:
        run_game(screen, screen_scale, base_dir, canvas, player, drum_kit)


if __name__ == '__main__':
    main()
