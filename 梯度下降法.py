#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from sympy import *
import sys
import re


# In[2]:


f=open("input.txt", "r", encoding="utf-8-sig")
str_f=f.read()
f.close()
text=[]
text=str_f.split("\n")
variable_number = len(text)-2

print(text)
print(variable_number)


# In[3]:


if "max" in text[-2]:
    temp_str=text[-2].replace("-","+")
    temp_list=[]
    for i in range(len(text[-2])):
        if temp_str[i] == "+" and text[-2][i] == "+":
            temp_list.append("-")
        else:
            temp_list.append(temp_str[i])
    text[-2]=''.join(temp_list)
    if "max=+" not in text[-2]:
        text[-2]=text[-2].replace("max=","max=-")
text[-2]


# In[4]:


names = locals()
for i in range(0,variable_number):
    exec(text[i])
    
y = eval(text[-2][4:])
print(y)

Epsilon = float(text[-1])

Derivative=[]
for i in range(0,variable_number):
    Derivative.append(diff(y,names['x' + str(i+1)]))
Derivative = tuple(Derivative)
    
print(Derivative)
print(Epsilon)


# In[5]:


position_dict={}
for i in range(0,variable_number):
    position_dict[names['x' + str(i+1)]]=0
print(position_dict)
position_dict[x1]=1
#Grad=list(Derivative) 


# In[6]:


while(1):
    Grad=list(Derivative)
    for i in range(0,variable_number):
        Grad[i]=Grad[i].evalf(subs =position_dict)
    print(Grad)
    Grad_np=np.array(Grad, dtype='float64')
    abs_Grad_np=float(np.linalg.norm(Grad_np))
    print(abs_Grad_np)
    if abs_Grad_np<Epsilon:
        Objective_value=y.evalf(subs =position_dict)
        if "max" in text[-2]:
            Objective_value = -Objective_value
        print(position_dict)
        print(Objective_value)
        break;
    P=-(Grad_np/abs_Grad_np)
    print(P)

    h=symbols('h')
    X_hP={}
    for i in range(0,variable_number):
        X_hP[names['x' + str(i+1)]]=position_dict[names['x' + str(i+1)]]+h*P[i]
    print(X_hP)
    minf=y.subs(X_hP)
    print(minf)
    der_minf=diff(minf,h)
    print(der_minf)
    h_solution=solve(der_minf,h)[0]
    print(h_solution)
    for i in range(0,variable_number):
        position_dict[names['x' + str(i+1)]]=position_dict[names['x' + str(i+1)]]+h_solution*P[i]
    print(position_dict)
    print("\n")


# In[7]:


f=open("output.txt", "w", encoding="utf-8")
f.truncate()
f.write("Status: Local optimal solution found."+"\n")
for i in range(0,variable_number):
    f.write('x' + str(i+1)+': ')
    f.write("%.3f" %position_dict[names['x' + str(i+1)]])
    f.write("\n")
f.write("Objective value: "+"%.3f"%Objective_value+"\n")
f.write("Epsilon: "+str(Epsilon))
f.close()
