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
        # Draw shadows
        self.draw_sprite(self.sprites['logo'], x=32, y=22, rot=0, scale=self.screen_scale)

        # Draw shadows
        self.draw_sprite(self.sprites['player'], x=self.player.x+1, y=self.player.y+1, rot=0, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['drumstick'], x=self.player.left_stick.x, y=self.player.left_stick.y, rot=self.player.left_stick.rot, scale=self.screen_scale, colour=(86, 108, 134))
        self.draw_sprite(self.sprites['drumstick'], x=self.player.right_stick.x, y=self.player.right_stick.y, rot=self.player.right_stick.rot, scale=self.screen_scale, colour=(86, 108, 134))

        for element in self.drum_kit.elements:
            self.draw_sprite(self.sprites[element.name], x=element.x + 1, y=element.y + 1, rot=element.rotation,
                             scale=self.screen_scale, colour=(86, 108, 134))

        # Draw foreground
        self.draw_sprite(self.sprites['player'], self.player.x, y=self.player.y, rot=0, scale=self.screen_scale)
        self.draw_sprite(self.sprites['drumstick'], x=self.player.left_stick.x, y=self.player.left_stick.y, rot=self.player.left_stick.rot, scale=self.screen_scale)
        self.draw_sprite(self.sprites['drumstick'], x=self.player.right_stick.x, y=self.player.right_stick.y, rot=self.player.right_stick.rot, scale=self.screen_scale)
        for element in self.drum_kit.elements:
            self.draw_sprite(self.sprites[element.name], x=element.x, y=element.y, rot=element.rotation,
                             scale=self.screen_scale+element.scale)


    def draw_sprite(self, sprite_img_original, x, y, rot, scale, colour=None, flipped=False, alpha=255):
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

        # if alpha < 255:
        #     sprite_img.set_alpha(alpha)

        rect = sprite_img.get_rect(center=((x*self.screen_scale), (y*self.screen_scale)))
        self.screen.blit(sprite_img, rect.topleft)
