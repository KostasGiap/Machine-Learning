import numpy as np
import random
import sys


class Probability(object):
    def __init__(self, N, t):
        self.N = N 
        self.t = t + 1
        self.a = self.InitTableA()
        self.v = self.InitTableV()
        self.e = np.array([1,3,1])
        self.B =  np.zeros((self.N, self.t), dtype=float)
        self.ev =  np.array([0,1,1])
        self.Bv =  np.zeros((self.N, self.t), dtype=float)

        
    
    def InitTableA(self):
        A = np.zeros((self.N, self.t), dtype=float)
        for i in range(self.N):
            p = random.random()
            if p <= 0.25: A[i][0] = 1
            elif p > 0.25 and p <= 0.5  : A[i][0] = 2
            elif p > 0.5  and p <= 0.75 : A[i][0] = 3
            elif p > 0.75 and p <= 1.0  : A[i][0] = 4
        return A
            
    def InitTableV(self):
        v = np.zeros((self.N, self.t), dtype=int)
        t = 1
        while t < self.t:
            v = self.Vt(v_table=v, t=t)
            t += 1
        return v
    
    def Vt(self, v_table, t):
        for i in range(self.N):
            p = random.random()
            if v_table[i][t-1] == -1:
                if p <= 0.7 : v_table[i][t] = -1
                elif p > 0.7: v_table[i][t] = 0
            elif v_table[i][t-1] == 0:
                if p <= 0.25 : v_table[i][t] = -1
                elif p > 0.25 and p <= 0.75: v_table[i][t] = 0
                else: v_table[i][t] = 1
            elif v_table[i][t-1] == 1:
                if p <= 0.3 : v_table[i][t] = 0
                elif p > 0.3 and p <= 1.0: v_table[i][t] = 1
        return v_table
    
    def FillTableA(self):
        self.P = np.zeros((self.N), dtype=float)
        t = 1
        while t < self.t:
            for i in range(self.N):
                p = random.random()
                if self.a[i][t-1] == 1 and self.v[i][t-1] == -1:
                    if p <= 0.2 : self.a[i][t] = 1
                    elif p > 0.2 and p <= 0.3 : self.a[i][t] = 2
                    elif p > 0.3 and p <= 1.0 : self.a[i][t] = 4

                elif self.a[i][t-1] == 1 and self.v[i][t-1] == 0:
                    if p <= 0.6 : self.a[i][t] = 1
                    elif p > 0.6 and p <= 0.8 : self.a[i][t] = 2
                    elif p > 0.8 and p <= 1.0 : self.a[i][t] = 4
                
                elif self.a[i][t-1] == 1 and self.v[i][t-1] == 1:
                    if p <= 0.2 : self.a[i][t] = 1
                    elif p > 0.2 and p <= 0.9 : self.a[i][t] = 2
                    elif p > 0.9 and p <= 1.0 : self.a[i][t] = 4
                
                elif self.a[i][t-1] == 2 and self.v[i][t-1] == -1:
                    if p <= 0.7: self.a[i][t] = 1
                    elif p > 0.7 and p <= 0.9 : self.a[i][t] = 2
                    elif p > 0.9 and p <= 1.0 : self.a[i][t] = 3
                
                elif self.a[i][t-1] == 2 and self.v[i][t-1] == 0:
                    if p <= 0.2 : self.a[i][t] = 1
                    elif p > 0.2 and p <= 0.8 : self.a[i][t] = 2
                    elif p > 0.8 and p <= 1.0 : self.a[i][t] = 3
                
                elif self.a[i][t-1] == 2 and self.v[i][t-1] == 1:
                    if p <= 0.1 : self.a[i][t] = 1
                    elif p > 0.1 and p <= 0.3 : self.a[i][t] = 2
                    elif p > 0.3 and p <= 1.0 : self.a[i][t] = 3
                
                elif self.a[i][t-1] == 3 and self.v[i][t-1] == -1:
                    if p <= 0.7: self.a[i][t] = 2
                    elif p > 0.7 and p <= 0.9 : self.a[i][t] = 3
                    elif p > 0.9 and p <= 1.0 : self.a[i][t] = 4
                
                elif self.a[i][t-1] == 3 and self.v[i][t-1] == 0:
                    if p <= 0.2 : self.a[i][t] = 2
                    elif p > 0.2 and p <= 0.8 : self.a[i][t] = 3
                    elif p > 0.8 and p <= 1.0 : self.a[i][t] = 4
                
                elif self.a[i][t-1] == 3 and self.v[i][t-1] == 1:
                    if p <= 0.1 : self.a[i][t] = 2
                    elif p > 0.1 and p <= 0.3 : self.a[i][t] = 3
                    elif p > 0.3 and p <= 1.0 : self.a[i][t] = 4
                
                elif self.a[i][t-1] == 4 and self.v[i][t-1] == -1:
                    if p <= 0.1: self.a[i][t] = 1
                    elif p > 0.1 and p <= 0.8 : self.a[i][t] = 3
                    elif p > 0.8 and p <= 1.0 : self.a[i][t] = 4
                
                elif self.a[i][t-1] == 4 and self.v[i][t-1] == 0:
                    if p <= 0.2 : self.a[i][t] = 1
                    elif p > 0.2 and p <= 0.4 : self.a[i][t] = 3
                    elif p > 0.4 and p <= 1.0 : self.a[i][t] = 4
                
                elif self.a[i][t-1] == 4 and self.v[i][t-1] == 1:
                    if p <= 0.7 : self.a[i][t] = 1
                    elif p > 0.7 and p <= 0.8 : self.a[i][t] = 3
                    elif p > 0.8 and p <= 1.0 : self.a[i][t] = 4
                    
            if t < self.t-1:
                s = self.InitWeights(t)
                self.Resample(s)
            t += 1
        return self.a

    def InitWeights(self, t):
        s = 0
        for i in range(self.N):
            if self.a[i][t-1] == 1:
                if self.e[t-1] == 1: self.P[i] = 0.5
                elif self.e[t-1] == 2: self.P[i] = 0.2
                elif self.e[t-1] == 3: self.P[i] = 0.1
                elif self.e[t-1] == 4: self.P[i] = 0.2
            elif self.a[i][t-1] == 2:
                if self.e[t-1] == 1: self.P[i] = 0.2
                elif self.e[t-1] == 2: self.P[i] = 0.5
                elif self.e[t-1] == 3: self.P[i] = 0.2
                elif self.e[t-1] == 4: self.P[i] = 0.1
            elif self.a[i][t-1] == 3:
                if self.e[t-1] == 1: self.P[i] = 0.1
                elif self.e[t-1] == 2: self.P[i] = 0.2
                elif self.e[t-1] == 3: self.P[i] = 0.5
                elif self.e[t-1] == 4: self.P[i] = 0.2
            elif self.a[i][t-1] == 4:
                if self.e[t-1] == 1: self.P[i] = 0.2
                elif self.e[t-1] == 2: self.P[i] = 0.1
                elif self.e[t-1] == 3: self.P[i] = 0.2
                elif self.e[t-1] == 4: self.P[i] = 0.5
            s += self.P[i]
        return s
    
    def Resample(self, s):
        for i in range(self.N):
            p = s * random.random()
            ts = 0
            j = 0
            while ts < p:
                ts = ts + self.P[j]
                j += 1
            j = j-1
            for k in range(self.t):
                self.B[i][k] = self.a[j][k]
        for i in range(self.N):
            for j in range(self.t):

                self.a[i][j] = self.B[i][j]
            
    
    def Calculate(self):
        P2 = np.zeros((self.t-1), dtype=float)
        P3 = np.zeros((self.t-1), dtype=float)
        P4 = np.zeros((self.t-1), dtype=float)
        for i in range(self.N):
            P2[int(self.a[i][2])-1] += 1
            P3[int(self.a[i][3])-1] += 1
            P4[int(self.a[i][4])-1] += 1
        return P2, P3, P4
    

    def VtWithWeights(self):
        v = np.zeros((self.N, self.t), dtype=int)
        self.P = np.zeros((self.N), dtype=float)
        t = 1
        while t < self.t:
            v = self.Vt(v, t)
            if t < self.t-1:
                s = self.AddWeightsV(v, t)
                v = self.ResampleV(v, s)
            t += 1
        return v
    
    def AddWeightsV(self, v, t):
        s = 0
        for i in range(self.N):
            if v[i][t-1] == -1:
                if self.ev[t-1] == -1: self.P[i] = 0.7
                elif self.ev[t-1] == 0: self.P[i] = 0.2
                elif self.ev[t-1] == 1: self.P[i] = 0.1
            elif v[i][t-1] == 0:
                if self.ev[t-1] == -1: self.P[i] = 0.25
                elif self.ev[t-1] == 0: self.P[i] = 0.5
                elif self.ev[t-1] == 1: self.P[i] = 0.25
            elif v[i][t-1] == 1:
                if self.ev[t-1] == -1: self.P[i] = 0.1
                elif self.ev[t-1] == 0: self.P[i] = 0.2
                elif self.ev[t-1] == 1: self.P[i] = 0.7
            s += self.P[i]
        return s
    
    def ResampleV(self, v, s):
        for i in range(self.N):
            p = s * random.random()
            ts = 0
            j = 0
            while ts < p:
                ts = ts + self.P[j]
                j += 1
            j = j-1
            for k in range(self.t):
                self.Bv[i][k] = v[j][k]
        for i in range(self.N):
            for j in range(self.t):
                v[i][j] = self.Bv[i][j]
        return v
    
    def CalculateV(self, v):
        P2 = np.zeros((3), dtype=float)
        P3 = np.zeros((3), dtype=float)
        P4 = np.zeros((3), dtype=float)
        for i in range(self.N):
            P2[int(v[i][2])-1] += 1
            P3[int(v[i][3])-1] += 1
            P4[int(v[i][4])-1] += 1
        return P2, P3, P4


        


