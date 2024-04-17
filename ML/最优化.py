import numpy as np

def f(x):
    ''' 目标函数 '''
    x1 = x[0]
    x2 = x[1]
    y = 100*((x2-x1**2)**2)+(x1-1)**2
    return y

def num_grad(x,h):
    ''' 求梯度 '''
    df = np.zeros(x.size)
    for i in range(x.size):
        x1,x2 = x.copy(),x.copy()
        x1[i] = x[i] - h
        x2[i] = x[i] + h
        y1,y2 = f(x1),f(x2)
        df[i] = (y2-y1)/(2*h)
        return df
    
