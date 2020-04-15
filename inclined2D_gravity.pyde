
dispScale = 50                   # pixels/AU
AU = 1.496e11                    # astronomical unit in m
G_si = 6.67e-11                  # universal gravitational constant in m³/(kg*s²)
M = 1.989e30                     # Solar mass in kg
T = 86400                        # seconds/day
G = (G_si*M*(T**2))/((AU)**3)
#print(G)

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
    def __init__(self, Mass, EQ_rad, distanceFromSun, inclination, velocity, acceleration, R, G, B):
        self.col = list((R, G, B))
        self.Mass = Mass
        self.EQ_rad = EQ_rad
        self.r = distanceFromSun
        self.i = inclination
        self.vel = velocity
        self.acc = acceleration
        self.Epot = 0
        self.Ekin = 0
        self.Epotlist = []
        
        #calculation of initial position:
        if self.i != 0:
            x_init = sqrt((self.r**2) / (tan(radians(self.i))**2 +1))
            z_init = sqrt(self.r**2 - x_init**2)
        else:
            x_init = self.r
            z_init = 0
        self.pos = PVector(x_init, 0, z_init)
        #print(self.pos)
        
        self.history = [self.pos]
        
        
    def display(self):
        fill(self.col[0], self.col[1] ,self.col[2])
        x = self.pos.x * dispScale + width / 2.0
        y = self.pos.y * dispScale + height / 2.0
        """
        z = self.pos.z * dispScale
        
        noStroke()
        lights()
        pushMatrix()
        translate(x, y, z)
        sphere(self.EQ_rad)
        popMatrix()
        """
        ellipse(x, y, self.EQ_rad, self.EQ_rad)
        
        for i in self.history:
            fill(self.col[0], self.col[1] ,self.col[2])
            xhistory = i.x * dispScale + width / 2.0
            yhistory = i.y * dispScale + height / 2.0
            """
            zhistory = i.z * dispScale
            
            pushMatrix()
            translate(xhistory, yhistory, zhistory)
            sphere(1)
            popMatrix()
            """
            
            ellipse(xhistory, yhistory, 2, 2)
        #print(len(self.history))
        
        if len(self.history) >= 10:
            self.history.pop(1)
               
                        
    def applyForce(self, f):
        self.f = f
        self.f.div(self.Mass)
        self.acc.add(self.f)
        self.move(self.acc)
        
    def move(self, a):
        self.acc = a
        self.history.append(self.pos.copy())
        
        
        #this is were we have to do the RK 4 Shit
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc.mult(0)
        
        
        
        # calculating kinetic energy (Ekin = 1/2*m*v²):
        self.Ekin = 0        
        self.v = self.vel.copy().mag()
        self.Ekin = 0.5 * (self.Mass) * self.v ** 2
        
        # calculating potential energy:
        self.Epot = 0
        for i in self.Epotlist:
            self.Epot = self.Epot + i
        
        #print(self.Mass * M)
        #print(self.v)
        #print(self.Ekin)# *10**10) 
        #print(self.Epot)     
        
    

        
