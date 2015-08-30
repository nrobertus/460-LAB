from random import randint
import math

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
        self.jobs_copy = []
        tripped = False
        if not rand:
            f = open("jobs.txt", 'r')
            jobList = f.read()
            jobList = jobList.translate(None, '\n').translate(None, ' ').split(';')
            for job in jobList:
                job = job.split(',')
                if(len(job) == 3):
                    self.jobs.append(makeJob(int(job[0]), int(job[1]), int(job[2])))
                    self.jobs_copy.append(makeJob(int(job[0]), int(job[1]), int(job[2])))
        else:
            for i in range(0, 1000):
                self.jobs.append(makeJob(i+1, i+1, randint(0, 500)))

        #initialize the ticker
        self.tick = 0
        #set the next core counter to mod out to 0
        nextCore = self.num_cores - 1
        #Setup a queue of queues for cores to look at
        queues = []
        cores_busy=[]
        for x in range(0, self.num_cores):
            queue = []
            queues.append(queue)
            cores_busy.append(True)
        self.jobs_count = 0
        while(True):
            #increment the ticker
            self.tick += 1

            #manage jobs and queues
            for index, job in enumerate(self.jobs):
                job.arrival = job.arrival - 1
                if(job.arrival == 0):
                    nextCore = (nextCore+1)%self.num_cores
                    queues[nextCore].append(job)
                    self.jobs.pop(index)
                    self.jobs_count += 1


            #Manage core usage
            for index, core in enumerate(self.cores):
                #print "core: " + str(index)
                busy = core.tick_job()
                cores_busy[index] = busy

                if not busy:
                    if(queues[index]):
                        core.get_job(queues[index][0])
                        queues[index].pop(0)

            #Check for a break case
            if len(self.jobs) == 0:

                num_queues = len(queues)
                emtpy_queues = []
                idle_cores = []

                for queue in queues:
                    if not queue:
                        emtpy_queues.append("empty")

                if(num_queues == len(emtpy_queues)):
                    for x in cores_busy:
                        if x == False:
                            idle_cores.append("idle")
                    if(num_queues == len(idle_cores)):
                        if not tripped:
                            tripped = True
                        else:
                            break
        return self.tick

class core:
    def __init__(self):
        self.currentJobTime = 0

    def get_job(self, job):
        self.currentJobTime = job.time
    def tick_job(self):
        if self.currentJobTime:
            self.currentJobTime = self.currentJobTime - 1
            #print "time left: " + str(self.currentJobTime)
            if (self.currentJobTime == 0):
                return False
            else:
                return True
        else:
            return False

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

#Main function
def main(user_input, random_bool, trials, core_count):
    def average(s): return sum(s) * 1.0 / len(s)
    values = []
    f = open("output.txt", "w")
    if(user_input):
        core_count = int(raw_input("Enter number of cores: "))
        user_rand = raw_input("Use random input? (Y/N) ")
        if(user_rand == 'Y'):
            random_bool = True
        elif(user_rand == 'N'):
            random_bool = False
        trials = int(raw_input("Enter number of trials: "))

    x = processor(core_count)
    f.write("Cores: " + str(core_count) + "\n")
    f.write("Random data: " + str(random_bool) + "\n")
    f.write("# of trials: " + str(trials) + "\n\n")
    f.write("======================================\n\n")

    for z in range(0, trials):
        current = x.proc_manager(random_bool)
        values.append(current)
        f.write(str(current) + " ms\n")
        print str(current) + " ms"

    minimum = min(values)
    maximum = max(values)
    avg = average(values)
    variance = map(lambda x: (x - avg)**2, values)
    std_dev = math.sqrt(average(variance))

    f.write("\n======================================\n\n")
    f.write("Average: " + str(avg) + " ms\n")
    f.write("Minimum: " + str(minimum) + " ms\n")
    f.write("Maximum: " + str(maximum) + " ms\n")
    f.write("Standard deviation: " + str(std_dev) + " ms")

    print "======================================"
    print "Average: " + str(avg) + " ms"
    print "Minimum: " + str(minimum) + " ms"
    print "Maximum: " + str(maximum) + " ms"
    print "Standard deviation: " + str(std_dev) + " ms"

    f.close()

#Call the main function
main(True, False, 100, 3)