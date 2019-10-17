import pygame
from importlib import import_module

class Controller(object):

    def __init__(self, size, names):
        self.screen = pygame.display.get_surface()
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        self.surface = pygame.Surface(size).convert()
        self.iterations = 0 
        self.finished = False
        self.fps = 60.0
        self.time = 0.0
        self.scene =  None
        self.scene_name = None
        self.scene_previous = None
        self.size = size
        self.scene_class_names = names 

    def update(self,tick):
        if self.scene == None:
            raise Exception("No Scene Provided")
        self.screen = pygame.display.get_surface()
        self.time =  pygame.time.get_ticks()
        if self.scene.quit:
            self.finished = True
        elif self.scene.finished:
            previous = self.scene_name
            self.scene_previous = previous
            self.scene_name = self.scene.next
            self.set_scene(self.scene_name)
        self.scene.update(self.surface, self.keys, tick)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.keys = pygame.key.get_pressed()
            elif event.type == pygame.KEYUP:
                self.keys = pygame.key.get_pressed()
            self.scene.get_event(event)
        
    def set_scene(self,scene_name):
        if scene_name != None:
            self.scene_name = scene_name
            scene_imp = import_module("scenes." + scene_name)
            scene = getattr(scene_imp, self.scene_class_names[scene_name])
            self.scene = scene()
        else:
            raise Exception("No scene provided")

    def mainloop(self):
        while not self.finished:
            self.event_loop()
            self.update(self.clock.tick(self.fps))
            self.screen.blit(self.surface, (0,0))
            pygame.display.update()