class bodies():
    def __init__(self, body1, body2, body3, body4, body5): #container method for all bodies
        self.bodies = list((body1, body2, body3, body4, body5)) #list of all bodies
        self.energysum = 0.0 # total energy of the system
        
        

    def display(self):
        count=0
        for x in self.bodies:
            x.display()
                        
            count = count + 30
            textSize(32)
            #text("Velocity =", 10, 20+count)
            #text(sqrt(x.vel.x**2 + x.vel.y**2), 160, 20 + count)
            
            textSize(32)
            #text("kinetic Energy =", 10, 2*20+(len(self.bodies)*30)+count)  
            #text(x.Ekin * 10**10, 270, 2*20+(len(self.bodies)*30)+count)     # scale appropriately
            
            textSize(32)
            #text("potential Energy =", 10, 3*20+(2*len(self.bodies)*30)+count)
            #text(x.Epot *10**10, 300, 3*20+(2*len(self.bodies)*30)+count)    # scale appropriately
            
            textSize(32)
            #text("total Energy =", 10, 4*20+(3*len(self.bodies)*30)+count)
            #text((x.Epot+x.Ekin) *10**10, 230, 4*20+(3*len(self.bodies)*30)+count)    # scale appropriately
            
        textSize(32)
        text("TOTAL Energy =", width/2 - 250, 100)
        text(self.energysum * 10**7, width/2 + 50, 100)    # scale appropriately
        
        #print(self.energysum)    
        #print(x.Epot+x.Ekin)
        
    def update(self):
        self.gravity()
        self.display()
        
        
    def gravity(self):
        self.energysum = 0
        
        for i in self.bodies:
            Fg = PVector(0,0,0) # total force on body i
            i.Epotlist = []
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
                
                
                # calculating gravitational potential energy between bodies i and j (Epot = -G*M*m/r):
                self.R = self.r.copy().mag()
                Epot = -G * i.Mass * j.Mass / self.R
                
                i.Epotlist.append(Epot)  # used to calculate total potential energy for each body
                            
            i.applyForce(Fg) # apply summed force
            
            # calculating total energy of the system: 
            self.energysum = self.energysum + i.Epot + i.Ekin
            
            #print(Fg)
            #print(self.Epot)
            #print(len(i.Epotlist))
            #print(i.Epotlist)
        
        
fwidth, fheight = 1800 , 1200

#sun initial conditions
s_M = 1.989e+30 / M   # mass
s_r = 0               # distance from Sun
s_i = 0               # orbit inclination to ecliptic in degrees
sun_initial_vel = PVector(0,0,0)

#jupiter initial conditions
j_r = 4.9465          # distance from Sun in AU
j_M = 1.898e+27 / M   # mass
j_p = 11.86 * 365.26  # jupiter period in days
j_i = 1.304           # orbit inclination to ecliptic in degrees
jupiter_initvel = PVector(0, -0.0079238502673, 0) # AU/day


#earth initial condidtions
e_M = 5.24e+24 / M    # mass
e_r = 0.98329         # distance from Sun
e_i = 0               # orbit inclination to ecliptic in degrees
einitvel = sqrt(((s_M*G)/((e_r)**2)))
Earth_initial_vel = PVector(0, -0.0174939, 0)
Earth_initial_acc = PVector(0,0, 0)

#sat1 initial condidtions
sat1_M = 3000/ M      # mass
sat1_r = -0.98329     # distance from Sun in AU
sat1_i = 0            # orbit inclination to ecliptic in degrees
sat1_initvel = PVector(0, 0.0174939, 0)# + 0.000590254)

#venus initial conditions
venus_m = 4.8675e+24 / M  # mass
ven_r = 0.718             # distance from Sun in AU
ven_i = 3.39              # orbit inclination to ecliptic in degrees
ven_initvel = PVector(0, -0.020364, 0)



def setup():

    size(fwidth, fheight, P3D)
    global Sun, earth, jupiter, sat1, container
    noStroke()
    sat1 = body(sat1_M, 4, sat1_r, sat1_i, sat1_initvel, Earth_initial_acc, 255, 250, 250)
    Sun = body(s_M , 15, s_r, s_i, sun_initial_vel, Earth_initial_acc, 255, 234, 0)
    earth = body(e_M, 6, e_r, e_i, Earth_initial_vel, Earth_initial_acc, 0, 245, 194)
    jupiter = body(j_M, 12, j_r, j_i, jupiter_initvel, Earth_initial_acc, 245, 90, 0)
    venus = body(venus_m, 5, ven_r, ven_i, ven_initvel, Earth_initial_acc, 214, 181, 50) 
    
    container = bodies(Sun, earth, jupiter, venus, sat1)
    background(0)
    
def draw():
    frameRate(60)
    background(0)
    container.update()
    container.gravity()
