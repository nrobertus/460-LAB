#################################
# PROGRAM SOURCE CODE -- PYTHON #
#################################

import time
from random import randint
import operator
import numpy as np

####################
# Helper functions #
####################

def getInput(filename):
    output = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.translate(None, '\n')
            line = line.split(' ')
            line_data ={"arrival":int(line[0]), "track": int(line[1]), "sector": int(line[2])}
            output.append(line_data)
    return output

def generateInput(quantity):
    output = []
    for x in range(0, quantity):
        new_request = {"arrival":randint(0, 99), "track":randint(0, 249), "sector": randint(0,7)}
        output.append(new_request)
    output = sorted(output, key=operator.itemgetter("arrival"))
    return output

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def standard_dev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5


def variance(data):
    """Calculates the population variance."""
    return np.var(data)
    
def RESET():
    clock.RESET()
    head.RESET()
##################################
# Classes for the clock and head #
##################################

class clock():
    def __init__(self):
        self.clock_var = 0

    def tick_01(self):
        self.clock_var += 0.1

    def tick_1(self):
        self.clock_var += 1

    def tick_10(self):
        self.clock_var += 10

    def get_clock(self):
        return self.clock_var

    def RESET(self):
        self.clock_var = 0

class head():
    def __init__(self):
        self.position = 0
        self.track = 0
        self.direction = -1

    def toggle_direction(self):
        if self.direction == -1:
            self.direction = 1
        else:
            self.direction = -1
    def set_direction_back(self):
        self.direction = -1

    def set_direction_forward(self):
        self.direction = 1

    def move_head_forward(self):
        if(self.position < 250):
            self.position = self.position + 1
        clock.tick_01()
        self.direction = 1

    def move_head_back(self):
        if(self.position > 0):
            self.position = self.position - 1
        clock.tick_01()
        self.direction = -1

    def seek_track(self):
        if(self.track == 7):
            self.track = 0
        else:
            self.track = self.track + 1
        clock.tick_1()

    def set_head(self, location):
        self.position = location

    def get_head(self):
        return self.position

    def get_track(self):
        return self.track

    def get_direction(self):
        return self.direction

    def RESET(self):
        self.position = 0
        self.track = 0
        self.direction = -1

############################
# Start the clock and head #
############################

clock = clock()
head = head()


def seek(disk, sector):
    #increment the clock by 10
    clock.tick_10()
    
    #seek the disk
    while(head.get_head() != disk):
        if(head.get_head() < disk):
            head.move_head_forward()
        elif(head.get_head() > disk):
            head.move_head_back()
    
    #seek the sector
    while(head.get_track() != sector):
        head.seek_track()

    #Add another tick, for reasons
    clock.tick_1()
    return clock.get_clock()

def FCFS(input):
    turnarounds = []
    for request in input:
        #ensure the arrival time is observed
        while(clock.get_clock() < request['arrival']):
            clock.tick_01()
        #print when the job is starting
        #fill the request
        seek(request['track'], request['sector'])
        
        turnarounds.append(clock.get_clock() - request['arrival'])
    f.write("Total Time: " + str(clock.get_clock()) + "\n")
    f.write("Average:" + str(mean(turnarounds)) + "\n")
    f.write("Standard deviation:" + str(standard_dev(turnarounds)) + "\n")
    f.write("Variance:" + str(variance(turnarounds)) + "\n")
    RESET()

