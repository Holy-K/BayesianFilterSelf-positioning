

import numpy as np



class Bayesian():
    def __init__(self,t,map):
        self.t = t
        self.row = np.shape(map)[0]
        self.column = np.shape(map)[1]
        self.map = map
        self.f_s_tm1 = np.zeros((self.row,self.column))
        self.p_s_t_a_tm1 = np.zeros((self.row,self.column))
        self.p_o_t_s_t = np.zeros((self.row,self.column))
        self.g_s_t = np.zeros((self.row,self.column))
        self.f_s_t = np.zeros((self.row,self.column))
        

    def print_baysian(self):
        print("t=",self.t)
        print("F(s",self.t-1,") =\n",self.f_s_tm1)
        print("P(s",self.t,"|a",self.t-1,") =\n",self.p_s_t_a_tm1)
        print("P(o",self.t,"|s",self.t,") =\n",self.p_o_t_s_t)
        print("G(s",self.t,") =\n",self.g_s_t)        
        print("F(s",self.t,") =\n",self.f_s_t)        
        print("\n")

     #G(st)F(st)を計算
    def calcBayesian(self):    
        self.g_s_t = np.multiply(self.p_o_t_s_t , self.p_s_t_a_tm1)
        self.f_s_t = self.g_s_t / np.sum(self.g_s_t)  

    #観測結果otからP(ot|st)を計算(上,右,下,左)
    def observeReflection(self,observe):
        for i in range(self.row):
            for j in range(self.column):
                observe_compare = observe == self.map[i,j,:]
                if np.all(observe_compare ) == True:
                    self.p_o_t_s_t[i,j] = 0.7
                else:
                    self.p_o_t_s_t[i,j] = 0.02

    #行動at-1からP(st|at-1)を計算
    def actionReflection(self,direction):
        self.p_s_t_a_tm1 = self.f_s_tm1.copy() 
        if direction == "up":                       
            for i in range(self.row):
                for j in range(self.column):  
                    if self.map[i,j,0] == 0:                        
                        self.p_s_t_a_tm1[i,j] -= self.f_s_tm1[i,j].copy()  * 0.8   
                        self.p_s_t_a_tm1[i-1,j] += self.f_s_tm1[i,j].copy()  * 0.8

        elif direction == "right":
             for i in range(self.row):
                for j in range(self.column):
                    if self.map[i,j,1] == 0:   
                        self.p_s_t_a_tm1[i,j] = self.p_s_t_a_tm1[i,j] - self.f_s_tm1[i,j].copy() * 0.8
                        print("midle",self.f_s_tm1[i,j])
                        print("midle2",self.p_s_t_a_tm1[i-1,j])
                        self.p_s_t_a_tm1[i,j+1] += self.f_s_tm1[i,j].copy() * 0.8
                        print("after",self.f_s_tm1[i,j])
                        print("after2",self.p_s_t_a_tm1[i-1,j])

        elif direction == "down":
             for i in range(self.row):
                for j in range(self.column):
                    if self.map[i,j,2] == 0:
                        self.p_s_t_a_tm1[i,j] -= self.f_s_tm1[i,j].copy() * 0.8                 
                        self.p_s_t_a_tm1[i+1,j] += self.f_s_tm1[i,j].copy() * 0.8

        elif direction == "left":
             for i in range(self.row):
                for j in range(self.column):
                    if self.map[i,j,3] == 0:
                        self.p_s_t_a_tm1[i,j] -= self.f_s_tm1[i,j] * 0.8
                        self.p_s_t_a_tm1[i,j-1] += self.f_s_tm1[i,j] * 0.8
        else:
            print("error:Please input correct direction")

#結果を表示
def print_allBayesian():
    t1.print_baysian()
    t2.print_baysian()
    t3.print_baysian()
    t4.print_baysian()



#main--------------------------------------------------------------------
#mapの定義[上,右,下,左]0:壁無し,1:壁あり

map = [[[1,0,0,1],[1,0,1,0],[1,0,0,0],[1,1,1,0]],
       [[0,0,0,1],[1,1,0,0],[0,0,1,1],[1,1,0,0]],
       [[0,0,0,1],[0,0,0,0],[1,0,0,0],[0,1,0,0]],
       [[0,1,1,1],[0,0,1,1],[0,0,1,0],[0,1,1,0]]]


map2 = [[[1,0,0,1],[1,0,1,0],[1,1,0,0]],
       [[0,1,0,1],[1,0,0,1],[0,1,1,0]],
       [[0,0,1,1],[0,0,1,0],[1,1,1,0]]]
map = np.array(map)
observe = [[1,0,0,0],[0,0,0,0],[1,0,0,1],[0,0,0,1]]
observe2 = [[0,0,1,0],[1,0,0,1],[1,0,1,0],[1,1,0,0]]
observe = np.array(observe)

action = ["up","left","left","down"]
action2 = ["right","up","right","right"]

#インスタンス化(t,map)
t= np.zeros(4)
t1 = Bayesian(1,map)
t2 = Bayesian(2,map)
t3 = Bayesian(3,map)
t4 = Bayesian(4,map)

#calc t1
t1.f_s_tm1 = np.full((np.shape(map)[0],np.shape(map)[1]),0.0625)#初期条件F(s0)を設定(デフォルトは4x4等確率)
#t1.f_s_tm1 = np.array([[0.1,0.1,0.1],[0.1,0.2,0.1],[0.1,0.1,0.1]])

t1.observeReflection(observe[0])#観測結果otからP(ot|st)を計算
t1.actionReflection(action[0])#行動at-1からP(st|at-1)を計算
t1.calcBayesian()#G(st)F(st)を計算

#calc t2
t2.f_s_tm1 = t1.f_s_t
t2.observeReflection(observe[1])#観測結果otからP(ot|st)を計算
t2.actionReflection(action[1])#行動at-1からP(st|at-1)を計算
t2.calcBayesian()#G(st)F(st)を計算

#calc t3
t3.f_s_tm1 = t2.f_s_t
t3.observeReflection(observe[2])#観測結果otからP(ot|st)を計算
t3.actionReflection(action[2])#行動at-1からP(st|at-1)を計算
t3.calcBayesian()#G(st)F(st)を計算

#calc t4
t4.f_s_tm1 = t3.f_s_t
t4.observeReflection(observe[3])#観測結果otからP(ot|st)を計算
t4.actionReflection(action[3])#行動at-1からP(st|at-1)を計算
t4.calcBayesian()#G(st)F(st)を計算

#結果の表示（少数点以下4桁）
np.set_printoptions(precision=4,suppress=True)
print_allBayesian()
print(np.sum(t1.f_s_tm1))
print(np.sum(t1.f_s_t))
print(np.sum(t2.f_s_t))
print(np.sum(t3.f_s_t))
print(np.sum(t4.f_s_t))


