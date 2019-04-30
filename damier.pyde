import math

cote = 50
colonnesVisibles = 28
lignesVisibles = 18
marges = 2
origines = []
points = []
portee = 6
ticPrecedent = 0
colonnes = colonnesVisibles + 2*marges
lignes = lignesVisibles + 2*marges

def setup():
    size(colonnesVisibles*cote,lignesVisibles*cote)
    global origines, points, ticPrecedent
    origines = grilleCarre()
    points = grilleCarre()
    ticPrecedent=millis()


def grilleCarre():
    global marges, colonnes, lignes, cote
    return [[PVector(i*cote,j*cote) for j in range(-marges,lignes+1)] for i in range(-marges,colonnes+1)]

def draw():
    global origines, points, ticPrecedent, portee
    cibles = [[distort(origines[i][j],portee) for j in range(lignes+1)] for i in range(colonnes+1)]
    tic=millis()
    deplaceVers(points,cibles,tic-ticPrecedent)
    ticPrecedent=tic
    dessineGrille(points)

def freeze():
    global origines, points
    origines = [[points[i][j].copy() for j in range(lignes+1)] for i in range(colonnes+1)]

def dessineGrille(grille):
    for i in range(colonnes):
        for j in range(lignes):
            couleur = (i+j)%2 * 255
            dessineCase(grille,i,j,couleur)

def deplaceVers(points,cibles,delai):
    deplacementMax=0.1*delai
    for i in range(1,colonnes):
        for j in range(1,lignes):
            point = points[i][j]
            cible = cibles[i][j]
            vecteur = PVector.sub(cible,point)
            distance = vecteur.mag()
            if distance > deplacementMax:
                vecteur.mult(deplacementMax/distance)
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


def focalise(distortion):
    def df(point,casePortee):
        mousePos = PVector(mouseX, mouseY)
        distance = point.dist(mousePos)
        portee = cote*casePortee
        if distance>portee:
            return point
        coef = 1 - distance/portee
        return distortion(point,mousePos,coef)
    return df

def vibref(point,mousePos,coef):
    amplitudemax = cote / 4
    amplitude = amplitudemax * coef
    point = PVector.add(point,PVector(random(-amplitude,amplitude),random(-amplitude,amplitude)))
    return point


def spheref(point,mousePos,coef):
    rayon = PVector.sub(point,mousePos)
    point = PVector.add(point,rayon.mult(coef))
    return point

def tourbillonf(point,mousePos,coef):
    rayon = PVector.sub(point,mousePos)
    point = PVector.add(mousePos,rayon.rotate(coef*coef*math.pi/3))
    return point

def bruitf(point,mousePos,coef):
    s = 0.005
    perturbation = PVector((noise(point.x*s,mousePos.y*s)-0.5)*cote*2,(noise(point.y*s,mousePos.x*s)-0.5)*cote*2)
    point = PVector.add(point,perturbation.mult(coef))
    return point


def creuxEtoilef(point,mousePos,coef):
    point = PVector.add(point,mousePos.sub(point).mult(sin(coef)))
    return point

racine_de_deux = sqrt(2)
def creux2(point,casePortee):
    global racine_de_deux
    mousePos = PVector(mouseX, mouseY)
    rayon = PVector.sub(point,mousePos)
    distance = max(abs(rayon.x),abs(rayon.y))*racine_de_deux
    portee = cote*casePortee
    if distance>portee:
        return point
    coef = 1 - distance/portee
    point = PVector.add(point,mousePos.sub(point).mult(sin(coef)))
    return point

def idem(point,casePortee):
    return point

distortions = [idem,
               focalise(bruitf),
               focalise(tourbillonf),
               focalise(spheref),
               focalise(creuxEtoilef),
               creux2,
               focalise(vibref),
               focalise(lambda p,m,c: spheref(tourbillonf(p,m,c),m,c)),
              ]
distort = distortions[0]

def mouseClicked():
    global distortions,  distort
    index = distortions.index(distort)
    distort = distortions[(index+1) % len(distortions)]

def keyPressed():
    global distortions, distort, portee
    if key=='\n':
        freeze()
        distort = distortions[0]
    elif key=='q':
        exit()
    elif keyCode==UP:
        portee+=1
    elif keyCode==DOWN:
        portee-=1
