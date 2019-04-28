import math

cote = 50
colonnes = 28
lignes = 18
points = []
portee = 6


def setup():
    size(colonnes*cote,lignes*cote)


def draw():
    global points
    points = [[PVector(i*cote,j*cote) for j in range(lignes+1)] for i in range(colonnes+1)]
    for i in range(colonnes+1):
        for j in range(lignes+1):
            points[i][j] = distort(points[i][j],portee)
    for i in range(colonnes):
        for j in range(lignes):
            couleur = (i+j)%2 * 255
            case(i,j,couleur)
    
    
def case(i,j,couleur):
    fill(couleur);
    stroke(couleur);
    beginShape();
    vertex(points[i][j].x,points[i][j].y,);
    vertex(points[i+1][j].x,points[i+1][j].y,);
    vertex(points[i+1][j+1].x,points[i+1][j+1].y,);
    vertex(points[i][j+1].x,points[i][j+1].y,);
    endShape(CLOSE);

def vibre(point,casePortee):
    mousePos = PVector(mouseX, mouseY)
    distance = point.dist(mousePos)
    porte = cote*casePortee
    amplitudemax = cote / 4
    amplitude = amplitudemax * (1 - distance / porte)
    if distance > 0  and distance<porte:
        point = point.add(PVector(random(-amplitude,amplitude),random(-amplitude,amplitude)))
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
    s = 0.01
    mousePos = PVector(mouseX, mouseY)
    distance = point.dist(mousePos)
    portee = cote*casePortee
    if distance > 0  and distance<portee:
        ratio = distance/portee
        rayon = PVector.sub(point,mousePos)
        #point = PVector.add(point,PVector((noise(rayon.x)-0.5)*cote/2,(noise(rayon.y)-0.5)*cote/2))
        #point = PVector.add(point,PVector((noise(point.x)-0.5)*cote,(noise(point.y)-0.5)*cote))
        point = PVector.add(point,PVector((noise(point.x*s,mousePos.y*s)-0.5)*cote*2,(noise(point.y*s,mousePos.y*s)-0.5)*cote*2).mult(1-ratio))
        #point = PVector.add(point,rayon.mult(noise(rayon.x,rayon.y)/10))
        #point = PVector.add(point,rayon.mult(noise(point.x,point.y)/5))
        #point = PVector.add(point,rayon.mult(noise(point.x,point.y)/5))
    return point


def creux(point,casePortee):
    mousePos = PVector(mouseX, mouseY)
    distance = point.dist(mousePos)
    porte = cote*casePortee
    if distance > 0  and distance<porte:
        coef = (porte-distance)/(porte)
        point = point.add(mousePos.sub(point).mult(sin(coef)))
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
