from heuristic import*;
import copy
class A_star:
    def __init__(self, res, model):
        self.opened = []
        self.closed = []
        self.index = 2
        self.dim = len(res)
        self.success = False
        self.res = res
        self.model = model
        self.begin = self.begin()
        self.solution = self.solution()
        self.algo()

    def begin(self):
        self.begin = {}
        h = Heuristic(self.res, self.model)
        self.begin = {
            "matrix":self.res,
            "h":h.mannhathan(),
            "g":0,
            "id":1,
            "ancestors":[]
        }
        # print ('begin', self.begin)
        return self.begin

    def solution(self):
        self.solution = {}
        self.solution = {
            "matrix":self.model,
            "id":0
        }
        return self.solution

    def select_with_strategy(self):
        min = self.opened[0]
        for item in self.opened:
            if item != min and ((item["h"] + item["g"]) < (min["h"] + min["g"])):
                min = item
        return min

    def create_elem(self, matrix, e):
        elem = {}
        h = Heuristic(matrix, self.model)
        elem = {
            "matrix":matrix,
            "id":self.index,
            "h":h.mannhathan(),
            "g":0,
            "ancestors":[]
        }
        self.index += 1
        return elem

    def is_not_ancestor(self, matrix, e):
        present = True
        for elem in e["ancestors"]:
            if matrix == elem["matrix"]:
                present = False
                break
        return present



    def expand(self, e):
        states = []
        for i in range(self.dim):
            for j in range(self.dim):
                if e['matrix'][i][j] == 0:
                    x0 = j
                    y0 = i
                    break
        if x0 != 0:
            matrix = copy.deepcopy(e["matrix"])
            matrix[y0][x0 - 1],matrix[y0][x0] = matrix[y0][x0],matrix[y0][x0 - 1]
            if self.is_not_ancestor(matrix, e):
                elem = self.create_elem(matrix, e)
                states.append(elem)
        if x0 != self.dim - 1:
            matrix = copy.deepcopy(e["matrix"])
            matrix[y0][x0 + 1],matrix[y0][x0] = matrix[y0][x0],matrix[y0][x0 + 1]
            if self.is_not_ancestor(matrix, e):
                elem = self.create_elem(matrix, e)
                states.append(elem)
        if y0 != 0:
            matrix = copy.deepcopy(e["matrix"])
            matrix[y0 - 1][x0],matrix[y0][x0] = matrix[y0][x0],matrix[y0 - 1][x0]
            if self.is_not_ancestor(matrix, e):
                elem = self.create_elem(matrix, e)
                states.append(elem)
        if y0 != self.dim - 1:
            matrix = copy.deepcopy(e["matrix"])
            matrix[y0 + 1][x0],matrix[y0][x0] = matrix[y0][x0],matrix[y0 + 1][x0]
            if self.is_not_ancestor(matrix, e):
                elem = self.create_elem(matrix, e)
                states.append(elem)
        sorted_states = sorted(states, key=lambda k: k['h'])
        return sorted_states

    def is_present_in_either(self, matrix):
        present = False
        for el in self.opened:
            if el["matrix"] == matrix:
                present = True
                break
        if present == False:
            for el in self.closed:
                if el["matrix"] == matrix:
                    present = True
                    break
        return present

    def is_present_in_closed(self, matrix):
        present = False
        for el in self.closed:
            if el["matrix"] == matrix:
                present = True
                break
        return present


    def algo(self):
        self.opened.append(self.begin)
        while self.opened and not self.success:
        # i = 0
        # while i < 5 and self.opened:
            # i += 1
            e = self.select_with_strategy()
            self.success = (e['matrix'] == self.solution['matrix'])
            if self.success == True:
                print ('E', e)
            if not self.success:
                self.opened.remove(e)
                self.closed.append(e)
                states = self.expand(e)
                # print ("NEW LEVEL")
                # print ('E_CURRENT', e)
                # print ('states', states)
                for s in states:
                    if not self.is_present_in_either(s["matrix"]):
                        self.opened.append(s)
                        s["ancestors"].append(e)
                        s["g"] = e["g"] + 1
                        # print ("ABSENT")
                    else:
                        if (s["g"] + s['h']) > e["g"] + 1 + s["h"]:
                            s["g"] = e["g"] + 1
                            s["ancestors"].append[e]
                            if self.is_present_in_closed(s["matrix"]):
                                self.closed.remove(s)
                                self.opened.append(s)
                                # print ("INTO CLOSED")
                    #         else:
                    #             print ("INTO OPENED")
                    # print ('s', s)
        if self.success:
            print ("YAY")
            # print ('opened', self.opened)




    # def check(self):
    #     test_1 = {}
    #     test_1 = {
    #         "matrix":self.res,
    #         "h":200,
    #         "g":300,
    #         "id":1
    #     }
    #     test_2 = {}
    #     test_2 = {
    #         "matrix":self.model,
    #         "h":0,
    #         "g":0,
    #         "id":0
    #     }
    #     self.opened.append(test_2)
    #     self.opened.append(test_1)
    #     print ('els', self.opened)
    #     self.opened.remove(test_2)
    #     print ('els', self.opened)
    #     cmp = (test_2['matrix'] == test_1['matrix'])
    #     print ('cmp', cmp)
    #     return self.opened