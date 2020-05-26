# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 09:59:43 2020

@author: Mitzie
"""

import xlsxwriter as excel
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from matplotlib.pyplot import figure
import matplotlib as mpl

from mpl_toolkits.mplot3d import Axes3D

import math  
import os
clear = lambda: os.system('cls')  # On Windows System
Maxi = 20
Mini = 30
none = 0

from mpl_toolkits import mplot3d
yes = 1; no = 0;
on = 1; off = 0;
year = 365; iteration = 0.1
spB  = 1;  pB  = 10; pV  = 100; pJ  = 1000; pVJ  = 10000; 
rspB = 2;  rpB = 20; rpV = 200; rpJ = 2000; rpVJ = 20000; 
sys = 0
v1 = 11;
v2 = 12;


fig,ax=plt.subplots()
# -------------------- choose stuff --------------------------
unit = year


plt.rcParams.update({'font.size': 13})

plt.close('all')

SunSat  = open("SunSatDist.txt","r")
Base    = open("BaselineDist.txt","r"); 
Venus   = open("VenusDist.txt","r");     
Jupiter = open("JupiterDist.txt","r");
SRP     = open("SolarDist.txt","r")
ALL     = open("ALLDist.txt","r")
Moon    = open("MoonDist.txt","r")

Base2    = open("BaselineDistv2.txt","r"); 
ALL2     = open("ALLDistv2.txt","r")



#-----Solar rad ------

spB  = open("sBpos.txt","r")
pB   = open("Bpos.txt","r"); 
pV   = open("Vpos.txt","r"); 
pJ   = open("Jpos.txt","r"); 
pSol = open("Solpos.txt","r")
pALL = open("ALLpos.txt","r")
pM   = open("Mpos.txt","r")

pALL2 = open("ALLposv2.txt","r")
pB2   = open("Bposv2.txt","r"); 


year1 = 0.1
year2 = 58
"""
yearOld1 = year1
yearOld2 = year2
"""
#year1 = 40
#year2 = 50


print("year1 = ",year1)
print("year2 = ",year2)
it1 = int(round(year1*10*365.25,0))
it2 = int(round(year2*10*365.25,0))



"""
itOld1 = int(round(yearOld1*10*365.25,0))
itOld2 = int(round(yearOld2*10*365.25,0))
"""

print("range1 = ",it1, " ;  range2= ",it2)



rang = range(it2-it1)
rang2 = 50000
rang3 = 105000


displnDn = off
dispReg  = off

dispDist = on
dispDistReg = off
plt.close('all')


#---- No solar radiation

class body(object):
    def __init__(self, txt, size, color,offset):
        self.txt   = txt;       self.size  = size;       self.color = color; self.offset = offset

    def readSSV(self):
        count = 0
        self.xpos = []; self.ypos = []; self.zpos = [];
        #self.idk = self.txt.read().splitlines()
        self.idk = self.txt
        for line in self.idk:
            if 1 == 1:
                if self.idk[count] == self.idk[-1]:
                    continue
                split = line.split()
                count += 1    
                self.xpos.append(float(split[self.offset*3 + 1]))
                self.ypos.append(float(split[self.offset*3 + 2]))
                self.zpos.append(float(split[self.offset*3 + 3]))
        #return self.xpos, self.ypos, self.zpos
    
    def use(self):
        self.readSSV()

def calculateDistance(body1,body2,name,extrema):  
    dist = []; itnr = []; 
    for i in rang:
        x1 = body1.xpos[it1+i]; y1 = body1.ypos[it1+i]; z1 = body1.zpos[it1+i]; 
        x2 = body2.xpos[it1+i]; y2 = body2.ypos[it1+i]; z2 = body2.zpos[it1+i]; 
        dist.append(math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2))
        itnr.append(it1+i)

    return dist, itnr

#----------------------- Satellite dist --------------------------------
def reader(file):
    num = []
    file = file;  txt = file.read();  txt = txt.split(",")
    for x in range(len(txt)-1): 
    #for x in range(91000):                     #<-- Number of iteration to look at
        curnum = float(txt[x])
        num.insert(x,curnum)
    value = num
    return value

#----------------------- Lyaponov exponent ----------------------------

#initdist = reader(Base)
#print("init dist",initdist[0])

fig, ax = plt.subplots()
#plt.figure(dpi = 100, figsize=(15, 8))


def Lyaponov(data):
    data = data; dn = []; l = []; ldiv =[]; d0 = data[0]
    #for n in range(len(data)):       
        #dn.insert(n,data[n]/d0)
        #l.insert(n,np.log(dn[n]))
        #if n==0: 
       #     ldiv.insert(n,l[n]/1)
      #  else: 
     #       ldiv.insert(n,l[n]/n)
    #N = len(ldiv); Sum = sum(ldiv); LyapExpAve = 1/(N) * Sum; 
    dnlog = np.log(data)
    return 1, dnlog


def regression(data):
    dnlog = data;
    xYears = [x/3652.5 for x in list(range(len(dnlog[rang2:rang3])))]
    
    x = np.array(xYears).reshape((-1,1));  y = np.array(dnlog[rang2:rang3])
    model = LinearRegression().fit(x,y)
    r_sq = model.score(x,y); 

    y_pred     = model.intercept_ + model.coef_ * x
    slope      = str(model.coef_); slope = slope.replace("[", "");   slope = slope.replace("]", "");  slopeFloat = float(slope)
    intercept  = str(model.intercept_); equation  = intercept + " + " + slope + "x" 

    return slope,y_pred, equation, r_sq


#------------------------ Apply the lyapanov ----------------------------
def runData(data,printname,col, col2):
    data = data;  satDistance = reader(data);  
    days = [x/10 for x in range(len(satDistance))]
    years = [x/365.25 for x in days]
    reg  = regression(Lyaponov(satDistance)[1])
    reg1 = regression(satDistance)    
    lndn = Lyaponov(satDistance)[1]
    if dispDist == yes:
        if unit == year: 
            ax.plot(years,satDistance, col ,label = "Distance between the two satellites in the " + printname + " system",linewidth = 1.3); 
            ax.legend(loc='upper left');
            
        #if unit == year: 
         #   ax.plot(years[rang2:rang3],satDistance[rang2:rang3], col ,label = "The " + printname + " system",linewidth = 1.3); 
          #  ax.legend(loc='upper left');
    if dispDistReg == yes:
        if unit == year: 
            ax.plot(years[rang2:rang3],reg1[1],col,linestyle='dashed');#plt.legend(loc='upper left',fontsize=12); plt.xlabel("Time (years)",fontsize=15); plt.ylabel ("Distance (AU)",fontsize=15);    plt.title("Distance between the satellites over time",fontsize=20)
 
    if dispReg  == yes:        
        if unit == year:
            plt.plot(years[rang2:rang3],reg[1],col,linestyle='dashed');plt.xlabel("Time (years)",fontsize=15);      plt.ylabel ("Distance, logarithmic scale",fontsize=15); 

    if displnDn == yes: 
        if unit == year:
            plt.plot(years[rang2:rang3],lndn[rang2:rang3],col,label = "The " + printname + " system"); plt.legend(loc='upper left',fontsize=12); plt.xlabel("Time (years)",fontsize=15);      plt.ylabel ("Distance, logarithmic scale",fontsize=15); # plt.title("Distance between satellites on logarithmic scale over time",fontsize=20)
        #plt.savefig(system + 'lnPlot.png')


        
    #ax.set_ylim(ymin=0.95, ymax=1.7)   
    
    sizzle = 5; mizzle = 'o'
    if col2 == v1:      
        EAR_S1 = calculateDistance(S1,Ear,"dist sat1 to sun",none)
        EAR_s1Dist = EAR_S1[0]; ItNr1 = EAR_S1[1]; 
        EAR_S2 = calculateDistance(S2,Ear,"dist sat2 to sun",none)
        EAR_s2Dist = EAR_S2[0]; ItNr2 = EAR_S2[1]; 

    
        yearNr1 = [x/10/365.25 for x in ItNr1]
        yearNr2 = [x/10/365.25 for x in ItNr2]    
    #ax.plot(yearNr1,EAR_s1Dist,label = "Dist between Earth and satellite 1", c = '#6E006F',marker = 'o', ms = 1); 
    #ax.plot(yearNr2,EAR_s2Dist,label = "Dist between Earth and satellite 2", c ='m' ,marker = 'o',ms = 1); 

    ax2 = ax.twinx()
    if Earth_ == on:
        #ax.plot(yearNr1,EAR_s1Dist,label = "Dist between Earth and satellite 1", c = 'k',marker = 'o', ms = 1); 
        E_col1 = '#f55ffa'; E_col2 = '#6E006F'
        #if col2 == v2:
         #   E_col1 = 'k'; E_col2 = 'k'
        if col2 == v1:
            ax.plot(yearNr1,EAR_s1Dist,label = "Distance between Earth and satellite 1", c = E_col1,linewidth = 1.4);
            ax.plot(yearNr2,EAR_s2Dist,label = "Distance between Earth and satellite 2", c = E_col2,linewidth = 1);



        if col2 == v2:
            v2_EAR_S1 = calculateDistance(v2_S1,v2_Ear,"dist sat1 to sun",none)
            v2_EAR_s1Dist = v2_EAR_S1[0]; ItNr1 = v2_EAR_S1[1]; 
            v2_EAR_S2 = calculateDistance(v2_S2,v2_Ear,"dist sat2 to sun",none)
            v2_EAR_s2Dist = v2_EAR_S2[0]; ItNr2 = v2_EAR_S2[1]; 
            yearNr1 = [x/10/365.25 for x in ItNr1]
            yearNr2 = [x/10/365.25 for x in ItNr2]   
            ax.plot(yearNr1,v2_EAR_s1Dist,label = "Distance between Earth and satellite 1 (comparison system)", c = '#ff9696',linewidth = 1);
            ax.plot(yearNr2,v2_EAR_s2Dist,label = "Distance between Earth and satellite 2 (comparison system)", c ='#ff0000',linewidth = 1);
        
        
    
    if Sun_ == on:
        #ax2 = ax.twinx()
        S_col1 = '#D1C989'; S_col2 = "#D4810A"
        if col2 == v1:
          #  S_col1 = 'k'; S_col2 = 'k'
            Sun_S1 = calculateDistance(S1,Sun,"dist sat1 to sun",none)
            sun_s1Dist = Sun_S1[0]; #ItNr1 = SunS1[1]; 
            Sun_S2 = calculateDistance(S2,Sun,"dist sat2 to sun",none)
            sun_s2Dist = Sun_S2[0]; #ItNr2 = SunS2[1]; 
            ax.plot(yearNr1,sun_s1Dist,label = "Distance between Sun and satellite 1",   c = S_col1 ,linewidth = 1);
            ax.plot(yearNr2,sun_s2Dist,label = "Distance between Sun and satellite 2",   c = S_col2 ,linewidth = 1); 
            ax.legend(loc='upper right',fontsize=12, framealpha = 1  ) 
        if col2 == v2:        
            v2_Sun_S1 = calculateDistance(v2_S1,v2_Sun,"dist sat1 to sun",none)
            v2_sun_s1Dist = v2_Sun_S1[0]; #ItNr1 = SunS1[1]; 
            v2_Sun_S2 = calculateDistance(v2_S2,v2_Sun,"dist sat2 to sun",none)
            v2_sun_s2Dist = v2_Sun_S2[0]; #ItNr2 = SunS2[1]; 
            ax.plot(yearNr1,v2_sun_s1Dist,label = "Distance between Sun and satellite 1",   c = '#11fc00',linewidth = 1);
            ax.plot(yearNr2,v2_sun_s2Dist,label = "Distance between Sun and satellite 2",   c = '#098700',linewidth = 1);         
        
    
    if Jupiter_ == on:
        J_col1 = '#7A2626'; J_col2 = "#D50000"
        #if col2 == v2:
         #   J_col1 = 'k'; J_col2 = 'k'   
        if col2 == v1:
            JUP_S1 = calculateDistance(S1,Jup,"dist sat1 to sun",none)
            JUP_s1Dist = JUP_S1[0]; #ItNr1 = SunS1[1]; 
            JUP_S2 = calculateDistance(S2,Jup,"dist sat2 to sun",none)
            JUP_s2Dist = JUP_S2[0]; #ItNr2 = SunS2[1]; 
            ax2.plot(yearNr1,JUP_s1Dist,label = "Distance between Jupiter and satellite 1",   c = J_col1,linewidth = .8);
            ax2.plot(yearNr2,JUP_s2Dist,label = "Distance between Jupiter and satellite 2",   c = J_col2,linewidth = .8);
        if col2 == v2:      
            
            v2_JUP_S1 = calculateDistance(v2_S1,v2_Jup,"dist sat1 to sun",none)
            v2_JUP_s1Dist = v2_JUP_S1[0]; #ItNr1 = SunS1[1]; 
            v2_JUP_S2 = calculateDistance(v2_S2,v2_Jup,"dist sat2 to sun",none)
            v2_JUP_s2Dist = v2_JUP_S2[0]; #ItNr2 = SunS2[1]; 
            ax.plot(yearNr1,v2_JUP_s1Dist,label = "Distance between Jupiter and satellite 1",   c = '#11fc00',linewidth = 1);
            ax.plot(yearNr2,v2_JUP_s2Dist,label = "Distance between Jupiter and satellite 2",   c = '#098700',linewidth = 1);        
        
        
        
    if Venus_ == on:    
        V_col1 = '#00CE89'; V_col2 = '#008B61'
        #if col2 == v2:
         #   V_col1 = 'k'; V_col2 = 'k'     
        if col2 == v1:
            VEN_S1 = calculateDistance(S1,Ven,"dist sat1 to sun",none)
            VEN_s1Dist = VEN_S1[0]; #ItNr1 = SunS1[1]; 
            VEN_S2 = calculateDistance(S2,Ven,"dist sat2 to sun",none)
            VEN_s2Dist = VEN_S2[0]; #ItNr2 = SunS2[1];     
            ax.plot(yearNr1,VEN_s1Dist,label = "Distance between Venus and satellite 1", c = '#7ad67a',linewidth = 1); 
            ax.plot(yearNr2,VEN_s2Dist,label = "Distance between Venus and satellite 2", c = '#0bab00',linewidth = 1); 
        if col2 == v2:
            v2_VEN_S1 = calculateDistance(v2_S1,v2_Ven,"dist sat1 to sun",none)
            v2_VEN_s1Dist = v2_VEN_S1[0]; #ItNr1 = SunS1[1]; 
            v2_VEN_S2 = calculateDistance(v2_S2,v2_Ven,"dist sat2 to sun",none)
            v2_VEN_s2Dist = v2_VEN_S2[0]; #ItNr2 = SunS2[1];     
            ax.plot(yearNr1,v2_VEN_s1Dist,label = "Distance between Venus and satellite 1", c = '#11fc00',linewidth = 1); 
            ax.plot(yearNr2,v2_VEN_s2Dist,label = "Distance between Venus and satellite 2", c = '#098700',linewidth = 1);     
    
    
    if Moon_ == on:   
        M_col1 = '#C8C8C8'; M_col2 = '#777777'
        
        #if col2 == v2:
         #   M_col1 = 'k'; M_col2 = 'k'           
        if col2 == v1:
            MOO_S1 = calculateDistance(S1,Moo,"dist sat1 to sun",none)
            MOO_s1Dist = MOO_S1[0]; #ItNr1 = SunS1[1]; 
            MOO_S2 = calculateDistance(S2,Moo,"dist sat2 to sun",none)
            MOO_s2Dist = MOO_S2[0]; #ItNr2 = SunS2[1];     
            ax.plot(yearNr1,MOO_s1Dist,label = "Distance between Moon and satellite 1", c = '#4045ff',linewidth = 1); 
            ax.plot(yearNr2,MOO_s2Dist,label = "Distance between Moon and satellite 2", c ='#000487',linewidth = 1);
        
        if col2 == v2:
            v2_MOO_S1 = calculateDistance(v2_S1,v2_Moo,"dist sat1 to sun",none)
            v2_MOO_s1Dist = v2_MOO_S1[0]; #ItNr1 = SunS1[1]; 
            v2_MOO_S2 = calculateDistance(v2_S2,v2_Moo,"dist sat2 to sun",none)
            v2_MOO_s2Dist = v2_MOO_S2[0]; #ItNr2 = SunS2[1];     
            ax.plot(yearNr1,v2_MOO_s1Dist,label = "Distance between Moon and satellite 1", c = '#11fc00',linewidth = 1); 
            ax.plot(yearNr2,v2_MOO_s2Dist,label = "Distance between Moon and satellite 2", c = '#098700',linewidth = 1);
        
    if lineMarks == on:
        co = 'r'
        ax.axvline(x=year_1_1, color=co, linestyle='--',linewidth = 0.8)
        ax.axvline(x=year_2_1, color=co, linestyle='--',linewidth = 0.8)
        ax.axvline(x=year_1_2, color=co, linestyle='--',linewidth = 0.8)
        ax.axvline(x=year_2_2, color=co, linestyle='--',linewidth = 0.8)
        ax.axvline(x=year_1_3, color=co, linestyle='--',linewidth = 0.8)
        ax.axvline(x=year_2_3, color=co, linestyle='--',linewidth = 0.8)
        #ax.axvline(x=year_1_4, color=co, linestyle='--',linewidth = 0.8)
        #ax.axvline(x=year_2_4, color=co, linestyle='--',linewidth = 0.8)
    

    ax.legend(loc='upper left',fontsize = 9, framealpha = 0.95  ) 
    ax.set_xlabel("Time (years)"); ax.set_ylabel ("Distance (AU)",color = 'k');  #ax.set_title("Distance between bodies",fontsize=20)
    ax.tick_params(axis='y', labelcolor='k')
    ax.set_ylim(ymin=0, ymax=2.8)



    if (Sun_ == on and odd == on) or (Jupiter_ == on and odd == on):
        
        ax2.legend(loc='upper right',fontsize=9, framealpha = 1  ) 
        ax2.set_xlabel("Time (years)"); ax2.set_ylabel ("Distance scaled for Jupiter",color = '#D50000',fontsize=13);  
        ax2.tick_params(axis='y', labelcolor='#D50000')
        ax2.set_ylim(ymin=2, ymax=9.5)
   

plt.show()

#-------------------- main code --------------------------------------



#----No radiation -------------



fig,ax = plt.subplots(dpi = 150, figsize=(10, 5))
year_1_1 =  29
year_2_1 =  30
range1_1 = int(round(year_1_1*10*365.25,0))
range2_1 = int(round(year_2_1*10*365.25,0))
#range1_1 =  106653  ;  
#range2_1=  108844

year_1_2 = 45.6
year_2_2  = 47.2
range1_2 = int(round(year_1_2*10*365.25,0)) 
range2_2=  int(round(year_2_2*10*365.25,0))               
""" 
year_1_1 =  29.2
year_2_1 =  29.8
range1_1 =  106653  ;  range2_1=  108844

