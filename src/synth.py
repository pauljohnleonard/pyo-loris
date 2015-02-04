import loris, os, time
from pyo import *
import math
   
CTRLS=True

class Synth:
    
    
    def __init__(self,feat):
        
        self.mixer=Mixer(outs=2, chnls=1).out()

        # these are arrays
        self.freqs=SigTo(value=feat.freq,time=1.0)       
        self.ampsNoise=SigTo(value=feat.noise,time=1.0)
        self.ampsTone=SigTo(value=feat.tone,time=1.0)
        
        
        if CTRLS:
            self.freqs.ctrl([SLMap(20., 2000., 'log', 'value',feat.freq)])
            self.ampsNoise.ctrl([SLMap(0.,1., 'lin', 'value',feat.noise)])
            self.ampsTone.ctrl([SLMap(0.,1., 'lin', 'value',feat.tone)])
        
        self.parts=PartialOsc(freq=self.freqs,ampTone=self.ampsTone,ampNoise=self.ampsNoise,scale=1.0/len(feat.freq))
       
        
        scale=1.0/len(feat.freq)
        osc=self.parts.osc
        
        for key in range(len(osc)):
        
        
            self.mixer.addInput(key,osc[key])
            self.mixer.setAmp(key,0,scale)
            self.mixer.setAmp(key,1,scale)          
       
        self.mixer.out()
       
       
    def setTarget(self,feat,time=None):
        """
        set the target for all the oscillators in terms of noise tone and freq.
        """
        if time != None:
            self.freqs.setTime(time)
            self.ampsNoise.setTime(time)
            self.ampsTone.setTime(time)
            
        self.freqs.setValue(feat.freq)
        self.ampsNoise.setValue(feat.noise)
        self.ampsTone.setValue(feat.tone)
        
        
        
class Feature:
    
    def __init__(self,fund):
        self.freq=[]
        self.noise=[]
        self.tone=[]
        
        self.freq=Feature.factory.harmonics(fund)
        
        for i in range(Feature.factory.n):
            self.noise.append(0.0)
            self.tone.append(1.0)
        
        
        
        
class Factory:
    
    def __init__(self,n):
        self.n=n
        
    def harmonics(self,fund):
        freqs=[]
        for i in range(self.n):
            freqs.append((i+1)*fund)
            
        return freqs
    
    def random_values(self,min=0,max=1.0):
        vals=[]
        for i in range(self.n):
            fact1=random.random()
            fact2=1.0-fact1
            
            vals.append(max*fact1+min*fact2)
            
        return vals
        
        
class PartialOsc:
    
    """
    Oscillator for a single Partial
    
    part is a loris Partial list.
    
    output(t)=(ampTone+ampNoise*LPF(whiteNoise)))*sin(freq*2*pi*t+phase)
 
    """
    
    def __init__(self,freq,ampTone,ampNoise,scale):
            
        init_phase=0
        
           
        self.white = Noise() 
        
        # low pass filter the noise 
        # loris uses 4 forward and back coeffecients but pyo only has a bi quad.
        # TODO implement general digital filter in pyo
        self.mod=Biquad(self.white, freq=500, q=1, type=0, mul=ampNoise, add=ampTone)
                                
        
        self.osc=Sine(freq=freq,mul=self.mod,phase=init_phase)
        
     
    def out(self):
        self.osc.out()
    
        


def process():





if __name__ == "__main__":
    s = Server().boot()

    spc_file="samples/clarinet.spc"
    parts=loris.importSpc(spc_file)

    n = len(parts)


    if True:
        cnt=0
        for part in parts:
            print "***************************************************"
            it=part.iterator()
            while not it.atEnd():
                bp=it.next()
                print "t:",bp.time(), " a:",bp.amplitude()," bw:",bp.bandwidth()," f:",bp.frequency()," p:",bp.phase()
                #
                break
            cnt+=1
        print " There are ",cnt," Partials "










    fMax=15000
    fund=100.0
 
    factory=Feature.factory=Factory(int(fMax/fund))
    
    feat=Feature(fund)
    synth=Synth(feat)
    
    s.start()
    
    dt=.2
    while True:
        time.sleep(dt)
        feat.tone=factory.random_values()
        
        synth.setTarget(feat,dt)
        time.sleep(.1)

    s.gui(locals())
        
