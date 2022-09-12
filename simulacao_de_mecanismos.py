import math as m



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



#Entrada:
L1 = 200
L2 = 80
L3 = 180
L4 = 150
theta2 = 70
ref = [0, 0] #origem das coordenadas

#Cálculos:
z = m.sqrt((L1**2) + (L2**2) - (2*L1*L2*m.cos(theta2*m.pi/180.0)))
gamma = (180*m.acos(((z**2) - (L3**2) - (L4**2))/(-2*L3*L4))/m.pi)
alpha = (180*m.acos(((z**2) + (L4**2) - (L3**2))/(2*z*L4))/m.pi)
beta = (180*m.acos(((z**2) + (L1**2) - (L2**2))/(2*z*L1))/m.pi)
theta4 = (180-(alpha+beta))
theta3 = ((m.acos(((L4**2) + (L1**2) - (L2**2) - (L3**2) - (2*L4*L1*m.cos((alpha+beta)*m.pi/180.0)))/(2*L2*L3))*180/m.pi)+theta2)

#Definição das coordenadas das juntas do mecanismo:
joints = []
#J12:
joints.append(ref)
#J23:
joints.append([ref[0]+(L2*m.cos(theta2*m.pi/180.0)), ref[1]+(L2*m.sin(theta2*m.pi/180.0))])
#J34
joints.append([joints[1][0]+(L3*m.cos(theta3*m.pi/180.0)), joints[1][1]+(L3*m.sin(theta3*m.pi/180.0))])
#J41:
joints.append([(ref[0]+L1), ref[1]])



print(joints)