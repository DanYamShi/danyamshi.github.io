import numpy as np
import os, time, msvcrt, math, random, pygame, sys
from random import randint
from pygame.locals import *
import Pokemon_Battle

FPS = 30                    # frames per second to update the screen
WINWIDTH = 640              # width of the program's window, in pixels
WINHEIGHT = 480             # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
BACKGROUND = (0, 0, 0)      #black
CAMERASLACK = 0             # how far from the center the squirrel moves before moving the camera
MOVERATE = 30                # how fast the player moves
SIZE = 30


# MAPS AND OBJECTS
#------------------------------------------
# 0 - floor
# '' -  black block (no message)
# 1 - transparent block (no message)
# 2,3 - exits
# 4 and over - objects (messages)
# 100 and over - interactable players
# https://onlinepngtools.com/resize-png to resize

#map of second floor of player house (7x9)
m_1 = np.array([['',2,0,0,4,5,6,7,8], 
                [0,0,0,0,18,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,9,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,10,0,0,0,0,0,0,12],
                [0,11,0,0,0,0,0,0,13]])

#map of first floor of player house (9x11)
m_3 = np.array([[1,2,0,0,3,3,1,7,7,8,9], 
                [0,0,0,0,0,0,1,0,0,0,0],
                [0,0,0,0,0,0,1,1,0,0,1],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,101,1,1,0,0,0],
                [0,0,0,0,0,0,1,1,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
                [1,0,0,100,0,0,0,0,0,0,1],
                [1,1,2,1,1,1,1,1,1,1,1]])

m_2 = np.array([['',2,0,0,7,8,21,14,15,16,17], 
                [0,0,0,0,0,0,1,0,0,0,0],
                [0,0,0,0,0,0,1,1,0,0,1],
                [0,0,0,0,22,0,0,0,0,0,0],
                [0,0,0,0,0,1001,20,1,18,0,0],
                [0,0,0,0,0,18,1,1,18,0,0],
                [12,0,0,0,0,0,0,0,0,0,12],
                [13,19,0,1002,0,0,0,0,0,0,13],
                ['','',3,'','','','','','','','']])

#test map (9x11)
test = np.array([['',0 ,'',0 ,0 ,0 ,'',0 ,0 ,0 ,''], 
                 ['',0 ,'',0 ,'',0 ,'',0 ,'',0 ,''],
                 ['',0 ,'',0 ,'',0 ,0 ,0 ,'',0 ,''],
                 ['',0 ,'',0 ,'','','','','',0 ,''],
                 ['',0 ,'',0 ,'',0 ,0 ,0 ,0 ,0 ,''],
                 ['',0 ,'',0 ,'',0 ,0 ,0 ,0 ,0 ,''],
                 ['',0 ,'',0 ,'',0 ,0 ,0 ,0 ,0 ,''],
                 ['',0 ,0 ,0 ,'',0 ,0 ,0 ,0 ,0 ,''],
                 ['','','','','','','','','','','']])

#list of all maps [map, floor index in FLOORIMAGES]
map_lays = [[m_1, 0], [m_2, 1]] 

#dict of object descriptions
d_1 = {4 : "This is a gaming laptop.", 6 : "This is a Wii.", 
       7 : "This is a TV.", 8 : "This is a TV.", 11 : "A  warm bed.",
       14 : "Ouch! That's hot!", 15 : "Ouch! That's hot!", 16 : "Empty, except a half-finished bottle of vodka.",
       17 : "A layer of dust covers the bookshelf.", 1001 : "Mom: Hello.", 
       1002 : ["battle", "True Blue", "True Blue: Boundless!", 2, "True Blue: You are BOUNDLESS!!!", 3]} 

#list of all the object description dictionaries for each map in map_lays
item_descript_lays = [d_1, d_1] 

#dict of winning dialogue
post_battle_msg = {1002 : ["\nTrue Blue: Well done! You truly enbody\nthe UofT spirit!\n", "True Blue: Good luck with your studies!"]}

#dict of replacement dialogue (cannot challenge the most trainers twice)
replace_battle_msg = {1002 : "True Blue: You've already beaten me!"}

