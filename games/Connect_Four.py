from random import randint
import os
from termcolor import colored 
from colorama import init 
import time

init() # initiate colouring

single_row = []; matrix = []

for column in range(7): #create 1 row of 7 columns
    single_row.append(0)
for row in range(6): #create 6 rows of 10 columns
    matrix.append(single_row[:])
    
board = matrix[:] #create specific and unique matrices

column_labels = [colored('1', 'yellow'), colored('2', 'yellow'), colored('3', 'yellow'), colored('4', 'yellow'), colored('5', 'yellow'), 
                 colored('6', 'yellow'), colored('7', 'yellow')]

# COORDINATE
#------------------------------------------
def column():
    while True:
        try:
            C = int(input("Choose a column (1-7): ")) #prompt user to input column number
            if 0 < C < 8: #check if column number is valid
                C = C - 1 #convert to index
                break
            else:
                print("Invalid choice, please enter another value.")
        except ValueError: #accept this error and restart loop
            print("Invalid choice, please enter another value.")
    return C

# TURNS
#------------------------------------------
def coin_toss(n):     
    os.system('cls') 
    print("---------------------------------------- \n")
    print(" G A M E   S T A R T \n")
    print("----------------------------------------")
    coin = str.upper(input("User "+str(n)+", Heads (H) or Tails (T)? ")) #prompt user to input H or T
    toss = randint(0,1) #randomly choose heads (1) or tails (2)
    
    if coin != "H" and coin != "T": #check if input is either T or H
        return coin_toss(n)
    
    if toss == 1:
        result = "H"
        print("The coin is: "+result)     
    elif toss == 0:
        result = "T"
        print("The coin is: "+result)
         
    if coin == result: #check if guess is correct
        print("Good guess!\n")
        time.sleep(1)
        return user_turn(n)
    else:
        print("Bad guess.\n")
        if n == 1:
            n = 2
        else:
            n = 1
        time.sleep(0.5)
        return user_turn(n)  
        
def user_turn(n):
    print("----------------------------------------")
    print(" U S E R   "+str(n)+"   T U R N")
    print("----------------------------------------\n")
    print_map(board)
    print("")
    C = column()
    
    for R in range(0,6):
        if board[0][C] == 1 or board[0][C] == 2: #check if all of column is filled
            a = False
        elif board[R][C] == 1 or board[R][C] == 2 or board[5][C] == 0: #check if column is open
            board[R-1][C] = n
            a = True
            break            
            
    if a == False: 
        os.system('cls')
        print("\nColumn full, please choose another column.\n")
        return user_turn(n)
        
    return turn_decider(n)
    
def turn_decider(n): 
    c = check() #check if no one has won (0) or someone has won (1,2)
    os.system('cls')
    if c == 0:
        if n == 1: 
            n = 2
        else:
            n = 1
        return user_turn(n)
    elif c == 4:
        print("")
        print_map(board)    
        print("")
        print("Game Finished. It's a Tie!")        
    else: 
        print("")
        print_map(board)    
        print("")
        print("Game Finished. User "+str(c)+" wins!")
        
    answer = str.upper(input("Play Again? (Y or N): "))
    if answer == "Y":
        os.system('cls')
        os.system("start "+"Connect_Four.py")
        quit()
    else:
        quit()
        
def check():
    win_connect_four = {1:3,2:4} #dict of winning connect four value reassign
    tie = True #assume tie
    
    for a in range(0,6): #loop process for all rows
        for b in range(0,7): #loop process for all columns 
            for c in range(1,3): #loop process for chips 1 and 2
                if a+3 < 6: #check all possible horizontal rows
                    if board[a][b] == board[a+1][b] == board[a+2][b] == board[a+3][b] == c: 
                        board[a][b] = board[a+1][b] = board[a+2][b] = board[a+3][b] = win_connect_four[c] #reassign winning connect four value 
                        return c
                    
                if b+3 < 7: #check all possible vertical rows
                    if board[a][b] == board[a][b+1] == board[a][b+2] == board[a][b+3] == c: 
                        board[a][b] = board[a][b+1] = board[a][b+2] = board[a][b+3] = win_connect_four[c] #reassign winning connect four value 
                        return c
                    
                if a+3 < 6 and b+3 < 7: #check all possible upward diagonals (left to right)  
                    if board[a][b] == board[a+1][b+1] == board[a+2][b+2] == board[a+3][b+3] == c:
                        board[a][b] = board[a+1][b+1] = board[a+2][b+2] = board[a+3][b+3] = win_connect_four[c] #reassign winning connect four value 
                        return c
                    
                if a-3 >= 0 and b+3 < 7: #check all possible lower diagonals (left to right)
                    if board[a][b] == board[a-1][b+1] == board[a-2][b+2] == board[a-3][b+3] == c:
                        board[a][b] = board[a-1][b+1] = board[a-2][b+2] = board[a-3][b+3] = win_connect_four[c] #reassign winning connect four value 
                        return c
                    
                if board[a][b] == 0:
                    tie = False
                    
    if tie == True:
        return 4 #4 means tie
    else:
        return 0 #0 means no one has won

# CHANGE AND PRINT MAPS
#------------------------------------------
def print_map(specific_map):
    for i in range(6): #for all rows
        x = str(specific_map[i])
        x = x.replace('0,', colored('0')) #background is empty
        x = x.replace('0]', colored('0')) 
        x = x.replace('1,', colored('1', 'grey', 'on_red')) #user 1 chip is grey on red
        x = x.replace('1]', colored('1', 'grey', 'on_red'))
        x = x.replace('2,', colored('2', 'grey', 'on_blue')) #user 2 chip is grey on blue
        x = x.replace('2]', colored('2', 'grey', 'on_blue'))
        x = x.replace('3,', colored('1', 'green', 'on_red')) #user 1 winner chips are green on red
        x = x.replace('3]', colored('1', 'green', 'on_red'))
        x = x.replace('4,', colored('2', 'green', 'on_blue')) #user 2 winner chips are green on blue
        x = x.replace('4]', colored('2', 'green', 'on_blue'))        
        x = x[1:]
        
        print(' '+x) #print replaced rows
        
    print("\n"+' '+column_labels[0]+' '+column_labels[1]+' '+column_labels[2]+' '+column_labels[3]+' '+column_labels[4]+' '+  
          column_labels[5]+' '+column_labels[6]) #print last row with column labels
    
# START
#------------------------------------------
def start():
    print("----------------------------------------\n")
    print(" W E L C O M E   T O   C O N N E C T   F O U R !\n")
    print("----------------------------------------")
    mode = input("PvE (1) or PvP? (2)? ")
    
    if mode == "1":
        os.system('cls')
        print("\nPvE is currently unavailable.\n")
        return start()
        #os.system("start "+"Connect_Four_PvE.py")
        #quit()        
    elif mode == "2":
        os.system('cls')
        while True:
            try:
                n = int(input("\nWho will flip the coin? User (1) or User (2)? "))
                if n == 1 or n == 2:
                    break
                else:
                    print("Invalid choice, please enter either 1 or 2.")
            except ValueError:
                print("Invalid choice, please enter either 1 or 2.")    
        return coin_toss(n)
    else:
        os.system('cls')
        return start()     
        
start()