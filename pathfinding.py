"""
# PROJET
*Recherche de chemin optimal*


Que ce soit dans le cadre de la robotique, des jeux vidéos ou de la vie de tous les jours,
on aime souvent passer par le chemin le plus court. Mais comment trouver ce chemin ? C’est
l’objectif de ce projet. Pour s’initier à ce problème nous travaillerons dans un espace défini sous
forme d’une grille 2D avec des obstacles prédéfinis. L’objectif sera alors de trouver le chemin le plus court d’un point A à un
point B en passant de pixel à pixel, puis de l'afficher.


Tout d'abord il est important d'importer lesmlibrairies nécessaires au projet, voici le code ci-dessous :
"""

import numpy as np # Pour manipuler des tableaux de nombres
import matplotlib.pyplot as plt # pour afficher des images
import time # qui nous servira à calculer le temps mis par notre algorithme
import random # qui nous sera utile dans la fonction random_points

"""
Pour se faciliter la vie, c'est une bonne idée de créer quelques fonctions qui nous serons utiles tout au long du programme. 
Les voici :
"""

# création d'une image
def creer_image(hauteur, largeur):
  return np.ones((hauteur, largeur))*255

# montrer une image
def montrer_image(image):
  plt.imshow(image, cmap='terrain',vmin = 0, vmax = 255)
  plt.show()

"""
Il faut ensuite créer un monde, avec des obstacles (qui auront une valeur de -1), en 2D et le visualiser sous forme de graphique grâce à matplotlib :
"""

hauteur = 20
largeur = 20

# création du monde
monde = creer_image(hauteur, largeur)

# dessiner les obstacles
monde[5, :-5] = -1
monde[10, 5:] = -1
monde[15, :-5] = -1

# afficher le monde
plt.title("Monde avec murs")
montrer_image(monde)

"""
Il faut maintenant définir un point de départ (le point A) et un point d'arrivée (le point B).
"""

# Point A
monde[0, 0] = 100

# Point B
monde[18, 2] = 100

# afficher le monde
plt.title("Monde avec points")
montrer_image(monde)

"""
Il faut maintenant utiliser un algorithme appelé pathfinding pour numéroter tous les pixels de l'image en fonction de leur distance, en partant de notre point A qui a une valeur de 0. Puis nous allons afficher la longueur du chemin entre les points A et B, avant d'afficher le chemin sur l'image.
"""

# fonction is_pixel_in_image_or_wall pour vérifier si le pixel est dans l'image ou non, ou si le pixel est un mur
def is_pixel_in_image_or_wall(image, cord_y, cord_x):
  if cord_y >= image.shape[0] or cord_y < 0 or cord_x >= image.shape[1] or cord_x < 0:
    return False
  if image[cord_y, cord_x] == -1:
    return False
  else:
    return True

# fonction distance qui assigne une valeur différente
# à chaque pixel qui n'est pas un obstacle
def pathfinding(image, point_a):
  liste_principale = []
  liste_principale.append((point_a[0], point_a[1], 0))

  visited = np.zeros((image.shape)) # nouvelle image pour savoir quels pixels ont déjà été visités
  visited[point_a[0], point_a[1]] = 1

  for element in liste_principale:
    liste_adjacent = []

    if is_pixel_in_image_or_wall(monde, element[0]-1, element[1]) == True and visited[element[0]-1, element[1]] == 0:
      liste_adjacent.append((element[0]-1, element[1], element[2]+1))
      visited[element[0]-1, element[1]] = 1 
    if is_pixel_in_image_or_wall(monde, element[0]+1, element[1]) == True and visited[element[0]+1, element[1]] == 0:
      liste_adjacent.append((element[0]+1, element[1], element[2]+1))
      visited[element[0]+1, element[1]] = 1 
    if is_pixel_in_image_or_wall(monde, element[0], element[1]+1) == True and visited[element[0], element[1]+1] == 0:
      liste_adjacent.append((element[0], element[1]+1, element[2]+1))
      visited[element[0], element[1]+1] = 1 
    if is_pixel_in_image_or_wall(monde, element[0], element[1]-1) == True and visited[element[0], element[1]-1] == 0:
      liste_adjacent.append((element[0], element[1]-1, element[2]+1))
      visited[element[0], element[1]-1] = 1 

    for new_adjacent in liste_adjacent:
      liste_principale.append(new_adjacent)

  return liste_principale

#fonction neighbour_white qui renvoie True si un voisin (dans l'image) est blanc (255)
def neighbour_white(image, cord_y, cord_x):
  if cord_y+1 < image.shape[0] and image[cord_y+1, cord_x] == 255:
    return True
  if image[cord_y-1, cord_x] == 255 and cord_y-1 >= 0:
    return True
  if cord_x+1 < image.shape[1] and image[cord_y, cord_x+1] == 255:
    return True
  if image[cord_y, cord_x-1] == 255 and cord_x-1 >= 0:
    return True
  return False

