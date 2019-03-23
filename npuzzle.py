import parse
import sys
from model import *
from solvability import *
from solve import *
from generator import createPuzzle

try:
    tak = parse.parse_file(sys.argv[1]) if len(sys.argv) > 1 else createPuzzle(3)
    model = Model(len(tak))
    solvable = Solvability(tak, model.model).solvable
    if not solvable:
        print('N-Puzzle is not solvable')
        exit()
except Exception as e:
    sys.stderr.write(str(e) + '\n')
    sys.exit()
print('👋   Ok, we have a puzzle to solve. What algorithm shall we use ? 💁')
print('1. A*')
print('2. Greedy Search')
print('3. Uniform cost')
try:
    heuristic = 0
    algo = int(input('>  '))
    if abs(algo) > 3 or algo == 0:
        raise(True)
    if algo != 3:
        print('👌  And, what about heuristic ?')
        print('1. Manhattan 🚕')
        print('2. Out of place 🌴')
        print('3. Euclidian 📐')
        print('4. Linear conflict ⚔️')
        heuristic = int(input('>  '))
        if abs(heuristic) > 4 or heuristic == 0:
            raise(True)
except:
    print('Invalid input 🤷‍♀️')
    exit()

tak = Solve(tak, model.model, model.model_dic, heuristic, greedy=algo == 2, uniform_cost=algo == 3)