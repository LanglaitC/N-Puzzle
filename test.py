liste = []
dico = {}
new = {'c': 'test', 'f': 'test1'}
liste.append(new)
dico['new'] = new
to_change = new
new['f'] = 'qwe'
print(dico, liste)