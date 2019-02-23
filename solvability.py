import math

class Solvability:

    def __init__(self, tak, model):
        self.tak = tak
        self.model = model
        self.dim = len(self.tak)
        self.solvable = self.find_d() % 2 == self.find_p() % 2


    def find_d(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.tak[i][j] == 0:
                    xi = j
                    yi = i
                    break
        if self.dim % 2 != 0:
            xf = math.ceil(self.dim / 2)
            yf = math.ceil(self.dim / 2)
        else:
            xf = self.dim / 2 - 1
            yf = self.dim / 2
        d = math.fabs(xf - xi) + math.fabs(yf - yi)
        return d

    def find_p(self):
        tab = []
        p = 0
        for line in self.tak:
            tab += line
        model_tab = []
        for line in self.model:
            model_tab += line
        for i in range(len(tab)):
            for j in range(i, len(tab)):
                if model_tab.index(tab[i]) > model_tab.index(tab[j]):
                    tab[j], tab[i] = tab[i], tab[j]
                    p += 1
        return p