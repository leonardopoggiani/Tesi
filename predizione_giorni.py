# -*- coding: utf-8 -*-
"""predizione_giorni.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eef48YiFrLabbva696y4Py_CJRy5LYq6
"""

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import numpy as np
from pandas.tseries.offsets import DateOffset

df = pd.read_csv("dati_preprocessati.csv")
df.head()

plt.suptitle('Giorni anomali')

plotting = df.iloc[0:800]

plt.figure(figsize=(20,10))
plt.title("Serie temporali e giorni anomali")
plt.plot(plotting.index,plotting["Affluenza"],color="b",marker="o")
plt.plot(plotting.index,plotting["Anomalous"],color="r")

plt.show()

dataset = pd.read_csv('dati_preprocessati.csv', usecols=[1], engine='python')

plt.figure(figsize=(20,10))
plt.plot(dataset.iloc[0:800])
plt.plot()
plt.show()

train = dataset

scaler = MinMaxScaler()
scaler.fit(train)
train = scaler.transform(train)

n_input = 12
n_features = 1

generator = TimeseriesGenerator(train, train, length=n_input, batch_size=32)
model = Sequential()
model.add(LSTM(200, activation='relu', input_shape=(n_input, n_features)))
model.add(Dropout(0.15))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(generator, epochs=100)

pred_list = []

batch = train[-n_input:].reshape((1, n_input, n_features))
for i in range(n_input):
    pred_list.append(model.predict(batch)[0])
    batch = np.append(batch[:, 1:, :], [[pred_list[i]]], axis=1)

add_dates = [df.index[-1] + x for x in range(0, 13)]
future_dates = pd.DataFrame(index=add_dates[1:], columns=df.columns)

df_predict = pd.DataFrame(scaler.inverse_transform(pred_list), index=future_dates[-n_input:].index, columns=['Prediction'])

df_proj = pd.concat([df, df_predict], axis=1)
df_proj = df_proj.iloc[3500:]

plotting = df.iloc[3500:]

plt.figure(figsize=(20, 5))
plt.plot(df_proj.index, df_proj['Affluenza'])
plt.plot(df_proj.index, df_proj['Prediction'], color='g')
plt.plot(plotting.index,plotting["Anomalous"], color="r")
plt.legend(loc='best', fontsize='xx-large')
plt.xticks(fontsize=18)
plt.yticks(fontsize=16)
plt.show()