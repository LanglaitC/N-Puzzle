import math
from generator import *
import copy

class Puzzle:
    def __init__(self, res, model):
        self.tak = res
        self.dim = len(res)
        self.model = model
        self.solvable = self.find_d() % 2 == self.find_p() % 2
        self.heuristic = {"newton": self.newton_heuristic, "outta_place": self.outta_place_heuristic}
        self.solve()


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
        for i in range(len(tab)):
            for j in range(len(tab)):
                if tab[i][j] == elem:
                    return {"x": j, "y": i}

    def newton_heuristic(self, tab):
        res = 0
        for i in range(self.dim):
            for j in range(self.dim):
                pos_in_model = self.find_elem(self.model, tab[i][j])
                res += math.fabs(pos_in_model['x'] - j) + math.fabs(pos_in_model['y'] - i)
        return res

    def outta_place_heuristic(self, tab):
        res = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if (tab[i][j] != self.model[i][j]):
                    res += 1
        return res * 3
    
    def isInList(self, new, opened, closed):
        for each in opened:
            if each["tak"] == new["tak"] and each["cost"] <= new["cost"]:
                return True
        for each in closed:
            if each["tak"] == new["tak"]:
                return True
        return False

    def find_all_neighbours(self, tab):
        pos0 = None
        res =  []
        for i in range(self.dim):
            for j in range(self.dim):
                if tab[i][j] == 0:
                    pos0 = {"y": i, "x": j}
                    break
            if pos0 is not None:
                break
        if pos0["y"] != 0:
            new = copy.deepcopy(tab)
            new[pos0["y"]][pos0["x"]], new[pos0["y"] - 1][pos0["x"]] = new[pos0["y"] - 1][pos0["x"]], new[pos0["y"]][pos0["x"]]
            res.append(new)
        if pos0["y"] != self.dim - 1:
            new = copy.deepcopy(tab)
            new[pos0["y"]][pos0["x"]], new[pos0["y"] + 1][pos0["x"]] = new[pos0["y"] + 1][pos0["x"]], new[pos0["y"]][pos0["x"]]
            res.append(new)
        if pos0["x"] != 0:            
            new = copy.deepcopy(tab)
            new[pos0["y"]][pos0["x"]], new[pos0["y"]][pos0["x"] - 1] = new[pos0["y"]][pos0["x"] - 1], new[pos0["y"]][pos0["x"]]
            res.append(new)
        if pos0["x"] != self.dim - 1:
            new = copy.deepcopy(tab)
            new[pos0["y"]][pos0["x"]], new[pos0["y"]][pos0["x"] + 1] = new[pos0["y"]][pos0["x"] + 1], new[pos0["y"]][pos0["x"]]
            res.append(new)
        return res


    def solve(self):
        if (self.solvable == False):
            print("Taquin isn't solvable, try a new one")
        else:
            open_list = [{"tak": self.tak, "h": 0, "c":0, "cost":0}]
            closed_list = []
            i = 0
            while len(open_list):
                current = open_list.pop(0)
                if current["tak"] == self.model:
                    print(current)
                    return True
                neighbours = self.find_all_neighbours(current["tak"])
                to_insert = []
                for each in neighbours:
                    new = {"tak":each, "h":self.heuristic["newton"](each) ,"c": current["c"] + 1}
                    new["cost"] = new["h"] + new["c"]
                    to_insert.append(new)
                to_insert.sort(key=lambda x: x['cost'], reverse=True)
                for each in to_insert:
                    if self.isInList(each, open_list, closed_list):
                        i += 1
                        pass
                    else:
                        open_list.insert(0, each)
                if i % 300 == 0:
                    print('open :', len(open_list))
                closed_list.append(current)
                open_list.sort(key=lambda x: x['cost'], reverse=False)
                
                



