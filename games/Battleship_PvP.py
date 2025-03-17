from random import randint
import os
import msvcrt 
from termcolor import colored 
from colorama import init 
import time
  
init() # initiate colouring

single_row_1 = []; single_row_2 = []; single_row_3 = []; single_row_4 = []
matrix_1 = []; matrix_2 = []; matrix_3 = []; matrix_4 = []

for column in range(10): #create 1 row of 10 columns
    single_row_1.append(0)
    single_row_2.append(0)
    single_row_3.append(0)
    single_row_4.append(0)
for row in range(10): #create 10 rows of 10 columns
    matrix_1.append(single_row_1[:])
    matrix_2.append(single_row_2[:])
    matrix_3.append(single_row_3[:])
    matrix_4.append(single_row_4[:])

user_1_map = matrix_1[:] #create specific and unique matrices
user_2_map = matrix_2[:]
hidden_user_1_map = matrix_3[:] 
hidden_user_2_map = matrix_4[:] 

row_labels = [colored('A', 'yellow'), colored('B', 'yellow'), colored('C', 'yellow'), colored('D', 'yellow'), colored('E', 'yellow'), 
              colored('F', 'yellow'), colored('G', 'yellow'), colored('H', 'yellow'), colored('I', 'yellow'), colored('J', 'yellow')]

column_labels = [colored('1', 'yellow'), colored('2', 'yellow'), colored('3', 'yellow'), colored('4', 'yellow'), colored('5', 'yellow'), 
                 colored('6', 'yellow'), colored('7', 'yellow'), colored('8', 'yellow'), colored('9', 'yellow'), colored('10', 'yellow')]

dict_row = {"A" : 1, "B" : 2, #dict of alpha-numerical coordinates
            "C" : 3, "D" : 4,
            "E" : 5, "F" : 6,
            "G" : 7, "H" : 8,
            "I" : 9, "J" : 10}   

dict_orient = {"b'M'" : "RIGHT","b'K'" : "LEFT","b'H'" : "UP","b'P'" : "DOWN"} #dict of keyboard inputs/outputs

# COORDINATES PROCESSING
#------------------------------------------
def coordinates():
    iteration = 0 #set loop count to 0
    while True:
        try:
            if iteration > 0: #check if loop performed more than once
                print("Invalid coordinates, please try again.")
            
            iteration += 1
            coord = input("Coordinates (A-J, 1-10) (i.e G7): ")
            
            if len(coord) > 1: #check if coord has two or more characters
                A = str.upper(coord[0]); B = int(coord[1:]) #separate into row (A) and column (B)
                
                if A == "D" and B == 1111: #cheat
                    print_map(AI_map)
                
                for key in dict_row: #convert A to numerical row number
                    if A == key:
                        A = dict_row[key]  
                        A = A - 1 #convert to index
                        
                        if 0 < B < 11: #check if B is a valid column number
                            B = B - 1 #convert to index
                            return A,B     
        except ValueError: #accept this error and restart loop
            iteration = 0
            print("Invalid coordinates, please try again.")    

# TURNS 
#------------------------------------------
def coin_toss(n):     
    os.system('cls')   
    print("----------------------------------------")
    print("\n G A M E   S T A R T \n")
    print("----------------------------------------")
    coin = str.upper(input("User "+str(n)+", Heads (H) or Tails (T)? ")) #prompt user to input H or T
    toss = randint(0,1) #randomly choose heads (1) or tails (2)
    
    if coin != "H" and coin != "T": #check if input is either T or H
        return coin_toss(n)
    
    os.system('cls')
    if toss == 1:
        result = "H"
        print("\nThe coin is: "+result)     
    elif toss == 0:
        result = "T"
        print("\nThe coin is: "+result)
        
    if coin == result: #check if guess is correct
        print("Good guess!\n")
        print("User "+str(n)+", keep the computer; other User, look away.")
        time.sleep(4)
        return user_turn(n)
    else:
        print("Bad guess.\n")
        if n == 1:
            n = 2
            print("Pass computer to User 2.")
        else:
            n = 1
            print("Pass computer to User 1.")
        time.sleep(3)
        return user_turn(n)  

