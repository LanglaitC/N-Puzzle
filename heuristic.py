import math
## Methods making the calculation of the heuristic h(x)
class Heuristic:
    def __init__(self, res, model):
        self.dim = len(res)
        self.model = model
        self.tak = res
        self.h1 = self.miss_placed()
        self.h2 = self.mannhathan()

    def miss_placed(self):
        model_tab = []
        tab = []
        count = 0
        for line in self.tak:
            tab += line
        for line in self.model:
            model_tab += line
        for i in range(self.dim * self.dim):
            if tab[i] != model_tab[i]:
                count += 1
        # print ('miss_placed :', count)
        return count

    def mannhathan(self):
        dist = 0
        for i in range(len(self.model)):
            for j in range(len(self.model)):
                if self.tak[i][j] != self.model[i][j]:
                    val = self.tak[i][j]
                    dist += math.fabs(j - self.find_x(val)) + math.fabs(i - self.find_y(val))
        # print ('mannhatan :', dist)
        return dist


    def find_x(self, val):
        for i in range(len(self.model)):
            for j in range(len(self.model)):
                if self.model[i][j] == val:
                    return j 


    def find_y(self, val):
        for i in range(len(self.model)):
            for j in range(len(self.model)):
                if self.model[i][j] == val:
                    return i
    