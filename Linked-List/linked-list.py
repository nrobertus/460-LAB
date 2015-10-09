#IMPORTS
import threading
import sys
import time
from random import randint
from threading import Thread, Lock


#DEFINES
LIST_LIMIT = 20
INT_LIMIT = 40

# Duration in seconds
t_end = time.time() + 10 

# Threading lock
lock = Lock()

# Gather time
start_date = time.strftime("%m_%d_%Y")
start_time = time.strftime("%H_%M_%S")

# Open file writer
filename = "output/"+str(start_date) + "_" + str(start_time) + "_LST.txt"
f = open(filename, "w")

# Print file header
f.write("Date: " + start_date.replace("_", "/") + "\n")
f.write("Time: " + start_time.replace("_", ":") + "\n")
f.write("="*10 + "\n")

#LINKED LIST IMPLEMENTATION
class Node(object):
 
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next
  
class DoubleList(object):
 
    head = None
    tail = None
 
    def append(self, data, end):
        if self.count() < LIST_LIMIT:
            new_node = Node(data, None, None)
            if self.head is None:
                self.head = self.tail = new_node
                return True
            elif end == 'tail':
                new_node.prev = self.tail
                new_node.next = None
                self.tail.next = new_node
                self.tail = new_node
                return True
            elif end == 'head':
                new_node.next = self.head
                new_node.prev = None
                self.head.prev = new_node
                self.head = new_node
                return True
            else:
                print"Invalid placement value."
                return False
        else:
            print "Append refused: list too long."
            f.write("Append refused: list too long")
            f.close()
            quit()
            return False
 
    def remove(self, node_value):
        current_node = self.head
 
        while current_node is not None:
            if (current_node.data % 2) == node_value:
                # if it's not the first element
                if current_node.prev is not None and current_node.next is not None:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                    return True
                elif current_node.next is not None:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                    self.head = current_node.next
                    current_node.next.prev = None
                    return True
                elif current_node.prev is not None:
                    current_node.prev.next = None
                    return True
                else:    
                    self.head = None
                    print("Buffer is empty")
                    f.write("Buffer is empty")
                    f.close()
                    quit()
                    return True
            current_node = current_node.next
    def show(self):
        print ("Current list -> "),     
        current_node = self.head
        while current_node is not None:
            print(current_node.data), 
            f.write(str(current_node.data) + " "),
            current_node = current_node.next
        print ""
        f.write("\n")

    def count(self):
        list_length = 0
        current_node = self.head
        while current_node is not None:
            list_length = list_length + 1
            current_node = current_node.next
        return list_length
 

#Helper function to create random node values
def generate_value():
    return randint(0,INT_LIMIT)

#Producer class
def producer(id, list_d, end):
    while time.time() < t_end:
        lock.acquire()
        successful = list_d.append(generate_value(), end)
        if not successful:
            print("Producer "+str(id)+": No nodes added")
            f.write("Producer "+str(id)+": No nodes added\n")
        else:
            print("Producer "+str(id)+": Added A Node")
            f.write("Producer "+str(id)+": Added A Node\n")
        list_d.show()
        lock.release()

#Consumer class
def consumer(id, list_d, mod_value):
    while time.time() < t_end:
        lock.acquire()
        type_str = ''
        if mod_value == 0:
            type_str = "even"
        elif mod_value == 1:
            type_str = "odd"
        successful = list_d.remove(mod_value)
        if not successful:
            print("Consumer "+str(id)+": No nodes deleted")
            f.write("Consumer "+str(id)+": No nodes deleted\n")
        else:
            print("Consumer "+str(id)+": Deleted "+ type_str+" Node")
            f.write("Consumer "+str(id)+": Deleted "+type_str+" Node\n")
        list_d.show()
        lock.release()
    
d = DoubleList()    #Init list

d.append(generate_value(), 'head') #Add three values to the list
d.append(generate_value(), 'head')
d.append(generate_value(), 'head')
d.show() #Print that list

p1 = threading.Thread(target=producer, args=(1, d,'head',))  #init producer 1, have it push to the head
p2 = threading.Thread(target=producer, args=(2, d,'head',))  #init producer 2, have it push to the tail
c1 = threading.Thread(target=consumer, args=(1, d, 0,))      #init consumer 1, have it remove even nodes
c2 = threading.Thread(target=consumer, args=(2, d, 1,))      #init consumer 2, have it remove odd nodes

#Start up the threads
p1.start()
p2.start()
c1.start()
c2.start()