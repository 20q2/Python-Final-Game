import random

floor = []
rooms = []
floor_width = 40
floor_height = 40



def Initialize_Floor():
    global floor
    for i in range(0,floor_height):
        row = []
        for j in range(0,floor_width):
            row.append('.')
        floor.append(row)
    #help

def Print_Floor():
    for i in range(0,floor_height):
        print("".join(floor[i]))

def Clear_Floor():
    for i in range(0,floor_height):
        for j in range(0, floor_width):
            floor[i][j] = '.'
    roomslen = len(rooms)
    for x in range(0,roomslen):
        rooms.pop()
        
class Point:
    def __init__(self, row, column):
        self.r = row
        self.c = column

class Room:
    def __init__(self, height, width):
       self.height = height
       self.width = width

    def Place_Char(self, item):
        print("origin", self.originr, self.originc)
        posr = 0
        posc = 0
        worked = False
        for i in range(0,100):
            posr = random.randint(1,self.size-2)
            posc = random.randint(1,self.size-2)
            if floor[self.originr+posr][self.originc+posc] == '.':
                worked = True
                break
        if worked:
            floor[self.originr+posr][self.originc+posc] = item

    def Is_Within(self, point): #Return true when point is within this rooms dimensions
        #  this.botrow+1 >= pointr >= this.toprow-1 and this.rightcol+1 >= pointc >= this.leftcol-1
       # print("this:[{0},{1}]-{2} , point:[{3},{4}]".format(self.originr,self.originc,self.size,point.r,point.c))
        if point.r <= self.originr+self.size+1:
            #print("confirmed: {0} is <= {1}".format(point.r, self.originr+self.size+1))
            if point.r >= self.originr-1:
                #print("confirmed: {0} is >= {1}".format(point.r, self.originr-1))
                if point.c <= self.originc+self.size+1:
                    #print("confirmed: {0} is <= {1}".format(point.c, self.originc+self.size+1))
                    if point.c >= self.originc-1:
                        #print("confirmed: {0} is >= {1}".format(point.c, self.originc-1))
                        return True
        return False
                
    def Is_Facing(self, Room):
        return 0

    def Is_Adjacent(self, Room):
        return 0

    def Random_Dimensions(self):
        attempts = 0
        while True:
            attempts = attempts + 1
            if attempts == 50:
                return False
            self.size = random.randint(4,9)
            self.originr = random.randint(0,floor_height-self.size-1)
            self.originc = random.randint(0,floor_width-self.size-1)
            
            self.origin = Point(self.originr, self.originc)
            self.topleft = Point(self.originr, self.originc)
            self.topright = Point(self.originr, self.originc+self.size)
            self.bottomleft = Point(self.originr+self.size, self.originc)
            self.bottomright = Point(self.originr+self.size, self.originc+self.size)

            #check rooms potential dimensions against other existing rooms
            within_flag = False
            for x in rooms:
                string = "checking this point [{3},{4}] against room: [{0},{1}] size:{2}"
                #print(string.format(x.origin.r,x.origin.c,x.size,self.originr,self.originc))
                #If any corner is within the other rooms dimensions, try again
                if x.Is_Within(self.topleft):
                    within_flag = True
                if x.Is_Within(self.topright):
                    within_flag = True
                if x.Is_Within(self.bottomleft):
                    within_flag = True
                if x.Is_Within(self.bottomright):
                    within_flag = True
                #check the other way around too!
                if self.Is_Within(x.topleft):
                    within_flag = True
                if self.Is_Within(x.topright):
                    within_flag = True
                if self.Is_Within(x.bottomleft):
                    within_flag = True
                if self.Is_Within(x.bottomright):
                    within_flag = True


            if within_flag:
                #print("One failed attempt")
                continue
            else:
                #print("Room location confirmed, adding to global")
                break

        global floor
        for i in range(0,self.size): #Draw walls in appropriate spots
            floor[self.originr][self.originc+i+1] = '#'
            floor[self.originr+i+1][self.originc] = '#'
            floor[self.originr+self.size][self.originc+i+1] = '#'
            floor[self.originr+i+1][self.originc+self.size] = '#'

        floor[self.originr][self.originc] = '+' #For hallways generation
        floor[self.topright.r][self.topright.c] = '+'
        floor[self.bottomleft.r][self.bottomleft.c] = '+'
        floor[self.bottomright.r][self.bottomright.c] = '+'
        return True

def Convert_Hallways():
    #Sweep floor, replace all sides of hallways with actual walls
    hallways = []
    for i in range(0,floor_height):
        for j in range(0,floor_width):
            if floor[i][j] == '^' or floor[i][j] == 'V' or floor[i][j] == '<' or floor[i][j] == '>':
                hall_point = Point(i,j)
                hallways.append(hall_point)
                #Replace surrounding areas with walls
                if floor[i+1][j] == '.':
                    floor[i+1][j] = '#'
                if floor[i-1][j] == '.':
                    floor[i-1][j] = '#'
                if floor[i][j+1] == '.':
                    floor[i][j+1] = '#'
                if floor[i][j-1] == '.':
                    floor[i][j-1] = '#'

                if floor[i-1][j-1] == '.':
                    floor[i-1][j-1] = '#'
                if floor[i+1][j+1] == '.':
                    floor[i+1][j+1] = '#'
                if floor[i+1][j-1] == '.':
                    floor[i+1][j-1] = '#'
                if floor[i-1][j+1] == '.':
                    floor[i-1][j+1] = '#'
    #Move through stored hallway tiles, turn them into empty
    for x in hallways:
        floor[x.r][x.c] = '.'

