"""Color chooser part"""
import pygame, tkinter as tk
from tkinter import colorchooser
pygame.init()


class ColorChooser:
    """color chooser class of the game"""
    def __init__(self, W, H, screen):
        # defining width, height, screen
        self.WIDTH = W
        self.HEIGHT = H
        self.screen = screen
        # rect for color chooser part
        self.settingsBg = pygame.Rect((0, 0), (141, self.HEIGHT))
        self.colorPalletRect = pygame.Rect((12, 562), (108, 15))
        self.chosenColorRect = pygame.Rect((12, 586), (108, 15))

        # font
        self.font = pygame.font.Font("04B_19.ttf", 12)
        # text, rect for text
        self.pallet = self.font.render("COLOR  PALLET", True, (255, 255, 255))
        self.palletRect = self.pallet.get_rect(center=self.colorPalletRect.center)
        # ------------------------------------------------------------------------------------------------------------#
        self.chosen = self.font.render("NONE", True, (255, 255, 255))
        self.chosenRect = self.chosen.get_rect(center=self.chosenColorRect.center)

        # list of colors
        self.colorList = self.makeColors()
        # past colors
        self.pastColors = [[(255, 255, 255), False] for _ in range(9)]
        self.colorList += self.pastColors
        # row and cols
        self.col = 9
        self.row = len(self.colorList)//self.col
        # width and height of the color rects
        self.sqSize = 12
        # top vars
        self.x = [self.sqSize, self.sqSize*(self.col+1)]
        self.y = [self.sqSize, self.sqSize*(self.row+1)]

        # color
        self.color = [255, 255, 255]


    def makeColors(self, r=255, g=255, b=255):
        """Making Colors"""
        # row => y, col => x
        # row => y, col => x
        colorNum = 1
        color = [r, g, b]
        colorDict = {1: (color[0], color[1], color[2]),
                     2: (color[2], color[0], color[1]),
                     3: (color[1], color[2], color[0]),
                     4: (color[2], color[1], color[0]),
                     5: (color[0], color[2], color[1]),
                     6: (color[2], color[1], color[0])}
        colorList = []

        # use row and col
        for row in range(1, 55):
            for col in range(1, 8):
                colorList.append(colorDict[colorNum])

                # decrease color
                if color[0] > 5:
                    color[0] -= 5
                elif color[1] > 5:
                    color[1] -= 5
                elif color[2] > 5:
                    color[2] -= 5
                # redefine colorDict
                colorDict = {1: (color[0], color[1], color[2]),
                             2: (color[2], color[0], color[1]),
                             3: (color[1], color[2], color[0]),
                             4: (color[2], color[1], color[0]),
                             5: (color[0], color[2], color[1]),
                             6: (color[2], color[1], color[0])}

                # change colorNum and delete some colors append another colors
                if color[0] == 5 and color[1] == 5 and color[1] == 5:
                    for i in range(colorNum):
                        del colorList[-100-i]
                        colorList.insert(-99-i, (257 - colorNum * 2, 257 - colorNum * 2, 257 - colorNum * 2))
                    colorNum += 1
                    color = [r, g, b]
        for i in range(colorNum):
            del colorList[-78 - i]
            colorList.insert(-77 - i, (256 - colorNum * 2, 256 - colorNum, 256 - colorNum))
        return self.appendColors(colorList)

    @staticmethod
    def appendColors(colors):
        """append new colors"""
        # deleting some colors
        del colors[-1], colors[-2]

        # add 2 new row
        # use dict for less line
        translate = {0: (255, 120, 55, 0), 1: (90, 90, 90, 2)}
        for i in range(2):
            # define r, g, b, minus var
            r, g, b, minus = translate[i]
            # append new colors
            for _ in range(11-minus):
                r -= 5
                g -= 5
                b -= 5
                colors.append((r, g, b))

        newList = []
        # change newList
        for color in colors:
            newList.append([color, True])
        return newList

    def findColor(self, value="press"):
        """finding chosen color"""
        # startPos => 12, 12    endPos => 120, 552
        # row => y, col => x
        x, y = pygame.mouse.get_pos()
        if self.x[0] <= x <= self.x[1] and self.y[0] <= y <= self.y[1]:
            # getting col and rows
            col = x // self.sqSize
            row = y // self.sqSize
            # getting index
            index = (row - 1) * self.col + col - 1
            # put the color that we choose to the past colors
            if value == "press":
                self.addColors(index)
            elif value == "motion":
                self.chosen = self.font.render(f"{self.colorList[index][0]}", True, self.colorList[index][0])
                self.chosenRect = self.chosen.get_rect(center=self.chosenColorRect.center)


    def addColors(self, index):
        """adding colors to the past colors"""
        # counter var
        counter = 0
        # change color for the first time
        for num, color in enumerate(self.pastColors):
            if color[1] is False:
                self.pastColors[num] = [self.colorList[index][0], True]
                break
            else:
                counter += 1

        # add to the colors
        if counter == 9:
            # check if there is True in the index list
            newList = [[self.colorList[index][0], True]]
            # change pas colors
            newList += self.pastColors[:8]
            self.pastColors = newList
        self.color = self.colorList[index][0]
        # redefine colorLists some elements
        self.colorList[396:] = self.pastColors

    def colorChooser(self):
        """color chooser"""
        # define root and color chose
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        color = colorchooser.askcolor()[1]
        # destroy root
        try:
            root.destroy()
        except:
            pass
        # convert hex to rgb
        if color:
            color = tuple(int(color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
            # check if there is True in the index list
            newList = [[color, True]]
            # change pas colors
            newList += self.pastColors[:8]
            self.pastColors = newList
            # redefine colorLists some elements
            self.colorList[396:] = self.pastColors
            # change color
            self.color = color

    def changeAlpha(self, value="motion"):
        """changing alpha value of the buttons"""
        x, y = pygame.mouse.get_pos()
        if self.colorPalletRect.left <= x <= self.colorPalletRect.right and self.colorPalletRect.top <= y <= self.colorPalletRect.bottom:
            self.pallet.set_alpha(155)
            if value == "press":
                self.colorChooser()
        else:
            self.pallet.set_alpha(255)

    def drawColors(self):
        """Drawing colors"""
        # row => y, col => x
        # startPos => 12, 12    endPos => 120, 552
        # drawing rects
        pygame.draw.rect(self.screen, (55, 55, 55), self.settingsBg)
        pygame.draw.rect(self.screen, (150, 150, 150), self.colorPalletRect)
        pygame.draw.rect(self.screen, (150, 150, 150), self.chosenColorRect)
        element = 0
        # use for loop for drawing
        for row in range(1, self.row + 1):
            for col in range(1, self.col + 1):
                # define colorRect and draw it
                colorRect = pygame.Rect((col * self.sqSize, row * self.sqSize), (self.sqSize, self.sqSize))
                pygame.draw.rect(self.screen, self.colorList[element][0], colorRect)

                element += 1
        # use for loop, rows and columns for position.
        for row in range(1, self.row + 2):
            for col in range(1, self.col + 2):
                # draw lines
                # | line
                pygame.draw.line(self.screen, (200, 200, 200), (col * self.sqSize, self.y[0]), (col * self.sqSize, self.y[1]))
                # - line
                pygame.draw.line(self.screen, (200, 200, 200), (self.x[0], row*self.sqSize), (self.x[1], row*self.sqSize))
        # drawing texts
        self.screen.blit(self.pallet, self.palletRect)
        self.screen.blit(self.chosen, self.chosenRect)
        # check alpha values
        self.changeAlpha()
