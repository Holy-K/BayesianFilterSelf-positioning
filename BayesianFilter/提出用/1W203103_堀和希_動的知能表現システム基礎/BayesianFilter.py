

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
    def observeReflection(self,observe,observe_accuracy,observe_misrecognitionRate):
        for i in range(self.row):
            for j in range(self.column):
                observe_compare = observe == self.map[i,j,:]
                if np.all(observe_compare ) == True:
                    self.p_o_t_s_t[i,j] = observe_accuracy
                else:
                    self.p_o_t_s_t[i,j] = observe_misrecognitionRate

    #行動at-1からP(st|at-1)を計算
    def actionReflection(self,direction,action_slipRate):
        self.p_s_t_a_tm1 = self.f_s_tm1.copy() 
        if direction == "up":                       
            for i in range(self.row):
                for j in range(self.column):  
                    if self.map[i,j,0] == 0:                        
                        self.p_s_t_a_tm1[i,j] -= self.f_s_tm1[i,j].copy()  * (1-action_slipRate)   
                        self.p_s_t_a_tm1[i-1,j] += self.f_s_tm1[i,j].copy()  * (1-action_slipRate)  

        elif direction == "right":
             for i in range(self.row):
                for j in range(self.column):
                    if self.map[i,j,1] == 0:   
                        self.p_s_t_a_tm1[i,j] = self.p_s_t_a_tm1[i,j] - self.f_s_tm1[i,j].copy() * (1-action_slipRate)  
                        print("midle",self.f_s_tm1[i,j])
                        print("midle2",self.p_s_t_a_tm1[i-1,j])
                        self.p_s_t_a_tm1[i,j+1] += self.f_s_tm1[i,j].copy() * (1-action_slipRate)  
                        print("after",self.f_s_tm1[i,j])
                        print("after2",self.p_s_t_a_tm1[i-1,j])

        elif direction == "down":
             for i in range(self.row):
                for j in range(self.column):
                    if self.map[i,j,2] == 0:
                        self.p_s_t_a_tm1[i,j] -= self.f_s_tm1[i,j].copy() * (1-action_slipRate)                  
                        self.p_s_t_a_tm1[i+1,j] += self.f_s_tm1[i,j].copy() * (1-action_slipRate)  

        elif direction == "left":
             for i in range(self.row):
                for j in range(self.column):
                    if self.map[i,j,3] == 0:
                        self.p_s_t_a_tm1[i,j] -= self.f_s_tm1[i,j] * (1-action_slipRate)  
                        self.p_s_t_a_tm1[i,j-1] += self.f_s_tm1[i,j] * (1-action_slipRate)  
        else:
            print("error:Please input correct direction")

#結果をまとめて表示
def print_allBayesian():
    t1.print_baysian()
    t2.print_baysian()
    t3.print_baysian()
    t4.print_baysian()



#main

#設定1:mapの定義[上,右,下,左]0:壁無し,1:壁あり

map = [[[1,0,0,1],[1,0,1,0],[1,0,0,0],[1,1,1,0]],
       [[0,0,0,1],[1,1,0,0],[0,0,1,1],[1,1,0,0]],
       [[0,0,0,1],[0,0,0,0],[1,0,0,0],[0,1,0,0]],
       [[0,1,1,1],[0,0,1,1],[0,0,1,0],[0,1,1,0]]]
map = np.array(map)

#設定2:観測結果を定義[上,右,下,左]0:壁無し,1:壁あり
observe = [[1,0,0,0],[0,0,0,0],[1,0,0,1],[0,0,0,1]]
observe = np.array(observe)
observe_accuracy = 0.7#観測の精度を定義
observe_misrecognitionRate = 0.02 #誤認識が生じる確率を定義

#設定3:行動を定義
action = ["up","left","left","down"]
action_slipRate = 0.2 #スリップが生じて動けない確率を定義

#インスタンス化(t,map)
t1 = Bayesian(1,map)
t2 = Bayesian(2,map)
t3 = Bayesian(3,map)
t4 = Bayesian(4,map)

#設定4：初期条件F(s0)を定義(デフォルトは4x4等確率)
t1.f_s_tm1 = np.full((np.shape(map)[0],np.shape(map)[1]),0.0625)


#calc t1
t1.observeReflection(observe[0],observe_accuracy,observe_misrecognitionRate)#観測結果otからP(ot|st)を計算
t1.actionReflection(action[0],action_slipRate)#行動at-1からP(st|at-1)を計算
t1.calcBayesian()#G(st)F(st)を計算

#calc t2
t2.f_s_tm1 = t1.f_s_t
t2.observeReflection(observe[1],observe_accuracy,observe_misrecognitionRate)#観測結果otからP(ot|st)を計算
t2.actionReflection(action[1],action_slipRate)#行動at-1からP(st|at-1)を計算
t2.calcBayesian()#G(st)F(st)を計算

#calc t3
t3.f_s_tm1 = t2.f_s_t
t3.observeReflection(observe[2],observe_accuracy,observe_misrecognitionRate)#観測結果otからP(ot|st)を計算
t3.actionReflection(action[2],action_slipRate)#行動at-1からP(st|at-1)を計算
t3.calcBayesian()#G(st)F(st)を計算

#calc t4
t4.f_s_tm1 = t3.f_s_t
t4.observeReflection(observe[3],observe_accuracy,observe_misrecognitionRate)#観測結果otからP(ot|st)を計算
t4.actionReflection(action[3],action_slipRate)#行動at-1からP(st|at-1)を計算
t4.calcBayesian()#G(st)F(st)を計算

#結果の表示（少数点以下4桁、階乗表示off）
np.set_printoptions(precision=4,suppress=True)
print_allBayesian()

#Enterkeyで終了
while True:
       key = input(' Enterキーを押したら終了します')
       if not key:
           break
