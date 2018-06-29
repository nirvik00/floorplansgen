import rhinoscriptsyntax as rs
import math
import random
import operator
from operator import itemgetter

def gen_rect(a,b,ar,D):
    L=ar/D #D is constant- room depth, L=variable length
    u_=[b[0]-a[0],b[1]-a[1],0]
    norm=math.sqrt((b[0]-a[0])*(b[0]-a[0])+(b[1]-a[1])*(b[1]-a[1]))
    u=[u_[0]/norm,u_[1]/norm,0]
    U=[u[0]*L+a[0],u[1]*L+a[1],0]#next pt
    ru=[-u_[1]/norm,u_[0]/norm,0]
    rU=[ru[0]*D+U[0],ru[1]*D+U[1],0]#perpendicular pt
    V=[ru[0]*D+a[0],ru[1]*D+a[1],0]#last perpendicular pt
    poly=rs.AddPolyline([a,U,rU,V,a])
    rs.ObjectLayer(poly,"ns_rooms")
    return [a,U,rU,V,a],poly

def check_boundary(pt,boundary):
    m=rs.PointInPlanarClosedCurve(pt,boundary)
    if(m==0):
        return True#outside - delete
    else:
        return False#inside - do not delete

def gen_rooms(r,iniU,iniV,room_li,D,boundary,rec_counter):
    ar=random.randint(200,500)
    #D=20
    a=r[0]
    b=r[1]
    ini_di=rs.Distance(iniU,iniV)
    res=gen_rect(a,b,ar,D)
    room=res[1]
    new_a=res[0][1]
    this_di=rs.Distance(new_a,iniV)
    #print('rec: ',rec_counter)
    
    t=check_boundary(new_a,boundary)
    if(t==False):
        rec_counter+=1
        new_r=[new_a,iniV]
        room_li.append(room)
        Global_Room_Li.append(room)
        gen_rooms(new_r,new_a,iniV,room_li,D,boundary,rec_counter)
    else:
        rs.DeleteObject(room)
    return [room_li,D]

def get_spine(boundary, pts=None):
    if(pts==None):
        pts=rs.CurvePoints(boundary)
    k=0
    vec_li=[]
    for i in pts:
        if(k<len(pts)-2):
            vec_li.append([pts[k],pts[k+1]])
        elif(k==len(pts)-2):
            vec_li.append([pts[k],pts[0]])
        k+=1    
    spine=random.choice(vec_li)
    return spine

def get_spine_off(spine,D,corr_di):
    D+=corr_di
    a=spine[0]
    b=spine[1]
    u_=[b[0]-a[0],b[1]-a[1],0]
    norm=rs.Distance(a,b)
    u=[u_[0]/norm,u_[1]/norm,0]
    ru=[-u[1]*D+a[0],u[0]*D+a[1],0]
    v_=[a[0]-b[0],a[1]-b[1],0]
    v=[v_[0]/norm,v_[1]/norm,0]
    rv=[v[1]*D+b[0],-v[0]*D+b[1],0]    
    return [ru,rv]

def init_proc(boundary,corr_di,main_subdiv_li,proc_recursion):
    rs.EnableRedraw(False)
    ini_D=20
    r=get_spine(boundary) # pick a side and make a vector
    L=get_spine_off(r,ini_D,corr_di)
    Q=get_spine_off(L,ini_D,0)
    room_li=[]
    rec_counter=0
    gen_room_li=gen_rooms(r,r[0],r[1],room_li,ini_D,boundary,rec_counter)
    L_room_li=[]
    L_rec_counter=0
    gen_room_li=gen_rooms(L,L[0],L[1],L_room_li,ini_D,boundary,L_rec_counter)
    used_boundary=rs.AddPolyline([r[0],r[1],Q[1],Q[0],r[0]])
    cen=rs.CurveAreaCentroid(used_boundary)[0]
    T=rs.AddTextDot(proc_recursion,cen)
    rs.ObjectLayer(used_boundary,"ns_rooms")
    rs.ObjectLayer(T,"ns_rooms")
    try:
        rem_boundary=rs.CurveBooleanDifference(boundary,used_boundary)[0]    
        srf=rs.AddPlanarSrf(rem_boundary)
        B=rs.BoundingBox(srf)
        Rem_Boundary=rs.AddPolyline([B[0],B[1],B[2],B[3],B[0]])
        rs.ObjectLayer(Rem_Boundary,"ns_rooms")
        rs.DeleteObjects([rem_boundary,srf,used_boundary])
        rs.EnableRedraw(True)
        proc_recursion+=1
        rs.GetString("Type key to continue")
        new_Site=init_proc(Rem_Boundary,Corr_Di,main_subdiv_li,proc_recursion)
    except:
        pass

rs.ClearCommandHistory()
rs.AddLayer("ns_rooms")
Corr_Di=5
Global_Room_Li=[]
Site=rs.GetObject('Pick Site')
Boundary=Site

rc=0
yn="t"
main_subdiv_li=[]
while((yn!="n" or yn!="N") and rc<10):
    rc+1
    yn=rs.GetString("run code? ")
    if(yn=="n" or yn=="N"):
        break
    else:
        X=rs.ObjectsByLayer("ns_rooms")
        rs.DeleteObjects(X)
        dup_Site=rs.CopyObject(Site, [0,0,0])
        main_subdiv_li.append(dup_Site)
        new_Site=init_proc(Boundary,Corr_Di,main_subdiv_li,0)
