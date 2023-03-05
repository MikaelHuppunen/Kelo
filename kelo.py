import json
from copy import copy, deepcopy
import numpy as np

save = True

with open("kelo.txt", 'r') as f:
    data = json.loads(f.read())

def sortusers():
    global data
    temp_data = np.array(deepcopy(data))
    elos = temp_data[:,1]
    elos = elos.tolist()
    for i in range(len(elos)):
        max_index = elos.index(max(elos))
        data[i] = temp_data[max_index].tolist()
        elos[max_index] = "-10000"

def calculate_elo(black, white, winner):
    global data
    data[black][1] = float(data[black][1])
    data[white][1] = float(data[white][1])
    R1 = 10**(data[black][1]/400)
    R2 = 10**(data[white][1]/400)
    expectancy1 = R1/(R1+R2)
    expectancy2 = R2/(R1+R2)
    S1 = int(winner == "black")+0.5*int(winner == "draw")
    S2 = int(winner == "white")+0.5*int(winner == "draw")
    data[black][1] += 40*(S1-expectancy1)
    data[white][1] += 40*(S2-expectancy2)
    print("{0:10}{1:10}".format(data[white][0], round(data[white][1],1)))
    print("{0:10}{1:10}".format(data[black][0], round(data[black][1],1)))

def game():
    global data
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
            return

def adduser():
    global data
    name = str(input("Input name: "))
    for i in range(len(data)):
        if name == data[i][0]:
            print("player already exists")
            return
    try:
        startingelo = float(input("Input elo: "))
    except ValueError:
        print("not a valid elo")
        return
    data += [[name,startingelo]]
    print("user added")

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
            print(f"no user {user} exists")
    elif command == "game":
        game()
    elif command == "showusers":
        sortusers()
        for i in range(len(data)):
            print("{0:10}{1:10}".format(data[i][0],round(float(data[i][1]),1)))
    elif command == "abort":
        save = False
        print("exiting without saving")
        break
    elif command == "exit":
        break
    elif command == "help":
        print("{0:15}{1:15}".format("game", "input a chess game"))
        print("{0:15}{1:15}".format("adduser", "add a user"))
        print("{0:15}{1:15}".format("remove", "remove a user"))
        print("{0:15}{1:15}".format("showusers", "show elos of all users"))
        print("{0:15}{1:15}".format("abort", "exit without saving"))
        print("{0:15}{1:15}".format("exit", "exit"))
    else:
        print("invalid command, type help for list of commands")

#turns all ' characters to "
inputdata = list(str(data))
for i in range(len(inputdata)):
    if inputdata[i] == "'":
        inputdata[i] = '"'

if(save):
    with open("kelo.txt", 'w') as f:
        data = f.write("".join(inputdata))