from tkinter import Tk, Canvas, Frame, BOTH, CURRENT
import random

class Beads(Frame):
    
    def __init__(self, master=None):
        super().__init__()
        self.init_window()
        
        self.pole_coords= (195, 900, 205, 10)  #top left, bottom right (x0, y0, x1, y1)
        self.rect_w = 10
        self.rect_h = 10
        self.N = 5
        self.beads_available = []
        self.beads_solution = []
        self.beads_user = []
        self.beads_solution_done = []
        self.draw_pole()
        self.init_beads()
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
    
    def init_beads(self):
        colors = ('red', 'blue', 'yellow', 'orange', 'purple', 'sky blue', 'hot pink', 'black', 'chartreuse', 'forest green')
        x0 = 300
        x1 = 370
        y0 = 800
        y1 = 870
        N = len(colors)
        tags = ('available',)
        for i in range(N):
            self.beads_available.append(self.draw_bead_square((x0, y0, x1,y1), colors[i], tags))
            y0 -= 75
            y1 -= 75
        x0 +=75
        x1 += 75
        y0 = 800
        y1 = 870
        for i in range(N):
            self.beads_available.append(self.draw_bead_circle((x0, y0, x1,y1), colors[i], tags))
            y0 -= 75
            y1 -= 75
        x0 +=75
        x1 += 75
        y0 = 800
        y1 = 870
        for i in range(N):
            self.beads_available.append(self.draw_bead_oval((x0+10, y0, x1-10,y1), colors[i], tags))
            y0 -= 75
            y1 -= 75

    def start(self):
        print(self.beads_solution, self.beads_user)
        for item in self.beads_solution:
            print(item)
            self.canvas.delete(item)
        for item in self.beads_user:
            print(item)
            self.canvas.delete(item)
        for item in self.beads_solution_done:
            print(item)
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
        Nitems = len(self.beads_available)
        for item in range(N):
            itemid = self.beads_available[int(random.random()*Nitems)]
            color=self.canvas.itemcget(itemid, 'fill')
            shape=self.canvas.gettags(itemid)
            if shape[0] == 'square':
                self.beads_solution.append(self.draw_bead_square((x0, y0, x1,y1), color))
            if shape[0] == 'circle':
                self.beads_solution.append(self.draw_bead_circle((x0, y0, x1,y1), color))
            if shape[0] == 'oval':
                self.beads_solution.append(self.draw_bead_oval((x0+10, y0, x1-10,y1), color))
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
                    print('match')
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