year_1_2 = 47.1
year_2_2  = 47.7
range1_2 =  172033  ;  range2_2=  174224
"""


#year_1_2 = year_1_1
#year_2_2  = year_2_1
#range1_2 = range1_1
#range2_2=  range2_1  



year_1_3 = 53
year_2_3  = 54
range1_3 = int(round(year_1_3*10*365.25,0)) 
range2_3=  int(round(year_2_3*10*365.25,0)) 

#year_1_3 = year_1_2
#year_2_3  = year_2_2
#range1_3 = range1_2
#range2_3=  range2_2  

year_1_4 = 11.3
year_2_4  = 13
range1_4 = int(round(year_1_4*10*365.25,0)) 
range2_4=  int(round(year_2_4*10*365.25,0)) 


lineMarks = off


sys = pJ

sys2=pB2
system = "baseline"      

"""
syst2 = sys2.read().splitlines()
v2_S1  = body(syst2,.1, "#080303", 3); 
v2_S2  = body(syst2, .1, "#D200DE",4);
v2_Ear = body(syst2,1 , "#3D9839",1); 
v2_Sun = body(syst2,200, "#F6FF05",0); 
v2_Ven = body(syst2, 1 , "#F0C577",5); 
v2_Jup = body(syst2,6 , "#C18B00",6); 
v2_Moo = body(syst2,1 , "#8e8ea4",2); 
v2_IterNr = body(syst2 ,1 , "#b",0); 

