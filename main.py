class processor:

    def __init__(self, cores):
        self.cores = [];
        for x in range(0,cores):
            c = core()
            self.cores.append(c)
        for core_ in self.cores:
            core_.execute_task(10)




class core:
    def __init__(self):
        self.data = [];

    def execute_task(self, steps):
        while(steps>0):
            print steps
            steps  -= 1




x = processor(10)