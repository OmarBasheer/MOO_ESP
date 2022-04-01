import numpy as np
import ssa as fun
import sys
import matplotlib.pyplot as plt

def main(argv):
    SearchAgents_no=100
    Function_name='F3'
    Max_iteration=1000
    [lb,ub,dim]=fun.Parameters(Function_name)
    [fMin,bestX,SSA_curve]=fun.SSA(SearchAgents_no,Max_iteration,lb,ub,dim,Function_name)
    print(['最优值为：',fMin])
    print(['最优变量为：',bestX])
    thr1=np.arange(len(SSA_curve[0,:]))

    plt.plot(thr1, SSA_curve[0,:])

    plt.xlabel('num')
    plt.ylabel('object value')
    plt.title('line')
    plt.show()
if __name__=='__main__':
	main(sys.argv)