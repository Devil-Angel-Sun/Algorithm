import matplotlib.pyplot as plt
import numpy as np

def sigmoid(x):
    return 1.0/(1.0+np.exp(-x))

if __name__=='__main__':
    x = np.arange(-6,6,0.05)
    plt.plot(x, sigmoid(x))
    plt.axvline(x = 0.0, color = 'k')
    plt.axhline(y = 0.0, ls = 'dotted', color = 'k')
    plt.axhline(y = 0.5, ls = 'dotted', color = 'k')
    plt.axhline(y = 1.0, ls = 'dotted', color = 'k')
    plt.yticks([-0.1,0.5,1.0])
    plt.ylim(-0.1,1.1)
    plt.xlabel('z')
    plt.ylabel('$\phi (z)$')
    plt.show()