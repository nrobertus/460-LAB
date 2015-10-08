#IMPORTS
import threading
import sys
import time
from random import randint

#DEFINES
LIST_LIMIT = 20
INT_LIMIT = 40

t_end = time.time() + 10 #duration in seconds


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
            return False
 
    def remove(self, even):
        current_node = self.head
        even_ness = ''
        while current_node is not None:
            if not even:
                even_ness = "Odd"
                if((current_node.data%2) != 0):
                    if self.head == self.tail:  # If the list is only one node long
                        self.head = None        # delete the node
                        print (even_ness + " node removed")
                        return True
                    elif self.head == current_node: 
                        self.head = current_node.next
                        print (even_ness + " node removed")
                        return True
                    elif self.tail == current_node:
                        current_node.prev.next = None
                        print (even_ness + " node removed")
                        return True
                    else:
                        current_node.prev.next = current_node.next
                        current_node.next.prev = current_node.prev
                        print (even_ness + " node removed")
                        return True
                else:
                    current_node = current_node.next
            else:
                even_ness = "Even"
                if((current_node.data%2) == 0):
                    if self.head == self.tail:
                        self.head = None
                        print (even_ness + " node removed")
                        return True
                    if self.head == current_node:
                        self.head = current_node.next
                        print (even_ness + " node removed")
                        return True
                    elif self.tail == current_node:
                        current_node.prev.next = None
                        print (even_ness + " node removed")
                        return True
                    else:
                        current_node.prev.next = current_node.next
                        current_node.next.prev = current_node.prev
                        print (even_ness + " node removed")
                        return True
                else:
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
        #list_d.show()
        successful = list_d.append(generate_value(),'tail')
        if not successful:
            print "Producer 1: No nodes added"
            time.sleep(0.01)
        else:
            print("Producer 1: Added A Node")
            #list_d.show()
def producer_2(list_d):
    while time.time() < t_end:
        #list_d.show()
        successful = list_d.append(generate_value(),'head')
        if not successful:
            print ("Producer 2: No nodes added")
            time.sleep(0.01)
        else:
            print ("Producer 2: Added A Node")
            #list_d.show()
def consumer_1(list_d):
    while time.time() < t_end:
        #list_d.show()
        successful = list_d.remove(False)
        if not successful:
            print("Consumer 1: No nodes deleted")
            time.sleep(0.01)
        else:
            print("Consumer 1: Delete A Node")
            #list_d.show()
def consumer_2(list_d):
    while time.time() < t_end:
        #list_d.show()
        successful = list_d.remove(True)
        if not successful:
            print("Consumer 2: No nodes deleted")
            time.sleep(0.01);
        else:
            print("Consumer 2: Delete A Node")
            #list_d.show()


d = DoubleList()


p1 = threading.Thread(target=producer_1, args=(d,))
p2 = threading.Thread(target=producer_2, args=(d,))
c1 = threading.Thread(target=consumer_1, args=(d,))
c2 = threading.Thread(target=consumer_2, args=(d,))

p1.start()
p2.start()
c1.start()
c2.start()