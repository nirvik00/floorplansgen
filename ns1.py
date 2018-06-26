import rhinoscriptsyntax as rs
from read_file import read_obj
import math
import random
import operator
from operator import itemgetter

class main_proc(object):
    def __init__(self):
        self.R=read_obj()
        self.pts=[]
        self.func_obj_li=[]
        self.gen_site(1000,300)
        self.func_obj()
    def gen_site(self,a,b):
        self.pts=[]
        p0=[0,0,0]
        p1=[a,0.0]
        p2=[a,b,0]
        p3=[0,b,0]
        poly=rs.AddPolyline([p0,p1,p2,p3,p0])
        self.pts.append([p0,p1,p2,p3])
        return poly    
    def func_obj(self):
        self.R.read()
        self.func_obj_li=self.R.return_obj()
        self.place(self.func_obj_li[0])
    def place(self,obj):
        r=get_rand_range(0.3,3)
        x=math.sqrt((obj[2])/r)
        y=x*r
        print("\n\n")
        print('dim: ini area=%s, x=%s, y=%s, final_area=%s'%(obj[2],x,y,x*y))
        
        
        
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


main_proc()