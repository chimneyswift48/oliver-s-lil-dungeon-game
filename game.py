"""
the Dungeon Explorer game logic
"""
from pydantic import BaseModel
import random

class Fireball(BaseModel):
    x: int
    y: int
    direction:str = "up"
    
class Bullet(BaseModel):
    x: int
    y: int
    direction:str
    active: bool = True
    
class Skeleton(BaseModel):
    x: int
    y: int
    direction:str = "down"
    
class Rat(BaseModel):
    x: int
    y: int
    direction:str = "right"
    
class Level(BaseModel):
    level: list[list[str]]
    fireballs: list[Fireball] = []
    rats: list[Rat] = []
    skeletons: list[Skeleton] = []

class DungeonGame(BaseModel):
    status: str = "running"
    x: int
    y: int
    coins: int = 0
    health: int = 3
    items: list[str] = []
    current_level:Level
    level_number: int=0
    cheat_mode:bool = False
    with_bullets:bool= False
    bullets: list [Bullet] =[]

def parse_level (level):
    return [list(row) for row in level]

LEVEL_ONE = Level(
    level=parse_level([
        "k#####....",
        "..........",
        ".#######D#",
        ".c#...t#k.",
        ".##.t..##e",
        "....#t.##.",
        "#####f.D..",
        "....####D#",
        "..#......#",
        "x.....cc##",
    ]),
    fireballs=[
        Fireball(x=0, y=5)],
    rats=[
        Rat(x=4, y=1)],
)

LEVEL_TWO = Level(
    level=parse_level([
        "wwwwwwwwww",
        "wwwwwwwwww",
        "wwwwwwwwww",
        "wwwwwwwwww",
        "wwwwwwwwww",
        "wwwwwwwwww",
        "wwwwwwwwww", 
        "wwwwwwwwww",
        "wwwwwwwwww",
        "X........w",
        "w.wwwwww.w",
        "wDwwwwww.w",
        "w.ẽwE...ew",
        "wwwwwwwwww",
    ]),
)

LEVEL_THREE = Level(
    level=parse_level([
        "vvvwwXwwvv",
        "vvvww.wwvv",
        "vvvww.wwvv",
        "vvvww.wwvv",
        "vvvwwbwwvv",
        "vvvww.wwvv",
        "vvvwwwwwvv",
        "vvvwwwwwvv",
        "vvvwwwwwvv",
        "vvvwwwwwvv",
        "vvvwwwwwvv",
        "vvvwwwwwvv",
        "vvvwwwwwvv",
        "vvvxwwwwvv",
    ]),
)

LEVEL_FOUR = Level(
    level=parse_level([
        "##..k...##vvvv",
        "#...tt...#vvvv",
        "..........vvvv",
        ".tt....tt.vvve",
        ".ttt...kt.vvv.",
        "........t.vvvs",
        "wwwwwwww##www.",
        "wwwwwwww#.wwww",
        "wwwwwwww#.www.",
        "wwwwwwww#.wwww",
        "wwwwwwww#.ww#.",
        "#########.ww#.",
        "..........ww#.",
        "...X.hh...ww#.",
    ]),
    rats=[
        Rat(x=13, y=12,direction= "up")],
    skeletons=[
        Skeleton(x=6,y=2),Skeleton(x=2,y=2),Skeleton(x=1,y=1),Skeleton(x=6,y=2),Skeleton(x=6,y=2),Skeleton(x=6,y=2),Skeleton(x=6,y=2),Skeleton(x=6,y=2),Skeleton(x=6,y=2),Skeleton(x=7,y=2),Skeleton(x=3,y=5),Skeleton(x=4,y=5),Skeleton(x=5,y=5)]
    
)

LEVELS = [LEVEL_ONE, LEVEL_TWO,LEVEL_THREE,LEVEL_FOUR]

SWITCH_1=[
    [9,1,"f"],
    [9,8,"f"],
    [12,1,"f"],
    [12,8,"f"],
    [10,4,"h"],
    [11,5,"h"],
    [0,4,"."],
    [0,5,"x"],
    ]


def get_next_position1(x, y, direction):
    if direction == "right" and x < 9:
        x += 1
    elif direction == "left" and x > 0:
        x -= 1
    elif direction == "up" and y > 0:
        y -= 1
    elif direction == "down" and y < 9:
        y += 1
    return x, y

