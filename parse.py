import sys

def check_validity(tab, dim):
    vert_dim = len(tab);
    hash_tab = {};
    if vert_dim < 2:
        raise Exception("File is not valid format");
    if vert_dim != dim:
        raise Exception("Invalid file, taquin should be a square");
    for i in range(dim):
        for j in range(dim):
            if tab[i][j] >= dim * dim or tab[i][j] < 0:
                raise Exception("Character " + str(tab[i][j])+ " is out of range should be between 0 and " + str(dim * dim - 1) + ", position : (" + str(i + 1) + "," + str(j + 1) + ")");
            if tab[i][j] not in hash_tab:
                hash_tab[tab[i][j]] = 1;
            else:
                raise Exception("Duplicate Character " + str(tab[i][j]) + " at position : (" + str(i + 1) + "," + str(j + 1) + ")");
    return tab;

def parse_line(line):
    convert = [];
    for each in line.split():
        try:
            convert.append(int(each));
        except Exception as e:
            raise e;
    if len(convert) == 0:
        raise Exception("Lign is empty");
    return convert;

def is_comment(line):
    '''Function that states if a given line is a commnent'''
    if (not line or not isinstance(line, str)):
        return False;
    for each in line:
        if each in ' \t':
            pass;
        elif each == '#':
            return True;
        else:
            return False;
    return False;
    
def parse_file(file):
    '''Function that parses the file to check it and return a new taquin instance based on its content'''
    try:
        fd = open(file);
        content = fd.read().split('\n');
    except Exception as e:
        raise Exception("File doesn't exist or isn't valid format");
    if content == "":
        raise Exception("File is empty");
    result = [];
    dim = None;
    for line in content:
        if (is_comment(line)):       ##  Si la ligne commence par une diese c'est un commentaire
            pass
        else:                        ##  Sinon on verifie que chaque element de la ligne est un nombre entier et on le convertit en int
            convert = parse_line(line);
            if dim is not None and dim != len(convert):
                raise Exception("Invalid file, taquin should be a square");
            dim = len(convert);
            result.append(convert);
    result = check_validity(result, dim);
    return result;