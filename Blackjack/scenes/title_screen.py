from scenes.scene_template import Scene
import pygame
from components import Button
import components

#PLEASE CHANGE THIS RESOURCES PATH TO WHEREEVER THE FINAL PROJECT IS STORED ON YOUR MACHINE
#YOU NEED TO INCLUDE 2 \\'s AT THE END AS THE LAST ONE IS PERCEIVED AS EOL (END OF LINE)
resources_path = r"C:\Users\user\Desktop\SFU\CMPT 365\Final Project\Blackjack\resources\\"
button_width = 200
button_height = 80
size = (928, 696)
centerx = size[0]//2
centery = size[1]//2

button_rect = pygame.Rect((centerx - button_width/2),(centery - button_height/2 + 100), button_width, button_height)
button_color = (46, 46, 234)
button_text_color = (216, 47, 213)
bg_color_def = (52, 36, 173)
bg_color_grad = (127, 27, 170)
button_color_def = (30, 16, 229)
button_color_grad = (85, 0, 244)

class Logo(pygame.sprite.Sprite):

    def __init__(self):
        self.logo = self.casino_logo_gfx()
        self.logo_rect = self.logo.get_rect(right =0, centery = centery - 175)
        self.x = self.logo_rect.x
        self.finished = False

    def update(self, surface, tick):
        if not self.finished:
            self.logo_rect.x += 0.4 * tick

        if self.logo_rect.x  >= centerx - 350:
            self.finished = True 
            self.logo_rect.x = centerx - 350

    def draw(self, surface):
        surface.blit(self.logo, self.logo_rect)

    def casino_logo_gfx(self):
        return pygame.image.load(resources_path + r"graphics" + r"\blackjack_logo.png")


class TitleScreen(Scene):
    
    name = "title_screen"
    
    def __init__(self):      
        super().__init__()
        self.background_color = (10, 10, 30)
        self.logo = Logo()
        self.play_button = Button(button_color_def, button_color_grad, button_rect , button_text_color, "blippo" ,60,"Play")

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.finished = True
            self.quit = True 
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_F4:
                self.finished  = True
                self.quit = True

    def update(self, surface, keys, tick):
        self.play_button.update()
        if self.play_button.action == 'pressed':
            self.next = "blackjack"
            self.finished = True
        self.logo.update(surface, tick)
        self.draw(surface)
    

    def draw(self, surface):
        components.fill_gradient(surface,bg_color_def,bg_color_grad)
        self.logo.draw(surface)
        self.play_button.draw(surface)
        

