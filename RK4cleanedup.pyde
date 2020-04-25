
# Choose 2D or 3D display
dim = 2 #D

# to solar radiate or not to solar radiate
SolarRadiation = 1

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



#----------------------------------------------------------------------------------------------------------------   
# ----------------------------- Body class ----------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------  

class body(object):
    def __init__(self, name, Mass, rad, distanceFromSun, inclination, velocity, satOrPlan, R, G, B):
        self.col    = list((R, G, B));   self.Mass = Mass       ;      self.EQ_rad = rad;         self.sat = satOrPlan
        self.r      = distanceFromSun;   self.i    = inclination;      self.name   = name   
        self.velmag = velocity       ;   self.acc  = vec0       ;      self.SaveData = createWriter(self.name)
        
        self.pos  = PVector(self.r, 0, 0);   self.history = [self.pos] 
        self.Epot = 0;      self.Ekin = 0;   self.Epotlist = []
     
        self.c0 = PVector(0,0,0); self.c1 = PVector(0,0,0); self.c2 = PVector(0,0,0); self.c3 = PVector(0,0,0)
        self.k0 = PVector(0,0,0); self.k1 = PVector(0,0,0); self.k2 = PVector(0,0,0); self.k3 = PVector(0,0,0)
         
    #------------------------ Calculate velocity with inclination -----------------------------------------------    
        self.irads = radians(self.i)
        self.Vx    = 0.0
        self.Vy    = self.velmag * cos(self.irads)
        self.Vz    = self.velmag * sin(self.irads)
        self.vel   = PVector(self.Vx, self.Vy, self.Vz)
        
        
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
            
            noStroke();  lights();   pushMatrix();  translate(x, y, z);   sphere(self.EQ_rad);   popMatrix()
            
            for i in self.history:
                fill(self.col[0], self.col[1] ,self.col[2])
                xhistory = i.x * dispScale + width / 2.0
                yhistory = i.y * dispScale + height / 2.0
                zhistory = i.z * dispScale
                
                pushMatrix();   sphere(1);    popMatrix();     translate(xhistory, yhistory, zhistory)  
            
            if len(self.history) >= 10:
                self.history.pop(1) 
          
    
    # ---------------------------- Printing position --------------------------------------------------
    
    def printer(self):
        if self.sat == 1:
            self.SaveData.print(self.pos);      self.SaveData.print(",");       self.SaveData.flush()                
        
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
    def __init__(self, body1, body2, body3, body4, body5, body6):      #container method for all bodies
        self.bodies = list((body1, body2, body3, body4, body5, body6)) #list of all bodies
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
            text("TOTAL Energy =",       width/2 - 250, 100)
            text(self.energysum * 10**7, width/2 + 50,  100)    # scale appropriately
    
#-------------------------------------- gravity --------------------------------
    def gravity(self, body1, body2):
        bi      = body1;                    bj      = body2
        r       = bi.pos - bj.pos;          r_mag2  = r.mag()**2;
        r_norm  = r.copy().normalize();     f_mag   = - G * bi.Mass * bj.Mass / r_mag2
        
        idk     = f_mag * r_norm / bi.Mass; e_sum   =  -G * bi.Mass * bj.Mass / r.mag()
        return    idk, e_sum, r.mag()
        #grav  [0]   [1]    [2]       
    
#----------------------------------- Solar radiation ------------------------    
    def solar(self, Sun, sat):
        Sun   = Sun;  sat = sat;   
        e     = Sun.pos - sat.pos;   eNorm = r.copy().normalize();                       # Vector for distance to sun
        n     = sat.vel;             nNorm = n.copy().normalize();                       # Vector for satellite's velocity
        cos0  = (e.x * n.x + e.y * n.y + e.z * n.z)/(e.mag() * n.mag())                  # cos of angle between sun vector and vel vector 
        F     = - P*cos0*A*((1 - eps)*eNorm + 2*eps*cos0*nNorm)                          #F = −P cos(θ )A [(1−ε)e + 2ε cos(θ )n]
        accel = F / sat.Mass;     return accel
    
        
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
                grav = self.gravity(i,j)                           
                if i == 1 and j.sat == 1 and SolarRadiation == 1:              #  <--  j depends on how many planets we have before satellites
                    solarRad = self.solar(i,j)
                    i.k0 += solarRad()
                i.k0   += grav[0]                
                self.energysum += grav[1]
            self.energysum += i.Mass * i.vel.mag()**2 / 2
            
        #-------------------------- c1 & k1 ---------------------------------------
        for i in self.bodies:
            i.c1 = i.vel + tstep/2*i.k0
            i.k1 = PVector(.0,.0,.0)
            for j in self.bodies:
                if j == i:
                    continue
                grav = self.gravity(i,j)
                i.k1 += grav[0]
                if i == 1 and j.sat == 1 and SolarRadiation == 1: 
                    solarRad = self.solar(i,j)
                    i.k1 += solarRad()

                
        #-------------------------- c2 & k2 ---------------------------------------
        for i in self.bodies:
            i.c2 = i.vel + tstep/2*i.k1
            i.k2 = PVector(.0,.0,.0)
            for j in self.bodies:
                if j == i:
                    continue
                if i == 1 and j.sat == 1 and SolarRadiation == 1: 
                    solarRad = self.solar(i,j)
                    i.k2 += solarRad()
                grav = self.gravity(i,j)
                i.k2 += grav[0]          
                      
        #-------------------------- c3 & k3 ---------------------------------------
        for i in self.bodies:
            i.c3 = i.vel + tstep*i.k2
            i.k3 = PVector(.0,.0,.0)
            for j in self.bodies:
                if j == i:
                    continue
                if i == 1 and j.sat == 1 and SolarRadiation == 1: 
                    solarRad = self.solar(i,j)
                    i.k3 += solarRad()
                grav = self.gravity(i,j)
                i.k3 += grav[0]
                
        #----------------- weighted average ------------------
        for i in self.bodies:
            i.pos += tstep/6*(i.c0 + 2*i.c1 + 2*i.c2 + i.c3)
            i.vel += tstep/6*(i.k0 + 2*i.k1 + 2*i.k2 + i.k3)

    # ---------------------------------- Update function ---------------------------------------------
                      
    def update(self):
        for i in range(10):
            self.rk4Step(timestep)       # Integration method RK4
        if disp == 1:
            self.display()               # Display system
        for i in self.bodies:       
            i.printer()                  # Save data in .txt file
            
