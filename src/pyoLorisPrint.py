import loris, os, time

import math
            
parts=loris.importSpc("flute.spc")




cnt=0
for part in parts:
    
        #print "*****************************************"
        #it=part.iterator()
        #while not it.atEnd():
        #    bp=it.next()
        #    print "t:",bp.time(), " a:",bp.amplitude()," bw:",bp.bandwidth()," f:",bp.frequency()," p:",bp.phase()
        cnt+=1
    print " There are ",cnt," Partials "
    
t=0

for part in parts:
   for bp in part:
       t=max(t,bp.time()) 
       
       


        
