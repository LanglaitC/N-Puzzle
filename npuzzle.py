import parse;
import sys;
from model import *;

try:
    ##TODO if no argument is given make a random puzzle
    res = parse.parse_file(sys.argv[1]);
    Model(res); 
except Exception as e:
    raise e;
    exit(1);

