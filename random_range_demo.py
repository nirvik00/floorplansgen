import random
import operator
from operator import itemgetter
import rhinoscriptsyntax as rs

rs.ClearCommandHistory()


li=[]
for i in range(100000):
    r=(random.random()*3)+0.3
    li.append(r)
li.sort()
min=(li[0])
max=(li[-1])-0.3
n=random.choice(li)
#print(min,max,n)
return n