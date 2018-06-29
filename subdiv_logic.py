import rhinoscriptsyntax as rs
import math
import random
import operator
from operator import itemgetter


class pt_obj(object):
    def __init__(self,id,x,y):
        self.id=id
        self.x=x
        self.y=y

class subdiv(object):
    def __init__(self, site_poly):
        self.site_poly=site_poly
        self.get_segment(self.site_poly)
        
    def get_segment(self,poly):
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
            if(rs.Distance(a,b)>0.1):
                seg_li.append([a,b])
        
        #2. choose the segment
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
        
        for i in split_pts:
            print(i)
        print('\n')
        
        rs.DeleteObject(M)
        
        #6. organize the indices to include splitting points
        split_pt_li=[]
        for i in range(len(poly_pt_li)-1):
            a=poly_pt_li[i][0]
            b=poly_pt_li[i+1][0]
            a_id=poly_pt_li[i][1]
            b_id=poly_pt_li[i+1][1]
            print(a_id, b_id)
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
                    print(id)
        
        split_pt_li.sort(key=operator.itemgetter(1)) # sort the split_id
        p=split_pt_li[0][0]
        q=split_pt_li[1][0]        
        p_id=split_pt_li[0][1]
        q_id=split_pt_li[1][1]        
        
        # 7. Construct the polygons
        poly_1_pts=[]
        poly_1_pts.append(split_pt_li[0])
        X=poly_pt_li[int(math.ceil(p_id)):int(math.floor(q_id))+1]
        for i in X:
            poly_1_pts.append(i)
        poly_1_pts.append(split_pt_li[1])
        poly_1_pts.append(split_pt_li[0])
        
        poly1=[]
        for i in poly_1_pts:
            print('pt: ',i[0])
            rs.AddPoint(i[0])
            poly1.append(i[0])
        poly1x=rs.AddPolyline(poly1)
        
        poly_2_pts=[]
        Y=poly_pt_li[:int(math.ceil(p_id))]#last index not included
        poly_2_pts.append(split_pt_li[1])
        Z=Y+poly_pt_li[int(math.ceil(q_id)):-1]
        for i in Z:
            poly_2_pts.append(i)
        poly_2_pts.append(split_pt_li[1])
        poly2=[]
        k=-1
        for i in poly_2_pts:
            k+=1
            poly2.append(i[0])
        poly2x=rs.AddPolyline(poly2)
        
        rs.CopyObject(poly1x,[0,0,50])
        rs.CopyObject(poly2x,[0,0,100])
        
SITE=rs.GetObject("Pick site curve ")
subdiv(SITE)