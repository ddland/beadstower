from tkinter import Tk, Canvas, Frame, BOTH, CURRENT
import random


colors = ('red', 'blue', 'yellow', 'orange', 'purple', 'sky blue', 'hot pink', 'black', 'chartreuse', 'forest green', 'white', 'orchid')
keys = {1:'a',
        2:'b',
        3:'c',
        4:'d',
        5:'e',
        6:'f',
        7:'g',
        8:'h',
        9:'i',
        10:'j',
        11:'k',
        12:'l',
        }


class Beads(Frame):
    
    def __init__(self, master=None):
        super().__init__()
        self.init_window()
        
        self.pole_coords= (195, 900, 205, 10)  #top left, bottom right (x0, y0, x1, y1)
        self.rect_w = 10
        self.rect_h = 10
        self.N = 5
        self.beads_solution = []
        self.beads_user = []
        self.beads_solution_done = []
        self.draw_pole()
        self.start()

    def init_window(self):
        self.master.title('Kralen stapel')
        self.pack(fill=BOTH, expand=1)
        
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)
        self.poging = 0
        self.pogingtxt = 'aantal pogingen %d'
        
        self.textID = self.canvas.create_text(350,40, text=self.pogingtxt%(self.poging))
    
        self.canvas.bind("<Button-1>", self.click)
        self.master.bind("<Key>", self.keypress)


    def keypress(self, event):
        if event.char == self.beads_solution[0]:
            item = self.beads_solution.pop(0)
            self.canvas.create_text(self.solX0, self.solY0, font=('Helvetica', '44'), text=item)
            self.beads_solution_done.append(item)
            self.solY0 -= 75

        print(dir(event))
        print(event.keycode, event.char)
    
    def start(self):
        for item in self.beads_solution:
            self.canvas.delete(item)
        for item in self.beads_user:
            self.canvas.delete(item)
        for item in self.beads_solution_done:
            self.canvas.delete(item)
        self.solX0 = 165
        self.solX1 = 235
        self.solY0 = 800
        self.solY1 = 870
        
        self.poging = 0
        self.canvas.itemconfigure(self.textID, text=self.pogingtxt%(self.poging))
        self.beads_solution=[]
        self.beads_solution_done=[]
        self.beads_user = []
        self.draw_solution(self.N)
        
    def draw_solution(self, N):
        x0 = 50
        x1 = 120
        y0 = 800
        y1 = 870
        Nitems = len(keys)
        for item in range(1,N+1):
            self.canvas.create_text(x0, y0, font=('Helvetica', '44'),text=keys[item])
            self.beads_solution.append(keys[item])
            y0 -= 75
            y1 -= 75


    def draw_pole(self):
        self.pole_id = self.canvas.create_rectangle(*self.pole_coords,fill='brown')
        self.pole_base_id = self.canvas.create_rectangle(150, 950, 250, 875, fill='brown') 

    def draw_bead_square(self, coords, color, tags=()):
        return self.canvas.create_rectangle(*coords, fill=color, tags=('square',*tags))

    def draw_bead_circle(self, coords, color, tags=()):
        return self.canvas.create_oval(*coords, fill=color, tags=('circle',*tags))
    
    def draw_bead_oval(self, coords, color,tags=()):
        return self.canvas.create_oval(*coords, fill=color, tags=('oval',*tags))


    def click(self, event):
        tags = ('sol',)
        if self.canvas.find_withtag(CURRENT):
            if 'available' in self.canvas.gettags(CURRENT):
                shape = self.canvas.gettags(CURRENT)[0]
                color = self.canvas.itemcget(CURRENT, 'fill')
                curID = self.beads_solution[0]
                shapeID = self.canvas.gettags(curID)[0]
                colorID = self.canvas.itemcget(curID, 'fill')
                if (shapeID == shape) and (color == colorID):
                    if shape == 'square':
                        self.beads_user.append(self.draw_bead_square((self.solX0, self.solY0, self.solX1,self.solY1), color, tags))
                    if shape == 'circle':
                        self.beads_user.append(self.draw_bead_circle((self.solX0, self.solY0, self.solX1,self.solY1), color, tags))
                    if shape == 'oval':
                        self.beads_user.append(self.draw_bead_oval((self.solX0+10, self.solY0, self.solX1-10,self.solY1), color, tags))
                    self.solY0 -= 75
                    self.solY1 -= 75

                    item = self.beads_solution.pop(0)
                    self.beads_solution_done.append(item)
                    if len(self.beads_solution) == 0:
                        self.canvas.itemconfigure(self.textID, text='Gewonnen!')
                        self.canvas.update()
                        self.after(3000, self.start())
                else:
                    self.poging +=1
                    self.canvas.itemconfigure(self.textID, text=self.pogingtxt%(self.poging))

    def place_bead(self):
        pass

    def correct_bead(self):
        pass

if __name__ == '__main__':
    root = Tk()
    app = Beads(root)
    root.geometry("800x1000")
    root.mainloop()
