import os
import pygame

class Canvas:
    def __init__(self, screen, base_dir, screen_size, screen_scale):
        self.screen = screen
        self.base_dir = base_dir
        self.screen_size = screen_size
        self.screen_scale = screen_scale

    def draw(self):
        self.draw_drums()

    def draw_drums(self):
        self.draw_sprite('sprites', 'drum_snare', x=37, y=57, rot=0, scale=self.screen_scale)
        self.draw_sprite('sprites', 'drum_floor', x=26, y=57, rot=0, scale=self.screen_scale)
        self.draw_sprite('sprites', 'drum_rack', x=29, y=51, rot=0, scale=self.screen_scale)
        self.draw_sprite('sprites', 'drum_kick', x=31, y=56, rot=0, scale=self.screen_scale)

        self.draw_sprite('sprites', 'stand_tall', x=21, y=51, rot=0, scale=self.screen_scale)
        self.draw_sprite('sprites', 'stand_tall', x=44, y=51, rot=0, scale=self.screen_scale)
        self.draw_sprite('sprites', 'stand_medium', x=24, y=55, rot=0, scale=self.screen_scale)
        self.draw_sprite('sprites', 'stand_hihat', x=40, y=55, rot=0, scale=self.screen_scale)

        self.draw_sprite('sprites', 'cymbal_crash1', x=20.5, y=44.5, rot=0, scale=self.screen_scale)
        self.draw_sprite('sprites', 'cymbal_crash2', x=43.5, y=44.5, rot=0, scale=self.screen_scale)
        self.draw_sprite('sprites', 'cymbal_ride', x=23.5, y=51.5, rot=0, scale=self.screen_scale)
        self.draw_sprite('sprites', 'cymbal_hihat', x=40, y=50, rot=0, scale=self.screen_scale)

    def draw_sprite(self, sprite_dir, sprite_name, x, y, rot, scale, colour=None, flipped=False):
        sprite_img = (pygame.image.load(os.path.join(self.base_dir, 'bin', sprite_dir, f'{sprite_name}.png'))
                      .convert_alpha())
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
