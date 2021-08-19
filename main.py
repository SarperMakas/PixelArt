"""Main file of Pixel Art App"""
import pygame, ctypes, numpy as np
from colors import ColorChooser
from canvas import Canvas
from settings import Settings
from tkinter import filedialog
from PIL import Image


class Main:
    """Main class of the app"""
    def __init__(self):
        # defining width, height, screen
        self.WIDTH = ctypes.windll.user32.GetSystemMetrics(0)-36
        self.HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)-60
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # running var for checking if we need to run and clock for timing
        self.running = True
        self.clock = pygame.time.Clock()
        # color chooser class, canvas, settings
        self.color = ColorChooser(self.WIDTH, self.HEIGHT, self.screen)
        self.canvas = Canvas(self.WIDTH, self.HEIGHT, self.screen)
        self.sets = Settings(self.WIDTH, self.HEIGHT)

        # font
        self.font = pygame.font.Font("04B_19.ttf", 12)
        # text
        self.settings = self.font.render("SETTINGS", True, (255, 255, 255))
        self.settingsBgRect = pygame.Rect((12, 610), (108, 15))
        self.settingsRect = self.settings.get_rect(center=self.settingsBgRect.center)

        # save button
        self.save = self.font.render("SAVE", True, (255, 255, 255))
        self.saveBgRect = pygame.Rect((12, 634), (108, 15))
        self.saveRect = self.save.get_rect(center=self.saveBgRect.center)

    def checkClick(self):
        """check if the user click to the settings"""
        # positions and rect dict
        x, y = pygame.mouse.get_pos()
        rectDict = {0: self.settingsBgRect, 1: self.saveBgRect}
        # for loop
        for num in range(2):
            rect = rectDict[num]
            # check clicks
            if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                if rect == self.settingsBgRect and num == 0:
                    self.sets.run()
                elif rect == self.saveBgRect and num == 1:
                    self.savePixels()

    def checkAlpha(self):
        """change alpha value of s"""
        x, y = pygame.mouse.get_pos()
        # dicts for rect and text
        rectDict = {0: self.settingsBgRect, 1: self.saveBgRect}
        textDict = {0: self.settings, 1: self.save}
        # for loop
        for num in range(2):
            rect = rectDict[num]
            text = textDict[num]
            # change alpha values
            if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                text.set_alpha(155)
            else:
                text.set_alpha(255)

    def savePixels(self):
        """saving canvas"""
        # change root
        self.sets.root.geometry("20x20")
        self.sets.root.attributes("-topmost", True)
        self.sets.root.withdraw()
        # save file
        file = filedialog.asksaveasfilename(initialdir="C:\\Users\\%USERNAME%\\Desktop",
                                            defaultextension=".txt",
                                            filetypes=[
                                                ("PNG file", ".png")])
        try:
            self.sets.root.destroy()
        except:
            pass
        if file != "":
            self.sets = Settings(self.WIDTH, self.HEIGHT)
            # save
            img = Image.fromarray(self.canvas.array, 'RGB')
            img.save(f'{file}')
            img = pygame.transform.scale2x(pygame.image.load(f"{file}"))
            pygame.image.save(img, file)
            

        
    def drawMenu(self):
        """drawing settings button"""
        # draw rects and buttons
        pygame.draw.rect(self.screen, (150, 150, 150), self.settingsBgRect)
        self.screen.blit(self.settings, self.settingsRect)
        pygame.draw.rect(self.screen, (150, 150, 150), self.saveBgRect)
        self.screen.blit(self.save, self.saveRect)

    def check(self):
        """check"""
        # change settings
        if self.sets.value is not None:
            self.canvas.sqSize = self.sets.value[0]
            self.canvas.reArray(self.sets.value[0], self.sets.value[1], self.sets.value[2])
            self.sets.value = None
            self.sets = Settings(self.WIDTH, self.HEIGHT)
        # redefine sets
        if self.sets.redefine is True:
            self.sets = Settings(self.WIDTH, self.HEIGHT)

    def event(self):
        """Event loop and checks for event"""
        for event in pygame.event.get():
            # check exit game
            if event.type == pygame.QUIT:
                self.running = False
            # check mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.color.findColor()
                self.color.changeAlpha("press")
                self.checkClick()
            # check mouse motions
            if event.type == pygame.MOUSEMOTION:
                self.color.findColor("motion")
                self.checkAlpha()

            if pygame.mouse.get_pressed(3)[0] is True:
                self.canvas.pixel(self.color.color)

    def draw(self):
        """Drawing screen"""
        self.screen.fill((0, 0, 0))
        self.color.drawColors()
        self.canvas.draw()
        self.drawMenu()
        pygame.display.flip()

    def main(self):
        """main function of the Main class"""
        while self.running:
            self.clock.tick(80)
            self.event()
            self.check()
            self.draw()


if __name__ == '__main__':
    Main().main()