def Cut_Ends():
    #map is now mess of tangled hallways and rooms
    #Create "Despawners" at each edge of the map, stop when hitting an intersection
    #first, convert all the + debug corners back into #
    for i in range(0,floor_height):
        for j in range(0,floor_width):
            if floor[i][j] == '+':
                floor[i][j] = '#'

    #First scan - Top to bottom
    for j in range(0,floor_width):##!!!
        for i in range(0,floor_height): ##!!!
            edge_check = 0
            if i == 0:
                edge_check = 1
            if floor[i][j] == '^': ## IMPORTANT TO CHANGE
                if ((floor[i][j+1] == '.' or floor[i][j+1] == '#') and (floor[i][j-1] == '.' or floor[i][j-1] == '#')
                    and (floor[i-1+edge_check][j] == '.' or floor[i-1+edge_check][j] == '^')): #Make sure its not part of an intersection
                    floor[i][j] = '.'
                else:
                    break
            if floor[i][j] == ':':
                floor[i][j] = '#'
            if floor[i][j] == '#':
                break #moveon to next column
                
    #Then bottom to top
    for j in range(0,floor_width):##!!!
        for i in range(floor_height-1,0,-1): ##!!!
            edge_check = 0
            if i == floor_height-1:
                edge_check = 1
            if floor[i][j] == 'V': ## IMPORTANT TO CHANGE
                if ((floor[i][j+1] == '.' or floor[i][j+1] == '#') and (floor[i][j-1] == '.' or floor[i][j-1] == '#')
                    and (floor[i+1-edge_check][j] == '.' or floor[i+1-edge_check][j] == 'V')):
                    floor[i][j] = '.'
                else:
                    break
            if floor[i][j] == ':':
                floor[i][j] = '#'
            if floor[i][j] == '#':
                break #moveon to next column

    #Left to right
    for i in range(0,floor_height):##!!!
        for j in range(0,floor_width): ##!!!
            edge_check = 0
            if j == 0:
                edge_check = 1
            if floor[i][j] == '<': ## IMPORTANT TO CHANGE
                if ((floor[i+1][j] == '.' or floor[i+1][j] == '#') and (floor[i-1][j] == '.' or floor[i-1][j] == '#')
                    and (floor[i][j-1+edge_check] == '.' or floor[i][j-1+edge_check] == '<')):
                    floor[i][j] = '.'
                else:
                    break
            if floor[i][j] == ':':
                floor[i][j] = '#'
            if floor[i][j] == '#':
                break #moveon to next column

    #right to left
    for i in range(0,floor_height):##!!!
        for j in range(floor_width-1, 0, -1): ##!!!
            edge_check = 0
            if j == floor_width-1:
                edge_check = 1
            if floor[i][j] == '>': ## IMPORTANT TO CHANGE
                if ((floor[i+1][j] == '.' or floor[i+1][j] == '#') and (floor[i-1][j] == '.' or floor[i-1][j] == '#')
                    and (floor[i][j+1-edge_check] == '.' or floor[i][j+1-edge_check] == '>')):
                    floor[i][j] = '.'
                else:
                    break
            if floor[i][j] == ':':
                floor[i][j] = '#'
            if floor[i][j] == '#':
                break #moveon to next column

    #Move on to the next part!
    Print_Floor()
    Convert_Hallways()
                
