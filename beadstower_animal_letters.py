import beadstower_animal as BB
from tkinter import PhotoImage, NW, CURRENT

class AnimalLetters(BB.AnimalBeads):
    def __init__(self, master=None):
        BB.AnimalBeads.__init__(self)
        self.add_letters()

    def add_letters(self):
        base_chrd = 97 # a
        for item in self.images:
            IMID = self.imageID[item]
            self.imageID[item] = [IMID, chr(base_chrd)]
            base_chrd += 1

    def bindkeys_game(self):
        self.root.bind('<Key>', self.turn)

    def turn(self, event):
        x0 = self.x0_pole - 25
        tag = ['all', 'user']
        currentID = self.beads_solution[0]
        currentTags = self.canvas.gettags(currentID)
        image = currentTags[2]
        currentLetter = self.imageID[currentTags[2]][1]
        if event.char == currentLetter:
            self.beads_user.append(self.canvas.create_image(x0, self.solY0, anchor=NW, image=self.imageID[image][0], tags=tag+[image]))
            self.solY0 -= 50
            item = self.beads_solution.pop(0)
            self.beads_solution_done.append(item)
        if len(self.beads_solution) == 0:
            self.canvas.itemconfigure(self.textID, text='You Won!')
            self.canvas.update()
            self.root.after(3000, self.draw_game_extra)

if __name__ == '__main__':
    game = AnimalLetters()
    game.root.mainloop()
