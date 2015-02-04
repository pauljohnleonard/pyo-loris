

import loris, os, time
#import plotter
import sys

name='samples/clarinet'

  
a = loris.Analyzer( 270 )       # reconfigure Analyzer
a.setFreqDrift( 30 )

file=loris.AiffFile( name+'.aiff' )
v = file.samples()
samplerate=file.sampleRate()

parts = a.analyze( v, samplerate )
    

# loris.channelize( flut, loris.createFreqReference( flut, 291*.8, 291*1.2, 50 ), 1 )

refenv = a.fundamentalEnv()
loris.channelize( parts, refenv, 1 )
loris.distill( parts )
 
     
if True:
    cnt=0
    for part in parts:
        #print "*****************************************"
        #it=part.iterator()
        #while not it.atEnd():
        #    bp=it.next()
        #    print "t:",bp.time(), " a:",bp.amplitude()," bw:",bp.bandwidth()," f:",bp.frequency()," p:",bp.phase()
        cnt+=1
    print " There are ",cnt," Partials "
    
# sys.exit(0)
# plotter.plot(parts)

for part in parts:
    print "*****************************************"
    it=part.iterator()
    while not it.atEnd():
        bp=it.next()
        print "t:",bp.time(), " a:",bp.amplitude()," bw:",bp.bandwidth()," f:",bp.frequency()," p:",bp.phase()
    
loris.exportSpc(name+".spc",parts,60)
print "Done"

 