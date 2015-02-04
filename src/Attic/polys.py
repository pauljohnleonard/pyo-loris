'''
Code snippet to plot multiple triangle's in Matplotlib using different methods.
'''
import time
import sys
import matplotlib.pyplot as pp
import random
 
if sys.platform == "win32":
     # On Windows, the best timer is time.clock()
     default_timer = time.clock 
else:     
    # On most other platforms the best timer is time.time()     
    default_timer = time.time
     
     
# generate ends for the triangle line segments
xtris = []
ytris = []
for i in range(1000):
    x1 = random.random()
    x2 = x1 + random.random()/5.0
    x3 = x1 + random.random()/5.0
    xtips = [x1,x2,x3]
    y1 = random.random()
    y2 = y1 + random.random()/5.0
    y3 = y1 + random.random()/5.0
    ytips = [y1,y2,y3]
    xtris.append(xtips)
    ytris.append(ytips)
 
############################
# time sequential call to matplotlib
pp.figure()
pp.subplot(1,3,1)
 
t0 = default_timer()
for xtips,ytips in zip(xtris,ytris):
    pp.fill(xtips,ytips,
            facecolor='b',alpha=0.1, edgecolor='none')
t1 = default_timer()
 
pp.title('Sequential Plotting')
 
print 'Execution time for sequential plotting = %f sec' % (t1-t0)
 
# rebuild ends using none to separate polygons
xlist = []
ylist = []
for xtips,ytips in zip(xtris,ytris):
    xlist.extend(xtips)
    xlist.append(None)
    ylist.extend(ytips)
    ylist.append(None)
 
############################
# build argument list
call_list = []
for xtips,ytips in zip(xtris,ytris):
    call_list.append(xtips)
    call_list.append(ytips)
    call_list.append('-b')
     
############################
# time single call to matplotlib
pp.subplot(1,3,2)
 
t0 = default_timer()
pp.fill(*call_list,
            facecolor='b',alpha=0.1, edgecolor='none')
 
t1 = default_timer()
 
pp.title('Single Plot extended call')
 
print 'Execution time for extended call plotting = %f sec' % (t1-t0)
 
     
############################
# time single call to matplotlib
pp.subplot(1,3,3)
 
t0 = default_timer()
pp.fill(xlist,ylist,
        facecolor='b',alpha=0.1,edgecolor='none')
t1 = default_timer()
 
pp.title('Single Plot Using None')
 
print 'Execution time when using None = %f sec' % (t1-t0)
 
pp.show()
