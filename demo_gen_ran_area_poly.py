import rhinoscriptsyntax as rs
import math
import random


def gen_site():
    a=200
    b=a/3
    p0=[0,0,0]
    p1=[a,0,0]
    p2=[a,b,0]
    p3=[0,b,0]
    poly=rs.AddPolyline([p0,p1,p2,p3,p0])
    return poly

def gen_subdiv_poly(a,b,poly,ar):
    norm=rs.Distance(a,b)
    m=random.random()*norm
    ve=[(b[0]-a[0])/norm,(b[1]-a[1])/norm,0] # vector along side ab
    vec=[(b[0]-a[0])*m/norm,(b[1]-a[1])*m/norm,0] 
    p=[a[0]+vec[0],a[1]+vec[1],0] # point p on segment ab
    u=[p[0]-ve[1],p[1]+ve[0],0] # vector normal to ab at p
    v=[p[0]+ve[1],p[1]-ve[0],0]
    if(rs.PointInPlanarClosedCurve(u,poly)==0):
        r=[v[0],v[1],0]
    else:
        r=[u[0],u[1],0]
    rs.AddPoint(p)
    rs.AddLine(p,r)

def gen_corr(poly):
    pts=rs.CurvePoints(poly)
    r=random.choice([0,len(pts)-2])
    if(r==0):
        a=len(pts)-2
        b=r
        print('con 1')
    else:
        a=r-1
        b=r
        print('con 2')
    area0=100
    gen_subdiv_poly(pts[a],pts[b],poly,area0)

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


rs.ClearCommandHistory()
Poly=gen_site()
gen_corr(Poly)