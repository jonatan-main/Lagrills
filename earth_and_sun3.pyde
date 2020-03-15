#Adding Lagrange points
#centered coordinate system

# constants
m_sun   = 1.89e+30 #kg #mass of the sun
m_earth = 5.97*10**24 #kg #mass of the earth
d       = 149600 #km #distance earth-sun
G       = 6.67408e-11 #m3/(kg*s2) #universal gravitational constant
r_sun   = 696340 #km #radius of the sun
r_earth = 6371 * 10 #km #radius of the earth
k       = 10000 #scaling factor

class Body():
    def __init__(self,m,rad,x0,y0,vx0,vy0,ax0,ay0,r,g,b):
        self.m   = m
        self.rad = rad
        self.loc = PVector (x0, y0)
        self.v   = PVector (vx0, vy0)
        self.a   = PVector (ax0, ay0)
        self.col = PVector (r,g,b)
        
    def update(self):
        self.a.mult(0.00000000001)
        self.v.add(self.a)
        self.loc.add(self.v)
        self.a.mult(0)
       
    def applyForce(self, force):
        self.f = force.copy()
        self.a.add(self.f.div(self.m))

    def display(self):
        fill(self.col[0],self.col[1],self.col[2])
        ellipse(self.loc[0], self.loc[1], self.rad/k, self.rad/k)
       
def setup():
    size(1000,1000)
    global sun,earth,F,L2_loc
    
    sun   = Body(m_sun, r_sun, 0, 0,0,0,0,0, 255,255,0)
    earth = Body(m_earth, r_earth, sun.loc[0]+d/1000, sun.loc[1],0,3,0,0, 0,0,255)
    F = m_earth * G * m_sun / d**2
    print(F)
    L2_loc = PVector (0,0)
    L2_loc[0] = earth.loc[0] * (1+(m_earth/(3*m_sun))**(1/3))
    print(L2_loc)
    print(L2_loc.mag())
        
def draw():
    background(255)
    translate(width/2, height/2)
    sun.display()
    
    forcedirection = sun.loc-earth.loc
    dirnormalized = forcedirection.normalize()
    force = dirnormalized.mult(F)
    earth.applyForce(force)
    earth.update()
    earth.display()
    
    v = earth.loc.copy()
    L2_direction = v.normalize()
    L2_locnew = L2_loc.mag() * L2_direction
    fill(0)
    ellipse(L2_locnew[0], L2_locnew[1], 5,5)
    
## NOTES    
#Calculation of L2
# x = r2 * (1+(M2/(3M1)**(1/3))
#L2_loc = PVector (0,0)
#L2_loc[0] = earth.loc[0] * (1+(m_earth/(3*m_sun))**(1/3))
# earth.loc-L2_loc = vector from earth to L2
    
    
    
    
