import parse;
import sys;

try:
    parse.parse_file(sys.argv[1]);   
except Exception as e:
    raise e;
    exit(1);
