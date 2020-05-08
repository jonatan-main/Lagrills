
#---- Choose 2D or 3D display
dim = 3 #D

#------- to solar radiate or not to solar radiate
SolarRadiation = 0

#-------adding bodies
    #0 = ignore.      1 = add       2 = ONLY baseline and that planet   
    #baseline = 1, ONLY display sun, earth and sats - No matter the other numbers
baseline = 1
Venus    = 1
Jupiter  = 1

#Set the baseline to either only sun/satellites (0) or sun/satellite/earth. (1)
whichBase = 0

#------ Choose whether to display.  
 #disp = 1 will display. Won't otherwise. 
disp = 1

# ------ Choose whether to display text about .  
 #disptext = 1 will display. Won't otherwise. 
disptext = 0

#-----Choose timestep for RK4
timestep = 0.01

#-------Size of window
fwidth, fheight = 800 , 800



dispScale = 50                   # pixels/AU

count = 0

#----------------------------------------------------------------------------------------------------------------   
# ----------------------------- Body class ----------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------  

class body(object):
    def __init__(self, name, Mass, rad, position, inclination, velocity, satOrPlan, R, G, B):
        self.col    = list((R, G, B));   self.Mass = Mass       ;      self.EQ_rad = rad;         self.sat = satOrPlan
        self.pos    = position;   self.i    = inclination;      self.name   = name   
        self.velmag = velocity       ;   self.acc  = vec0       ;      self.SaveData = createWriter(self.name)
        
        self.history = [self.pos] 
        self.Epot = 0;      self.Ekin = 0;   self.Epotlist = []
     
        self.c0 = PVector(0,0,0); self.c1 = PVector(0,0,0); self.c2 = PVector(0,0,0); self.c3 = PVector(0,0,0)
        self.k0 = PVector(0,0,0); self.k1 = PVector(0,0,0); self.k2 = PVector(0,0,0); self.k3 = PVector(0,0,0)
         
    #------------------------ Calculate velocity with inclination -----------------------------------------------    
        self.vel   = velocity
        
        
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
            """
            for i in self.history:
                fill(self.col[0], self.col[1] ,self.col[2])
                xhistory = i.x * dispScale + width / 2.0
                yhistory = i.y * dispScale + height / 2.0
                zhistory = i.z * dispScale
                
                
                pushMatrix();   sphere(1);    popMatrix();     translate(xhistory, yhistory, zhistory)  
            """
            if len(self.history) >= 10:
                self.history.pop(1) 
          
    
    # ---------------------------- Printing position --------------------------------------------------
    
    def printer(self):
        #if self.sat == 1:
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
    def __init__(self, sun,earth, sat1, sat2, ven, jup):      #container method for all bodies
        self.bodies = list((sun,earth, sat1, sat2, ven, jup)) #list of all bodies

        self.energysum = 0.0                                    # total energy of the system
    count = 0
        
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
        
        acc     = f_mag * r_norm / bi.Mass; e_sum   =  -G * bi.Mass * bj.Mass / r.mag()
        return    acc, e_sum, r.mag()
        #grav  [0]   [1]    [2]       

#----------------------------------- Solar radiation ------------------------    
    def solar(self, Sun, sat):
        Sun   = Sun;  sat = sat;   
        e     = Sun.pos - sat.pos;   eNorm = e.copy().normalize();    eMag = e.mag()                      # Vector for distance to sun
        n     = sat.vel;             nNorm = n.copy().normalize();                       # Vector for satellite's velocity
        cos0  = (e.x * n.x + e.y * n.y + e.z * n.z)/(e.mag() * n.mag())                  # cos of angle between sun vector and vel vector 
        P     = L/(4*PI*(eMag**2)) * 1/c
        F     = - P*cos0*A*((1 - eps)*eNorm + 2*eps*cos0*nNorm)                          #F = −P cos(θ )A [(1−ε)e + 2ε cos(θ )n]
        accel = F / sat.Mass;   
        return accel

