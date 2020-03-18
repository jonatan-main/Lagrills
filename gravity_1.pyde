
scale = 2

        
class body(object):
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
        
        
   

    
        
class bodies():
    def __init__(self, body1, body2): #container method for all bodies
        self.bodies = list((body1, body2)) #list of all bodies
        
        self.masses = list((self.bodies[0].Mass, self.bodies[1].Mass)) # list of masses of all bodies
        self.positions = list((self.bodies[0].pos, self.bodies[1].pos)) #list of posititons of all bodies
        
        self.COM = self.positions[1].mult(self.masses[1])
        self.COM.add(self.positions[0].mult(self.masses[0])) #calculate center of mass of system
        self.COM.div(self.masses[0] + self.masses[1])
        
        

    def display(self):
        for x in self.bodies:
            self.bodies[x].display()
        
    def applyForce(self, f):
        self.f = f
        for x in self.bodies:
            self.bodies[x].applyForce(f)
        
        
    def gravity(self):
        for i in self.bodies:
            r = PVector(self.positions[i].x -  self.COM.x, self.positions[i].y - self.COM.y) #calculate vector between object and center of system
            
            
            r_mag = r.mag() * scale #calculate magnitude and direction of vector multiplied by our scale to insert real life conditions
            r_norm = r.div(r_mag)
            
            
            f_mag = 6.67e-11 * self.masses[0] * self.masses[1] #calculate magnitude of gravitational force
            f_mag = f_mag / r_mag**2
            
            Fg = r_norm.mult(f_mag) #calculate Fg and apply it
            self.bodies[i].applyForce()
            

width, height = 1800 , 1200


Sun_initial_pos = PVector(width/2, height/2)    
Earth_initial_pos = PVector(Sun_initial_pos.x - 148/scale, height/2)
Earth_initial_vel = PVector(0,2)
Earth_initial_acc = PVector(0,0)


def setup():

    size(width, height)
    global Sun, earth, container
    Sun = body(1000 , 60, Sun_initial_pos, Earth_initial_vel, Earth_initial_acc)
    earth = body(1500, 60, Earth_initial_pos, Earth_initial_vel, Earth_initial_acc)
    container = bodies(Sun, earth)
    
    
def draw():
    frameRate(60)
    background(255)
    container.display()

    container.gravity()
    


        
    
    
    