#------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Initial conditions ---------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------

#---------------- Unit conversion ------------------------
#AU in meter          solar mass in kg      #sec/day         
AU = 1.496e11;        M = 1.989e30;         T = 86400;

#---------------- Grav constant --------------------------

G_si = 6.67e-11                      # universal gravitational constant in m³/(kg*s²)
G  = (G_si*M*(T**2))/((AU)**3)       #gravitational constant

#----------------  Radiation pressure --------------------
#Reflection    Area of satellite
eps  = 0.5;    A = (4.2 * 2.7)/AU**2          #These depend on the satellite
P_si = 4.56e-6                                #Nm^-2 SI unit                 N = kg * m * s^-2
P    = (P_si * AU * T**2)/(M)                 # This depends on distance from Sun, so we need to find a way to express this as a function of distance. 



#----------------  Planets   ----------------------
#planet    mass          ;    dist from sun   ;   inclination   ;    velocity
SunM     = 1.989e+30 / M ;    Sunr   = 0.0    ;   SunI   = 0.0  ;    SunVel   = 0.0                       #Sun  
VenM     = 4.8675e+24 / M;    Venr   = 0.718  ;   VenI   = 3.39 ;    VenVel   = -0.020364                 #Venus
EarthM   = 5.24e+24 / M  ;    Earthr = 0.98329;   EarthI = 0.0  ;    EarthVel = -0.0174939                #Earth
JupM     = 1.898e+27 / M ;    Jupr   = 4.9465 ;   JupI   = 1.304;    JupVel   = -0.0079238502673          #Jupiter

#--------------------   Satellites ----------------------------
#satnr     mass          ;    dist from sun    ;   inclination   ;    velocity
sat1M    = 3000/ M       ;    sat1r  = -0.98329;   sat1I  = 0.0  ;    sat1Vel  = 0.0174939;                                           #sat 1 vel(?): + 0.000590254)
sat2r    = sat1r - 0.001

vec0 = PVector(.0,.0,.0)
#------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------Setup and draw ------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------

def setup():
    size(fwidth, fheight, P3D)
    global Sun, earth, jupiter, sat1, container, vec0
    noStroke()
    
   #body    =     (txtPos        mass    rad   dist    incl    initVel    sat?   R    G    B  )
    sat1    = body("nSat1.txt" , 1/M   ,  4 ,  sat1r , sat1I  , sat1Vel  , 1,    255, 250, 250)
    sat2    = body("nSat2.txt" , 1/M   ,  4 ,  sat2r , sat1I  , sat1Vel  , 1,    255, 250, 250)
    Sun     = body("nSun.txt"  , SunM  ,  15,  Sunr  , SunI   , SunVel   , 0,    255, 234, 0  )
    Earth   = body("nEarth.txt", EarthM,  6 ,  Earthr, EarthI , EarthVel , 0,    0,   245, 194)
    Jupiter = body("nJup.txt"  , JupM  ,  12,  Jupr  , JupI   , JupVel   , 0,    245, 90,  0  )
    Venus   = body("nVen.txt"  , VenM  ,  5 ,  Venr  , VenI   , VenVel   , 0,    214, 181, 50 ) 
    
    container = bodies(Sun, Earth, Jupiter, Venus, sat1, sat2)
    
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
        dispScale = 100; 
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
        
        
#-----------idk??------------
JupP = 11.86 * 365.26      # jupiter period in days
einitvel = sqrt(((SunM*G)/((Earthr)**2)))
