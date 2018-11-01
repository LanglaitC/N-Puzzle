import parse;
import sys;
from model import *;
from puzzle import *;

try:
    ##TODO if no argument is given make a random puzzle
    res = parse.parse_file(sys.argv[1]);
    model = Model(len(res)).model;
    print(Model(len(res)));
    tak = Puzzle(res, model)
    # print(tak)
except Exception as e:
   raise e;
   exit(1);

