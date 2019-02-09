import parse
import sys
from model import *
from puzzle import *
from generator import createPuzzle

try:
    ##TODO if no argument is given make a random puzzle
    res = parse.parse_file(sys.argv[1]) if len(sys.argv) > 1 else createPuzzle(4)
    model = Model(len(res))
    # print(tak)
except Exception as e:
   raise(e)
tak = Puzzle(res, model.model, model.model_dic)