# checkpoint/respawn point
checkpoint_row = 3; checkpoint_col = 4; checkpoint_map_num = 0

##What about exp and money?


# MAIN FUNCTIONS
#------------------------------------------
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, PLAYER_LEFT_IMAGES, PLAYER_RIGHT_IMAGES, PLAYER_FRONT_IMAGES, PLAYER_BACK_IMAGES, FLOORIMAGES, ITEMIMAGES, NPCIMAGES, p_name
    
    p_name = 'Daniel'
    with open("Pokemon_Global.txt","w") as file:
        file.write(p_name+'\n') 

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('icon.png'))
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Pokemon')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    # load the image files
    PLAYER_LEFT_IMAGES = []
    PLAYER_RIGHT_IMAGES = []
    PLAYER_FRONT_IMAGES = []
    PLAYER_BACK_IMAGES = []
    FLOORIMAGES = []
    ITEMIMAGES = []
    NPCIMAGES = []
    for i in range(1, 4):
        PLAYER_LEFT_IMAGES.append(pygame.transform.scale(pygame.image.load('left%s.png' % i), (32, 32)))
        PLAYER_RIGHT_IMAGES.append(pygame.transform.scale(pygame.image.load('right%s.png' % i), (32, 32)))
        PLAYER_FRONT_IMAGES.append(pygame.transform.scale(pygame.image.load('front%s.png' % i), (32, 32)))
        PLAYER_BACK_IMAGES.append(pygame.transform.scale(pygame.image.load('back%s.png' % i), (32, 32)))
    
    for i in range(1, 3):
        FLOORIMAGES.append(pygame.transform.scale(pygame.image.load('floor%s.png' % i), (SIZE, SIZE)))
        
    for i in range(1, 23):
        ITEMIMAGES.append(pygame.image.load('item%s.png' % i))
        
    for i in range(1,3):
        NPCIMAGES.append(pygame.image.load('npc%s.png' % i))

    while True:
        starting_map_num = 0 
        starting_position = [3,4]
        playerObj = {'surface': PLAYER_FRONT_IMAGES[0], 'size': SIZE,
                     'x': HALF_WINWIDTH, 'y': HALF_WINHEIGHT} 
        
        runGame(playerObj, starting_map_num, starting_position)


