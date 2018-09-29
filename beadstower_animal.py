import beadstower_base as BB
from tkinter import PhotoImage, NW, CURRENT
import random

class AnimalBeads(BB.MainWindow):
    def __init__(self, master=None):
        BB.MainWindow.__init__(self)
        self.extra_config()

    def extra_config(self):
        self.solY0 = self.h - self.yoffset - 50


    def draw_game_extra(self):
        self.draw_game()
        self.extra_config()

    def draw_background(self):
        self.load_image()
        self.draw_pole()
        self.draw_beads()
        self.textID = self.canvas.create_text(350,40, text=self.trytext%(self.tryout), tags=['all'])       


    def load_image(self):
        self.images = ['Bear', 'Beaver', 'Fish', 'Insect'] # sorted a-z for keypress
        self.imageID = {}
        x0 = 20
        y0 = 700
        for item in self.images:
            IMID = PhotoImage(file='images/'+item+'.gif')
            self.imageID[item] = [IMID,]
            y0 -=50
        self.Nimages = len(self.images)
    
    def draw_beads(self):
        tag = ['all', 'available', 'image']
        x0 = self.x0_pole + int(0.3*self.w)
        y0org = self.h - self.yoffset - 50
        y0 = y0org
        for i in self.imageID.keys():
            self.beads_available.append(self.canvas.create_image(x0, y0, anchor=NW, image=self.imageID[i][0], tags=tag+[i]))
            y0 -= 50

    def draw_solution(self):
        tag = ['all', 'solution']
        x0 = self.x0_pole - int(0.2*self.w)
        y0 = self.h - self.yoffset - 50
        keys = list(self.imageID.keys())
        for item in range(self.Nbeads):
            key = keys[int(random.random()*len(keys))]
            self.beads_solution.append(self.canvas.create_image(x0, y0, anchor=NW, image=self.imageID[key][0], tags=tag+[key]))
            y0 -= 50

    def turn(self, event):
        tag = ['all', 'user']
        x0 = self.x0_pole - 25
        if self.canvas.find_withtag(CURRENT):
            self.tryout += 1
            self.canvas.itemconfigure(self.textID, text=self.trytext%(self.tryout))
            alltags = self.canvas.gettags(CURRENT)
            image = alltags[3]
            currentID = self.beads_solution[0]
            currentTags = self.canvas.gettags(currentID)

            if 'available' in alltags:
                if image == currentTags[2]:
                    self.beads_user.append(self.canvas.create_image(x0, self.solY0, anchor=NW, image=self.imageID[image][0], tags=tag+[image]))
                    self.solY0 -= 50
                    item = self.beads_solution.pop(0)
                    self.beads_solution_done.append(item)
                    if len(self.beads_solution) == 0:
                        self.canvas.itemconfigure(self.textID, text='You Won!')
                        self.canvas.update()
                        self.root.after(3000, self.draw_game_extra)




if __name__ == '__main__':
    game = AnimalBeads()
    game.root.mainloop()

