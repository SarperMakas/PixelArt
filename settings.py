"""Settings"""
import tkinter as tk
from tkinter import messagebox


class Settings:
    """Settings class"""
    def __init__(self, w, h):
        # width, height
        self.WIDTH = w
        self.HEIGHT = h
        # root, geometry, title
        self.root = tk.Tk()
        self.root.title("Pixel Art - Settings")
        self.root.geometry("300x80")
        # fonts
        self.fontSize, self.fontBg, self.fontFg, self.font = 13, "#a0a0a0", "#ffffff", "04B_19"
        self.root.config(bg=self.fontBg)
        # labels
        self.size = tk.Label(self.root, text="SIZE: ", height=2, width=16, bg=self.fontBg, font=(self.font, self.fontSize),
                             fg=self.fontFg)
        # texts
        self.sizeText = tk.Text(self.root, height=2, width=16)
        # buttons
        self.button = tk.Button(self.root, text="SUBMIT", height=2, width=30, bg=self.fontBg, font=(self.font, self.fontSize),
                                fg=self.fontFg, command=self.check)
        # redefine
        self.redefine = False
        # value
        self.value = None

    def check(self):
        """check text buttons"""
        value = tk.messagebox.askyesnocancel("Pixel Art", "Your work would be unsaved\nDo you want to change canvas?")
        if self.sizeText.get(0.0, tk.END) and value == 1:
            try:
                # row, col number and size
                size = int(self.sizeText.get(0.0, tk.END))
                row = self.HEIGHT // int(self.sizeText.get(0.0, tk.END))
                col = self.WIDTH // int(self.sizeText.get(0.0, tk.END))
                self.redefine = False
                self.value = [size, row, col]
                self.root.destroy()
            except ValueError:
                messagebox.showinfo("Error", "Size should be int")
        self.root.destroy()
        del self.root
        del tk.Tk

    def draw(self):
        """draw"""
        self.redefine = True
        # put vars in to the screen
        self.size.grid(row=0, column=0, sticky=tk.W)
        self.sizeText.grid(row=0, column=1, sticky=tk.W)
        self.button.grid(row=2, column=0, columnspan=2)

    def run(self):
        """run settings"""
        self.draw()
        self.root.resizable(False, False)
        self.root.mainloop()

