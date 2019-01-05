import math
from generator import *
import copy
import time

class Puzzle:
    def __init__(self, res, model):
        self.tak = res
        self.dim = len(res)
        self.model = model
        self.solvable = self.find_d() % 2 == self.find_p() % 2
        self.heuristic = {"newton": self.newton_heuristic, "outta_place": self.outta_place_heuristic}
        self.model = self.to_tuple(self.model)
        self.tak = self.to_tuple(self.tak)
        self.solve()

    def to_tuple(self, matrix):
        tab = []
        if type(matrix[0]) is not list:
            return matrix
        else:
            for i in range (len(matrix)):
                tab = tab + self.to_tuple(matrix[i])
        return tuple(tab)

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
        padding = find_padding(len(self.tak) * len(self.tak)) + 1
        res = ""
        for i in range(len(self.tak)):
            for j in range(len(self.tak[i])):
                res += str(str(self.tak[i][j]).ljust(padding))
            res += '\n'
        return res

    def find_elem(self, tab, elem):
        for i in range(self.dim):
            for j in range(self.dim):
                if tab[i * self.dim + j] == elem:
                    return i * self.dim + j

    def newton_heuristic(self, tab):
        res = 0
        for i in range(self.dim):
            for j in range(self.dim):
                pos = i * self.dim + j
                pos_in_model = self.find_elem(self.model, tab[i * self.dim + j])
                res += math.fabs(pos_in_model % self.dim - pos % self.dim) + math.fabs(math.floor(pos_in_model / self.dim) - math.floor(pos / self.dim))
        return res

    def outta_place_heuristic(self, tab):
        res = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if (tab[i * self.dim + j] != self.model[i * self.dim + j]):
                    res += 1
        return res
    
    def isInList(self, new, opened, closed):
        if new['tak'] in opened:
            return True
        if new["tak"] in closed:
            if (closed[new['tak']] > new['cost']):
                return False
            return True
        return False

    def get_result_in_order(self, oldest):
        res = []
        while (oldest['parent']):
            res.insert(0, {'tak': oldest['tak'], 'h':oldest['h']})
            oldest = oldest['parent']
        return (res)

    def print_result(self, tab, h):
        print('Heuristic: ' +  str(h))
        for i in range(self.dim):
            print(tab[i*self.dim:i*self.dim+self.dim])
        print('\n')
        return True

    def find_all_neighbours(self, tab):
        pos0 = None
        res =  []
        for i in range(self.dim):
            for j in range(self.dim):
                if tab[i * self.dim + j] == 0:
                    pos0 = i * self.dim + j
                    break
            if pos0 is not None:
                break
        if pos0 % self.dim != 0:
            new = list(tab)
            new[pos0], new[pos0 - 1] = new[pos0 - 1], new[pos0]
            res.append(tuple(new))
        if pos0 % self.dim != self.dim - 1:
            new = list(tab)
            new[pos0], new[pos0 + 1] = new[pos0 + 1], new[pos0]
            res.append(tuple(new))
        if pos0 / self.dim >= 1: 
            new = list(tab)
            new[pos0], new[pos0 - self.dim] = new[pos0 - self.dim], new[pos0]
            res.append(tuple(new))
        if pos0 / self.dim < self.dim - 1:
            new = list(tab)
            new[pos0], new[pos0 + self.dim] = new[pos0 + self.dim], new[pos0]
            res.append(tuple(new))
        return res


    def solve(self):
        if (self.solvable == False):
            print("Taquin isn't solvable, try a new one")
        else:
            open_list = [{"tak": self.tak, "h": 0, "c":0, "cost":0, 'parent':False}]
            open_list_hash = {}
            open_list_hash[open_list[0]['tak']] = open_list[0]['cost']
            closed_list = {}
            i = 0
            while len(open_list):
                i += 1
                current = open_list.pop(0)
                if current["tak"] == self.model:
                    #result = self.get_result_in_order(current)
                    print(current['c']);
                    #for each in result:
                    #    self.print_result(each['tak'], each['h'])
                    return True
                del open_list_hash[current['tak']]
                neighbours = self.find_all_neighbours(current["tak"])
                to_insert = []
                for each in neighbours:
                    new = {"tak":each, "h":self.heuristic["newton"](each) ,"c": current["c"] + 1, "parent": current}
                    new["cost"] = new["h"] + new["c"]
                    to_insert.append(new)
                to_insert.sort(key=lambda x: x['cost'], reverse=True)
                for each in to_insert:
                    if self.isInList(each, open_list_hash, closed_list):
                        pass
                    else:
                        open_list.insert(0, each)
                        open_list_hash[each['tak']] = each['cost']
                closed_list[current['tak']] = current['cost']
                open_list.sort(key=lambda x: x['cost'], reverse=False)
                
                



