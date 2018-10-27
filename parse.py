import sys

def parse_file(file):
    '''Fonction that parses the file to create a new taquin instance'''
    try:
        fd = open(file);
        content = fd.read().split('\n');
    except Exception as e:
        raise e;
    if content == "":
        raise Exception("File is empty");
    result = []
    for line in content:
        if (line[0] == '#'):
            print("comment");
        else:
            result.push(line);