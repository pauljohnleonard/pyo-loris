from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
import loris

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
for part in parts_loris:
  t=[]
  v=[]
  #print "*****************************************"
  it=part.iterator()
  
  t=None
  
  while not it.atEnd():
      bp=it.next()
      
      if bp.amplitude() >1e-4:
         if not t:
             t=[]
             v=[]
         t.append(bp.time())
         v.append(bp.frequency())
      else:
          if t:     
              parts.append([t,v])
              cnt+=1
          t=None
 
  if t:        
    cnt+=1
    parts.append([t,v])
 
  if cnt > 400:
      break 
  
print " There are ",cnt," Partials "

t=0
for part in parts_loris:
   for bp in part:
       t=max(t,bp.time()) 

    
    
    
    
l.nextRow()
l2 = l.addLayout(colspan=1, border=(10,0,0))
l2.setContentsMargins(0, 0, 0, 10)

plot = l2.addPlot(title="FREQS")

for p in parts:
     plot.plot(p[0],p[1])
    
plot.showGrid(x=True,y=True,alpha=.9)

## Start Qt event loop unless running in interactive mode.

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
