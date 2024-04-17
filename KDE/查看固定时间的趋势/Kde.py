import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import LeaveOneOut
#import scipy.signal as signal
import time
#from scipy import interpolate
import warnings
warnings.filterwarnings("ignore")

class Kdemodel:
    def __init__(self, file, timecut):
        self.file = file
        self.timecut = timecut
    
    def train_data(file, timecut):
        '''判断timecut是根据什么聚合'''
        data = pd.read_csv(file)
        data.columns = ['timestamp','value']
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        value = dict()
        if timecut == 'Day':
            data['date'] = data['timestamp'].dt.date
        elif timecut == 'Weekday':
            data['date'] = data['timestamp'].dt.weekday
        elif timecut == 'Hour':
            data['date'] = data['timestamp'].dt.hour
       
    
        newdata = data[['date','value']]
        newdata = newdata.groupby('date').mean()
        
        start = time.time()
        bandwidths = 10 ** np.linspace(-1,1,100)
        grid = GridSearchCV(KernelDensity(),{ 'bandwidth' : bandwidths, 'kernel' : ['gaussian','tophat','epanechnikov','exponential','linear','cosine']} ,cv =LeaveOneOut())
        grid.fit(newdata['value'].values.reshape(-1,1))
        end = time.time()
        print('running time of time = hour: '+ str((end - start)) +' s')
        
        kde = KernelDensity(kernel = grid.best_params_['kernel'], bandwidth = grid.best_params_['bandwidth']).fit(newdata['value'].values.reshape(-1,1))
        kde.score_samples(newdata['value'].values.reshape(-1,1))
        newdata['score'] = np.exp(kde.score_samples(newdata['value'].values.reshape(-1,1)))
        #newdata['score'] = kde.score_samples(newdata['value'].values.reshape(-1,1))  # 点x对应概率的log值
                
        return newdata