def Generate_Hallways():
    for room in rooms:
    #Stretch a hallway from each direction of each room
        #up, travel until hitting endge of map, a # (then make a door) or, a + (restart)
        for i in range(0,2):
            hall_pos = random.randint(1,room.size-1)
            start = Point(room.originr,room.originc+hall_pos)
            if floor[start.r][start.c] == ':':#check if we already got some openings
                continue

            inc = 0
            we_good = True
            end = Point(0,0)
            hallway = []
            while True: #stretch till we hit a wall or end of floor
                inc = inc - 1
                if start.r+inc == -1: #we good, end it off
                    end = Point(start.r+inc+1,start.c)
                    break              
                if floor[start.r+inc][start.c] == '#':
                    end = Point(start.r+inc,start.c)
                    break
                if floor[start.r+inc][start.c] == '+':
                    we_good = False #Try again
                    break
                if floor[start.r+inc][start.c] != '.':
                    end = Point(start.r+inc,start.c)
                    break
                hallway.append(Point(start.r+inc,start.c))

            if we_good: #work our way back from end 
                if floor[end.r][end.c] == '#': #make dat door
                    floor[end.r][end.c] = ':'
                floor[start.r][start.c] = ':'
                for x in hallway:
                    floor[x.r][x.c] = '^'
                break #Only 1 per side    

        #down
        for i in range(0,2):
            hall_pos = random.randint(1,room.size-1)
            start = Point(room.originr+room.size,room.originc+hall_pos)
            if floor[start.r][start.c] == ':':#check if we already got some openings
                continue

            inc = 0
            we_good = True
            end = Point(0,0)
            hallway = []
            while True: #stretch till we hit a wall or end of floor
                inc = inc + 1
                if start.r+inc == floor_height: #CHECK THIS!!!!!
                    end = Point(start.r+inc-1,start.c)
                    break              
                if floor[start.r+inc][start.c] == '#':
                    end = Point(start.r+inc,start.c)
                    break
                if floor[start.r+inc][start.c] == '+':
                    we_good = False #Try again
                    break
                if floor[start.r+inc][start.c] != '.':
                    end = Point(start.r+inc,start.c)
                    break
                
                hallway.append(Point(start.r+inc,start.c))

            if we_good: #work our way back from end 
                if floor[end.r][end.c] == '#': #make dat door
                    floor[end.r][end.c] = ':'
                floor[start.r][start.c] = ':'
                for x in hallway:
                    floor[x.r][x.c] = 'V'
                break #Only 1 per side

        #left
        for i in range(0,2):
            hall_pos = random.randint(1,room.size-1)
            start = Point(room.originr+hall_pos,room.originc)
            if floor[start.r][start.c] == ':':#check if we already got some openings
                continue

            inc = 0
            we_good = True
            end = Point(0,0)
            hallway = []
            while True: #stretch till we hit a wall or end of floor
                inc = inc - 1
                if start.c+inc == -1: #CHECK THIS!!!!!
                    end = Point(start.r,start.c+inc+1) #!!!!
                    break              
                if floor[start.r][start.c+inc] == '#':
                    end = Point(start.r,start.c+inc)
                    break
                if floor[start.r][start.c+inc] == '+':
                    we_good = False #Try again
                    break
                if floor[start.r][start.c+inc] != '.':
                    end = Point(start.r,start.c+inc)
                    break
                
                hallway.append(Point(start.r,start.c+inc))

            if we_good: #work our way back from end 
                if floor[end.r][end.c] == '#': #make dat door
                    floor[end.r][end.c] = ':'
                floor[start.r][start.c] = ':'
                for x in hallway:
                    floor[x.r][x.c] = '<'
                break #Only 1 per side

        #right
        for i in range(0,2):
            hall_pos = random.randint(1,room.size-1)
            start = Point(room.originr+hall_pos,room.originc+room.size)
            if floor[start.r][start.c] == ':':#check if we already got some openings
                continue

            inc = 0
            we_good = True
            end = Point(0,0)
            hallway = []
            while True: #stretch till we hit a wall or end of floor
                inc = inc + 1
                if start.c+inc == floor_width: #CHECK THIS!!!!!
                    end = Point(start.r,start.c+inc-1) #!!!!
                    break              
                if floor[start.r][start.c+inc] == '#':
                    end = Point(start.r,start.c+inc)
                    break
                if floor[start.r][start.c+inc] == '+':
                    we_good = False #Try again
                    break
                if floor[start.r][start.c+inc] != '.':
                    end = Point(start.r,start.c+inc)
                    break
                
                hallway.append(Point(start.r,start.c+inc))

            if we_good: #work our way back from end 
                if floor[end.r][end.c] == '#': #make dat door
                    floor[end.r][end.c] = ':'
                floor[start.r][start.c] = ':'
                for x in hallway:
                    floor[x.r][x.c] = '>'
                break #Only 1 per side

    Cut_Ends()
    
def Output_Floor(filename):
    textures = ["tileset = ground.png\n","tileset = brick&stone.png\n"]

    with open(filename, "w") as f:
        with open("template.txt", "r") as temp:
             lines = temp.readlines()
             for x in lines:
                f.write(x)
        f.seek(9)
        a = random.randint(0,1)
        f.write(textures[a]) #Can change tileset
        f.write("map = ")

        for i in range(0,floor_height):
            f.write("".join(floor[i]))
            f.write("\n")
            f.write("      ")

def Full_Create():
    #Make some rooms of varying sizes
    Clear_Floor()
    for i in range(0,9):
        new_room = Room(0,0)
        check = new_room.Random_Dimensions()
        if check:
            rooms.append(new_room)

    rooms[0].Place_Char('p')
    rooms[1].Place_Char('b')
    rooms[2].Place_Char('s')
    rooms[0].Place_Char('$')
    rooms[0].Place_Char('f')
    rooms[1].Place_Char('0')
    rooms[1].Place_Char('1')
    rooms[3].Place_Char('c')
    rooms[3].Place_Char('F')
    rooms[4].Place_Char('a')
    rooms[5].Place_Char('o')
    rooms[5].Place_Char('O')
    rooms[5].Place_Char('S')

    
    #Extend hallways randomly, then snip the ends
    Generate_Hallways()
    print("Generation done.\nRooms:")
    for x in rooms:
        string = "[{0},{1}] size:{2}"
        print(string.format(x.origin.r,x.origin.c,x.size))

    Print_Floor()
    Output_Floor("level.txt")
