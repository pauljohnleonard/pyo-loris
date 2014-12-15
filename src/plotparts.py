from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
import loris
import threading,time


app = QtGui.QApplication([])
view = pg.GraphicsView()

l = pg.GraphicsLayout(border=(100,100,100))
view.setCentralItem(l)
view.show()
view.setWindowTitle('Partial-- display')
view.resize(1100,800)


parts_loris=loris.importSpc("clarinet.aiff.spc")
    
    
parts=[]


cnt=0
t=[]
v=[]
c=[]

on=False
for part in parts_loris:
  #print "*****************************************"
  it=part.iterator()
  
  while not it.atEnd():
      bp=it.next()
          
      if bp.amplitude() > 1e-5:
         t.append(bp.time())
         v.append(bp.frequency())
         if on:
            c.append(1)      
         on=True
      else:
        if on:
           c.append(0)
           on=False
        
  if on:
        c.append(0)
  on=False
      
  
print len(t),len(c)
  
  
tmax=0
for part in parts_loris:
   for bp in part:
       tmax=max(t,bp.time()) 

    
l.nextRow()
l2 = l.addLayout(colspan=1, border=(10,0,0))
l2.setContentsMargins(0, 0, 0, 10)

plot = l2.addPlot(title="FREQS")

#for x,y in zip(t,v):
#    print x,y,"|",

cc=np.array(c)

it=pg.PlotDataItem(t,v,connect=cc)

plot.addItem(it)
#plot.plot(t,v)
    
plot.showGrid(x=True,y=True,alpha=.9)

## Start Qt event loop unless running in interactive mode.

def runner():
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

if __name__ == '__main__':
    
    t = threading.Thread(target=runner)
    t.daemon = True
    t.start()

