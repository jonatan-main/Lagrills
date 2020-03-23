
scale = 200
AU = 148000000
G_si = 6.67e-11
M = 1.989e30
T = 100
G = G_si*M*T**2/AU**3 #kg*T/pixels
print(G)


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
        self.vel.add(acc)
        self.pos.add(self.vel)
        self.acc.mult(0)
        #print(self.vel)
        
    
      
        
class bodies():
    def __init__(self, body1, body2, body3): #container method for all bodies
        self.bodies = list((body1, body2, body3)) #list of all bodies

        
        

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
                self.r_norm = self.r.copy()
                self.r_norm.normalize()
            
            
                f_mag = G * i.Mass * j.Mass #calculate magnitude of gravitational force
                f_mag = - f_mag / self.r_mag
            
                Fg = self.r_norm.mult(f_mag) #calculate Fg and apply it
                i.applyForce(Fg)
            

width, height = 1800 , 1200

#sun initial conditions
s_M = 1.989e+30 / M
Sun_initial_pos = PVector(width/2, height/2)    
sun_initial_vel = PVector(0,0)

#jupiter initial conditions
j_r = (777920000 / AU) * scale
j_M = 1.898e+27 / M
jupiter_initpos = PVector(width/2 - j_r, height/2)
j_initvel = sqrt((s_M*G)/(j_r**2))
jupiter_initvel = PVector(0, j_initvel)


#earth initial condidtions
e_M = 5.24e+24 / M
e_r = 1 * scale
Earth_initial_pos = PVector(Sun_initial_pos.x - e_r , height/2)
Earth_initial_vel = PVector(0, sqrt((s_M*G)/e_r**2))
Earth_initial_acc = PVector(0,0)


def setup():

    size(width, height)
    global Sun, earth, jupiter, container
    Sun = body(s_M , 60, Sun_initial_pos, sun_initial_vel, Earth_initial_acc)
    earth = body(e_M, 60, Earth_initial_pos, Earth_initial_vel, Earth_initial_acc)
    jupiter = body(j_M, 60, jupiter_initpos, jupiter_initvel, Earth_initial_acc)
    
    container = bodies(Sun, earth, jupiter)
    background(255)
    
def draw():
    frameRate(60)
    #background(255)
    container.display()
    container.gravity()
    


        
    
    
    