def user_turn(n):
    print("----------------------------------------")
    print(" U S E R   "+str(n)+"   T U R N")
    print("----------------------------------------\n")
    print("Opponent Map")
    hidden_map(n)
    print("\nYour Map")
    if n == 1:
        print_map(user_1_map)
    else:
        print_map(user_2_map)
    print("")            
    A, B = coordinates() #prompt user to input coordinates
    os.system('cls')
    
    if n == 1:
        location = user_2_map[A][B] #set player chosen coordinate to a variable
        if location == 1: #check if user 2 ship is at coordinate
            user_2_map[A][B] = 2
            print("\nUser 1 hit a ship!\n")
            return turn_decider(n)
        elif location == 0: #check if coordinate is empty
            user_2_map[A][B] = 3
            print("\nUser 1 missed.\n")
            return turn_decider(n)
        else: #check if coordinate has been attempted previously
            print("\nYou have already tried this space, please enter another coordinate.\n")
            return user_turn(n)        
    else:
        location = user_1_map[A][B]
        if location == 1: #check if user 2 ship is at coordinate
            user_1_map[A][B] = 2
            print("\nUser 2 hit a ship!\n")
            return turn_decider(n)
        elif location == 0: #check if coordinate is empty
            user_1_map[A][B] = 3
            print("\nUser 2 missed.\n")
            return turn_decider(n)
        else: #check if coordinate has been attempted previously
            print("\nYou have already tried this space, please enter another coordinate.\n")
            return user_turn(n)          
        
def turn_decider(n):    
    user_1_survive = False #assume both users have not survived
    user_2_survive = False
    
    for a in range(0,10):
        for b in range(0,10):
            if user_1_map[a][b] == 1: #check if there are remaining ships on user 1 map
                user_1_survive = True
                break
                
    for c in range(0,10):
        for d in range(0,10):
            if user_2_map[c][d] == 1: #check if there are remaining ships on user 2 map
                user_2_survive = True
                break
                
    if user_1_survive and user_2_survive: #check if both user and AI have survived
        if n == 1: #change turns
            n = 2
        else:
            n = 1
        print("Pass computer to User "+str(n)+".")
        time.sleep(3)
        return user_turn(n)
    
    os.system('cls')
    if user_1_survive == False:   
        print("Game Finished. User 2 wins!")
    else:  
        print("Game Finished. User 1 wins!")   
        
    print("\nUser 1 Map")
    print_map(user_1_map)
    print("\nUser 2 Map")
    print_map(user_2_map)
    print("")         
        
    answer = str.upper(input("\nPlay Again? (Y or N): "))
    if answer == "Y":
        os.system('cls')
        os.system("start "+"Battleship_PvP.py")
        quit()
    else:
        quit()

# MAKE MAPS
#------------------------------------------
def make_user_map(h,g):
    ships = ["Destroyer (2)", "Submarine (3)", "Cruiser (3)", "Battleship (4)", "Carrier (5)"] #create 5 ships (ship size in brackets)
    user_maps = [user_1_map, user_2_map] #create maps list 
    
    for n in range(h,3): #loop process for user 1 and user 2 originally; will change with h
        for x in range(g,5): #loop process for 5 ships originally; will change with g 
            print("----------------------------------------\n")
            print(" U S E R   "+str(n)+"   M A K E   Y O U R   M A P \n")
            print("----------------------------------------")             
            if n == 1:
                print_map(user_1_map)
            else:
                print_map(user_2_map)
            print("\nEnter the starting location for your "+ships[x]+":")
            A, B = coordinates() #prompt user to input starting coordinates of ship
            
            #create equations to relate ship sequence to ship size: [1->2, 2->3, 3->3, 4->4, 5->5] (d is largest index of ship)
            if x <= 1:
                d = x + 1
            elif x >= 2:
                d = x    
                
            while(user_maps[n-1][A][B] != 0): #check if there is a ship already there
                print("Invalid choice, enter another starting location.")
                A, B = coordinates()
        
            user_maps[n-1][A][B] = 1 #set starting coordinate of ship to 1
            
            if B + d > 9: #check if rest of ship passes over right boundary of map
                right = "" #invalid
            else:
                for y in range(1,d+1): 
                    if user_maps[n-1][A][B+y] != 0: #check if ships overlap
                        right = "" #invalid
                        break
                    else:
                        right = "RIGHT " #right is valid
                
            if B - d < 0: #check if rest of ship passes over left boundary of map
                left = "" #invalid
            else:
                for y in range(1,d+1):
                    if user_maps[n-1][A][B-y] != 0: #check if ships overlap
                        left = "" #invalid
                        break
                    else:
                        left = "LEFT " #left is valid
                        
            if A - d < 0: #check if rest of ship passes over upper boundary of map
                up = "" #invalid
            else:
                for y in range(1,d+1):
                    if user_maps[n-1][A-y][B] != 0: #check if ships overlap
                        up = "" #invalid 
                        break
                    else:
                        up = "UP " #up is valid
                
            if A + d > 9: #check if rest of ship passes over lower boundary of map
                down = ""
            else:
                for y in range(1,d+1):
                    if user_maps[n-1][A+y][B] != 0: #check if ships overlap
                        down = ""
                        break
                    else:
                        down = "DOWN " #down is valid        
                        
            if right == "" and left == "" and up == "" and down == "": #check if all directions are invalid
                os.system('cls')
                print("\nInvalid choice, please try again.\n")
                user_maps[n-1][A][B] = 0 #reset starting coordinates to 0
                h = n #set h to current user
                g = x #set g to current ship sequence
                return make_user_map(h,g) #retry entire function from where user has left off

            possible_directions = right+left+up+down
            possible_directions = possible_directions[:-1] #removes space from end of possible directions list
            print("How would you like to orient your ship? ("+possible_directions+")?") #print possible directions
                
            msvcrt.getch()
            orient = str(msvcrt.getch())  #prompts user to input arrow key
                
            for key in dict_orient: #convert arrow key code to direction (RIGHT, LEFT, UP, DOWN)
                if orient == key:
                    orient = dict_orient[key]        
            
            while orient not in possible_directions: #checks if input is a valid direction
                print("Invalid choice, please try again.")
                print("How would you like to orient your ship? ("+possible_directions+")?")
                msvcrt.getch()
                orient = str(msvcrt.getch())  
                    
                for key in dict_orient:
                    if orient == key:
                        orient = dict_orient[key]               
            
            if orient+" " == right: #fill in rest of the ship to the right of starting coordinate with 1
                for y in range(1,d+1):
                    user_maps[n-1][A][B+y] = 1
            elif orient+" " == left: #fill in rest of the ship to the left of starting coordinate with 1
                for y in range(1,d+1):
                    user_maps[n-1][A][B-y] = 1
            elif orient+" " == up: #fill in rest of the ship above starting coordinate with 1
                for y in range(1,d+1):
                    user_maps[n-1][A-y][B] = 1 
            elif orient+" " == down: #fill in rest of the ship below starting coordinate with 1
                for y in range(1,d+1):
                    user_maps[n-1][A+y][B] = 1               
            os.system('cls')
            
            if n == 2 and x == 4:
                print("\nAfter pause, share computer with User 1.")
                time.sleep(3)                
                os.system('cls') 
        
    while True:
        try:
            n = int(input("\nWho will flip the coin? User (1) or User (2)? ")) #prompt user to input 1 or 2
            if n == 1 or n == 2: #check if input is either 1 or 2
                break
            else: 
                print("Invalid choice, please enter either 1 or 2.")
        except ValueError: #accept errors and loop again
            print("Invalid choice, please enter either 1 or 2.")      
    return coin_toss(n)

