import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

TILE_WIDTH = TILE_SIZE * COLS
TILE_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg= "black", width= TILE_WIDTH,height= TILE_HEIGHT, borderwidth= 0, highlightthickness= 0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2)-(window_width/2))
window_y = int((screen_height/2)-(window_height/2))

#format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game
Snake =Tile(TILE_SIZE * 5, TILE_SIZE * 5) #single tile, snake's head
Food =Tile(TILE_SIZE * 10, TILE_SIZE * 10)

Snake_body = []
velocityX = 0
velocityY = 0
Game_over = False
score = 0

def change_diraction(e): #e = event
    
    global velocityX, velocityY

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down"  and velocityY != -1):
        velocityX = 0  
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right"  and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global Snake, Snake_body, Food, Game_over, score

    if (Game_over):
        return
    if (Snake.x < 0 or Snake.x >= window_width or Snake.y < 0 or Snake.y >= window_height):
        Game_over = True
        return
    for tile in Snake_body:
        if (Snake.x == tile.x and Snake.y == tile.y):
            Game_over = True
            return   

    #collisions
    if (Snake.x == Food.x and Snake.y == Food.y):
        Snake_body.append(Tile(Food.x, Food.y))
        Food.x = random.randint(0, COLS-1) * TILE_SIZE
        Food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    #update snake body
    for i in range(len(Snake_body)-1, -1, -1):
        tile = Snake_body[i]
        if (i == 0):
            tile.x = Snake.x 
            tile.y = Snake.y
        else:
            prev_tile = Snake_body[i-1] 
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    Snake.x += velocityX * TILE_SIZE
    Snake.y += velocityY * TILE_SIZE



def draw():
    global Snake, Snake_body, Food, Game_over, score

    move()

    canvas.delete("all")

    #draw food
    canvas.create_rectangle(Food.x, Food.y, Food.x + TILE_SIZE, Food.y + TILE_SIZE, fill = "red")


    #draw snake
    canvas.create_rectangle(Snake.x, Snake.y, Snake.x + TILE_SIZE, Snake.y + TILE_SIZE, fill = "lime green")

    #snake body
    for tile in Snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "lime green")

    if(Game_over):
        canvas.create_text(window_width/2, window_height/2, font= "Arial 20", text= f" Game Over: {score}", fill = "white")
    else:
        canvas.create_text(30, 20, font= "Arial 10", text= f"Score: {score}", fill="white")

    window.after(100, draw) #100ms = 1/10 second, frame/second

draw()

window.bind("<KeyRelease>", change_diraction)


window.mainloop()
