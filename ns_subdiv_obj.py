import rhinoscriptsyntax as rs
import math
import random
import operator
from operator import itemgetter

class subdiv_obj(object):
    def __init__(self,poly_,func_li_):
        self.site_poly=poly_
        self.func_li=func_li_
        
        self.check_subdiv()
        
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
        
    def check_subdiv(self):
        pts=rs.CurvePoints(self.site_poly)
        seg_li=[]
        for i in range(len(pts)-1):
            d=rs.Distance(pts[i],pts[i+1])
            if(d>0.001):
                seg_li.append([pts[i],pts[i+1],d])
        seg_li.sort(key=operator.itemgetter(2), reverse=True)
        L=([seg_li[0][0],seg_li[0][1]])
        site_area=rs.CurveArea(self.site_poly)[0]
        bool_subdiv_ar=False
        req_ar=None
        for i in self.func_li:
            print(i)
            name=i[0]
            ar=i[1]
            if(ar>0.75*site_area and ar<1.25*site_area):
                print('found: %s'%(ar))
                bool_subdiv_ar=True
                req_ar=ar
                break
            pass
        self.subdiv(req_ar,L[0],L[1])# area,u,v
    
    def subdiv(self,ar,u,v):
        print('None')
        if(ar==None):
            p=[(u[0]+v[0])/2,(u[1]+v[1])/2,0]
            rs.AddPoint(p)      
            norm=rs.Distance(u,v)
            A=[(v[0]-u[0])/norm,(v[1]-u[1])/norm,0]
            rA=[-A[1],A[0],0]
            rrA=[A[1],-A[0],0]
            t0=rs.PointInPlanarClosedCurve(rA,self.site_poly)
            t1=rs.PointInPlanarClosedCurve(rrA,self.site_poly)
            q=None
            if(t0==0):
                q=[rA[0]+p[0],rA[1]+p[1],0]
            else:
                q=[rrA[0]+p[0],rrA[1]+p[1],0]
                
            rs.AddLine(p,q)
            m=1000
            U=[p[0]+(q[0]-p[0])*m,p[1]+(q[1]-p[1])*m,0]
            L=rs.AddLine(U,p)
            req_pt=None
            intx=rs.CurveCurveIntersection(L,self.site_poly)
            if(intx and len(intx)>0):
                req_pt=intx[0][1]
            rs.AddPoint(req_pt)
            rs.DeleteObject(L)
            additional_pts.append([req_pt,p])
            self.split_poly(additional_pts)
    
    def split_poly(self,pts):
        site_pts=rs.CurvePoints(self.site_poly)
        seg_li=[]
        for i in range(len(site_pts)-1):
            a=site_pts[i]
            b=site_pts[i+1]
            d=rs.Distance(a,b)
            if(d>0.01 and [a,b] not in seg_li):
                seg_li.append([a,b])
        
            
            
            
