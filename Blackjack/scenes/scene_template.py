class Scene(object):

    name = "Scene"

    def __init__(self):
        self.next = None
        self.quit = False 
        self.finished = False 

    def get_event(self, event):
        # manage events that the controller passes down 
        # Template, write in child.
        pass

    def update(self, surface, keys, time, tick):
        # updates for the current scene, called each frame and is responsible
        # for updates to the display, write in child.
        pass                

    def draw(self, surface):
        # perform the actual drawing of the updates, wriite in child. 
        pass