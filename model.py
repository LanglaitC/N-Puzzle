import math;
from generator import *;

class Model:
    def __init__(self, tab):
        self.tab = tab
        self.dim = len(tab)
        self.model = self.build()

    def build(self):
        x = int(math.ceil(self.dim / 2))
        model = [[]]
        model = [[0 for i in range(self.dim)] for j in range(self.dim)]
        self.print_tab(model)
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
        self.print_tab(model)


    def print_tab(self, arr):
        padding = find_padding(len(arr) * len(arr));
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                print str(arr[i][j]).ljust(padding),
            print
            
        