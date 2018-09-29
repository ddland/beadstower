from tkinter import Tk, Canvas, Frame, BOTH, CURRENT, YES
import random

class MainWindow():
    def __init__(self, master=None):
        super().__init__()
        self.root = Tk()
        self.root.title('Beads Tower')
        self.w, self.h =  500,800
        self.canvas = Canvas(self.root, width=self.w, height=self.h, background='white')
        self.canvas.pack(fill=BOTH, expand=YES)

        self.fullscreen = False
        
        self.bindkeys_screen()
        self.bindkeys_game()
        self.config()
        
        self.initialize()
        self.draw_background()
        self.draw_game()

    def config(self):
        self.Nbeads = 5 # 5 beads
        self.colors = ('red', 'blue', 'yellow', 'orange', 'purple', 'sky blue', 'hot pink', 'black', 'chartreuse', 'forest green', 'white', 'orchid')
        self.Ncolors = len(self.colors)
        self.beadsize = int(0.3*0.9*self.h/self.Nbeads) #diameter or cross section of beads
        self.beads_available = []
        self.beads_solution = []
        self.beads_user = []
        self.beads_solution_done = []
        self.ws = int(1.1*self.beadsize)
        self.trytext = 'Tries: %d'
        self.tryout = 0
        self.polewidth = 5

    def initialize(self):
        self.yoffset = int(0.05*self.h)
        self.solY0 = self.h-self.yoffset
        self.solY1 = self.h-self.yoffset-self.beadsize


    def draw_background(self):
        self.draw_pole()
        self.draw_beads()
        self.textID = self.canvas.create_text(350,40, text=self.trytext%(self.tryout), tags=['all'])

    def draw_game(self):
        for item in self.beads_solution:
            self.canvas.delete(item)
        for item in self.beads_user:
            self.canvas.delete(item)
        for item in self.beads_solution_done:
            self.canvas.delete(item)
        self.tryout = 0
        self.beads_solution = []
        self.beads_user = []
        self.beads_solution_done = []
        self.initialize()
        self.canvas.itemconfigure(self.textID, text=self.trytext%(self.tryout))
        self.draw_solution()
        
    def draw_pole(self):
        # pole for the bead
        # at 1/3 of width, 90% height
        tags = ['all', 'tower']
        self.x0_pole = int(0.3*self.w)
        self.canvas.create_rectangle(self.x0_pole-self.polewidth, self.yoffset, self.x0_pole+self.polewidth, self.h-self.yoffset, fill='brown', tags=tags)
        self.canvas.create_rectangle(self.x0_pole-6*self.polewidth, self.h-self.yoffset, self.x0_pole+6*self.polewidth, self.h-self.yoffset+6*self.polewidth, fill='brown', tags=tags)

    def draw_beads(self):
        tags = ['all', 'available']
        x0 = self.x0_pole + int(0.3*self.w)
        x1 = x0 + self.beadsize
        y0org = self.h - self.yoffset
        y1org = y0org - self.beadsize
        
        y0 = y0org
        y1 = y1org
        for i in range(self.Ncolors):
            tag = tags + ['square']
            self.beads_available.append(self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.colors[i], tags=tag))
            y0 -= self.ws
            y1 -= self.ws
        x0 += self.ws
        x1 += self.ws
        y0 = y0org
        y1 = y1org
        for i in range(self.Ncolors):
            tag = tags + ['circle']
            self.beads_available.append(self.canvas.create_oval(x0, y0, x1, y1, fill=self.colors[i], tags=tag))
            y0 -= self.ws
            y1 -= self.ws

    def draw_solution(self):
        tags = ['all', 'solution']
        x0 = self.x0_pole - int(0.2*self.w)
        x1 = x0 + self.beadsize
        y0 = self.h - self.yoffset
        y1 = y0 - self.beadsize
        ws = int(1.1*self.beadsize)
        NbeadsAvailable = len(self.beads_available)
        for item in range(self.Nbeads):
            itemid = self.beads_available[int(random.random()*NbeadsAvailable)]
            color = self.canvas.itemcget(itemid, 'fill')
            alltags = self.canvas.gettags(itemid)
            if 'square' in alltags:
                tag = tags + ['square']
                self.beads_solution.append(self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags=tag))
            elif 'circle' in alltags:
                tag = tags + ['circle']
                self.beads_solution.append(self.canvas.create_oval(x0, y0, x1, y1, fill=color, tags=tag))
            y0 -= self.ws
            y1 -= self.ws


    def turn(self, event):
        tag = ['all', 'user']
        x0 = self.x0_pole - int(0.5*self.beadsize)
        x1 = self.x0_pole + int(0.5*self.beadsize)
        if self.canvas.find_withtag(CURRENT):
            alltags = self.canvas.gettags(CURRENT)
            self.tryout += 1
            self.canvas.itemconfigure(self.textID, text=self.trytext%(self.tryout))
            if 'available' in alltags:
                color = self.canvas.itemcget(CURRENT, 'fill')
                shape = alltags[2] # shape location in tags
                currentID = self.beads_solution[0]
                currentTags = self.canvas.gettags(currentID)
                currentColor = self.canvas.itemcget(currentID, 'fill')
                currentShape = currentTags[2] # shape location in tags
                if (shape == currentShape) and (color == currentColor):
                    if 'square' == shape:
                        self.beads_user.append(self.canvas.create_rectangle(x0, self.solY0, x1, self.solY1, fill=color, tags=tag))
                    elif 'circle' == shape:
                        self.beads_user.append(self.canvas.create_oval(x0, self.solY0, x1, self.solY1, fill=color, tags=tag))
                    self.solY0 -= self.ws
                    self.solY1 -= self.ws
                    item = self.beads_solution.pop(0)
                    self.beads_solution_done.append(item)
                    if len(self.beads_solution) == 0:
                        self.canvas.itemconfigure(self.textID, text='You Won!')
                        self.canvas.update()
                        self.root.after(3000, self.draw_game)


    def resize(self, event):
        wscale = float(event.width)/self.w
        hscale = float(event.height)/self.h
        self.w, self.h = event.width, event.height
        self.root.config(width=self.w, height=self.h)
        self.canvas.scale('all',0,0,wscale, hscale)

    def setsize(self):
        wscale = float(self.root.winfo_width())/self.w
        hscale = float(self.root.winfo_height())/self.h
        self.w, self.h = self.root.winfo_width(), self.root.winfo_height()
        self.canvas.scale('all',0,0,wscale, hscale)

    def bindkeys_game(self):
        self.root.bind('<Button-1>', self.turn)

    def bindkeys_screen(self):
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.end_fullscreen)
        self.root.bind('<Configure>', self.resize)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
        self.setsize()

    def end_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes('-fullscreen', self.fullscreen)
        self.setsize()


class OtherColor(MainWindow):
    def __init__(self, master=None):
        MainWindow.__init__(self)

    def config(self):
        self.Nbeads = 100



if __name__ == '__main__':
    game = MainWindow()
    #game = OtherColor()
    game.root.mainloop()
