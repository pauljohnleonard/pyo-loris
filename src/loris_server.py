from pyo import *
import time,gc
import atexit
import loris
from  pyoLorisSynth import *


class Thing:
    
    def __init__(self,name,size,sr,parts):
        self.size=size
        self.sr=44100
        self.name=name
        self.parts=parts
        
        
class Model:
    
    def __init__(self):
        self.thing=None
                   
        self.server = Server().boot().start()
        atexit.register(self.quit)

    def synth(self):   
        
        if self.thing == None:
            return
        thing=self.thing
        
        self.synth=LorisSynth(thing.parts,thing.sr,thing.size)
        self.synth.out()
 
       # time.sleep(10)
    
  
  
    def analyze(self,name,resolution=270,drift=30,lobe=270,floor=80):
        
        
#         name="clarinet.aiff"
 
        
        file=loris.AiffFile(name)
        samps  = file.samples()
        samplerate=file.sampleRate()
             
        print "analyse",resolution,drift,lobe
      
        anal=loris.Analyzer(resolution)    #  reso,lobe)       # reconfigure Analyzer
        anal.setFreqDrift(drift)       #  df )
     
 
        parts = anal.analyze( samps, samplerate )
            
        
        # loris.channelize( flut, loris.createFreqReference( flut, 291*.8, 291*1.2, 50 ), 1 )
        
        refenv = anal.fundamentalEnv()
        loris.channelize( parts, refenv, 1 )
        loris.distill( parts )
        loris.exportSpc(name+".spc",parts,60)
#         parts=loris.importSpc(name+".spc")
        
        
        self.thing=Thing(name,len(samps),samplerate,parts)

    def quit(self):
        self.server.stop()
    


model=Model()

if True:
  model.analyze(name='clarinet.aiff',drift=30,resolution=270,lobe=120,floor=80)
  model.synth()

time.sleep(10)
