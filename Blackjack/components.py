import pygame

#PLEASE CHANGE THIS RESOURCES PATH TO WHEREEVER THE FINAL PROJECT IS STORED ON YOUR MACHINE
#YOU NEED TO INCLUDE 2 \\'s AT THE END AS THE LAST ONE IS PERCEIVED AS EOL (END OF LINE)
resources_path = r"C:\Users\user\Desktop\SFU\CMPT 365\Final Project\Blackjack\resources\\"

class Button(pygame.sprite.Sprite):

    def __init__(self, def_color, grad_color, rect, button_text_color, font, size, text = ''):
        self.def_color = def_color
        self.grad_color = grad_color
        self.rect = rect
        self.text = text
        self.font = font
        self.size = size
        self.button_text_color = button_text_color
        self.button = self.make_button()
        self.action = None 

    def make_button(self):
        final_button  = pygame.Surface((self.rect.w,self.rect.h)).convert()
        fill_gradient(final_button, self.def_color, self.grad_color)
        final_button_rect =  final_button.get_rect()
        if self.text != '':
            fontpath = resources_path + r"fonts\{}.ttf".format(self.font)
            font = pygame.font.Font(fontpath,self.size)
            text = font.render(self.text, 1, self.button_text_color)
            final_button.blit(text, text.get_rect(center =  final_button_rect.center))
        return final_button

    def update(self):
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if pos[0] > self.rect.left and pos[0] < self.rect.left +self.rect.w:
            if pos[1] > self.rect.top and pos[1] < self.rect.top +self.rect.h:
                if click[0] == 1:
                    #print("button clicked")
                    self.action = "pressed"

    def draw(self, surface):
        surface.blit(self.button, self.rect)



def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
        """fill a surface with a gradient pattern
        Parameters:
        color -> starting color
        gradient -> final color
        rect -> area to fill; default is surface's rect
        vertical -> True=vertical; False=horizontal
        forward -> True=forward; False=reverse
        
        Pygame recipe: http://www.pygame.org/wiki/GradientCode
        """
        if rect is None: rect = surface.get_rect()
        x1,x2 = rect.left, rect.right
        y1,y2 = rect.top, rect.bottom
        if vertical: h = y2-y1
        else:        h = x2-x1
        if forward: a, b = color, gradient
        else:       b, a = color, gradient
        rate = (
            float(b[0]-a[0])/h,
            float(b[1]-a[1])/h,
            float(b[2]-a[2])/h
        )
        fn_line = pygame.draw.line
        if vertical:
            for line in range(y1,y2):
                color = (
                    min(max(a[0]+(rate[0]*(line-y1)),0),255),
                    min(max(a[1]+(rate[1]*(line-y1)),0),255),
                    min(max(a[2]+(rate[2]*(line-y1)),0),255)
                )
                fn_line(surface, color, (x1,line), (x2,line))
        else:
            for col in range(x1,x2):
                color = (
                    min(max(a[0]+(rate[0]*(col-x1)),0),255),
                    min(max(a[1]+(rate[1]*(col-x1)),0),255),
                    min(max(a[2]+(rate[2]*(col-x1)),0),255)
                )
                fn_line(surface, color, (col,y1), (col,y2))
 