def main():
    print "[*] Calculating relocation through N={0} iterations...".format(N)
    p.FillTableA()
    P2, P3, P4 = p.Calculate()
    print "P(X2|e1:3) = ({0}, {1}, {2}, {3})".format(P2[0]/N, P2[1]/N, P2[2]/N, P2[3]/N)
    print "P(X3|e1:3) = ({0}, {1}, {2}, {3})".format(P3[0]/N, P3[1]/N, P3[2]/N, P3[3]/N)
    print "P(X4|e1:3) = ({0}, {1}, {2}, {3})".format(P4[0]/N, P4[1]/N, P4[2]/N, P4[3]/N)
    print "\n"

    print "[*] Calculating velocity through N={0} iterations...".format(N)
    v = p.VtWithWeights()
    P2, P3, P4 = p.CalculateV(v)
    print "P(V2|e1:3) = ({0}, {1}, {2})".format(P2[0]/N, P2[1]/N, P2[2]/N)
    print "P(V3|e1:3) = ({0}, {1}, {2})".format(P3[0]/N, P3[1]/N, P3[2]/N)
    print "P(V4|e1:3) = ({0}, {1}, {2})".format(P4[0]/N, P4[1]/N, P4[2]/N)


if __name__ == "__main__":
    N = 10000
    p = Probability(N, t=4)
    main()

    

    
    