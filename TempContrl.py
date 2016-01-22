# -*- coding: utf-8 -*-
"""
Created on Sat Nov 07 10:46:54 2015

@author: Kamyar
"""

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml import NetworkWriter
import numpy as np
import serial as ser
import thread
import scipy.sparse

data=ser.Serial('com7', 9600)

n=8; #number of sensors
M=10*np.identity(n)
M2=10*scipy.sparse.rand(1000, n, 0.5)
M2=M2.todense()
M2=np.asarray(M2)
settemp=650 # \set temprature of box in arbiturrary units from 0-1023
G=10;
target0=np.ones([1,n]) * settemp;
target=target0;
tolerance=1E-4;
er=np.zeros([1,n]);
Output=np.ones([1,n]);
power=np.ones([1,n]);
temp=np.zeros([1,n]);
lasttemp=np.zeros([1,n]);
dtemp=np.zeros([1,n]);
count=0;
s=-1;
traininginterval=100;
alpha=-1;

kd=-0.5;
kp=1;

net= buildNetwork(3*n,n*5,n);
ds = SupervisedDataSet(3*n,n);
trainer = BackpropTrainer(net, ds);


while (1==1):
    if (data.inWaiting()>0):
        s=s+1;
        mydata=data.readline()          #Reading serial data from Arduino
        if (s>2):

            lasttemp=temp;
            
            newdata = mydata.split(",")
            
            newdata=newdata[0:(n)]
            newdata=map(float,newdata)
            newdata=np.asarray(newdata)
            newdata[8]=settemp #remove this line when the missing sensor is connected
            # pin 8 is not connected to anything, therefore needs to be initialized as the set temp in order to keep the network sane. 
            
            print(newdata) 
            #if (s==1):
                #ds.clear();         #Clearing the initializations 
            
            for i in range(0,((len(newdata)+1)/n)):         #Making sure data points are not bunched together
                
                stor=newdata[ (n*i):((n*i)+(n-1)) ]
              #  R=10000*(11264*G+25*stor)/(14336*G-25*stor);
              #  temp= 0.00320822*np.power(R,4) - 0.52473409*np.power(R,3)  + 38.22403854*np.power(R,2) - 1566.33874662*R + 32214.23699140;
          #      temp=newdata;            
                dtempold=dtemp;
                dtemp=lasttemp-temp;
                
                x=np.concatenate([dtempold, temp, dtemp],axis=1);    
                count=count+1;
            if (s<50) and (s>1):
                ds.addSample(x,Output)
                thread.start_new_thread(trainer.trainEpochs, (5,))                    
                #Quick traning for first 50 data points
            
            if (count>=traininginterval) and (s<43200):         #Collecting Data
                ds.addSample(x,Output)
                thread.start_new_thread(trainer.trainEpochs, (10,))   
                count=0;
    
            elif (s==43200): # 43200 is the training time of roughly 12 hours, expressed in multiples of the 30 second sensor cycle
                ds.addSample(x,Output)
                thread.start_new_thread(trainer.trainEpochs, (1000,))          #Extra long training after data collection is done
                if (threading.activeCount()==0):        
                    NetworkWriter.writeToFile(net, 'network.xml')
    
    
                
            
            
            older=er;
            er=target-temp;         #calculating error
            der=older-er;
            if (np.absolute(np.mean(er)>2)):
                er=er/(np.mean(er)/2)
            vec=np.concatenate([dtemp, temp, er],axis=1); 
            vec=vec[0];
            Output=100*net.activate(vec);            #Calculaing the output using NN
            


                    
            if (np.min(np.absolute(er))<tolerance) and (s<43200):           #Chainging target temprature when training to collect more data
                if alpha==-1:
                    target=target0;
                    alpha=0;
                elif alpha==1:
                    target=target0+0.1;
                    alpha=-1;
                elif alpha==0:
                    target=target0-0.1;
                    alpha=1;


            if (s>400):
                Output=np.floor(Output)
                Output=map(int, Output)
            
            if (s<40):
                d=np.mod(s,n)
                Output=100*M[d,:]
            elif (s<400):
                d=np.mod(s,n)
                Output=100*M2[d,:]
                Output=map(int,Output)
                
            for k in range(0,len(Output)):
                if (Output[k]<0):
                    Output[k]=0
                if (Output[k]>1000):
                    Output[k]=1000
            output=' '.join(str(x) for x in Output)
            output='11111 '+ output+' '+ output
            print(Output)
            Output=map(float, Output)
            data.write(output)
            Output=np.array(Output)/100
        
            
        
            
        
