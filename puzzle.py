import math
from generator import *
import copy
import time
import heapq

class Puzzle:
    def __init__(self, res, model, model_dic):
        self.currentHeuristic = "manhattan"
        self.tak = res
        self.dim = len(res)
        self.model = model
        self.model_dic = model_dic
        self.solvable = self.find_d() % 2 == self.find_p() % 2
        self.heuristic = {"manhattan": self.manhattan_heuristic, "outta_place": self.outta_place_heuristic, "linear_man": self.linear_man_heuristic}
        self.tak = self.to_tuple(self.tak)
        self.model = self.to_tuple(self.model)
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

    def manhattan_heuristic(self, tab):
        res = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if tab[i * self.dim + j] != 0:
                    pos = i * self.dim + j
                    pos_in_model = self.model_dic[tab[i * self.dim + j]]
                    res += math.fabs(pos_in_model % self.dim - pos % self.dim) + math.fabs(math.floor(pos_in_model / self.dim) - math.floor(pos / self.dim))
        return res

    def outta_place_heuristic(self, tab):
        res = 0
        for i in range(self.dim * self.dim):
            if (tab[i] != self.model[i]) and tab[i] != 0:
                res += 1
        return res

    def different_sign(self, a, b):
        if (a >= 0 and b >= 0) or (a <= 0 and b <= 0):
            return False
        return True

    def linear_conflict(self, tab):
        conflict = 0
        for i in range(self.dim * self.dim):
            if i / self.dim == self.model_dic[tab[i]] / self.dim and tab[i] != 0:
                j = 1
                while (j + i % self.dim < self.dim):
                    if (i + j) / self.dim == self.model_dic[tab[i + j]] / self.dim and tab[i + j] != 0 and tab[i] != 0:
                        if self.different_sign(j, self.model_dic[tab[i + j]] % self.dim - self.model_dic[tab[i]] % self.dim):
                            conflict += 1
                    j += 1
            if i % self.dim == self.model_dic[tab[i]] % self.dim and tab[i] != 0:
                j = self.dim
                while ((j + i) / self.dim < self.dim):
                    if (i + j) % self.dim == self.model_dic[tab[i + j]] % self.dim and tab[i + j] != 0 and tab[i] != 0:
                        if self.different_sign(j, self.model_dic[tab[i + j]] / self.dim - self.model_dic[tab[i]] / self.dim):
                            conflict += 1
                    j += self.dim 
        return conflict

    def linear_man_heuristic(self, tab):
        return self.manhattan_heuristic(tab) + 2 * self.linear_conflict(tab)
    
    def isInList(self, new, liste):
        if new in liste:
            return True
        return False

    def get_result_in_order(self, oldest):
        res = []
        while (oldest['parent']):
            res.insert(0, {'tak': oldest['tak'], 'h':oldest['h']})
            oldest = oldest['parent']
        return (res)

    def print_resolution(self, current, state):
        print('Complexity in time: ' + str(state['time']))
        print('Complexity in space: ' + str(state['space']))
        currentParent = current[4]
        while currentParent:
            self.print_result(currentParent[3])
            currentParent = currentParent[4]
        print('Final cost: ' + str(current[0]))
        return
        

    def print_result(self, tab):
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
            heuristic_value = self.heuristic[self.currentHeuristic](self.tak)
            open_list = []
            firstValue = (heuristic_value, heuristic_value, 0, self.tak, False)
            heapq.heappush(open_list, firstValue)
            open_list_hash = {}
            open_list_hash[open_list[0][3]] = {"tak": self.tak, "h": heuristic_value, "c": 0, "cost": heuristic_value, "parent": False}
            closed_list = {}
            complexity = {'time': 1, 'space': 1}
            while len(open_list):
                current = heapq.heappop(open_list)
                if current[1] == 0:
                    self.print_resolution(current, complexity)
                    return True
                if (len(open_list_hash[current[3]]) == 1):
                    del open_list_hash[current[3]]
                else:
                    open_list_hash[current[3]]
                if current[3] not in closed_list:
                    complexity['space'] += 1
                closed_list[current[3]] = current[0]
                for each in self.find_all_neighbours(current[3]):
                    if self.isInList(each, closed_list):
                        continue
                    new = {"tak":each, "h": self.heuristic[self.currentHeuristic](each) ,"c": current[2] + 1, "parent": current}
                    new["cost"] = new["h"] + new["c"]
                    new_node = (new["cost"], new['h'], new['c'], new['tak'], new['parent'])
                    if not self.isInList(each, open_list_hash):
                        heapq.heappush(open_list, new_node)
                        complexity['time'] += 1
                        complexity['space'] += 1
                        if new['tak'] not in open_list_hash:
                            complexity['space'] += 1
                        open_list_hash[each] = [new_node]
                    else:
                        if (open_list_hash[each][0][0] < new['cost']):
                            heapq.heappush(open_list, new_node)
                            open_list_hash[each].insert(0, new_node)
                            complexity['space'] += 1