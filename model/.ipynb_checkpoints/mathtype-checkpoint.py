import math
import numpy as np
def normal(x, mu, sigma):
    p = 1 / (math.sqrt(2 * math.pi) * sigma)
    return p * np.exp(- (x - mu) ** 2/(2 * sigma ** 2))
    

# 再次使用numpy进行可视化
x = np.arange(-7, 7, 0.01)

# 均值和标准差对
params = [(0, 1), (0, 2), (3, 1)]
d2l.plot(x, [normal(x, mu, sigma) for mu, sigma in params], xlabel='x',
         ylabel='p(x)', figsize=(4.5, 2.5),
         legend=[f'mean {mu}, std {sigma}' for mu, sigma in params])