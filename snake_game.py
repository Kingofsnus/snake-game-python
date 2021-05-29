from tkinter import *
import random


GAME_WIDTH = 750
GAME_HEIGHT = 750
SPEED = 80
SPACE_SIDE = 50
BODY_PARTS = 3
SNAKE_COLOR = '#fc03fc'
FOOD_COLOR = '#6600ff'
BACKGROUND_COLOR = '#111317'


class Snake:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0,BODY_PARTS):
            self.coordinates.append([0,0])

        for x ,y in self.coordinates:
            square = canvas.create_rectangle(x,y, x+SPACE_SIDE,y+SPACE_SIDE,fill=SNAKE_COLOR,tag='snake')
            self.squares.append(square)


class Food:
    
    def __init__(self):
        
        x = random.randint(0, (GAME_WIDTH/SPACE_SIDE)-1) * SPACE_SIDE
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIDE)-1) * SPACE_SIDE

        self.coordinates = [x,y]

        canvas.create_oval(x,y, x+SPACE_SIDE, y+SPACE_SIDE, fill=FOOD_COLOR,tag='food')


def next_turn(snake,food):
    x,y =   snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIDE

    elif direction == 'down':
        y += SPACE_SIDE

    elif direction == 'right':
        x += SPACE_SIDE

    elif direction == 'left':
        x -= SPACE_SIDE
    
    snake.coordinates.insert(0, (x,y) )
    square = canvas.create_rectangle(x,y, x+SPACE_SIDE, y+SPACE_SIDE,fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1
        label.config(text=f'Score: {score}')

        canvas.delete('food')
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if collisions(snake):
        game_over()
    else:    
        wind.after(SPEED,next_turn,snake,food)
    
    
def change_directory(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def collisions(snake):
    x,y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    
    return False
    
        
def game_over():
    
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_height()/2 ,canvas.winfo_width()/2 ,font=('ink free',60),text='Game Over',fill='red',tag='gameover')


wind = Tk()
wind.resizable(False,False)

score = 0
direction = 'down'

label = Label(wind,text='Score: {}'.format(score),font=('ink free',40))
label.pack()

canvas = Canvas(wind,bg=BACKGROUND_COLOR,width=GAME_WIDTH,height=GAME_HEIGHT)
canvas.pack()

wind.update()

wind_width = wind.winfo_width()
wind_height = wind.winfo_height()
screen_width = wind.winfo_screenwidth()
screen_height = wind.winfo_screenheight()

x = int((screen_width/2) - (wind_width/2))
y = int((screen_height/2) - (wind_height/2))

wind.geometry(f'{wind_width}x{wind_height}+{x}+{y}')

wind.bind('<Right>',lambda eve:change_directory('right'))
wind.bind('<Left>',lambda eve:change_directory('left'))
wind.bind('<Up>',lambda eve:change_directory('up'))
wind.bind('<Down>',lambda eve:change_directory('down'))


snake = Snake()
food = Food()

next_turn(snake,food)

wind.mainloop()