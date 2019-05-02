import math

## uncomment when launching from command line
from processing.pdf.PGraphicsPDF import PDF

## uncomment when launching from IDE
#add_library('pdf')

cote = 30
colonnesVisibles = 41
lignesVisibles = 27
marges = 2
origines = []
points = []
portee = 6
force = 0.5
ticPrecedent = 0
colonnes = colonnesVisibles + 2*marges
lignes = lignesVisibles + 2*marges
printing=False

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
    global origines, points, ticPrecedent, portee, force
    cibles = [[distort(origines[i][j],portee,force) for j in range(lignes+1)] for i in range(colonnes+1)]
    tic=millis()
    deplaceVers(points,cibles,tic-ticPrecedent)
    ticPrecedent=tic
    startPrinting()
    dessineGrille(points)
    endPrinting()

def startPrinting():
    global printing
    if printing:
        filename="/tmp/damier-####.pdf"
        print("printing to " + filename + "...")
        beginRecord(PDF, filename )

def endPrinting():
    global printing
    if printing:
        endRecord()
        print("... done.")
        printing = False

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
            ladistance = vecteur.mag()
            if ladistance > 0 and ladistance > deplacementMax:
                vecteur.mult(deplacementMax/ladistance)
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
    def df(point,casePortee,force):
        mousePos = PVector(mouseX, mouseY)
        ladistance = distance(point,mousePos)
        portee = cote*casePortee
        if ladistance>portee:
            return point
        coef = 1 - ladistance/portee
        return distortion(point,mousePos,coef,force)
    return df

def distanceEuclidienne(p1,p2):
    return p1.dist(p2)

ratiomagique = (1+sqrt(2))/2
def distanceMax(p1,p2):
    global ratiomagique
    rayon = PVector.sub(p1,p2)
    return max(abs(rayon.x),abs(rayon.y))*ratiomagique

def distanceAdd(p1,p2):
    global ratiomagique
    rayon = PVector.sub(p1,p2)
    return (abs(rayon.x)+abs(rayon.y))/ratiomagique

distance=distanceEuclidienne
distances=[distanceEuclidienne,distanceMax,distanceAdd]

def vibre(point,mousePos,coef,force):
    amplitudemax = cote / 4 * force
    amplitude = amplitudemax * coef
    point = PVector.add(point,PVector(random(-amplitude,amplitude),random(-amplitude,amplitude)))
    return point


def sphere(point,mousePos,coef,force):
    rayon = PVector.sub(point,mousePos)
    l = (force - 0.4) * 10
    coef = coef ** l
    point = PVector.add(point,rayon.mult(coef))
    return point

def tourbillon(point,mousePos,coef,force):
    angleMax = math.pi/3*2*force
    rayon = PVector.sub(point,mousePos)
    point = PVector.add(mousePos,rayon.rotate(coef*coef*angleMax))
    return point

def bruit(point,mousePos,coef,force):
    s = 0.005
    perturbation = PVector((noise(point.x*s,mousePos.y*s)-0.5)*cote*2,(noise(point.y*s,mousePos.x*s)-0.5)*cote*2)
    point = PVector.add(point,perturbation.mult(coef*force*2))
    return point

def creux(point,mousePos,coef,force):
    point = PVector.add(point,mousePos.sub(point).mult(sin(coef*force*2)))
    return point

def idem(point,casePortee,force):
    return point

distortions = [idem,
               focalise(sphere),
               focalise(creux),
               focalise(tourbillon),
               focalise(vibre),
               focalise(lambda p,m,c,f: sphere(tourbillon(p,m,c,f),m,c,f)),
               focalise(bruit),
              ]
distort = distortions[0]
nextDistortion = distortions[1]

def mouseClicked():
    global distortions, distort, nextDistortion, noMoveYet
    freeze()
    noMoveYet = True
    nextDistortion = distort
    distort = distortions[0]

noMoveYet=True
def mouseMoved():
    global noMoveYet, distort, distortions, nextDistortion
    if noMoveYet:
        noMoveYet = False
        distort = nextDistortion

def keyPressed():
    global distortions, distort, distances, distance, portee, force, printing, noMoveYet, nextDistortion, origines
    if key==' ':
        index = distortions.index(distort)
        distort = distortions[(index+1) % len(distortions)]
        distance = distances[0]
        force = 0.5
    elif key=='c':
        origines = grilleCarre()
    elif key=='q':
        exit()
    elif keyCode==UP:
        portee+=1
    elif keyCode==DOWN:
        portee-=1
    elif keyCode==RIGHT:
        force+=0.1
    elif keyCode==LEFT:
        force-=0.1
    elif key=='d':
        index = distances.index(distance)
        distance = distances[(index+1) % len(distances)]
    elif key=='p':
        printing = True