def SSTF(input):
    todo = []
    queue = []
    turnarounds = []
    for request in input:
        queue.append(request)
    while True:
        for i, request in enumerate(queue):
            if clock.get_clock() >= request['arrival']:     #if any of the requests are less than or equal to the clock, 
                todo.append(request)                        #append them to a todo.
                queue.pop(i)
        if(len(todo)==1):                                   #if the length of todo is 1, do the task.
            seek(todo[0]['track'], todo[0]['sector'])
            
            turnarounds.append(clock.get_clock() - todo[0]['arrival'])
            todo.pop()

        elif(len(todo) > 1):                                #if the length of todo is more than 1, pick the closest task and start on it.
            todo_scores = []
            for i, todo_item in enumerate(todo):
                score = abs(head.get_head() - todo_item['track'])
                todo_scores.append({'index':i, 'score':score})
            todo_sorted = sorted(todo_scores, key=operator.itemgetter("score"))
            seek(todo[todo_sorted[0]['index']]['track'],todo[todo_sorted[0]['index']]['sector'])
            
            turnarounds.append(clock.get_clock() - todo[todo_sorted[0]['index']]['arrival'])
            todo.pop(todo_sorted[0]['index'])
        elif(len(todo) == 0) and (len(queue) > 0):
            clock.tick_1()
        elif(len(todo) == 0) and (len(queue) == 0):
            f.write("Total Time: " + str(clock.get_clock()) + "\n")
            f.write("Average:" + str(mean(turnarounds)) + "\n")
            f.write("Standard deviation:" + str(standard_dev(turnarounds)) + "\n")
            f.write("Variance:" + str(variance(turnarounds)) + "\n")
            RESET()
            break

def LOOK(input):
    todo = []
    queue = []
    turnarounds = []
    for request in input:
        queue.append(request)
    while True:
        for i, request in enumerate(queue):
            if clock.get_clock() >= request['arrival']:     #if any of the requests are less than or equal to the clock, 
                todo.append(request)                        #append them to a todo.
                queue.pop(i)
        if(len(todo)==1):                                   #if the length of todo is 1, do the task.
            seek(todo[0]['track'], todo[0]['sector'])
            turnarounds.append(clock.get_clock() - todo[0]['arrival'])
            
            todo.pop()

        elif(len(todo) > 1):                                #if the length of todo is more than 1, pick the closest task and start on it.
            todo_behind = []
            todo_ahead = []
            for i, todo_item in enumerate(todo):
                if(todo_item['track'] < head.get_head()): #todo item is behind the head
                    todo_behind.append({"index":i, "distance":abs(head.get_head() - todo_item['track'])})
                elif(todo_item['track'] > head.get_head()): #todo item is ahead of the head
                    todo_ahead.append({"index":i, "distance":abs(head.get_head() - todo_item['track'])})
            todo_ahead = sorted(todo_ahead, key=operator.itemgetter("distance"))
            todo_behind = sorted(todo_behind, key=operator.itemgetter("distance"))
            if(head.get_direction() == -1): #head is moving backwards
                if(len(todo_behind) > 0):
                    seek(todo[todo_behind[0]['index']]['track'], todo[todo_behind[0]['index']]['sector'])
                    turnarounds.append(clock.get_clock() - todo[todo_behind[0]['index']]['arrival'])
                    
                    todo.pop(todo_behind[0]['index'])
                else:
                    seek(todo[todo_ahead[0]['index']]['track'],todo[todo_ahead[0]['index']]['sector'])
                    turnarounds.append(clock.get_clock() - todo[todo_ahead[0]['index']]['arrival'])
                    
                    head.toggle_direction()
                    todo.pop(todo_ahead[0]['index'])
            elif(head.get_direction() == 1): #head is moving forwards
                if(len(todo_ahead) > 0):
                    seek(todo[todo_ahead[0]['index']]['track'], todo[todo_ahead[0]['index']]['sector'])
                    turnarounds.append(clock.get_clock() - todo[todo_ahead[0]['index']]['arrival'])
                    
                    todo.pop(todo_ahead[0]['index'])
                else:
                    seek(todo[todo_behind[0]['index']]['track'],todo[todo_behind[0]['index']]['sector'])
                    turnarounds.append(clock.get_clock() - todo[todo_behind[0]['index']]['arrival'])
                    
                    head.toggle_direction()
                    todo.pop(todo_behind[0]['index'])
        elif(len(todo) == 0) and (len(queue) > 0):
            clock.tick_1()
        elif(len(todo) == 0) and (len(queue) == 0):
            f.write("Total Time: " + str(clock.get_clock()) + "\n")
            f.write("Average:" + str(mean(turnarounds)) + "\n")
            f.write("Standard deviation:" + str(standard_dev(turnarounds)) + "\n")
            f.write("Variance:" + str(variance(turnarounds)) + "\n")
            RESET()
            break

