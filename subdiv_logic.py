import rhinoscriptsyntax as rs
import math
import random
import operator
from operator import itemgetter


class subdiv(object):
    def __init__(self, site_poly):
        self.site_poly=site_poly
        
        
        self.main_counter=0
        self.max_recursion=8
        self.get_segment(self.site_poly,0)
        
        #print('number of recursions= %s'%(self.main_counter))
        
    def get_segment(self,poly,rec_counter):
        #rec_counter
        rec_counter+=1
        self.main_counter+=1
        #1. create segments of poly
        poly_pts=rs.CurvePoints(poly)
        poly_pt_li=[]
        k=-1
        for i in poly_pts:
            k+=1
            poly_pt_li.append([i,k])
        seg_li=[]
        for i in range(len(poly_pts)-1):
            a=poly_pts[i]
            b=poly_pts[i+1]
            d=rs.Distance(a,b)
            if(rs.Distance(a,b)>0.1):
                seg_li.append([a,b,d])
        
        #2. choose the segment
        seg_li.sort(key=operator.itemgetter(2))
        L=random.choice(seg_li)
        
        #3. get point on the segment
        p=[(L[0][0]+L[1][0])/2,(L[0][1]+L[1][1])/2,0]
        
        #4. find the normal
        norm=rs.Distance(L[0],L[1])
        u=[(L[1][0]-L[0][0])/norm,(L[1][1]-L[0][1])/norm,0]
        ru=[p[0]-u[1],p[1]+u[0],0]
        rru=[p[0]+u[1],p[1]-u[0],0]
        q_=None
        if(rs.PointInPlanarClosedCurve(ru,poly)==0):
            q_=rru
        else:
            q_=ru
        q=[q_[0]+(q_[0]-p[0])*1000,q_[1]+(q_[1]-p[1])*1000,0]
        M=rs.AddLine(p,q) #vector from p to infinity in direction pq
        
        #5. find intersection with poly
        intx=rs.CurveCurveIntersection(M,poly)
        split_pts=[intx[0][1],intx[1][1]]        
        rs.DeleteObject(M)
        
        #6. organize the indices to include splitting points
        split_pt_li=[]
        ids=[]
        split_ids=[]
        for i in range(len(poly_pt_li)):
            ids.append(i)
            split_pt_li.append(poly_pt_li[i])
        for i in range(len(poly_pt_li)-1):
            a=poly_pt_li[i][0]
            b=poly_pt_li[i+1][0]
            a_id=poly_pt_li[i][1]
            b_id=poly_pt_li[i+1][1]
            norm1=rs.Distance(a,b)
            u=[(b[0]-a[0]),(b[1]-a[1]),0]
            for c in split_pts:
                norm2=rs.Distance(a,c)
                v=[c[0]-a[0],c[1]-a[1],0]
                x=a[0]+u[0]*((u[0]*v[0]+u[1]*v[1])/(norm1*norm1))
                y=a[1]+u[1]*((u[0]*v[0]+u[1]*v[1])/(norm1*norm1))
                z=0
                pt=[x,y,z]
                d=rs.Distance(pt,c)
                if(d<1):
                    id=(a_id+b_id)/2
                    split_pt_li.append([c,id])
                    ids.append(id)
                    split_ids.append(id)
        ids.sort()
        split_ids.sort()
        p=split_ids[0]
        q=split_ids[1]
        split_pt_li.sort(key=operator.itemgetter(1)) # sort the split_id       
        pt_p=None
        for i in split_pt_li:
            pt=i[0]
            id=i[1]
            if(id==p):
                pt_p=pt
        pt_q=None
        for i in split_pt_li:
            pt=i[0]
            id=i[1]
            if(id==q):
                pt_q=pt
        
        # 7. Construct the polygons
        # 7a. first polygon
        ids_1=ids[int(p+0.5):int(q+0.5)+1]
        poly_1_pts=[]
        k=-1
        for i in ids_1:
            k+=1
            for j in split_pt_li:
                pt=j[0]
                id=j[1]
                if(id==i):
                    poly_1_pts.append(pt)
        poly_1_pts.append(pt_q)
        poly_1_pts.append(pt_p)
        
        # 7b. second polygon
        poly_2_pts=[]
        poly_2_pts.append(pt_p)
        poly_2_pts.append(pt_q)
        for j in split_pt_li:
            pt=j[0]
            id=j[1]
            if(id>q):
                if(pt not in poly_2_pts):
                    poly_2_pts.append(pt)
        for j in split_pt_li:
            pt=j[0]
            id=j[1]
            if(id<p):
                if(pt not in poly_2_pts):
                    poly_2_pts.append(pt)    
        poly_2_pts.append(pt_p)
        
        #8. Continue the recursion
        try:
            poly1=rs.AddPolyline(poly_1_pts)     
            poly2=rs.AddPolyline(poly_2_pts)
            rs.DeleteObject(poly)
            #if(self.main_counter<3):
            if(rec_counter<3):
                self.get_segment(poly1,rec_counter)
                self.get_segment(poly2,rec_counter)
        except:
            pass
        
        
rs.EnableRedraw(False)
SITE=rs.GetObject("Pick site curve ")
b=rs.BoundingBox(SITE)
x=rs.Distance(b[0],b[1])
y=rs.Distance(b[1],b[2])
a=10
b=3
for i in range(a):
    for j in range(b):
        siteX=rs.CopyObject(SITE,[i*(1.5*x),j*(1.25*y),0])
        subdiv(siteX)

rs.EnableRedraw(True)