# fonction trajectoire qui calcule et qui affiche la trajectoire entre le point A (0, 0) et le point B (18, 2)
def trajectoire(image, point_a, point_b):
  longueur = image[point_b[0], point_b[1]]  
  print("Longueur du chemin : {} pixels".format(int(longueur)+1))
  image[point_b[0], point_b[1]] = 255
  for i in range(int(longueur), 0, -1):
    compteur = 0
    for y in range(image.shape[0]):
      for x in range(image.shape[1]):
        if image[y, x] == i and compteur == 0:
          if neighbour_white(image, y, x) == True:
            image[y, x] = 255
            compteur += 1
  image[point_a[0], point_a[1]] = 255

# tests + affichage (pathfinding)
debut = time.process_time()
liste_principale = pathfinding(monde, (0, 0)) # forme => (y, x) !
for element in liste_principale:
  monde[element[0], element[1]] = element[2]
plt.title("Image après pathfinding")
montrer_image(monde)

# affichage chemin (trajectoire)
trajectoire(monde, (0, 0), (18, 2))
plt.title("Chemin entre A et B :")
montrer_image(monde)

print("Durée du programme sans récurrences : {} sec.".format(round(time.process_time() - debut, 2)))

"""
Afin de tester notre algorithme, nous allons sélectionner deux points, A et B, au hasard (ils ne pourront pas être sur un obstacle) et nous allons leur appliquer notre algorithme entier. Tout cela sera fait sur une nouvelle image.
"""

# nouvelle image
map = creer_image(hauteur, largeur)

# dessiner les obstacles
map[5, :-5] = -1
map[10, 5:] = -1
map[15, :-5] = -1

# fonction random_points qui génère 2 points aléatoire sur la map qui ne sont pas des murs
def random_points(image):
  # point 1
  is_wall = True
  while is_wall:
    point_a = (random.randint(0, image.shape[0]-1), random.randint(0, image.shape[1]-1))
    if image[point_a[0], point_a[1]] != -1:
      is_wall = False
  # point 2
  is_wall = True
  while is_wall:
    point_b = (random.randint(0, image.shape[0]-1), random.randint(0, image.shape[1]-1))
    if image[point_b[0], point_b[1]] != -1:
      is_wall = False

  return point_a, point_b

point_a, point_b = random_points(map)

#on dessine les points puis on affiche la map sans le chemin
map[point_a[0], point_a[1]] = 100
map[point_b[0], point_b[1]] = 100

plt.title("Map avec les deux points ({} et {}) :".format(point_a, point_b))
montrer_image(map)

# on applique tout l'algorithme à la map et aux deux points
liste_principale = pathfinding(map, point_a) 
for element in liste_principale:
  map[element[0], element[1]] = element[2]

plt.title("Map après pathfinding :")
montrer_image(map)

trajectoire(map, point_a, point_b)
plt.title("Chemin entre A et B :")
montrer_image(map)

"""
Recréons maintenant notre algorithme en utilisant les récurrences :
"""

# créer un nouveau monde pour tester avec les récurrences
monde2 = creer_image(hauteur, largeur)

# dessiner les obstacles sur le monde 2
monde2[5, :-5] = -1
monde2[10, 5:] = -1
monde2[15, :-5] = -1

# fonction pathfinding_with_recurrence
def pathfinding_with_recurrence(monde2, point):

  monde2[point[0], point[1]] = point[2]

  if is_pixel_in_image_or_wall(monde2, point[0]+1, point[1]) == True and point[2]+1 < monde2[point[0]+1, point[1]]:
    pathfinding_with_recurrence(monde2, (point[0]+1, point[1], point[2]+1))
  if is_pixel_in_image_or_wall(monde2, point[0]-1, point[1]) == True and point[2]+1 < monde2[point[0]-1, point[1]]:
    pathfinding_with_recurrence(monde2, (point[0]-1, point[1], point[2]+1))
  if is_pixel_in_image_or_wall(monde2, point[0], point[1]+1) == True and point[2]+1 < monde2[point[0], point[1]+1]:
    pathfinding_with_recurrence(monde2, (point[0], point[1]+1, point[2]+1))
  if is_pixel_in_image_or_wall(monde2, point[0], point[1]-1) == True and point[2]+1 < monde2[point[0], point[1]-1]:
    pathfinding_with_recurrence(monde2, (point[0], point[1]-1, point[2]+1))


# tests + affichage (pathfinding_with_recurrence)
debut = time.process_time()
pathfinding_with_recurrence(monde2, (0, 0, 0)) # => 0, 0 est le point A, de distance 0
plt.title("Image après pathfinding avec récurrence :")
montrer_image(monde2)

# affichage chemin (trajectoire)
trajectoire(monde2, (0, 0), (18, 2))
plt.title("Chemin entre A et B :")
montrer_image(monde2)

print("Durée du programme avec récurrences : {} sec.".format(round(time.process_time() - debut, 2)))