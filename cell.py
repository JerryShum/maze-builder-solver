from graphics import Line, Point

class Cell:
    def __init__(self, row, col, window=None):
        self.__window = window
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.row = row
        self.col = col
        
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        
        self.visited = False
   
        
    def draw(self,x1,y1,x2,y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        
        if self.__window == None:
            return
        
        if self.has_left_wall:
            point1 = Point(x1, y1)
            point2 = Point(x1, y2)
            line = Line(point1, point2)
            self.__window.draw_line(line, "black")
        else:
            point1 = Point(x1, y1)
            point2 = Point(x1, y2)
            line = Line(point1, point2)
            self.__window.draw_line(line, "white")
        
        if self.has_right_wall:
            point1 = Point(x2, y1)
            point2 = Point(x2, y2)
            line = Line(point1, point2)
            self.__window.draw_line(line, "black")
        else:
            point1 = Point(x2, y1)
            point2 = Point(x2, y2)
            line = Line(point1, point2)
            self.__window.draw_line(line, "white")
        
        if self.has_top_wall:
            point1 = Point(x1, y1)
            point2 = Point(x2, y1)
            line = Line(point1, point2)
            self.__window.draw_line(line, "black")
        else:
            point1 = Point(x1, y1)
            point2 = Point(x2, y1)
            line = Line(point1, point2)
            self.__window.draw_line(line, "white")
            
        
        if self.has_bottom_wall:
            point1 = Point(x1, y2)
            point2 = Point(x2, y2)
            line = Line(point1, point2)
            self.__window.draw_line(line, "black")
        else:
            point1 = Point(x1, y2)
            point2 = Point(x2, y2)
            line = Line(point1, point2)
            self.__window.draw_line(line, "white")
            
    def draw_move(self, to_cell, undo=False, bfs=False):
        
        if self.__window == None:
            return
        
        #! self center coordinates
        xoffset = abs(self.__x2 - self.__x1) // 2
        xcenter = self.__x1 + xoffset
        
        yoffset = abs(self.__y2 - self.__y1) // 2
        ycenter = self.__y1 + yoffset
        
        #! to_cell center coordinates
        xoffset2 = abs(to_cell.__x2 - to_cell.__x1) // 2
        xcenter2 = to_cell.__x1 + xoffset2
        
        yoffset2 = abs(to_cell.__y2 - to_cell.__y1) // 2
        ycenter2 = to_cell.__y1 + yoffset2
        
        # if we are undoing, set the line to gray
        if undo:
            fill_color = "gray"
        elif bfs:
            fill_color = "green"
        else:
            fill_color = "red"
            
        #! Define the center points of each cell in coordinates
        point1 = Point(xcenter, ycenter)
        point2 = Point(xcenter2, ycenter2)
        
        #! Draw a line between the 2 center points
        line = Line(point1, point2)
        self.__window.draw_line(line, fill_color)

        
        
        
        