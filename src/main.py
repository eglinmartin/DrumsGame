import sys
import os
import pygame
import random

from utils import Input, create_sine_wave
from canvas import Canvas


class Controller:
    def __init__(self):
        pass

    def update(self):
        pass


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

        # self.left_stick = Drumstick(base_x=36, base_y=49)
        # self.right_stick = Drumstick(base_x=30, base_y=49)
        self.trigger_positions = {
            Input.CRASH1: [self.x-6, self.y-4, 225],
            Input.CRASH2: [self.x+6, self.y-5, 135],
            Input.RIDE: [self.x-2, self.y+1, 260],
            Input.HIHAT: [self.x+7, self.y, 100],
            Input.HIHAT_OPEN: [self.x+7, self.y-1, 100],
            Input.SNARE: [self.x+2, self.y+4, 330],
            Input.RACKTOM: [self.x-7, self.y+1, 320],
            Input.FLOORTOM: [self.x-1, self.y+4, 300]
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
    def __init__(self, drum_kit):
        self.x = drum_kit.x + 1
        self.base_y = drum_kit.y - 8
        self.y = self.base_y

        self.left_stick = Drumstick(base_x=self.x+4, base_y=self.y+1)
        self.right_stick = Drumstick(base_x=self.x-4, base_y=self.y+1)

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


class Hardware:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.rotation = 0
        self.scale = 0
        self.name = name

    def update(self):
        pass


class Cymbal:
    def __init__(self, x, y, base_angle, vel_amount, direction, name, hihat=False):
        self.x = x
        self.y = y
        self.velocity = 0
        self.rotation_animation = create_sine_wave(20, 5, 8, 800)
        self.rotation_frame = 0
        self.vel_amount = vel_amount
        self.base_angle = base_angle
        self.rotation = base_angle
        self.direction = direction
        self.name = name
        self.scale = 0

        self.hihat = hihat
        self.raised = False
        self.base_height = y
        self.height = self.base_height

    def trigger(self):
        if self.hihat:
            if self.raised:
                self.rotation_frame = 5
                self.velocity = self.vel_amount
        else:
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

        if self.hihat:
            if self.raised:
                if self.y > (self.base_height - 0.8):
                    self.y -= 0.2
                else:
                    self.y = (self.base_height - 0.8)
            else:
                if self.y < self.base_height:
                    self.y += 0.4
                else:
                    self.y = self.base_height


class Drum:
    def __init__(self, x, y, base_angle, vel_amount, name):
        self.x = x
        self.y = y
        self.vel_amount = vel_amount
        self.scale = 0
        self.rotation = base_angle
        self.name = name

    def trigger(self):
        self.scale = self.vel_amount

    def update(self):
        if self.scale > 0:
            self.scale -= 0.1
        else:
            self.scale = 0


class DrumKit:
    def __init__(self):
        self.x = 63
        self.y = 59

        self.stand_kick = Hardware(x=self.x, y=self.y+4, name='stand_kick')
        self.stand_snare = Hardware(x=self.x+5, y=self.y+3, name='stand_snare')
        self.stand_floortom = Hardware(x=self.x-5, y=self.y+4, name='stand_floortom')
        self.stand_hihat = Hardware(x=self.x+9, y=self.y-1, name='stand_hihat')
        self.stand_ride = Hardware(x=self.x-9, y=self.y-1, name='stand_medium')
        self.stand_crash1 = Hardware(x=self.x-11, y=self.y-5, name='stand_tall')
        self.stand_crash2 = Hardware(x=self.x+13, y=self.y-5, name='stand_tall')
        self.cymbal_hihat_bottom = Hardware(x=self.x+9, y=self.y-5, name='cymbal_hihat')

        self.kick = Drum(x=self.x, y=self.y, base_angle=0, vel_amount=1, name='drum_kick')
        self.snare = Drum(x=self.x+5, y=self.y-1, base_angle=0, vel_amount=1, name='drum_snare')
        self.racktom = Drum(x=self.x-2, y=self.y-5, base_angle=355, vel_amount=1, name='drum_rack')
        self.floortom = Drum(x=self.x-5, y=self.y+1, base_angle=0, vel_amount=1, name='drum_floor')

        self.cymbal_hihat = Cymbal(x=self.x+9, y=self.y-6, base_angle=0, vel_amount=1, direction=1, name='cymbal_hihat_top', hihat=True)
        self.cymbal_crash1 = Cymbal(x=self.x-11.5, y=self.y-11.5, base_angle=340, vel_amount=4, direction=0, name='cymbal_crash')
        self.cymbal_crash2 = Cymbal(x=self.x+12.5, y=self.y-11.5, base_angle=20, vel_amount=4, direction=1, name='cymbal_crash')
        self.cymbal_ride = Cymbal(x=self.x-9.5, y=self.y-4.5, base_angle=355, vel_amount=1, direction=0, name='cymbal_ride')

        self.elements = [
            self.stand_kick, self.stand_snare, self.stand_floortom,
            self.stand_hihat, self.stand_ride, self.stand_crash1,
            self.stand_crash2, self.cymbal_hihat_bottom,
            self.floortom, self.racktom, self.snare, self.kick,
            self.cymbal_crash1, self.cymbal_hihat, self.cymbal_ride, self.cymbal_crash2
        ]

    def update(self):
        for element in self.elements:
            element.update()


def parse_user_input(player, drum_kit, mixer, controller):
    # Get state of held keys
    key = pygame.key.get_pressed()
    if key[pygame.K_LSHIFT]:
        drum_kit.cymbal_hihat.raised = False
    else:
        drum_kit.cymbal_hihat.raised = True

    # Get state of pressed keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
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
            if event.key == pygame.K_COMMA:
                if drum_kit.cymbal_hihat.raised:
                    drum_kit.cymbal_hihat.trigger()
                    player.trigger(Input.HIHAT_OPEN)
                    mixer.play_sound(Input.HIHAT_OPEN)
                else:
                    player.trigger(Input.HIHAT)
                    mixer.play_sound(Input.HIHAT)

            # Hi-hat pedal
            if event.key == pygame.K_LSHIFT:
                mixer.play_sound(Input.HIHAT)

            # Ride cymbal
            if event.key == pygame.K_PERIOD:
                drum_kit.cymbal_ride.trigger()
                player.trigger(Input.RIDE)
                mixer.play_sound(Input.RIDE)

            # Crash cymbal 1
            if event.key == pygame.K_SLASH:
                drum_kit.cymbal_crash1.trigger()
                player.trigger(Input.CRASH1)
                mixer.play_sound(Input.CRASH1)

            # Crash cymbal 2
            if event.key == pygame.K_m:
                drum_kit.cymbal_crash2.trigger()
                player.trigger(Input.CRASH2)
                mixer.play_sound(Input.CRASH2)


def run_game(clock, screen, canvas, player, drum_kit, mixer, controller):
    player.update()
    drum_kit.update()
    controller.update()

    parse_user_input(player, drum_kit, mixer, controller)

    screen.fill((148, 176, 194))
    canvas.draw()
    pygame.display.flip()

    clock.tick(60)


def main():
    pygame.init()

    base_dir = r"C:\Storage\Programming\DrumsGame"
    pygame.mixer.init(channels=16)
    mixer = Mixer(base_dir)

    screen_size = {'width':128, 'height': 72}
    screen_scale = 8

    screen = pygame.display.set_mode((screen_size['width']*screen_scale,
                                     screen_size['height']*screen_scale))

    controller = Controller()

    drum_kit = DrumKit()
    player = Player(drum_kit)
    canvas = Canvas(screen, base_dir, screen_size, screen_scale, controller, player, drum_kit)

    clock = pygame.time.Clock()
    while True:
        run_game(clock, screen, canvas, player, drum_kit, mixer, controller)


if __name__ == '__main__':
    main()
