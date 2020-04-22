
# Choose 2D or 3D display
dim = 2 #D

# Choose whether to display.  
 #disp = 1 will display. Won't otherwise. 
disp = 1

# Choose whether to display text about .  
 #disptext = 1 will display. Won't otherwise. 
disptext = 0


#Choose timestep for RK4
timestep = 0.1


#Size of window
fwidth, fheight = 800 , 800


dispScale = 50                   # pixels/AU
AU   = 1.496e11                    # astronomical unit in m
G_si = 6.67e-11                  # universal gravitational constant in m³/(kg*s²)
M    = 1.989e30                     # Solar mass in kg
T    = 86400                        # seconds/day
G    = (G_si*M*(T**2))/((AU)**3)



#----------------------------------------------------------------------------------------------------------------   
# ----------------------------- Body class ----------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------  

class body(object):
    def __init__(self,name, Mass, EQ_rad, distanceFromSun, inclination, velocity, R, G, B):
        self.col = list((R, G, B));   self.Mass = Mass;        self.EQ_rad = EQ_rad; 
        self.r = distanceFromSun;     self.i = inclination;    self.name = name   
        self.velmag = velocity;       self.acc = PVector(.0,.0,.0)
        
        self.pos = PVector(self.r, 0, 0);   self.history = [self.pos] 
        self.Epot = 0;   self.Ekin = 0;     self.Epotlist = []
     
        self.SaveData = createWriter(self.name)
        
        self.c0 = PVector(0,0,0); self.c1 = PVector(0,0,0); self.c2 = PVector(0,0,0); self.c3 = PVector(0,0,0)
        self.k0 = PVector(0,0,0); self.k1 = PVector(0,0,0); self.k2 = PVector(0,0,0); self.k3 = PVector(0,0,0)
         
    #------------------------ Calculate velocity with inclination -----------------------------------------------    
        self.irads = radians(self.i)
        self.Vx = 0.0
        self.Vy = self.velmag * cos(self.irads)
        self.Vz = self.velmag * sin(self.irads)
        self.vel = PVector(self.Vx, self.Vy, self.Vz)
        
        
    # ------------------------ calculation of initial position: ------------------------------
        """
        if self.i != 0:
            x_init = sqrt((self.r**2) / (tan(radians(self.i))**2 +1))
            z_init = sqrt(self.r**2 - x_init**2)
        else:
            x_init = self.r
            z_init = 0
        
        print(self.pos)
        """
        
    #--------------------------------------- 3D display -------------------------------------------------------           
    if dim == 3:
        def display(self):
            fill(self.col[0], self.col[1] ,self.col[2])
            x = self.pos.x * dispScale + width / 2.0
            y = self.pos.y * dispScale + height / 2.0
            z = self.pos.z * dispScale
            
            noStroke()
            lights()
            pushMatrix()
            translate(x, y, z)
            sphere(self.EQ_rad)
            popMatrix()
            
            for i in self.history:
                fill(self.col[0], self.col[1] ,self.col[2])
                xhistory = i.x * dispScale + width / 2.0
                yhistory = i.y * dispScale + height / 2.0
                zhistory = i.z * dispScale
                
                pushMatrix()
                translate(xhistory, yhistory, zhistory)
                sphere(1)
                popMatrix()
            
            if len(self.history) >= 10:
                self.history.pop(1) 
          
    
    # ---------------------------- Printing position --------------------------------------------------
    def printer(self):
        self.SaveData.print(self.pos) 
        self.SaveData.print(",")
        self.SaveData.flush()                
        
    # -----------------------------Display 2D ------------------------------------------------------        

    if dim == 2:     
        def display(self):
            fill(self.col[0], self.col[1] ,self.col[2])
            x = self.pos.x * dispScale + width / 2.0
            y = self.pos.y * dispScale + height / 2.0
    
            ellipse(x, y, self.EQ_rad, self.EQ_rad)

        
#----------------------------------------------------------------------------------------------------------------   
# ----------------------------- Container class -----------------------------------------------------------------    
#----------------------------------------------------------------------------------------------------------------   
  
class bodies():
    def __init__(self, body1, body2, body3, body4, body5):      #container method for all bodies
        self.bodies = list((body1, body2, body3, body4, body5)) #list of all bodies
        self.energysum = 0.0                                    # total energy of the system
        
        
    #------------------------------- Display stuff ---------------------------------------------------------
    if disp == 1:
        def display(self):
            count=0
            for x in self.bodies:
                x.display()
                            
                count = count + 30
                #------------------------------- Display text ---------------
                if disptext == 1:
                    textSize(32)
                    text("Velocity =", 10, 20+count)
                    text(sqrt(x.vel.x**2 + x.vel.y**2), 160, 20 + count)
                    
                    textSize(32)
                    text("kinetic Energy =", 10, 2*20+(len(self.bodies)*30)+count)  
                    text(x.Ekin * 10**10, 270, 2*20+(len(self.bodies)*30)+count)              # scale appropriately
                    
                    textSize(32)
                    text("potential Energy =", 10, 3*20+(2*len(self.bodies)*30)+count)
                    text(x.Epot *10**10, 300, 3*20+(2*len(self.bodies)*30)+count)             # scale appropriately
                    
                    textSize(32)
                    text("total Energy =", 10, 4*20+(3*len(self.bodies)*30)+count)
                    text((x.Epot+x.Ekin) *10**10, 230, 4*20+(3*len(self.bodies)*30)+count)    # scale appropriately
                
            textSize(32)
            text("TOTAL Energy =", width/2 - 250, 100)
            text(self.energysum * 10**7, width/2 + 50, 100)    # scale appropriately
            

