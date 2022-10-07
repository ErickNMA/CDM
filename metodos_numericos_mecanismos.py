#Importando as bibliotecas:
import math as m
import matplotlib.pyplot as plt

#Classe do mecanismo:
class Mechanism:
    #Construtor da classe, para definir o objeto do mecanismo, com o comprimento dos links:
    def __init__(self, L1, L2, L3, L4):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.L4 = L4

    #Método Algébrico (Norton):
    def nortonAngles(self, theta2, precision=4):
        self.theta2 = (theta2*m.pi/180)

        Ax = self.L2*m.cos(self.theta2)
        Ay = self.L2*m.sin(self.theta2)

        S = (((self.L2**2) - (self.L3**2) + (self.L4**2) - (self.L1**2))/(2*(Ax-self.L1)))
        P = (((Ay**2)/((Ax-self.L1)**2))+1)
        Q = ((2*Ay*(self.L1-S))/(Ax-self.L1))
        R = (((self.L1-S)**2) - (self.L4**2))        

        try:
            By1 = ((-Q+m.sqrt((Q**2)-(4*P*R)))/(2*P))
            By2 = ((-Q-m.sqrt((Q**2)-(4*P*R)))/(2*P))
            Bx1 = (S-((2*Ay*By1)/(2*(Ax-self.L1))))
            Bx2 = (S-((2*Ay*By2)/(2*(Ax-self.L1))))
        except:
            return None
        
        theta31 = m.atan((By1-Ay)/(Bx1-Ax))
        theta32 = m.atan((By2-Ay)/(Bx2-Ax))

        theta41 = m.atan(By1/(Bx1-self.L1))
        theta42 = m.atan(By2/(Bx2-self.L1))

        return [[round((theta31*180/m.pi), precision), round(((theta41*180/m.pi)+180), precision)], [round((theta32*180/m.pi), precision), round(((theta42*180/m.pi)-180), precision)]]

    #Método dos Laços de Vetores:
    def vectorsAngles(self, theta2, precision=4):
        self.theta2 = (theta2*m.pi/180)

        k1 = (self.L1/self.L2)
        k2 = (self.L1/self.L4)
        k3 = (((self.L2**2) - (self.L3**2) + (self.L4**2) + (self.L1**2))/(2*self.L2*self.L4))

        A = (m.cos(self.theta2) - k1 - (k2*m.cos(self.theta2)) + k3)
        B = (-2*m.sin(self.theta2))
        C = (k1 - ((k2+1)*m.cos(self.theta2)) + k3)

        try:
            theta41 = (2*m.atan((-B-m.sqrt((B**2)-(4*A*C)))/(2*A)))
            theta42 = (2*m.atan((-B+m.sqrt((B**2)-(4*A*C)))/(2*A)))
            theta31 = m.asin(((self.L4*m.sin(theta41))-(self.L2*m.sin(self.theta2)))/self.L3)
            theta32 = m.asin(((self.L4*m.sin(theta42))-(self.L2*m.sin(self.theta2)))/self.L3)
        except:
            return None

        return [[round((theta31*180/m.pi), precision), round((theta41*180/m.pi), precision)], [round((theta32*180/m.pi), precision), round((theta42*180/m.pi), precision)]]
    
    #Método de Newton-Raphson:
    def newtonAngles(self, theta2, chute_theta_3, chute_theta_4, precision=4):
        #Definição das constantes e variáveis:
        self.theta2 = (theta2*m.pi/180)+1e-15
        self.theta3 = (chute_theta_3*m.pi/180)+1e-15
        self.theta4 = (chute_theta_4*m.pi/180)+1e-15
        self.erro = (10**(-precision))
        self.f1 = self.erro
        self.f2 = self.erro

        i = 0
        it = []
        t3 = []
        t4 = []

        #Looping de repetição:
        while(True):
            #Definição das funções em malha fechada para ordenadas e abcissas:
            self.f1 = (self.L1 + (self.L4*m.cos(self.theta4)) - (self.L2*m.cos(self.theta2)) - (self.L3*m.cos(self.theta3)))
            self.f2 = ((self.L4*m.sin(self.theta4)) - (self.L2*m.sin(self.theta2)) - (self.L3*m.sin(self.theta3)))

            #Armazena os valores a cada iteração para plotagem:
            it.append(i)
            t3.append(self.theta3*180/m.pi)
            t4.append(self.theta4*180/m.pi)
            i = i+1

            #Confere erro:
            if((abs(self.f1) < self.erro) and (abs(self.f2) < self.erro)):
                break

            #Definição dos elementos da Matriz Jacobiana:
            self.d13 = (self.L3*m.sin(self.theta3))
            self.d14 = (-self.L4*m.sin(self.theta4))
            self.d23 = (-self.L3*m.cos(self.theta3))
            self.d24 = (self.L4*m.cos(self.theta4))

            #Definições das variações dos ângulos:
            try:
                self.delta4 = ((-self.f2+((self.d23*self.f1)/self.d13))/(self.d24-((self.d23*self.d14)/self.d13)))
                self.delta3 = ((-self.f1 - (self.d14*self.delta4))/self.d13)
            except:
                return None

            #Atualiza os valores dos Ângulos
            self.theta3 = (self.theta3 + self.delta3)
            self.theta4 = (self.theta4 + self.delta4)

        plt.plot(it, t3, 'red', label='theta3')
        plt.plot(it, t4, 'blue', label='theta4')
        plt.tick_params(labelsize=20)
        plt.ylabel('Ângulo (º)', fontsize=30)
        plt.xlabel('Iterações', fontsize=30)
        #plt.xlim(2400, 2520)
        plt.legend(fontsize=20)
        #plt.ylim(74, 81)
        #plt.title('Resposta ao degrau com 3 parâmetros (-5°)')
        plt.grid()
        plt.show()      

        return [round((self.theta3*180/m.pi), precision), round((self.theta4*180/m.pi), precision)]





fourlinks = Mechanism(180, 50, 150, 100)
#fourlinks = Mechanism(150, 60, 90, 120)
#fourlinks = Mechanism(18, 8, 20, 15)

angles = fourlinks.nortonAngles(30)
print('\n\n\n \t Método de Norton: \n \t Configuração Aberta: \t theta3: \t' + str(angles[0][0]) + ' \t theta4: \t' + str(angles[0][1]) + '\n \t Configuração Cruzada: \t theta3: \t' + str(angles[1][0]) + ' \t theta4: \t' + str(angles[1][1]))

angles = fourlinks.vectorsAngles(30)
print('\n\n\n \t Método dos Laços de Vetores: \n \t Configuração Aberta: \t theta3: \t' + str(angles[0][0]) + ' \t theta4: \t' + str(angles[0][1]) + '\n \t Configuração Cruzada: \t theta3: \t' + str(angles[1][0]) + ' \t theta4: \t' + str(angles[1][1]))

angles = [fourlinks.newtonAngles(30, 0, 50, 4), fourlinks.newtonAngles(30, 0, -50, 4)]
print('\n\n\n \t Método de Newton-Raphson: \n \t Configuração Aberta: \t theta3: \t' + str(angles[0][0]) + ' \t theta4: \t' + str(angles[0][1]) + '\n \t Configuração Cruzada: \t theta3: \t' + str(angles[1][0]) + ' \t theta4: \t' + str(angles[1][1]) + '\n\n\n')