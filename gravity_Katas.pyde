scale = 2
AU = 500.0
        
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
        
    def applyForce(self, f):
        self.f = f
        self.f.div(self.Mass)
        self.acc.add(self.f)
        self.move(self.acc)
        
    def move(self, acc):
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc.mult(0)
       # print(self.vel)
        
        
   

    
        
class bodies():
    def __init__(self, body1, body2): #container method for all bodies
        self.bodies = list((body1, body2)) #list of all bodies

        
        

    def display(self):
        for x in self.bodies:
            x.display()

        
        
    def gravity(self):
        for i in self.bodies:
            for j in self.bodies:
                if j == i:
                    continue
                
                self.r = PVector.sub(i.pos, j.pos) #calculate vector between object and center of system
            
            
                self.r_mag = self.r.mag()**2 #calculate magnitude and direction of vector multiplied by our scale to insert real life conditions
                #self.r_norm = normalize(PVector.r)
                self.r_norm = self.r.copy().normalize()
                #self.r_norm1 = self.r_norm.copy().normalize()
            
            
                f_mag = 1 * i.Mass * j.Mass #calculate magnitude of gravitational force
                f_mag1 =  f_mag / self.r_mag
            
                Fg = self.r_norm.mult(f_mag1) #calculate Fg and apply it
                j.applyForce(Fg)
            

width, height = 1800 , 1200


Sun_initial_pos = PVector(width/2, height/2)    
Sun_init_vel = PVector(0,0)
Earth_initial_pos = PVector(Sun_initial_pos.x - AU , height/2)
Earth_initial_vel = PVector(0,1)
Earth_initial_acc = PVector(0,0)


def setup():

    size(width, height)
    global Sun, earth, container
    Sun = body(1000 , 300, Sun_initial_pos, Sun_init_vel, Earth_initial_acc)
    earth = body(1, 60, Earth_initial_pos, Earth_initial_vel, Earth_initial_acc)
    container = bodies(Sun, earth)
    
    
def draw():
    frameRate(60)
    background(255)
    container.display()
    container.gravity()