v2_S1.use(); 
v2_S2.use()
v2_Ear.use(); v2_Sun.use(); 
#v2_Jup.use(); 
#v2_Ven.use()
#v2_Moo.use()





"""
syst = sys.read().splitlines()
S1  = body(syst,.1, "#080303", 3); 
S2  = body(syst, .1, "#D200DE",4);
Ear = body(syst,1 , "#3D9839",1); 
Sun = body(syst,200, "#F6FF05",0); 
Ven = body(syst, 1 , "#F0C577",5); 
Jup = body(syst,6 , "#C18B00",6); 
Moo = body(syst,1 , "#8e8ea4",2); 
IterNr = body(syst ,1 , "#b",0); 
  
S1.use(); 
S2.use()
Ear.use(); 
Sun.use(); 
Jup.use(); 
#Moo.use()








odd = on


Sun_      = off
Earth_    = on
Jupiter_  = on
Venus_    = off
Moon_     = off

#sSBase = runData(SunSat,  "Sun satellites only",'y',v1);
#sBase  = runData(Base,    "Baseline",'g',v1);    
#sVen   = runData(Venus,   "Venus",'r',v1); #dark yellow
sJup   = runData(Jupiter, "Jupiter",'b',v1); #dark orange
#sSol   = runData(SRP,     "SRP",'c',v1); #blue
#sALL   = runData(ALL,     "Full",'k',v1); #Magenta
#sMoo   = runData(Moon,    "Moon",'#8396E0',v1); #gray/blue ish
   
#sALL2   = runData(ALL2,     "Full v2",'#b5b5b5', v2); #Magenta
#sBase2  = runData(Base2,    "Baseline v2",'#8aff8c', v2);  
              



  







