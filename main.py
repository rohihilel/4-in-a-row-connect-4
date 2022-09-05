#roee hilel, 328487657

from tkinter import *
import setup
import save_load



#the gui
class GUI:
    elementSize = 50
    gridBorder = 3
    gridColor = "#AAA"
    p1Color = "#4096EE"
    p2Color = "#FF1A00"
    backgroundColor = "#FFFFFF"
    gameOn = False

    def __init__(self, master):
        self.master = master

        master.title('Connect Four')
        label1 = Label(master, text="Four In A Row!!!")
        label1.grid(row=0, column=0)
        button1 = Button(master, text="New Game!", command=self._newGameButton)
        button1.grid(row=1, column=0)

        label2 = Label(master, text="Four In A Row!!!")
        label2.grid(row=0, column=1, columnspan=2)
        button2 = Button(master, text="Save!", command=self._save)
        button2.grid(row=1, column=1)
        button3 = Button(master, text="Load!", command=self._load)
        button3.grid(row=1, column=2)



        self.canvas = Canvas(master, width=200, height=50, background=self.backgroundColor, highlightthickness=0)
        self.canvas.grid(row=2)

        self.currentPlayerVar = StringVar(self.master, value="")
        self.currentPlayerLabel = Label(self.master, textvariable=self.currentPlayerVar, anchor=W)
        self.currentPlayerLabel.grid(row=2,column=1,columnspan =2)

        self.canvas.bind('<Button-1>', self._canvasClick)
        self.newGame()

    def draw(self):
        for c in range(self.game.size['c']):
            for r in range(self.game.size['r']):
                if r >= len(self.game.grid[c]): continue

                x0 = c * self.elementSize
                y0 = r * self.elementSize
                x1 = (c + 1) * self.elementSize
                y1 = (r + 1) * self.elementSize
                fill = self.p1Color if self.game.grid[c][r] == self.game.players[True] else self.p2Color
                ball = self.canvas.create_oval(x0 + 2,
                                               self.canvas.winfo_height() - (y0 + 2),
                                               x1 - 2,
                                               self.canvas.winfo_height() - (y1 - 2),
                                               fill=fill, outline=self.gridColor)

    def move_ball(self):

        self.canvas.move(self.ball, 0, self.yspeed)
        (leftpos, toppos, rightpos, bottompos) = self.canvas.coords(self.ball)
        if (leftpos == self.leftpos) and (toppos == self.toppos_end) and (
                rightpos == (self.rightpos)) and (bottompos == self.bottompos_end):
            self.yspeed =0

        self.canvas.after(30,self.move_ball)



    def animation(self, c, player):
        #we will want to see what is the coard to make animition to
        '''self.canvas.create_oval(x0 + 2,
                                        self.canvas.winfo_height() - (y0 + 2),
                                        x1 - 2,
                                        self.canvas.winfo_height() - (y1 - 2),
                                        fill=fill, outline=self.gridColor)'''
        #this it the coard the canvas gets,


        #those are the first coardinations

        c_start = c
        r_start = 9
        x0_start = c_start * self.elementSize
        y0_start = r_start * self.elementSize
        x1_start = (c_start + 1) * self.elementSize
        y1_start = (r_start + 1) * self.elementSize
        fill = self.p1Color if player == "X" else self.p2Color


        self.ball = self.canvas.create_oval(x0_start + 2,
                                            self.canvas.winfo_height() - (y0_start + 2),
                                            x1_start - 2,
                                            self.canvas.winfo_height() - (y1_start - 2),
                                            fill=fill, outline=self.gridColor)



        # coard stop = when it should be place
        c_end = c
        r_end = len(self.game.grid[c])
        x0_end = c_end * self.elementSize
        y0_end = r_end * self.elementSize
        x1_end = (c_end + 1) * self.elementSize
        y1_end = (r_end + 1) * self.elementSize

        end_ball = self.canvas.create_oval(x0_end + 2,
                                           self.canvas.winfo_height() - (y0_end + 2),
                                           x1_end - 2,
                                           self.canvas.winfo_height() - (y1_end - 2),
                                           fill=None, outline="white")
        #we want to get the coard so we made an invisible second ball and we will get its coards

        (self.leftpos, self.toppos_end, self.rightpos, self.bottompos_end) = self.canvas.coords(end_ball)

        self.yspeed = 10


        self.canvas.after(30,self.move_ball)










    def drawGrid(self):
        x0, x1 = 0, self.canvas.winfo_width()#gets the width info
        for r in range(1, self.game.size['r']):
            y = r * self.elementSize
            self.canvas.create_line(x0, y, x1, y, fill=self.gridColor)#create the lines

        y0, y1 = 0, self.canvas.winfo_height()
        for c in range(1, self.game.size['c']):
            x = c * self.elementSize
            self.canvas.create_line(x, y0, x, y1, fill=self.gridColor)

    def drop(self, column):
        return self.game.drop(column)

    def newGame(self):
        # Ask for players' names
        self.p1 = 'Blue'
        self.p2 = 'Red'

        # Ask for grid size
        columns = 10
        rows = 10

        self.game = setup.four_in_a_row(columns=columns, rows=rows)

        self.canvas.delete(ALL)
        self.canvas.config(width=(self.elementSize) * self.game.size['c'],
                           height=(self.elementSize) * self.game.size['r'])
        self.master.update()  # Rerender window
        self.drawGrid()
        self.draw()

        self._updateCurrentPlayer()

        self.gameOn = True

    def _updateCurrentPlayer(self):
        p = self.p1 if self.game.first_player else self.p2
        self.currentPlayerVar.set('Current player: ' + p)


    def _canvasClick(self, event):
        if not self.gameOn: return
        if self.game.game_over: return

        c = event.x // self.elementSize

        if (0 <= c < self.game.size['c']):
            self.draw()
            col = self.game.color()

            self.animation(c,col)

            self.drop(c)

            self._updateCurrentPlayer()

        if self.game.game_over:
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            if self.game.game_over == 'draw':
                t = 'DRAW!'
            else:
                winner = self.p1 if self.game.first_player else self.p2
                t = winner + ' won!'
            self.canvas.create_text(x, y, text=t, font=("Verdana", 50), fill="#333")

    def _newGameButton(self):
        self.newGame()

    def _save(self):
        grid = self.game.grid
        save_load.save(grid)

    def _load(self):
        board = save_load.load()
        self.game.grid = board
        self.draw()


root = Tk()
app = GUI(root)

root.mainloop()