#--------------------- dist printer ---------------------------------------
    def printDist(self, sat1, sat2):
        s1 = sat1;    s2 = sat2; 
        d = s1.pos - s2.pos;  dMag = d.mag()
        dis.print(dMag);      dis.print(",");       dis.flush()     
    
        
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
                if i.sat == 1 and j == self.bodies[0] and SolarRadiation == 1: 
                    solarRad = self.solar(j,i)
                    i.k0 += solarRad
                    #print("k0")
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
                if i.sat == 1 and j == self.bodies[0] and SolarRadiation == 1: 
                    solarRad = self.solar(j,i)
                    i.k1 += solarRad
                    #print("k1")

                
        #-------------------------- c2 & k2 ---------------------------------------
        for i in self.bodies:
            i.c2 = i.vel + tstep/2*i.k1
            i.k2 = PVector(.0,.0,.0)
            for j in self.bodies:
                if j == i:
                    continue
                if i.sat == 1 and j == self.bodies[0] and SolarRadiation == 1: 
                    solarRad = self.solar(j,i)
                    i.k2 += solarRad
                    #print("k2")
                grav = self.gravity(i,j)
                i.k2 += grav[0]          
                      
        #-------------------------- c3 & k3 ---------------------------------------
        for i in self.bodies:
            i.c3 = i.vel + tstep*i.k2
            i.k3 = PVector(.0,.0,.0)
            for j in self.bodies:
                if j == i:
                    continue
                if i.sat == 1 and j == self.bodies[0] and SolarRadiation == 1: 
                    solarRad = self.solar(j,i)
                    i.k3 += solarRad
                    #print("k3")
                grav = self.gravity(i,j)
                i.k3 += grav[0]

                
        #----------------- weighted average ------------------
        for i in self.bodies:
            i.pos += tstep/6*(i.c0 + 2*i.c1 + 2*i.c2 + i.c3)
            i.vel += tstep/6*(i.k0 + 2*i.k1 + 2*i.k2 + i.k3)

            
    # ---------------------------------- Update function ---------------------------------------------
                        
    def update(self):
        for i in range(10):
            self.count += 1
            print('Iterations:   ', self.count)
            self.rk4Step(timestep)       # Integration method RK4
            self.printDist(self.bodies[2],self.bodies[3])
          #  self.testPrint_pos()
        if disp == 1:
            self.display()               # Display system
        #for i in self.bodies:       
         #   i.printer()                  # Save position in .txt file
        self.dumpPos()

    def dumpPos(self):
        SaveData.print(self.count * timestep)
        for i in self.bodies:
            SaveData.print(" " + str(i.pos[0]) + " " + str(i.pos[1]) + " " + str(i.pos[2]))
        SaveData.print('\n')    
    # ------------------------- inertia stuff -------------------------------------
    def inertia(self):
        initV = PVector(0,0,0)
        sysMass = 0.0
        for i in self.bodies:
            tmpV = i.vel * i.Mass
            initV += tmpV
            sysMass += i.Mass
        
        for i in self.bodies:
            i.vel -= initV / sysMass

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
c    = 299792458*T/AU;         L = (3.83e+26) * (T**3)/(M*AU**2)



#----------------  Planets   ----------------------
#planet    mass          ;                                      position                                                ;   inclination   ;    velocity
SunM     = 1.989e+30 / M ;    Sunr   = PVector(0.0, 0.0, 0.0)                                                           ;   SunI   = 0.0  ;    SunVel   =  PVector(0.0, 0.0, 0.0)                                                            #Sun         
EarthM   = 5.24e+24 / M  ;    Earthr = PVector(-9.152923286693947E-01,  3.776418237478736E-01, -1.208588286966104E-05)  ;   EarthI = 0.0  ;    EarthVel = PVector(-6.841340411390929E-03, -1.597525470908048E-02,  6.625416874865121E-07)    #Earth
VenMx    = 4.8675e+24 / M;    Venr   = PVector(-6.998043908272225E-02,  7.158154699036847E-01,  1.386035510207141E-02)  ;   VenI   = 3.39 ;    VenVel = PVector(-2.019909347984435E-02, -2.077073275674056E-03,  1.137128532180597E-03)      #Venus
JupMx    = 1.898e+27 / M ;    Jupr   = PVector(9.470804281047529E-01, -5.119863904201112E+00,  7.568600326021274E-05)   ;   JupI   = 1.304;    JupVel   = PVector(7.337101313074398E-03,  1.730925767269614E-03, -1.713172526105119E-04)     #Jupiter