def get_next_position2(x, y, direction):
    if direction == "right" and x < 9:
        x += 1
    elif direction == "left" and x > 0:
        x -= 1
    elif direction == "up" and y > 0:
        y -= 1
    elif direction == "down" and y < 13:
        y += 1
    return x, y

def get_next_position3(x, y, direction):
    if direction == "right" and x < 13:
        x += 1
    elif direction == "left" and x > 0:
        x -= 1
    elif direction == "up" and y > 0:
        y -= 1
    elif direction == "down" and y < 13:
        y += 1
    return x, y

def move_player(game, direction: str) -> None:
    """Things that happen when the player walks on stuff"""
    if direction == "cheat":
        game.level_number += 1
        game.cheat_mode= True
        if game.level_number < len(LEVELS):
            # move to next level
            game.current_level = LEVELS[game.level_number]
        else:
            # no more levels left
            game.status = "finished"
    
    if game.level_number ==0:
        new_x, new_y = get_next_position1(game.x, game.y, direction)
    elif game.level_number ==3:
        new_x, new_y = get_next_position3(game.x, game.y, direction)
    else:
        new_x, new_y = get_next_position2(game.x, game.y, direction)
    
    canBeWalkedOn = ".x$ctkdeEẽhb"
    if game.current_level.level[new_y][new_x] in canBeWalkedOn or game.cheat_mode==True:
        if game.current_level.level[new_y][new_x] == "c":
            game.current_level.level[new_y][new_x] = "."
            game.coins += 1
        if game.current_level.level[new_y][new_x] == "t":
            game.health -= 1
        if game.current_level.level[new_y][new_x] == "h":
            game.current_level.level[new_y][new_x] = "."
            game.health += 1
        if game.current_level.level[new_y][new_x] == "b":
            game.current_level.level[new_y][new_x] = "."
            game.with_bullets = True
        if game.current_level.level[new_y][new_x] == "x":
            game.level_number += 1
            if game.level_number < len(LEVELS):
                # move to next level
                game.current_level = LEVELS[game.level_number]
            else:
                # no more levels left
                game.status = "finished"
        if game.current_level.level[new_y][new_x] == "k":
            game.items.append("key")
            game.current_level.level[new_y][new_x] = "."
        
        
        if game.level_number== 0 and game.current_level.level[new_y][new_x] == "e":
            game.current_level.level[new_y][new_x] = "."
            for x in range(3,9):
                game.current_level.level[8][x] = "t"
            game.current_level.level[6][0] = "."
            game.current_level.level[3][4] = "t"
        if game.level_number== 1 and game.current_level.level[new_y][new_x] == "e":
            game.current_level.level[new_y][new_x] = "."
            for x in range(1,9):
                for y in range(1,8):
                    game.current_level.level[y][x] = "."
            game.current_level.level[3][2] = "t"
            game.current_level.level[3][3] = "t"
            game.current_level.level[3][6] = "t"
            game.current_level.level[3][7] = "t"
            game.current_level.level[5][4] = "t"
            game.current_level.level[5][5] = "t" 
        if game.level_number== 1 and game.current_level.level[new_y][new_x] == "E":  
            game.current_level.level[new_y][new_x] = "."
            game.current_level.level[8][4] = "." 
            game.current_level.level[8][5] = "."
            game.current_level.level[1][1] = "k"
            game.current_level.level[1][8] = "h"
            game.current_level.level[7][1] = "c"
            game.current_level.level[7][8] = "c"
            game.current_level.fireballs=[Fireball(x=1,y=1),Fireball(x=8,y=1)]
            game.current_level.skeletons=[Skeleton(x=4,y=3),Skeleton(x=5,y=3)]
        if game.level_number== 1 and game.current_level.level[new_y][new_x] == "ẽ":
            game.current_level.level[new_y][new_x] = "."
            game.current_level.level[12][3] = "."
            for x in range(1,8):
                for y in range(10,12):
                    game.current_level.level[y][x] = "."
            
            for x,y,tiles in SWITCH_1:
                game.current_level.level[x][y]=tiles

            game.current_level.rats=[Rat(x=3,y=1),Rat(x=5,y=4)]
            
        game.x = new_x
        game.y = new_y   
    if "key" in game.items and game.current_level.level[new_y][new_x] == "D":  # check whether there is a door
        game.items.remove("key")     # key can be used once
        game.current_level.level[new_y][new_x] = "d" # replace the closed door by an open one         
            
def start_game():
    return DungeonGame(
        x=8,
        y=1,
        current_level=LEVEL_ONE)

