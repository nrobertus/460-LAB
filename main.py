from random import randint
import sys
random_bool = False
trials = 100
core_count = 3
user_input = True

class processor:

    def __init__(self, cores):
        #Globals for jobs and cores
        self.jobs = []
        self.cores = []
        self.num_cores = cores


        #Core initialization
        for x in range(0,cores):
            c = core()
            self.cores.append(c)

    #Function to manage cores and jobs
    def proc_manager(self, rand):

        if not rand:
            f = open("jobs.txt", 'r')
            jobList = f.read()
            jobList = jobList.translate(None, '\n').translate(None, ' ').split(';')
            for job in jobList:
                job = job.split(',')
                if(len(job) == 3):
                    newJob = makeJob(int(job[0]), int(job[1]), int(job[2]))
                    self.jobs.append(newJob)
        else:
            for i in range(0, 1000):
                time = randint(0, 500)
                newJob = makeJob(i+1, i+1, time)
                self.jobs.append(newJob)

        #initialize the ticker
        self.tick = 0
        #set the next core counter to mod out to 0
        nextCore = self.num_cores - 1
        #Setup a queue of queues for cores to look at
        queues = []
        for x in range(0, self.num_cores):
            queue = []
            queues.append(queue)
        while(True):
            #increment the ticker
            self.tick += 1
            #main loop for adding jobs to queues
            for index, job in enumerate(self.jobs) :
                job.arrival = job.arrival - 1
                if(job.arrival == 0):
                    nextCore = (nextCore+1)%self.num_cores
                    queues[nextCore].append(job.time)
                    self.jobs.pop(index)
            for index, core in enumerate(self.cores):
                busy = core.tick_job()
                if not busy:
                    if(queues[index]):
                        core.get_job(queues[index][0])
                        queues[index].pop(0)
            if len(self.jobs) == 0:
                num_queues = len(queues)
                emtpy_queues = []
                for queue in queues:
                    if not queue:
                        emtpy_queues.append("empty")
                if(num_queues == len(emtpy_queues)):
                    break

            #print self.tick
            #failsafe to exit loop, TEMP
        print self.tick
        return self.tick
    def print_jobs(self):
        for job in self.jobs:
            print job.arrival

class core:
    def __init__(self):
        self.data = [];
        self.currentJobTime = 0

    def get_job(self, job):
        self.currentJobTime = job

    def tick_job(self):
        if self.currentJobTime:
            self.currentJobTime = self.currentJobTime - 1

            if (self.currentJobTime == 0):
                return False
            else:
                return True
        else:
            return False
    def execute_task(self, steps):
        while(steps>0):
            print steps
            steps  -= 1

class job(object):
    id = 0
    arrival = 0
    time = 0

    def __init__(self, id, arrival, time):
        self.id = id
        self.arrival = arrival
        self.time = time

def makeJob(id, arrival, time):
    Job = job(id, arrival, time)
    return Job

if(user_input):
    core_count = int(raw_input("Enter number of cores: "))
    user_rand = raw_input("Use random input? (Y/N) ")
    if(user_rand == 'Y'):
        random_bool = True
    elif(user_rand == 'N'):
        random_bool = False
    trials = int(raw_input("Enter number of trials: "))

x = processor(core_count)
tick_counter = 0
for z in range(0, trials):
    current = x.proc_manager(random_bool)
    tick_counter += current
    #print current

average = tick_counter/trials
print "======================================"
print "Average:"
print average
