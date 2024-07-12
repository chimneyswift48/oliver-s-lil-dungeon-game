"""
graphics engine for 2D games
"""
import os
import numpy as np
import cv2
from game import start_game, move_player, update1, update2, create_bullets

from pygame import mixer

mixer.init()
mixer.music.load("Dungeon Quest.mp3")
mixer.music.play(loops=-1)
img = cv2.imread("title.png")

img[-100:] = 0  # last 100 pixel rows are black
img = cv2.putText(
    img,
    "press any key to start",
    org=(15, 990),  # x/y position of the text
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=2,
    color=(255, 255, 255),  # white
    thickness=3,
)

cv2.imshow("Cutscene", img)
cv2.waitKey(0)

# title of the game window
GAME_TITLE = "Dungeon Explorer"

# map keyboard keys to move commands
MOVES = {
    "a": "left",
    "d": "right",
    "w": "up",
    "s": "down",
    "x": "cheat"
}

BULLET_MOVES = {
    2: "left",
    3: "right",
    0: "up",
    1: "down",
}

#
# constants measured in pixels
#
SCREEN_SIZE_X, SCREEN_SIZE_Y = 970, 940
TILE_SIZE = 64


def read_image(filename: str) -> np.ndarray:
    """
    Reads an image from the given filename and doubles its size.
    If the image file does not exist, an error is created.
    """
    img = cv2.imread(filename)  # sometimes returns None
    if img is None:
        raise IOError(f"Image not found: '{filename}'")
    img = np.kron(img, np.ones((2, 2, 1), dtype=img.dtype))  # double image size
    return img


def read_images():
    return {
        filename[:-4]: read_image(os.path.join("tiles", filename))
        for filename in os.listdir("tiles")
        if filename.endswith(".png")
    }


def draw_tile(frame, x, y, image, xbase=0, ybase=0):
    # calculate screen position in pixels
    xpos = xbase + x * TILE_SIZE
    ypos = ybase + y * TILE_SIZE
    # copy the image to the screen
    frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = image


SYMBOLS={
    ".": "floor",
    "#": "wall",
    "x": "stairs_down",
    "X": "stairs_up",
    "$": "chest",
    "f": "fountain",
    "c": "coin",
    "t": "trap",
    "k": "key",
    "D": "closed_door",
    "d": "open_door",
    "e": "eye",
    "E": "eye",
    "ẽ": "eye",
    "w": "water",
    "h": "heart",
    "v": "black",
    "b": "bullet",
    "s": "sewer"
    }

def draw(game, images):
    # initialize screen
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)
    # draw dungeon tiles
    for y, row in enumerate(game.current_level.level):
        for x, tile in enumerate(row):
            draw_tile(frame, x=x, y=y, image=images[SYMBOLS[tile]])
            

    # draw player
    draw_tile(frame, x=game.x, y=game.y, image=images["player"])
    
    #draw coin symbol
    draw_tile(frame, x=0, y=0, image=images["coin"],xbase=650,ybase=35)
    
    #draw bullets symbol
    if game.with_bullets == True and game.level_number==2:
        draw_tile(frame, x=0, y=0, image=images["bullet"],xbase=640,ybase=435)
    
    # draw text
    cv2.putText(frame,
            str(game.coins),
            org=(730, 78),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.5,
            color=(255, 128, 128),
            thickness=3,
            )
    
    if game.with_bullets==True and game.level_number==2:
        cv2.putText(frame,
            str("press arrow keys"),
            org=(730, 450),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.8,
            color=(255, 128, 128),
            thickness=2,
            )
    if game.with_bullets==True and game.level_number==2:
        cv2.putText(frame,
            str("to shoot"),
            org=(730, 485),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.8,
            color=(255, 128, 128),
            thickness=2,
            )
    
    #draw hearts
    for i in range(game.health):
        y = i // 4  # floor division: rounded down
        x = i % 4   # modulo: remainder of an integer division
        draw_tile(frame, xbase=640, ybase=100, x=x, y=y, image=images["heart"])
        
    #draw items
    for i, item in enumerate(game.items):
        y = i // 2  # floor division: rounded down
        x = i % 2   # modulo: remainder of an integer division
        draw_tile(frame, xbase=640, ybase=300, x=x, y=y, image=images[item])
    
    Elements=[
        [game.current_level.fireballs, "fireball"],
        [game.current_level.rats, "rat"],
        [game.current_level.skeletons, "skeleton"]
    ]
    for monsters,imagename in Elements:
        for t in monsters:
            draw_tile(frame, x=t.x, y=t.y, image=images[imagename])
            
    # draw bullets
    for t in game.bullets:
        if t.active==True:
            draw_tile(frame, x=t.x, y=t.y, image=images["bullet"])
            
    
    # display complete image
    cv2.imshow(GAME_TITLE, frame)


def handle_keyboard(game):
    """keys are mapped to move commands"""
    code=(cv2.waitKey(1) & 0xFF)
    key = chr (code)
    if key == "q":
        game.status = "exited"
    if key in MOVES:
        move_player(game, MOVES[key])
    if code in BULLET_MOVES:
        create_bullets(game, BULLET_MOVES[code])
        

# game starts
images = read_images()
game = start_game()
cheat_mode=False
with_bullets=False
counter = 0
while game.status == "running":
    counter += 1

    draw(game, images)
    if counter % 20 == 0:
        update1(game)
    if counter % 45 == 0:
        update2(game)
    handle_keyboard(game)

mixer.music.stop()
cv2.destroyAllWindows()