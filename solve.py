import math
import copy
import time
import heapq

class Solve:
    def __init__(self, tak, model, model_dic, heuristic, greedy, uniform_cost):
        self.dim = len(tak)
        self.model = model
        self.model_dic = model_dic
        self.greedy = greedy
        self.uniform_cost = uniform_cost
        self.currentHeuristic = heuristic
        self.heuristic = {
            1: self.manhattan_heuristic, 
            2: self.outta_place_heuristic,
            3: self.euclidian_heuristic,
            4: self.linear_man_heuristic
        }
        self.tak = self.to_tuple(tak)
        self.model = self.to_tuple(self.model)
        self.solve()

    def set_param(self, elem, tak):
        h = self.heuristic[self.currentHeuristic](tak) if not self.uniform_cost else 0
        new = {"tak":tak, "h": h ,"c": elem[2] + 1, "parent": elem}
        new["f"] = (new["h"] + new["c"]) if not self.greedy else new["h"]
        return new

    def to_tuple(self, matrix):
        tab = []
        if type(matrix[0]) is not list:
            return matrix
        else:
            for i in range (len(matrix)):
                tab = tab + self.to_tuple(matrix[i])
        return tuple(tab)

    def euclidian_heuristic(self, tab):
        res = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if tab[i * self.dim + j] != 0:
                    pos = i * self.dim + j
                    pos_in_model = self.model_dic[tab[i * self.dim + j]]
                    dx = pos_in_model % self.dim - pos % self.dim
                    dy = math.floor(pos_in_model / self.dim) - math.floor(pos / self.dim)
                    res += math.sqrt(dx * dx + dy * dy)
        return res

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

    def print_resolution(self, current, state):
        padding = len(str(self.dim * self.dim))
        currentParent = current
        res = ""
        while currentParent:
            res = self.display_puzzle(currentParent[3], padding) + '\n' + res
            currentParent = currentParent[4]
        print(res)
        print('Final cost: ' + str(current[2]))
        print('Complexity in time: ' + str(state['time']))
        print('Complexity in space: ' + str(state['space']))

    def display_puzzle(self, tab, padding):
        res = ""
        for i in range(self.dim):
            for j in range(self.dim):
                res += str(tab[i * self.dim + j]).ljust(padding + 1)
            res += '\n'
        return res

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
        heuristic_value = self.heuristic[self.currentHeuristic](self.tak) if not self.uniform_cost else 0
        open_list = []
        firstValue = (heuristic_value, heuristic_value, 0, self.tak, False)
        heapq.heappush(open_list, firstValue)
        open_list_hash = {}
        open_list_hash[open_list[0][3]] = {"tak": self.tak, "h": heuristic_value, "c": 0, "f": heuristic_value, "parent": False}
        closed_list = {}
        complexity = {'time': 1, 'space': 1}
        while len(open_list):
            current = heapq.heappop(open_list)
            if current[1] == 0 and current[3] == self.model:
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
                new = self.set_param(current, each)
                new_node = (new["f"], new['h'], new['c'], new['tak'], new['parent'])
                if not self.isInList(each, open_list_hash):
                    heapq.heappush(open_list, new_node)
                    complexity['time'] += 1
                    complexity['space'] += 1
                    if new['tak'] not in open_list_hash:
                        complexity['space'] += 1
                    open_list_hash[each] = [new_node]
                else:
                    if (open_list_hash[each][0][0] < new['f']):
                        heapq.heappush(open_list, new_node)
                        open_list_hash[each].insert(0, new_node)
                        complexity['space'] += 1