def runGame(playerObj, map_num, position, previous_team = []):
    current_map = map_lays[map_num][0]
    floor_index = map_lays[map_num][1]
    map_height = len(current_map)
    map_width = len(current_map[0])   
    
    camerax = 0          # camerax and cameray are the top left of where the camera view is
    cameray = 0
    floorObjs = []       # stores the floor plan
    mapObjs = []         # stores all the items in the map     
    npcObjs = []         # stores all the npc's on the map  
    
    # 15 units border
    width_adjust = HALF_WINWIDTH - SIZE*(position[0]+1)
    height_adjust = HALF_WINHEIGHT - SIZE*(position[1]-1)
    
    count = 0
    for height in range(map_height):
        for width in range(map_width):
            if current_map[height][width] != '': #check if not inside wall
                floorObjs.append(makeNew(camerax, cameray, FLOORIMAGES[floor_index]))
                floorObjs[count]['x'] = SIZE*width + width_adjust
                floorObjs[count]['y'] = SIZE*height + height_adjust
                count += 1

    # create map and npc items       
    count_a = 0
    count_b = 0
    for height in range(len(current_map)):
        for width in range(len(current_map[0])):
            if current_map[height][width] != '' and int(current_map[height][width]) != 0: #check if not inside wall and not floor
                item_index = int(current_map[height][width])-1
                if item_index < 1000:
                    mapObjs.append(makeNew(camerax, cameray, ITEMIMAGES[item_index]))
                    mapObjs[count_a]['x'] = SIZE*width + width_adjust
                    mapObjs[count_a]['y'] = SIZE*height + height_adjust
                    count_a += 1
                else:
                    npcObjs.append(makeNew(camerax, cameray, NPCIMAGES[item_index-1000]))
                    npcObjs[count_b]['x'] = SIZE*width + width_adjust
                    npcObjs[count_b]['y'] = SIZE*height + height_adjust     
                    count_b += 1
    
    # main game loop
    while True: 
        # adjust camerax and cameray if beyond the "camera slack" (???)
        playerCenterx = playerObj['x'] + int(playerObj['size'] / 2)
        playerCentery = playerObj['y'] + int(playerObj['size'] / 2)
        if (camerax + HALF_WINWIDTH) - playerCenterx > CAMERASLACK:
            camerax = playerCenterx + CAMERASLACK - HALF_WINWIDTH
        elif playerCenterx - (camerax + HALF_WINWIDTH) > CAMERASLACK:
            camerax = playerCenterx - CAMERASLACK - HALF_WINWIDTH
        if (cameray + HALF_WINHEIGHT) - playerCentery > CAMERASLACK:
            cameray = playerCentery + CAMERASLACK - HALF_WINHEIGHT
        elif playerCentery - (cameray + HALF_WINHEIGHT) > CAMERASLACK:
            cameray = playerCentery - CAMERASLACK - HALF_WINHEIGHT

        # display the black background
        DISPLAYSURF.fill(BACKGROUND)

        # display the floor
        for tile in floorObjs:
            tileRect = pygame.Rect( (tile['x'] - camerax, tile['y'] - cameray, tile['width'], tile['height']) )
            DISPLAYSURF.blit(tile['Image'], tileRect)


        # display the map items
        for item in mapObjs:
            itemRect = pygame.Rect( (item['x'] - camerax, item['y'] - cameray, item['width'], item['height']) )
            DISPLAYSURF.blit(item['Image'], itemRect)
            
        # display the npc's
        for npc in npcObjs:
            npcRect = pygame.Rect( (npc['x'] - camerax, npc['y'] - cameray, npc['width'], npc['height']) )
            DISPLAYSURF.blit(npc['Image'], npcRect)        

        # display the player 
        playerObj['rect'] = pygame.Rect( (playerObj['x'] - camerax, playerObj['y'] - cameray, playerObj['size'], playerObj['size']) )
        DISPLAYSURF.blit(playerObj['surface'], playerObj['rect'])
        
        position = step(playerObj, position, map_num, previous_team) #move player      


