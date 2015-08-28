class processor:

    def __init__(self, cores):
        self.jobs = []
        f = open("jobs.txt", 'r')
        jobList = f.read()
        jobList = jobList.translate(None, '\n').translate(None, ' ').split(';')


        for job in jobList:
            job = job.split(',')
            if(len(job) == 3):
                newJob = {'id':job[0], 'arrival':job[1], 'time':job[2]}
                self.jobs.append(newJob)
                
        for job in self.jobs:
            print job
        self.cores = [];
        for x in range(0,cores):
            c = core()
            self.cores.append(c)


class core:
    def __init__(self):
        self.data = [];

    def execute_task(self, steps):
        while(steps>0):
            print steps
            steps  -= 1




x = processor(10)