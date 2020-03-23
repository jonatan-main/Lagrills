
scale = 90
AU = 148000000
G_si = 6.67e-11
M = 1.989e30
T = 365*24
G = G_si*M*T**2/AU**3 #kg*T/pixels
print(G)

def mouseClicked(): 
    global scale
    if scale == 90:
        scale = 100
    elif scale ==100:
        scale = 120
    elif scale == 120:
        scale = 150
    elif scale == 150:
        scale = 170
    elif scale == 170:
        scale = 210
    elif scale == 210:
        scale = 90

class body(object):
    def __init__(self, Mass, EQ_rad, position, velocity, acceleration, R, G, B):
        self.col = list((R, G, B))
        self.Mass = Mass
        self.EQ_rad = EQ_rad
        self.pos = position
        self.vel = velocity
        self.acc = acceleration
        
    def display(self):
        fill(self.col[0], self.col[1] ,self.col[2])
        ellipse(self.pos.x, self.pos.y, self.EQ_rad*scale, self.EQ_rad*scale)
        textSize(32)
        
        
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
    def __init__(self, body1, body2, body3, body4): #container method for all bodies
        self.bodies = list((body1, body2, body3, body4)) #list of all bodies

        
        

    def display(self):
        count=0
        for x in self.bodies:
            x.display()
            count = count + 30
            text("Velocity =", 10, 20+count)
            text(sqrt(x.vel.x**2 + x.vel.y**2), 160, 20 + count)

        
        
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
jupiter_initvel = PVector(0, 1.5)


#earth initial condidtions
e_M = 5.24e+24 / M
e_r = 1 * scale
Earth_initial_pos = PVector(Sun_initial_pos.x - e_r , height/2)
Earth_initial_vel = PVector(0, 3.14159)
Earth_initial_acc = PVector(0,0)

#sat1 initial condidtions
sat_M = 2000 / M
sat_r = (777810000/ AU) * scale
sat1_initpos = PVector(jupiter_initpos.x, jupiter_initpos.y + (j_r-sat_r))
sat1_initvel = PVector(-0.9099999, 1.858000093)



def setup():

    size(width, height)
    global Sun, earth, jupiter, sat1, container
    noStroke()
    sat1 = body(sat_M, .05, sat1_initpos, sat1_initvel, Earth_initial_acc, 255, 250, 250)
    Sun = body(s_M , .5, Sun_initial_pos, sun_initial_vel, Earth_initial_acc, 255, 234, 0)
    earth = body(e_M, .05, Earth_initial_pos, Earth_initial_vel, Earth_initial_acc, 0, 245, 194)
    jupiter = body(j_M, .1, jupiter_initpos, jupiter_initvel, Earth_initial_acc, 245, 90, 0)
    
    container = bodies(Sun, earth, jupiter, sat1)
    #background(0)
    
def draw():
    frameRate(60)
    background(0)
    container.display()
    container.gravity()
    
    


        
    
    
    
