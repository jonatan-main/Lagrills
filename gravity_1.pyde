        
def setup():
    size(1800, 1200)
    global p,s
    p = earth()
    s = Sun()
    
def draw():
    background(255)
    p.show()
    p.update()
    s.show()
    p.Gravity(s.mass)
    

    
    
    
    
