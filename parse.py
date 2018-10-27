import sys

def parse_file(file):
    '''Fonction that parses the file to check it and return a new taquin instance based on its content'''
    try:
        fd = open(file);
        content = fd.read().split('\n');
    except Exception as e:
        raise Exception("File doesn't exist or isn't valid format");
    if content == "":
        raise Exception("File is empty");
    result = [];
    for line in content:
        if (line and line[0] == '#'):       ##  Si la ligne commence par une diese c'est un commentaire
            pass
        else:
            convert = [];                   ##  Sinon on verifie que chaque element de la ligne est un nombre entier et on le convertit en int
            for each in line.split():
                try:
                    convert.append(int(each));
                except Exception as e:
                    raise e;
            result.append(convert);
    if len(result) < 2:
        raise Exception("File is not valid format");
    return result;
                