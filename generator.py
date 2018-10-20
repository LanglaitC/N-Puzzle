import sys;
import random;

##  function to find the number of digits of the max number of the puzzle
##  so we can apply a padding to all numbers and the final writing is smooth

def find_padding(max):
    i = 10;
    res = 1;
    while max / i >= 1:
        res += 1;
        i *= 10;
    return(res);

if len(sys.argv) != 2:
    sys.stderr.write("usage generator.py [dimension taquin]\n");
    exit(1);

try:
    dim = int(sys.argv[1]);
    if dim >= 100 or dim <= 0:
        raise Exception("number should be between 1 and 99");
except Exception as e:
    sys.stderr.write(str(e)+"\n");
    sys.stderr.write("usage generator.py x [dimension taquin (0 < x < 100)]\n");
    exit(1)

##  fill an array with the right number of elements depending on the puzzle dimension
##  asked from the user then write it on the random.txt file

res = [];
for x in range(dim):
    res += range(x * dim, (x+1) * dim);

random.shuffle(res);
f = open('random.txt', "w+")
padding = find_padding(dim * dim);
f.write("## Randomly generated taquin of dimension "+ str(dim) +" ##\n");
for x in range(dim):
    f.write(' '.join(str(e).ljust(padding) for e in res[x * dim: (x + 1) * dim])+"\n");