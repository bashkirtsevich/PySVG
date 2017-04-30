#!/usr/bin/env python
"""The positioning in this system is not relative to pixels but to a base unit.
The Camera class takes care of rendering objects in their proper position.
"""
import os, glob
import pygame



#HIGHEST LEVEL
class GameApp:
    """The smartest thing to do would be to inherit from it and override
    the init, update, and draw functions.
    """
    def __init__(self):
        #Display
        self.displaySize = 1024, 768
        self.display = pygame.display.set_mode(self.displaySize)
        
        #Peripherals
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        
        #Other objects
        self.clock = pygame.time.Clock()
        
        #Groups
        self.updateInstances = []
        self.drawInstances = []
        
        #Resources
        self.resources = loadResources()
        
        #Data
        self.fpsStandard = 60
        self.loopFlag = True
        
        self.init() #Start the personalized init
    
    def init(self):
        pass
    
    def beforeUpdate(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.loopFlag = False
        
        self.keyboard.update(self.events)
        self.mouse.update()
    
    def update(self):
        pass
    
    def draw(self):
        pass
    
    def afterUpdate(self):
        pygame.display.flip()
        self.clock.tick(self.fpsStandard) #Keep framerate stable
    
    def startLoop(self):
        while self.loopFlag:
            self.beforeUpdate()
            self.update()
            self.draw()
            self.afterUpdate()

#HIGH LEVEL
class Camera:
    """A camera class, which follows a subject(must have x, y coordinates).
    Using its draw function will draw all objects in its root application's
    drawInstances list at the proper coordinates.
    In short, don't draw() single objects, draw() cameras.
    
    """
    def __init__(self, root, subject, fix=1.0, zoom=16.0):
        self.root = root #GameApp instance
        self.subject = subject #Instance with x and y values
        self.fix = fix #0<x<1, ratio of movement to subject
        self.zoom = zoom #amount of pixels per base unit e.g: 16
        
        pos = self.x, self.y = subject.x, subject.y
        size = self.root.displaySize[0] / self.zoom, self.root.displaySize[1] / self.zoom
        
        self.rect = pygame.Rect(pos, size)
        
    def update(self):
        self.x = self.subject.x*(self.fix) + self.x*(1-self.fix)
        self.y = self.subject.y*(self.fix) + self.y*(1-self.fix)
        self.rect.center = self.x, self.y
        
    def draw(self):
        for obj in self.root.drawInstances:
            if self.rect.collidepoint(obj.x, obj.y):
                x = self.rect.centerx - self.x*self.zoom + obj.x*self.zoom
                y = self.rect.centery - self.y*self.zoom + obj.y*self.zoom
                obj.draw((int(x), int(y)))

#RESOURCE LEVEL
def loadResources():
    """Will properly load .png and .ogg files
    producing a 'filename':pygameobject dictionary
    """
    workingDirectory = os.path.split(__file__)[0] + "/"
    
    images = []
    sounds = []
    
    subDirsToExplore = 3
    actualDir = ""
    for i in range(subDirsToExplore):
        actualDir = actualDir + "*/"
        
        for image in glob.glob(workingDirectory + actualDir + '*.png'):
            images.append(image)
        for sound in glob.glob(workingDirectory + actualDir + '*.ogg'):
            sounds.append(sound)
    
    resources = {}
    
    for image in images:
        imageName = os.path.split(image)[1]
        resources[imageName] = loadImage(image)
    for sound in sounds:
        soundName = os.path.split(sound)[1]
        resources[soundName] = loadSound(sound)
    
    return resources

def loadImage(path):
    """Return surface from full image path
    """
    try:
        image = pygame.image.load(path)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', path
        raise SystemExit, message
    return image, image.get_rect()

def loadSound(path):
    return None

#WRAPPING LEVEL
class Keyboard:
    """There should be a single instance of this class.
    Update it every frame, feeding it all events from pygame.event.get()
    """
    def __init__(self):
        self.pressed = [[], [], []] #Keyboard status
    def update(self, events):
        self.pressed.insert(1, [])
        for k in self.pressed[0]: self.pressed[1].append(k)
        if len(self.pressed) > 3: self.pressed.pop()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.pressed[0].append(event.key)
            elif event.type == pygame.KEYUP:
                try: self.pressed[0].remove(event.key)
                except ValueError: pass
    def check(self, key):
        """Checks if a key is pressed, returns bool"""
        for pressed in self.pressed[0]:
            if key == pressed:
                return True
        return False
    def checkPrev(self, key):
        """Checks if a key was pressed, returns bool"""
        for pressed in self.pressed[1]:
            if key == pressed:
                return True
        return False
    def checkPressed(self, key):
        """Checks if a key has just been pressed, returns bool"""
        if self.check(key) and not self.checkPrev(key):
            return True
        return False
    def checkReleased(self, key):
        """Checks if a key has just been released, returns bool"""
        if not self.check(key) and self.checkPrev(key):
            return True
        return False

class Mouse:
    """One more self-explicative singleton. Update each frame!
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.xPrev = 0
        self.yPrev = 0
        self.pressed = [0,0,0]
        self.pressedPrev = [0,0,0]
    def update(self):
        self.xPrev, self.yPrev = self.x, self.y
        self.pressedPrev = self.pressed
        
        self.x, self.y = pygame.mouse.get_pos()
        self.pressed = pygame.mouse.get_pressed()
