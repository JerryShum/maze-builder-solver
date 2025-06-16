from cell import Cell
import time
import random
from collections import deque
class Maze:
    def __init__(self, x1,y1, num_rows, num_cols, cell_size_x, cell_size_y, window = None, seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.__cells = []
        
        if seed != None:
            random.seed(seed)
        
        self.__create_cells()
        self.__break_walls_r_dfs(0,0)
        self.__break_entrance_and_exit()
        self.__reset_cells_visited()
        
    
    def __create_cells(self):
        for row in range(self.num_rows):
            
            rowList = []
            for col in range(self.num_cols):
               
                rowList.append(Cell(row,col, self.window))
            self.__cells.append(rowList)
        
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.__draw_cell(row, col)
    
    def __draw_cell(self, row, col):
        x1 = self.x1 + col * self.cell_size_x
        x2 = self.x1 + col * self.cell_size_x + self.cell_size_x
        y1 = self.y1 + row * self.cell_size_y
        y2 = self.y1 + row * self.cell_size_y + self.cell_size_y
        self.__cells[row][col].draw(x1,y1,x2,y2)
        
        self.__animate()
    
    def __animate(self):
        if self.window == None:
            return
        
        self.window.redraw()
        time.sleep(1/60)
    
    def __reset_cells_visited(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.__cells[row][col].visited = False
        
    def __break_entrance_and_exit(self):
        # set the top left cell
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        
        # set the bottom right cell
        self.__cells[self.num_rows - 1][self.num_cols - 1].has_bottom_wall = False
        self.__draw_cell(self.num_rows - 1, self.num_cols - 1)
    
    
    #! DFS algorithm for breaking down walls 
    def __break_walls_r_dfs(self, row, col):
        current_cell = self.__cells[row][col]
        current_cell.visited = True
        
        while True:
            neighbours = []
            
            # check the array for cells to top, left, bottom, right of the current cell
            # once we get a list of potential neighbours, -> choose a random neighbour to travel to.
            
            #! checking for the cell to the top
            if row - 1 >= 0:
                top_cell = self.__cells[row - 1][col]
                if not top_cell.visited:
                    neighbours.append(("top", top_cell, row - 1, col))
                    
            #! checking for the cell to the left
            if col - 1 >= 0:
                left_cell = self.__cells[row][col - 1]
                if not left_cell.visited:
                    neighbours.append(("left", left_cell, row, col - 1))
          
            #! Checking for the cell to the bottom
            if row + 1 < self.num_rows:
                bottom_cell = self.__cells[row + 1][col]
                if not bottom_cell.visited:
                    neighbours.append(("bottom", bottom_cell, row + 1, col))
              
            #! Checking for the cell to the right
            if col + 1 < self.num_cols:
                right_cell = self.__cells[row][col + 1]
                if not right_cell.visited:
                    neighbours.append(("right", right_cell, row, col + 1))
              
                    
            if len(neighbours) == 0:
                self.__draw_cell(row,col)
                return
            
            # Pick a random neighbour
            randomNum = random.randint(0,len(neighbours) - 1)
            direction = neighbours[randomNum][0]
            next_cell = neighbours[randomNum][1]
            travelRow = neighbours[randomNum][2]
            travelCol = neighbours[randomNum][3]
            
            # break down walls between that cell
            if direction == "top":
                current_cell.has_top_wall = False
                next_cell.has_bottom_wall = False
                self.__break_walls_r_dfs(travelRow, travelCol)
            elif direction == "left":
                current_cell.has_left_wall = False
                next_cell.has_right_wall = False
                self.__break_walls_r_dfs(travelRow, travelCol)
            elif direction == "bottom":
                current_cell.has_bottom_wall = False
                next_cell.has_top_wall = False
                self.__break_walls_r_dfs(travelRow, travelCol)
            elif direction == "right":
                current_cell.has_right_wall = False
                next_cell.has_left_wall = False
                self.__break_walls_r_dfs(travelRow, travelCol)
            
    
    def __break_walls_bfs(self, row, col):
        current_cell=self.__cells[row][col]
        current_cell.visited = True
        queue = deque()
        queue.append(current_cell)
        
        while queue:
            # removes item from the front of the queue
            queue_cell = queue.popleft()
            #! Update row and col to the new cell that we dequeued
            row = queue_cell.row
            col = queue_cell.col
            current_cell = self.__cells[row][col]
            
            # find neighbours
            neighbours = []
            
            # once we get a list of potential neighbours, -> choose a random neighbour to travel to.
            #! checking for the cell to the top
            if row - 1 >= 0:
                top_cell = self.__cells[row - 1][col]
                if not top_cell.visited:
                    neighbours.append(("top", top_cell, row - 1, col))
                    
            #! checking for the cell to the left
            if col - 1 >= 0:
                left_cell = self.__cells[row][col - 1]
                if not left_cell.visited:
                    neighbours.append(("left", left_cell, row, col - 1))
          
            #! Checking for the cell to the bottom
            if row + 1 < self.num_rows:
                bottom_cell = self.__cells[row + 1][col]
                if not bottom_cell.visited:
                    neighbours.append(("bottom", bottom_cell, row + 1, col))
              
            #! Checking for the cell to the right
            if col + 1 < self.num_cols:
                right_cell = self.__cells[row][col + 1]
                if not right_cell.visited:
                    neighbours.append(("right", right_cell, row, col + 1))
              
            # if the cell we travel to has no potential neighbours, re-draw that cell
            if len(neighbours) == 0:
                self.__draw_cell(row,col)
            
            #@ SINCE ITS BFS -> we want to travel to all the neighbours first (adding them to the queue)
            # since the queue loops, we add all the neighbours' neighbours to the queue aswell
            while len(neighbours) > 0:
                # travel to a random neighbour
                randnum = random.randint(0, len(neighbours) - 1)
                direction = neighbours[randnum][0]
                neighbour_cell = neighbours[randnum][1]
                
                if direction == "top":
                    current_cell.has_top_wall = False
                    neighbour_cell.has_bottom_wall = False
                elif direction == "left":
                    current_cell.has_left_wall = False
                    neighbour_cell.has_right_wall = False
                elif direction == "bottom":
                    current_cell.has_bottom_wall = False
                    neighbour_cell.has_top_wall = False
                elif direction == "right":
                    current_cell.has_right_wall = False
                    neighbour_cell.has_left_wall = False
                    
                # remove neighbour from neighbours array
                neighbours.pop(randnum)
                
                #! mark the neighbour_cell as visited
                neighbour_cell.visited = True
                queue.append(neighbour_cell)
                
                # draw the current cell to update the walls
                self.__draw_cell(row, col)

        
    def __solve_r(self, row, col):
        self.__animate()
        current_cell = self.__cells[row][col]
        current_cell.visited = True
        
        # if we re at the bottom right cell (end) -> we are done
        if current_cell == self.__cells[self.num_rows - 1][self.num_cols - 1] :
            return True
        
        #----------
        
        # check each direction
        # Check top cell
        if row - 1 >= 0 and not current_cell.has_top_wall:
            top_cell = self.__cells[row - 1][col]
            if not top_cell.visited:
                current_cell.draw_move(top_cell)
                if self.__solve_r(row - 1, col):
                    return True
                else:
                    current_cell.draw_move(top_cell, undo=True)

        # Check left cell
        if col - 1 >= 0 and not current_cell.has_left_wall:
            left_cell = self.__cells[row][col - 1]
            if not left_cell.visited:
                current_cell.draw_move(left_cell)
                if self.__solve_r(row, col - 1):
                    return True
                else:
                    current_cell.draw_move(left_cell, undo=True)

        # Check bottom cell
        if row + 1 < self.num_rows and not current_cell.has_bottom_wall:
            bottom_cell = self.__cells[row + 1][col]
            if not bottom_cell.visited:
                current_cell.draw_move(bottom_cell)
                if self.__solve_r(row + 1, col):
                    return True
                else:
                    current_cell.draw_move(bottom_cell, undo=True)

        # Check right cell
        if col + 1 < self.num_cols and not current_cell.has_right_wall:
            right_cell = self.__cells[row][col + 1]
            if not right_cell.visited:
                current_cell.draw_move(right_cell)
                if self.__solve_r(row, col + 1):
                    return True
                else:
                    current_cell.draw_move(right_cell, undo=True)
        
        return False
    
    def solve_bfs(self, row, col):
        
        self.__animate()
        current_cell = self.__cells[row][col]
        current_cell.visited = True
        
        #! Dictionary to store the parent of each cell
        # (row,col) -> (prev_row, prev_col)
        parents = {}
        

        queue = deque()
        queue.append(current_cell)
        
        while queue:
            queue_cell = queue.popleft()
            queue_cell.visited = True
            row = queue_cell.row
            col = queue_cell.col
            
            # if queue_cell is the end_cell (bottom left)
            if queue_cell == self.__cells[self.num_rows -1][self.num_cols - 1]:
                break
            
   
            
            #! Find the neighbours of the cell
            #@ checking for the cell to the top
            if row - 1 >= 0:
                top_cell = self.__cells[row - 1][col]
                if not top_cell.visited and not queue_cell.has_top_wall and not top_cell.has_bottom_wall:
                    # mark as visited
                    top_cell.visited = True
                    
                    # add the neighbour to the queue
                    queue.append(top_cell)
                    
                    # add the neighbour to the parents dictionary
                    parents[(row - 1, col)] = (row, col)
                    
                    queue_cell.draw_move(top_cell)
                    self.__animate()
                    
            #@ checking for the cell to the left
            if col - 1 >= 0:
                left_cell = self.__cells[row][col - 1]
                if not left_cell.visited and not queue_cell.has_left_wall and not left_cell.has_right_wall:
                    # mark as visited
                    left_cell.visited = True
                    
                    
                    # add the neighbour to the queue
                    queue.append(left_cell)
                    
                    # add the neighbour to the parents dictionary
                    parents[(row, col - 1)] = (row, col)
                    
                    queue_cell.draw_move(left_cell)
                    self.__animate()
          
            #@ Checking for the cell to the bottom
            if row + 1 < self.num_rows:
                bottom_cell = self.__cells[row + 1][col]
                if not bottom_cell.visited and not queue_cell.has_bottom_wall and not bottom_cell.has_top_wall:
                    # mark as visited
                    bottom_cell.visited = True
                    
                    # add the neighbour to the queue
                    queue.append(bottom_cell)
                    
                    # add the neighbour to the parents dictionary
                    parents[(row + 1, col)] = (row, col)
                    
                    queue_cell.draw_move(bottom_cell)
                    self.__animate()
              
            #@ Checking for the cell to the right
            if col + 1 < self.num_cols:
                right_cell = self.__cells[row][col + 1]
                if not right_cell.visited and not queue_cell.has_right_wall and not right_cell.has_left_wall:
                    # mark as visited
                    right_cell.visited = True
                    
                    # add the neighbour to the queue
                    queue.append(right_cell)
            
                    # add the neighbour to the parents dictionary
                    parents[(row, col + 1)] = (row, col)
                    
                    queue_cell.draw_move(right_cell)
                    self.__animate()
        
        #! Backtrack from the end cell to the start cell (solution for the maze)
        # starting from the end cell
        current_cell = self.__cells[self.num_rows - 1][self.num_cols - 1]
        
        # re-assigning current_cell to the parent of the current cell
        # draw_move(current_cell)
        # until current_cell is the start cell
        while current_cell != self.__cells[0][0]:
            prev_row, prev_col = parents[(current_cell.row, current_cell.col)]
            current_cell.draw_move(self.__cells[prev_row][prev_col], bfs=True)
            current_cell = self.__cells[prev_row][prev_col]
            self.__animate()
            
        return True
        
        
    
    def solve(self, algorithm="dfs"):
        if algorithm == "dfs":
            if self.__solve_r(0,0):
                return True
            else:
                return False
        elif algorithm == "bfs":
            if self.solve_bfs(0,0):
                return True
            else:
                return False
                
            

            
            
            
        
        
        