import pygame
import pytmx
import pyscroll
import self as self

from player import Player


class Game:

    def __init__(self):
        # creer la fenetre du jeu

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("NibninAdventure - La Fabuleuse Histoire du Fromage Perdu")

        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # generer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # definir une liste qui va stocker les rectangles de collision

        self.walls = []

        for obj in tmx_data.objects:
            if obj.__class__ == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def run(self):

        clock = pygame.time.Clock()

        # boucle du jeu

        running = True

        while running:

            self.handle_input()
            self.group.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()
