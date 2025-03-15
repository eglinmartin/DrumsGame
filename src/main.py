import sys
import os
import pygame

from utils import Input, create_sine_wave
from canvas import Canvas


class Mixer:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def play_sound(self, input_type):
        channel_id = input_type.value['channel']
        ogg_name = f'{str(input_type).lower().split('.')[1]}.ogg'
        sound = pygame.mixer.Sound(os.path.join(self.base_dir, 'ogg', ogg_name))
        pygame.mixer.Channel(channel_id).play(sound)


class Drumstick:
    def __init__(self, base_x, base_y):
        self.base_x = base_x
        self.base_y = base_y
        self.x = base_x
        self.y = base_y
        self.base_rot = 180
        self.rot = 180

        self.distance_x = 0
        self.distance_y = 0
        self.distance_rot = 0

        self.trigger_positions = {
            Input.CRASH1: [24, 46, 225],
            Input.CRASH2: [40, 45, 135],
            Input.RIDE: [22, 50, 300],
            Input.HIHAT: [36, 50, 100],
            Input.HIHAT_OPEN: [36, 48, 100],
            Input.SNARE: [3, 52, 300],
            Input.RACKTOM: [29, 48, 300],
            Input.FLOORTOM: [25, 52, 300]
        }

    def trigger(self, input_type):
        self.x = self.trigger_positions.get(input_type)[0]
        self.y = self.trigger_positions.get(input_type)[1]
        self.rot = self.trigger_positions.get(input_type)[2]

        self.distance_x = abs(self.x - self.base_x)
        self.distance_y = abs(self.y - self.base_y)
        self.distance_rot = abs(self.rot - self.base_rot)

    def update(self):
        if abs(self.base_x - self.x) < 1:
            self.x = self.base_x
        elif self.x > self.base_x:
            self.x -= self.distance_x / 10
        elif self.x < self.base_x:
            self.x += self.distance_x / 10

        if abs(self.base_y - self.y) < 1:
            self.y = self.base_y
        elif self.y > self.base_y:
            self.y -= self.distance_y / 10
        elif self.y < self.base_y:
            self.y += self.distance_y / 10

        if abs(self.base_rot - self.rot) < 5:
            self.y = self.base_y
        if self.rot < self.base_rot:
            self.rot += self.distance_rot / 10
        elif self.rot > self.base_rot:
            self.rot -= self.distance_rot / 10


class Player:
    def __init__(self):
        self.base_y = 48
        self.y = self.base_y

        self.left_stick = Drumstick(base_x=36, base_y=49)
        self.right_stick = Drumstick(base_x=30, base_y=49)

    def trigger(self, input_type):
        if input_type == Input.KICK:
            self.y = self.base_y + 0.5

        if input_type in [Input.CRASH1, Input.HIHAT, Input.HIHAT_OPEN, Input.RIDE, Input.FLOORTOM]:
            self.right_stick.trigger(input_type)
        elif input_type in [Input.SNARE, Input.CRASH2, Input.RACKTOM]:
            self.left_stick.trigger(input_type)

    def update(self):
        if self.y > self.base_y:
            self.y -= 0.05
        else:
            self.y = self.base_y

        self.left_stick.update()
        self.right_stick.update()


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


def parse_user_input(player, drum_kit, mixer):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()

            # Kick drum
            if event.key == pygame.K_SPACE:
                drum_kit.kick.trigger()
                player.trigger(Input.KICK)
                mixer.play_sound(Input.KICK)

            # Snare drum
            if event.key == pygame.K_a:
                drum_kit.snare.trigger()
                player.trigger(Input.SNARE)
                mixer.play_sound(Input.SNARE)

            # Rack tom
            if event.key == pygame.K_s:
                drum_kit.racktom.trigger()
                player.trigger(Input.RACKTOM)
                mixer.play_sound(Input.RACKTOM)

            # Floor tom
            if event.key == pygame.K_d:
                drum_kit.floortom.trigger()
                player.trigger(Input.FLOORTOM)
                mixer.play_sound(Input.FLOORTOM)

            # Hi-hat cymbal
            if event.key == pygame.K_PERIOD:
                if key[pygame.K_LSHIFT]:
                    player.trigger(Input.HIHAT)
                    mixer.play_sound(Input.HIHAT)
                    print('closed')
                else:
                    player.trigger(Input.HIHAT_OPEN)
                    mixer.play_sound(Input.HIHAT_OPEN)
                    print('open')

            # Hi-hat pedal
            if event.key == pygame.K_LSHIFT:
                mixer.play_sound(Input.HIHAT)

            # Ride cymbal
            if event.key == pygame.K_COMMA:
                drum_kit.cymbal_ride.trigger()
                player.trigger(Input.RIDE)
                mixer.play_sound(Input.RIDE)

            # Crash cymbal 1
            if event.key == pygame.K_m:
                drum_kit.cymbal_crash1.trigger()
                player.trigger(Input.CRASH1)
                mixer.play_sound(Input.CRASH1)

            # Crash cymbal 2
            if event.key == pygame.K_SLASH:
                drum_kit.cymbal_crash2.trigger()
                player.trigger(Input.CRASH2)
                mixer.play_sound(Input.CRASH2)

    # Snare roll
    key = pygame.key.get_pressed()
    if key[pygame.K_LCTRL] and key[pygame.K_a]:
        print(Input.SNAREROLL)


def run_game(screen, canvas, player, drum_kit, mixer):
    player.update()
    drum_kit.update()

    clock = pygame.time.Clock()
    fps = 60

    parse_user_input(player, drum_kit, mixer)

    screen.fill((148, 176, 194))
    canvas.draw()
    pygame.display.flip()
    clock.tick(fps)


def main():
    pygame.init()

    base_dir = r"C:\Storage\Programming\DrumsGame"
    pygame.mixer.init(channels=16)
    mixer = Mixer(base_dir)

    screen_size = {'width':128, 'height': 72}
    screen_scale = 8

    screen = pygame.display.set_mode((screen_size['width']*screen_scale,
                                     screen_size['height']*screen_scale))

    player = Player()
    drum_kit = DrumKit()
    canvas = Canvas(screen, base_dir, screen_size, screen_scale, player, drum_kit)

    while True:
        run_game(screen, canvas, player, drum_kit, mixer)


if __name__ == '__main__':
    main()
