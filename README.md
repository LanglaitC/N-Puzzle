# N-Puzzle
Un projet algorithmique issu de l'ecole 42. 
L'objectif est de resoudre un taquin passe en argument

## Usage
On definit un taquin dans un fichier txt
Format du fichier txt

`#` permet de commenter une ligne du fichier
La premier ligne non commente doit contenir la dimension du taquin sous la forme
d'un chiffre : ex "3" pour un puzzle 3x3
Le restant des lignes est dedie a la definition du taquin ex:
4
12 9  1  3
14 2  6  7
4  5  10 11
8  13 15 

## Valeur de retour
On retourne :
- le nombre de mouvements optimal necessaires pour arriver de l'etat initial a
a la solution selon notre algorithme.
- la sequence ordonne de tout les etats selon les mouvements trouves par notre
  algoritme. Si l'etat initial est insolvable, l'utilisateur est informe et le
  programme exit de lui meme.