#------------------------------------------- RK4 integration ----------------------------------------------
    def rk4Step(self, tstep):
        self.energysum = 0.0
        #-------------------------- c0 & k0 ---------------------------------------
        for i in self.bodies:
            i.c0 = i.vel


            i.k0 = PVector(.0,.0,.0)
            for j in self.bodies:
                if j == i:
                    continue
                r       = i.pos - j.pos
                r_mag2  = r.mag()**2
                r_norm  = r.copy().normalize()
                f_mag   = - G * i.Mass * j.Mass / r_mag2
                i.k0   += f_mag * r_norm / i.Mass
                self.energysum += -G * i.Mass * j.Mass / r.mag()

            self.energysum += i.Mass * i.vel.mag()**2 / 2
            
        #-------------------------- c1 & k1 ---------------------------------------
        for i in self.bodies:
            i.c1 = i.vel + tstep/2*i.k0

            i.k1 = PVector(.0,.0,.0)
            for j in self.bodies:
                if j == i:
                    continue
                r       = (i.pos + tstep/2*i.c0) - (j.pos + tstep/2*j.c0)
                r_mag2  = r.mag()**2
                r_norm  = r.copy().normalize()
                f_mag   = - G * i.Mass * j.Mass / r_mag2
                i.k1   += f_mag * r_norm / i.Mass
                
        #-------------------------- c2 & k2 ---------------------------------------
        for i in self.bodies:
            i.c2 = i.vel + tstep/2*i.k1

            i.k2 = PVector(.0,.0,.0)
            for j in self.bodies:
                if j == i:
                    continue
                r       = (i.pos + tstep/2*i.c1) - (j.pos + tstep/2*j.c1)
                r_mag2  = r.mag()**2
                r_norm  = r.copy().normalize()
                f_mag   = - G * i.Mass * j.Mass / r_mag2
                i.k2   += f_mag * r_norm / i.Mass
                
        #-------------------------- c3 & k3 ---------------------------------------
        for i in self.bodies:
            i.c3 = i.vel + tstep*i.k2

            i.k3 = PVector(.0,.0,.0)
            for j in self.bodies:
                if j == i:
                    continue
                r       = (i.pos + tstep*i.c2) - (j.pos + tstep*j.c2)
                r_mag2  = r.mag()**2
                r_norm  = r.copy().normalize()
                f_mag   = - G * i.Mass * j.Mass / r_mag2
                i.k3   += f_mag * r_norm / i.Mass
        
        #----------------- weighted average ------------------
        for i in self.bodies:
            i.pos += tstep/6*(i.c0 + 2*i.c1 + 2*i.c2 + i.c3)
            i.vel += tstep/6*(i.k0 + 2*i.k1 + 2*i.k2 + i.k3)
 
    # ---------------------------------- Update function ---------------------------------------------
                      
    def update(self):
        for i in range(10):
            self.rk4Step(timestep)       # Integration method RK4
        if disp == 1:
            self.display()          # Display system
        for i in self.bodies:       
            i.printer()             # Save data in .txt
#------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Initial conditions ---------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------



InitAcc = PVector (0,0,0)

#--------------- sun initial conditions ----------------
SunM     = 1.989e+30 / M       # mass
Sunr     = 0.0                 # distance from Sun
SunI     = 0.0                 # orbit inclination to ecliptic in degrees
SunVel   = 0.0

#--------------- jupiter initial conditions ---------------

Jupr     = 4.9465              # distance from Sun in AU
JupM     = 1.898e+27 / M       # mass
JupP     = 11.86 * 365.26      # jupiter period in days
JupI     = 1.304               # orbit inclination to ecliptic in degrees
JupVel   = -0.0079238502673    # AU/day


#--------------- earth initial condidtions ---------------
EarthM   = 5.24e+24 / M        # mass
Earthr   = 0.98329             # distance from Sun
EarthI   = 0.0                 # orbit inclination to ecliptic in degrees
einitvel = sqrt(((SunM*G)/((Earthr)**2)))
EarthVel = -0.0174939

#--------------- venus initial conditions ---------------
VenM     = 4.8675e+24 / M      # mass
Venr     = 0.718               # distance from Sun in AU
VenI     = 3.39                # orbit inclination to ecliptic in degrees
VenVel   = -0.020364


# --------------- sat1 initial condidtions ---------------
sat1M    = 3000/ M             # mass
sat1r    = -0.98329            # distance from Sun in AU
sat1I    = 0.0                 # orbit inclination to ecliptic in degrees
sat1Vel  = 0.0174939           # + 0.000590254)




#------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------Setup and draw ------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
def setup():

    size(fwidth, fheight, P3D)
    global Sun, earth, jupiter, sat1, container, dim, disp
    noStroke()
    
   #body    =     (txtPos        mass    rad   dist    incl    initVel      R    G    B  )
    sat1    = body("nSat1.txt" , sat1M ,  4 ,  sat1r , sat1I  , sat1Vel  ,  255, 250, 250)
    Sun     = body("nSun.txt"  , SunM  ,  15,  Sunr  , SunI   , SunVel   ,  255, 234, 0  )
    Earth   = body("nEarth.txt", EarthM,  6 ,  Earthr, EarthI , EarthVel ,  0,   245, 194)
    Jupiter = body("nJup.txt"  , JupM  ,  12,  Jupr  , JupI   , JupVel   ,  245, 90,  0  )
    Venus   = body("nVen.txt"  , VenM  ,  5 ,  Venr  , VenI   , VenVel   ,  214, 181, 50 ) 
    
    container = bodies(Sun, Earth, Jupiter, Venus, sat1)
    background(0)
    frameRate(60)
    
def draw():
    #background(0)
    container.update()
    

#---------------------------------- Scaling the window ----------------------------
def mouseClicked(): # change to use dispScale and have a fall through
    background(0)
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
