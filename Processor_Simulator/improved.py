from random import randint
import math
import time
start_date = time.strftime("%m_%d_%Y")
start_time = time.strftime("%H_%M_%S")

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
        core_status=[]
        core_total_time = []
        for x in range(0, self.num_cores):
            queue = []
            queues.append(queue)
            core_status.append(0)
            core_total_time.append(0)
        while(True):
            #increment the ticker
            self.tick += 1
            #calculate the total time left for each core (remaining time on current job + total time of jobs in queue)
            for index, core in enumerate(self.cores):
                core_total_time[index] = 0
                if(queues[index]):
                    for job in queues[index]:
                        core_total_time[index] += job.time
                core_total_time[index] += core_status[index]
            #manage jobs and queues
            for index, job in enumerate(self.jobs):
                job.arrival = job.arrival - 1
                if(job.arrival == 0):

                    core_index = core_total_time.index(min(core_total_time))
                    queues[core_index].append(job)
                    self.jobs.pop(index)

            #Manage core usage
            for index, core in enumerate(self.cores):
                #print "core: " + str(index)
                busy = core.tick_job()
                core_status[index] = busy

                if busy == 0:
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
                    for x in core_status:
                        if x == 0:
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
            return self.currentJobTime
        else:
            return 0

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
    trial_results = []
    filename = "output/optimized/"+str(start_date) + "_" + str(start_time) + "_OPT.txt"
    f = open(filename, "w")
    if(user_input):
        core_count = int(raw_input("Enter number of cores: "))
        user_rand = raw_input("Use random input? (Y/N) ")
        if(user_rand == 'Y'):
            random_bool = True
        elif(user_rand == 'N'):
            random_bool = False
        trials = int(raw_input("Enter number of trials: "))

    #initialize the processor with the given number of cores
    x = processor(core_count)

    #print a header to the output file
    f.write("Date: " + start_date.replace("_", "/") + "\n")
    f.write("Time: " + start_time.replace("_", ":") + "\n")
    f.write("Cores: " + str(core_count) + "\n")
    f.write("Random data: " + str(random_bool) + "\n")
    f.write("# of trials: " + str(trials) + "\n\n")
    f.write("======================================\n\n")

    #Run the given number of trials and print the output to the file and the console
    for z in range(0, trials):
        current = x.proc_manager(random_bool)
        trial_results.append(current)
        f.write(str(current) + " ms\n")
        print str(current) + " ms"

    #calculate stats on all the trials
    minimum = min(trial_results)
    maximum = max(trial_results)
    avg = average(trial_results)
    variance = map(lambda x: (x - avg)**2, trial_results)
    std_dev = math.sqrt(average(variance))

    #print the statistics in a footer on the output file and close the file writer
    f.write("\n======================================\n\n")
    f.write("Average: " + str(avg) + " ms\n")
    f.write("Minimum: " + str(minimum) + " ms\n")
    f.write("Maximum: " + str(maximum) + " ms\n")
    f.write("Standard deviation: " + str(std_dev) + " ms")
    f.close()

    #Print the final summary to the console
    print "======================================"
    print "Average: " + str(avg) + " ms"
    print "Minimum: " + str(minimum) + " ms"
    print "Maximum: " + str(maximum) + " ms"
    print "Standard deviation: " + str(std_dev) + " ms"




#Call the main function with default values to be overwritten by user input
main(True, False, 100, 3)