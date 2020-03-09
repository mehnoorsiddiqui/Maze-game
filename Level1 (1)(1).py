import turtle
import math

wn=turtle.Screen()
wn.bgcolor("plum")
wn.title("A Maze Game")
wn.setup(700,700)
wn.tracer(0)

#set score on screen
score=turtle.Turtle(visible=False)  # For time output
score.penup()
score.color("black")
score.setposition(300, 300)  # In this position I want to output variable
score.write("Score="+str(0),align="right",font=("Arial",14,"normal"))


#register shapes
turtle.register_shape("wall.gif")
turtle.register_shape("Player.gif")
turtle.register_shape("Candy.gif")
turtle.register_shape("Door.gif")

#create block
class Block(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("black")
        self.penup()
        self.speed(0)
        
#create Player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("Player.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.candy=0

    def go_up(self):
        #calculate the spot to move to
        move_to_x=self.xcor()
        move_to_y=self.ycor()+24
        #check if the space has a wall
        if (move_to_x , move_to_y) not in walls:
            if (move_to_x , move_to_y) not in dr:
                    self.goto(move_to_x , move_to_y)
            
    def go_down(self):
        #calculate the spot to move to
        move_to_x=self.xcor()
        move_to_y=self.ycor()-24
        #check if the space has a wall
        if (move_to_x , move_to_y) not in walls:
            if (move_to_x , move_to_y) not in dr:
                    self.goto(move_to_x , move_to_y)

    def go_left(self):
        #calculate the spot to move to
        move_to_x=self.xcor()-24
        move_to_y=self.ycor()
        #check if the space has a wall
        if (move_to_x , move_to_y) not in walls:
            if (move_to_x , move_to_y) not in dr:
                    self.goto(move_to_x , move_to_y)
                    
    def go_right(self):
        #calculate the spot to move to
        move_to_x=self.xcor()+24
        move_to_y=self.ycor()
        #check if the space has a wall
        if (move_to_x , move_to_y) not in walls:
            if (move_to_x , move_to_y) not in dr:
                    self.goto(move_to_x , move_to_y)

    def is_collision(self,other):
        a=self.xcor()-other.xcor()
        b=self.ycor()-other.ycor()
        distance=math.sqrt((a**2)+(b**2))
        if distance < 5 :
            return True
        else:
            return False
    def is_collide(self,other):
        a=self.xcor()-other.xcor()
        b=self.ycor()-other.ycor()
        distance=math.sqrt((a**2)+(b**2))
        if distance < 25 :
            return True
        else:
            return False

class Treasure(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("Candy.gif")
        self.penup()
        self.speed(0)
        self.candy=100
        self.goto(x,y)

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

class Door(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("Door.gif")
        self.penup()
        self.speed(0)
        self.goto(x,y)

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()
        
#create levels lists
levels=[""]

maze = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP X                 T  X",
"X  X  XX    XXXXXXXXXXXXX",
"X  X  X                 X",
"X       XXXXXX   XXXXXXXX",
"X XXXX  XXT XX   XX  T  X",
"X XXXX  XX  XX   XX     X",
"X XXXX  XX  XX      XXXXX",
"XXXXXX                  X",
"X T     XXXXXXXXXXXXXXXXX",
"XXXX      XXXXXXXXXXXXXXX",
"X         X    T XXXXXXXX",
"X                XXXXX  X",
"XX   XXXXXXXXXX  XXXXX  X",
"XXX  XXXXXXXXXX         X",
"XXX                    TX",
"XXX         XXXXXXXXXXXXX",
"XXXXXXXXXX  XXXXXXXXXXXXX",
"XXXXXXXXXX              X",
"XX T XXXXX             TD",
"XX   XXXXXXXXXXXXX  XXXXX",
"XX    YXXXXXXXXXXX  XXXXX",
"XX                      X",
"XXXX                    X",
"XXXXXXXXXXXXXXXXXXXXXXXXX"]
#add a treasure list
treasures= []

#add a door list
doors=[]

#add maze to mazes lists
levels.append(maze)

#create level setup function
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            #get the character at each x,y coordinate
            #note the order of each y and x in the next line
            character=level[y][x]
            #calculate the screen x,y coordinate
            screen_x=-288+(x*24)
            screen_y=288-(y*24)

            #check if it is an X (representing a wall)
            if character=='X':
                block.goto(screen_x,screen_y)
                block.shape("wall.gif")
                block.stamp()
                
                #add cordinates to wall list
                walls.append((screen_x,screen_y))

            #check if it is a P (representing the player)
            if character=="P":
                player.goto(screen_x,screen_y)

            #check if it is a T(representing treasure)
            if character=="T":
                treasures.append(Treasure(screen_x,screen_y))

            #check if it is a D(representing Door)
            if character=="D":
                doors.append(Door(screen_x,screen_y))
                block.stamp()
            
                #add cordinates to wall list
                dr.append((screen_x,screen_y))

#create class instances
block=Block()
player=Player()

#create walls co-ordinate lists
walls=[]
dr=[]
#set up the game
setup_maze(levels[1])


#keyboard bindings
turtle.listen()
turtle.onkey(player.go_left,"Left")
turtle.onkey(player.go_right,"Right")
turtle.onkey(player.go_up,"Up")
turtle.onkey(player.go_down,"Down")


#Main Game Loop
try:
    while True :
        for treasure in treasures:
            if player.is_collision(treasure):
                player.candy += treasure.candy
                print("Player points : {}".format(player.candy))
                treasure.destroy()
                treasures.remove(treasure)
                score.undo()  # undraw the last time update
                score.setposition(300,300)
                score.write("Points : {}".format(player.candy),align="right",font=("Arial",14,"normal"))
                wn.update()

        for door in doors:
            if player.candy >= 300:
                door.hideturtle()
                if player.is_collide(door):
                    print("YOU WIN!!")  
                    wn.bye()
                    
        wn.update()

except turtle.Terminator:
    pass

   









    
