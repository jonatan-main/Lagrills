scal3 = 10000
sunpos1 = PVector(0.0)
sunPos = PVector(500,400)

def keyPressed():
    if keyCode == 38:
        scal += 50
    if keyCode == 40:
        scal -= 50
def keyReleased():
    if keyCode == 38:
        scal += 0
    if keyCode == 40:
        scal +=0
Grav_con = 6.67408*10**-11

class Body(object):
    def __init__(self, Mass, EQ_rad, X, Y):
        self.Mass = Mass
        self.EQ_rad = EQ_rad
        self.pos = PVector(X,Y)
        self.normPos = PVector(X,Y)
            
    def display(self):
        fill(247, 247 ,0)
        ellipse(self.pos[0], self.pos[1], self.EQ_rad/scal3, self.EQ_rad/scal3)
        
class Earth(Body):
    def __init__(self, Mass, EQ_rad, X, Y, Vxo, Vyo):
        self.Mass = Mass
        self.EQ_rad = EQ_rad
        self.pos = PVector(X,Y)
        self.v = PVector(Vxo, Vyo)
        self.initpos = PVector(X,Y)
        
    def display(self):
        fill(2, 124 ,188)
        ellipse(self.pos[0], self.pos[1], self.EQ_rad/scal3, self.EQ_rad/scal3)
       

  #def gravity(self, other):
        #disp = 
        
def setup():
    size(1000, 800)
    global sun,earth
    
    
    sun = Body(1.89*10**30, 696340, width/2, height/2)
    earth = Earth(5.97*10**24, 63780*5, width/2, height/2 + 1480000/scal3*2, 5, 0)
    #grav = Force(earth.Mass, sun.Mass, 1480000)
    #L1 = L1_point(earth.Mass, sun.Mass, 1480000)
    
def draw():
    background(255)
    sun.display()
    locSun = sun.normPos
    acc = PVector (locSun[0]-earth.pos[0],locSun[1]-earth.pos[1])
    acc.mult(0.0002)
    earth.v.add(acc)
    earth.pos.add(earth.v)
   
    #line(earth.pos[0],earth.pos[1], locSun[0],locSun[1])
    #line(300,400+1480000/scal3*2,700,400+1480000/scal3*2)
    
    noFill()
    ellipse(sun.pos[0],sun.pos[1],sun.pos[0]+210,200+sun.pos[1])
    earth.display()
    #keyPressed()
    #keyReleased()


def Force(Mass1, Mass2, Dist):
    return [Grav_con*Mass1*Mass2/Dist**2]
    
  
def L1_point(M1, M2, Dist):
    return [Dist*((M2/(3*M1))**(1/3))]


        
    
    
    
