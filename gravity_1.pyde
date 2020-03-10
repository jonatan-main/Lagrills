

def keyPressed():
    
    if keyCode == UP:
        scal += 50
    if keyCode == DOWN:
        scal -= 50
        
def keyReleased():
    if keyCode == UP:
        scal += 0
    if keyCode == DOWN:
        scal +=0

scal3 = 10000

class Body(object):
    def __init__(self, Mass, EQ_rad, X, Y):
        self.Mass = Mass
        self.EQ_rad = EQ_rad
        self.pos = list((X,Y))
        
    def display(self):
        fill(247, 247 ,0)
        ellipse(self.pos[0], self.pos[1], self.EQ_rad/scal3, self.EQ_rad/scal3)
        
class Earth(Body):
    def __init__(self, Mass, EQ_rad, X, Y, Vxo, Vyo):
        self.Mass = Mass
        self.EQ_rad = EQ_rad
        self.pos = list((X,Y))
        self.v = list((Vxo, Vyo))
        
    def display(self):
        fill(2, 124 ,188)
        ellipse(self.pos[0], self.pos[1], self.EQ_rad/scal3, self.EQ_rad/scal3)
        
    #def gravity(self, other):
        #disp = 
        

def setup():
    size(1800, 1200)
    global sun,earth
 
    
    
    sun = Body(1.89*10**30, 696340, width/2, height/2)
    earth = Earth(5.97*10**24, 63780, width/2, height/2 + 1480000/scal3*3, 10, 10)
    
def draw():
    background(255)
    sun.display()
    earth.display()
    #eyPressed()
    #keyReleased()

    


        
    
    
    
