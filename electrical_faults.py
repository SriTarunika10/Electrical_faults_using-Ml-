# -*- coding: utf-8 -*-
"""Electrical faults

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e7l_5RZDI_D-okEQJwRFQxBhq-RAnOyK
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings

import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# Setup

sns.set_style('darkgrid')
plt.rcParams['figure.figsize'] = (12,9)
plt.rcParams['font.size'] = 20
warnings.filterwarnings('ignore')

binary_data = pd.read_csv('/content/detect_dataset.csv')
multi_data = pd.read_csv('/content/classData.csv')

binary_data.info()

multi_data.info()

#Exploratory Data Analysis - Binary Classification
binary_data.drop(binary_data.iloc[:,[7,8]], axis=1, inplace=True)
print(f'Number of Samples: {binary_data.shape[0]}\nNumber of Features: {binary_data.shape[1]}')

#Heat map
sns.heatmap(binary_data.corr(), annot=True, cmap='Blues')
plt.show()

plt.figure(figsize=(25,6))

a1 = plt.subplot2grid((1,3),(0,0))
a1.scatter(binary_data['Ia'], binary_data['Va'])
a1.set_title('Line a')
a1.set_xlabel('Ia')
a1.set_ylabel('Va')

a2 = plt.subplot2grid((1,3),(0,1))
a2.scatter(binary_data['Ib'], binary_data['Vb'])
a2.set_title('Line b')
a2.set_xlabel('Ib')
a2.set_ylabel('Vb')

a3 = plt.subplot2grid((1,3),(0,2))
a3.scatter(binary_data['Ic'], binary_data['Vc'])
a3.set_title('Line c')
a3.set_xlabel('Ic')
a3.set_ylabel('Vc')

plt.show()

#Composition of Target variable
binary_data['Output (S)'].value_counts()

plt.pie(x=binary_data['Output (S)'].value_counts(), labels=['No Fault', 'Fault'],
        explode = [0, 0.2], autopct= '%1.1f%%', labeldistance=1.15,
       colors=['#0c06c7', '#05daed'])
plt.show()

def dist(cola,colb):

    fig, axs = plt.subplots(ncols=2, nrows=1, figsize=(18,10))

    sns.distplot(binary_data[cola], label='Line Current', hist=True, color='#fc0328', ax=axs[0])
    sns.distplot(binary_data[colb], label='Line Voltage', hist=True, color='#0c06c7', ax=axs[1])

    axs[0].legend(loc='upper right', prop={'size': 12})
    axs[1].legend(loc='upper right', prop={'size': 12})

    plt.show()

lines = [
    ('Ia', 'Va'),
    ('Ib', 'Vb'),
    ('Ic', 'Vc')
]

for cola,colb in lines:
    dist(cola,colb)
    print('\n')

binary_data.isna().sum()

#Binary Classification Neural Network Model
binary_data.head()

y = binary_data.iloc[:,0]
X = binary_data.iloc[:,1:7]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

tf.random.set_seed(2)

model1 = keras.models.Sequential()

model1.add(keras.layers.Dense(6,
                              input_shape=(6,),
                              name='Input_layer',
                              activation='relu'))
model1.add(keras.layers.Dense(16,
                             name='Hidden_layer1',
                             activation='relu'))
model1.add(keras.layers.Dense(1,
                             name='Output_layer',
                             activation='sigmoid'))

model1.compile(
    loss=tf.keras.losses.binary_crossentropy,
    optimizer=tf.keras.optimizers.Adam(lr=0.03),
    metrics=[
        tf.keras.metrics.BinaryAccuracy(name='accuracy')
    ]
)

history = model1.fit(X_train, y_train, epochs=5, validation_split=0.2)

model1.summary()

history = pd.DataFrame(history.history)

plt.figure(figsize=(18,8))

a1 = plt.subplot2grid((1,2),(0,0))
a1.plot(history['accuracy'], label='Accuracy')
a1.set_title('Accuracy')

a2 = plt.subplot2grid((1,2),(0,1))
a2.plot(history['loss'], label='Loss')
a2.set_title('Loss')

plt.show()

y_pred = model1.predict(X_test)
y_pred.shape, y_test.shape

y_pred = np.where(y_pred>0.5, 1, 0)

print(f'Accuracy Score: {accuracy_score(y_test, y_pred)*100:.03f}%')
print(f'Precision Score: {precision_score(y_test, y_pred)*100:.03f}%')
print(f'Recall Score: {recall_score(y_test, y_pred)*100:.03f}%')

Accuracybinaryclassification= 95.502

confusion_matrix(y_test, y_pred)

print(classification_report(y_test, y_pred))

#Exploratory Data Analysis - Multiclass Classification
print(f'Number of Samples: {multi_data.shape[0]}\nNumber of Features: {multi_data.shape[1]}')

#Heat map
plt.figure(figsize=(18,12))
sns.heatmap(multi_data.corr(), annot=True, cmap='Blues')
plt.show()

plt.figure(figsize=(25,6))

a1 = plt.subplot2grid((1,3),(0,0))
a1.scatter(multi_data['Ia'], multi_data['Va'])
a1.set_title('Line a')
a1.set_xlabel('Ia')
a1.set_ylabel('Va')

a2 = plt.subplot2grid((1,3),(0,1))
a2.scatter(multi_data['Ib'], multi_data['Vb'])
a2.set_title('Line b')
a2.set_xlabel('Ib')
a2.set_ylabel('Vb')

a3 = plt.subplot2grid((1,3),(0,2))
a3.scatter(multi_data['Ic'], multi_data['Vc'])
a3.set_title('Line c')
a3.set_xlabel('Ic')
a3.set_ylabel('Vc')

plt.show()

def dist(cola,colb):

    fig, axs = plt.subplots(ncols=2, nrows=1, figsize=(18,10))

    sns.distplot(multi_data[cola], label='Line Current', hist=True, color='#fc0328', ax=axs[0])
    sns.distplot(multi_data[colb], label='Line Voltage', hist=True, color='#0c06c7', ax=axs[1])

    axs[0].legend(loc='upper right', prop={'size': 12})
    axs[1].legend(loc='upper right', prop={'size': 12})

    plt.show()

for cola, colb in lines:
    dist(cola,colb)
    print('\n')

multi_data.isna().sum()

#Multiclass Classification Neural Network Model
#Output: [G C B A]
#[0 0 0 0] - No Fault
#[1 0 0 1] - LG fault (Between Phase A and Ground)
#[0 0 1 1] - LL fault (Between Phase A and Phase B)
#[1 0 1 1] - LLG Fault (Between Phases A,B and Ground)
#[0 1 1 1] - LLL Fault (Between all three phases)
#[1 1 1 1] - LLLG fault (Three phase symmetrical fault)""

multi_data['faultType'] = multi_data['G'].astype(str) + multi_data['C'].astype(str) + multi_data['B'].astype(str) + multi_data['A'].astype(str)
multi_data.head()

plt.pie(multi_data['faultType'].value_counts(), autopct='%1.1f%%',
       labels=['No Fault', 'LLG Fault', 'LLLG Fault', 'LG Fault', 'LLL Fault', 'LL Fault'])
plt.show()

X = multi_data.drop(['G','C','B','A','faultType'], axis=1)
y = multi_data['faultType']

enc = LabelEncoder()
y = enc.fit_transform(y)

y = keras.utils.to_categorical(y, 6)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

tf.random.set_seed(2)

model2 = keras.models.Sequential()

model2.add(keras.layers.Dense(128,
                              input_shape=(6,),
                              name='Input_layer',
                              activation='relu'))
model2.add(keras.layers.Dense(240,
                              name='Hidden_layer1',
                              activation='relu'))
model2.add(keras.layers.Dense(240,
                              name='Hidden_layer2',
                              activation='tanh'))
model2.add(keras.layers.Dense(240,
                              name='Hidden_layer3',
                              activation='relu'))

model2.add(keras.layers.Dense(6,
                             name='output_layer',
                             activation='softmax'))

model2.compile(
    loss='categorical_crossentropy',
    metrics = ['accuracy']
)

model2.summary()

history = model2.fit(X_train, y_train, epochs=50, batch_size=64, validation_split=0.2)

history = pd.DataFrame(history.history)

plt.figure(figsize=(18,8))

a1 = plt.subplot2grid((1,2),(0,0))
a1.plot(history['accuracy'], label='Accuracy')
a1.set_title('Accuracy')

a2 = plt.subplot2grid((1,2),(0,1))
a2.plot(history['loss'], label='Loss')
a2.set_title('Loss')

plt.show()

y_pred_prob = model2.predict(X_test)
y_pred = np.argmax(y_pred_prob, axis=1)
y_test = np.argmax(y_test, axis=1)

y_test.shape, y_pred.shape

print(f'Accuracy Score : {accuracy_score(y_test, y_pred)*100:.03f}%')

AccuracyMulticlassification=75.461

print(classification_report(y_test, y_pred))

if (AccuracyMulticlassification<=Accuracybinaryclassification):
  print("Binary classification has the highest score than Multi classification:", Accuracybinaryclassification)
else:
  print("Multi classification has the highest score than  Binary classification:",AccuracyMulticlassification)

