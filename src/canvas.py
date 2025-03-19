import os
import pygame


class PopUp:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def update(self):
        if self.size > 0:
            self.size -= 1
        else:
            self.size = 0


class Canvas:
    def __init__(self, screen, base_dir, screen_size, screen_scale, controller, player, drum_kit):
        self.screen = screen
        self.base_dir = base_dir
        self.screen_size = screen_size
        self.screen_scale = screen_scale

        self.controller = controller
        self.drum_kit = drum_kit
        self.player = player
        self.controller = controller

        self.sprites = {}
        self.load_sprites()

    def load_sprites(self):
        sprite_dir = os.path.join(self.base_dir, 'bin', 'sprites')
        for spr_img in os.listdir(sprite_dir):
            image = pygame.image.load(os.path.join(sprite_dir, spr_img)).convert_alpha()
            self.sprites[spr_img[:-4]] = image

    def draw(self):
        self.draw_drums()
        self.draw_sprite(self.sprites['logo'], x=87, y=34, rot=0, scale=self.screen_scale)

    def draw_drums(self):
        self.draw_sprite(self.sprites['stand_tall'], x=22, y=52, rot=0, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['stand_tall'], x=45, y=52, rot=0, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['stand_medium'], x=25, y=56, rot=0, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['stand_hihat'], x=41, y=56, rot=0, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['stand_kick'], x=32, y=61, rot=0, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['stand_snare'], x=37, y=60, rot=0, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['stand_floortom'], x=27, y=61, rot=0, scale=self.screen_scale, colour=(86, 108, 134))

        self.draw_sprite(self.sprites['drum_snare'], x=37, y=56, rot=0, scale=self.screen_scale+self.drum_kit.snare.scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['drum_floor'], x=27, y=56, rot=self.drum_kit.floortom.rotation, scale=self.screen_scale+self.drum_kit.floortom.scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['drum_rack'], x=30, y=52, rot=self.drum_kit.racktom.rotation, scale=self.screen_scale+self.drum_kit.racktom.scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['drum_kick'], x=32, y=57, rot=0, scale=self.screen_scale+self.drum_kit.kick.scale, colour=(86, 108, 134))

        self.draw_sprite(self.sprites['cymbal_crash'], x=21.5, y=45.5, rot=self.drum_kit.cymbal_crash1.rotation, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['cymbal_crash'], x=44.5, y=45.5, rot=self.drum_kit.cymbal_crash2.rotation, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['cymbal_ride'], x=24.5, y=52.5, rot=self.drum_kit.cymbal_ride.rotation, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['cymbal_hihat'], x=41, y=52, rot=0, scale=self.screen_scale, colour=(86, 108, 134))

        self.draw_sprite(self.sprites['player'], x=33, y=self.player.y+1, rot=0, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['player'], x=32, y=self.player.y, rot=0, scale=self.screen_scale)
        self.draw_sprite(self.sprites['drumstick'], x=self.player.left_stick.x, y=self.player.left_stick.y, rot=self.player.left_stick.rot, scale=self.screen_scale)
        self.draw_sprite(self.sprites['drumstick'], x=self.player.right_stick.x, y=self.player.right_stick.y, rot=self.player.right_stick.rot, scale=self.screen_scale)

        self.draw_sprite(self.sprites['stand_tall'], x=21, y=51, rot=0, scale=self.screen_scale)
        self.draw_sprite(self.sprites['stand_tall'], x=44, y=51, rot=0, scale=self.screen_scale)
        self.draw_sprite(self.sprites['stand_medium'], x=24, y=55, rot=0, scale=self.screen_scale)
        self.draw_sprite(self.sprites['stand_hihat'], x=40, y=55, rot=0, scale=self.screen_scale)
        self.draw_sprite(self.sprites['stand_kick'], x=31, y=60, rot=0, scale=self.screen_scale)
        self.draw_sprite(self.sprites['stand_snare'], x=36, y=59, rot=0, scale=self.screen_scale)
        self.draw_sprite(self.sprites['stand_floortom'], x=26, y=60, rot=0, scale=self.screen_scale)

        self.draw_sprite(self.sprites['drum_snare'], x=36, y=55, rot=self.drum_kit.snare.rotation, scale=self.screen_scale+(self.drum_kit.snare.scale/4 * self.screen_scale))
        self.draw_sprite(self.sprites['drum_floor'], x=26, y=57, rot=self.drum_kit.floortom.rotation, scale=self.screen_scale+(self.drum_kit.floortom.scale/4 * self.screen_scale))
        self.draw_sprite(self.sprites['drum_rack'], x=29, y=51, rot=self.drum_kit.racktom.rotation, scale=self.screen_scale+(self.drum_kit.racktom.scale/4 * self.screen_scale))
        self.draw_sprite(self.sprites['drum_kick'], x=31, y=56, rot=self.drum_kit.kick.rotation, scale=self.screen_scale+(self.drum_kit.kick.scale/4 * self.screen_scale))

        self.draw_sprite(self.sprites['cymbal_crash'], x=20.5, y=44.5, rot=self.drum_kit.cymbal_crash1.rotation, scale=self.screen_scale)
        self.draw_sprite(self.sprites['cymbal_crash'], x=43.5, y=44.5, rot=self.drum_kit.cymbal_crash2.rotation, scale=self.screen_scale)
        self.draw_sprite(self.sprites['cymbal_ride'], x=23.5, y=51.5, rot=self.drum_kit.cymbal_ride.rotation, scale=self.screen_scale)
        self.draw_sprite(self.sprites['cymbal_hihat'], x=40, y=51, rot=0, scale=self.screen_scale)
        self.draw_sprite(self.sprites['cymbal_hihat_top'], x=40, y=self.drum_kit.cymbal_hihat.height, rot=self.drum_kit.cymbal_hihat.rotation, scale=self.screen_scale)

    def draw_sprite(self, sprite_img_original, x, y, rot, scale, colour=None, flipped=False):
        sprite_img = sprite_img_original.copy()
        if colour:
            pixel_array = pygame.PixelArray(sprite_img)
            for px in range(sprite_img.get_width()):
                for py in range(sprite_img.get_height()):
                    alpha = pixel_array[px, py] >> 24  # Extract the alpha component
                    pixel_array[px, py] = (alpha << 24) | (colour[0] << 16) | (colour[1] << 8) | colour[2]  # RGBA format

        sprite_img = pygame.transform.scale(sprite_img, (sprite_img.get_width()*scale, sprite_img.get_height()*scale))

        if rot:
            sprite_img = pygame.transform.rotate(sprite_img, rot)

        if flipped:
            sprite_img = pygame.transform.flip(sprite_img, flip_x=flipped, flip_y=False)

        rect = sprite_img.get_rect(center=((x*self.screen_scale), (y*self.screen_scale)))
        self.screen.blit(sprite_img, rect.topleft)
