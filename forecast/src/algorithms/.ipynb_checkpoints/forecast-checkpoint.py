from fbprophet import Prophet
from collections import Counter
import json
import os

class Forecast(object):
    """docstring for Forecast."""

    def __init__(self, inputMax=None, inputMin=0):
        with open(os.path.join(os.path.dirname(__file__),'holidays.json'),'r') as f:
            self.holidayJson = json.load(f)
        self.inputMax = inputMax
        self.inputMin = inputMin

    def holiday(self,data):
        dutyday_list = []
        holiday_list = []
        for year in self.holidayJson:
            dutyday_list.extend([year+'-'+k[:2]+'-'+k[2:] for k,v in self.holidayJson[year].items() if v==1])
            holiday_list.extend([year+'-'+k[:2]+'-'+k[2:] for k,v in self.holidayJson[year].items() if v==2])
        data['dutyday'] = data['ds'].apply(lambda x:1 if (str(x)[:10] in dutyday_list) else 0)
        data['holiday'] = data['ds'].apply(lambda x:1 if (str(x)[:10] in holiday_list) else 0)
        data['workday'] = data['ds'].apply(lambda x:0 if (str(x)[:10] in dutyday_list) or (str(x)[:10] in holiday_list) else 1)
        return data

    def timecut(self,data):
        df = data.copy()
        # df.sort_values(by='timestamp',inplace=True,ascending=True)
        time_list = list(df.timestamp)
        timecut_list = list(map(lambda x:x[0]-x[1],zip(time_list[1:],time_list[:-1])))
        timecut_dict = dict(Counter(timecut_list))
        timecut_max = max(timecut_dict, key=lambda k: timecut_dict[k])
        return timecut_max

    def forecast(self,data,days,timecut=None):
        train = data.copy()
        if not timecut:
            timecut_max = self.timecut(train)
        else:
            timecut_max = timecut
        train = self.holiday(train)
        ##拟合
        prophet = Prophet(weekly_seasonality=False,daily_seasonality=True)
        prophet.add_seasonality(name='dutyday',period=1,fourier_order=30,condition_name='dutyday')
        prophet.add_seasonality(name='holiday',period=1,fourier_order=30,condition_name='holiday')
        prophet.add_seasonality(name='workday',period=7,fourier_order=30,condition_name='workday')
        prophet.fit(train)
        ##待预测的时间点
        future = prophet.make_future_dataframe(periods = int(days*86400/timecut_max),freq=str(timecut_max)+'s')
        future = self.holiday(future)
        ##预测
        forecast = prophet.predict(future)
        ##数据调整
        if self.inputMin or self.inputMin==0:
            forecast['yhat'] = forecast['yhat'].apply(lambda x:x if x>self.inputMin else self.inputMin)
            forecast['yhat_lower'] = forecast['yhat_lower'].apply(lambda x:x if x>self.inputMin else self.inputMin)
            forecast['yhat_upper'] = forecast['yhat_upper'].apply(lambda x:x if x>self.inputMin else self.inputMin)
        if self.inputMax or self.inputMax==0:
            forecast['yhat'] = forecast['yhat'].apply(lambda x:x if x<self.inputMax else self.inputMax)
            forecast['yhat_lower'] = forecast['yhat_lower'].apply(lambda x:x if x<self.inputMax else self.inputMax)
            forecast['yhat_upper'] = forecast['yhat_upper'].apply(lambda x:x if x<self.inputMax else self.inputMax)
        return forecast