def CLOOK(input):
    todo = []
    queue = []
    turnarounds = []
    for request in input:
        queue.append(request)
    while True:
        for i, request in enumerate(queue):
            if clock.get_clock() >= request['arrival']:     #if any of the requests are less than or equal to the clock, 
                todo.append(request)                        #append them to a todo.
                queue.pop(i)
        if(len(todo)==1):                                   #if the length of todo is 1, do the task.
            seek(todo[0]['track'], todo[0]['sector'])
            
            todo.pop()

        elif(len(todo) > 1):                                #if the length of todo is more than 1, pick the closest task and start on it.
            todo_behind = []
            todo_ahead = []
            for i, todo_item in enumerate(todo):
                if(todo_item['track'] < head.get_head()): #todo item is behind the head
                    todo_behind.append({"index":i, "distance":abs(head.get_head() - todo_item['track'])})
                elif(todo_item['track'] > head.get_head()): #todo item is ahead of the head
                    todo_ahead.append({"index":i, "distance":abs(head.get_head() - todo_item['track'])})
            todo_ahead = sorted(todo_ahead, key=operator.itemgetter("distance"))
            todo_behind = sorted(todo_behind, key=operator.itemgetter("distance"))
            if(head.get_direction() == -1): #head is moving backwards
                if(len(todo_behind) > 0):
                    seek(todo[todo_behind[0]['index']]['track'], todo[todo_behind[0]['index']]['sector'])
                    turnarounds.append(clock.get_clock() - todo[todo_behind[0]['index']]['arrival'])
                    
                    todo.pop(todo_behind[0]['index'])
                else:
                    head.set_head(250)
                    index = todo_ahead[len(todo_ahead) -1]['index']
                    seek(todo[index]['track'],todo[index]['sector'])
                    turnarounds.append(clock.get_clock() - todo[index]['arrival'])
                    
                    todo.pop(index)
            elif(head.get_direction() == 1): #head is moving forwards
                if(len(todo_ahead) > 0):
                    seek(todo[todo_ahead[0]['index']]['track'], todo[todo_ahead[0]['index']]['sector'])
                    turnarounds.append(clock.get_clock() - todo[todo_ahead[0]['index']]['arrival'])
                    
                    todo.pop(todo_ahead[0]['index'])
                else:
                    head.set_head(0)
                    index = todo_behind[len(todo_behind) -1]['index']
                    seek(todo[index]['track'],todo[index]['sector'])
                    turnarounds.append(clock.get_clock() - todo[index]['arrival'])
                    
                    todo.pop(index)
        elif(len(todo) == 0) and (len(queue) > 0):
            clock.tick_1()
        elif(len(todo) == 0) and (len(queue) == 0):
            f.write("Total Time: " + str(clock.get_clock()) + "\n")
            f.write("Average:" + str(mean(turnarounds)) + "\n")
            f.write("Standard deviation:" + str(standard_dev(turnarounds)) + "\n")
            f.write("Variance:" + str(variance(turnarounds)) + "\n")
            RESET()
            break
        
random_input = generateInput(50)
input = getInput('input.txt')

start_date = time.strftime("%m_%d_%Y")
start_time = time.strftime("%H_%M_%S")
filename = "output/" + str(start_date) + "_" + str(start_time) + ".txt"
f = open(filename, "w")

f.write("Nathan Robertus\nCSCI 460\nAssignment 3\n\n")
f.write("========================PROGRAM_OUTPUT========================\n")
f.write("\n\nPROVIDED INPUT\n\n")

f.write("FCFS\n")
FCFS(input)

f.write("\nSSTF\n")
SSTF(input)

f.write("\nLOOK\n")
LOOK(input)

f.write("\nCLOOK\n")
CLOOK(input)

f.write("\n\nRANDOM INPUT \n\n")


f.write("FCFS\n")
FCFS(random_input)

f.write("\nSSTF\n")
SSTF(random_input)

f.write("\nLOOK\n")
LOOK(random_input)

f.write("\nCLOOK\n")
CLOOK(random_input)

f.close()