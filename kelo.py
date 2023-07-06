import json
from copy import copy, deepcopy
import numpy as np
import math

save = True
startingelo = 1284

from datetime import datetime

with open("kelo.txt", 'r') as f:
    data = json.loads(f.read())

with open("games.txt", 'r') as f:
    played_games = json.loads(f.read())

def sortusers():
    '''
    Sorts users by elo
    '''
    global data
    #saves orignal data to numpy array
    temp_data = np.array(deepcopy(data))
    elos = temp_data[:,1].tolist()
    for i in range(len(elos)):
        max_index = elos.index(max(elos))
        data[i] = temp_data[max_index].tolist()
        elos[max_index] = "-10000"

def calculate_elo(black, white, winner):
    '''
    Calculates new elo scores for each player (black and white) depending on the winner (winner)
    and the current elo rating of each player
    '''
    global data
    data[black][1] = float(data[black][1])
    data[white][1] = float(data[white][1])
    transformed_rating1 = 10**(data[black][1]/400)
    transformed_rating2 = 10**(data[white][1]/400)
    expectancy1 = transformed_rating1/(transformed_rating1+transformed_rating2)
    expectancy2 = transformed_rating2/(transformed_rating1+transformed_rating2)
    score1 = int(winner == "black")+0.5*int(winner == "draw")
    score2 = int(winner == "white")+0.5*int(winner == "draw")
    #calculate new elos
    data[black][1] += 40*(score1-expectancy1)
    data[white][1] += 40*(score2-expectancy2)
    #add 1 to number of games
    data[black][2] = int(data[black][2])+1
    data[white][2] = int(data[white][2])+1
    print("{0:10}{1:10}".format(data[white][0], round(data[white][1],1)))
    print("{0:10}{1:10}".format(data[black][0], round(data[black][1],1)))

def game():
    '''
    Command for adding the results of a finished official kelo-game
    '''
    global data
    global played_games
    white = input("White: ")
    for i in range(len(data)):
        if white == data[i][0]:
            white = i
            break
    else:
        print(f"no user {white} exists")
        return
    black = input("Black: ")
    for i in range(len(data)):
        if black == data[i][0]:
            if i == white:
                print("not possible")
                return
            black = i
            break
    else:
        print(f"no user {black} exists")
        return
    while True:
        winner = input("Winner: ")
        if(winner != "black" and winner != "white" and winner != "draw"):
            print("black, white or draw")
        else:
            calculate_elo(black, white, winner)
            played_games += [[data[white][0], data[black][0], int((winner == "white")-(winner == "black")), datetime.now().isoformat()]]
            return

def adduser():
    '''
    Command for adding a new user to the kelo database
    '''
    global data, startingelo
    name = str(input("Input name: "))
    for i in range(len(data)):
        if name == data[i][0]:
            print("player already exists")
            return
    data += [[name,startingelo,0]]
    print("user added")

def edituser():
    '''
    Command for editing an existing user's kelo information, ie. elo and number of games
    '''
    user = input("User name: ")
    for i in range(len(data)):
        if user == data[i][0]:
            try:
                newname = input("new name: ")
                try:
                    elo = float(input(f"elo: "))
                except ValueError:
                    elo = data[i][1]
                try:
                    games = int(input("number of games: "))
                except ValueError:
                    games = data[i][2]
                data[i] = [newname,elo,games]
            except ValueError:
                print("invalid")
            return
    print(f"no user {user} exists")

# Main loop
while(True):
    command = input("Input command: ")
    if command == "adduser":
        adduser()
    elif command == "removeuser":
        user = input("Which user do you want to remove: ")
        for i in range(len(data)):
            if user == data[i][0]:
                data.pop(i)
                print("user removed")
                break
        else:
            #if no break
            print(f"no user {user} exists")
    elif command == "game":
        game()
    elif command == "showusers":
        sortusers()
        for i in range(len(data)):
            print("{0:10}{1:10}".format(data[i][0],round(float(data[i][1]),1)))
    elif command == "edituser":
        edituser()
    elif command == "abort":
        save = False
        print("exiting without saving")
        break
    elif command == "exit":
        break
    elif command == "help":
        print("{0:15}{1:15}".format("game", "input a chess game"))
        print("{0:15}{1:15}".format("adduser", "add a user"))
        print("{0:15}{1:15}".format("removeuser", "remove a user"))
        print("{0:15}{1:15}".format("showusers", "show elos of all users"))
        print("{0:15}{1:15}".format("editusers", "edit elo and number of games of a users"))
        print("{0:15}{1:15}".format("abort", "exit without saving"))
        print("{0:15}{1:15}".format("exit", "exit"))
    else:
        print("invalid command, type help for list of commands")

#turns all ' characters to "
inputdata = list(str(data))
for i in range(len(inputdata)):
    if inputdata[i] == "'":
        inputdata[i] = '"'
played_games2 = list(str(played_games))
for i in range(len(played_games2)):
    if played_games2[i] == "'":
        played_games2[i] = '"'

# Save changes to file 'kelo.txt'
if(save):
    with open("kelo.txt", 'w') as f:
        data = f.write("".join(inputdata))
    with open("games.txt", 'w') as f:
        played_games = f.write("".join(played_games2))

# Sort users when exiting program
sortusers()
