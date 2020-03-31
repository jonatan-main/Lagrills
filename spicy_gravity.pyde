
dispScale = 50 # px/au - scale is a function, dont use that
AU = 1.496e11 # m
G_si = 6.67e-11 # m³/(kg*s²)
M = 1.989e30 # Solar mass in kg
T = 86400 # seconds/day
G = (G_si*M*(T**2))/((AU)**3)#kg*T/pixels
print(G)

def mouseClicked(): # change to use dispScale and have a fall through
    global dispScale
    if dispScale == 90:
        dispScale = 100
    elif dispScale == 100:
        dispScale = 120
    elif dispScale == 120:
        dispScale = 150
    elif dispScale == 150:
        dispScale = 170
    elif dispScale == 170:
        dispScale = 210
    elif dispScale == 210:
        dispScale = 90
    else:
        dispScale = 100

class body(object):
    def __init__(self, Mass, EQ_rad, position, velocity, acceleration, R, G, B):
        self.col = list((R, G, B))
        self.Mass = Mass
        self.EQ_rad = EQ_rad
        self.pos = position
        self.vel = velocity
        self.acc = acceleration
        self.history = [self.pos]

   
        
    def display(self): # changed to use a 0,0 centred coordinate system, and then translate that to the screen
        fill(self.col[0], self.col[1] ,self.col[2])
        x = self.pos.x * dispScale + width / 2.0
        y = self.pos.y * dispScale + height / 2.0
        ellipse(x, y, self.EQ_rad, self.EQ_rad)
        
        for i in self.history:
            fill(self.col[0], self.col[1] ,self.col[2])
            xhistory = i.x * dispScale + width / 2.0
            yhistory = i.y * dispScale + height / 2.0
            ellipse(xhistory, yhistory, 2, 2)
        print(len(self.history))
        
        if len(self.history) > 250:
            self.history.pop(1)
        #else:
         #   continue
        #print(self.history[len(self.history)-1])
        
                        
    def applyForce(self, f):
        self.f = f
        self.f.div(self.Mass)
        self.acc.add(self.f)
        self.move(self.acc)
        
    def move(self, acc):
        self.history.append(self.pos.copy())
        self.vel.add(acc)
        self.pos.add(self.vel)
        self.acc.mult(0)
        #self.history.append(self.pos)
            
        
        #print(self.vel)
        

        
class bodies():
    def __init__(self, body1, body2, body3, body4): #container method for all bodies
        self.bodies = list((body1, body2, body3, body4)) #list of all bodies

        
        

    def display(self):
        count=0
        for x in self.bodies:
            x.display()
            count = count + 30
            textSize(32)
            text("Velocity =", 10, 20+count)
            text(sqrt(x.vel.x**2 + x.vel.y**2), 160, 20 + count)
            
        
    def gravity(self):
        for i in self.bodies:
            Fg = PVector(0,0) # total force on body i
            for j in self.bodies:
                if j == i:
                    continue
                
                self.r = PVector.sub(i.pos, j.pos) #calculate vector between object i and j
                
                self.r_mag2 = (self.r.mag()**2) #calculate magnitude squared
                
                self.r_norm = self.r.copy()
                self.r_norm.normalize()
            
                f_mag = G * i.Mass * j.Mass #calculate magnitude of gravitational force
                f_mag = - f_mag / self.r_mag2
            
                Fg += self.r_norm.mult(f_mag) #calculate Fg and add to total force
                
            i.applyForce(Fg) # apply summed force
            #print(Fg)
                
#width, height = 1800 , 1200 # width and height are system variables (set by size) and should not be used like this
fwidth, fheight = 1800 , 1200

#sun initial conditions
s_M = 1.989e+30 / M
Sun_initial_pos = PVector(0,0) # change in coord system
sun_initial_vel = PVector(0,0)

#jupiter initial conditions
j_r = 5.203 # au
j_M = 1.898e+27 / M
j_p = 11.86 * 365.26 # jupiter period in days
jupiter_initpos = PVector(j_r, 0) # change in coord system
jupiter_initvel = PVector(0, j_r * 2 * 3.1416 / j_p)


#earth initial condidtions
e_M = 5.24e+24 / M
e_r = 0.9832
einitvel = sqrt(((s_M*G)/((e_r)**2)))
Earth_initial_pos = PVector(e_r , 0) # change in coord system
Earth_initial_vel = PVector(0, .01)
Earth_initial_vel = PVector(0, e_r * 2 * 3.1416 / 365.26)
Earth_initial_acc = PVector(0,0)

#sat1 initial condidtions
sat_M = 1000 / M
sat_r = 0.9832899
sat1_initpos = PVector(sat_r, 0) # change in coord system
sat1_initvel = PVector(0, .013)



def setup():

    size(fwidth, fheight)
    global Sun, earth, jupiter, sat1, container
    noStroke()
    sat1 = body(sat_M, 4, sat1_initpos, sat1_initvel, Earth_initial_acc, 255, 250, 250)
    Sun = body(s_M , 15, Sun_initial_pos, sun_initial_vel, Earth_initial_acc, 255, 234, 0)
    earth = body(e_M, 6, Earth_initial_pos, Earth_initial_vel, Earth_initial_acc, 0, 245, 194)
    jupiter = body(j_M, 12, jupiter_initpos, jupiter_initvel, Earth_initial_acc, 245, 90, 0)
    
    container = bodies(Sun, earth, jupiter, sat1)
    background(0)
    
def draw():
    frameRate(60)
    background(0)
    container.display()
    container.gravity()

    
    
    
    


        
    
    
    
