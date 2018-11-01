import math
from generator import *

class Puzzle:
    def __init__(self, res, model):
        self.tak = res
        self.model = model
        self.solvable = self.find_d() % 2 == self.find_p() % 2
        # print self.solvable


    def find_d(self):
        for i in range(len(self.tak)):
            for j in range(len(self.tak)):
                if self.tak[i][j] == 0:
                    xi = j
                    yi = i
                    break
        if len(self.tak) % 2 != 0:
            xf = math.ceil(len(self.tak) / 2)
            yf = math.ceil(len(self.tak) / 2)
        else:
            xf = len(self.tak) / 2 - 1
            yf = len(self.tak) / 2
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


    def __str__(self):
        padding = find_padding(len(self.tak) * len(self.tak)) + 1;
        res = "";
        for i in range(len(self.tak)):
            for j in range(len(self.tak[i])):
                res += str(str(self.tak[i][j]).ljust(padding))
            res += '\n';
        return res;