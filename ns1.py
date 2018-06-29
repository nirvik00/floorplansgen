import rhinoscriptsyntax as rs
from ns_read_file import read_obj
import math
import random
import operator
from operator import itemgetter

from ns_subdiv_obj import subdiv_obj

class main_proc(object):
    def __init__(self,Area):
        self.area=Area
        self.poly=self.gen_site()
        self.pts=rs.CurvePoints(self.poly)
        self.func_li=[]
        
        self.R=read_obj()
        self.func_obj()
        s=subdiv_obj(self.poly,self.func_li)
        
    def gen_site(self):
        a=math.sqrt(self.area/3)
        b=3*a
        self.pts=[]
        p0=[0,0,0]
        p1=[a,0,0]
        p2=[a,b,0]
        p3=[0,b,0]
        poly=rs.AddPolyline([p0,p1,p2,p3,p0])
        return poly    
        
    def func_obj(self):
        self.R.read()
        self.func_obj_li=self.R.return_obj()
        for i in self.func_li:
            r=get_rand_range(0.3,3.0)
            x=math.sqrt(i[2]/r)
            y=x*r
            #print('name= %s, area= %s, a= %s, b= %s'%(i[1],i[2],x,y))
        


def get_rand_range(min,max):
    li=[]
    for i in range(100):
        r=(random.random()*max)+min
        li.append(r)
    li.sort()
    min=(li[0])
    max=(li[-1])-min
    n=random.choice(li)
    return n

AREA=29548
main_proc(AREA)