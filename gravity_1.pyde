
scale = 500000

class Body():
    def __init__(self, Mass, EQ_rad, pos):
        self.Mass = Mass
        self.EQ_rad = EQ_rad
        self.pos = pos
        
    def display(self):
        fill(247, 247 ,0)
        ellipse(self.pos.x, self.pos.y, self.EQ_rad/scale, self.EQ_rad/scale)
        
class Earth(Body):
    def __init__(self, Mass, EQ_rad, position, velocity, acceleration):
        self.Mass = Mass
        self.EQ_rad = EQ_rad
        self.pos = position
        self.vel = velocity
        self.acc = acceleration
        
    def display(self):
        fill(2, 124 ,188)
        ellipse(self.pos.x, self.pos.y, self.EQ_rad/scale, self.EQ_rad/scale)
        
    def move(self):
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc.mult(0)
        
    def applyForce(self, force):
        self.force = force
        self.acc.add(self.force)
    
        

    def gravity(self, other):
        self.mass1 = other.Mass
        self.mass2 = self.Mass
        self.pos1 = self.pos
        self.pos2 = other.pos
        self.r = self.pos1.sub(self.pos2)
        self.rmag = self.r.mag()
        self.r_norm = self.r.div(self.rmag)
        
        self.Fmag = (6.67*10**-11)*(self.mass1* self.mass2)/ self.rmag**3
        self.gravity = self.r_norm.mult(self.Fmag)
        
        self.applyForce(self.gravity)
        

Sun_initial_pos = list((2200/2, 1600/2))
Earth_initial_pos= list((Sun_initial_pos.x, Sun_initial_pos.y - (148000000/scale)))
Earth_initial_vel= list((0,0))
Earth_initial_acc= list((0,0))
global width,height
width = 2200
height = 1600
Force = PVector(0,1)

def setup():

    size(width, height)
    global Sun,earth
    Sun = Body(1.89 , 69634000, Sun_initial_pos)
    earth = Earth(0.4, 6800000, Earth_initial_pos, Earth_initial_vel, Earth_initial_acc)
    
def draw():
    frameRate(60)
    background(255)
    Sun.display()
    earth.display()
    earth.move()
    earth.applyForce(Force)
    earth.gravity(Sun)
    


        
    
    
    
