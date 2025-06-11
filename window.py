from tkinter import *
import time
from maze import Maze

#! This window class encapsulates the GUI and Canvas that we are going to be using
#@ We define properties of the window (title,width,height)
## Using TKinter we are creating a root(which is basically the window itself)
## Canvas is what we use to draw stuff onto the screen using methods
## Redraw updates the GUI and wait_for_close is a loop that keeps calling redraw aslong as we want
class Window:
    def __init__(self, title, height, width):
        self.title = title
        self.height = height
        self.width = width
        self.__root = Tk()
        self.__root.title(self.title)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        
        self.maze = None
        self.windowRunning = False
        
        #@ Creating input and maze screens
        self.inputFrame = Frame(self.__root)
        self.mazeFrame = Frame(self.__root)
                
        #@ Setup functions for input and maze screens
        self.setup_input_screen()
        self.setup_maze_screen()
        
        #@ Start with the input screen -> maze screen is called with a button (from setup_input_screen)
        self.inputFrame.pack()

        
        # #! Button for generating maze
        # self.createButton = Button(self.__root, text="Create Maze")
        # self.createButton.config(command=self.create_maze)
        # self.createButton.pack()
        # self.createButtonPress = False
        
    def setup_input_screen(self):
        #! Input Screen
        Label(self.inputFrame, text="Maze Size").pack()
        Label(self.inputFrame, text="Rows").pack()
        self.rowInput = Entry(self.inputFrame)
        self.rowInput.pack()
        
        Label(self.inputFrame, text="Columns").pack()
        self.colInput = Entry(self.inputFrame)
        self.colInput.pack()
        
        start_button = Button(self.inputFrame, text="Generate Maze", command=self.start_maze_screen)
        start_button.pack()
    
    def setup_maze_screen(self):
        # Canvas
        self.canvas = Canvas(self.mazeFrame, bg="white", width=self.width, height=self.height)
        self.canvas.pack()

        # Buttons
        self.solveButton = Button(self.mazeFrame, text="Solve Maze", command=self.solve_maze)
        self.solveButton.pack()

        self.clearButton = Button(self.mazeFrame, text="Clear & Back", command=self.back_to_input_screen)
        self.clearButton.pack()
    
    def start_maze_screen(self):
        try:
            rows = int(self.rowInput.get())
            cols = int(self.colInput.get())
            
        except ValueError:
            print("Invalid input")
            return

        self.createButtonPress = True

        self.inputFrame.pack_forget()
        self.mazeFrame.pack()

        self.maze = Maze(10, 10, rows, cols, 25, 25, self, 0.5)
    
    def back_to_input_screen(self):
        self.canvas.delete("all")
        self.createButtonPress = False
        self.mazeFrame.pack_forget()
        self.inputFrame.pack()

    #! Function for button callback
    def create_maze(self):
        if self.createButtonPress == False:
            self.createButtonPress = True
            self.maze = Maze(10,10,10,10,30,30,self, 4)
        else:
            return
    
    def solve_maze(self):
        if self.maze != None:
            self.maze.solve()
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.createButtonPress = False
    
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)
        
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
        
    def wait_for_close(self):
        self.windowRunning = True
        
        while self.windowRunning:
            self.redraw()
            time.sleep(1/60)
    
    def close(self):
        self.windowRunning = False
                