# SUPPORTING FUNCTIONS
#------------------------------------------
def step(playerObj, position, map_num, previous_team):
    step = ''
    p_row, p_col = position    
    current_map = map_lays[map_num][0]
    map_height = len(current_map)
    map_width = len(current_map[0])    
    
    # move the player  
    for event in pygame.event.get():        
        if event.type == KEYDOWN:              
            if event.key in (K_UP, K_w) and (p_row - 1) >= 0 and current_map[p_row-1][p_col] != '': # check if exceeds upper boundary
                step = 'up'
                p_row -= 1
                playerObj['surface'] = PLAYER_BACK_IMAGES[1]
                
            elif event.key in (K_DOWN, K_s) and (p_row + 1) < map_height and current_map[p_row+1][p_col] != '': # check if exceeds lower boundary
                step = 'down'
                p_row += 1
                playerObj['surface'] = PLAYER_FRONT_IMAGES[1]
                
            elif event.key in (K_LEFT, K_a) and (p_col - 1) >= 0 and current_map[p_row][p_col-1] != '': # check if exceeds left boundary
                step = 'left'
                p_col -= 1
                playerObj['surface'] = PLAYER_LEFT_IMAGES[1]
                                
            elif event.key in (K_RIGHT, K_d) and (p_col + 1) < map_width and current_map[p_row][p_col+1] != '': # check if exceeds right boundary
                step = 'right'
                p_col += 1
                playerObj['surface'] = PLAYER_RIGHT_IMAGES[1]
            
        elif event.type == KEYUP:
            if event.key in (K_LEFT, K_a):
                playerObj['surface'] = PLAYER_LEFT_IMAGES[0]
            elif event.key in (K_RIGHT, K_d):
                playerObj['surface'] = PLAYER_RIGHT_IMAGES[0]
            elif event.key in (K_UP, K_w):
                playerObj['surface'] = PLAYER_BACK_IMAGES[0]
            elif event.key in (K_DOWN, K_s):
                playerObj['surface'] = PLAYER_FRONT_IMAGES[0]

            elif event.key == K_ESCAPE:
                terminate()      
    
    # print message and begin battle if applicable
    if step != '':
        map_value = int(current_map[p_row][p_col])
        position = [p_row, p_col]
        change_map(playerObj, position, map_num, map_value, step, previous_team) #check if map changes     
        
        if map_value in [1,2,3,5,12,13,20]: #check for obstacles w/o msg
            if step == 'up':
                p_row += 1
            elif step == 'down':
                p_row -= 1
            elif step == 'left':
                p_col += 1
            elif step == 'right':
                p_col -= 1            
            step = ''
        
        for key in item_descript_lays[map_num]: #check for obstacle msg
            if map_value == key:
                msg = item_descript_lays[map_num][map_value]
                
                if step == 'up':
                    p_row += 1
                elif step == 'down':
                    p_row -= 1
                elif step == 'left':
                    p_col += 1
                elif step == 'right':
                    p_col -= 1
                step = ''
                
                if 'battle' not in msg: # check if no battle
                    print('\n'+msg)
                else:
                    print('\n'+msg[2])
                    time.sleep(msg[3]) 
                    
                    p = map_value # p is a convenient placeholder to use in opponents dict in Pokemon_Battle.py
                    winner, previous_team = Pokemon_Battle.battle_main(p, previous_team, msg) # process battle
                    
                    if winner == 'user': # check if player won battle
                        post_msg = post_battle_msg[map_value]
                        for x in post_msg:
                            print(x)
                            time.sleep(3)
                        
                        item_descript_lays[map_num][map_value] = replace_battle_msg[map_value]
                        
                    else:
                        position = [checkpoint_row, checkpoint_col] # relocate to checkpoint
                        playerObj = {'surface': PLAYER_FRONT_IMAGES[0], 'size': SIZE,
                                     'x': HALF_WINWIDTH, 'y': HALF_WINHEIGHT} 
                        
                        return runGame(playerObj, checkpoint_map_num, position) # wipe battle history, previous_team = []  
                
    # actually move the player 
    if step == 'left':
        for num in range(MOVERATE):
            playerObj['x'] -= 1
    elif step == 'right':
        for num in range(MOVERATE):
            playerObj['x'] += 1
    elif step == 'up':
        for num in range(MOVERATE):
            playerObj['y'] -= 1
    elif step == 'down':
        for num in range(MOVERATE):
            playerObj['y'] += 1
    
    pygame.display.update()
    FPSCLOCK.tick(FPS)  
    position = [p_row, p_col]
    
    return position 
    
    
def change_map(playerObj, position, map_num, map_value, step, previous_team):
    map_num_new = map_num
    p_row, p_col = position
    
    if map_value in [2,3]:
        if map_num == 0: #check if map is player house second floor
            if step == 'left':
                p_row_new = 0; p_col_new = 2; map_num_new = 1
                
            ##What about the animation for mom when player comes down for the first time?
            
        elif map_num == 1: #check if map is player house first floor
            if step == 'left': #check if location is staircase
                p_row_new = 0; p_col_new = 2; map_num_new = 0
            elif step == 'down': #check if location is door to outside
                p_row_new = 0; p_col_new = 2; map_num_new = 1
                print("\nNot programmed.\n") 
                
                ##What happens if player wants to leave house?
        
        if map_num != map_num_new:
            playerObj['x'] = HALF_WINWIDTH + (p_col_new - p_col)*SIZE
            playerObj['y'] = HALF_WINHEIGHT + (p_row_new - p_row - 1)*SIZE
            position = [p_row_new, p_col_new]
            
            return runGame(playerObj, map_num_new, position, previous_team)

def terminate():
    pygame.quit()
    sys.exit()

def makeNew(camerax, cameray, image):
    gr = {}
    gr['Image'] = image
    gr['width'] = image.get_width()
    gr['height'] = image.get_height()
    gr['rect'] = pygame.Rect( (gr['width'], gr['height'], gr['width'], gr['height']) )
    return gr

if __name__ == '__main__':
    main()