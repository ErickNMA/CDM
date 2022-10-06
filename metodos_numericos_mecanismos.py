import math as m

class Mecanism:
    def __init__(self, L1, L2, L3, L4, theta2):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.L4 = L4
        self.theta2 = theta2

    def nortonAngles(self):
        Ax = self.L2*m.cos(self.theta2*m.pi/180.0)
        Ay = self.L2*m.sin(self.theta2*m.pi/180.0)

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

        angles = [[(theta31*180/m.pi), ((theta41*180/m.pi)+180)], [(theta32*180/m.pi), (180-(theta42*180/m.pi))]]

        return angles





#fourlinks = Mecanism(180, 50, 150, 100, 30)
fourlinks = Mecanism(150, 60, 90, 120, 120)

print(fourlinks.nortonAngles())