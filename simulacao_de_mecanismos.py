import math as m
import copy
import cv2 as cv
import numpy as np



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



def hasSimilar(n, list):
    for i in range(len(list)):
        if((abs(n-list[i])<1e-6)):
            return True
    return False

def checkLinks(links, coords):
    cont = 0
    for j in range(len(links)):
        i = j+4
        if(abs((((coords[i%4][0]-coords[(i-1)%4][0])**2) + ((coords[i%4][1]-coords[(i-1)%4][1])**2)) - (links[i%4]**2)) < 1e-4):
            cont += 1
    if(cont == len(links)):
        return True
    else:
        return False

def isIn(n, list):
    cont = 0
    for i in range(len(list)): #solução i
        cont = 0
        for j in range(len(list[i])): #junta j
            for k in range(len(list[i][j])): #coordenada k
                if(abs(list[i][j][k]-n[j][k])<1):
                    cont += 1
        #print(cont)
        if(cont == 8):
            return True
    return False

def kinematicsSolve(ang, cross=False, plot=False, dinamic=False):
    #Entrada:
    L1 = 180
    L2 = 50
    L3 = 150
    L4 = 100
    theta2 = ang    
    ref = [0, 0] #origem das coordenadas

    links = [L1, L2, L3, L4]

    possible_angles = []

    possible_angles.append([theta2])

    #Cálculos de todos os possíveis ângulos:
    z = m.sqrt((L1**2) + (L2**2) - (2*L1*L2*m.cos(theta2*m.pi/180.0)))
    #gamma
    gamma = (180*m.acos(((z**2) - (L3**2) - (L4**2))/(-2*L3*L4))/m.pi)
    possible_angles.append([((gamma%360)*(gamma/abs(gamma+1e-12))), (((360-gamma)%360)*((360-gamma)/abs((360-gamma)+1e-12)))])
    #alpha
    alpha = (180*m.acos(((z**2) + (L4**2) - (L3**2))/(2*z*L4))/m.pi)
    possible_angles.append([((alpha%360)*(alpha/abs(alpha+1e-12))), (((360-alpha)%360)*((360-alpha)/abs(360-alpha+1e-12)))])
    #beta
    beta = (180*m.acos(((z**2) + (L1**2) - (L2**2))/(2*z*L1))/m.pi)
    possible_angles.append([((beta%360)*(beta/abs(beta+1e-12))), (((360-beta)%360)*((360-beta)/abs((360-beta+1e-12))))])
    #theta4
    possible_angles.append([])
    for i in range(2):
        for j in range(2):
            theta4 = (180-(possible_angles[2][i]+possible_angles[3][j]))
            possible_angles[4].append((theta4%360)*(theta4/abs(theta4+1e-12)))
    #theta3
    possible_angles.append([])
    for i in range(2):
        for j in range(2):
            x = (m.acos(((L4**2) + (L1**2) - (L2**2) - (L3**2) - (2*L4*L1*m.cos((possible_angles[2][i]+possible_angles[3][j])*m.pi/180.0)))/(2*L2*L3))*180/m.pi)
            possible_angles[5].append(((x+theta2)%360)*((x+theta2)/abs((x+theta2+1e-12))))
            possible_angles[5].append(((360+possible_angles[5][len(possible_angles[5])-1])%360)*((360+possible_angles[5][len(possible_angles[5])-1])/abs(360+possible_angles[5][len(possible_angles[5])-1]+1e-12)))
            possible_angles[5].append(((360-possible_angles[5][len(possible_angles[5])-1])%360)*((360-possible_angles[5][len(possible_angles[5])-1])/abs(360-possible_angles[5][len(possible_angles[5])-1]+1e-12)))
            possible_angles[5].append(((-x+theta2)%360)*((-x+theta2)/abs((-x+theta2+1e-12))))
            possible_angles[5].append(((360+possible_angles[5][len(possible_angles[5])-1])%360)*((360+possible_angles[5][len(possible_angles[5])-1])/abs(360+possible_angles[5][len(possible_angles[5])-1]+1e-12)))
            possible_angles[5].append(((360-possible_angles[5][len(possible_angles[5])-1])%360)*((360-possible_angles[5][len(possible_angles[5])-1])/abs(360-possible_angles[5][len(possible_angles[5])-1]+1e-12)))

    #Filtrar ângulos iguais e ângulos de interesse:
    angles = []
    #theta2:
    angles.append(possible_angles[0])
    #theta3:
    angles.append([])
    for i in range(len(possible_angles[5])):
        if(not hasSimilar(possible_angles[5][i], angles[1])):
            angles[1].append(possible_angles[5][i])
    #gamma:
    angles.append([])
    for i in range(len(possible_angles[1])):
        if(not hasSimilar(possible_angles[1][i], angles[2])):
            angles[2].append(possible_angles[1][i])
    #theta4:
    angles.append([])
    for i in range(len(possible_angles[4])):
        if(not hasSimilar(possible_angles[4][i], angles[3])):
            angles[3].append(possible_angles[4][i])



    #Findind solutions:
    joints = []
    solutions = []
    cont = 0
    for i in range(len(angles[1])):
        for j in range(len(angles[3])):
            for k in range(2):
                #Definição das coordenadas das juntas do mecanismo:
                joints.clear()
                #J12:
                joints.append(ref)
                #J23:
                joints.append([ref[0]+(L2*m.cos(theta2*m.pi/180.0)), ref[1]+(L2*m.sin(theta2*m.pi/180.0))])
                if(k%2):
                    #J34
                    joints.append([joints[1][0]+(L3*m.cos(angles[1][i]*m.pi/180.0)), joints[1][1]+(L3*m.sin(angles[1][i]*m.pi/180.0))])
                    #J41:
                    joints.append([(ref[0]+L1), ref[1]])
                else:
                    lastjoint = [(ref[0]+L1), ref[1]]
                    #J34
                    joints.append([lastjoint[0]+(L4*m.cos(angles[3][j]*m.pi/180.0)), lastjoint[1]+(L4*m.sin(angles[3][j]*m.pi/180.0))])
                    #J41:
                    joints.append(lastjoint)
                
                

                if(checkLinks(links, joints)):
                    #print("--------------------------------\nJOINTS: ", joints)
                    if(not isIn(joints, solutions)):
                        aux = copy.deepcopy(solutions)
                        aux.append(joints)
                        solutions.clear()
                        solutions = copy.deepcopy(aux)
                        cont += 1
                    #print("SOL: ", solutions, "\n--------------------------------")

    #Definição dos ângulos:
    #conf. aberta:
    final_angles = []
    t2 = (m.atan((solutions[0][0][1]-solutions[0][1][1])/(solutions[0][0][0]-solutions[0][1][0]))*180/m.pi)
    t3 = (m.atan((solutions[0][1][1]-solutions[0][2][1])/(solutions[0][1][0]-solutions[0][2][0]))*180/m.pi)
    y = (m.acos(((z**2)-(L3**2)-(L4**2))/(-2*L3*L4))*180/m.pi)
    t4 = ((m.atan((solutions[0][2][1]-solutions[0][3][1])/(solutions[0][2][0]-solutions[0][3][0]))*180/m.pi)+180)
    final_angles.append([t2, t3, y, t4])
    #conf. cruzada  :
    t2 = (m.atan((solutions[1][0][1]-solutions[1][1][1])/(solutions[1][0][0]-solutions[1][1][0]))*180/m.pi)
    t3 = (m.atan((solutions[1][1][1]-solutions[1][2][1])/(solutions[1][1][0]-solutions[1][2][0]))*180/m.pi)
    y = (360-(m.acos(((z**2)-(L3**2)-(L4**2))/(-2*L3*L4))*180/m.pi))
    t4 = (360-((m.atan((solutions[1][2][1]-solutions[1][3][1])/(solutions[1][2][0]-solutions[1][3][0]))*180/m.pi)+180))
    final_angles.append([t2, t3, y, t4])

    print("\n\n\n*******************************************************************************************************")
    print("Configuração Aberta:")
    print("Ângulos: ", "\t theta2 =", round(final_angles[0][0], 4), "\t theta3 =", round(final_angles[0][1], 4), "\t gamma =", round(final_angles[0][2], 4), "\t theta4 =", round(final_angles[0][3], 4))
    print("\nConfiguração Cruzada:")
    print("Ângulos: ", "\t theta2 =", round(final_angles[1][0], 4), "\t theta3 =", round(final_angles[1][1], 4), "\t gamma =", round(final_angles[1][2], 4), "\t theta4 =", round(final_angles[1][3], 4))
    print("\n*******************************************************************************************************\n\n\n")

    if(plot):
        #Plotagem
        origem = [460, 350]
        scale = 3
        w = 1280
        h = 720
        frame = np.ones((h, w, 3)) * 255
        if(cross):
            #Link 1:
            p1a = origem[0]+(scale*solutions[1][3][0])
            p1b = h-origem[1]-(scale*solutions[1][3][1])
            p2a = origem[0]+(scale*solutions[1][0][0])
            p2b = h-origem[1]-(scale*solutions[1][0][1])
            cv.line(frame, (int(p1a), int(p1b)), (int(p2a), int(p2b)), (0, 255, 255), 15)
            #Link 2:
            p1a = origem[0]+(scale*solutions[1][0][0])
            p1b = h-origem[1]-(scale*solutions[1][0][1])
            p2a = origem[0]+(scale*solutions[1][1][0])
            p2b = h-origem[1]-(scale*solutions[1][1][1])
            cv.line(frame, (int(p1a), int(p1b)), (int(p2a), int(p2b)), (255, 0, 0), 15)
            #Link 3:
            p1a = origem[0]+(scale*solutions[1][1][0])
            p1b = h-origem[1]-(scale*solutions[1][1][1])
            p2a = origem[0]+(scale*solutions[1][2][0])
            p2b = h-origem[1]-(scale*solutions[1][2][1])
            cv.line(frame, (int(p1a), int(p1b)), (int(p2a), int(p2b)), (0, 255, 0), 15)
            #Link 4:
            p1a = origem[0]+(scale*solutions[1][2][0])
            p1b = h-origem[1]-(scale*solutions[1][2][1])
            p2a = origem[0]+(scale*solutions[1][3][0])
            p2b = h-origem[1]-(scale*solutions[1][3][1])
            cv.line(frame, (int(p1a), int(p1b)), (int(p2a), int(p2b)), (0, 0, 255), 15)
            cv.imshow("Configuracao Cruzada", frame)
        else:
            #Link 1:
            p1a = origem[0]+(scale*solutions[0][3][0])
            p1b = h-origem[1]-(scale*solutions[0][3][1])
            p2a = origem[0]+(scale*solutions[0][0][0])
            p2b = h-origem[1]-(scale*solutions[0][0][1])
            cv.line(frame, (int(p1a), int(p1b)), (int(p2a), int(p2b)), (0, 255, 255), 15)
            #Link 2:
            p1a = origem[0]+(scale*solutions[0][0][0])
            p1b = h-origem[1]-(scale*solutions[0][0][1])
            p2a = origem[0]+(scale*solutions[0][1][0])
            p2b = h-origem[1]-(scale*solutions[0][1][1])
            cv.line(frame, (int(p1a), int(p1b)), (int(p2a), int(p2b)), (255, 0, 0), 15)
            #Link 3:
            p1a = origem[0]+(scale*solutions[0][1][0])
            p1b = h-origem[1]-(scale*solutions[0][1][1])
            p2a = origem[0]+(scale*solutions[0][2][0])
            p2b = h-origem[1]-(scale*solutions[0][2][1])
            cv.line(frame, (int(p1a), int(p1b)), (int(p2a), int(p2b)), (0, 255, 0), 15)
            #Link 4:
            p1a = origem[0]+(scale*solutions[0][2][0])
            p1b = h-origem[1]-(scale*solutions[0][2][1])
            p2a = origem[0]+(scale*solutions[0][3][0])
            p2b = h-origem[1]-(scale*solutions[0][3][1])
            cv.line(frame, (int(p1a), int(p1b)), (int(p2a), int(p2b)), (0, 0, 255), 15)
            cv.imshow("Configuracao Aberta", frame)
        
        cv.waitKey(dinamic*30)

var = 0
while True:
    kinematicsSolve(var%360, False, True, True)
    var += 1

#kinematicsSolve(30)