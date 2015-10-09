#IMPORTS
import threading
import sys
import time
from random import randint
from threading import Thread, Lock

#DEFINES
LIST_LIMIT = 20
INT_LIMIT = 40

t_end = time.time() + 10 #duration in seconds

lock = Lock() # Threading lock

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
            print ("New node added to " + end)
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
            sys.exit()
            return False
 
    def remove(self, node_value):
        current_node = self.head
 
        while current_node is not None:
            if (current_node.data%2) == node_value:
                # if it's not the first element
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                else:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                    self.head = current_node.next
                    current_node.next.prev = None

            current_node = current_node.next
    def show(self):
        print ("Current list -> "),
        current_node = self.head
        while current_node is not None:
            print(current_node.data), 
            current_node = current_node.next
        print ""

    def count(self):
        list_length = 0
        current_node = self.head
        while current_node is not None:
            list_length = list_length + 1
            current_node = current_node.next
        return list_length
 

def generate_value():
    return randint(0,INT_LIMIT)

def producer_1(list_d):
    while time.time() < t_end:
        lock.acquire()
        #list_d.show()
        successful = list_d.append(generate_value(),'tail')
        if not successful:
            print "Producer 1: No nodes added"
            time.sleep(0.01)
        else:
            print("Producer 1: Added A Node")
            #list_d.show()
        lock.release()
def producer_2(list_d):
    while time.time() < t_end:
        lock.acquire()
        #list_d.show()
        successful = list_d.append(generate_value(),'head')
        if not successful:
            print ("Producer 2: No nodes added")
            time.sleep(0.01)
        else:
            print ("Producer 2: Added A Node")
            #list_d.show()
        lock.release()
def consumer_1(list_d):
    while time.time() < t_end:
        #list_d.show()
        lock.acquire()
        successful = list_d.remove(1)
        if not successful:
            print("Consumer 1: No nodes deleted")
        else:
            print("Consumer 1: Delete A Node")
        lock.release()
            #list_d.show()
def consumer_2(list_d):
    while time.time() < t_end:
        #list_d.show()
        lock.acquire()
        successful = list_d.remove(0)
        if not successful:
            print("Consumer 2: No nodes deleted")
            time.sleep(0.01);
        else:
            print("Consumer 2: Delete A Node")
            #list_d.show()
        lock.release()


d = DoubleList()


p1 = threading.Thread(target=producer_1, args=(d,))
p2 = threading.Thread(target=producer_2, args=(d,))
c1 = threading.Thread(target=consumer_1, args=(d,))
c2 = threading.Thread(target=consumer_2, args=(d,))

p1.start()
p2.start()
c1.start()
c2.start()