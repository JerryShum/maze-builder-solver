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