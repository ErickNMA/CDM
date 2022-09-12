import math as m
from tabnanny import check



#class FOURLINKS:
#    def __init__(self, L1, L2, L3, L4):
#        self.L1 = L1
#        self.L2 = L2
#        self.L3 = L3
#        self.L4 = L4
#    
#    def ptn(self):
#        print(self.L1)
#    
#
#teste = FOURLINKS(1, 2, 3, 4)
#
#teste.ptn()

def checkLinks(links, coords):
    cont = 0
    for j in range(len(links)):
        i = j+4
        if(((((coords[i%4][0]-coords[(i-1)%4][0])**2) + ((coords[i%4][1]-coords[(i-1)%4][1])**2)) - (links[i%4]**2)) < 1e-6):
            cont += 1
    if(cont == len(links)):
        return True
    else:
        return False



#Entrada:
L1 = 200
L2 = 80
L3 = 180
L4 = 150
theta2 = 70
ref = [0, 0] #origem das coordenadas
cruzado = False

#Cálculos:
links = [L1, L2, L3, L4]
z = m.sqrt((L1**2) + (L2**2) - (2*L1*L2*m.cos(theta2*m.pi/180.0)))
joints = []
solutions = []
angles = []
cont = 0
for i in range(2):
    alpha = (180*m.acos(((z**2) + (L4**2) - (L3**2))/(2*z*L4))/m.pi)*((-1)**i)
    for j in range(2):
        beta = (180*m.acos(((z**2) + (L1**2) - (L2**2))/(2*z*L1))/m.pi)*((-1)**j)
        for k in range(2):
            theta3 = ((((-1)**k)*m.acos(((L4**2) + (L1**2) - (L2**2) - (L3**2) - (2*L4*L1*m.cos((alpha+beta)*m.pi/180.0)))/(2*L2*L3))*180/m.pi)+theta2)
            for l in range(2):
                theta4 = (180-(alpha+beta))*((-1)**l)
                print(alpha, beta, theta3, theta4)
                for n in range(2):
                    joints.clear()
                    #J12:
                    joints.append(ref)
                    #J23:
                    joints.append([ref[0]+(L2*m.cos(theta2*m.pi/180.0)), ref[1]+(L2*m.sin(theta2*m.pi/180.0))])
                    #J34
                    if(n):
                        joints.append([joints[1][0]+(L3*m.cos(theta3*m.pi/180.0)), joints[1][1]+(L3*m.sin(theta3*m.pi/180.0))])
                    else:
                        joints.append([(ref[0]+L1)+(L4*m.cos(theta4*m.pi/180.0)), ref[1]+(L4*m.sin(theta4*m.pi/180.0))])
                    #J41:
                    joints.append([(ref[0]+L1), ref[1]])

                    if(checkLinks(links, joints)):
                        if(joints not in solutions):
                            solutions.append(joints)
                            gamma = (180*m.acos(((z**2) - (L3**2) - (L4**2))/(-2*L3*L4))/m.pi)*((-1)**i)
                            angles.append([theta2, theta3, gamma, theta4])
                            cont += 1



print(solutions)

print(angles)

print(cont)