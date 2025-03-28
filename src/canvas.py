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

        self.sprites = {}
        self.load_sprites()

        self.shadow_surf = pygame.Surface((self.screen_size['width'] * self.screen_scale,
                                      self.screen_size['height'] * self.screen_scale))
        self.shadow_surf.set_colorkey((2, 3, 4))
        self.shadow_surf.set_alpha(128)

    def load_sprites(self):
        sprite_dir = os.path.join(self.base_dir, 'bin', 'sprites')
        for spr_img in os.listdir(sprite_dir):
            image = pygame.image.load(os.path.join(sprite_dir, spr_img)).convert_alpha()
            self.sprites[spr_img[:-4]] = image

    def draw(self):
        self.draw_shadows_layer()
        self.draw_foreground_layer()

    def draw_shadows_layer(self):
        sprites = []
        self.shadow_surf.fill((2, 3, 4))

        # Draw logo shadow
        sprites.append(self.draw_sprite(self.sprites['logo'], x=self.controller.logo.x+1,
                                        y=self.controller.logo.y+1, rot=self.controller.logo.rotation,
                                        scale=self.screen_scale, shadow=True))

        # Draw player
        sprites.append(self.draw_sprite(self.sprites['player'], x=self.player.x+1, y=self.player.y+1, rot=0, scale=self.screen_scale, shadow=True))
        sprites.append(self.draw_sprite(self.sprites['drumstick'], x=self.player.left_stick.x+1, y=self.player.left_stick.y+1, rot=self.player.left_stick.rot, scale=self.screen_scale, shadow=True))
        sprites.append(self.draw_sprite(self.sprites['drumstick'], x=self.player.right_stick.x+1, y=self.player.right_stick.y+1, rot=self.player.right_stick.rot, scale=self.screen_scale, shadow=True))

        for element in self.drum_kit.elements:
            sprites.append(self.draw_sprite(self.sprites[element.name], x=element.x + 1, y=element.y + 1,
                                            rot=element.rotation, scale=self.screen_scale, shadow=True))

        for sprite in sprites:
            self.shadow_surf.blit(sprite[0], sprite[1])

        self.screen.blit(self.shadow_surf, (0, 0))


    def draw_foreground_layer(self):
        sprites = []

        # Draw logo
        sprites.append(self.draw_sprite(self.sprites['logo'], x=self.controller.logo.x,
                                        y=self.controller.logo.y, rot=self.controller.logo.rotation,
                                        scale=self.screen_scale + self.controller.logo.scale))

        # Draw player
        sprites.append(self.draw_sprite(self.sprites['player'], x=self.player.x, y=self.player.y, rot=0, scale=self.screen_scale))
        sprites.append(self.draw_sprite(self.sprites['drumstick'], x=self.player.left_stick.x, y=self.player.left_stick.y, rot=self.player.left_stick.rot, scale=self.screen_scale))
        sprites.append(self.draw_sprite(self.sprites['drumstick'], x=self.player.right_stick.x, y=self.player.right_stick.y, rot=self.player.right_stick.rot, scale=self.screen_scale))

        for element in self.drum_kit.elements:
            sprites.append(self.draw_sprite(self.sprites[element.name], x=element.x, y=element.y,
                           rot=element.rotation, scale=self.screen_scale + element.scale))

        for sprite in sprites:
            self.screen.blit(sprite[0], sprite[1])


    def draw_sprite(self, sprite_img_original, x, y, rot, scale, colour=None, flipped=False, shadow=False):
        sprite_img = sprite_img_original.copy()

        if shadow:
            colour = (28, 47, 80)

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
        return [sprite_img, rect]
