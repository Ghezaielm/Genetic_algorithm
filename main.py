import numpy as np 
import matplotlib.pyplot as plt




class GA():
    def __init__(self):
        self.N = 150
        self.offspring_rate = [1 for i in range(self.N)]
        self.mutation_rate = 0.2
        self.selection_rate = 0.05
        self.n_params = 100
        self.topInd = False
        self.gen = 0
        self.pop = []
        self.min_val = -30
        self.max_val = 30
        self.target = np.random.randint(self.min_val,self.max_val,self.n_params).tolist()
        self.parents = []
        self.fitness = []
        self.couples = []
        self.OAF = False
        self.recombination_rate = 0.2
        self.fits = []
        
    def show(self,mode='ref'):
        if mode == 'ref':
            f = plt.figure(figsize=(10,10))
            ax = f.add_subplot(111)
            ax.plot(self.target)
            ax.set_title('reference')
            plt.show()
        else:
            f = plt.figure(figsize=(10,5))
            ax = f.add_subplot(111)
            ax.plot(self.topInd,label="topInd")
            ax.plot(self.target,label="reference")
            ax.set_title('Generation {}'.format(self.gen))
            plt.legend()
            plt.show()
            
    def generatePop(self):
        #print("Generating population ...")
        if self.gen == 0:
            self.pop = [np.random.randint(self.min_val,self.max_val,self.n_params).tolist()
                        for i in range(self.N)]
            #print("Initial population = {}".format(len(self.pop)))
        else:
            #print("Mating ...")
            self.pop = [GA.mate(self,couple) for couple in self.couples]
            
    def mutate(self):
        #print("Mutate individuals ...")
        for idx,i in enumerate(self.pop):
            n_mutations = np.random.randint(1,round(self.n_params*self.mutation_rate),1)[0]
            positions = np.random.choice([i for i in range(self.n_params)],n_mutations,
                                        replace=False).tolist()
            
            for j in positions:
                self.pop[idx][j] = np.random.randint(self.min_val,self.max_val,1)[0]

    def getFitness(self):

        #print("Computing fitness ...")
        self.fitness = []
        for i in self.pop:
            self.fitness.append(1/np.mean([(self.target[j]-i[j])**2 
                                         for j in range(self.n_params)]))
        #print("#### Statistics")
        #print("Max fitness = {}".format(max(self.fitness)))
        #print("Min fitness = {}".format(min(self.fitness)))
        #print("Mean fitness = {}".format(np.mean(self.fitness)))
        self.fits.append(min(self.fitness))
        
    def parent_selection(self):
        #print("Selecting parents ...")
        self.p_fitness = [(idx,i) for idx,i in enumerate(self.fitness)]
        self.p_fitness = sorted(self.p_fitness, key=lambda x:x[1])[::-1]
        self.parents = [self.pop[i[0]] 
                        for i in self.p_fitness[:round(self.N*self.selection_rate)]]
        self.p_fitness = [self.p_fitness[i][0] for i in range(round(self.N*self.selection_rate))]
        self.couples = [(p1,p2) for p1,i in enumerate(self.parents)
                       for p2,j in enumerate(self.parents) if p1!=p2]
        #print("Mean fit scores = {}".format(np.mean(self.p_fitness)))
        #print("\n","\n")
        self.gen+=1
        
    def mate(self,couple):
        p1 = self.parents[couple[0]]
        p2 = self.parents[couple[1]]
        def crossing_over(p1,p2):
            offspring = []
            for idx,i in enumerate(p1):
                curr = [p1[idx],p2[idx]]
                offspring.append(np.random.choice(curr,1)[0])
            return offspring
        return crossing_over(p1,p2)
    
    def check(self):
        f = plt.figure(111)
        ax = f.add_subplot(111)
        ax.plot(self.fits)
        plt.show()
    
        
        
                
a = GA()
for gen in range(50):
    a.generatePop()
    a.mutate()
    a.getFitness()
    a.parent_selection()
    a.topInd = a.parents[0]
    a.show(mode="final")
a.check()


