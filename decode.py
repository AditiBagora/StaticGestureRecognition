import wx
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import cv2
import imutils
import pyttsx3 
#import the newly created GUI_CODE file
import gui_code1
#importing * : to enable writing sin(13) instead of math.sin(13)
from math import *
 
#inherit from the MyFrame1 created in wxFowmBuilder and create CalcFrame
class MyFrame1(gui_code1.MyFrame2):
    #constructor
    def __init__(self,parent):
        #initialize parent class
        gui_code1.MyFrame2.__init__(self,parent)
    def decode_msg( self, event ):
        words=['Coin','Vehicle','Rock And Roll','Peace']
        codes=[[1,1,1,0],[1,1,0,0,0],[1,0.5,0.5,1,1],[1,1,0.5,0,0]]
        # load the image and convert it from BGR to RGB so that
        # we can dispaly it with matplotlib
        image_file_path=self.m_filePicker2.GetPath()
        image = cv2.imread(image_file_path)
        image = imutils.resize(image, width=600)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        data=[]  
        r=image.shape[0]
        c=image.shape[1]
        # reshape the image to be a list of pixels
        image1 = image.reshape((r*c, 3))
        k=2
        l=0
        # cluster the pixel intensities
        clt = KMeans(n_clusters = k)
        clt.fit(image1)
        labels = clt.labels_
        for i in range(r):
           for j in range(c):
               
               if labels[l]==0:
                 image[i][j]=(0,0,0)
               else:  
                 image[i][j]=(255,255,255)
               l=l+1
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        cnts,h = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
        cX=0
        cY=0
        bm=0
        flag=0
        for c in cnts:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            x,y,w,h=cv2.boundingRect(c)
            if h>w:
              vertical=1
            else:
              vertical=0
            M = cv2.moments(c)
            if vertical==0:
             if M["m00"]>100000:
               if M["m00"]<160000:
                 cX = int((M["m10"] / M["m00"]))
                 cY = int((M["m01"] / M["m00"]))
                 plt.scatter([cX],[cY])
                 cv2.drawContours(image,[c], -1, (100, 100, 100), 3)
                 bm=c
                 flag=1
            else:
              if M["m00"]>200000:
               if M["m00"]<280000:
                 cX = int((M["m10"] / M["m00"]))
                 cY = int((M["m01"] / M["m00"]))
                 plt.scatter([cX],[cY])
                 cv2.drawContours(image,[c], -1, (100, 100, 100), 3)
                 bm=c
                 flag=1
        cb=[]         
        d1=[]
        cbd=[]
        lt=100
        ut=200
        if flag==1:
           if vertical==1:
             plt.imshow(image)
             plt.scatter([cX],[cY])
             c=0
             e=0
             f=0
             j=0
             for i in bm[:,0]:
               c=c+1
             for i in range(c-1):
               g=bm[i]-bm[i+1]
               if g[:,0]>0:
                 d=g[:,1]/g[:,0]
                 if d>0:
                   f=0
                 else:
                   if flag==0:
                     f=f+1
                   flag=0
                 if f==10:
                     d1.append(bm[i-10,0])
             for i in d1:
                dist=cY-i[1]+cX-i[0]
                cbd.append(dist)
                plt.scatter([i[0]],[i[1]])
             for i in cbd:
                if ((i>lt)and(i<ut)):
                   cb.append(0.5)
                elif(i>ut):
                   cb.append(1)
                else:
                   if i<0:
                     cb.append(0)
             str1 = ''.join(str(e) for e in cb)
             self.m_textCtrl3.SetValue(str1)
             for i in codes:
                if cb==i:
                   break
                j=j+1
             self.m_textCtrl4.SetValue(words[j])
             plt.show()
             engine=pyttsx3.init('dummy')
             engine.say(words[j])
             engine.runAndWait()
           else:
             plt.imshow(image)
             plt.scatter([cX],[cY])
             c=0
             e=0
             f=0
             j=0
             for i in bm[:,0]:
               c=c+1
             
             
             for i in range(c-1):
               g=bm[i+1]-bm[i]
               
               if g[:,0]>0:
                  
                 d=g[:,1]/g[:,0]
                 
                 if d<0:
                   f=0
                 else:
                   if flag==0:
                     f=f+1
                   flag=0
                     
                 if f==8:
                     d1.append(bm[i-15,0])
                 
             for i in d1:
                dist=cY-i[1]+cX-i[0]
                cbd.append(dist)
                plt.scatter([i[0]],[i[1]])
             
             for i in cbd:
                if ((i>lt)and(i<ut)):
                   cb.append(0.5)
                elif(i>ut):
                   cb.append(1)
                else:
                   if i<0:
                     cb.append(0)
             str1 = ''.join(str(e) for e in cb)
             self.m_textCtrl3.SetValue(str1)
             for i in codes:
                if cb==i:
                   break
                j=j+1
             plt.show()
             self.m_textCtrl4.SetValue(words[j])
             engine=pyttsx3.init('dummy')
             engine.say(words[j]) 
             engine.runAndWait()
        else:
           print ("Cluster again")
        event.Skip()
#mandatory in wx, create an app, False stands for not deteriction stdin/stdout
app = wx.App(None)   
#create an object of CalcFrame
frame = MyFrame1(None)
#refer manual for details
 
#show the frame
frame.Show(True)
#start the applications
app.MainLoop()