def move_fireballs(game):
    for f in game.current_level.fireballs:
        new_x, new_y = get_next_position1(f.x, f.y, f.direction)
        if game.current_level.level[new_y][new_x] in ".€kch":  # flies over coins and keys
            f.x, f.y = new_x, new_y
        
        if game.current_level.level[new_y][new_x] in "#" or \
            game.current_level.level[new_y][new_x] in "w" or \
            game.current_level.level[new_y][new_x] in "k" or \
            game.current_level.level[new_y][new_x] in "c" or \
            game.current_level.level[new_y][new_x] in "h" or \
            game.current_level.level[new_y][new_x] in "x" or new_y==0:  # check whether there is a wall
            if f.direction =="up":
                f.direction ="down"
            elif f.direction =="down":
                f.direction = "up"

def move_rats(game):
    for f in game.current_level.rats:
        if game.level_number==3:
            new_x, new_y = get_next_position3(f.x, f.y, f.direction)
        else:
            new_x, new_y = get_next_position1(f.x, f.y, f.direction)

        if game.current_level.level[new_y][new_x] in ".€khcse":  # flies over coins and keys
            f.x, f.y = new_x, new_y
        
        if game.level_number< 3:
            if game.current_level.level[new_y][new_x] in "#wx" or \
                new_x==0 or new_x == 9:  # check whether there is a wall
                if f.direction =="right":
                    f.direction ="left"
                elif f.direction =="left":
                    f.direction = "right"
                elif f.direction =="up":
                    f.direction ="down"
                elif f.direction =="down":
                    f.direction = "up"
        else:
            if game.current_level.level[new_y][new_x] in "#xw" or \
                new_y==0 or new_y == 13:
                    # check whether there is a wall
                if f.direction =="right":
                    f.direction ="left"
                elif f.direction =="left":
                    f.direction = "right"
                elif f.direction =="up":
                    f.direction ="down"
                elif f.direction =="down":
                    f.direction = "up"
                    
            if game.current_level.level[new_y][new_x] == "e":
                game.current_level.level[new_y][new_x] == "."
                for x in range(0,10):
                    for y in range(6,12):
                        game.current_level.level[y][x] = "."
                game.current_level.level[10][13] = "D"
                game.current_level.level[12][13] = "D"
                game.current_level.level[13][13] = "x"
                
                
def create_bullets(game, direction): 
    if game.with_bullets==True:
        bullets=Bullet(x=game.x, y=game.y, direction=direction)
        game.bullets.append(bullets)
                
def move_bullets(game):
    for f in game.bullets:
        if game.level_number ==3:
            new_x, new_y = get_next_position3(f.x, f.y, f.direction)
        else:
            new_x, new_y = get_next_position2(f.x, f.y, f.direction)
        # flies over coins and keys
        if game.current_level.level[new_y][new_x] in ".€kchw":
            f.x, f.y = new_x, new_y

        if game.current_level.level[new_y][new_x] in "w":
            game.current_level.level[new_y][new_x]="."
            
        if game.current_level.level[new_y][new_x] in "#kchxvt" or \
            new_y==0 or new_y==13 or new_x==13 or new_x==0:
            f.active=False
        

def move_skeletons(game):
    for f in game.current_level.skeletons:
        new_x, new_y = get_next_position1(f.x, f.y, f.direction)
        while new_y==9:
            new_y-=1
        if game.current_level.level[new_y][new_x] in ".€kthc":  # flies over coins and keys
            f.x, f.y = new_x, new_y
        
        #if game.current_level.level[new_y][new_x] in "#" or \
            #game.current_level.level[new_y][new_x] in "w" or \
            #game.current_level.level[new_y][new_x] in "t" or \
            #game.current_level.level[new_y][new_x] in "x" or new_y!=0:  # check whether there is a wall
        f.direction = random.choice(["up", "down", "left", "right"])

def update1(game):
    # health check
    if game.health <= 0:
        game.status = "game over"
    
    move_fireballs(game)
    move_bullets(game)
    move_skeletons(game)
    check_collision1(game)
    
def update2(game):
    move_rats(game)
    check_collision2(game)            

def check_collision1(game):
    for f in game.current_level.fireballs:
        if f.x == game.x and f.y == game.y:
            game.health -= 1
    
    for f in game.current_level.skeletons:
        if f.x == game.x and f.y == game.y:
            game.health -= 1

def check_collision2(game):            
    for t in game.current_level.rats:
        if t.x == game.x and t.y == game.y:
            game.health -= 1
    