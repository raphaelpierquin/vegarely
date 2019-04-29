import math

cote = 50
colonnes = 28
lignes = 18
origines = []
points = []
portee = 6
ticPrecedent = 0

def setup():
    size(colonnes*cote,lignes*cote)
    global origines, points
    origines = [[PVector(i*cote,j*cote) for j in range(lignes+1)] for i in range(colonnes+1)]
    points = [[PVector(i*cote,j*cote) for j in range(lignes+1)] for i in range(colonnes+1)]
    ticPrecedent=millis()


def draw():
    global origines, points
    cibles = [[distort(origines[i][j],portee) for j in range(lignes+1)] for i in range(colonnes+1)]
    tic=millis()
    deplaceVers(points,cibles,tic-ticPrecedent)
    ticPrecent=tic
    dessineGrille(points)

def dessineGrille(grille):
    for i in range(colonnes):
        for j in range(lignes):
            couleur = (i+j)%2 * 255
            dessineCase(grille,i,j,couleur)

def deplaceVers(points,cibles,delai):
    for i in range(colonnes):
        for j in range(lignes):
            point = points[i][j]
            cible = cibles[i][j]
            vecteur = PVector.sub(cible,point)
            distance = vecteur.mag()
            if distance > 10:
                vecteur.mult(10/distance)
            point.add(vecteur)


def dessineCase(grille,i,j,couleur):
    fill(couleur);
    stroke(couleur);
    beginShape();
    vertex(grille[i][j].x,grille[i][j].y,);
    vertex(grille[i+1][j].x,grille[i+1][j].y,);
    vertex(grille[i+1][j+1].x,grille[i+1][j+1].y,);
    vertex(grille[i][j+1].x,grille[i][j+1].y,);
    endShape(CLOSE);

def vibre(point,casePortee):
    mousePos = PVector(mouseX, mouseY)
    distance = point.dist(mousePos)
    porte = cote*casePortee
    amplitudemax = cote / 4
    amplitude = amplitudemax * (1 - distance / porte)
    if distance > 0  and distance<porte:
        point = PVector.add(point,PVector(random(-amplitude,amplitude),random(-amplitude,amplitude)))
    return point

def sphere(point,casePortee):
    mousePos = PVector(mouseX, mouseY)
    distance = point.dist(mousePos)
    portee = cote*casePortee
    if distance > 0  and distance<portee:
        ratio = distance/portee
        rayon = PVector.sub(point,mousePos)
        point = PVector.add(point,rayon.mult(1-ratio))
    return point

def tourbillon(point,casePortee):
    mousePos = PVector(mouseX, mouseY)
    distance = point.dist(mousePos)
    portee = cote*casePortee
    if distance > 0  and distance<portee:
        ratio = distance/portee
        rayon = PVector.sub(point,mousePos)
        point = PVector.add(mousePos,rayon.rotate((1-ratio)*(1-ratio)*math.pi/3))
    return point

def bruit(point,casePortee):
    s = 0.005
    mousePos = PVector(mouseX, mouseY)
    distance = point.dist(mousePos)
    portee = cote*casePortee
    if distance > 0  and distance<portee:
        ratio = distance/portee
        perturbation = PVector((noise(point.x*s,mousePos.y*s)-0.5)*cote*2,(noise(point.y*s,mousePos.x*s)-0.5)*cote*2)
        point = PVector.add(point,perturbation.mult(1-ratio))
    return point


def creux(point,casePortee):
    mousePos = PVector(mouseX, mouseY)
    distance = point.dist(mousePos)
    porte = cote*casePortee
    if distance > 0  and distance<porte:
        coef = (porte-distance)/(porte)
        point = PVector.add(point,mousePos.sub(point).mult(sin(coef)))
    return point

distortions = [bruit,
               tourbillon,
               sphere,
               creux,
               vibre,
               lambda pi,po: sphere(tourbillon(pi,po),po-2),
              ]
distort = distortions[0]

def mouseClicked():
    global distortions,  distort
    index=distortions.index(distort)
    distort=distortions[(index+1) % len(distortions)]