VenM     = 1/M;      JupM = 1/M;       

if whichBase == 0: 
    EarthM = 1/M;

#------------------- Which planets to use and txt names -----------------
if baseline == 1: 
    if SolarRadiation == 0:
        printName = "BaselineDist.txt";                print("Baseline")
        posPrint  = "Bpos.txt";
    else:
        if SolarRadiation == 1:
            printName = "RAD_BaselineDist.txt";        print("Baseline - Radiation")
            posPrint  = "rBpos.txt";
if baseline != 1:
    if Jupiter == 1 and Venus == 1:
        JupM = JupMx;   VenM = VenMx;  
        if SolarRadiation == 0:
            printName = "VenusJupiterDist.txt";        print("Venus and Jupiter")
            posPrint  = "VJpos.txt";
        if SolarRadiation == 1:
            printName = "RAD_VenusJupiterDist.txt";    print("Venus and Jupiter - Radiation")
            posPrint  = "rVJpos.txt";
    if Venus   == 2:
        VenM = VenMx
        if SolarRadiation == 0:
            printName = "VenusDist.txt";               print("Venus")
            posPrint  = "Vpos.txt";
        if SolarRadiation == 1:
            printName = "RAD_VenusDist.txt";           print("Venus - Radiation")
            posPrint  = "rVpos.txt";
    if Jupiter == 2:
        JupM = JupMx
        if SolarRadiation == 0:
            printName = "JupiterDist.txt";             print("Jupiter") 
            posPrint  = "Jpos.txt";       
        if SolarRadiation == 1:    
            printName = "RAD_JupiterDist.txt";         print("Jupiter - Radiation")
            posPrint  = "rJpos.txt";


#--------------------   Satellites ----------------------------
#satnr     mass          ;    dist from sun                                                                          ;   inclination   ;    velocity
sat1M    = 3000/ M       ;    sat1r  = PVector(9.074193903154508E-01, -4.443287201862671E-01,  1.782264146190762E-05);   sat1I  = 0.0  ;    sat1Vel  = PVector(7.279297845320503E-03,  1.538824941906287E-02, -1.039231649497660E-07);                                           #sat 1 vel(?): + 0.000590254)
sat2r    = PVector(9.000100848742620E-01, -4.596533466028270E-01,  1.793888448704480E-05)  ;                                                sat2Vel  = PVector(7.538996982885025E-03,  1.526027083742198E-02, -1.346088368565081E-07);

vec0 = PVector(.0,.0,.0)


#------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------Setup and draw ------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
    
    
def setup():
    size(fwidth, fheight, P3D)
    global Sun, earth, jupiter, sat1, container, vec0,dis, printName, L, eps, A, count, test, SaveData
    noStroke()
    
   #body    =     (txtPos        mass    rad   dist    incl    initVel    sat?   R    G    B  )
    sat1    = body("nSat1.txt" , 1/M   ,  4 ,  sat1r , sat1I  , sat1Vel  , 1,    255, 250, 200)
    sat2    = body("nSat2.txt" , 1/M   ,  4 ,  sat2r , sat1I  , sat2Vel  , 1,    255, 250, 250)
    Sun     = body("nSun.txt"  , SunM  ,  15,  Sunr  , SunI   , SunVel   , 0,    255, 234, 0  )
    Earth   = body("nEarth.txt", EarthM,  6 ,  Earthr, EarthI , EarthVel , 0,    0,   245, 194)
    Jupiter = body("nJup.txt"  , JupM  ,  12,  Jupr  , JupI   , JupVel   , 0,    245, 90,  0  )
    Venus   = body("nVen.txt"  , VenM  ,  5 ,  Venr  , VenI   , VenVel   , 0,    214, 181, 50 ) 
    SaveData = createWriter(posPrint)
    dis = createWriter(printName)
    container = bodies(Sun, Earth, sat1, sat2, Venus, Jupiter)
    #background(0)
    frameRate(60)
    container.inertia()
    count = 0
    
def draw():
    background(0)
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
