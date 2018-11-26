import math
from generator import *

class Model:
    def __init__(self, len):
        self.dim = len
        self.model = self.build()

    def build(self):
        x = int(math.ceil(self.dim / 2))
        model = [[]]
        model = [[0 for i in range(self.dim)] for j in range(self.dim)]
        s = 0
        for l in range(x):
            k = 0
            n = self.dim - 2 * l
            p = 2 * n + 2 * (n - 2)
            h = (n - 1) * 3 + 1
            for j in range(l, n + l):
                model[l][j] = k + 1 + s
                model[self.dim - l - 1][j] = h + s
                if (h + s) == (self.dim * self.dim) and j == l:
                    model[self.dim - l - 1][j] = 0
                h -= 1
                k += 1
            k = 0
            for i in range(l + 1, self.dim - l - 1):
                model[i][l] = p + s
                model[i][self.dim - l - 1] = n + k + 1 + s
                p -= 1
                k += 1
            s += 2 * n + 2 * (n - 2)
        return model


    def __str__(self):
        padding = find_padding(len(self.model) * len(self.model)) + 1
        res = ""
        for i in range(len(self.model)):
            for j in range(len(self.model[i])):
                res += str(str(self.model[i][j]).ljust(padding))
            res += '\n'
        return res
            
        