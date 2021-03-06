import rhinoscriptsyntax as rs
import operator
from operator import itemgetter
import math
from ns_func_obj_file import func_obj

class read_obj(object):
    def __init__(self):     
        self.func_obj_li=[]
    def read(self):
        filename='function_obj.csv'
        with open(filename, "r") as file:
            x=file.readlines()      
        file.close()    
        obj_li=[]
        k=-1
        for i in x:
            k+=1
            if(k>0):
                nm=i.split(",")[0]
                if(nm=="" or not nm):
                    break                
                ar=float((i.split(",")[1]).split("\n")[0])
                self.func_obj_li.append([k,nm,ar])
                
    def return_obj(self):    
        self.func_obj_li.sort(key=operator.itemgetter(2))
        return self.func_obj_li


#######################
"""
rs.ClearCommandHistory()
R=read_obj()
R.read()
R.return_obj()
"""
##########################