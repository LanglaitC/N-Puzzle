import sys

comment_charac = '#'

def check_validity(tab, dim):
    '''Function that goes through the parsed result and throws an error if it is of invalid dimension, contains any duplicate or any character out of valid range'''
    vert_dim = len(tab)
    hash_tab = {}  ## Hash tab is filed as we go through the parsed taquin to easily detect duplicates
    if vert_dim < 2:
        raise Exception("Your taquin should be at least 2x2")
    if vert_dim != dim: ## Check if the given taquin got as much line as column, else it is not a valid one
        raise Exception("Invalid file, taquin should be a square")
    for i in range(dim):
        for j in range(dim):
            if tab[i][j] >= dim * dim or tab[i][j] < 0:
                raise Exception("Character " + str(tab[i][j])+ " is out of range should be between 0 and " + str(dim * dim - 1) + ", position : (" + str(i + 1) + "," + str(j + 1) + ")")
            if tab[i][j] not in hash_tab:
                hash_tab[tab[i][j]] = 1
            else:
                raise Exception("Duplicate Character " + str(tab[i][j]) + " at position : (" + str(i + 1) + "," + str(j + 1) + ")")
    return tab

def parse_line(line):
    '''Function that transforms a lign into an array containing numbers, throws an arry if it encounters anything else than letters and whitespaces'''
    convert = []
    for each in line.split():
        try:
            if each[0] == comment_charac: ## If comment character is detected stop analysing the line
                break 
            convert.append(int(each))  ## If the element can't be converted to int then it contains letters and is not a valid element
        except Exception as e:
            raise e
    if len(convert) == 0:   ## File contains an empty line, it is not valid
        return False
    return convert

def is_comment(line):
    '''Function that states if a given line is a commnent'''
    if (not line or not isinstance(line, str)):
        return False
    for each in line:
        if each in ' \t':
            pass
        elif each == comment_charac:   ## Return true if it encounters nothing but whitespaces between start of the line and the first #
            return True
        else:               ## Else return false, the line is not a comment
            return False
    return False            ## If no # is encountered, the lign is empty or filled with whitespaces and is not valid
    
def parse_file(file):
    '''Function that parses the file to check it and return a new taquin instance based on its content'''
    try:
        fd = open(file)
        content = fd.read().split('\n')
    except Exception:
        raise Exception("File doesn't exist or isn't valid format")
    result = []
    dim = None
    for line in content:
        if (is_comment(line)):       ## If the lign is a comment we pass to the next one
            pass
        else:                        ##  Else we transform it into an array and add it to the final result
            convert = parse_line(line)
            if not convert: ## If we encounter empty line break
                break
            if dim is not None and dim != len(convert): ## If the dimension is different from the previously parsed lign, the taquin is not valid
                raise Exception("Invalid file, taquin should be a square")
            dim = len(convert)
            result.append(convert)
    result = check_validity(result, dim)
    return result