# CHANGE AND PRINT MAPS
#------------------------------------------
def hidden_map(n):
    for a in range(0,10):
        for b in range(0,10):
            if n == 1: #for user 1
                if user_2_map[a][b] == 1:
                    hidden_user_2_map[a][b] = 0 #hide ship (1) on actual map as 0 on hidden map
                else:
                    hidden_user_2_map[a][b] = user_2_map[a][b]
            else: #for user 2
                if user_1_map[a][b] == 1:
                    hidden_user_1_map[a][b] = 0 #hide ship (1) on actual map as 0 on hidden map
                else:
                    hidden_user_1_map[a][b] = user_1_map[a][b]                
    if n == 1:
        return print_map(hidden_user_2_map)
    else:
        return print_map(hidden_user_1_map)
        
def print_map(specific_map):
    for i in range(10): #for all rows
        x = str(specific_map[i])
        x = x.replace('0,', colored('0', 'blue')) #blue ocean background
        x = x.replace('0]', colored('0', 'blue'))
        x = x.replace('1,', colored('S', 'green')) #ship (1) = green
        x = x.replace('1]', colored('S', 'green'))
        x = x.replace('2,', colored('H', 'red')) #hit (2) = red
        x = x.replace('2]', colored('H', 'red'))
        x = x.replace('3,', colored('M', 'cyan')) #miss (3) = cyan
        x = x.replace('3]', colored('M', 'cyan'))
        x = x[1:]

        print(' '+x+'  '+row_labels[i]) #print replaced rows with row labels
            
    print("\n "+column_labels[0]+' '+column_labels[1]+' '+column_labels[2]+' '+column_labels[3]+' '+column_labels[4]+' '+  
          column_labels[5]+' '+column_labels[6]+' '+column_labels[7]+' '+column_labels[8]+' '+column_labels[9]) #print last row with column labels
        
# START
#------------------------------------------
def start():
    print("----------------------------------------\n")
    print(" W E L C O M E   T O   B A T T L E S H I P ! \n")
    print("----------------------------------------")
    mode = input("PvE (1) or PvP? (2)? ")
    
    if mode == "1":
        os.system("start "+"Battleship_PvE.py")
        quit()
    elif mode == "2":
        os.system('cls')
        h = 1 #user 1 starts
        g = 0 #start with ship index 0
        return make_user_map(h,g)        
    else:
        os.system('cls')
        return start()
    
start()