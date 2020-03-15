
scale = 2

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
        
    def applyForce(self, force):
        self.force = force
        #print(force)
        self.force.div(self.Mass)
        self.acc.add(self.force)
        #print(self.acc)    
        self.move(self.acc)
        
    def move(self, acc):
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc.mult(0)
       # print(self.vel)
        
        
   

    
        
class gravity():
    def __init__(self, body1, body2):
        self.sun = body1
        self.earth = body2
        self.sMass = body1.Mass
        self.eMass = body2.Mass
        self.sun_pos = body1.pos
        self.e_pos = body2.pos
        
        
    def gravity(self):
        self.r = PVector(self.e_pos.x - self.sun_pos.x, self.e_pos.y - self.sun_pos.y)
        self.rmag = self.r.mag()
        print(self.rmag)
        self.r_norm = self.r.normalize()
        #print(r_norm)
        self.Fg_mag = (6.67*10**-11) * (self.sMass * self.eMass) / self.rmag**2
        # print(r)
        self.Fg = self.r_norm.mult(self.Fg_mag)
        self.earth.applyForce(self.Fg)
        #print(Fg)

width, height = 1800 , 1200


Sun_initial_pos = PVector(width/2, height/2)    
Earth_initial_pos = PVector(Sun_initial_pos.x - 148/scale, height/2)
Earth_initial_vel = PVector(0,2)
Earth_initial_acc = PVector(0,0)


def setup():

    size(width, height)
    global Sun, earth, container
    Sun = Body(1000 , 60, Sun_initial_pos)
    earth = Earth(1500, 60, Earth_initial_pos, Earth_initial_vel, Earth_initial_acc)
    container = gravity(Sun, earth)
    
    
def draw():
    frameRate(60)
    background(255)
    Sun.display()
    earth.display()

    container.gravity()
    


        
    
    
    
